from sqlalchemy.orm import Session

from app.clients.greenhouse_client import GreenhouseClient
from app.repositories.job_repository import JobRepository
from app.models.job import Job
from app.services.job_service import JobService
from app.jobs.job_skill_extractor import JobSkillExtractor


class JobFetchService:

    def __init__(self, db: Session):
        self.client = GreenhouseClient()
        self.job_repository = JobRepository(db)
        self.job_service = JobService(self.job_repository)
        self.skill_extractor = JobSkillExtractor()

    def fetch_jobs(self, company, existing_jobs: dict[str, Job] | None = None):
        if existing_jobs is None:
            existing_jobs = {job.greenhouse_job_id: job for job in self.job_repository.get_all()}
        response = self.client.fetch_jobs(company.greenhouse_token)
        counts = {"created": 0, "updated": 0, "skipped": 0, "job_ids": set()}
        for job in response.get("jobs", []):
            self.skill_extractor.extract_skills(job.get("content") or "", db=self.job_repository.db)
            counts["job_ids"].add(str(job["id"]))
            result = self.job_service.save_job(job, company.name, existing_jobs)
            counts[result] += 1
        return counts

    def close(self):
        self.client.close()
