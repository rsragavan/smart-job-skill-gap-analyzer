class SkillGapService:

    def find_missing_skills(
        self,
        resume_skills: list[str],
        job_skills: list[str]
    ) -> list[str]:

        resume_set = set(skill.lower() for skill in resume_skills)

        job_set = set(skill.lower() for skill in job_skills)

        missing = job_set - resume_set

        return sorted(missing)