from collections import Counter

from sqlalchemy.orm import Session

from app.models.job import Job, JobStatus
from app.jobs.job_skill_extractor import JobSkillExtractor


class AnalyticsService:

    def __init__(self, db: Session):
        self.db = db
        self.extractor = JobSkillExtractor()

    def get_top_skills(self):

        jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()

        counter = Counter()

        for job in jobs:

            skills = self.extractor.extract_skills(
                job.description
            )

            counter.update(skills)

        return dict(
            counter.most_common(20)
        )

    def get_top_companies(self):

        jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()

        counter = Counter()

        for job in jobs:
            if job.company:
                counter.update([job.company])

        return dict(counter.most_common(20))

    def get_jobs_per_company(self):

        jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()

        companies = {}

        for job in jobs:
            name = job.company or "Unknown"
            companies.setdefault(name, []).append({
                "id": job.id,
                "title": job.title
            })

        return companies

    def get_average_match_percentage(self, resume_skills: list[str] | None = None):

        # If resume_skills is None, try to compute using latest resume in DB
        from app.repositories.resume_history_repository import ResumeHistoryRepository

        if resume_skills is None:
            repo = ResumeHistoryRepository(self.db)
            latest = repo.get_latest()
            if latest is None:
                return 0.0

            if isinstance(latest.extracted_skills, str):
                resume_skills = [s.strip().lower() for s in latest.extracted_skills.split(",") if s.strip()]
            else:
                resume_skills = latest.extracted_skills

        jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()

        percentages = []

        for job in jobs:
            job_skills = self.extractor.extract_skills(job.description)
            if not job_skills:
                continue

            matched = len(set([s.lower() for s in job_skills]) & set([s.lower() for s in resume_skills]))
            pct = round((matched / len(job_skills)) * 100, 2) if len(job_skills) > 0 else 0.0
            percentages.append(pct)

        if not percentages:
            return 0.0

        return round(sum(percentages) / len(percentages), 2)

    def get_overview(self):
        top_skills = self.get_top_skills()
        top_companies = self.get_top_companies()
        jobs_per_company = self.get_jobs_per_company()
        avg_match = self.get_average_match_percentage()

        return {
            "top_skills": top_skills,
            "top_companies": top_companies,
            "jobs_per_company": jobs_per_company,
            "average_match_percentage": avg_match,
        }
