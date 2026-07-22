from app.db.database import SessionLocal
from app.models.company import Company

db = SessionLocal()

company = db.query(Company).first()

print("Name:", company.name)
print("Token:", company.greenhouse_token)
print("Career URL:", company.career_url)

db.close()