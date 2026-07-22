from app.services.resume_analysis_service import ResumeAnalysisService

job_skills = [
    "java",
    "spring boot",
    "mysql",
    "docker",
    "git",
    "aws",
    "linux"
]

service = ResumeAnalysisService()

result = service.analyze(
    "uploads/ragavan_resume.pdf",
    job_skills
)

print(result)