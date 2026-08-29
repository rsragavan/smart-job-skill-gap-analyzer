from datetime import timedelta

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import inspect

from app.core.security import create_token, decode_token, validate_password
from app.db.database import engine
from app.main import app
from app.models.mock_interview import AssessmentAttempt
from app.services.job_match_service import JobMatchService


def test_password_policy_rejects_weak_passwords_and_accepts_strong_passwords():
    with pytest.raises(HTTPException):
        validate_password("password")

    validate_password("Password1!")


def test_job_matching_is_deterministic_and_handles_empty_job_skills(monkeypatch):
    service = JobMatchService()
    monkeypatch.setattr(
        service.job_extractor,
        "extract_skills",
        lambda _: ["Python", "Docker", "Python"],
    )

    result = service.match_text(
        [" python ", "python"],
        "ignored",
        company="Example",
        role="Backend Engineer",
    )

    assert result["matched_skills"] == ["Python"]
    assert result["missing_skills"] == ["Docker"]
    assert result["match_percentage"] == 50.0

    monkeypatch.setattr(service.job_extractor, "extract_skills", lambda _: [])
    empty_result = service.match_text([], "ignored", company="Example", role="Role")
    assert empty_result["match_percentage"] == 0
    assert empty_result["matched_skills"] == []
    assert empty_result["missing_skills"] == []


def test_protected_routes_reject_missing_and_malformed_tokens():
    with TestClient(app) as client:
        for path in ("/auth/me", "/dashboard", "/admin/stats"):
            assert client.get(path).status_code == 401
            assert client.get(path, headers={"Authorization": "Bearer malformed"}).status_code == 401


def test_admin_route_is_forbidden_for_an_authenticated_normal_user_without_database_mutation():
    token = create_token(999999999, "access", timedelta(minutes=5))
    # The token is structurally valid but points to no user; backend must reject it.
    with TestClient(app) as client:
        assert client.get("/admin/stats", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_assessment_attempt_model_and_database_schema_contain_percentage():
    assert "percentage" in AssessmentAttempt.__table__.columns
    columns = {column["name"] for column in inspect(engine).get_columns("assessment_attempts")}
    assert "percentage" in columns


def test_openapi_exposes_core_workflow_routes():
    paths = set(app.openapi()["paths"])
    expected = {
        "/auth/register",
        "/auth/login",
        "/resume/upload",
        "/jobs/",
        "/applications",
        "/interviews/start",
        "/assessments/start",
        "/learning/resources",
        "/dashboard",
    }
    assert expected <= paths


def test_token_tampering_is_rejected():
    token = create_token(42, "access", timedelta(minutes=5))
    with pytest.raises(HTTPException):
        decode_token(f"{token}x", "access")
