import asyncio
import csv
import io
import secrets
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.models.job import Job, JobStatus
from app.models.company import Company
from app.models.resume_history import ResumeHistory
from app.models.user import Role, User
from app.models.unknown_skill import UnknownSkill
from app.models.company_intelligence import StartupInformation
from app.models.company_intelligence import CompanyInterviewQuestion, CompanyRole, CompanySelectionProcess
from app.models.job_application import JobApplication
from app.models.mock_interview import MockInterview
from app.models.learning_progress import LearningProgress
from app.models.user_target import UserTarget
from app.models.admin import AdminActivityLog, SystemSetting
from app.core.security import hash_password
from app.schemas.company_intelligence import StartupUpsert
from app.services.technical_skills_engine import skills_engine
from app.services.verified_import_service import company_import_service, startup_import_service
from app.services.company_intelligence_service import company_intelligence_service
from app.services.startup_ingestion_service import startup_ingestion_service

router = APIRouter(prefix="/admin", tags=["Administration"])
admin_only = require_roles(Role.ADMIN)


@router.post("/import/companies")
def import_verified_companies(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    return company_import_service.import_all(db)


@router.post("/import/startups")
def import_verified_startups_catalog(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    return startup_import_service.import_all(db)


@router.post("/startups/ingest")
def ingest_startups(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    return startup_ingestion_service.ingest(db)


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
        "companies": db.query(Company).count(),
        "startups": db.query(StartupInformation).count(),
        "applications": db.query(JobApplication).count(),
        "target_companies": db.query(UserTarget).filter(UserTarget.is_active.is_(True)).count(),
        "mock_interviews": db.query(MockInterview).count(),
        "learning_progress": db.query(LearningProgress).filter(LearningProgress.status == "completed").count(),
        "most_applied_companies": _counts(db.query(JobApplication).all(), "custom_company_name"),
        "most_popular_roles": _counts(db.query(JobApplication).all(), "custom_job_title"),
        "recent_registrations": [_user_summary(item) for item in db.query(User).order_by(User.created_at.desc()).limit(8).all()],
        "recent_applications": [{"id": item.id, "company": item.custom_company_name, "role": item.custom_job_title, "status": item.status, "applied_at": item.applied_at} for item in db.query(JobApplication).order_by(JobApplication.applied_at.desc()).limit(8).all()],
        "last_synchronization": last_sync[0] if last_sync else None,
    }


@router.get("/startup-diagnostics")
def startup_diagnostics(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    startups = db.query(StartupInformation).all()
    counts = company_intelligence_service._job_counts(db, startups)
    payload = [company_intelligence_service._startup_payload(item, counts.get(company_intelligence_service._normalized(item.name))) for item in startups]
    duplicate_groups: dict[str, list[int]] = {}
    for item in startups:
        duplicate_groups.setdefault(company_intelligence_service._normalized(item.name), []).append(item.id)
    return {
        "startup_count": len(payload),
        "verified_startup_count": sum(item["verified"] for item in payload),
        "startup_with_funding": sum(bool(item["funding_stage"] or item["latest_funding_amount"]) for item in payload),
        "startup_with_founders": sum(bool(item["founders"]) for item in payload),
        "startup_with_technology": sum(bool(item["tech_stack"]) for item in payload),
        "startup_with_open_roles": sum(item["open_roles"] is not None and item["open_roles"] > 0 for item in payload),
        "startup_with_careers_url": sum(bool(item["careers_url"]) for item in payload),
        "startup_with_verification_source": sum(bool(item["source_url"]) for item in payload),
        "duplicate_groups": [ids for ids in duplicate_groups.values() if len(ids) > 1],
    }


@router.get("/company-diagnostics")
def company_diagnostics(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    counts = company_intelligence_service._company_job_counts(db, companies)
    payload = [company_intelligence_service._company_payload(item, counts.get(company_intelligence_service._normalized(item.name))) for item in companies]
    duplicate_groups: dict[str, list[dict]] = {}
    for item in payload:
        duplicate_groups.setdefault(company_intelligence_service._normalized(item["name"]), []).append({"id": item["id"], "name": item["name"], "website_url": item["website_url"], "country": item["country"], "verification_status": item["verification_status"]})
    return {
        "company_count": len(payload),
        "verified_company_count": sum(item["verified"] for item in payload),
        "unverified_company_count": sum(item["verification_status"] == "Unverified" for item in payload),
        "unknown_company_count": sum(item["verification_status"] == "Unknown" for item in payload),
        "with_website": sum(bool(item["website_url"]) for item in payload),
        "with_careers_url": sum(bool(item["career_url"]) for item in payload),
        "with_verification_source": sum(bool(item["data_source_url"]) for item in payload),
        "with_technology": sum(bool(item["tech_stack"]) for item in payload),
        "with_products": sum(bool(item["products"]) for item in payload),
        "with_hiring_status": sum(bool(item["hiring_status"]) for item in payload),
        "with_active_jobs": sum(item["open_roles"] is not None and item["open_roles"] > 0 for item in payload),
        "duplicate_groups": [items for items in duplicate_groups.values() if len(items) > 1],
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


def _user_summary(user: User) -> dict:
    return {"id": user.id, "full_name": user.full_name, "email": user.email, "role": user.role.value, "is_active": user.is_active, "created_at": user.created_at, "last_login": user.last_login}


def _counts(rows, field: str) -> list[dict]:
    counts: dict[str, int] = {}
    for row in rows:
        value = getattr(row, field, None)
        if value:
            counts[value] = counts.get(value, 0) + 1
    return [{"name": name, "count": count} for name, count in sorted(counts.items(), key=lambda pair: pair[1], reverse=True)[:10]]


class UserUpdate(BaseModel):
    role: Role | None = None
    is_active: bool | None = None


class CompanyUpsert(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    career_url: str = ""
    greenhouse_token: str | None = None
    industry: str | None = None
    headquarters: str | None = None
    country: str | None = None
    website_url: str | None = None
    public_email: str | None = None
    tech_stack: str | None = None
    hiring_status: str | None = None
    remote_policy: str | None = None
    description: str | None = None


class VerificationUpdate(BaseModel):
    verified: bool
    verification_source: str | None = None


class JobUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    status: JobStatus | None = None


def _audit(db: Session, admin: User, action: str, resource: str, resource_id: int | None = None, detail: str | None = None) -> None:
    db.add(AdminActivityLog(admin_user_id=admin.id, action=action, resource=resource, resource_id=resource_id, detail=detail))


@router.get("/users/manage")
def manage_users(search: str | None = None, role: Role | None = None, active: bool | None = None, page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100), _: User = Depends(admin_only), db: Session = Depends(get_db)):
    query = db.query(User)
    if search: query = query.filter((User.full_name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%")))
    if role: query = query.filter(User.role == role)
    if active is not None: query = query.filter(User.is_active.is_(active))
    total = query.count(); rows = query.order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": [_user_summary(item) for item in rows], "page": page, "page_size": page_size, "total": total}


@router.patch("/users/{user_id}")
def update_user(user_id: int, payload: UserUpdate, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(User, user_id)
    if not row: raise HTTPException(404, "User not found")
    if row.id == admin.id and payload.is_active is False: raise HTTPException(400, "Administrators cannot deactivate themselves")
    if payload.role is not None: row.role = payload.role
    if payload.is_active is not None: row.is_active = payload.is_active
    _audit(db, admin, "update", "user", row.id); db.commit(); db.refresh(row)
    return _user_summary(row)


@router.delete("/users/{user_id}")
def delete_user(user_id: int, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(User, user_id)
    if not row: raise HTTPException(404, "User not found")
    if row.id == admin.id: raise HTTPException(400, "Administrators cannot delete themselves")
    _audit(db, admin, "delete", "user", row.id); db.delete(row); db.commit()
    return {"deleted": user_id}


@router.post("/users/{user_id}/reset-password")
def reset_user_password(user_id: int, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(User, user_id)
    if not row: raise HTTPException(404, "User not found")
    temporary_password = secrets.token_urlsafe(12)
    row.password_hash = hash_password(temporary_password); _audit(db, admin, "update", "user", row.id, "password reset"); db.commit()
    return {"user_id": row.id, "temporary_password": temporary_password}


@router.get("/users/{user_id}/activity")
def user_activity(user_id: int, _: User = Depends(admin_only), db: Session = Depends(get_db)):
    if not db.get(User, user_id): raise HTTPException(404, "User not found")
    return [{"type": "application", "id": item.id, "status": item.status, "created_at": item.applied_at} for item in db.query(JobApplication).filter_by(user_id=user_id).order_by(JobApplication.applied_at.desc()).limit(100).all()]


@router.get("/companies")
def admin_companies(search: str | None = None, page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100), _: User = Depends(admin_only), db: Session = Depends(get_db)):
    query = db.query(Company)
    if search: query = query.filter(Company.name.ilike(f"%{search}%"))
    total = query.count(); rows = query.order_by(Company.name).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": [{"id": item.id, "name": item.name, "career_url": item.career_url, "industry": item.industry, "hiring_status": item.hiring_status, "is_active": item.is_active} for item in rows], "total": total, "page": page}


@router.get("/companies/unverified")
def unverified_companies(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    return [{"id": item.id, "name": item.name, "website_url": item.website_url, "career_url": item.career_url, "verification_status": item.verification_status, "data_source_url": item.data_source_url, "last_verified_at": item.last_verified_at} for item in db.query(Company).filter(Company.verification_status != "Verified").order_by(Company.name).all()]


@router.get("/startups/unverified")
def unverified_startups(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    return [{"id": item.id, "name": item.name, "website_url": item.website_url, "careers_url": item.careers_url, "verification_status": "Verified" if item.source_url and item.last_verified_at else "Unverified", "source_url": item.source_url, "last_verified_at": item.last_verified_at} for item in db.query(StartupInformation).filter((StartupInformation.source_url.is_(None)) | (StartupInformation.last_verified_at.is_(None))).order_by(StartupInformation.name).all()]


@router.patch("/companies/{company_id}/verification")
def update_company_verification(company_id: int, payload: VerificationUpdate, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(Company, company_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Company not found")
    source = (payload.verification_source or row.data_source_url or row.website_url or row.career_url) if payload.verified else payload.verification_source
    if payload.verified and not source:
        raise HTTPException(status_code=422, detail="A verification source is required before marking a company verified")
    row.verification_status = "Verified" if payload.verified else "Unverified"
    row.data_source_url = source
    row.last_verified_at = datetime.now(UTC) if payload.verified else None
    _audit(db, admin, "verify" if payload.verified else "unverify", "company", row.id, source)
    db.commit()
    return {"id": row.id, "verification_status": row.verification_status, "verified": payload.verified, "data_source_url": row.data_source_url, "last_verified_at": row.last_verified_at}


@router.patch("/startups/{startup_id}/verification")
def update_startup_verification(startup_id: int, payload: VerificationUpdate, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(StartupInformation, startup_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Startup not found")
    source = (payload.verification_source or row.source_url or row.website_url or row.careers_url) if payload.verified else payload.verification_source
    if payload.verified and not source:
        raise HTTPException(status_code=422, detail="A verification source is required before marking a startup verified")
    row.source_url = source
    row.last_verified_at = datetime.now(UTC) if payload.verified else None
    _audit(db, admin, "verify" if payload.verified else "unverify", "startup", row.id, source)
    db.commit()
    return {"id": row.id, "verification_status": "Verified" if payload.verified else "Unverified", "verified": payload.verified, "source_url": row.source_url, "last_verified_at": row.last_verified_at}


@router.post("/companies")
def create_company(payload: CompanyUpsert, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    if db.query(Company).filter(Company.name.ilike(payload.name.strip())).first(): raise HTTPException(409, "Company already exists")
    row = Company(name=payload.name.strip(), greenhouse_token=payload.greenhouse_token or f"admin-{secrets.token_hex(8)}", career_url=payload.career_url or payload.website_url or "", **payload.model_dump(exclude={"name", "greenhouse_token", "career_url"}))
    db.add(row); db.flush(); _audit(db, admin, "create", "company", row.id); db.commit(); db.refresh(row)
    return {"id": row.id, "name": row.name}


@router.patch("/companies/{company_id}")
def update_company(company_id: int, payload: CompanyUpsert, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(Company, company_id)
    if not row: raise HTTPException(404, "Company not found")
    values = payload.model_dump(exclude={"greenhouse_token"}, exclude_unset=True)
    for key, value in values.items(): setattr(row, key, value)
    if payload.greenhouse_token: row.greenhouse_token = payload.greenhouse_token
    _audit(db, admin, "update", "company", row.id); db.commit(); return {"id": row.id, "name": row.name}


@router.delete("/companies/{company_id}")
def delete_company(company_id: int, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(Company, company_id)
    if not row: raise HTTPException(404, "Company not found")
    _audit(db, admin, "delete", "company", row.id); db.delete(row); db.commit(); return {"deleted": company_id}


@router.delete("/startups/{startup_id}")
def delete_startup(startup_id: int, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(StartupInformation, startup_id)
    if not row: raise HTTPException(404, "Startup not found")
    _audit(db, admin, "delete", "startup", row.id); db.delete(row); db.commit(); return {"deleted": startup_id}


class RolePayload(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None
    is_open: bool = False
    required_skills: str | None = None


class ProcessPayload(BaseModel):
    round_number: int = Field(ge=1)
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None
    expected_duration: str | None = None
    difficulty: str | None = None
    interview_mode: str | None = None
    preparation_topics: str | None = None


class QuestionPayload(BaseModel):
    company_role_id: int
    category: str = "Technical"
    question: str = Field(min_length=3)
    difficulty: str | None = None
    preparation_tip: str | None = None


@router.post("/companies/{company_id}/roles")
def create_company_role(company_id: int, payload: RolePayload, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    if not db.get(Company, company_id): raise HTTPException(404, "Company not found")
    row = CompanyRole(company_id=company_id, **payload.model_dump()); db.add(row); db.flush(); _audit(db, admin, "create", "company_role", row.id); db.commit(); return {"id": row.id, "title": row.title}


@router.patch("/company-roles/{role_id}")
def update_company_role(role_id: int, payload: RolePayload, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(CompanyRole, role_id)
    if not row: raise HTTPException(404, "Company role not found")
    for key, value in payload.model_dump().items(): setattr(row, key, value)
    _audit(db, admin, "update", "company_role", row.id); db.commit(); return {"id": row.id, "title": row.title}


@router.delete("/company-roles/{role_id}")
def delete_company_role(role_id: int, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(CompanyRole, role_id)
    if not row: raise HTTPException(404, "Company role not found")
    _audit(db, admin, "delete", "company_role", row.id); db.delete(row); db.commit(); return {"deleted": role_id}


@router.post("/company-roles/{role_id}/rounds")
def create_hiring_round(role_id: int, payload: ProcessPayload, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    if not db.get(CompanyRole, role_id): raise HTTPException(404, "Company role not found")
    row = CompanySelectionProcess(company_role_id=role_id, **payload.model_dump()); db.add(row); db.flush(); _audit(db, admin, "create", "hiring_round", row.id); db.commit(); return {"id": row.id, "title": row.title}


@router.patch("/hiring-rounds/{round_id}")
def update_hiring_round(round_id: int, payload: ProcessPayload, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(CompanySelectionProcess, round_id)
    if not row: raise HTTPException(404, "Hiring round not found")
    for key, value in payload.model_dump().items(): setattr(row, key, value)
    _audit(db, admin, "update", "hiring_round", row.id); db.commit(); return {"id": row.id, "title": row.title}


@router.delete("/hiring-rounds/{round_id}")
def delete_hiring_round(round_id: int, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(CompanySelectionProcess, round_id)
    if not row: raise HTTPException(404, "Hiring round not found")
    _audit(db, admin, "delete", "hiring_round", row.id); db.delete(row); db.commit(); return {"deleted": round_id}


@router.post("/interview-questions")
def create_interview_question(payload: QuestionPayload, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    if not db.get(CompanyRole, payload.company_role_id): raise HTTPException(404, "Company role not found")
    row = CompanyInterviewQuestion(**payload.model_dump()); db.add(row); db.flush(); _audit(db, admin, "create", "interview_question", row.id); db.commit(); return {"id": row.id, "question": row.question}


@router.patch("/interview-questions/{question_id}")
def update_interview_question(question_id: int, payload: QuestionPayload, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(CompanyInterviewQuestion, question_id)
    if not row: raise HTTPException(404, "Interview question not found")
    for key, value in payload.model_dump().items(): setattr(row, key, value)
    _audit(db, admin, "update", "interview_question", row.id); db.commit(); return {"id": row.id, "question": row.question}


@router.delete("/interview-questions/{question_id}")
def delete_interview_question(question_id: int, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(CompanyInterviewQuestion, question_id)
    if not row: raise HTTPException(404, "Interview question not found")
    _audit(db, admin, "delete", "interview_question", row.id); db.delete(row); db.commit(); return {"deleted": question_id}


@router.patch("/jobs/{job_id}")
def update_job(job_id: int, payload: JobUpdate, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(Job, job_id)
    if not row: raise HTTPException(404, "Job not found")
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(row, key, value)
    row.inactive_at = datetime.now(UTC) if row.status == JobStatus.INACTIVE else None
    _audit(db, admin, "update", "job", row.id); db.commit(); return {"id": row.id, "status": row.status.value}


@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(Job, job_id)
    if not row: raise HTTPException(404, "Job not found")
    _audit(db, admin, "delete", "job", row.id); db.delete(row); db.commit(); return {"deleted": job_id}


@router.get("/audit")
def audit_logs(page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=200), _: User = Depends(admin_only), db: Session = Depends(get_db)):
    query = db.query(AdminActivityLog); total = query.count(); rows = query.order_by(AdminActivityLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": [{"id": item.id, "admin_user_id": item.admin_user_id, "action": item.action, "resource": item.resource, "resource_id": item.resource_id, "detail": item.detail, "created_at": item.created_at} for item in rows], "total": total}


@router.get("/settings")
def settings(_: User = Depends(admin_only), db: Session = Depends(get_db)):
    return [{"key": item.key, "value": item.value, "updated_at": item.updated_at} for item in db.query(SystemSetting).order_by(SystemSetting.key).all()]


@router.put("/settings/{key}")
def update_setting(key: str, value: str, admin: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(SystemSetting, key) or SystemSetting(key=key); row.value = value; row.updated_by = admin.id; db.add(row); _audit(db, admin, "update", "setting", detail=key); db.commit(); return {"key": key, "value": value}


@router.get("/export/{resource}")
def export_resource(resource: str, format: str = Query("json", pattern="^(json|csv)$"), _: User = Depends(admin_only), db: Session = Depends(get_db)):
    models = {"companies": Company, "startups": StartupInformation, "jobs": Job, "users": User}
    model = models.get(resource)
    if model is None: raise HTTPException(404, "Export resource not supported")
    rows = db.query(model).limit(5000).all(); data = [{column.name: getattr(row, column.name) for column in model.__table__.columns} for row in rows]
    if format == "json": return data
    output = io.StringIO(); writer = csv.DictWriter(output, fieldnames=list(data[0]) if data else [column.name for column in model.__table__.columns]); writer.writeheader(); writer.writerows(data)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={resource}.csv"})


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


def _save_startup(db: Session, payload: StartupUpsert, startup: StartupInformation | None = None) -> StartupInformation:
    row = startup or StartupInformation(name=payload.name.strip(), industry=payload.industry.strip(), location=payload.location.strip())
    for field in ("industry", "location", "state", "description", "funding_stage", "latest_funding_amount", "website_url", "careers_url", "public_email", "tech_stack", "hiring_status", "open_positions", "source_url"):
        setattr(row, field, getattr(payload, field))
    if startup is None: db.add(row)
    db.commit(); db.refresh(row); return row


@router.post("/startups")
def create_startup(payload: StartupUpsert, _: User = Depends(admin_only), db: Session = Depends(get_db)):
    if db.query(StartupInformation).filter_by(name=payload.name.strip()).first(): raise HTTPException(status_code=409, detail="Startup already exists")
    return _save_startup(db, payload)


@router.patch("/startups/{startup_id}")
def update_startup(startup_id: int, payload: StartupUpsert, _: User = Depends(admin_only), db: Session = Depends(get_db)):
    row = db.get(StartupInformation, startup_id)
    if not row: raise HTTPException(status_code=404, detail="Startup not found")
    return _save_startup(db, payload, row)


@router.post("/startups/import")
def import_verified_startups(payload: list[StartupUpsert], _: User = Depends(admin_only), db: Session = Depends(get_db)):
    imported = 0
    for item in payload:
        row = db.query(StartupInformation).filter_by(name=item.name.strip()).first()
        _save_startup(db, item, row); imported += 1
    return {"imported": imported}


sync_router = APIRouter(tags=["Administration"])


@sync_router.post("/jobs/sync")
async def sync_jobs(_: User = Depends(admin_only)):
    try:
        from app.scheduler.job_scheduler import sync_jobs_in_worker
        return await asyncio.to_thread(sync_jobs_in_worker)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Job synchronization failed") from exc
