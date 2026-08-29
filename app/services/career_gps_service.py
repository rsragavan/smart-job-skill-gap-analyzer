import re
from collections import Counter, defaultdict
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.career_gps import CareerGoal, CareerProgress
from app.models.gamification import UserGamification
from app.models.job import Job, JobStatus
from app.models.job_application import JobApplication
from app.models.company import Company
from app.models.company_intelligence import CompanyInterviewQuestion, CompanyPreparation, CompanyResource, CompanyRole, CompanySelectionProcess, CompanySkill, StartupInformation
from app.models.learning_progress import LearningProgress
from app.models.mock_interview import CodingAttempt, MockInterview
from app.models.gamification import UserBadge
from app.models.resume_history import ResumeHistory
from app.models.user_target import UserTarget
from app.jobs.job_skill_extractor import JobSkillExtractor
from app.services.skill_gap_service import skill_gap_service


CAREER_PATHS = {
    "Backend": {"python", "java", "node.js", "nodejs", "go", "c#", "spring boot", "sql", "api"},
    "Frontend": {"react", "react.js", "angular", "vue", "typescript", "javascript", "html", "css"},
    "Full Stack": {"react", "javascript", "python", "node.js", "nodejs", "sql", "api"},
    "Cloud": {"aws", "azure", "gcp", "terraform", "kubernetes", "docker"},
    "DevOps": {"docker", "kubernetes", "jenkins", "terraform", "linux", "ci/cd"},
    "AI": {"python", "machine learning", "tensorflow", "pytorch", "llm"},
    "ML": {"python", "machine learning", "pandas", "numpy", "scikit-learn", "tensorflow"},
    "Cyber Security": {"linux", "networking", "python", "security", "iam", "siem"},
    "Data Engineering": {"python", "sql", "spark", "airflow", "kafka", "etl"},
    "Mobile": {"swift", "kotlin", "flutter", "react native", "android", "ios"},
}

CERTIFICATIONS = {
    "aws": "AWS Certified Cloud Practitioner",
    "azure": "Microsoft Azure Fundamentals",
    "kubernetes": "Certified Kubernetes Application Developer",
    "docker": "Docker Certified Associate",
    "terraform": "HashiCorp Terraform Associate",
    "python": "Python Institute PCAP",
    "sql": "Oracle SQL Associate",
}


def _normalize(value: str) -> str:
    value = re.sub(r"[^a-z0-9+#./-]+", " ", value.casefold())
    return " ".join(value.split())


