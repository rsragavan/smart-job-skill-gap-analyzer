from app.db.database import SessionLocal
from app.models.job import Job, JobStatus
from app.services.job_match_service import JobMatchService


class JobRecommendationService:

    def __init__(self):
        self.matcher = JobMatchService()

    def recommend_jobs(self, resume_skills):

        db = SessionLocal()

        try:

            jobs = db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()

            recommendations = []

            for job in jobs:

                result = self.matcher.match_job(
                    resume_skills,
                    job
                )

                # Count total skills in the job
                total_skills = (
                    len(result["matched_skills"]) +
                    len(result["missing_skills"])
                )

                # Skip jobs with very few detectable skills
                if total_skills < 3:
                    continue

                # Skip low-quality matches
                if result["match_percentage"] < 30:
                    continue

                recommendations.append(result)

            # Sort by highest match percentage
            recommendations.sort(
                key=lambda x: x["match_percentage"],
                reverse=True
            )

            # Return only the top 5 jobs
            return recommendations[:5]

        finally:
            db.close()
