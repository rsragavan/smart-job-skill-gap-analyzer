from app.services.skill_gap_service import SkillGapService

resume = [
    "java",
    "git",
    "docker"
]

job = [
    "java",
    "git",
    "docker",
    "spring boot",
    "aws",
    "postgresql"
]

service = SkillGapService()

missing = service.find_missing_skills(
    resume,
    job
)

print("Missing Skills:")
print(missing)