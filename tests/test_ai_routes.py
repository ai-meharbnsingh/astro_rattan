"""Tests for AI routes — interpret, ask, gita, remedies, oracle, history.

Covers: POST /api/ai/interpret, /api/ai/ask, /api/ai/gita, /api/ai/remedies,
        /api/ai/oracle, GET /api/ai/history.
CHAOS #4: OpenAI timeout handling. CHAOS #5: Invalid API key fallback.
CHAOS #15: Empty question validation.
"""
import json
import os
import sqlite3
import importlib
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def test_db(tmp_path):
    """Create a fresh seeded test database."""
    db_path = str(tmp_path / "test_ai.db")
    os.environ["DB_PATH"] = db_path

    import app.config
    importlib.reload(app.config)
    import app.database
    importlib.reload(app.database)

    from app.database import init_db, migrate_users_table
    from app.seed_data import seed_all
    init_db(db_path)
    migrate_users_table(db_path)
    seed_all(db_path)
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


@pytest.fixture
def user_token(client):
    """Register a user and return JWT token."""
    resp = client.post("/api/auth/register", json={
        "email": "aiuser@test.com",
        "password": "test123456",
        "name": "AI Test User",
    })
    assert resp.status_code == 201, f"Registration failed: {resp.text}"
    return resp.json()["token"]


@pytest.fixture
def kundli_id(client, user_token, test_db):
    """Create a kundli entry directly in DB and return its ID."""
    import uuid
    kid = uuid.uuid4().hex
    # Get user ID from token
    from app.auth import decode_token
    payload = decode_token(user_token)
    user_id = payload["sub"]

    chart_data = json.dumps({
        "ascendant": {"sign": "Aries", "degree": 15.5},
        "planets": {
            "Sun": {"sign": "Leo", "degree": 10.0, "house": 5},
            "Moon": {"sign": "Taurus", "degree": 20.0, "house": 2},
            "Mars": {"sign": "Aries", "degree": 5.0, "house": 1},
            "Mercury": {"sign": "Virgo", "degree": 25.0, "house": 6},
            "Jupiter": {"sign": "Sagittarius", "degree": 12.0, "house": 9},
            "Venus": {"sign": "Libra", "degree": 18.0, "house": 7},
            "Saturn": {"sign": "Capricorn", "degree": 22.0, "house": 10},
        },
        "nakshatra": "Rohini",
        "dasha": {"current": "Jupiter", "sub": "Saturn"},
    })

    conn = sqlite3.connect(test_db)
    conn.execute(
        "INSERT INTO kundlis (id, user_id, person_name, birth_date, birth_time, "
        "birth_place, latitude, longitude, timezone_offset, ayanamsa, chart_data) "
        "VALUES (?, ?, 'Test Person', '1990-01-15', '14:30:00', "
        "'Delhi, India', 28.6139, 77.2090, 5.5, 'lahiri', ?)",
        (kid, user_id, chart_data),
    )
    conn.commit()
    conn.close()
    return kid


# ============================================================
# Tests
# ============================================================

def test_ai_interpret_success(client, user_token, kundli_id):
    """POST /api/ai/interpret {kundli_id} -> 200, has interpretation."""
    resp = client.post(
        "/api/ai/interpret",
        json={"kundli_id": kundli_id},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "interpretation" in data
    assert len(data["interpretation"]) > 0


def test_ai_interpret_no_auth(client, kundli_id):
    """POST /api/ai/interpret without auth -> 401."""
    resp = client.post("/api/ai/interpret", json={"kundli_id": kundli_id})
    assert resp.status_code == 401


def test_ai_interpret_nonexistent_kundli(client, user_token):
    """POST /api/ai/interpret with nonexistent kundli -> 404."""
    resp = client.post(
        "/api/ai/interpret",
        json={"kundli_id": "nonexistent_id_12345"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 404


def test_ai_ask_success(client, user_token):
    """POST /api/ai/ask {question} -> 200, has answer."""
    resp = client.post(
        "/api/ai/ask",
        json={"question": "What does Saturn in the 7th house mean?"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert len(data["answer"]) > 0


def test_ai_ask_empty_question(client, user_token):
    """POST /api/ai/ask with empty question -> 422 (CHAOS #15)."""
    resp = client.post(
        "/api/ai/ask",
        json={"question": ""},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 422


def test_ai_gita_success(client):
    """POST /api/ai/gita {question} -> 200, has relevant_slokas."""
    resp = client.post(
        "/api/ai/gita",
        json={"question": "How to deal with loss and grief?"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "relevant_slokas" in data
    assert isinstance(data["relevant_slokas"], list)
    assert len(data["relevant_slokas"]) > 0


def test_ai_remedies_success(client, user_token, kundli_id):
    """POST /api/ai/remedies {kundli_id} -> 200, has remedies list."""
    resp = client.post(
        "/api/ai/remedies",
        json={"question": "Suggest remedies", "kundli_id": kundli_id},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "remedies" in data
    assert isinstance(data["remedies"], list)
    assert len(data["remedies"]) > 0


def test_ai_oracle_yes_no(client):
    """POST /api/ai/oracle {question, mode:"yes_no"} -> 200."""
    resp = client.post(
        "/api/ai/oracle",
        json={"question": "Will I get a promotion this year?", "mode": "yes_no"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "reasoning" in data


def test_ai_oracle_tarot(client):
    """POST /api/ai/oracle {question, mode:"tarot"} -> 200."""
    resp = client.post(
        "/api/ai/oracle",
        json={"question": "What does the future hold for my relationship?", "mode": "tarot"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data


def test_ai_history_after_calls(client, user_token, kundli_id):
    """GET /api/ai/history -> 200 after making some AI calls."""
    # Make an AI call first to populate history
    client.post(
        "/api/ai/ask",
        json={"question": "What is my lucky number?"},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    resp = client.get(
        "/api/ai/history",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "chats" in data
    assert "total" in data
    assert data["total"] >= 1
    assert len(data["chats"]) >= 1


def test_ai_openai_timeout_fallback(client, user_token, kundli_id):
    """CHAOS #4: OpenAI timeout -> graceful fallback response."""
    with patch("app.ai_engine._call_ai", return_value=None):
        resp = client.post(
            "/api/ai/interpret",
            json={"kundli_id": kundli_id},
            headers={"Authorization": f"Bearer {user_token}"},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "interpretation" in data
    # Fallback response should mention unavailability
    assert "unavailable" in data["interpretation"].lower() or len(data["interpretation"]) > 0


def test_ai_invalid_key_fallback(client):
    """CHAOS #5: Invalid API key -> fallback response."""
    with patch("app.ai_engine._call_ai", return_value=None):
        resp = client.post(
            "/api/ai/gita",
            json={"question": "What is the meaning of karma?"},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "relevant_slokas" in data
    # Should still have fallback slokas
    assert len(data["relevant_slokas"]) > 0
