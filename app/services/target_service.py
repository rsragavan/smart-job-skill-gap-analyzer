"""Orchestrate active career targets for scraped jobs and custom JDs."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.career_gps import CareerGoal
from app.models.job import Job, JobStatus
from app.models.company import Company
from app.models.company_intelligence import CompanyRole
from app.models.resume_history import ResumeHistory
from app.models.user_target import TargetSourceType, UserTarget
from app.schemas.roadmap import RoadmapResponse
from app.schemas.target import CustomTargetRequest, TargetResponse
from app.services.job_match_service import JobMatchService
from app.services.roadmap_service import roadmap_service
from app.services.skill_gap_service import skill_gap_service
from app.models.content import CodingQuestion, InterviewQuestion, LearningResource
from app.models.job import JobStatus
from app.services.mock_interview_service import MockInterviewService


class TargetService:
    def __init__(self, db: Session):
        self.db = db
        self.match_service = JobMatchService()

    def get_active(self, user_id: int) -> TargetResponse | None:
        target = self._active_row(user_id)
        return self._to_response(target, self._stored_analysis(target) if target else None) if target else None

    def set_from_job(self, user_id: int, job_id: int) -> TargetResponse:
        job = (
            self.db.query(Job)
            .filter(Job.id == job_id, Job.status == JobStatus.ACTIVE)
            .first()
        )
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

        resume_skills = self._require_resume_skills(user_id)
        match = self.match_service.match_job(resume_skills, job)
        company = self.db.query(Company).filter(Company.name == job.company).first()
        role = self.db.query(CompanyRole).filter(CompanyRole.company_id == company.id, CompanyRole.title.ilike(job.title)).first() if company else None
        target = self._replace_active(
            user_id=user_id,
            source_type=TargetSourceType.SCRAPED,
            job_id=job.id,
            company=job.company,
            role_title=job.title,
            location=job.location,
            job_description=job.description,
            match_percentage=match["match_percentage"],
            matched_skills=match["matched_skills"],
            missing_skills=match["missing_skills"],
        )
        target.company_id = company.id if company else None
        target.company_role_id = role.id if role else None
        self._sync_career_goals(user_id, company=job.company, role=job.title, experience="fresher")
        self.db.commit()
        self.db.refresh(target)
        return self._to_response(target, match)

    def set_custom(self, user_id: int, payload: CustomTargetRequest) -> TargetResponse:
        resume_skills = self._require_resume_skills(user_id)
        match = self.match_service.match_text(
            resume_skills,
            payload.job_description,
            company=payload.company.strip(),
            role=payload.role.strip(),
            location=payload.location.strip() if payload.location else None,
        )
        company = self.db.query(Company).filter(Company.name.ilike(payload.company.strip())).first()
        role = self.db.query(CompanyRole).filter(CompanyRole.company_id == company.id, CompanyRole.title.ilike(payload.role.strip())).first() if company else None
        target = self._replace_active(
            user_id=user_id,
            source_type=TargetSourceType.CUSTOM,
            job_id=None,
            company=payload.company.strip(),
            role_title=payload.role.strip(),
            location=payload.location.strip() if payload.location else None,
            job_description=payload.job_description.strip(),
            match_percentage=match["match_percentage"],
            matched_skills=match["matched_skills"],
            missing_skills=match["missing_skills"],
        )
        target.company_id = company.id if company else None
        target.company_role_id = role.id if role else None
        self._sync_career_goals(user_id, company=target.company, role=target.role_title, experience="fresher")
        self.db.commit()
        self.db.refresh(target)
        return self._to_response(target, match)

    def set_company_role(self, user_id: int, company_id: int, role_id: int) -> TargetResponse:
        company = self.db.get(Company, company_id)
        role = self.db.query(CompanyRole).filter_by(id=role_id, company_id=company_id).first()
        if company is None or role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company role not found")
        resume_skills = self._require_resume_skills(user_id)
        description = role.description or company.description or role.title
        match = self.match_service.match_text(resume_skills, description, company=company.name, role=role.title, location=company.headquarters)
        target = self._replace_active(user_id=user_id, source_type=TargetSourceType.CUSTOM, job_id=None, company=company.name, role_title=role.title, location=company.headquarters, job_description=description, match_percentage=match["match_percentage"], matched_skills=match["matched_skills"], missing_skills=match["missing_skills"])
        target.company_id = company.id
        target.company_role_id = role.id
        self._sync_career_goals(user_id, company=company.name, role=role.title, experience="fresher")
        self.db.commit(); self.db.refresh(target)
        return self._to_response(target, match)

    def generate_roadmap(self, user_id: int) -> RoadmapResponse:
        target = self._active_row(user_id)
        if target is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active target. Choose a company or paste a job description first.",
            )

        roadmap = roadmap_service.generate(
            company=target.company,
            role=target.role_title,
            match_percentage=target.match_percentage or 0,
            matched_skills=list(target.matched_skills or []),
            missing_skills=list(target.missing_skills or []),
        )
        target.roadmap_id = roadmap["roadmap_id"] if isinstance(roadmap, dict) else roadmap.roadmap_id
        self.db.commit()
        if isinstance(roadmap, dict):
            return RoadmapResponse(**roadmap)
        return roadmap

    def clear_active(self, user_id: int) -> None:
        for row in self.db.query(UserTarget).filter_by(user_id=user_id, is_active=True).all():
            row.is_active = False
        self.db.commit()

    def skill_gap(self, user_id: int) -> dict:
        target = self._active_row(user_id)
        if target is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active target selected.")
        resume = self.db.query(ResumeHistory).filter_by(user_id=user_id).order_by(ResumeHistory.uploaded_at.desc()).first()
        resume_skills = [item.strip() for item in (resume.extracted_skills if resume else "").split(",") if item.strip()]
        target_skills = skill_gap_service.extract_target_skills(target.role_title, target.job_description)
        target_skills = skill_gap_service.normalize_skills(target_skills + list(target.matched_skills or []) + list(target.missing_skills or []))
        market_counts = {}
        for job in self.db.query(Job).filter(Job.status == JobStatus.ACTIVE).all():
            for skill in skill_gap_service.extract_target_skills(job.title, job.description):
                key = skill_gap_service._key(skill)
                market_counts[key] = market_counts.get(key, 0) + 1
        analysis = skill_gap_service.analyze(resume_skills, target_skills, role=target.role_title, job_description=target.job_description, market_counts=market_counts)
        missing_keys = {skill_gap_service._key(item) for item in analysis["missing_skills"]}
        learning = [{"title": item.title, "skill": item.skill, "reason": f"{item.skill} is a skill gap for this target."} for item in self.db.query(LearningResource).filter(LearningResource.active.is_(True), LearningResource.verified.is_(True)).all() if skill_gap_service._key(item.skill) in missing_keys][:8]
        coding = []
        for item in self.db.query(CodingQuestion).filter(CodingQuestion.active.is_(True), CodingQuestion.verified.is_(True)).order_by(CodingQuestion.id).all():
            values = {skill_gap_service._key(value) for value in [item.topic, *(item.skills or []), item.title]}
            matched = values & missing_keys
            if matched:
                coding.append({"id": item.id, "title": item.title, "topic": item.topic, "difficulty": item.difficulty, "reason": f"{sorted(matched)[0]} is a missing skill for your target."})
            if len(coding) >= 8: break
        interviews = []
        for item in self.db.query(InterviewQuestion).filter(InterviewQuestion.active.is_(True), InterviewQuestion.verified.is_(True)).order_by(InterviewQuestion.id).all():
            values = {skill_gap_service._key(value) for value in [item.topic, item.skill, item.question]}
            matched = values & missing_keys
            if matched:
                interviews.append({"id": item.id, "question": item.question, "category": item.category, "topic": item.topic, "source": "CURATED", "reason": f"{sorted(matched)[0]} is relevant to your role and is currently a skill gap."})
            if len(interviews) >= 8: break
        roadmap = roadmap_service.generate(target.company, target.role_title, analysis["match_percentage"], analysis["matched_skills"], analysis["missing_skills"])
        return {"target": {"company": target.company, "role": target.role_title, "source_type": target.source_type.value if hasattr(target.source_type, "value") else str(target.source_type)}, "resume_skills": skill_gap_service.normalize_skills(resume_skills), **analysis, "learning_recommendations": learning, "coding_recommendations": coding, "interview_recommendations": interviews, "roadmap": roadmap}

    def _active_row(self, user_id: int) -> UserTarget | None:
        return (
            self.db.query(UserTarget)
            .filter_by(user_id=user_id, is_active=True)
            .order_by(UserTarget.updated_at.desc())
            .first()
        )

    def _require_resume_skills(self, user_id: int) -> list[str]:
        resume = (
            self.db.query(ResumeHistory)
            .filter_by(user_id=user_id)
            .order_by(ResumeHistory.uploaded_at.desc())
            .first()
        )
        if resume is None or not (resume.extracted_skills or "").strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Upload a resume before selecting a target.",
            )
        return [skill.strip() for skill in resume.extracted_skills.split(",") if skill.strip()]

    def _replace_active(
        self,
        *,
        user_id: int,
        source_type: TargetSourceType,
        job_id: int | None,
        company: str,
        role_title: str,
        location: str | None,
        job_description: str | None,
        match_percentage: float,
        matched_skills: list[str],
        missing_skills: list[str],
    ) -> UserTarget:
        for row in self.db.query(UserTarget).filter_by(user_id=user_id, is_active=True).all():
            row.is_active = False

        target = UserTarget(
            user_id=user_id,
            source_type=source_type,
            job_id=job_id,
            company=company,
            role_title=role_title,
            location=location,
            job_description=job_description,
            match_percentage=match_percentage,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            roadmap_id=None,
            is_active=True,
        )
        self.db.add(target)
        self.db.flush()
        return target

    def _sync_career_goals(self, user_id: int, *, company: str, role: str, experience: str = "fresher") -> None:
        for key, value in (("target_company", company), ("goal_role", role), ("experience_level", experience)):
            goal = self.db.query(CareerGoal).filter_by(user_id=user_id, goal_key=key).first()
            if goal is None:
                self.db.add(CareerGoal(user_id=user_id, goal_key=key, goal_value=value))
            else:
                goal.goal_value = value

    @staticmethod
    def _stored_analysis(target: UserTarget) -> dict:
        details = [{"skill": skill, "priority": "MEDIUM", "reason": f"{skill} appears in the target requirements but was not detected in the resume.", "job_market": {"jobs": None, "status": "INSUFFICIENT_DATA"}} for skill in target.missing_skills or []]
        return {"missing_skill_details": details, "skill_gap_explanations": {"matched": "Matched because the skill appears in both the resume and target requirements.", "missing": "Missing because the skill appears in the target requirements but was not detected in the resume."}}

    @staticmethod
    def _to_response(target: UserTarget, analysis: dict | None = None) -> TargetResponse:
        source = target.source_type.value if hasattr(target.source_type, "value") else str(target.source_type)
        return TargetResponse(
            id=target.id,
            source_type=source,  # type: ignore[arg-type]
            job_id=target.job_id,
            company_id=target.company_id,
            company_role_id=target.company_role_id,
            company=target.company,
            role_title=target.role_title,
            location=target.location,
            job_description=target.job_description,
            match_percentage=target.match_percentage or 0,
            matched_skills=list(target.matched_skills or []),
            missing_skills=list(target.missing_skills or []),
            missing_skill_details=(analysis or {}).get("missing_skill_details", []),
            skill_gap_explanations=(analysis or {}).get("skill_gap_explanations", {}),
            roadmap_id=target.roadmap_id,
            is_active=target.is_active,
            created_at=target.created_at,
            updated_at=target.updated_at,
        )
