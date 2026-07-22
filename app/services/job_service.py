from app.models.job import Job, JobStatus
from app.repositories.job_repository import JobRepository


class JobService:

    def __init__(self, repository: JobRepository):
        self.repository = repository

    def save_job(self, job_data: dict, company_name: str, existing_jobs: dict[str, Job]):
        greenhouse_job_id = str(job_data["id"])
        location_data = job_data.get("location") or {}
        location = location_data.get("name", "Unknown") if isinstance(location_data, dict) else str(location_data)
        departments = job_data.get("departments") or []
        department_names = [
            department.get("name", "")
            for department in departments
            if isinstance(department, dict)
        ]
        metadata = job_data.get("metadata") or []
        employment_type = "Unknown"
        if isinstance(metadata, list):
            for item in metadata:
                if isinstance(item, dict) and "employment" in item.get("name", "").lower():
                    employment_type = str(item.get("value") or "Unknown")
                    break
        elif isinstance(metadata, dict):
            employment_value = metadata.get("Employment Type")
            if isinstance(employment_value, list) and employment_value:
                employment_type = str(employment_value[0].get("value") or "Unknown") if isinstance(employment_value[0], dict) else str(employment_value[0])
            elif employment_value:
                employment_type = str(employment_value)

        values = {
            "title": job_data.get("title") or "Untitled job",
            "company": company_name,
            "location": location or "Unknown",
            "department": ", ".join(name for name in department_names if name) or "Unknown",
            "employment_type": employment_type,
            "description": job_data.get("content") or "",
            "url": job_data.get("absolute_url") or "",
            "status": JobStatus.ACTIVE,
            "inactive_at": None,
        }

        existing = existing_jobs.get(greenhouse_job_id)
        if existing is None:
            job = Job(greenhouse_job_id=greenhouse_job_id, **values)
            self.repository.add(job)
            existing_jobs[greenhouse_job_id] = job
            return "created"

        changed = any(getattr(existing, field) != value for field, value in values.items())
        if not changed:
            return "skipped"

        for field, value in values.items():
            setattr(existing, field, value)
        return "updated"
