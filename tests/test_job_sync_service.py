from app.db.database import SessionLocal
from app.services.job_sync_service import JobSyncService


def main():
    db = SessionLocal()

    try:
        sync_service = JobSyncService(db)
        sync_service.sync_all_jobs()
    finally:
        db.close()


if __name__ == "__main__":
    main()