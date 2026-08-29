from datetime import UTC, datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.job import Job
from app.models.company import Company
from app.models.company_intelligence import CompanyRole, CompanySelectionProcess
from app.models.job_application import ApplicationStageHistory, ApplicationTimeline, JobApplication
from app.repositories.job_application_repository import JobApplicationRepository

ALLOWED_STATUS = {"Applied", "In Progress", "Shortlisted", "Interview", "Offer", "Accepted", "Rejected", "Withdrawn", "Resume Shortlisted", "Online Assessment", "Assessment Passed", "Technical Interview", "Technical Round 2", "Managerial Interview", "HR Interview", "Offer Received", "Reviewing", "Technical Round", "HR Round"}
STATUS_PROGRESS = {"Applied": 10, "In Progress": 30, "Reviewing": 30, "Resume Shortlisted": 35, "Shortlisted": 35, "Online Assessment": 45, "Assessment Passed": 55, "Interview": 65, "Technical Round": 65, "Technical Interview": 65, "Technical Round 2": 70, "Managerial Interview": 75, "HR Round": 80, "HR Interview": 80, "Offer": 90, "Offer Received": 90, "Accepted": 100, "Rejected": 100, "Withdrawn": 100}

class JobApplicationService:
    def __init__(self): self.repository = JobApplicationRepository()
    def apply_for_job(self, db: Session, user_id: int, job_id: int, notes: str | None = None):
        job = db.get(Job, job_id)
        if not job: raise HTTPException(status_code=404, detail="Job not found.")
        if self.repository.already_applied(db, user_id, job_id): raise HTTPException(status_code=400, detail="You have already applied for this job.")
        company = db.query(Company).filter(Company.name == job.company).first()
        role = db.query(CompanyRole).filter_by(company_id=company.id, title=job.title).first() if company else None
        item = JobApplication(user_id=user_id, job_id=job_id, source_type="scraped", company_id=company.id if company else None, company_role_id=role.id if role else None, status="Applied", notes=notes)
        db.add(item); db.flush(); self._record(db, item, None, "Applied", user_id, notes); db.commit(); db.refresh(item); return self._serialize(item, db)
    def create_custom_application(self, db: Session, user_id: int, data):
        self._valid(data.status); item = JobApplication(user_id=user_id, source_type="custom", status=data.status, notes=data.notes, applied_at=data.applied_at or datetime.now(UTC), interview_date=data.interview_date, custom_company_name=data.company_name.strip(), custom_job_title=data.job_title.strip(), custom_location=data.location.strip() if data.location else None, custom_job_url=data.job_url.strip() if data.job_url else None)
        db.add(item); db.flush(); self._record(db, item, None, data.status, user_id, data.notes); db.commit(); db.refresh(item); return self._serialize(item, db)
    def get_my_applications(self, db: Session, user_id: int): return [self._serialize(x, db) for x in self.repository.get_by_user(db, user_id)]
    def update_application(self, db: Session, application_id: int, user_id: int, status=None, notes=None, current_selection_round=None, current_round_number=None, interview_date=None):
        item = self._owned(db, application_id, user_id)
        if status is not None and status != item.status:
            self._valid(status); previous = item.status; item.status = status; self._record(db, item, previous, status, user_id, notes if notes is not None else item.notes)
        if notes is not None: item.notes = notes
        if current_selection_round is not None: item.current_selection_round = current_selection_round
        if current_round_number is not None: item.current_round_number = current_round_number
        if interview_date is not None: item.interview_date = interview_date
        db.commit(); db.refresh(item); return self._serialize(item, db)
    def get_timeline(self, db, application_id, user_id): self._owned(db, application_id, user_id); return db.query(ApplicationTimeline).filter_by(application_id=application_id).order_by(ApplicationTimeline.updated_at).all()
    def get_history(self, db, application_id, user_id): self._owned(db, application_id, user_id); return db.query(ApplicationStageHistory).filter_by(application_id=application_id).order_by(ApplicationStageHistory.changed_at).all()
    def delete_application(self, db, application_id, user_id): self.repository.delete(db, self._owned(db, application_id, user_id)); return {"message": "Application deleted successfully."}
    def get_dashboard_stats(self, db, user_id):
        rows = self.repository.get_by_user(db, user_id); interview = {"Interview", "Technical Interview", "Technical Round", "Technical Round 2", "Managerial Interview", "HR Interview", "HR Round"}
        return {"total": len(rows), "applied": sum(x.status == "Applied" for x in rows), "in_progress": sum(x.status in {"In Progress", "Reviewing"} for x in rows), "shortlisted": sum(x.status in {"Shortlisted", "Resume Shortlisted"} for x in rows), "interview": sum(x.status in interview for x in rows), "offer": sum(x.status in {"Offer", "Offer Received"} for x in rows), "accepted": sum(x.status == "Accepted" for x in rows), "rejected": sum(x.status in {"Rejected", "Withdrawn"} for x in rows), "custom": sum(x.source_type == "custom" for x in rows), "upcoming_interviews": sum(x.interview_date is not None and x.interview_date >= datetime.now(UTC) for x in rows)}
    def _owned(self, db, app_id, user_id):
        item = self.repository.get(db, app_id)
        if not item: raise HTTPException(status_code=404, detail="Application not found.")
        if item.user_id != user_id: raise HTTPException(status_code=403, detail="Access denied.")
        return item
    @staticmethod
    def _valid(stage):
        if stage not in ALLOWED_STATUS: raise HTTPException(status_code=400, detail="Invalid application status.")
    @staticmethod
    def _record(db, item, previous, stage, user_id, notes):
        db.add(ApplicationTimeline(application_id=item.id, status=stage, notes=notes, progress_percentage=STATUS_PROGRESS[stage]))
        db.add(ApplicationStageHistory(application_id=item.id, previous_stage=previous, new_stage=stage, changed_by_user_id=user_id, notes=notes))
    @staticmethod
    def _serialize(item, db):
        job = item.job
        rounds = []
        if item.company_role_id:
            rounds = [{"round_number": row.round_number, "title": row.title} for row in db.query(CompanySelectionProcess).filter_by(company_role_id=item.company_role_id).order_by(CompanySelectionProcess.round_number).all()]
        return {"id": item.id, "job_id": item.job_id, "company_id": item.company_id, "company_role_id": item.company_role_id, "source_type": item.source_type, "job_title": job.title if job else item.custom_job_title, "company": job.company if job else item.custom_company_name, "location": job.location if job else item.custom_location, "job_url": job.url if job else item.custom_job_url, "status": item.status, "current_selection_round": item.current_selection_round, "current_round_number": item.current_round_number, "rounds": rounds, "notes": item.notes, "interview_date": item.interview_date, "applied_at": item.applied_at, "updated_at": item.updated_at}
job_application_service = JobApplicationService()
