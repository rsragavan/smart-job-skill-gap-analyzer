from app.models.resume_history import ResumeHistory
from app.repositories.resume_history_repository import ResumeHistoryRepository


class ResumeHistoryService:

    def __init__(self, repository: ResumeHistoryRepository):
        self.repository = repository

    def save_history(
        self,
        filename,
        skills,
        recommended_jobs
        , user_id=None, content_hash=None, ats_analysis=None, storage_path=None
    ):

        history = ResumeHistory(
            filename=filename,
            extracted_skills=", ".join(skills),
            recommended_jobs=len(recommended_jobs),
            user_id=user_id,
            content_hash=content_hash,
            ats_analysis=ats_analysis,
            storage_path=storage_path,
        )

        return self.repository.create(history)

    def get_history(self):

        return self.repository.get_all()
