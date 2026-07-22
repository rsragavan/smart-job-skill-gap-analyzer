from sqlalchemy.orm import Session

from app.models.company import Company


class CompanyService:

    def __init__(self, db: Session):
        self.db = db

    def get_all_active_companies(self):
        return (
            self.db.query(Company)
            .filter(Company.is_active.is_(True), Company.platform == "greenhouse")
            .all()
        )

    def get_company_by_token(self, token: str):
        return (
            self.db.query(Company)
            .filter(Company.greenhouse_token == token)
            .first()
        )
