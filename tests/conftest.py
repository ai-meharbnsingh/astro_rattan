"""Shared test fixtures — temp DB, TestClient, auth helpers.

Every test module gets a fresh SQLite database to ensure isolation.
Rate limiter is disabled by setting a very high limit.
"""
import os
import sqlite3
import tempfile
import pytest

# Disable rate limiting for tests
os.environ["RATE_LIMIT_PER_MINUTE"] = "9999"
os.environ["TESTING"] = "1"


def _bootstrap_db(db_path: str):
    """Full DB bootstrap: schema + migrations + seed."""
    from app.database import init_db, migrate_users_table
    from app.migrations import run_migrations
    from app.seed_data import seed_all
    init_db(db_path)
    migrate_users_table(db_path)
    run_migrations(db_path)
    seed_all(db_path)


@pytest.fixture(scope="module")
def client():
    """Module-scoped TestClient with fresh DB for each test module."""
    import tempfile
    db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_path = db_file.name
    db_file.close()
    
    os.environ["DB_PATH"] = db_path
    _bootstrap_db(db_path)
    
    # Import app after setting DB_PATH
    from app.main import app
    from fastapi.testclient import TestClient
    
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


@pytest.fixture(scope="module")
def db(client):
    """Module-scoped DB connection."""
    db_path = os.environ["DB_PATH"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    yield conn
    conn.close()


# ------------------------------------------------------------------
# Helper: register a user via the API and return (user_dict, token)
# ------------------------------------------------------------------
def _register_user(client, email, name="Test User", password="password123",
                   date_of_birth=None, gender=None, city=None):
    payload = {"email": email, "password": password, "name": name}
    if date_of_birth:
        payload["date_of_birth"] = date_of_birth
    if gender:
        payload["gender"] = gender
    if city:
        payload["city"] = city
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 201, f"Register failed: {resp.text}"
    data = resp.json()
    return data["user"], data["token"]


def _auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def _make_admin(db, user_id):
    """Promote a user to admin directly in the DB."""
    from app.auth import create_token
    db.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
    db.commit()
    # Return a fresh token with role=admin
    row = db.execute("SELECT id, email, role FROM users WHERE id = ?", (user_id,)).fetchone()
    return create_token({"sub": row["id"], "email": row["email"], "role": "admin"})


def _make_astrologer(db, user_id, display_name="Test Astrologer"):
    """Promote a user to astrologer and create the astrologer profile."""
    from app.auth import create_token
    db.execute("UPDATE users SET role = 'astrologer' WHERE id = ?", (user_id,))
    # Create astrologer record
    db.execute(
        """INSERT INTO astrologers (user_id, display_name, bio, specializations,
           experience_years, per_minute_rate, languages, is_available, is_approved)
           VALUES (?, ?, 'Test bio', 'Vedic,KP', 5, 10.0, '["English","Hindi"]', 1, 1)""",
        (user_id, display_name),
    )
    db.commit()
    # Fetch astrologer id
    row = db.execute("SELECT id FROM astrologers WHERE user_id = ?", (user_id,)).fetchone()
    # Return fresh token with role=astrologer
    user_row = db.execute("SELECT id, email FROM users WHERE id = ?", (user_id,)).fetchone()
    token = create_token({"sub": user_row["id"], "email": user_row["email"], "role": "astrologer"})
    return row["id"], token


def _create_kundli(db, user_id):
    """Insert a minimal kundli record and return its id."""
    import json
    chart = json.dumps({"planets": {"Sun": {"sign": "Aries", "degree": 10, "house": 1}}})
    db.execute(
        """INSERT INTO kundlis (user_id, person_name, birth_date, birth_time,
           birth_place, latitude, longitude, timezone_offset, ayanamsa, chart_data)
           VALUES (?, 'Test Person', '1990-01-15', '10:30:00',
           'Delhi', 28.6139, 77.2090, 5.5, 'lahiri', ?)""",
        (user_id, chart),
    )
    db.commit()
    row = db.execute(
        "SELECT id FROM kundlis WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
        (user_id,),
    ).fetchone()
    return row["id"]
