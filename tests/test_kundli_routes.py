"""Route-level tests for /api/kundli/* endpoints.

Uses FastAPI TestClient with a fresh temp DB per test session.
Covers happy path, error path, and chaos scenarios.

NOTE: These tests were written for SQLite and need rewriting for PostgreSQL.
They are skipped when DATABASE_URL points to PostgreSQL (production DB).
"""
import os
import json
import sqlite3
import importlib
import concurrent.futures

import pytest
from fastapi.testclient import TestClient

# Skip entire module if using PostgreSQL (tests use SQLite fixtures)
_db_url = os.getenv("DATABASE_URL", "")
if "postgresql" in _db_url or "neon.tech" in _db_url:
    pytest.skip("Kundli route tests require SQLite — PostgreSQL rewrite pending", allow_module_level=True)


# ── Fixtures ────────────────────────────────────────────────

@pytest.fixture(scope="module")
def test_db(tmp_path_factory):
    """Create a fresh test database with schema + seed data."""
    db_path = str(tmp_path_factory.mktemp("kundli_db") / "test_kundli.db")
    os.environ["DB_PATH"] = db_path
    # Reload config so DB_PATH is picked up
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


@pytest.fixture(scope="module")
def client(test_db):
    """TestClient with rate limiter disabled for tests."""
    os.environ["DB_PATH"] = test_db
    import app.config
    importlib.reload(app.config)
    import app.database
    importlib.reload(app.database)

    from app.main import app, limiter
    # Disable rate limiter in tests
    limiter.enabled = False
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture(scope="module")
def auth_token(client):
    """Register a test user and return JWT token."""
    resp = client.post("/api/auth/register", json={
        "email": "kundli_test@example.com",
        "password": "testpass123",
        "name": "Kundli Tester",
    })
    assert resp.status_code == 201, f"Register failed: {resp.text}"
    return resp.json()["token"]


@pytest.fixture(scope="module")
def auth_headers(auth_token):
    """Authorization headers with Bearer token."""
    return {"Authorization": f"Bearer {auth_token}"}


VALID_KUNDLI_PAYLOAD = {
    "person_name": "Test Person",
    "birth_date": "1990-05-15",
    "birth_time": "14:30:00",
    "birth_place": "Mumbai, India",
    "latitude": 19.076,
    "longitude": 72.8777,
    "timezone_offset": 5.5,
    "ayanamsa": "lahiri",
}


# ── 1. POST /api/kundli/generate ─────────────────────────

class TestGenerateKundli:
    """Tests for kundli generation endpoint."""

    def test_generate_kundli_success(self, client, auth_headers):
        """POST /api/kundli/generate → 201, returns chart_data with 9 planets."""
        resp = client.post("/api/kundli/generate", json=VALID_KUNDLI_PAYLOAD, headers=auth_headers)
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}: {resp.text}"
        data = resp.json()
        assert "id" in data
        assert data["person_name"] == "Test Person"
        assert "chart_data" in data
        chart = data["chart_data"]
        # Must contain planets section with 9 Vedic planets
        assert "planets" in chart
        planets = chart["planets"]
        expected_planets = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
        assert expected_planets.issubset(set(planets.keys())), f"Missing planets: {expected_planets - set(planets.keys())}"

    def test_generate_kundli_invalid_date(self, client, auth_headers):
        """POST /api/kundli/generate with invalid date → 422 or 500."""
        payload = {**VALID_KUNDLI_PAYLOAD, "birth_date": "not-a-date"}
        resp = client.post("/api/kundli/generate", json=payload, headers=auth_headers)
        # Either validation or server error — not 200/201
        assert resp.status_code in (422, 500), f"Expected 422 or 500, got {resp.status_code}"

    def test_generate_kundli_no_auth(self, client):
        """POST /api/kundli/generate without auth → 401."""
        resp = client.post("/api/kundli/generate", json=VALID_KUNDLI_PAYLOAD)
        assert resp.status_code == 401

    def test_generate_kundli_missing_fields(self, client, auth_headers):
        """POST /api/kundli/generate with missing required fields → 422."""
        resp = client.post("/api/kundli/generate", json={"person_name": "Incomplete"}, headers=auth_headers)
        assert resp.status_code == 422


# ── 2. GET /api/kundli/list ──────────────────────────────

