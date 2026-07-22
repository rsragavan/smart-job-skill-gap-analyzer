from app.db.database import SessionLocal
from app.services.company_service import CompanyService
from app.services.job_fetch_service import JobFetchService


def main():

    db = SessionLocal()

    company_service = CompanyService(db)

    fetch_service = JobFetchService(db)

    companies = company_service.get_all_active_companies()

    for company in companies:
        fetch_service.fetch_jobs(company)

    db.close()


if __name__ == "__main__":
    main()