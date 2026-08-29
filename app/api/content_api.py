from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.models.content import CodingQuestion, InterviewQuestion, LearningResource
from app.models.user import Role, User

router = APIRouter(tags=["Preparation Content"])
admin_only = require_roles(Role.ADMIN)


class ContentStatus(BaseModel):
    verified: bool | None = None
    active: bool | None = None


def _coding(row: CodingQuestion) -> dict:
    required = (row.description, row.input_format, row.output_format, row.constraints, row.examples, row.starter_code, row.function_signature)
    if not all(required):
        raise HTTPException(422, "Coding question is missing required problem data")
    source_type = row.source_type if row.source_type in {"COMPANY_SOURCED", "CURATED", "GENERATED_RECOMMENDATION"} else ("CURATED" if row.source == "Curated educational content" else "GENERATED_RECOMMENDATION")
    return {"id": row.id, "title": row.title, "description": row.description, "difficulty": row.difficulty, "category": row.category, "topic": row.topic, "skills": row.skills, "input_format": row.input_format, "output_format": row.output_format, "constraints": row.constraints, "examples": row.examples, "explanation": row.explanation, "expected_complexity": row.expected_complexity, "expected_space_complexity": row.expected_space_complexity, "tags": row.tags, "starter_code": row.starter_code, "function_signature": row.function_signature, "execution_mode": row.execution_mode, "test_cases": row.test_cases, "hints": row.hints, "source": row.source, "source_type": source_type, "verified": row.verified, "active": row.active}


@router.get("/interviews/coding-questions")
def coding_questions(difficulty: str | None = Query(None), topic: str | None = Query(None), db: Session = Depends(get_db), _: User = Depends(require_roles(Role.USER))):
    query = db.query(CodingQuestion).filter(CodingQuestion.active.is_(True), CodingQuestion.verified.is_(True))
    if difficulty: query = query.filter(CodingQuestion.difficulty == difficulty.casefold())
    if topic: query = query.filter(CodingQuestion.topic.ilike(f"%{topic}%"))
    return [_coding(row) for row in query.order_by(CodingQuestion.id).all()]


@router.get("/interviews/coding-questions/{question_id}")
def coding_question(question_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(Role.USER))):
    row = db.query(CodingQuestion).filter_by(id=question_id, active=True, verified=True).first()
    if not row: raise HTTPException(404, "Coding question not found")
    return _coding(row)


@router.get("/interviews/questions")
def interview_questions(category: str | None = None, topic: str | None = None, db: Session = Depends(get_db), _: User = Depends(require_roles(Role.USER))):
    query = db.query(InterviewQuestion).filter(InterviewQuestion.active.is_(True), InterviewQuestion.verified.is_(True))
    if category: query = query.filter(InterviewQuestion.category.ilike(category))
    if topic: query = query.filter(InterviewQuestion.topic.ilike(f"%{topic}%"))
    return [{"id": row.id, "question": row.question, "category": row.category, "topic": row.topic, "difficulty": row.difficulty, "sample_answer_guidance": row.sample_answer_guidance, "source": row.source} for row in query.order_by(InterviewQuestion.id).all()]


@router.get("/learning/resources")
def learning_resources(skill: str | None = None, topic: str | None = None, db: Session = Depends(get_db), _: User = Depends(require_roles(Role.USER))):
    query = db.query(LearningResource).filter(LearningResource.active.is_(True), LearningResource.verified.is_(True))
    if skill: query = query.filter(LearningResource.skill.ilike(f"%{skill}%"))
    if topic: query = query.filter(LearningResource.topic.ilike(f"%{topic}%"))
    return [{"id": row.id, "title": row.title, "description": row.description, "category": row.category, "topic": row.topic, "skill": row.skill, "resource_type": row.resource_type, "url": row.url, "source": row.source} for row in query.order_by(LearningResource.skill, LearningResource.id).all()]


@router.get("/admin/content/{content_type}")
def admin_content(content_type: str, _: User = Depends(admin_only), db: Session = Depends(get_db)):
    models = {"coding": CodingQuestion, "interview": InterviewQuestion, "learning": LearningResource}
    model = models.get(content_type)
    if model is None: return []
    return [{column.name: getattr(row, column.name) for column in model.__table__.columns} for row in db.query(model).order_by(model.id).all()]


@router.patch("/admin/content/{content_type}/{content_id}")
def update_content_status(content_type: str, content_id: int, payload: ContentStatus, _: User = Depends(admin_only), db: Session = Depends(get_db)):
    model = {"coding": CodingQuestion, "interview": InterviewQuestion, "learning": LearningResource}.get(content_type)
    if model is None: raise HTTPException(404, "Content type not found")
    row = db.get(model, content_id)
    if row is None: raise HTTPException(404, "Content not found")
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(row, key, value)
    db.commit()
    return {"id": row.id, "verified": row.verified, "active": row.active}
