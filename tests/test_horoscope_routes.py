"""Tests for Horoscope routes — daily/weekly/monthly/yearly by zodiac sign.

Covers: GET /api/horoscope/{sign}?period= with all 12 signs, periods,
        invalid sign, missing period default, response structure.
"""
import os
import importlib
import pytest
from fastapi.testclient import TestClient


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def test_db(tmp_path):
    """Create a fresh seeded test database with horoscopes."""
    db_path = str(tmp_path / "test_horoscope.db")
    os.environ["DB_PATH"] = db_path

    import app.config
    importlib.reload(app.config)
    import app.database
    importlib.reload(app.database)

    from app.database import init_db, migrate_users_table
    from app.seed_data import seed_all
    from app.horoscope_generator import generate_daily_horoscopes, seed_weekly_horoscopes

    init_db(db_path)
    migrate_users_table(db_path)
    seed_all(db_path)
    generate_daily_horoscopes(db_path)
    seed_weekly_horoscopes(db_path)
    return db_path


@pytest.fixture
def client(test_db):
    """TestClient with fresh seeded DB."""
    os.environ["DB_PATH"] = test_db
    import app.config
    importlib.reload(app.config)
    import app.database
    importlib.reload(app.database)

    from app.main import app
    return TestClient(app, raise_server_exceptions=False)


# ============================================================
# Tests
# ============================================================

def test_horoscope_aries_daily(client):
    """GET /api/horoscope/aries?period=daily -> 200."""
    resp = client.get("/api/horoscope/aries?period=daily")
    assert resp.status_code == 200
    data = resp.json()
    assert data["sign"] == "aries"
    assert data["period"] == "daily"
    assert "content" in data
    assert len(data["content"]) > 0
    assert "date" in data


def test_horoscope_leo_weekly(client):
    """GET /api/horoscope/leo?period=weekly -> 200."""
    resp = client.get("/api/horoscope/leo?period=weekly")
    assert resp.status_code == 200
    data = resp.json()
    assert data["sign"] == "leo"
    assert data["period"] == "weekly"
    assert "content" in data
    assert len(data["content"]) > 0


def test_horoscope_invalid_sign(client):
    """GET /api/horoscope/invalid_sign -> 422 (enum validation)."""
    resp = client.get("/api/horoscope/invalid_sign")
    assert resp.status_code == 422


def test_horoscope_default_period(client):
    """GET /api/horoscope/aries (no period) -> 200 with default=daily."""
    resp = client.get("/api/horoscope/aries")
    assert resp.status_code == 200
    data = resp.json()
    assert data["sign"] == "aries"
    assert data["period"] == "daily"


def test_horoscope_response_structure(client):
    """Response has: sign, period, content, date."""
    resp = client.get("/api/horoscope/taurus?period=daily")
    assert resp.status_code == 200
    data = resp.json()
    required_keys = {"sign", "period", "content", "date"}
    assert required_keys.issubset(set(data.keys())), f"Missing keys: {required_keys - set(data.keys())}"


ALL_SIGNS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]


@pytest.mark.parametrize("sign", ALL_SIGNS)
def test_all_12_signs_valid(client, sign):
    """All 12 zodiac signs return valid 200 response."""
    resp = client.get(f"/api/horoscope/{sign}?period=daily")
    assert resp.status_code == 200
    data = resp.json()
    assert data["sign"] == sign
    assert data["period"] == "daily"
    assert "content" in data
    assert len(data["content"]) > 10  # Non-trivial content


def test_horoscope_monthly(client):
    """GET /api/horoscope/scorpio?period=monthly -> 200 (uses default content)."""
    resp = client.get("/api/horoscope/scorpio?period=monthly")
    assert resp.status_code == 200
    data = resp.json()
    assert data["sign"] == "scorpio"
    assert data["period"] == "monthly"
    assert len(data["content"]) > 0


def test_horoscope_yearly(client):
    """GET /api/horoscope/pisces?period=yearly -> 200 (uses default content)."""
    resp = client.get("/api/horoscope/pisces?period=yearly")
    assert resp.status_code == 200
    data = resp.json()
    assert data["sign"] == "pisces"
    assert data["period"] == "yearly"
    assert len(data["content"]) > 0


def test_horoscope_invalid_period(client):
    """GET /api/horoscope/aries?period=biweekly -> 422 (enum validation)."""
    resp = client.get("/api/horoscope/aries?period=biweekly")
    assert resp.status_code == 422
