from datetime import timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_token
from app.db.database import engine
from app.main import app
from app.models.content import CodingQuestion
from app.models.user import Role, User
from app.services.execution_service import ExecutionService, execution_service


def test_run_and_submit_forward_the_current_code_and_question(monkeypatch):
    with Session(engine) as db:
        user = User(full_name="Coding Payload", email="coding-payload@example.test", password_hash="unused", role=Role.USER, is_active=True)
        db.add(user); db.flush()
        question = db.query(CodingQuestion).filter_by(title="Find the largest element in an array").first()
        db.commit(); user_id, question_id = user.id, question.id

    captured = []
    monkeypatch.setattr(execution_service, "execute", lambda **kwargs: captured.append(kwargs) or {"status": "ACCEPTED", "message": "All tests passed.", "passed_tests": 3, "failed_tests": 0, "total_tests": 3, "runtime_ms": 1, "output": "25\n5\n-1"})
    token = create_token(user_id, "access", timedelta(minutes=5))
    code = "def find_largest(arr):\n    return max(arr)"
    with TestClient(app) as client:
        run = client.post("/coding-practice/run", headers={"Authorization": f"Bearer {token}"}, json={"question_id": question_id, "language": "python", "code": code})
        submit = client.post("/coding-practice/submit-code", headers={"Authorization": f"Bearer {token}"}, json={"question_id": question_id, "language": "python", "code": code})
    assert run.status_code == submit.status_code == 200
    assert [item["code"] for item in captured] == [code, code]
    assert [item["function_signature"] for item in captured] == [question.function_signature, question.function_signature]
    assert captured[0]["include_hidden"] is False
    assert captured[1]["include_hidden"] is True

    with Session(engine) as db:
        db.delete(db.get(User, user_id)); db.commit()


def test_empty_code_is_rejected_before_runner_dispatch():
    result = ExecutionService().execute(code="", language="python", public_tests=[], hidden_tests=[], custom_input=None, include_hidden=False, function_signature="find_largest(arr)")
    assert result["status"] == "INVALID_REQUEST"
    assert "solution" in result["message"]
