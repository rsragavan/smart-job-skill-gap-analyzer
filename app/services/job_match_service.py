from app.jobs.job_skill_extractor import JobSkillExtractor
from app.services.skill_gap_service import SkillGapService


class JobMatchService:

    def __init__(self):
        self.job_extractor = JobSkillExtractor()
        self.gap_service = SkillGapService()

    def match_job(self, resume_skills, job):

        # Extract skills from job description
        job_skills = self.job_extractor.extract_skills(
            job.description
        )

        # Find missing skills
        missing_skills = self.gap_service.find_missing_skills(
            resume_skills,
            job_skills
        )

        matched_skills = list(
            set(job_skills) - set(missing_skills)
        )

        total = len(job_skills)

        if total == 0:
            percentage = 0
        else:
            percentage = round(
                (len(matched_skills) / total) * 100,
                2
            )

        return {
            "job_id": job.id,
            "job_title": job.title,
            "company": job.company,
            "location": job.location,
            "url": job.url,
            "match_percentage": percentage,
            "matched_skills": sorted(matched_skills),
            "missing_skills": sorted(missing_skills)
        }