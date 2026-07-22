from sqlalchemy.orm import Session

from app.services.technical_skills_engine import skills_engine


class JobSkillExtractor:

    def extract_skills(self, text: str, db: Session | None = None) -> list[str]:
        return skills_engine.extract(text, db=db, source="job" if db else None)
