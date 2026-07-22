from app.resume.skill_extractor import SkillExtractor

text = """
I know Java, Spring Boot, MySQL,
Git, Docker and AWS.
"""

extractor = SkillExtractor()

skills = extractor.extract_skills(text)

print(skills)