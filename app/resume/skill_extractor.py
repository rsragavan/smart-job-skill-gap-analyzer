from sqlalchemy.orm import Session

from app.services.technical_skills_engine import skills_engine


class SkillExtractor:

    def extract_skills(self, text: str, db: Session | None = None) -> list[str]:
        return skills_engine.extract(text, db=db, source="resume" if db else None)
