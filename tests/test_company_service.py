from app.db.database import SessionLocal
from app.services.company_service import CompanyService


def main():
    db = SessionLocal()

    service = CompanyService(db)

    companies = service.get_all_active_companies()

    print(f"Total Companies: {len(companies)}")

    for company in companies:
        print(company.name)

    db.close()


if __name__ == "__main__":
    main()