class CareerGPSService:
    def __init__(self, db: Session):
        self.db = db
        self.extractor = JobSkillExtractor()

    def get_dashboard(self, user_id: int) -> dict[str, Any]:
        resume_skills = self._resume_skills(user_id)
        goals = {
            goal.goal_key: goal.goal_value
            for goal in self.db.query(CareerGoal).filter_by(user_id=user_id).all()
        }
        active_target = (
            self.db.query(UserTarget)
            .filter_by(user_id=user_id, is_active=True)
            .order_by(UserTarget.updated_at.desc())
            .first()
        )
        jobs = self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all()
        demand = Counter()
        job_skills: dict[int, set[str]] = {}
        for job in jobs:
            skills = {_normalize(skill) for skill in self.extractor.extract_skills(job.description or "") if skill}
            job_skills[job.id] = skills
            demand.update(skills)

        progress_items = self.db.query(LearningProgress).filter_by(user_id=user_id).all()
        if active_target:
            progress_items = [item for item in progress_items if active_target.roadmap_id and item.roadmap_id == active_target.roadmap_id]
        completed_items = [item for item in progress_items if item.status == "completed"]
        completed_skills = self._completed_skills(progress_items)
        completed_projects = len({(item.roadmap_id, item.skill_key, item.item_key) for item in completed_items if item.item_type == "project"})
        learning_progress = round((len(completed_items) / len(progress_items)) * 100) if progress_items else 0
        gamification = self.db.query(UserGamification).filter_by(user_id=user_id).first()
        xp = gamification.total_xp if gamification else 0
        resume_score = min(100, len(resume_skills) * 8)
        skill_score = min(100, len(completed_skills) * 12)
        project_score = min(100, completed_projects * 20)
        xp_score = min(100, round(xp / 60))
        readiness = round(resume_score * 0.30 + skill_score * 0.25 + project_score * 0.20 + xp_score * 0.15 + learning_progress * 0.10)

        target_company = (active_target.company if active_target else None) or goals.get("target_company")
        goal_role = (active_target.role_title if active_target else None) or goals.get("goal_role")
        current_match = float(active_target.match_percentage) if active_target else 0.0
        remaining_skills = list(active_target.missing_skills or []) if active_target else []

        if active_target:
            target_skill_set = {
                _normalize(skill)
                for skill in list(active_target.matched_skills or []) + list(active_target.missing_skills or [])
                if skill
            }
            role_readiness = round(current_match) if target_skill_set else self._role_readiness(resume_skills, demand)
            source = active_target.source_type.value if hasattr(active_target.source_type, "value") else str(active_target.source_type)
            if source == "scraped":
                company_jobs = [job for job in jobs if job.company.casefold() == active_target.company.casefold()]
                company_readiness = self._company_readiness(company_jobs, job_skills, resume_skills) if company_jobs else round(current_match)
            else:
                company_readiness = round(current_match)
            missing = [_normalize(skill) for skill in remaining_skills][:12] or [skill for skill, _ in demand.most_common(30) if skill not in resume_skills][:12]
        else:
            role_readiness = self._role_readiness(resume_skills, demand)
            company_jobs = [job for job in jobs if target_company and job.company.casefold() == target_company.casefold()]
            company_readiness = self._company_readiness(company_jobs, job_skills, resume_skills) if company_jobs else role_readiness
            missing = [skill for skill, _ in demand.most_common(30) if skill not in resume_skills][:12]

        interview_readiness = round(min(100, project_score * 0.45 + skill_score * 0.35 + xp_score * 0.20))
        job_readiness_score = round((role_readiness + company_readiness) / 2)
        recommendations = self._recommendations(missing, demand, resume_skills)
        coach = self._coach_payload(user_id, active_target, resume_skills, missing, demand, progress_items, recommendations, jobs)
        path_scores = self._career_paths(resume_skills | set(completed_skills), demand)
        selected_path = goals.get("career_path") or (path_scores[0]["path"] if path_scores else "Full Stack")
        roadmap_days = max(0, sum(item.xp_earned for item in progress_items if item.status != "completed") // 10)
        progress = self._get_or_create_progress(user_id)
        needs_commit = progress in self.db.new
        needs_commit = needs_commit or progress.career_path != selected_path or progress.goal_role != goal_role or progress.target_company != target_company or progress.readiness_score != readiness or progress.role_readiness != role_readiness or progress.company_readiness != company_readiness or progress.estimated_learning_days != roadmap_days
        progress.career_path = selected_path
        progress.goal_role = goal_role
        progress.target_company = target_company
        progress.readiness_score = readiness
        progress.role_readiness = role_readiness
        progress.company_readiness = company_readiness
        progress.estimated_learning_days = roadmap_days
        if needs_commit:
            self.db.commit()

        unified = self._unified_progress(user_id, active_target, resume_skills, progress_items, goals, missing)

        source_type = None
        if active_target is not None:
            source_type = active_target.source_type.value if hasattr(active_target.source_type, "value") else str(active_target.source_type)

        return {
            "readiness_score": readiness,
            "company_readiness": company_readiness,
            "role_readiness": role_readiness,
            "interview_readiness": interview_readiness,
            "job_readiness_score": job_readiness_score,
            "estimated_salary_growth": {"percentage": min(60, round(readiness * 0.45)), "basis": "Estimated from readiness, completed projects, and skill coverage."},
            "career_path": selected_path,
            "resume_skills": sorted(resume_skills),
            "completed_skills": sorted(completed_skills),
            "skill_gaps": missing,
            "learning_progress": learning_progress,
            "completed_projects": completed_projects,
            "xp": xp,
            "estimated_learning_days": roadmap_days,
            "technology_trends": [{"skill": skill, "demand": count} for skill, count in demand.most_common(10)],
            "market_demand": [{"skill": skill, "jobs": count} for skill, count in demand.most_common(10)],
            "recommendations": recommendations,
            "career_paths": path_scores,
            "career_timeline": self._timeline(user_id, progress_items),
            "goals": {"career_path": selected_path, "goal_role": progress.goal_role, "target_company": target_company},
            "active_target": {
                "id": active_target.id,
                "company": active_target.company,
                "role_title": active_target.role_title,
                "source_type": source_type,
                "match_percentage": current_match,
                "remaining_skills": remaining_skills,
                "roadmap_id": active_target.roadmap_id,
            } if active_target else None,
            "current_match_percentage": current_match,
            "remaining_skills": remaining_skills,
            "source_type": source_type,
            "skill_analysis": self._skill_analysis(resume_skills, missing, demand, active_target),
            "learning_plan": coach["learning_plan"],
            "interview_preparation": coach["interview_preparation"],
            "application_insights": coach["application_insights"],
            "recommendations": {**recommendations, "companies": coach["companies"], "startups": coach["startups"]},
            "skill_progress": {"completed": sorted(completed_skills), "in_progress": sorted({item.skill_key for item in progress_items if item.status == "in_progress"}), "missing": missing, "learning_percentage": learning_progress, "interview_readiness": interview_readiness, "company_readiness": company_readiness, "overall_readiness": readiness},
            "daily_goal": {"progress": gamification.daily_goal_progress, "target": gamification.daily_goal_target, "completed": gamification.daily_goal_progress >= gamification.daily_goal_target} if gamification else {"progress": 0, "target": 1, "completed": False},
            "weekly_goal": {"progress": gamification.weekly_goal_progress, "target": gamification.weekly_goal_target, "completed": gamification.weekly_goal_progress >= gamification.weekly_goal_target} if gamification else {"progress": 0, "target": 5, "completed": False},
            "target": unified["target"],
            "readiness": unified["readiness"],
            "skills": unified["skills"],
            "learning": unified["learning"],
            "coding": unified["coding"],
            "interview": unified["interview"],
            "roadmap": unified["roadmap"],
            "career_goals": unified["goals"],
            "gamification": unified["gamification"],
            "next_action": unified["next_action"],
        }

    def _unified_progress(self, user_id: int, target: UserTarget | None, resume_skills: set[str], progress_items: list[LearningProgress], goals: dict[str, str], missing: list[str]) -> dict[str, Any]:
        target_skills = skill_gap_service.normalize_skills(list(target.matched_skills or []) + list(target.missing_skills or [])) if target else []
        skill_value = float(target.match_percentage) if target and target_skills else None
        completed_learning = sum(item.status == "completed" for item in progress_items)
        learning_value = round(completed_learning / len(progress_items) * 100) if progress_items else None
        attempts = self.db.query(CodingAttempt).filter_by(user_id=user_id).all()
        solved = len({item.question_id for item in attempts if item.status in {"PASSED", "ACCEPTED"}})
        coding_value = round(solved / len(attempts) * 100) if attempts else None
        interviews = self.db.query(MockInterview).filter_by(user_id=user_id, status="completed").order_by(MockInterview.completed_at.desc()).all()
        scored_interviews = [item.overall_score for item in interviews if item.overall_score is not None]
        interview_value = round(sum(scored_interviews) / len(scored_interviews)) if scored_interviews else None
        goal_rows = self.db.query(CareerGoal).filter_by(user_id=user_id).all()
        goal_items = [{"key": item.goal_key, "value": item.goal_value, "status": "PENDING"} for item in goal_rows]
        components = {"skill_match": skill_value, "learning": learning_value, "coding": coding_value, "interview": interview_value, "goals": None}
        weights = {"skill_match": 40, "learning": 20, "coding": 15, "interview": 15, "goals": 10}
        available_weight = sum(weights[key] for key, value in components.items() if value is not None)
        readiness_score = round(sum(components[key] * weights[key] for key in components if components[key] is not None) / available_weight) if available_weight else None
        missing_details = [{"skill": skill, "priority": "HIGH" if index < 2 else "MEDIUM", "reason": f"{skill} is missing from the active target skill set.", "action": f"Improve {skill}"} for index, skill in enumerate(missing)]
        learning_rows = [{"skill": item.skill_key, "item": item.item_key, "status": item.status} for item in progress_items]
        current = next((item.skill_key for item in progress_items if item.status == "in_progress"), None)
        next_topic = next((item.skill_key for item in progress_items if item.status == "not_started"), None)
        badges = self.db.query(UserBadge).filter_by(user_id=user_id).order_by(UserBadge.unlocked_at.desc()).all()
        gamification = self.db.query(UserGamification).filter_by(user_id=user_id).first()
        next_action = self._next_action(resume_skills, target, missing, progress_items, attempts, interviews)
        return {
            "target": {"company": target.company, "role": target.role_title, "experience_level": goals.get("experience_level", "fresher"), "source_type": target.source_type.value if target and hasattr(target.source_type, "value") else (str(target.source_type) if target else None)} if target else None,
            "readiness": {"score": readiness_score, "status": "AVAILABLE" if readiness_score is not None else "NOT_ENOUGH_DATA", "components": components, "weights": weights},
            "skills": {"matched": list(target.matched_skills or []) if target else [], "missing": missing, "high_priority": [item["skill"] for item in missing_details if item["priority"] == "HIGH"], "medium_priority": [item["skill"] for item in missing_details if item["priority"] == "MEDIUM"], "low_priority": [], "details": missing_details},
            "learning": {"status": "AVAILABLE" if progress_items else "UNAVAILABLE", "completed": completed_learning, "in_progress": sum(item.status == "in_progress" for item in progress_items), "remaining": sum(item.status == "not_started" for item in progress_items), "progress_percentage": learning_value, "items": learning_rows},
            "coding": {"status": "AVAILABLE" if attempts else "UNAVAILABLE", "attempted": len(attempts), "solved": solved, "success_rate": coding_value, "recommended_practice": missing[:5]},
            "interview": {"status": "AVAILABLE" if interviews else "UNAVAILABLE", "completed": len(interviews), "average_score": interview_value, "last_interview": interviews[0].completed_at if interviews else None, "strong_areas": sorted({skill for item in interviews for skill in (item.strengths or [])}), "weak_areas": sorted({skill for item in interviews for skill in (item.weaknesses or [])}), "recommended_type": "Technical" if target else None},
            "roadmap": {"status": "AVAILABLE" if target and target.roadmap_id else "UNAVAILABLE", "roadmap_id": target.roadmap_id if target else None, "progress_percentage": learning_value, "completed_topics": completed_learning, "remaining_topics": len(progress_items) - completed_learning, "current_topic": current, "next_topic": next_topic},
            "goals": {"status": "AVAILABLE" if goal_items else "UNAVAILABLE", "active": goal_items, "completed": [], "pending": goal_items, "completion_tracking_available": False},
            "gamification": {"xp": gamification.total_xp if gamification else 0, "badges": [{"name": item.name, "description": item.description, "unlocked_at": item.unlocked_at} for item in badges], "current_streak": gamification.current_streak if gamification else 0, "longest_streak": gamification.longest_streak if gamification else 0, "daily_goal": {"progress": gamification.daily_goal_progress, "target": gamification.daily_goal_target} if gamification else None, "weekly_goal": {"progress": gamification.weekly_goal_progress, "target": gamification.weekly_goal_target} if gamification else None},
            "next_action": next_action,
        }

    @staticmethod
    def _next_action(resume_skills, target, missing, progress_items, attempts, interviews):
        if not resume_skills:
            return {"title": "Upload a newer resume", "reason": "A resume is required to calculate personalized skill gaps."}
        if not target:
            return {"title": "Select a job target", "reason": "Career GPS follows the active target job."}
        if missing and not progress_items:
            return {"title": f"Start learning {missing[0]}", "reason": f"{missing[0]} is a missing skill for the active target."}
        if missing and not attempts:
            return {"title": f"Practice {missing[0]}", "reason": "Coding practice has not been recorded for this target yet."}
        if not interviews:
            return {"title": "Complete a technical mock interview", "reason": "No completed mock interview is recorded yet."}
        return {"title": "Continue your roadmap", "reason": "Keep progressing on the active target roadmap."}

    def _coach_payload(self, user_id: int, target: UserTarget | None, resume_skills: set[str], missing: list[str], demand: Counter, progress_items: list[LearningProgress], recommendations: dict[str, list[dict[str, Any]]], jobs: list[Job]) -> dict[str, Any]:
        company_recommendations = []
        by_company: dict[str, list[set[str]]] = defaultdict(list)
        for job in jobs:
            skills = {_normalize(item) for item in self.extractor.extract_skills(job.description or "")}
            if skills:
                by_company[job.company].append(skills)
        for name, sets in by_company.items():
            score = round(sum(len(resume_skills & skills) / len(skills) * 100 for skills in sets) / len(sets))
            company_recommendations.append({"name": name, "match_percentage": score, "reason": "Matches your resume against active job requirements."})
        company_recommendations.sort(key=lambda item: item["match_percentage"], reverse=True)
        startups = self.db.query(StartupInformation).order_by(StartupInformation.name).limit(6).all()
        startup_recommendations = [{"id": item.id, "name": item.name, "industry": item.industry, "reason": "Verified startup profile available for exploration."} for item in startups]
        roadmap = []
        if target:
            from app.roadmap.roadmap_engine import roadmap_engine
            roadmap = roadmap_engine.generate_company_roadmap(target.company, target.role_title, target.match_percentage or 0, list(target.matched_skills or []), missing)["roadmap"]
        tasks = [topic for skill in roadmap for topic in (skill.get("topics") or [])]
        learning_plan = {"days": {"30": tasks[:30], "60": tasks[:60], "90": tasks[:90]}, "daily_tasks": tasks[:7], "weekly_goals": [skill.get("skill") for skill in roadmap[:12]], "projects": [project for skill in roadmap for project in (skill.get("projects") or [])], "resources": [topic.get("resource") for skill in roadmap for topic in (skill.get("topics") or []) if isinstance(topic, dict) and topic.get("resource")], "difficulty": [skill.get("difficulty") for skill in roadmap], "estimated_days": sum(skill.get("estimated_days", 0) for skill in roadmap), "progress_percentage": round(sum(item.status == "completed" for item in progress_items) / len(progress_items) * 100) if progress_items else 0}
        preparation = {"required_skills": sorted(resume_skills | set(missing)), "topics": [], "dsa_topics": [], "system_design_topics": [], "coding_questions": [], "hr_questions": [], "behavioral_questions": [], "checklist": [], "tips": [], "resources": []}
        if target and target.company_role_id:
            role = self.db.query(CompanyRole).filter_by(id=target.company_role_id).first()
            rows = self.db.query(CompanyPreparation).filter_by(company_role_id=target.company_role_id).order_by(CompanyPreparation.learning_order).all()
            questions = self.db.query(CompanyInterviewQuestion).filter_by(company_role_id=target.company_role_id).all()
            resources = self.db.query(CompanyResource).filter_by(company_role_id=target.company_role_id).all()
            rounds = self.db.query(CompanySelectionProcess).filter_by(company_role_id=target.company_role_id).order_by(CompanySelectionProcess.round_number).all()
            preparation["required_skills"] = [item.strip() for item in (role.required_skills or "").split(",") if item.strip()] or preparation["required_skills"]
            preparation["topics"] = [item.topic for item in rows]
            preparation["dsa_topics"] = [item.topic for item in rows if item.category.casefold() in {"dsa", "algorithms", "data structures"}]
            preparation["system_design_topics"] = [item.topic for item in rows if "system" in item.category.casefold()]
            preparation["coding_questions"] = [{"question": item.question, "difficulty": item.difficulty, "tip": item.preparation_tip} for item in questions if item.category.casefold() in {"coding", "technical"}]
            preparation["hr_questions"] = [item.question for item in questions if item.category.casefold() == "hr"]
            preparation["behavioral_questions"] = [item.question for item in questions if item.category.casefold() in {"behavioral", "culture"}]
            preparation["checklist"] = [item.title for item in rounds]
            preparation["tips"] = [item.preparation_tip for item in questions if item.preparation_tip]
            preparation["resources"] = [{"title": item.title, "url": item.url, "type": item.resource_type} for item in resources]
        applications = self.db.query(JobApplication).filter_by(user_id=user_id).all()
        job_ids = [item.job_id for item in applications if item.job_id]
        jobs_by_id = {job.id: job for job in self.db.query(Job).filter(Job.id.in_(job_ids)).all()} if job_ids else {}
        companies = {jobs_by_id[item.job_id].company if item.job_id in jobs_by_id else item.custom_company_name for item in applications}
        interview_count = sum(1 for item in applications if "interview" in item.status.casefold() or "round" in item.status.casefold() or item.status.casefold() in {"technical", "hr"})
        rejected_count = sum(item.status in {"Rejected", "Withdrawn"} for item in applications)
        offers = sum(item.status in {"Offer", "Offer Received", "Accepted"} for item in applications)
        application_matches = []
        for application in applications:
            job = jobs_by_id.get(application.job_id)
            if job:
                application_matches.append(self._job_match_percentage(resume_skills, job))
        return {"learning_plan": learning_plan, "interview_preparation": preparation, "application_insights": {"applications_sent": len(applications), "interviews": interview_count, "interview_rate": round(interview_count / len(applications) * 100) if applications else 0, "rejections": rejected_count, "rejection_rate": round(rejected_count / len(applications) * 100) if applications else 0, "offers": offers, "offer_rate": round(offers / len(applications) * 100) if applications else 0, "companies_applied": len({item for item in companies if item}), "average_match_percentage": round(sum(application_matches) / len(application_matches)) if application_matches else 0, "top_industries": []}, "companies": company_recommendations[:6], "startups": startup_recommendations}

    def _job_match_percentage(self, resume_skills: set[str], job: Job) -> float:
        required = {_normalize(skill) for skill in self.extractor.extract_skills(job.description or "") if skill}
        return round(len(resume_skills & required) / len(required) * 100, 2) if required else 0.0

    @staticmethod
    def _skill_analysis(resume_skills: set[str], missing: list[str], demand: Counter, target: UserTarget | None) -> dict[str, Any]:
        categories = {"Programming Languages": {"python", "java", "javascript", "typescript", "go", "c++", "c#", "ruby", "kotlin", "swift"}, "Frontend": {"react", "angular", "vue", "html", "css"}, "Backend": {"fastapi", "django", "flask", "node.js", "spring", "express", "rest api"}, "Database": {"sql", "postgresql", "mysql", "mongodb", "redis"}, "Cloud": {"aws", "azure", "gcp"}, "DevOps": {"docker", "kubernetes", "terraform", "jenkins", "linux"}, "Tools": {"git", "github", "postman"}, "Soft Skills": {"communication", "leadership", "teamwork"}}
        grouped = {name: {"current": sorted(resume_skills & values), "missing": sorted(set(missing) & values)} for name, values in categories.items()}
        strong = sorted(set(target.matched_skills or []) if target else resume_skills & set(demand), key=str.casefold)
        return {"current_skills": sorted(resume_skills), "missing_skills": missing, "strong_skills": strong, "weak_skills": missing[:], "skill_match_percentage": target.match_percentage if target else 0, "priority_skills": sorted(missing, key=lambda item: -demand.get(_normalize(item), 0))[:8], "learning_priority": [{"skill": item, "importance": demand.get(_normalize(item), 0), "estimated_days": 7 + min(21, demand.get(_normalize(item), 0))} for item in missing[:8]], "categories": grouped}

    def update_goals(self, user_id: int, values: dict[str, str | None]) -> dict[str, Any]:
        allowed = {"career_path", "goal_role", "target_company"}
        for key, value in values.items():
            if key not in allowed or value is None:
                continue
            goal = self.db.query(CareerGoal).filter_by(user_id=user_id, goal_key=key).first()
            if goal is None:
                self.db.add(CareerGoal(user_id=user_id, goal_key=key, goal_value=value))
            else:
                goal.goal_value = value
        self.db.commit()
        return self.get_dashboard(user_id)

    def _resume_skills(self, user_id: int) -> set[str]:
        resume = self.db.query(ResumeHistory).filter_by(user_id=user_id).order_by(ResumeHistory.uploaded_at.desc()).first()
        if not resume or not resume.extracted_skills:
            return set()
        return {_normalize(skill) for skill in resume.extracted_skills.split(",") if skill.strip()}

    def _goal(self, user_id: int, key: str) -> str | None:
        goal = self.db.query(CareerGoal).filter_by(user_id=user_id, goal_key=key).first()
        return goal.goal_value if goal else None

    @staticmethod
    def _completed_skills(items: list[LearningProgress]) -> set[str]:
        grouped: dict[tuple[str, str], list[LearningProgress]] = defaultdict(list)
        for item in items:
            if item.item_type == "topic":
                grouped[(item.roadmap_id, item.skill_key)].append(item)
        return {skill for (_, skill), rows in grouped.items() if rows and all(row.status == "completed" for row in rows)}

    @staticmethod
    def _role_readiness(resume_skills: set[str], demand: Counter) -> int:
        demanded = set(demand)
        return round((len(resume_skills & demanded) / len(demanded)) * 100) if demanded else min(100, len(resume_skills) * 8)

    @staticmethod
    def _company_readiness(jobs: list[Job], job_skills: dict[int, set[str]], resume_skills: set[str]) -> int:
        scores = [round(len(resume_skills & job_skills[job.id]) / len(job_skills[job.id]) * 100) for job in jobs if job_skills[job.id]]
        return round(sum(scores) / len(scores)) if scores else 0

    def _career_paths(self, skills: set[str], demand: Counter) -> list[dict[str, Any]]:
        results = []
        for path, required in CAREER_PATHS.items():
            normalized_required = {_normalize(skill) for skill in required}
            matched = skills & normalized_required
            results.append({"path": path, "score": round(len(matched) / len(normalized_required) * 100), "matched_skills": sorted(matched), "next_skills": sorted(normalized_required - skills, key=lambda item: -demand.get(item, 0))[:5]})
        return sorted(results, key=lambda item: item["score"], reverse=True)

    def _recommendations(self, missing: list[str], demand: Counter, resume_skills: set[str]) -> dict[str, list[dict[str, Any]]]:
        skills = [skill for skill in missing if skill not in resume_skills]
        return {
            "skills": [{"name": skill, "reason": f"Appears in {demand[skill]} active job descriptions."} for skill in skills[:6]],
            "certifications": [{"name": CERTIFICATIONS.get(skill, f"{skill.title()} professional certificate"), "skill": skill} for skill in skills[:5]],
            "projects": [{"title": f"Build a {skill.title()} portfolio project", "skill": skill, "estimated_days": 7 + (demand[skill] % 8)} for skill in skills[:5]],
        }

    def _timeline(self, user_id: int, items: list[LearningProgress]) -> list[dict[str, Any]]:
        events = [{"date": item.updated_at.isoformat(), "type": "learning", "title": f"{item.status.replace('_', ' ').title()}: {item.skill_key}", "detail": item.item_type} for item in sorted(items, key=lambda row: row.updated_at, reverse=True)[:8]]
        resumes = self.db.query(ResumeHistory).filter_by(user_id=user_id).order_by(ResumeHistory.uploaded_at.desc()).limit(3).all()
        events.extend({"date": resume.uploaded_at.isoformat(), "type": "resume", "title": "Resume analyzed", "detail": resume.filename} for resume in resumes)
        return sorted(events, key=lambda event: event["date"], reverse=True)[:10]

    def _get_or_create_progress(self, user_id: int) -> CareerProgress:
        progress = self.db.query(CareerProgress).filter_by(user_id=user_id).first()
        if progress is None:
            progress = CareerProgress(user_id=user_id)
            self.db.add(progress)
        return progress
