from datetime import timedelta

import pytest

from app.core.security import create_token, decode_token
from app.main import app
from app.models.user import Role


def test_access_token_round_trip_and_tamper_detection():
    token = create_token(42, "access", timedelta(minutes=5))
    assert decode_token(token, "access")["sub"] == "42"
    with pytest.raises(Exception):
        decode_token(f"{token}x", "access")


def test_admin_and_system_routes_are_registered():
    paths = set(app.openapi()["paths"])
    assert "/admin/stats" in paths
    assert "/admin/audit" in paths
    assert "/health" in paths


def test_admin_role_is_explicitly_available():
    assert Role.ADMIN.value == "admin"
