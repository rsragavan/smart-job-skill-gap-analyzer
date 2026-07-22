from app.services.job_recommendation_service import JobRecommendationService

resume_skills = [
    "python",
    "docker",
    "git",
    "postgresql"
]

service = JobRecommendationService()

results = service.recommend_jobs(resume_skills)

print("Top Matching Jobs")

for job in results:

    print("----------------------")

    print(job["job_title"])

    print(job["company"])

    print(job["match_percentage"])