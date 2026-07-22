from app.models.job import Job
from app.services.job_match_service import JobMatchService

job = Job()

job.title = "Backend Developer"

job.company = "Canonical"

job.description = """
Python
FastAPI
Docker
Git
Linux
PostgreSQL
"""

resume_skills = [
    "python",
    "docker",
    "git"
]

service = JobMatchService()

result = service.match_job(
    resume_skills,
    job
)

print(result)