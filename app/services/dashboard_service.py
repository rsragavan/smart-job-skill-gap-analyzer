from sqlalchemy.orm import Session

from app.models.job import Job, JobStatus
from app.models.job_application import JobApplication
from app.models.mock_interview import MockInterview


class DashboardService:

    def __init__(self, db: Session):
        self.db = db

    def get_dashboard(self, user_id: int):

        # ==========================
        # Active Jobs
        # ==========================

        jobs = (
            self.db.query(Job)
            .filter(Job.status == JobStatus.ACTIVE)
            .all()
        )

        total_jobs = len(jobs)

        total_companies = len(
            {
                job.company
                for job in jobs
            }
        )

        python_jobs = 0
        java_jobs = 0
        docker_jobs = 0
        linux_jobs = 0
        remote_jobs = 0

        for job in jobs:

            description = (job.description or "").lower()
            location = (job.location or "").lower()

            if "python" in description:
                python_jobs += 1

            if "java" in description:
                java_jobs += 1

            if "docker" in description:
                docker_jobs += 1

            if "linux" in description:
                linux_jobs += 1

            if "remote" in location:
                remote_jobs += 1

        # ==========================
        # User Applications
        # ==========================

        total_applications = (
            self.db.query(JobApplication)
            .filter(JobApplication.user_id == user_id)
            .count()
        )

        applied = (
            self.db.query(JobApplication)
            .filter(
                JobApplication.user_id == user_id,
                JobApplication.status == "Applied",
            )
            .count()
        )

        reviewing = (
            self.db.query(JobApplication)
            .filter(
                JobApplication.user_id == user_id,
                JobApplication.status == "Reviewing",
            )
            .count()
        )

        shortlisted = (
            self.db.query(JobApplication)
            .filter(
                JobApplication.user_id == user_id,
                JobApplication.status == "Shortlisted",
            )
            .count()
        )

        interview_statuses = ("Interview", "Technical Round", "Technical Interview", "Technical Round 2", "Managerial Interview", "HR Round", "HR Interview")
        interview = (
            self.db.query(JobApplication)
            .filter(
                JobApplication.user_id == user_id,
                JobApplication.status.in_(interview_statuses),
            )
            .count()
        )

        offer = (
            self.db.query(JobApplication)
            .filter(
                JobApplication.user_id == user_id,
                JobApplication.status.in_(("Offer", "Offer Received")),
            )
            .count()
        )

        rejected = (
            self.db.query(JobApplication)
            .filter(
                JobApplication.user_id == user_id,
                JobApplication.status.in_(("Rejected", "Withdrawn")),
            )
            .count()
        )

        # ==========================
        # Recent Applications
        # ==========================

        recent_applications = (
            self.db.query(JobApplication)
            .filter(JobApplication.user_id == user_id)
            .order_by(JobApplication.applied_at.desc())
            .limit(5)
            .all()
        )

        recent = []

        for application in recent_applications:
            job = application.job
            recent.append(
                {
                    "id": application.id,
                    "job_id": job.id if job else None,
                    "job_title": job.title if job else application.custom_job_title,
                    "company": job.company if job else application.custom_company_name,
                    "location": job.location if job else application.custom_location,
                    "status": application.status,
                    "applied_at": application.applied_at,
                }
            )

        completed_interviews = self.db.query(MockInterview).filter(MockInterview.user_id == user_id, MockInterview.status == "completed").all()
        interview_scores = [row.overall_score for row in completed_interviews if row.overall_score is not None]
        recommended_interviews = []
        for application in self.db.query(JobApplication).filter(JobApplication.user_id == user_id, JobApplication.status.in_(("Technical Round", "Technical Interview", "HR Round", "HR Interview"))).limit(5).all():
            recommended_interviews.append({"application_id": application.id, "type": "HR" if "hr" in application.status.casefold() else "Technical", "company": application.custom_company_name or (application.job.company if application.job else None), "role": application.custom_job_title or (application.job.title if application.job else None)})

        # ==========================
        # Dashboard Response
        # ==========================

        return {
            "total_jobs": total_jobs,
            "total_companies": total_companies,

            "python_jobs": python_jobs,
            "java_jobs": java_jobs,
            "docker_jobs": docker_jobs,
            "linux_jobs": linux_jobs,
            "remote_jobs": remote_jobs,

            "total_applications": total_applications,
            "applied": applied,
            "reviewing": reviewing,
            "shortlisted": shortlisted,
            "interview": interview,
            "offer": offer,
            "rejected": rejected,
            "assessment_pending": self.db.query(JobApplication).filter(JobApplication.user_id == user_id, JobApplication.status == "Online Assessment").count(),
            "accepted": self.db.query(JobApplication).filter(JobApplication.user_id == user_id, JobApplication.status == "Accepted").count(),
            "active_applications": self.db.query(JobApplication).filter(JobApplication.user_id == user_id, ~JobApplication.status.in_(("Accepted", "Rejected", "Withdrawn"))).count(),

            "recent": recent,
            "interviews_completed": len(completed_interviews),
            "average_interview_score": round(sum(interview_scores) / len(interview_scores)) if interview_scores else 0,
            "coding_score": 0,
            "technical_score": round(sum(row.technical_score for row in completed_interviews if row.technical_score is not None) / max(1, sum(row.technical_score is not None for row in completed_interviews))) if completed_interviews else 0,
            "hr_score": round(sum(row.hr_score for row in completed_interviews if row.hr_score is not None) / max(1, sum(row.hr_score is not None for row in completed_interviews))) if completed_interviews else 0,
            "recommended_interviews": recommended_interviews,
        }
