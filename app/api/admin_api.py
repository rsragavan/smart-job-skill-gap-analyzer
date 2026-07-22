import asyncio

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.models.job import Job, JobStatus
from app.models.company import Company
from app.models.resume_history import ResumeHistory
from app.models.user import Role, User
from app.models.unknown_skill import UnknownSkill
from app.services.technical_skills_engine import skills_engine

router = APIRouter(prefix="/admin", tags=["Administration"])
admin_only = require_roles(Role.ADMIN)


@router.get("/stats")
def stats(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    last_sync = db.query(Company.last_scraped_at).order_by(Company.last_scraped_at.desc()).first()
    return {
        "users": db.query(User).count(),
        "active_users": db.query(User).filter(User.is_active.is_(True)).count(),
        "resumes": db.query(ResumeHistory).count(),
        "jobs": db.query(Job).count(),
        "active_jobs": db.query(Job).filter(Job.status == JobStatus.ACTIVE).count(),
        "inactive_jobs": db.query(Job).filter(Job.status == JobStatus.INACTIVE).count(),
        "last_synchronization": last_sync[0] if last_sync else None,
    }


@router.get("/users")
def users(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    return [{
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role.value,
        "is_active": user.is_active,
        "created_at": user.created_at,
    } for user in db.query(User).order_by(User.created_at.desc()).all()]


@router.get("/resumes")
def resumes(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    users_by_id = {user.id: user.email for user in db.query(User).all()}
    return [{
        "id": resume.id,
        "filename": resume.filename,
        "uploaded_at": resume.uploaded_at,
        "user_id": resume.user_id,
        "user_email": users_by_id.get(resume.user_id, "Unknown"),
    } for resume in db.query(ResumeHistory).order_by(ResumeHistory.uploaded_at.desc()).all()]


@router.get("/jobs")
def jobs(status: JobStatus = Query(default=JobStatus.ACTIVE), _: User = Depends(admin_only), db: Session = Depends(get_db)):
    return [{
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "url": job.url,
        "status": job.status.value,
        "inactive_at": job.inactive_at,
    } for job in db.query(Job).filter(Job.status == status).order_by(Job.id.desc()).all()]


@router.get("/skills/pending")
def pending_skills(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    return [{"id": skill.id, "skill_name": skill.skill_name, "source": skill.source, "frequency": skill.frequency, "first_seen": skill.first_seen, "last_seen": skill.last_seen} for skill in db.query(UnknownSkill).filter(UnknownSkill.status == "pending").order_by(UnknownSkill.frequency.desc(), UnknownSkill.last_seen.desc()).all()]


@router.post("/skills/{skill_id}/approve")
def approve_skill(skill_id: int, _: User = Depends(admin_only), db: Session = Depends(get_db)):
    skill = db.get(UnknownSkill, skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="Unknown skill not found")
    skill.status = "approved"
    skills_engine.add_skill(skill.skill_name)
    db.commit()
    return {"id": skill.id, "skill_name": skill.skill_name, "status": skill.status}


@router.post("/skills/{skill_id}/reject")
def reject_skill(skill_id: int, _: User = Depends(admin_only), db: Session = Depends(get_db)):
    skill = db.get(UnknownSkill, skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="Unknown skill not found")
    skill.status = "rejected"
    db.commit()
    return {"id": skill.id, "skill_name": skill.skill_name, "status": skill.status}


sync_router = APIRouter(tags=["Administration"])


@sync_router.post("/jobs/sync")
async def sync_jobs(request: Request, _: User = Depends(admin_only)):
    try:
        scheduler = getattr(request.app.state, "job_scheduler", None)
        if scheduler is not None:
            return await scheduler.run_once()
        from app.scheduler.job_scheduler import sync_jobs_in_worker
        return await asyncio.to_thread(sync_jobs_in_worker)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Job synchronization failed") from exc
