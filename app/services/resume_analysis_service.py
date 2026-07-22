from app.resume.resume_parser import ResumeParser
from app.resume.skill_extractor import SkillExtractor
from app.services.skill_gap_service import SkillGapService


class ResumeAnalysisService:

    def __init__(self):
        self.parser = ResumeParser()
        self.extractor = SkillExtractor()
        self.gap_service = SkillGapService()

    def analyze(self, resume_path, job_skills):

        text = self.parser.extract_text(resume_path)

        resume_skills = self.extractor.extract_skills(text)

        missing = self.gap_service.find_missing_skills(
            resume_skills,
            job_skills
        )

        return {
            "resume_skills": resume_skills,
            "missing_skills": missing
        }