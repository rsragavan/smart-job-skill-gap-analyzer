from sqlalchemy import case, func, or_
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.job import Job, JobStatus
from app.models.company_intelligence import (
    CompanyInsight, CompanyInterviewQuestion, CompanyLocation, CompanyPreparation, CompanyResource, CompanyRole,
    CompanySelectionProcess, CompanySkill, StartupInformation, StartupRole,
)
from app.models.resume_history import ResumeHistory
from app.models.user_target import UserTarget
from app.models.career_gps import CareerGoal
from app.jobs.job_skill_extractor import JobSkillExtractor


class CompanyIntelligenceService:
    def list_companies(self, db: Session, search: str | None = None, location: str | None = None, industry: str | None = None, freshers: bool | None = None, internships: bool | None = None, role: str | None = None, skill: str | None = None, verified: bool | None = None, page: int = 1, page_size: int = 24):
        query = db.query(Company)
        search = search.strip() if search else None
        if search:
            term = f"%{search}%"
            query = query.filter(or_(Company.name.ilike(term), Company.tech_stack.ilike(term), Company.products.ilike(term), Company.industry.ilike(term), Company.headquarters.ilike(term), Company.country.ilike(term)))
        if role:
            query = query.join(CompanyRole, CompanyRole.company_id == Company.id).filter(CompanyRole.title.ilike(f"%{role}%"))
        if skill:
            query = query.join(CompanySkill, CompanySkill.company_id == Company.id).filter(or_(CompanySkill.skill.ilike(f"%{skill}%"), Company.tech_stack.ilike(f"%{skill}%")))
        if location:
            query = query.filter(or_(Company.headquarters.ilike(f"%{location}%"), Company.office_locations.ilike(f"%{location}%")))
        if industry:
            query = query.filter(Company.industry.ilike(f"%{industry}%"))
        if freshers is not None:
            query = query.filter(Company.freshers_hiring == freshers)
        if internships is not None:
            query = query.filter(Company.internship_available == internships)
        if verified is not None:
            query = query.filter(Company.verification_status == ("Verified" if verified else "Unverified"))
        rows = query.order_by(Company.name).distinct().offset(max(page - 1, 0) * page_size).limit(min(max(page_size, 1), 100)).all()
        counts = self._company_job_counts(db, rows)
        return [self._company_payload(row, counts.get(self._normalized(row.name))) for row in rows]

    def target_intelligence(self, db: Session, company_id: int | None, role_id: int | None, company_name: str, role_title: str):
        company = db.get(Company, company_id) if company_id else db.query(Company).filter(Company.name.ilike(company_name)).first()
        if not company:
            return {"company": None, "role": None, "selection_process": [], "preparation": [], "skills": [], "questions": [], "resources": []}
        role = db.query(CompanyRole).filter(CompanyRole.id == role_id, CompanyRole.company_id == company.id).first() if role_id else db.query(CompanyRole).filter(CompanyRole.company_id == company.id, CompanyRole.title.ilike(role_title)).first()
        roles = db.query(CompanyRole).filter(CompanyRole.company_id == company.id).all()
        skills = db.query(CompanySkill).filter(CompanySkill.company_id == company.id).all()
        role_id_value = role.id if role else None
        selection = db.query(CompanySelectionProcess).filter(CompanySelectionProcess.company_role_id == role_id_value).order_by(CompanySelectionProcess.round_number).all() if role_id_value else []
        preparation = db.query(CompanyPreparation).filter(CompanyPreparation.company_role_id == role_id_value).order_by(CompanyPreparation.learning_order).all() if role_id_value else []
        questions = db.query(CompanyInterviewQuestion).filter(CompanyInterviewQuestion.company_role_id == role_id_value).all() if role_id_value else []
        resources = db.query(CompanyResource).filter(CompanyResource.company_role_id == role_id_value).all() if role_id_value else []
        return {
            "company": {column.name: getattr(company, column.name) for column in Company.__table__.columns},
            "role": {"id": role.id, "title": role.title, "description": role.description, "required_skills": role.required_skills, "is_open": role.is_open} if role else None,
            "available_roles": [{"id": item.id, "title": item.title, "is_open": item.is_open} for item in roles],
            "selection_process": [{column.name: getattr(item, column.name) for column in CompanySelectionProcess.__table__.columns} for item in selection],
            "preparation": [{column.name: getattr(item, column.name) for column in CompanyPreparation.__table__.columns} for item in preparation],
            "skills": [{"skill": item.skill, "importance": item.importance} for item in skills],
            "questions": [{column.name: getattr(item, column.name) for column in CompanyInterviewQuestion.__table__.columns} for item in questions],
            "resources": [{column.name: getattr(item, column.name) for column in CompanyResource.__table__.columns} for item in resources],
        }

    def list_target_companies(self, db: Session, search: str | None = None) -> list[dict]:
        # Reference companies are intentionally inactive for job scraping but
        # remain selectable as interview-preparation targets.
        query = db.query(Company)
        if search and search.strip():
            query = query.filter(Company.name.ilike(f"%{search.strip()}%"))
        companies = query.order_by(Company.name).limit(30).all()
        return [{"id": company.id, "name": company.name, "roles": [{"id": role.id, "title": role.title} for role in self.list_roles(db, company.id)]} for company in companies]

    def generate_target_preparation(self, db: Session, user_id: int, company_name: str, role_title: str, experience_level: str, job_description: str | None = None) -> dict:
        from app.schemas.target import CustomTargetRequest
        from app.services.target_service import TargetService

        company = next((candidate for candidate in db.query(Company).all() if self._normalized(candidate.name) == self._normalized(company_name)), None)
        role = db.query(CompanyRole).filter(CompanyRole.company_id == company.id, CompanyRole.title.ilike(role_title.strip())).first() if company else None
        target_service = TargetService(db)
        if job_description and job_description.strip():
            target_service.set_custom(user_id, CustomTargetRequest(company=company.name if company else company_name.strip(), role=role_title.strip(), job_description=job_description.strip()))
        elif role:
            target_service.set_company_role(user_id, company.id, role.id)
        else:
            target_service.set_custom(user_id, CustomTargetRequest(company=company.name if company else company_name.strip(), role=role_title.strip(), job_description=f"{role_title.strip()} at {company.name if company else company_name.strip()}. Required skills include programming, problem solving, data structures, algorithms, OOP, SQL, DBMS, operating systems, communication, and resume projects."))
        target = db.query(UserTarget).filter_by(user_id=user_id, is_active=True).first()
        return self._preparation_payload(db, target, experience_level, role, bool(job_description and job_description.strip()))

    def preparation_for_active_target(self, db: Session, user_id: int) -> dict | None:
        target = db.query(UserTarget).filter_by(user_id=user_id, is_active=True).order_by(UserTarget.updated_at.desc()).first()
        if target is None:
            return None
        role = db.query(CompanyRole).filter_by(id=target.company_role_id, company_id=target.company_id).first() if target.company_role_id and target.company_id else None
        experience = db.query(CareerGoal).filter_by(user_id=user_id, goal_key="experience_level").first()
        return self._preparation_payload(db, target, experience.goal_value if experience else "fresher", role, target.source_type.value == "custom" if hasattr(target.source_type, "value") else str(target.source_type) == "custom")

    def _preparation_payload(self, db: Session, target, experience_level: str, role: CompanyRole | None, has_job_description: bool = False) -> dict:
        company = db.get(Company, target.company_id) if target.company_id else None
        resume = db.query(ResumeHistory).filter_by(user_id=target.user_id).order_by(ResumeHistory.uploaded_at.desc()).first()
        resume_skills = {self._normalized(item) for item in (resume.extracted_skills.split(",") if resume and resume.extracted_skills else []) if item.strip()}
        role_skills = self._split_topics(role.required_skills if role else None)
        job_skills = JobSkillExtractor().extract_skills(target.job_description or "") if target.job_description else []
        target_skills = list(target.matched_skills or []) + list(target.missing_skills or [])
        company_skills = self._split_topics(",".join(item.skill for item in db.query(CompanySkill).filter_by(company_id=target.company_id).all()) if target.company_id else None)
        required = list(dict.fromkeys(role_skills + list(job_skills) + target_skills + company_skills + ["Data Structures", "Problem Solving", "OOP", "SQL", "DBMS", "Communication", "Resume Projects"]))
        matched = sorted([skill for skill in required if self._normalized(skill) in resume_skills], key=str.casefold)
        missing = sorted([skill for skill in required if self._normalized(skill) not in resume_skills], key=str.casefold)
        rounds = db.query(CompanySelectionProcess).filter_by(company_role_id=role.id).order_by(CompanySelectionProcess.round_number).all() if role else []
        source_warning = "Company not currently available in the verified company database. A role-based preparation plan has been generated." if company is None else "Company-specific verified interview information is not available. A role-based preparation plan has been generated." if not rounds else "Interview process may vary for this role and hiring drive. Review the evidence label for each round."
        if rounds:
            round_payload = [self._round_payload(row) for row in rounds]
        else:
            round_payload = self._generated_rounds(target.role_title)
        questions = [{"question": row.question, "category": row.category, "difficulty": row.difficulty or "Medium", "round": None, "expected_answer": None, "explanation": row.preparation_tip, "source_type": "RECENT_REPORTED" if row.preparation_tip else "HISTORICAL_REPORTED"} for row in (db.query(CompanyInterviewQuestion).filter_by(company_role_id=role.id).limit(25).all() if role else [])]
        if not questions:
            questions = self._generated_questions(target.role_title)
        overall = round((len(matched) / len(required)) * 100) if required else 0
        categories = {"Programming": {"programming", "problem solving", "data structures", "algorithms"}, "Data Structures": {"data structures", "algorithms"}, "DBMS": {"dbms", "sql"}, "OOP": {"oop"}, "SQL": {"sql"}, "Communication": {"communication"}, "Resume Projects": {"resume projects"}}
        component_scores = {name: round(sum(self._normalized(skill) in resume_skills for skill in values) / len(values) * 100) for name, values in categories.items()}
        company_info = {"name": target.company, "location": company.headquarters if company else None, "industry": company.industry if company else None, "company_type": company.platform if company else "Unknown", "verified": bool(company and company.verification_status.casefold() == "verified")}
        return {"company": target.company, "company_info": company_info, "role": target.role_title, "experience_level": experience_level, "target_id": target.id, "job_description_source": "JOB_DESCRIPTION_DATA" if has_job_description else "COMPANY_ROLE_DATA" if role else "GENERATED_RECOMMENDATION", "resume_skills": sorted(resume_skills), "required_skills": required, "readiness": {"overall": overall, "components": component_scores, "provisional": not bool(rounds or role_skills), "matched_skills": matched, "missing_skills": missing}, "notice": source_warning, "rounds": round_payload, "preparation_stages": round_payload, "coding_topics": [skill for skill in required if self._normalized(skill) in {"arrays", "strings", "hashing", "searching", "sorting", "data structures", "algorithms", "sql", "problem solving"}], "questions": questions, "preparation_priority": [{"topic": skill, "priority": "HIGH" if index < 3 else "MEDIUM" if index < 7 else "LOW"} for index, skill in enumerate(missing)], "mock_interview": {"company_id": target.company_id, "company_role_id": target.company_role_id, "experience_level": experience_level}, "career_gps_next_steps": [f"Complete {skill}" for skill in missing[:5]], "data_status": "VERIFIED_COMPANY_DATA" if rounds else "GENERATED_RECOMMENDATION"}

    @staticmethod
    def _split_topics(value: str | None) -> list[str]:
        return [item.strip() for item in (value or "").replace(";", ",").replace("\n", ",").split(",") if item.strip()]

    @staticmethod
    def _round_payload(row) -> dict:
        return {"round_number": row.round_number, "round_name": row.title, "purpose": row.purpose or row.description, "estimated_duration": row.expected_duration, "difficulty": row.difficulty, "topics": CompanyIntelligenceService._split_topics(row.preparation_topics), "skills": [], "question_types": [], "preparation_tasks": [], "practice_questions": [], "success_tips": [], "source_type": "VERIFIED_COMPANY_DATA" if (row.verification_status or "").casefold() == "verified" else "RECENT_REPORTED" if row.last_verified_at else "HISTORICAL_REPORTED", "source_url": row.source_url}

    @staticmethod
    def _generated_rounds(role: str) -> list[dict]:
        names = [("Aptitude + Programming Fundamentals", "Assess foundational reasoning and programming."), ("Programming / Coding", "Assess practical coding and problem solving."), ("Technical Interview", "Assess role fundamentals and project understanding."), ("HR / Final Discussion", "Assess communication, motivation, and fit.")]
        topics = [["Quantitative Aptitude", "Logical Reasoning", "Programming Fundamentals"], ["Arrays", "Strings", "Searching", "Sorting", "Recursion", "Data Structures"], ["OOP", "DBMS", "SQL", "Operating Systems", role, "Resume Projects"], ["Tell me about yourself", "Why this company?", "Why this role?", "Projects", "Strengths and weaknesses"]]
        return [{"round_number": index, "round_name": name, "purpose": purpose, "estimated_duration": None, "difficulty": "Medium", "topics": topic_list, "skills": topic_list, "question_types": [], "preparation_tasks": [f"Practice {topic}" for topic in topic_list[:3]], "practice_questions": [], "success_tips": ["Explain your reasoning clearly.", "Use examples from your resume."], "source_type": "GENERATED_RECOMMENDATION", "source_url": None} for index, ((name, purpose), topic_list) in enumerate(zip(names, topics), start=1)]

    @staticmethod
    def _generated_questions(role: str) -> list[dict]:
        prompts = [("Programming", "Reverse an array and explain the time complexity."), ("Data Structures", "How would you find duplicate elements efficiently?"), ("OOP", "Explain the four core OOP concepts with an example."), ("DBMS", "What is normalization and why is it useful?"), ("SQL", "Write a query to find the second-highest salary."), ("Projects", f"Explain your most relevant project for a {role} role."), ("HR", "Why do you want to join this company?")]
        return [{"question": question, "category": category, "difficulty": "Medium", "round": None, "expected_answer": None, "explanation": "System-generated preparation question; it is not a prediction of the actual interview.", "source_type": "GENERATED_PRACTICE_QUESTION"} for category, question in prompts]

    def get_company(self, db: Session, company_id: int):
        company = db.get(Company, company_id)
        if not company:
            return None
        roles = db.query(CompanyRole).filter_by(company_id=company_id).all()
        counts = self._company_job_counts(db, [company])
        return {
            **{column.name: getattr(company, column.name) for column in Company.__table__.columns},
            **self._company_payload(company, counts.get(self._normalized(company.name))),
            "skills": [{"skill": item.skill, "importance": item.importance} for item in db.query(CompanySkill).filter_by(company_id=company_id).all()],
            "roles": [{"id": role.id, "title": role.title, "description": role.description, "is_open": role.is_open} for role in roles],
            "locations": [{"city": location.city, "state": location.state, "country": location.country, "is_tamil_nadu": location.is_tamil_nadu} for location in db.query(CompanyLocation).filter_by(company_id=company_id).all()],
            "insights": self._insight(db.query(CompanyInsight).filter_by(company_id=company_id).first()),
        }

    def _company_job_counts(self, db: Session, companies: list[Company]) -> dict[str, tuple[int, int]]:
        names = {self._normalized(item.name) for item in companies}
        if not names:
            return {}
        normalized_company = func.lower(func.trim(Job.company))
        rows = db.query(
            normalized_company,
            func.count(Job.id),
            func.sum(case((Job.status == JobStatus.ACTIVE, 1), else_=0)),
        ).filter(normalized_company.in_(names)).group_by(normalized_company).all()
        return {name: (int(total), int(active or 0)) for name, total, active in rows}

    @staticmethod
    def _verification(company: Company) -> tuple[str, bool]:
        status = (company.verification_status or "UNKNOWN").strip().upper()
        verified = status == "VERIFIED" and bool(company.data_source_url) and bool(company.last_verified_at)
        if verified:
            return "Verified", True
        if status == "UNVERIFIED":
            return "Unverified", False
        return "Unknown", False

    def _company_payload(self, company: Company, job_counts: tuple[int, int] | None) -> dict:
        total_jobs, active_jobs = job_counts or (0, 0)
        open_roles = active_jobs if total_jobs else None
        if active_jobs > 0:
            hiring_status = "Hiring"
        elif total_jobs > 0:
            hiring_status = "Not currently hiring"
        elif company.career_url:
            hiring_status = "Check careers page"
        else:
            hiring_status = "Unknown"
        verification_status, verified = self._verification(company)
        return {
            "id": company.id, "name": company.name, "logo_url": company.logo_url,
            "industry": company.industry, "headquarters": company.headquarters, "country": company.country,
            "hiring_status": hiring_status, "internship_available": company.internship_available,
            "freshers_hiring": company.freshers_hiring, "description": company.description,
            "tech_stack": company.tech_stack, "products": company.products, "career_url": company.career_url,
            "website_url": company.website_url, "open_roles": open_roles,
            "verification_status": verification_status, "verified": verified,
            "data_source_url": company.data_source_url, "last_verified_at": company.last_verified_at,
        }

    def get_role(self, db: Session, company_id: int, role_id: int):
        role = db.query(CompanyRole).filter_by(id=role_id, company_id=company_id).first()
        if not role:
            return None
        return {
            "id": role.id, "title": role.title, "description": role.description, "is_open": role.is_open,
            "selection_process": [{"round_number": row.round_number, "title": row.title, "description": row.description, "purpose": row.purpose, "preparation_topics": row.preparation_topics, "expected_duration": row.expected_duration, "difficulty": row.difficulty, "interview_mode": row.interview_mode, "freshers_eligible": row.freshers_eligible, "source_url": row.source_url, "last_verified_at": row.last_verified_at, "verification_status": row.verification_status} for row in db.query(CompanySelectionProcess).filter_by(company_role_id=role_id).order_by(CompanySelectionProcess.round_number).all()],
            "questions": [{"category": row.category, "question": row.question, "difficulty": row.difficulty, "preparation_tip": row.preparation_tip} for row in db.query(CompanyInterviewQuestion).filter_by(company_role_id=role_id).all()],
            "resources": [{"title": row.title, "url": row.url, "resource_type": row.resource_type} for row in db.query(CompanyResource).filter_by(company_role_id=role_id).all()],
        }

    def list_roles(self, db: Session, company_id: int):
        return db.query(CompanyRole).filter_by(company_id=company_id).order_by(CompanyRole.title).all()

    def preparation(self, db: Session, company_id: int, role_id: int | None = None):
        if role_id is not None:
            role = db.query(CompanyRole).filter_by(id=role_id, company_id=company_id).first()
            if not role:
                return None
            return db.query(CompanyPreparation).filter_by(company_role_id=role.id).order_by(CompanyPreparation.learning_order).all()
        role_ids = [role.id for role in self.list_roles(db, company_id)]
        return db.query(CompanyPreparation).filter(CompanyPreparation.company_role_id.in_(role_ids)).order_by(CompanyPreparation.learning_order).all() if role_ids else []

    def list_startups(self, db: Session, search: str | None = None, location: str | None = None, industry: str | None = None, funding_stage: str | None = None, founder: str | None = None, page: int = 1, page_size: int = 24, verification_status: str | None = None):
        query = db.query(StartupInformation)
        if verification_status and verification_status.casefold() != "verified":
            return []
        query = query.filter(or_(StartupInformation.verification_status == "verified", (StartupInformation.verification_status.is_(None) & StartupInformation.source_url.is_not(None) & StartupInformation.last_verified_at.is_not(None))))
        search = search.strip() if search else None
        if search:
            term = f"%{search}%"
            query = query.filter(or_(*(
                field.ilike(term) for field in (
                    StartupInformation.name,
                    StartupInformation.tech_stack,
                    StartupInformation.industry,
                    StartupInformation.location,
                    StartupInformation.state,
                    StartupInformation.country,
                    StartupInformation.founders,
                )
            )))
        for field, value in ((StartupInformation.location, location), (StartupInformation.industry, industry), (StartupInformation.funding_stage, funding_stage)):
            if value and field not in (StartupInformation.state, StartupInformation.country):
                query = query.filter(field.ilike(f"%{value.strip()}%"))
        if founder:
            query = query.filter(StartupInformation.founders.ilike(f"%{founder.strip()}%"))
        rows = query.order_by(StartupInformation.name).offset(max(page - 1, 0) * page_size).limit(min(max(page_size, 1), 100)).all()
        counts = self._job_counts(db, rows)
        return [self._startup_payload(row, counts.get(self._normalized(row.name))) for row in rows]

    def get_startup(self, db: Session, startup_id: int):
        startup = db.get(StartupInformation, startup_id)
        if startup is None:
            return None
        counts = self._job_counts(db, [startup]).get(self._normalized(startup.name))
        roles = db.query(StartupRole).filter_by(startup_id=startup.id).order_by(StartupRole.title).all()
        return {
            **self._startup_payload(startup, counts),
            "preparation_tips": startup.preparation_tips,
            "roles": [{"id": role.id, "startup_id": role.startup_id, "title": role.title, "is_open": role.is_open} for role in roles],
        }

    def list_startup_roles(self, db: Session, startup_id: int):
        if db.get(StartupInformation, startup_id) is None:
            return None
        return db.query(StartupRole).filter_by(startup_id=startup_id).order_by(StartupRole.title).all()

    @staticmethod
    def _normalized(value: str) -> str:
        return " ".join(value.casefold().split())

    def _job_counts(self, db: Session, startups: list[StartupInformation]) -> dict[str, tuple[int, int]]:
        names = {self._normalized(item.name) for item in startups}
        if not names:
            return {}
        normalized_company = func.lower(func.trim(Job.company))
        rows = db.query(
            normalized_company,
            func.count(Job.id),
            func.sum(case((Job.status == JobStatus.ACTIVE, 1), else_=0)),
        ).filter(normalized_company.in_(names)).group_by(normalized_company).all()
        return {name: (int(total), int(active or 0)) for name, total, active in rows}

    def _startup_payload(self, startup: StartupInformation, job_counts: tuple[int, int] | None):
        total_jobs, active_jobs = job_counts or (0, 0)
        # A stored zero is not evidence of zero jobs. Use it only when the
        # existing jobs table contains a matching company or a positive value
        # was explicitly supplied by a trusted import.
        open_roles = active_jobs if total_jobs else (startup.open_positions if startup.open_positions > 0 else None)
        if active_jobs > 0:
            hiring_status = "Hiring"
        elif total_jobs > 0:
            hiring_status = "Not currently hiring"
        elif startup.careers_url:
            hiring_status = "Check careers page"
        else:
            hiring_status = "Unknown"
        stored_status = (startup.verification_status or "").casefold()
        verified = stored_status == "verified" or (not stored_status and bool(startup.source_url and startup.last_verified_at))
        verification_status = "Verified" if verified else "Rejected" if stored_status == "rejected" else "Pending" if stored_status == "pending" or not stored_status else "Unknown"
        return {
            "id": startup.id, "name": startup.name, "industry": startup.industry, "location": startup.location,
            "funding_stage": startup.funding_stage, "latest_funding_amount": startup.latest_funding_amount,
            "founded_year": startup.founded_year, "employees": startup.employees, "website_url": startup.website_url,
            "careers_url": startup.careers_url, "open_positions": open_roles, "open_roles": open_roles,
            "tech_stack": startup.tech_stack, "description": startup.description, "state": startup.state,
            "country": startup.country, "public_email": startup.public_email, "hiring_status": hiring_status,
            "source_url": startup.source_url, "source_name": startup.source_name, "founders": startup.founders, "investors": startup.investors,
            "products": startup.products, "culture_summary": startup.culture_summary,
            "verification_status": verification_status, "verified": verified,
            "last_verified_at": startup.last_verified_at, "last_updated": startup.last_updated,
        }

    @staticmethod
    def _insight(insight: CompanyInsight | None):
        if not insight:
            return None
        return {column.name: getattr(insight, column.name) for column in CompanyInsight.__table__.columns}


company_intelligence_service = CompanyIntelligenceService()
