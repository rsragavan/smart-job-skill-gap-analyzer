import hashlib
import logging
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.config import settings
from app.core.security import get_current_user
from app.models.resume_history import ResumeHistory
from app.models.user import User
from app.repositories.resume_history_repository import ResumeHistoryRepository
from app.resume.resume_parser import ResumeParser
from app.resume.skill_extractor import SkillExtractor
from app.services.job_recommendation_service import JobRecommendationService
from app.services.resume_history_service import ResumeHistoryService
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
    if file.content_type != "application/pdf" or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Only PDF resumes are accepted")
    content = await file.read()
    if not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=415, detail="Invalid PDF file")
    if len(content) == 0 or len(content) > settings.MAX_RESUME_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="Resume must be between 1 byte and 5 MB")
    digest = hashlib.sha256(content).hexdigest()
    existing = db.query(ResumeHistory).filter_by(user_id=user.id, content_hash=digest).first()
    if existing:
        raise HTTPException(status_code=409, detail="This resume was already uploaded")

    safe_name = f"{uuid4().hex}.pdf"
    file_path = UPLOAD_DIR / safe_name

    with open(file_path, "wb") as buffer:

        buffer.write(content)

    parser = ResumeParser()

    text = parser.extract_text(str(file_path))

    extractor = SkillExtractor()

    resume_skills = extractor.extract_skills(text, db=db)

    recommendation_service = JobRecommendationService()

    jobs = recommendation_service.recommend_jobs(
        resume_skills
    )

    try:

        repository = ResumeHistoryRepository(db)

        history_service = ResumeHistoryService(repository)

        history_service.save_history(
            filename=file.filename,
            skills=resume_skills,
            recommended_jobs=jobs,
            user_id=user.id,
            content_hash=digest,
        )
        db.commit()
    except Exception:
        if file_path.exists(): file_path.unlink()
        raise

    return {
        "filename": file.filename,
        "resume_skills": resume_skills,
        "recommended_jobs": jobs
    }


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
            "skills": item.extracted_skills.split(", "),
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
