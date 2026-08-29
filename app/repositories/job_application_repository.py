from sqlalchemy.orm import Session

from app.models.job_application import JobApplication


class JobApplicationRepository:

    def create(self, db: Session, application: JobApplication):
        db.add(application)
        db.commit()
        db.refresh(application)
        return application

    def get_by_user(self, db: Session, user_id: int):
        return (
            db.query(JobApplication)
            .filter(JobApplication.user_id == user_id)
            .order_by(JobApplication.applied_at.desc())
            .all()
        )

    def get(self, db: Session, application_id: int):
        return (
            db.query(JobApplication)
            .filter(JobApplication.id == application_id)
            .first()
        )

    def delete(self, db: Session, application: JobApplication):
        db.delete(application)
        db.commit()

    def update(self, db: Session):
        db.commit()

    def already_applied(
        self,
        db: Session,
        user_id: int,
        job_id: int,
    ):
        return (
            db.query(JobApplication)
            .filter(
                JobApplication.user_id == user_id,
                JobApplication.job_id == job_id,
            )
            .first()
        )