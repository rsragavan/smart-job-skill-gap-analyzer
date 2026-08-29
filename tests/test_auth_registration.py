from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import verify_password
from app.db.database import SessionLocal
from app.main import app
from app.models.user import User


def _payload(email: str | None = None) -> dict[str, str]:
    return {
        "full_name": "Registration Test User",
        "email": email or f"auth-test-{uuid4().hex}@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!",
    }


def test_registration_login_and_password_storage():
    payload = _payload()
    with TestClient(app) as client:
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 201
        body = response.json()
        assert {"access_token", "refresh_token", "user"} <= body.keys()
        assert "password" not in body and "password_hash" not in body
        assert "password" not in body["user"] and "confirm_password" not in body["user"]

        login = client.post("/auth/login", json={"email": payload["email"], "password": payload["password"]})
        assert login.status_code == 200
        me = client.get("/auth/me", headers={"Authorization": f"Bearer {login.json()['access_token']}"})
        assert me.status_code == 200
        assert me.json()["email"] == payload["email"]

    with SessionLocal() as db:
        user = db.query(User).filter(User.email == payload["email"]).one()
        assert user.password_hash != payload["password"]
        assert user.password_hash.startswith("$2")
        assert verify_password(payload["password"], user.password_hash)
        db.delete(user)
        db.commit()


def test_registration_required_fields_and_invalid_email_return_422():
    with TestClient(app) as client:
        payload = _payload()
        for field in ("full_name", "email", "password", "confirm_password"):
            response = client.post("/auth/register", json={key: value for key, value in payload.items() if key != field})
            assert response.status_code == 422
            assert response.json()["detail"]

        invalid = client.post("/auth/register", json={**payload, "email": "invalid-email"})
        assert invalid.status_code == 422


def test_registration_rejects_mismatch_and_weak_password():
    with TestClient(app) as client:
        mismatch = client.post("/auth/register", json={**_payload(), "confirm_password": "Password456!"})
        assert mismatch.status_code == 422
        assert mismatch.json()["detail"] == "Passwords do not match"

        weak = client.post("/auth/register", json={**_payload(), "password": "password", "confirm_password": "password"})
        assert weak.status_code == 422


def test_registration_rejects_duplicate_email():
    payload = _payload()
    with TestClient(app) as client:
        assert client.post("/auth/register", json=payload).status_code == 201
        duplicate = client.post("/auth/register", json=payload)
        assert duplicate.status_code == 409
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == payload["email"]).one()
        db.delete(user)
        db.commit()

