"""Target-aware coding practice endpoints.

The current deployment deliberately does not execute submitted source in the
FastAPI process. Run/submit expose the IDE contract and safe rubric results;
an external sandbox can be attached without changing the frontend contract.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import String
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.models.content import CodingQuestion
from app.models.mock_interview import AssessmentAttempt, CodingAttempt
from app.models.user import Role, User
from app.services.execution_service import SUPPORTED_LANGUAGES, execution_service
from app.services.coding_practice_service import coding_practice_service
from app.services.mock_interview_service import mock_interview_service

router = APIRouter(prefix="/coding-practice", tags=["Coding Practice"])


class CodeRequest(BaseModel):
    question_id: int
    code: str = Field(default="", max_length=100000)
    language: str = Field(default="python", max_length=30)
    custom_input: str | None = Field(default=None, max_length=20000)


class SubmitRequest(BaseModel):
    attempt_id: int = Field(gt=0)
    answers: dict[str, str] = Field(default_factory=dict)


class CodeSubmissionRequest(CodeRequest):
    pass


def _question(row: CodingQuestion) -> dict:
    if not all((row.description, row.input_format, row.output_format, row.constraints, row.examples, row.starter_code, row.function_signature)):
        raise HTTPException(422, "Question is not complete enough for practice")
    source_type = row.source_type if row.source_type in {"COMPANY_SOURCED", "CURATED", "GENERATED_RECOMMENDATION"} else ("CURATED" if row.source == "Curated educational content" else "GENERATED_RECOMMENDATION")
    return {"id": row.id, "title": row.title, "difficulty": row.difficulty, "category": row.category, "topic": row.topic, "skills": row.skills or [], "tags": row.tags or [], "source": source_type, "description": row.description, "input_format": row.input_format, "output_format": row.output_format, "constraints": row.constraints, "examples": row.examples, "explanation": row.explanation, "expected_complexity": row.expected_complexity, "expected_space_complexity": row.expected_space_complexity, "starter_code": row.starter_code, "function_signature": row.function_signature, "execution_mode": row.execution_mode, "test_cases": row.test_cases or [], "hints": row.hints or [], "source_type": source_type}


def _valid_query(db: Session, difficulty: str | None = None, topic: str | None = None, skill: str | None = None):
    query = db.query(CodingQuestion).filter(CodingQuestion.active.is_(True), CodingQuestion.verified.is_(True))
    if difficulty: query = query.filter(CodingQuestion.difficulty == difficulty.casefold())
    if topic: query = query.filter(CodingQuestion.topic.ilike(f"%{topic}%"))
    if skill: query = query.filter(CodingQuestion.skills.cast(String).ilike(f"%{skill}%"))
    return query.order_by(CodingQuestion.id)


@router.get("/questions")
def questions(difficulty: str | None = Query(None), topic: str | None = Query(None), skill: str | None = Query(None), db: Session = Depends(get_db), _: User = Depends(require_roles(Role.USER))):
    return [_question(row) for row in _valid_query(db, difficulty, topic, skill).all()]


@router.get("/questions/{question_id}")
def question(question_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(Role.USER))):
    row = _valid_query(db).filter(CodingQuestion.id == question_id).first()
    if not row: raise HTTPException(404, "Coding question not found")
    return _question(row)


@router.get("/recommended")
def recommended(topic: str | None = Query(None), skill: str | None = Query(None), difficulty: str | None = Query(None), experience_level: str = Query("fresher"), language: str | None = Query(None), db: Session = Depends(get_db), user: User = Depends(require_roles(Role.USER))):
    recommendation = coding_practice_service.recommend(db, user.id, topic=topic, skill=skill, difficulty=difficulty, experience_level=experience_level, language=language)
    return {"selection_mode": recommendation["selection_mode"], "target": recommendation["target"], "experience_level": recommendation["experience_level"], "language": recommendation["language"], "supported_languages": sorted(SUPPORTED_LANGUAGES), "message": "Recommended for your active target, resume skills, and skill gaps.", "questions": [{**_question(item["question"]), "recommendation_score": item["score"], "recommendation_reason": item["recommendation_reason"], "practice": item["practice"]} for item in recommendation["questions"]]}


@router.get("/runner-health")
def runner_health(_: User = Depends(require_roles(Role.USER))):
    return execution_service.health()


def _execute(row: CodingQuestion, payload: CodeRequest, user: User, db: Session, include_hidden: bool) -> dict:
    result = execution_service.execute(code=payload.code, language=payload.language, public_tests=row.test_cases or [], hidden_tests=row.hidden_test_cases or [], custom_input=payload.custom_input, include_hidden=include_hidden, function_signature=row.function_signature)
    attempt_id = None
    if include_hidden:
        attempt = CodingAttempt(user_id=user.id, question_id=row.id, language=payload.language, code=payload.code, status=result.get("status", "RUNNER_ERROR"), runtime_ms=result.get("runtime_ms"), passed_tests=result.get("passed_tests", 0), failed_tests=result.get("failed_tests", 0), total_tests=result.get("total_tests", 0), output=result.get("output"), error_message=result.get("error") or result.get("compilation_error"), is_submission=True)
        db.add(attempt)
        db.commit()
        attempt_id = attempt.id
    result.update({"attempt_id": attempt_id, "execution_mode": "LOCAL_RUNNER", "custom_input": payload.custom_input})
    return result


@router.post("/run")
def run(payload: CodeRequest, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    row = db.get(CodingQuestion, payload.question_id)
    if not row: raise HTTPException(404, "Coding question not found")
    return _execute(row, payload, user, db, False)


@router.post("/custom-test")
def custom_test(payload: CodeRequest, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    row = db.get(CodingQuestion, payload.question_id)
    if not row: raise HTTPException(404, "Coding question not found")
    return _execute(row, payload, user, db, False)


@router.post("/submit-code")
def submit_code(payload: CodeSubmissionRequest, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    row = db.get(CodingQuestion, payload.question_id)
    if not row: raise HTTPException(404, "Coding question not found")
    return _execute(row, payload, user, db, True)


@router.post("/submit")
def submit(payload: SubmitRequest, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return mock_interview_service.submit_assessment(db, user.id, payload.attempt_id, payload.answers)


@router.get("/history")
def history(user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    attempts = db.query(CodingAttempt).filter_by(user_id=user.id).order_by(CodingAttempt.submitted_at.desc()).limit(50).all()
    if attempts:
        questions_by_id = {row.id: row.title for row in db.query(CodingQuestion).filter(CodingQuestion.id.in_([item.question_id for item in attempts])).all()}
        return [{"id": row.id, "question": questions_by_id.get(row.question_id, "Coding question"), "question_id": row.question_id, "language": row.language, "score": f"{row.passed_tests}/{row.total_tests}" if row.total_tests else 0, "passed_tests": row.passed_tests, "failed_tests": row.failed_tests, "total_tests": row.total_tests, "status": row.status, "runtime_ms": row.runtime_ms, "submitted_at": row.submitted_at} for row in attempts]
    rows = db.query(AssessmentAttempt).filter_by(user_id=user.id).order_by(AssessmentAttempt.started_at.desc()).limit(50).all()
    return [{"id": row.id, "status": row.status, "score": row.score, "percentage": row.percentage, "passed": row.passed, "started_at": row.started_at, "completed_at": row.completed_at} for row in rows]


@router.get("/progress")
def progress(user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    rows = db.query(AssessmentAttempt).filter_by(user_id=user.id).all()
    completed = [row for row in rows if row.status == "completed"]
    coding_rows = db.query(CodingAttempt).filter_by(user_id=user.id).all()
    passed = [row for row in coding_rows if row.status in {"PASSED", "ACCEPTED"}]
    return {"attempted": len(rows), "solved": sum(1 for row in completed if row.passed), "accuracy": round(sum(row.percentage or 0 for row in completed) / len(completed)) if completed else 0, "coding_attempted": len(coding_rows), "coding_solved": len(passed), "coding_accuracy": round(sum((row.passed_tests / row.total_tests) * 100 for row in coding_rows if row.total_tests) / len([row for row in coding_rows if row.total_tests])) if any(row.total_tests for row in coding_rows) else 0}
