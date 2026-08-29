from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from collections import Counter

from fastapi.testclient import TestClient
from app.core.security import create_token
from app.db.database import SessionLocal
from app.main import app
from app.models.company import Company
from app.models.user import User
from app.services.company_intelligence_service import CompanyIntelligenceService


def _user_headers() -> dict[str, str]:
    with SessionLocal() as db:
        user_id = db.query(User.id).filter(User.role == "USER").order_by(User.id).first()[0]
    return {"Authorization": f"Bearer {create_token(user_id, 'access', timedelta(minutes=5))}"}


def test_company_list_detail_search_and_invalid_id():
    headers = _user_headers()
    with TestClient(app) as client:
        rows = client.get("/company-intelligence/companies", headers=headers)
        assert rows.status_code == 200
        assert rows.json()
        verified = client.get("/company-intelligence/companies", params={"verified": "true"}, headers=headers)
        unverified = client.get("/company-intelligence/companies", params={"verified": "false"}, headers=headers)
        assert verified.status_code == unverified.status_code == 200
        assert all(item["verified"] for item in verified.json())
        assert all(not item["verified"] for item in unverified.json())
        company_id = rows.json()[0]["id"]
        assert client.get(f"/company-intelligence/companies/{company_id}", headers=headers).status_code == 200
        assert client.get("/company-intelligence/companies/999999999", headers=headers).status_code == 404
        search = client.get("/company-intelligence/companies", params={"search": "  cAnOnIcAl  "}, headers=headers)
        assert search.status_code == 200
        assert any(item["name"] == "Canonical" for item in search.json())


def test_company_verification_and_open_roles_are_explicit():
    headers = _user_headers()
    with TestClient(app) as client:
        rows = client.get("/company-intelligence/companies", headers=headers).json()
    assert rows
    assert any(item["verified"] for item in rows)
    assert any(not item["verified"] for item in rows)
    assert all(item["open_roles"] is None or item["open_roles"] >= 0 for item in rows)


def test_company_payload_distinguishes_active_zero_and_unknown_jobs():
    company = SimpleNamespace(
        id=1, name="Example", logo_url=None, industry="Technology", headquarters="Chennai", country="India",
        career_url="https://example.com/careers", website_url="https://example.com", description=None,
        tech_stack=None, products=None, hiring_status=None, internship_available=False, freshers_hiring=False,
        data_source_url="https://example.com/about", last_verified_at=datetime.now(UTC), verification_status="Verified",
    )
    service = CompanyIntelligenceService()
    assert service._company_payload(company, (4, 2))["open_roles"] == 2
    assert service._company_payload(company, (4, 0))["open_roles"] == 0
    assert service._company_payload(company, None)["open_roles"] is None


def test_company_diagnostics_and_verification_mutations_are_admin_only():
    headers = _user_headers()
    with TestClient(app) as client:
        assert client.get("/admin/company-diagnostics").status_code == 401
        assert client.get("/admin/company-diagnostics", headers=headers).status_code == 403
        assert client.patch("/admin/companies/1/verification", headers=headers, json={"verified": False}).status_code == 403
        assert client.patch("/admin/startups/1/verification", headers=headers, json={"verified": False}).status_code == 403


def test_company_names_have_no_normalized_duplicates():
    with SessionLocal() as db:
        names = [" ".join(row.name.casefold().split()) for row in db.query(Company).all()]
    assert not [name for name, count in Counter(names).items() if count > 1]
