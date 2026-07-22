from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.job import Job, JobStatus
from app.models.resume_history import ResumeHistory
from app.models.user import User
from app.services.job_match_service import JobMatchService


router = APIRouter(prefix="/jobs", tags=["Jobs"])


def _resume_skills(db: Session, user_id: int) -> list[str]:
    history = (
        db.query(ResumeHistory)
        .filter(ResumeHistory.user_id == user_id)
        .order_by(ResumeHistory.uploaded_at.desc())
        .first()
    )
    if not history or not history.extracted_skills:
        return []
    return [skill.strip() for skill in history.extracted_skills.split(",") if skill.strip()]


def _job_response(job: Job, match: dict) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "department": job.department or "",
        "employment_type": job.employment_type or "",
        "url": job.url,
        "description": job.description,
        "status": job.status.value,
        "posted_date": job.created_at,
        "match_percentage": match["match_percentage"],
        "matched_skills": match["matched_skills"],
        "missing_skills": match["missing_skills"],
    }


@router.get("/")
def get_jobs(
    keyword: str = Query(""),
    title: str = Query(""),
    company: str = Query(""),
    location: str = Query(""),
    department: str = Query(""),
    employment_type: str = Query(""),
    required_skills: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    status: str = Query("ACTIVE"),
    sort: str = Query("newest"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Job)
    if status != "ALL":
        query = query.filter(Job.status == JobStatus(status) if status in JobStatus._value2member_map_ else JobStatus.ACTIVE)

    for value, field in (
        (keyword, (Job.title, Job.company, Job.location, Job.department, Job.employment_type)),
        (title, (Job.title,)),
        (company, (Job.company,)),
        (location, (Job.location,)),
        (department, (Job.department,)),
        (employment_type, (Job.employment_type,)),
    ):
        value = value.strip()
        if value:
            query = query.filter(or_(*(column.ilike(f"%{value}%") for column in field)))
    for skill in (value.strip() for value in required_skills.split(",")):
        if skill:
            query = query.filter(Job.description.ilike(f"%{skill}%"))

    if sort == "company":
        query = query.order_by(Job.company.asc())
    elif sort == "title":
        query = query.order_by(Job.title.asc())
    else:
        query = query.order_by(Job.created_at.asc() if sort == "oldest" else Job.created_at.desc())

    total = query.count()
    jobs = query.offset((page - 1) * page_size).limit(page_size).all()
    matcher = JobMatchService()
    resume_skills = _resume_skills(db, user.id)
    matches = [matcher.match_job(resume_skills, job) for job in jobs]
    if sort == "match":
        pairs = sorted(zip(jobs, matches), key=lambda pair: pair[1]["match_percentage"], reverse=True)
    else:
        pairs = zip(jobs, matches)

    total_pages = max(1, (total + page_size - 1) // page_size)
    return {
        "count": len(jobs),
        "total_count": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "jobs": [_job_response(job, match) for job, match in pairs],
    }
