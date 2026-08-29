from datetime import timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_token
from app.db.database import engine
from app.main import app
from app.models.content import InterviewQuestion
from app.models.mock_interview import MockInterview, MockInterviewQuestion
from app.models.user import Role, User
from app.models.user_target import TargetSourceType, UserTarget
from app.services.mock_interview_service import MockInterviewService


def _question(question_id: int, skill: str, difficulty: str = "medium", category: str = "Technical") -> InterviewQuestion:
    return InterviewQuestion(id=question_id, question=f"{skill} question {question_id}", category=category, topic=skill, skill=skill, difficulty=difficulty, sample_answer_guidance="Answer clearly.")


def test_missing_skill_selection_prioritizes_target_gap_and_avoids_duplicates():
    target = UserTarget(user_id=1, source_type=TargetSourceType.CUSTOM, company="Example", role_title="Backend Developer", matched_skills=["Python"], missing_skills=["Docker", "PostgreSQL"], match_percentage=50)
    rows = [_question(1, "Python"), _question(2, "Docker"), _question(3, "PostgreSQL"), _question(4, "React"), _question(5, "Docker")]

    selected = MockInterviewService._select_questions(rows, target, "technical", "fresher", limit=4)

    assert {row.skill for row in selected[:2]} <= {"Docker", "PostgreSQL"}
    assert len({row.id for row in selected}) == len(selected)


def test_experience_level_maps_to_compatible_difficulties_with_fallback():
    target = UserTarget(user_id=1, source_type=TargetSourceType.CUSTOM, company="Example", role_title="Backend Developer", matched_skills=[], missing_skills=[], match_percentage=0)
    rows = [_question(1, "Python", "easy"), _question(2, "Docker", "medium"), _question(3, "Kubernetes", "hard")]

    fresher = MockInterviewService._select_questions(rows, target, "technical", "fresher", limit=10)
    advanced = MockInterviewService._select_questions(rows, target, "technical", "advanced", limit=10)
    fallback = MockInterviewService._select_questions([_question(4, "Git", "easy")], target, "technical", "advanced", limit=10)

    assert {row.difficulty for row in fresher} == {"easy", "medium"}
    assert {row.difficulty for row in advanced} == {"medium", "hard"}
    assert [row.difficulty for row in fallback] == ["easy"]


def test_type_filter_supports_hr_behavioral_backend_database_cloud():
    rows = [
        _question(1, "Teamwork", category="HR"),
        _question(2, "Projects", category="Behavioral"),
        _question(3, "FastAPI", category="Technical"),
        _question(4, "SQL", category="Technical"),
        _question(5, "AWS", category="Cloud"),
    ]

    assert [row.id for row in MockInterviewService._eligible_by_type(rows, {"hr"})] == [1]
    assert [row.id for row in MockInterviewService._eligible_by_type(rows, {"behavioral"})] == [2]
    assert {row.id for row in MockInterviewService._eligible_by_type(rows, {"technical", "programming"})} == {3, 4}
    assert [row.id for row in MockInterviewService._eligible_by_type(rows, {"sql", "database"})] == [4]
    assert [row.id for row in MockInterviewService._eligible_by_type(rows, {"cloud", "devops"})] == [5]


def test_start_interview_api_preserves_fk_safe_snapshots_and_authentication():
    email = "mock-upgrade-user@example.test"
    with Session(engine) as db:
        old = db.query(User).filter_by(email=email).first()
        if old:
            db.delete(old)
            db.commit()
        user = User(full_name="Mock Upgrade User", email=email, password_hash="unused", role=Role.USER, is_active=True)
        db.add(user)
        db.flush()
        target = UserTarget(user_id=user.id, source_type=TargetSourceType.CUSTOM, company="Example", role_title="Backend Developer", match_percentage=50, matched_skills=["Python"], missing_skills=["Docker", "PostgreSQL"], is_active=True)
        db.add(target)
        db.commit()
        user_id = user.id

    token = create_token(user_id, "access", timedelta(minutes=5))
    with TestClient(app) as client:
        assert client.post("/interviews/start", json={"interview_type": "technical", "experience_level": "fresher"}).status_code == 401
        invalid = client.post("/interviews/start", json={"interview_type": "invalid", "experience_level": "fresher"}, headers={"Authorization": f"Bearer {token}"})
        assert invalid.status_code == 422
        response = client.post("/interviews/start", json={"interview_type": "technical", "experience_level": "fresher"}, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["questions"]
    assert len({question["id"] for question in payload["questions"]}) == len(payload["questions"])

    with Session(engine) as db:
        interview = db.query(MockInterview).filter_by(id=payload["id"], user_id=user_id).first()
        snapshots = db.query(MockInterviewQuestion).filter_by(interview_id=payload["id"]).all()
        assert interview is not None
        assert snapshots
        assert all(row.source_question_id is None for row in snapshots)
        assert any(row.skill in {"Docker", "PostgreSQL", "Python", "FastAPI", "SQL"} for row in snapshots)
        db.delete(db.get(User, user_id))
        db.commit()


def test_start_interview_returns_clear_error_without_active_target():
    email = "mock-no-target@example.test"
    with Session(engine) as db:
        old = db.query(User).filter_by(email=email).first()
        if old:
            db.delete(old)
            db.commit()
        user = User(full_name="No Target User", email=email, password_hash="unused", role=Role.USER, is_active=True)
        db.add(user)
        db.commit()
        user_id = user.id

    token = create_token(user_id, "access", timedelta(minutes=5))
    with TestClient(app) as client:
        response = client.post("/interviews/start", json={"interview_type": "technical", "experience_level": "fresher"}, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Please select an active target job before starting a mock interview."

    with Session(engine) as db:
        db.delete(db.get(User, user_id))
        db.commit()


def test_answer_complete_history_and_ownership_are_preserved():
    with Session(engine) as db:
        user = User(full_name="Interview Flow User", email="interview-flow@example.test", password_hash="unused", role=Role.USER, is_active=True)
        other = User(full_name="Other User", email="interview-other@example.test", password_hash="unused", role=Role.USER, is_active=True)
        db.add_all([user, other]); db.flush()
        db.add(UserTarget(user_id=user.id, source_type=TargetSourceType.CUSTOM, company="Example", role_title="Backend Developer", matched_skills=["Python"], missing_skills=["Docker"], is_active=True))
        db.commit(); user_id, other_id = user.id, other.id

    token = create_token(user_id, "access", timedelta(minutes=5))
    other_token = create_token(other_id, "access", timedelta(minutes=5))
    with TestClient(app) as client:
        started = client.post("/interviews/start", json={"interview_type": "technical", "experience_level": "fresher"}, headers={"Authorization": f"Bearer {token}"})
        assert started.status_code == 200
        interview = started.json()
        question_id = interview["questions"][0]["id"]
        answered = client.post(f"/interviews/{interview['id']}/questions/{question_id}/answer", json={"answer": "I would explain the design, trade-offs, edge cases, and testing approach."}, headers={"Authorization": f"Bearer {token}"})
        assert answered.status_code == 200
        completed = client.post(f"/interviews/{interview['id']}/complete", headers={"Authorization": f"Bearer {token}"})
        assert completed.status_code == 200
        assert completed.json()["status"] == "completed"
        assert client.get("/interviews/history", headers={"Authorization": f"Bearer {token}"}).status_code == 200
        assert client.get(f"/interviews/{interview['id']}", headers={"Authorization": f"Bearer {other_token}"}).status_code == 404

    with Session(engine) as db:
        db.delete(db.get(User, user_id)); db.delete(db.get(User, other_id)); db.commit()
