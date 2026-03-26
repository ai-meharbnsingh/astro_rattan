"""Tests for astrologer dashboard, consultations, profile, and availability."""
import pytest
from tests.conftest import (
    _register_user, _auth_header, _make_astrologer,
)


# ---- Fixtures ---- #

@pytest.fixture(scope="module")
def astro_setup(client, db):
    """Register an astrologer user with full profile."""
    astro_user, _ = _register_user(client, "astro_route@test.com", name="Astro Route")
    astrologer_id, astro_token = _make_astrologer(db, astro_user["id"], "Astro Route")

    # Also register a regular user (for non-astrologer access tests)
    reg_user, reg_token = _register_user(client, "regular_astro_test@test.com", name="Regular For Astro")

    return {
        "astro_user_id": astro_user["id"],
        "astrologer_id": astrologer_id,
        "astro_token": astro_token,
        "reg_token": reg_token,
    }


# ---- Tests ---- #

def test_astrologer_dashboard_200(client, astro_setup):
    """GET /api/astrologer/dashboard as astrologer returns 200."""
    resp = client.get("/api/astrologer/dashboard", headers=_auth_header(astro_setup["astro_token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert "earnings" in data
    assert "consultations" in data
    assert "rating" in data
    assert "upcoming" in data


def test_astrologer_profile_200(client, astro_setup):
    """GET /api/astrologer/profile returns the astrologer record."""
    resp = client.get("/api/astrologer/profile", headers=_auth_header(astro_setup["astro_token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert data["display_name"] == "Astro Route"
    assert data["bio"] == "Test bio"
    assert data["specializations"] == "Vedic,KP"
    assert data["per_minute_rate"] == 10.0
    assert data["languages"] == '["English","Hindi"]'
    assert data["is_available"] == 1


def test_astrologer_consultations_200(client, astro_setup):
    """GET /api/astrologer/consultations returns 200."""
    resp = client.get("/api/astrologer/consultations", headers=_auth_header(astro_setup["astro_token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_astrologer_update_profile_200(client, astro_setup):
    """PATCH /api/astrologer/profile updates bio — 200."""
    resp = client.patch(
        "/api/astrologer/profile",
        json={"bio": "Updated bio for testing", "specializations": "Vedic,KP,Numerology"},
        headers=_auth_header(astro_setup["astro_token"]),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["bio"] == "Updated bio for testing"
    assert data["specializations"] == "Vedic,KP,Numerology"


def test_astrologer_update_availability_200(client, astro_setup):
    """PATCH /api/astrologer/availability toggles availability — 200."""
    # Set to unavailable
    resp = client.patch(
        "/api/astrologer/availability",
        json={"is_available": False},
        headers=_auth_header(astro_setup["astro_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["is_available"] == 0

    # Toggle back to available
    resp = client.patch(
        "/api/astrologer/availability",
        json={"is_available": True},
        headers=_auth_header(astro_setup["astro_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["is_available"] == 1


def test_negative_per_minute_rate_422(client, astro_setup):
    """Negative per-minute rate returns 422 — CHAOS #12."""
    resp = client.patch(
        "/api/astrologer/profile",
        json={"per_minute_rate": -5.0},
        headers=_auth_header(astro_setup["astro_token"]),
    )
    assert resp.status_code == 422


def test_non_astrologer_dashboard_403(client, astro_setup):
    """Non-astrologer accessing astrologer endpoints returns 403."""
    resp = client.get("/api/astrologer/dashboard", headers=_auth_header(astro_setup["reg_token"]))
    assert resp.status_code == 403


def test_toggle_availability_on_off(client, astro_setup):
    """Toggle availability off then on verifies state changes."""
    # Off
    resp = client.patch(
        "/api/astrologer/availability",
        json={"is_available": False},
        headers=_auth_header(astro_setup["astro_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["is_available"] == 0

    # On
    resp = client.patch(
        "/api/astrologer/availability",
        json={"is_available": True},
        headers=_auth_header(astro_setup["astro_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["is_available"] == 1


def test_update_specializations(client, astro_setup):
    """Update specializations field is persisted."""
    resp = client.patch(
        "/api/astrologer/profile",
        json={"specializations": "Vedic,Tarot,Palmistry"},
        headers=_auth_header(astro_setup["astro_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["specializations"] == "Vedic,Tarot,Palmistry"
