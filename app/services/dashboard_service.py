from sqlalchemy.orm import Session

from app.models.job import Job, JobStatus


class DashboardService:

    def __init__(self, db: Session):
        self.db = db

    def get_dashboard(self):

        jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()

        total_jobs = len(jobs)

        companies = {
            job.company
            for job in jobs
        }

        total_companies = len(companies)

        python_jobs = 0
        java_jobs = 0
        docker_jobs = 0
        linux_jobs = 0
        remote_jobs = 0

        for job in jobs:

            description = job.description.lower()

            if "python" in description:
                python_jobs += 1

            if "java" in description:
                java_jobs += 1

            if "docker" in description:
                docker_jobs += 1

            if "linux" in description:
                linux_jobs += 1

            if "remote" in job.location.lower():
                remote_jobs += 1

        return {
            "total_jobs": total_jobs,
            "total_companies": total_companies,
            "python_jobs": python_jobs,
            "java_jobs": java_jobs,
            "docker_jobs": docker_jobs,
            "linux_jobs": linux_jobs,
            "remote_jobs": remote_jobs,
        }
