from app.services.skill_gap_service import SkillGapService


def test_taxonomy_aliases_are_canonical_and_duplicate_free():
    service = SkillGapService()
    assert service.normalize_skills(["postgres", "PostgreSQL", " python "]) == ["PostgreSQL", "Python"]


def test_matching_percentage_and_missing_skills_are_explainable():
    result = SkillGapService().analyze(
        ["Python", "FastAPI", "postgres"],
        ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
        role="Backend Developer",
        job_description="Python FastAPI PostgreSQL Docker AWS Docker",
    )
    assert result["matched_skills"] == ["FastAPI", "PostgreSQL", "Python"]
    assert result["missing_skills"] == ["AWS", "Docker"]
    assert result["match_percentage"] == 60.0
    assert result["missing_skill_details"][0]["priority"] == "HIGH"
    assert "target requirements" in result["missing_skill_details"][0]["reason"]


def test_priority_can_be_high_medium_or_low_without_fabricating_market_data():
    result = SkillGapService().analyze(
        [],
        ["Python", "Docker", "HTML"],
        role="Backend Developer",
        job_description="Python Python Docker",
    )
    priorities = {item["skill"]: item["priority"] for item in result["missing_skill_details"]}
    assert priorities == {"Python": "HIGH", "Docker": "MEDIUM", "HTML": "LOW"}
    assert all(item["job_market"]["status"] == "INSUFFICIENT_DATA" for item in result["missing_skill_details"])


def test_empty_inputs_return_a_zero_match_without_crashing():
    result = SkillGapService().analyze([], [])
    assert result["match_percentage"] == 0
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []


def test_authenticated_active_target_skill_gap_endpoint_returns_integrated_recommendations():
    from datetime import timedelta
    from fastapi.testclient import TestClient
    from sqlalchemy.orm import Session

    from app.core.security import create_token
    from app.db.database import engine
    from app.main import app
    from app.models.resume_history import ResumeHistory
    from app.models.user import Role, User
    from app.models.user_target import TargetSourceType, UserTarget

    with Session(engine) as db:
        user = User(full_name="Skill Gap API User", email="skill-gap-api@example.test", password_hash="unused", role=Role.USER, is_active=True)
        db.add(user); db.flush()
        db.add(UserTarget(user_id=user.id, source_type=TargetSourceType.CUSTOM, company="Example", role_title="Backend Developer", job_description="Python FastAPI Docker", matched_skills=["Python"], missing_skills=["Docker"], is_active=True))
        db.add(ResumeHistory(user_id=user.id, filename="resume.pdf", extracted_skills="Python,FastAPI", recommended_jobs=0))
        db.commit(); user_id = user.id

    token = create_token(user_id, "access", timedelta(minutes=5))
    with TestClient(app) as client:
        response = client.get("/targets/active/skill-gap", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["match_percentage"] == 66.67
    assert response.json()["missing_skills"] == ["Docker"]
    assert "learning_recommendations" in response.json()

    with Session(engine) as db:
        db.delete(db.get(User, user_id)); db.commit()
