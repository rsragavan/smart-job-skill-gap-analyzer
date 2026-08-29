import hashlib
import logging
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile, Query
from fastapi.responses import StreamingResponse
from io import BytesIO
import json
import fitz
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.config import settings
from app.core.security import get_current_user
from app.models.resume_history import ResumeHistory
from app.models.user import User
from app.models.user_target import UserTarget
from app.models.job import Job
from app.repositories.resume_history_repository import ResumeHistoryRepository
from app.resume.resume_parser import ResumeParseError, ResumeParser
from app.resume.skill_extractor import SkillExtractor
from app.services.job_recommendation_service import JobRecommendationService
from app.services.resume_history_service import ResumeHistoryService
from app.services.ats_resume_service import ats_resume_service
from app.services.job_match_service import JobMatchService
from fastapi import HTTPException

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    filename = file.filename or ""
    if file.content_type != "application/pdf" or not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Only PDF resumes are accepted")
    content = await file.read(settings.MAX_RESUME_SIZE_BYTES + 1)
    if len(content) > settings.MAX_RESUME_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="Resume exceeds the maximum allowed size")
    if not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=415, detail="Invalid PDF file")
    digest = hashlib.sha256(content).hexdigest()
    existing = db.query(ResumeHistory).filter_by(user_id=user.id, content_hash=digest).first()
    if existing:
        raise HTTPException(status_code=409, detail="This resume was already uploaded")

    safe_name = f"{uuid4().hex}.pdf"
    file_path = UPLOAD_DIR / safe_name

    try:
        file_path.write_bytes(content)
        text = ResumeParser().extract_text(str(file_path))
        resume_skills = SkillExtractor().extract_skills(text, db=db)
        jobs = JobRecommendationService().recommend_jobs(resume_skills)
        target = db.query(UserTarget).filter_by(user_id=user.id, is_active=True).order_by(UserTarget.updated_at.desc()).first()
        target_job = db.get(Job, target.job_id) if target and target.job_id else None
        if target:
            refreshed_match = JobMatchService().match_job(resume_skills, target_job) if target_job else JobMatchService().match_text(resume_skills, target.job_description or "", company=target.company, role=target.role_title)
            target.match_percentage = refreshed_match["match_percentage"]
            target.matched_skills = refreshed_match["matched_skills"]
            target.missing_skills = refreshed_match["missing_skills"]
        ats_report = ats_resume_service.analyze(text, resume_skills, target_role=target.role_title if target else None, target_company=target.company if target else None, job_description=target_job.description if target_job else target.job_description if target else None, target_missing_skills=list(target.missing_skills or []) if target else None)
        repository = ResumeHistoryRepository(db)
        history_service = ResumeHistoryService(repository)
        history = history_service.save_history(
            filename=filename,
            skills=resume_skills,
            recommended_jobs=jobs,
            user_id=user.id,
            content_hash=digest,
            ats_analysis=ats_report,
            storage_path=str(file_path),
        )
        logger.info("Resume processed successfully for user_id=%s", user.id)
    except ResumeParseError as exc:
        if file_path.exists():
            file_path.unlink()
        logger.warning("Resume parsing failed for user_id=%s: %s", user.id, exc)
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except (OSError, SQLAlchemyError) as exc:
        if file_path.exists():
            file_path.unlink()
        logger.exception("Resume processing failed for user_id=%s", user.id)
        raise HTTPException(status_code=422, detail="Resume could not be processed") from exc
    except Exception:
        if file_path.exists():
            file_path.unlink()
        logger.exception("Unexpected resume processing failure for user_id=%s", user.id)
        raise

    return {
        "filename": filename,
        "resume_id": history.id,
        "resume_skills": resume_skills,
        "recommended_jobs": jobs
        ,"ats_report": ats_report
    }


@router.get("/ats-report/latest")
def latest_ats_report(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(ResumeHistory).filter_by(user_id=user.id).order_by(ResumeHistory.uploaded_at.desc()).first()
    if item is None or not item.ats_analysis:
        raise HTTPException(status_code=404, detail="No ATS report is available. Upload a resume first.")
    return {"resume_id": item.id, "filename": item.filename, "uploaded_at": item.uploaded_at, "ats_report": item.ats_analysis}


@router.get("/ats-report/{history_id}")
def ats_report(history_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(ResumeHistory).filter_by(id=history_id, user_id=user.id).first()
    if item is None or not item.ats_analysis:
        raise HTTPException(status_code=404, detail="ATS report not found.")
    return {"resume_id": item.id, "filename": item.filename, "uploaded_at": item.uploaded_at, "ats_report": item.ats_analysis}


@router.get("/ats-report/{history_id}/export")
def export_ats_report(history_id: int, report_type: str = Query(default="ats"), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(ResumeHistory).filter_by(id=history_id, user_id=user.id).first()
    if item is None or not item.ats_analysis:
        raise HTTPException(status_code=404, detail="ATS report not found.")
    report = item.ats_analysis
    sections = {"ats": ("ATS Resume Report", report), "skill-gap": ("Skill Gap Report", report.get("skill_gap", {})), "preparation": ("Preparation Report", report.get("improvements", {})), "feedback": ("Resume Feedback", report.get("improvements", {}))}
    title, body = sections.get(report_type, sections["ats"])
    document = fitz.open()
    page = document.new_page()
    text = f"{title}\n\nResume: {item.filename}\nOverall Score: {report.get('overall_score', 'Not Available')}/100\n\n{json.dumps(body, indent=2, default=str)}"
    page.insert_text((50, 60), text[:8000], fontsize=9)
    payload = document.tobytes()
    document.close()
    return StreamingResponse(BytesIO(payload), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={report_type}-{item.id}.pdf"})


@router.get("/history")
def get_resume_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = ResumeHistoryRepository(db)
    try:
        history = repository.get_all_for_user(user.id)
    except SQLAlchemyError as exc:
        logger.exception("Unable to load resume history for user_id=%s", user.id)
        raise HTTPException(status_code=500, detail="Unable to load resume history") from exc

    return [
        {
            "id": item.id,
            "filename": item.filename,
            "skills": [skill for skill in item.extracted_skills.split(", ") if skill],
            "recommended_jobs": item.recommended_jobs,
            "uploaded_at": item.uploaded_at
        }
        for item in history
    ]


@router.delete("/history/{history_id}")
def delete_resume_history(history_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    repository = ResumeHistoryRepository(db)
    history = repository.get_by_id_for_user(history_id, user.id)

    if history is None:
        raise HTTPException(status_code=404, detail="Resume history not found")

    # Existing records used original filenames; never interpolate user-controlled paths.
    file_path = UPLOAD_DIR / Path(history.filename).name
    try:
        if file_path.exists():
            file_path.unlink()
    except OSError:
        pass

    repository.delete(history)

    return {"status": "deleted"}
