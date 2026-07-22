from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.company import Company


COMPANIES = [
    {
        "name": "Canonical",
        "platform": "greenhouse",
        "greenhouse_token": "canonical",
        "career_url": "https://job-boards.greenhouse.io/canonical",
    },
    {
        "name": "Razorpay Software Private Limited",
        "platform": "greenhouse",
        "greenhouse_token": "razorpaysoftwareprivatelimited",
        "career_url": "https://job-boards.greenhouse.io/razorpaysoftwareprivatelimited",
    },
    {
        "name": "Postman",
        "platform": "greenhouse",
        "greenhouse_token": "postman",
        "career_url": "https://job-boards.greenhouse.io/postman",
    },
    {
        "name": "Appian Corporation",
        "platform": "greenhouse",
        "greenhouse_token": "appian",
        "career_url": "https://job-boards.greenhouse.io/appian",
    },
    {
        "name": "Sagent India",
        "platform": "greenhouse",
        "greenhouse_token": "sagentindia",
        "career_url": "https://job-boards.greenhouse.io/sagentindia",
    },
    {
        "name": "MX Build Technologies India Private Limited",
        "platform": "greenhouse",
        "greenhouse_token": "mxbuildtechnologiesindiaprivatelimited",
        "career_url": "https://job-boards.greenhouse.io/mxbuildtechnologiesindiaprivatelimited",
    },
    {
        "name": "Mitsogo",
        "platform": "greenhouse",
        "greenhouse_token": "mitsogoinc",
        "career_url": "https://job-boards.greenhouse.io/mitsogoinc",
    },
    {
        "name": "Arcadia",
        "platform": "greenhouse",
        "greenhouse_token": "arcadiacareers",
        "career_url": "https://job-boards.greenhouse.io/arcadiacareers",
    },
    {
        "name": "Integrate",
        "platform": "greenhouse",
        "greenhouse_token": "integrate",
        "career_url": "https://job-boards.greenhouse.io/integrate",
        "is_active": False,
    },
    {
        "name": "GitLab",
        "platform": "greenhouse",
        "greenhouse_token": "gitlab",
        "career_url": "https://job-boards.greenhouse.io/gitlab",
    },
    {
        "name": "Cloudflare",
        "platform": "greenhouse",
        "greenhouse_token": "cloudflare",
        "career_url": "https://job-boards.greenhouse.io/cloudflare",
    },
    {
        "name": "MongoDB",
        "platform": "greenhouse",
        "greenhouse_token": "mongodb",
        "career_url": "https://job-boards.greenhouse.io/mongodb",
    },
    {
        "name": "Sentry",
        "platform": "greenhouse",
        "greenhouse_token": "sentry",
        "career_url": "https://job-boards.greenhouse.io/sentry",
        "is_active": False,
    },
    {
        "name": "Dropbox",
        "platform": "greenhouse",
        "greenhouse_token": "dropbox",
        "career_url": "https://job-boards.greenhouse.io/dropbox",
    },
    {
        "name": "Figma",
        "platform": "greenhouse",
        "greenhouse_token": "figma",
        "career_url": "https://job-boards.greenhouse.io/figma",
    },
    {
        "name": "Cockroach Labs",
        "platform": "greenhouse",
        "greenhouse_token": "cockroachlabs",
        "career_url": "https://job-boards.greenhouse.io/cockroachlabs",
    },
    {
        "name": "YugabyteDB",
        "platform": "greenhouse",
        "greenhouse_token": "yugabyte",
        "career_url": "https://job-boards.greenhouse.io/yugabyte",
    },
]
def seed_companies():
    db: Session = SessionLocal()

    try:
        for company in COMPANIES:

            exists = db.query(Company).filter(Company.greenhouse_token == company["greenhouse_token"]).first()

            if exists:
                print(f"Skipped: {company['name']}")
                continue

            db_company = Company(**company)

            db.add(db_company)

        db.commit()

        print("Company seeding completed")

    finally:
        db.close()


if __name__ == "__main__":
    seed_companies()
