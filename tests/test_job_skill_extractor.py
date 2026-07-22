from app.jobs.job_skill_extractor import JobSkillExtractor

description = """
We are looking for a Backend Developer.

Required Skills

Python
FastAPI
Docker
Git
PostgreSQL
Linux
"""

extractor = JobSkillExtractor()

skills = extractor.extract_skills(description)

print(skills)