from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.models.user import Role, User
from app.schemas.mock_interview import AssessmentStart, AssessmentSubmit, InterviewAnswer, MockInterviewStart
from app.services.mock_interview_service import mock_interview_service

router = APIRouter(prefix="/interviews", tags=["Mock Interviews"])


@router.post("/start")
def start_interview(payload: MockInterviewStart, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return mock_interview_service.start(db, user.id, payload)


@router.get("/history")
def interview_history(user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return mock_interview_service.history(db, user.id)


@router.get("/{interview_id}")
def get_interview(interview_id: int, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return mock_interview_service.get_interview(db, user.id, interview_id)


@router.post("/{interview_id}/questions/{question_id}/answer")
def answer_question(interview_id: int, question_id: int, payload: InterviewAnswer, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return mock_interview_service.answer(db, user.id, interview_id, question_id, payload.answer)


@router.post("/{interview_id}/complete")
def complete_interview(interview_id: int, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return mock_interview_service.complete(db, user.id, interview_id)


assessment_router = APIRouter(prefix="/assessments", tags=["Coding Assessments"])


@assessment_router.get("")
def list_assessments(user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return mock_interview_service.assessments(db, user.id)


@assessment_router.post("/start")
def start_assessment(payload: AssessmentStart, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return mock_interview_service.start_assessment(db, user.id, payload.assessment_id)


@assessment_router.post("/{attempt_id}/submit")
def submit_assessment(attempt_id: int, payload: AssessmentSubmit, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return mock_interview_service.submit_assessment(db, user.id, attempt_id, payload.answers)


@assessment_router.get("/history")
def assessment_history(user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return mock_interview_service.assessment_history(db, user.id)
