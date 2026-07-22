import logging
from datetime import UTC, datetime
from time import monotonic

from sqlalchemy.orm import Session

from app.models.job import Job, JobStatus
from app.services.company_service import CompanyService
from app.services.job_fetch_service import JobFetchService

logger = logging.getLogger(__name__)


class JobSyncService:
    """Synchronize active Greenhouse companies in one database transaction."""

    def __init__(self, db: Session):
        self.db = db
        self.company_service = CompanyService(db)
        self.job_fetch_service = JobFetchService(db)

    def sync_all_jobs(self) -> dict[str, int | float | str]:
        started = monotonic()
        sync_time = datetime.now(UTC)
        logger.info("Job synchronization started")
        companies = self.company_service.get_all_active_companies()
        counts: dict[str, int | float | str] = {
            "companies": len(companies), "new_jobs": 0, "updated_jobs": 0,
            "skipped_duplicates": 0, "inactive_jobs": 0, "failed_companies": 0,
        }
        existing_jobs = {
            job.greenhouse_job_id: job for job in self.db.query(Job).all()
        }

        try:
            for company in companies:
                logger.info("Synchronizing company: %s", company.name)
                try:
                    result = self.job_fetch_service.fetch_jobs(company, existing_jobs)
                    fetched_job_ids = result.pop("job_ids")
                    marked_inactive = 0
                    for job in existing_jobs.values():
                        if job.company == company.name and job.greenhouse_job_id not in fetched_job_ids and job.status != JobStatus.INACTIVE:
                            job.status = JobStatus.INACTIVE
                            job.inactive_at = sync_time
                            marked_inactive += 1
                    company.last_scraped_at = sync_time
                    counts["inactive_jobs"] += marked_inactive
                    for key in ("created", "updated", "skipped"):
                        counts[{"created": "new_jobs", "updated": "updated_jobs", "skipped": "skipped_duplicates"}[key]] += result[key]
                    logger.info(
                        "Company %s synchronized: %s new, %s updated, %s duplicate jobs skipped",
                        company.name, result["created"], result["updated"], result["skipped"],
                    )
                except Exception:
                    counts["failed_companies"] += 1
                    logger.exception("Company synchronization failed: %s", company.name)

            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        finally:
            self.job_fetch_service.close()

        counts["completed_at"] = sync_time.isoformat()
        counts["duration_seconds"] = round(monotonic() - started, 2)
        logger.info(
            "Job synchronization completed: %s new, %s updated, %s inactive, %s duplicate jobs skipped, duration=%ss",
            counts["new_jobs"], counts["updated_jobs"], counts["inactive_jobs"], counts["skipped_duplicates"], counts["duration_seconds"],
        )
        return counts
