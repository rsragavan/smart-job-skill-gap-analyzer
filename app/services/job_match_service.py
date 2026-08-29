from app.jobs.job_skill_extractor import JobSkillExtractor
from app.services.skill_gap_service import SkillGapService


class JobMatchService:

    def __init__(self):
        self.job_extractor = JobSkillExtractor()
        self.gap_service = SkillGapService()

    @staticmethod
    def _normalize(skill: str) -> str:
        return " ".join(skill.strip().casefold().split())

    def match_text(
        self,
        resume_skills,
        description: str,
        *,
        company: str,
        role: str,
        job_id: int | None = None,
        location: str | None = None,
        url: str | None = None,
    ):
        job_skills = self.gap_service.normalize_skills(
            self.job_extractor.extract_skills(description or "")
            + self.gap_service.extract_target_skills(role, "")
        )
        analysis = self.gap_service.analyze(resume_skills, job_skills, role=role, job_description=description)

        return {
            "job_id": job_id,
            "job_title": role,
            "company": company,
            "location": location,
            "url": url,
            "match_percentage": analysis["match_percentage"],
            "matched_skills": analysis["matched_skills"],
            "missing_skills": analysis["missing_skills"],
            "missing_skill_details": analysis["missing_skill_details"],
            "skill_gap_explanations": analysis["explanations"],
        }

    def match_job(self, resume_skills, job):
        return self.match_text(
            resume_skills,
            job.description,
            company=job.company,
            role=job.title,
            job_id=job.id,
            location=job.location,
            url=job.url,
        )
