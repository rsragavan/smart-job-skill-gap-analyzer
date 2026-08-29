from collections import Counter, defaultdict
from datetime import UTC, date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.models.job import Job, JobStatus
from app.jobs.job_skill_extractor import JobSkillExtractor
from app.models.gamification import Achievement, UserBadge, UserGamification
from app.models.learning_progress import LearningProgress
from app.models.resume_history import ResumeHistory
from app.models.job_application import JobApplication
from app.services.career_gps_service import CareerGPSService
from app.models.mock_interview import AssessmentAttempt, MockInterview
from app.models.user_target import UserTarget
from app.models.company import Company
from app.models.company_intelligence import CompanyInsight, StartupInformation


class AnalyticsService:

    def __init__(self, db: Session):
        self.db = db
        self.extractor = JobSkillExtractor()

    def get_top_skills(self):

        jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()

        counter = Counter()

        for job in jobs:

            skills = self.extractor.extract_skills(
                job.description
            )

            counter.update(skills)

        return dict(
            counter.most_common(20)
        )

    def get_top_companies(self):

        jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()

        counter = Counter()

        for job in jobs:
            if job.company:
                counter.update([job.company])

        return dict(counter.most_common(20))

    def get_jobs_per_company(self):

        jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()

        companies = {}

        for job in jobs:
            name = job.company or "Unknown"
            companies.setdefault(name, []).append({
                "id": job.id,
                "title": job.title
            })

        return companies

    def get_average_match_percentage(self, resume_skills: list[str] | None = None):

        # If resume_skills is None, try to compute using latest resume in DB
        from app.repositories.resume_history_repository import ResumeHistoryRepository

        if resume_skills is None:
            repo = ResumeHistoryRepository(self.db)
            latest = repo.get_latest()
            if latest is None:
                return 0.0

            if isinstance(latest.extracted_skills, str):
                resume_skills = [s.strip().lower() for s in latest.extracted_skills.split(",") if s.strip()]
            else:
                resume_skills = latest.extracted_skills

        jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()

        percentages = []

        for job in jobs:
            job_skills = self.extractor.extract_skills(job.description)
            if not job_skills:
                continue

            matched = len(set([s.lower() for s in job_skills]) & set([s.lower() for s in resume_skills]))
            pct = round((matched / len(job_skills)) * 100, 2) if len(job_skills) > 0 else 0.0
            percentages.append(pct)

        if not percentages:
            return 0.0

        return round(sum(percentages) / len(percentages), 2)

    def get_overview(self):
        top_skills = self.get_top_skills()
        top_companies = self.get_top_companies()
        jobs_per_company = self.get_jobs_per_company()
        avg_match = self.get_average_match_percentage()

        return {
            "top_skills": top_skills,
            "top_companies": top_companies,
            "jobs_per_company": jobs_per_company,
            "average_match_percentage": avg_match,
        }

    def get_placement_analytics(self, user_id: int) -> dict[str, Any]:
        resume = self.db.query(ResumeHistory).filter_by(user_id=user_id).order_by(ResumeHistory.uploaded_at.desc()).first()
        applications = self.db.query(JobApplication).filter_by(user_id=user_id).order_by(JobApplication.applied_at).all()
        interviews = self.db.query(MockInterview).filter_by(user_id=user_id).order_by(MockInterview.started_at).all()
        attempts = self.db.query(AssessmentAttempt).filter_by(user_id=user_id).all()
        learning = self.db.query(LearningProgress).filter_by(user_id=user_id).all()
        target = self.db.query(UserTarget).filter_by(user_id=user_id, is_active=True).first()
        career = CareerGPSService(self.db).get_dashboard(user_id)
        job_ids = [item.job_id for item in applications if item.job_id]
        jobs_by_id = {job.id: job for job in self.db.query(Job).filter(Job.id.in_(job_ids)).all()} if job_ids else {}
        statuses = Counter(item.status for item in applications)
        company_apps = Counter(self._application_company(item, jobs_by_id) for item in applications if self._application_company(item, jobs_by_id))
        role_apps = Counter(self._application_role(item, jobs_by_id) for item in applications if self._application_role(item, jobs_by_id))
        response_count = sum(statuses[status] for status in statuses if status != "Applied")
        interview_scores = [item.overall_score for item in interviews if item.status == "completed" and item.overall_score is not None]
        technical_scores = [item.technical_score for item in interviews if item.technical_score is not None]
        hr_scores = [item.hr_score for item in interviews if item.hr_score is not None]
        coding_scores = [item.score for item in attempts if item.score is not None]
        learning_completed = sum(item.status == "completed" for item in learning)
        skill_demand = Counter()
        company_demand = Counter()
        active_jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()
        resume_skills = self._split_skills(resume.extracted_skills if resume else "")
        jobs_by_company: dict[str, list[Job]] = defaultdict(list)
        for job in active_jobs:
            extracted = {_normalize_skill(skill) for skill in self.extractor.extract_skills(job.description or "")}
            skill_demand.update(extracted); company_demand[job.company or "Unknown"] += 1
            jobs_by_company[job.company or "Unknown"].append(job)
        company_matches = []
        for company, count in company_demand.items():
            company_jobs = jobs_by_company.get(company, [])
            scores = []
            for job in company_jobs:
                skills = {_normalize_skill(skill) for skill in self.extractor.extract_skills(job.description or "")}
                if skills: scores.append(round(len(skills & resume_skills) / len(skills) * 100))
            company_matches.append({"company": company, "jobs": count, "match_percentage": round(sum(scores) / len(scores)) if scores else 0})
        company_matches.sort(key=lambda item: item["match_percentage"], reverse=True)
        remote_company_ids = {
            company_id
            for company_id, in self.db.query(CompanyInsight.company_id).filter(CompanyInsight.remote_jobs.is_(True)).all()
        }
        remote_friendly = [
            company.name
            for company in self.db.query(Company).filter(Company.id.in_(remote_company_ids)).order_by(Company.name).all()
        ] if remote_company_ids else []
        components = {"company": career.get("company_readiness", 0), "interview": round(sum(interview_scores) / len(interview_scores)) if interview_scores else 0, "coding": round(sum(coding_scores) / len(coding_scores)) if coding_scores else 0, "resume": resume.ats_analysis.get("overall_score", 0) if resume and resume.ats_analysis else 0, "communication": round(sum(hr_scores) / len(hr_scores)) if hr_scores else 0, "learning": round(learning_completed / len(learning) * 100) if learning else 0}
        readiness_values = [value for value in components.values() if value > 0]
        applications_by_month = Counter(item.applied_at.strftime("%Y-%m") for item in applications if item.applied_at)
        timeline = self._placement_timeline(user_id, resume, target, applications, interviews, learning, jobs_by_id)
        return {"readiness": {"overall": round(sum(readiness_values) / len(readiness_values)) if readiness_values else 0, **components, "trend": self._readiness_trend(components, career)}, "applications": {"submitted": len(applications), "accepted": statuses["Accepted"], "rejected": statuses["Rejected"] + statuses["Withdrawn"], "shortlisted": statuses["Shortlisted"] + statuses["Resume Shortlisted"], "interview_scheduled": sum(statuses[item] for item in ("Interview", "Technical Interview", "Technical Round", "HR Interview", "HR Round")), "offers": statuses["Offer"] + statuses["Offer Received"], "offer_rate": round((statuses["Offer"] + statuses["Offer Received"]) / len(applications) * 100) if applications else 0, "response_rate": round(response_count / len(applications) * 100) if applications else 0, "company_wise": dict(company_apps), "role_wise": dict(role_apps), "monthly_timeline": [{"month": month, "applications": count} for month, count in sorted(applications_by_month.items())]}, "companies": {"top_hiring": company_demand.most_common(10), "most_applied": company_apps.most_common(10), "highest_match": company_matches[:10], "missing_skills": [item for item in company_matches if item["match_percentage"] < 50], "remote_friendly": remote_friendly}, "skills": {"most_requested": skill_demand.most_common(15), "strong": sorted(resume_skills & set(skill_demand)), "missing": [skill for skill, _ in skill_demand.most_common(30) if skill not in resume_skills][:15], "rare": sorted(resume_skills - set(skill_demand)), "trending": skill_demand.most_common(10), "learning_progress": components["learning"]}, "interviews": {"mock_interviews": len(interviews), "completed": sum(item.status == "completed" for item in interviews), "average_score": round(sum(interview_scores) / len(interview_scores)) if interview_scores else 0, "best_company": self._best_interview_company(interviews), "weak_areas": self._weak_areas(interviews), "technical_progress": round(sum(technical_scores) / len(technical_scores)) if technical_scores else 0, "hr_progress": round(sum(hr_scores) / len(hr_scores)) if hr_scores else 0, "coding_progress": round(sum(coding_scores) / len(coding_scores)) if coding_scores else 0}, "timeline": timeline, "recommendations": {"companies": company_matches[:5], "startups": [{"id": item.id, "name": item.name, "industry": item.industry} for item in self.db.query(StartupInformation).order_by(StartupInformation.name).limit(5).all()], "skills": [{"skill": skill, "reason": "Requested by active job listings."} for skill, _ in skill_demand.most_common(5) if skill not in resume_skills], "mock_interviews": [{"type": "Technical", "reason": "Application is in a technical stage."} for item in applications if "technical" in item.status.casefold() or "round" in item.status.casefold()][:3], "coding_practice": [{"topic": skill, "reason": "Appears in active job demand."} for skill, _ in skill_demand.most_common(5) if skill in {"arrays", "strings", "sql", "graphs", "dynamic programming"}]}}

    def get_notifications(self, user_id: int) -> list[dict[str, Any]]:
        now = datetime.now(UTC); notifications = []
        gamification = self.db.query(UserGamification).filter_by(user_id=user_id).first()
        if gamification and gamification.daily_goal_progress < gamification.daily_goal_target: notifications.append({"type": "learning", "title": "Practice today", "detail": f"Complete {gamification.daily_goal_target - gamification.daily_goal_progress} more learning activity.", "severity": "info"})
        tomorrow = (now + timedelta(days=1)).date()
        for item in self.db.query(JobApplication).filter(JobApplication.user_id == user_id).all():
            if item.interview_date and item.interview_date.date() == tomorrow: notifications.append({"type": "interview", "title": "Interview tomorrow", "detail": item.custom_company_name or "Scheduled interview", "severity": "warning"})
        resume = self.db.query(ResumeHistory).filter_by(user_id=user_id).order_by(ResumeHistory.uploaded_at.desc()).first()
        if resume is None or (now - resume.uploaded_at).days > 90: notifications.append({"type": "resume", "title": "Resume update needed", "detail": "Upload a current resume for accurate readiness analytics.", "severity": "info"})
        target = self.db.query(UserTarget).filter_by(user_id=user_id, is_active=True).first()
        if target and target.updated_at and (now - target.updated_at).total_seconds() < 86400: notifications.append({"type": "target", "title": "Target changed", "detail": f"Preparation is aligned to {target.company} · {target.role_title}.", "severity": "info"})
        if self.db.query(JobApplication).filter(JobApplication.user_id == user_id, JobApplication.status.in_(("Applied", "In Progress"))).count(): notifications.append({"type": "application", "title": "Application pending", "detail": "Review applications without a response.", "severity": "info"})
        return notifications

    @staticmethod
    def _application_company(item, jobs): return jobs[item.job_id].company if item.job_id in jobs else item.custom_company_name
    @staticmethod
    def _application_role(item, jobs): return jobs[item.job_id].title if item.job_id in jobs else item.custom_job_title
    @staticmethod
    def _best_interview_company(rows):
        completed = [item for item in rows if item.status == "completed" and item.overall_score is not None]
        return max(completed, key=lambda item: item.overall_score).company_name if completed else None
    @staticmethod
    def _weak_areas(rows):
        return ["Technical" if item.technical_score is not None and item.technical_score < 60 else "Communication" for item in rows if item.status == "completed"][:5]
    @staticmethod
    def _readiness_trend(components, career): return [{"label": "Current", "value": round(sum(components.values()) / len(components)) if components else 0}, {"label": "Career GPS", "value": career.get("readiness_score", 0)}]
    def _placement_timeline(self, user_id, resume, target, applications, interviews, learning, jobs):
        events = []
        if resume: events.append({"date": resume.uploaded_at.isoformat(), "type": "resume", "title": "Resume uploaded"})
        if target: events.append({"date": target.created_at.isoformat(), "type": "target", "title": "Target selected"})
        if learning: events.append({"date": min(item.updated_at for item in learning).isoformat(), "type": "learning", "title": "Learning started"})
        events.extend({"date": item.applied_at.isoformat(), "type": "application", "title": f"Application submitted: {self._application_company(item, jobs) or item.custom_company_name}"} for item in applications if item.applied_at)
        events.extend({"date": item.started_at.isoformat(), "type": "interview", "title": f"Mock interview: {item.interview_type}"} for item in interviews)
        return sorted(events, key=lambda item: item["date"])

    def get_dashboard(self, user_id: int, company: str | None = None, role: str | None = None, skill: str | None = None, date_from: str | None = None, date_to: str | None = None) -> dict[str, Any]:
        start = self._parse_date(date_from)
        end = self._parse_date(date_to) or date.today()
        jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()
        if company:
            jobs = [job for job in jobs if company.casefold() in (job.company or "").casefold()]
        if role:
            jobs = [job for job in jobs if role.casefold() in (job.title or "").casefold()]
        if start:
            jobs = [job for job in jobs if job.created_at.date() >= start]
        jobs = [job for job in jobs if job.created_at.date() <= end]

        resume = self.db.query(ResumeHistory).filter_by(user_id=user_id).order_by(ResumeHistory.uploaded_at.desc()).first()
        resume_skills = self._split_skills(resume.extracted_skills if resume else "")
        if skill:
            jobs = [job for job in jobs if skill.casefold() in (job.description or "").casefold()]
        demand = Counter()
        matched_jobs = []
        for job in jobs:
            extracted = {_normalize_skill(item) for item in self.extractor.extract_skills(job.description or "")}
            demand.update(extracted)
            if extracted:
                matched_jobs.append(round(len(extracted & resume_skills) / len(extracted) * 100, 2))
        match_percentage = round(sum(matched_jobs) / len(matched_jobs), 2) if matched_jobs else 0

        learning = self.db.query(LearningProgress).filter_by(user_id=user_id).all()
        completed_learning = [item for item in learning if item.status == "completed"]
        completed_skills = self._completed_skills(learning)
        projects_completed = len({(item.roadmap_id, item.skill_key, item.item_key) for item in completed_learning if item.item_type == "project"})
        missions = [item for item in learning if item.item_type == "mission"]
        gamification = self.db.query(UserGamification).filter_by(user_id=user_id).first()
        career_data = CareerGPSService(self.db).get_dashboard(user_id)
        career_score = career_data["readiness_score"]
        role_score = career_data["role_readiness"]
        trend = self._activity_series(learning, 30)
        return {
            "filters": {"company": company, "role": role, "skill": skill, "date_from": date_from, "date_to": date_to},
            "resume_statistics": {"uploads": self.db.query(ResumeHistory).filter_by(user_id=user_id).count(), "latest_upload": resume.uploaded_at.isoformat() if resume else None, "skills": len(resume_skills)},
            "job_statistics": {"jobs": len(jobs), "companies": len({job.company for job in jobs}), "applications": self.db.query(JobApplication).filter_by(user_id=user_id).count()},
            "skill_statistics": {"top": [{"name": name, "count": count} for name, count in demand.most_common(12)], "match_percentage": match_percentage, "matched": sorted(resume_skills & set(demand)), "missing": [name for name in demand if name not in resume_skills][:12]},
            "learning_statistics": {"total_items": len(learning), "completed_items": len(completed_learning), "progress": round(len(completed_learning) / len(learning) * 100) if learning else 0, "missions_completed": sum(item.status == "completed" for item in missions)},
            "roadmap_statistics": {"roadmaps": len({item.roadmap_id for item in learning}), "skills": len({item.skill_key for item in learning}), "completed_skills": len(completed_skills), "projects_completed": projects_completed},
            "career_statistics": {"readiness": career_score, "role_readiness": role_score, "path": career_data.get("career_path", "Full Stack")},
            "xp_statistics": {"total": gamification.total_xp if gamification else 0, "level": gamification.level if gamification else 1, "growth": self._xp_growth(learning)},
            "badge_statistics": {"unlocked": self.db.query(UserBadge).filter_by(user_id=user_id).count(), "achievements": self.db.query(Achievement).filter_by(user_id=user_id).count()},
            "mission_statistics": {"total": len(missions), "completed": sum(item.status == "completed" for item in missions), "completion_percentage": round(sum(item.status == "completed" for item in missions) / len(missions) * 100) if missions else 0},
            "charts": {"skill_match": [{"name": "Matched", "value": len(resume_skills & set(demand))}, {"name": "Missing", "value": len(set(demand) - resume_skills)}], "learning_progress": [{"name": "Completed", "value": len(completed_learning)}, {"name": "Remaining", "value": max(0, len(learning) - len(completed_learning))}], "completed_skills": [{"name": "Completed", "value": len(completed_skills)}, {"name": "Remaining", "value": max(0, len({item.skill_key for item in learning}) - len(completed_skills))}], "missing_skills": [{"name": name, "value": count} for name, count in demand.items() if name not in resume_skills][:8], "projects_completed": [{"name": "Completed", "value": projects_completed}, {"name": "Remaining", "value": max(0, sum(item.item_type == "project" for item in learning) - projects_completed)}], "daily_activity": trend, "weekly_activity": self._aggregate_activity(trend, 7), "monthly_activity": self._aggregate_activity(trend, 30)},
        }

    @staticmethod
    def _parse_date(value: str | None) -> date | None:
        try:
            return date.fromisoformat(value) if value else None
        except ValueError:
            return None

    @staticmethod
    def _split_skills(value: str) -> set[str]:
        return {_normalize_skill(item) for item in value.split(",") if item.strip()}

    @staticmethod
    def _completed_skills(items: list[LearningProgress]) -> set[str]:
        grouped: dict[tuple[str, str], list[LearningProgress]] = defaultdict(list)
        for item in items:
            if item.item_type == "topic":
                grouped[(item.roadmap_id, item.skill_key)].append(item)
        return {skill for (_, skill), rows in grouped.items() if rows and all(item.status == "completed" for item in rows)}

    @staticmethod
    def _xp_growth(items: list[LearningProgress]) -> list[dict[str, Any]]:
        totals: dict[str, int] = defaultdict(int)
        for item in items:
            if item.status == "completed":
                totals[item.updated_at.date().isoformat()] += item.xp_earned
        return [{"date": key, "xp": value} for key, value in sorted(totals.items())[-30:]]

    @staticmethod
    def _activity_series(items: list[LearningProgress], days: int) -> list[dict[str, Any]]:
        today = date.today()
        counts = defaultdict(int)
        for item in items:
            day = item.updated_at.date()
            if day >= today - timedelta(days=days - 1):
                counts[day.isoformat()] += 1
        return [{"date": (today - timedelta(days=offset)).isoformat(), "activity": counts[(today - timedelta(days=offset)).isoformat()]} for offset in range(days - 1, -1, -1)]

    @staticmethod
    def _aggregate_activity(series: list[dict[str, Any]], bucket_days: int) -> list[dict[str, Any]]:
        return [{"period": f"Last {bucket_days} days", "activity": sum(item["activity"] for item in series[-bucket_days:])}]


def _normalize_skill(value: str) -> str:
    return " ".join(value.casefold().replace("_", " ").split())