class TestListKundlis:

    def test_list_kundlis_success(self, client, auth_headers):
        """GET /api/kundli/list → 200, returns array."""
        resp = client.get("/api/kundli/list", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # At least one from previous test
        assert "id" in data[0]
        assert "person_name" in data[0]

    def test_list_kundlis_no_auth(self, client):
        """GET /api/kundli/list without auth → 401."""
        resp = client.get("/api/kundli/list")
        assert resp.status_code == 401


# ── 3. GET /api/kundli/{id} ─────────────────────────────

class TestGetKundli:

    def test_get_kundli_success(self, client, auth_headers):
        """GET /api/kundli/{id} → 200 with full chart data."""
        # First, get the list to find the ID
        list_resp = client.get("/api/kundli/list", headers=auth_headers)
        kundli_id = list_resp.json()[0]["id"]

        resp = client.get(f"/api/kundli/{kundli_id}", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == kundli_id
        assert "chart_data" in data
        assert "latitude" in data
        assert "longitude" in data

    def test_get_kundli_nonexistent(self, client, auth_headers):
        """GET /api/kundli/{nonexistent} → 404."""
        resp = client.get("/api/kundli/does_not_exist_12345", headers=auth_headers)
        assert resp.status_code == 404


# ── 4. POST /api/kundli/{id}/iogita ─────────────────────

class TestIogitaAnalysis:

    def test_iogita_analysis_success(self, client, auth_headers):
        """POST /api/kundli/{id}/iogita → 200, has basin and atom_activations."""
        list_resp = client.get("/api/kundli/list", headers=auth_headers)
        kundli_id = list_resp.json()[0]["id"]

        resp = client.post(f"/api/kundli/{kundli_id}/iogita", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "basin" in data
        assert "atom_activations" in data

    def test_iogita_nonexistent_kundli(self, client, auth_headers):
        """POST /api/kundli/{nonexistent}/iogita → 404."""
        resp = client.post("/api/kundli/nonexistent_xyz/iogita", headers=auth_headers)
        assert resp.status_code == 404


# ── 5. POST /api/kundli/match ────────────────────────────

class TestKundliMatch:

    def test_match_kundlis_success(self, client, auth_headers):
        """POST /api/kundli/match (create 2 kundlis) → 200, has total_score."""
        # Create second kundli
        payload2 = {**VALID_KUNDLI_PAYLOAD, "person_name": "Second Person", "birth_date": "1992-08-20"}
        resp2 = client.post("/api/kundli/generate", json=payload2, headers=auth_headers)
        assert resp2.status_code == 201
        id2 = resp2.json()["id"]

        list_resp = client.get("/api/kundli/list", headers=auth_headers)
        kundlis = list_resp.json()
        # Get any two different kundlis
        id1 = None
        for k in kundlis:
            if k["id"] != id2:
                id1 = k["id"]
                break
        assert id1 is not None, "Need at least 2 kundlis for match test"

        resp = client.post("/api/kundli/match", json={
            "kundli_id_1": id1,
            "kundli_id_2": id2,
        }, headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "total_score" in data
        assert isinstance(data["total_score"], (int, float))
        assert "person1" in data
        assert "person2" in data

    def test_match_same_kundli(self, client, auth_headers):
        """POST /api/kundli/match with same kundli → still succeeds (engine allows self-match)."""
        list_resp = client.get("/api/kundli/list", headers=auth_headers)
        kundli_id = list_resp.json()[0]["id"]
        resp = client.post("/api/kundli/match", json={
            "kundli_id_1": kundli_id,
            "kundli_id_2": kundli_id,
        }, headers=auth_headers)
        # The matching engine has no self-match guard, so it returns 200 with a score
        assert resp.status_code == 200
        data = resp.json()
        assert "total_score" in data

    def test_match_nonexistent_kundli(self, client, auth_headers):
        """POST /api/kundli/match with nonexistent kundli → 404."""
        list_resp = client.get("/api/kundli/list", headers=auth_headers)
        kundli_id = list_resp.json()[0]["id"]
        resp = client.post("/api/kundli/match", json={
            "kundli_id_1": kundli_id,
            "kundli_id_2": "nonexistent_xyz",
        }, headers=auth_headers)
        assert resp.status_code == 404


# ── 6. POST /api/kundli/{id}/dosha ──────────────────────

class TestDoshaCheck:

    def test_dosha_success(self, client, auth_headers):
        """POST /api/kundli/{id}/dosha → 200, has mangal_dosha."""
        list_resp = client.get("/api/kundli/list", headers=auth_headers)
        kundli_id = list_resp.json()[0]["id"]

        resp = client.post(f"/api/kundli/{kundli_id}/dosha", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "mangal_dosha" in data
        assert "kaal_sarp_dosha" in data
        assert "sade_sati" in data
        assert data["kundli_id"] == kundli_id

    def test_dosha_nonexistent(self, client, auth_headers):
        """POST /api/kundli/{nonexistent}/dosha → 404."""
        resp = client.post("/api/kundli/nonexistent_xyz/dosha", headers=auth_headers)
        assert resp.status_code == 404


# ── 7. POST /api/kundli/{id}/dasha ──────────────────────

class TestDashaCalculation:

    def test_dasha_success(self, client, auth_headers):
        """POST /api/kundli/{id}/dasha → 200, has mahadasha_periods."""
        list_resp = client.get("/api/kundli/list", headers=auth_headers)
        kundli_id = list_resp.json()[0]["id"]

        resp = client.post(f"/api/kundli/{kundli_id}/dasha", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "mahadasha_periods" in data
        assert isinstance(data["mahadasha_periods"], list)
        assert len(data["mahadasha_periods"]) > 0
        assert data["kundli_id"] == kundli_id

    def test_dasha_nonexistent(self, client, auth_headers):
        """POST /api/kundli/{nonexistent}/dasha → 404."""
        resp = client.post("/api/kundli/nonexistent_xyz/dasha", headers=auth_headers)
        assert resp.status_code == 404


# ── 8. POST /api/kundli/{id}/divisional ──────────────────

class TestDivisionalChart:

    def test_divisional_success(self, client, auth_headers):
        """POST /api/kundli/{id}/divisional → 200 with D9 chart."""
        list_resp = client.get("/api/kundli/list", headers=auth_headers)
        kundli_id = list_resp.json()[0]["id"]

        resp = client.post(
            f"/api/kundli/{kundli_id}/divisional",
            json={"chart_type": "D9"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["chart_type"] == "D9"
        assert "planet_signs" in data

    def test_divisional_nonexistent(self, client, auth_headers):
        """POST /api/kundli/{nonexistent}/divisional → 404."""
        resp = client.post(
            "/api/kundli/nonexistent_xyz/divisional",
            json={"chart_type": "D9"},
            headers=auth_headers,
        )
        assert resp.status_code == 404


# ── 9. POST /api/kundli/{id}/ashtakvarga ────────────────

class TestAshtakvarga:

    def test_ashtakvarga_success(self, client, auth_headers):
        """POST /api/kundli/{id}/ashtakvarga → 200, has planet_bindus."""
        list_resp = client.get("/api/kundli/list", headers=auth_headers)
        kundli_id = list_resp.json()[0]["id"]

        resp = client.post(f"/api/kundli/{kundli_id}/ashtakvarga", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "planet_bindus" in data
        assert "sarvashtakvarga" in data
        assert data["kundli_id"] == kundli_id

    def test_ashtakvarga_nonexistent(self, client, auth_headers):
        """POST /api/kundli/{nonexistent}/ashtakvarga → 404."""
        resp = client.post("/api/kundli/nonexistent_xyz/ashtakvarga", headers=auth_headers)
        assert resp.status_code == 404


# ── 10. Chaos & Edge Cases ───────────────────────────────

class TestKundliChaos:

    def test_latitude_out_of_range(self, client, auth_headers):
        """Birth place with latitude > 90 → 422 (validation error)."""
        payload = {**VALID_KUNDLI_PAYLOAD, "latitude": 999.0}
        resp = client.post("/api/kundli/generate", json=payload, headers=auth_headers)
        assert resp.status_code == 422

    def test_longitude_out_of_range(self, client, auth_headers):
        """Birth place with longitude > 180 → 422."""
        payload = {**VALID_KUNDLI_PAYLOAD, "longitude": -999.0}
        resp = client.post("/api/kundli/generate", json=payload, headers=auth_headers)
        assert resp.status_code == 422

    def test_concurrent_kundli_generation(self, client, auth_headers):
        """Concurrent kundli generation (10 threads) → all succeed (CHAOS #6)."""
        def generate_one(i):
            payload = {**VALID_KUNDLI_PAYLOAD, "person_name": f"Concurrent Person {i}"}
            return client.post("/api/kundli/generate", json=payload, headers=auth_headers)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(generate_one, i) for i in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        success_count = sum(1 for r in results if r.status_code == 201)
        assert success_count == 10, f"Only {success_count}/10 concurrent requests succeeded"

    def test_empty_person_name(self, client, auth_headers):
        """Empty person_name → 422."""
        payload = {**VALID_KUNDLI_PAYLOAD, "person_name": ""}
        resp = client.post("/api/kundli/generate", json=payload, headers=auth_headers)
        assert resp.status_code == 422
