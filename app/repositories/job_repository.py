from sqlalchemy.orm import Session

from app.models.job import Job


class JobRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_greenhouse_job_id(self, greenhouse_job_id: str):
        return (
            self.db.query(Job)
            .filter(Job.greenhouse_job_id == greenhouse_job_id)
            .first()
        )

    def get_by_id(self, job_id: int):
        """
        Returns a single job by its database ID.
        """
        return (
            self.db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

    def get_all(self):
        return (
            self.db.query(Job)
            .order_by(Job.created_at.desc())
            .all()
        )

    def create(self, job: Job):
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def add(self, job: Job):
        """Stage a job for the caller's batch transaction."""
        self.db.add(job)

    def update(self):
        self.db.commit()

    def delete(self, job: Job):
        self.db.delete(job)
        self.db.commit()

    def search_by_title(self, keyword: str):
        return (
            self.db.query(Job)
            .filter(Job.title.ilike(f"%{keyword}%"))
            .all()
        )

    def search_by_company(self, company: str):
        return (
            self.db.query(Job)
            .filter(Job.company.ilike(f"%{company}%"))
            .all()
        )

    def count(self):
        return self.db.query(Job).count()
