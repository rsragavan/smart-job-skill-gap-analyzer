from sqlalchemy.orm import Session

from app.models.resume_history import ResumeHistory


class ResumeHistoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, history: ResumeHistory):
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def get_all(self):
        return (
            self.db.query(ResumeHistory)
            .order_by(ResumeHistory.uploaded_at.desc())
            .all()
        )

    def get_all_for_user(self, user_id: int):
        return self.db.query(ResumeHistory).filter(ResumeHistory.user_id == user_id).order_by(ResumeHistory.uploaded_at.desc()).all()

    def get_latest_for_user(self, user_id: int):
        return self.db.query(ResumeHistory).filter(ResumeHistory.user_id == user_id).order_by(ResumeHistory.uploaded_at.desc()).first()

    def get_latest(self):
        """
        Returns the most recently uploaded resume.
        """
        return (
            self.db.query(ResumeHistory)
            .order_by(ResumeHistory.uploaded_at.desc())
            .first()
        )

    def get_by_id(self, id: int):
        return self.db.query(ResumeHistory).filter(ResumeHistory.id == id).first()

    def get_by_id_for_user(self, id: int, user_id: int):
        return self.db.query(ResumeHistory).filter(ResumeHistory.id == id, ResumeHistory.user_id == user_id).first()

    def delete(self, history: ResumeHistory):
        self.db.delete(history)
        self.db.commit()
        return True
