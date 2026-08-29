from app.db.database import SessionLocal
from app.services.job_sync_service import JobSyncService

def sync_jobs_in_worker() -> dict:
    db = SessionLocal()
    try:
        return JobSyncService(db).sync_all_jobs()
    finally:
        db.close()
