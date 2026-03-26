"""Tests for user profile, password change, and history endpoints."""
import pytest
from tests.conftest import _register_user, _auth_header


# ---- Fixtures ---- #

@pytest.fixture(scope="module")
def profile_setup(client, db):
    """Register a user with DOB, gender, city for profile tests."""
    user, token = _register_user(
        client,
        "profile_user@test.com",
        name="Profile User",
        password="password123",
        date_of_birth="1990-05-20",
        gender="male",
        city="Mumbai",
    )
    return {"user_id": user["id"], "token": token}


# ---- Tests ---- #

def test_get_me_200(client, profile_setup):
    """GET /api/auth/me returns 200 with name, email, role."""
    resp = client.get("/api/auth/me", headers=_auth_header(profile_setup["token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Profile User"
    assert data["email"] == "profile_user@test.com"
    assert data["role"] == "user"
    assert data["date_of_birth"] == "1990-05-20"
    assert data["gender"] == "male"
    assert data["city"] == "Mumbai"
    assert "avatar_url" in data


def test_update_profile_200(client, profile_setup):
    """PATCH /api/auth/profile updates name and city — 200."""
    resp = client.patch(
        "/api/auth/profile",
        json={"name": "Updated Profile User", "city": "Delhi"},
        headers=_auth_header(profile_setup["token"]),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Updated Profile User"
    assert data["city"] == "Delhi"


def test_change_password_200(client, profile_setup):
    """POST /api/auth/change-password with correct current password — 200."""
    resp = client.post(
        "/api/auth/change-password",
        json={"current_password": "password123", "new_password": "newpass456"},
        headers=_auth_header(profile_setup["token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["message"] == "Password changed successfully"

    # Change it back so other tests still work
    client.post(
        "/api/auth/change-password",
        json={"current_password": "newpass456", "new_password": "password123"},
        headers=_auth_header(profile_setup["token"]),
    )


def test_change_password_wrong_current_400(client, profile_setup):
    """POST /api/auth/change-password with wrong current password — 400."""
    resp = client.post(
        "/api/auth/change-password",
        json={"current_password": "totally_wrong", "new_password": "newpass456"},
        headers=_auth_header(profile_setup["token"]),
    )
    assert resp.status_code == 400


def test_user_history_200(client, profile_setup):
    """GET /api/auth/history returns 200 with kundlis, orders, consultations."""
    resp = client.get("/api/auth/history", headers=_auth_header(profile_setup["token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert "kundlis" in data
    assert "orders" in data
    assert "consultations" in data


def test_profile_without_auth_401(client):
    """GET /api/auth/me without auth returns 401."""
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_update_profile_empty_name_422(client, profile_setup):
    """PATCH /api/auth/profile with empty name returns 422."""
    resp = client.patch(
        "/api/auth/profile",
        json={"name": ""},
        headers=_auth_header(profile_setup["token"]),
    )
    assert resp.status_code == 422


def test_register_with_dob_gender_city(client, db):
    """Register with DOB, gender, city — stored correctly."""
    user, token = _register_user(
        client,
        "dob_test@test.com",
        name="DOB Test",
        date_of_birth="1985-12-25",
        gender="female",
        city="Kolkata",
    )
    # Verify stored in DB
    row = db.execute(
        "SELECT date_of_birth, gender, city FROM users WHERE id = ?", (user["id"],)
    ).fetchone()
    assert row["date_of_birth"] == "1985-12-25"
    assert row["gender"] == "female"
    assert row["city"] == "Kolkata"
