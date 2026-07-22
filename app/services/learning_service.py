from app.db.database import SessionLocal
from app.jobs.job_skill_extractor import JobSkillExtractor
from app.learning.roadmap_generator import RoadmapGenerator
from app.repositories.job_repository import JobRepository
from app.models.job import JobStatus
from app.repositories.resume_history_repository import ResumeHistoryRepository
from app.services.skill_gap_service import SkillGapService


class LearningService:

    def __init__(self):
        self.db = SessionLocal()

        self.job_repository = JobRepository(self.db)
        self.resume_repository = ResumeHistoryRepository(self.db)

        self.job_extractor = JobSkillExtractor()
        self.skill_gap_service = SkillGapService()
        self.roadmap_generator = RoadmapGenerator()

    def generate_learning_plan(self, job_id: int, user_id: int | None = None):

        try:

            # Get selected job
            job = self.job_repository.get_by_id(job_id)

            if job is None or job.status != JobStatus.ACTIVE:
                return {
                    "error": "Job not found"
                }

            # Get latest uploaded resume
            resume = self.resume_repository.get_latest() if user_id is None else self.resume_repository.get_latest_for_user(user_id)

            if resume is None:
                return {
                    "error": "No resume uploaded"
                }

            # Convert stored resume skills into a Python list
            if isinstance(resume.extracted_skills, str):
                resume_skills = [
                    skill.strip().lower()
                    for skill in resume.extracted_skills.split(",")
                    if skill.strip()
                ]
            else:
                resume_skills = resume.extracted_skills

            # Extract skills from job description
            job_skills = self.job_extractor.extract_skills(
                job.description
            )

            # Find missing skills
            missing_skills = self.skill_gap_service.find_missing_skills(
                resume_skills,
                job_skills
            )

            # Find matched skills
            matched_skills = sorted(
                list(set(job_skills) - set(missing_skills))
            )

            # Calculate match percentage
            if len(job_skills) == 0:
                percentage = 0
            else:
                percentage = round(
                    (len(matched_skills) / len(job_skills)) * 100,
                    2
                )

            # Generate learning roadmap
            roadmap = self.roadmap_generator.generate(
                missing_skills
            )

            total_days = sum(
                item["estimated_days"]
                for item in roadmap
            )

            return {
                "job_title": job.title,
                "company": job.company,
                "resume_skills": sorted(resume_skills),
                "job_skills": sorted(job_skills),
                "matched_skills": matched_skills,
                "missing_skills": sorted(missing_skills),
                "match_percentage": percentage,
                "total_missing_skills": len(missing_skills),
                "estimated_completion_days": total_days,
                "learning_roadmap": roadmap
            }

        finally:
            self.db.close()
