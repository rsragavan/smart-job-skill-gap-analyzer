from datetime import timedelta
from datetime import UTC, datetime
from types import SimpleNamespace
from collections import Counter

from fastapi.testclient import TestClient
from sqlalchemy import func

from app.core.security import create_token
from app.db.database import SessionLocal
from app.main import app
from app.models.company_intelligence import StartupInformation
from app.models.user import User
from app.services.company_intelligence_service import CompanyIntelligenceService


def _user_headers() -> dict[str, str]:
    with SessionLocal() as db:
        user_id = db.query(User.id).filter(User.role == "USER").order_by(User.id).first()[0]
    return {"Authorization": f"Bearer {create_token(user_id, 'access', timedelta(minutes=5))}"}


def test_startup_list_and_search_are_database_backed():
    headers = _user_headers()
    with TestClient(app) as client:
        response = client.get("/startups", headers=headers)
        assert response.status_code == 200
        assert response.json()
        chennai = client.get("/startups/search", params={"search": "  chEnNaI  "}, headers=headers)
        assert chennai.status_code == 200
        assert all("chennai" in item["location"].casefold() for item in chennai.json())


def test_startup_detail_and_invalid_id():
    headers = _user_headers()
    with SessionLocal() as db:
        startup_id = db.query(StartupInformation.id).order_by(StartupInformation.id).first()[0]
    with TestClient(app) as client:
        detail = client.get(f"/startups/{startup_id}", headers=headers)
        assert detail.status_code == 200
        assert "verification_status" in detail.json()
        assert client.get("/startups/999999999", headers=headers).status_code == 404
        assert client.get("/startups/999999999/roles", headers=headers).status_code == 404


def test_unavailable_job_relationship_is_not_reported_as_zero_roles():
    headers = _user_headers()
    with TestClient(app) as client:
        rows = client.get("/startups", headers=headers).json()
    assert rows
    # Current startup records have no matching rows in jobs; zero is therefore
    # unknown rather than a verified zero.
    assert all(row["open_roles"] is None for row in rows)
    assert all(row["hiring_status"] == "Check careers page" for row in rows)


def test_startup_diagnostics_requires_admin_authorization():
    headers = _user_headers()
    with TestClient(app) as client:
        assert client.get("/admin/startup-diagnostics").status_code == 401
        assert client.get("/admin/startup-diagnostics", headers=headers).status_code == 403


def test_startup_open_role_count_and_hiring_status_use_actual_job_evidence():
    startup = SimpleNamespace(
        id=1, name="Verified Startup", industry="Technology", location="Chennai", state=None, country="India",
        funding_stage="Seed", latest_funding_amount="$1M", founded_year=2020, employees=None,
        website_url="https://example.com", careers_url="https://example.com/careers", public_email=None,
        open_positions=0, tech_stack="Python", description="Description", hiring_status=None, source_url="https://example.com/about",
        founders="Founder", investors="Investor", products="Product", culture_summary="Culture",
        last_verified_at=datetime.now(UTC), last_updated=datetime.now(UTC), preparation_tips=None,
        verification_status="verified", source_name="test_source",
    )
    service = CompanyIntelligenceService()
    hiring = service._startup_payload(startup, (3, 2))
    not_hiring = service._startup_payload(startup, (3, 0))
    assert hiring["open_roles"] == 2
    assert hiring["hiring_status"] == "Hiring"
    assert not_hiring["open_roles"] == 0
    assert not_hiring["hiring_status"] == "Not currently hiring"
    assert hiring["verified"] is True


def test_startup_names_have_no_normalized_duplicates():
    with SessionLocal() as db:
        names = [" ".join(row.name.casefold().split()) for row in db.query(StartupInformation).all()]
    assert not [name for name, count in Counter(names).items() if count > 1]
