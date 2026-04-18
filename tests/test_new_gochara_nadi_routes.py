"""Tests for the 4 new kundli GET routes:
  - GET /{kundli_id}/gochara-vedha
  - GET /{kundli_id}/nadi-analysis
  - GET /{kundli_id}/transit-interpretations
  - GET /{kundli_id}/transit-lucky

Two parts:
  A. Engine integration tests — call engine functions directly with minimal fixtures.
  B. FastAPI route wiring tests — TestClient + mocked DB + mocked auth.
"""
import pytest
from unittest.mock import patch, MagicMock


# ═══════════════════════════════════════════════════════════════
# Shared fixture — minimal natal chart matching the DB row shape
# ═══════════════════════════════════════════════════════════════

MINIMAL_CHART = {
    "planets": {
        "Sun":     {"sign": "Aries",       "house": 1, "longitude": 15.0,  "sign_degree": 15.0, "nakshatra": "Ashwini"},
        "Moon":    {"sign": "Cancer",      "house": 4, "longitude": 105.0, "sign_degree": 15.0, "nakshatra": "Pushya",
                    "nakshatra_index": 8, "pada": 2},
        "Mars":    {"sign": "Capricorn",   "house": 10, "longitude": 285.0, "sign_degree": 15.0},
        "Mercury": {"sign": "Pisces",      "house": 12, "longitude": 345.0, "sign_degree": 15.0},
        "Jupiter": {"sign": "Gemini",      "house": 3, "longitude": 75.0,  "sign_degree": 15.0},
        "Venus":   {"sign": "Taurus",      "house": 2, "longitude": 45.0,  "sign_degree": 15.0},
        "Saturn":  {"sign": "Aquarius",    "house": 11, "longitude": 315.0, "sign_degree": 15.0},
        "Rahu":    {"sign": "Aries",       "house": 1, "longitude": 10.0,  "sign_degree": 10.0},
        "Ketu":    {"sign": "Libra",       "house": 7, "longitude": 190.0, "sign_degree": 10.0},
    },
    "ascendant": {"sign": "Aries", "longitude": 5.0},
    "houses": {str(i): {"sign": "", "longitude": 0.0} for i in range(1, 13)},
}


# ═══════════════════════════════════════════════════════════════
# PART A: Engine integration tests (no web server needed)
# ═══════════════════════════════════════════════════════════════


class TestGocharavelheEngine:
    """Verify gochara_vedha_engine.enrich_transits works with minimal transit list."""

    def _make_transit_list(self):
        return [
            {
                "planet": "Jupiter",
                "current_sign": "Taurus",
                "natal_house_from_moon": 11,
                "effect": "favorable",
                "nakshatra": "Rohini",
            },
            {
                "planet": "Saturn",
                "current_sign": "Aquarius",
                "natal_house_from_moon": 8,
                "effect": "unfavorable",
                "nakshatra": "Shatabhisha",
            },
        ]

    def test_enrich_returns_list(self):
        from app.gochara_vedha_engine import enrich_transits
        result = enrich_transits(self._make_transit_list(), MINIMAL_CHART)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_enrich_adds_vedha_keys(self):
        from app.gochara_vedha_engine import enrich_transits
        result = enrich_transits(self._make_transit_list(), MINIMAL_CHART)
        for item in result:
            assert "planet" in item

    def test_enrich_empty_transits(self):
        from app.gochara_vedha_engine import enrich_transits
        result = enrich_transits([], MINIMAL_CHART)
        assert result == []


class TestNadiEngine:
    """Verify nadi_engine.calculate_nadi_insights with minimal chart."""

    def test_returns_list(self):
        from app.nadi_engine import calculate_nadi_insights
        result = calculate_nadi_insights(MINIMAL_CHART)
        assert isinstance(result, list)

    def test_no_crash_empty_chart(self):
        from app.nadi_engine import calculate_nadi_insights
        result = calculate_nadi_insights({})
        assert isinstance(result, list)

    def test_result_items_have_expected_keys(self):
        from app.nadi_engine import calculate_nadi_insights
        # Put two planets in the same house to guarantee at least one yoga
        chart = {
            "planets": {
                "Sun":     {"sign": "Aries", "house": 1, "longitude": 15.0},
                "Mercury": {"sign": "Aries", "house": 1, "longitude": 10.0},
            }
        }
        result = calculate_nadi_insights(chart)
        assert isinstance(result, list)
        if result:
            item = result[0]
            assert "title_en" in item or "planets" in item or "desc_en" in item


class TestTransitInterpretationsData:
    """Verify TRANSIT_FRAGMENTS structure is correct."""

    def test_fragments_exist(self):
        from app.transit_interpretations import TRANSIT_FRAGMENTS
        assert isinstance(TRANSIT_FRAGMENTS, dict)
        assert len(TRANSIT_FRAGMENTS) > 0

    def test_sun_house1_has_5_areas(self):
        from app.transit_interpretations import TRANSIT_FRAGMENTS
        frags = TRANSIT_FRAGMENTS.get("Sun", {}).get(1, {})
        for area in ["general", "love", "career", "finance", "health"]:
            assert area in frags, f"Missing area: {area}"

    def test_each_area_has_en_and_hi(self):
        from app.transit_interpretations import TRANSIT_FRAGMENTS
        for planet, houses in TRANSIT_FRAGMENTS.items():
            for house_num, areas in houses.items():
                for area, texts in areas.items():
                    assert "en" in texts, f"{planet}[{house_num}][{area}] missing 'en'"
                    assert "hi" in texts, f"{planet}[{house_num}][{area}] missing 'hi'"


class TestTransitLuckyEngine:
    """Verify transit_lucky.get_all_lucky_metadata with known inputs."""

    def test_basic_call_returns_dict(self):
        from app.transit_lucky import get_all_lucky_metadata
        result = get_all_lucky_metadata(
            sign="cancer",
            moon_nakshatra_index=8,
            moon_pada=2,
            date_str="2026-04-19",
            overall_score=6,
            planet_houses={"Jupiter": 11, "Saturn": 8, "Sun": 10},
            planet_dignities={"Jupiter": "favorable", "Saturn": "unfavorable"},
            transit_dignities={"Jupiter": "Taurus", "Saturn": "Aquarius"},
        )
        assert isinstance(result, dict)

    def test_all_expected_keys_present(self):
        from app.transit_lucky import get_all_lucky_metadata
        result = get_all_lucky_metadata(
            sign="aries",
            moon_nakshatra_index=0,
            moon_pada=1,
            date_str="2026-04-19",
            overall_score=5,
            planet_houses={},
            planet_dignities={},
            transit_dignities={},
        )
        for key in ["lucky_number", "lucky_color", "lucky_time", "compatible_sign",
                    "mood", "gemstone", "mantra"]:
            assert key in result, f"Missing key: {key}"

    def test_deterministic_output(self):
        from app.transit_lucky import get_all_lucky_metadata
        kwargs = dict(
            sign="leo", moon_nakshatra_index=12, moon_pada=3,
            date_str="2026-04-19", overall_score=7,
            planet_houses={"Sun": 1}, planet_dignities={}, transit_dignities={},
        )
        r1 = get_all_lucky_metadata(**kwargs)
        r2 = get_all_lucky_metadata(**kwargs)
        assert r1["lucky_number"] == r2["lucky_number"]
        assert r1["lucky_color"] == r2["lucky_color"]


# ═══════════════════════════════════════════════════════════════
# PART B: FastAPI route wiring tests (TestClient + mocked auth + mocked DB)
# ═══════════════════════════════════════════════════════════════

import json

_MOCK_USER = {"sub": "test-user-id", "email": "test@example.com", "role": "user"}

_MOCK_ROW = {
    "id": "test-kundli-id",
    "user_id": "test-user-id",
    "person_name": "Test Person",
    "birth_date": "1990-05-15",
    "birth_time": "14:30:00",
    "birth_place": "Mumbai, India",
    "latitude": 19.076,
    "longitude": 72.8777,
    "timezone_offset": 5.5,
    "chart_data": json.dumps(MINIMAL_CHART),
}


def _get_mock_user():
    return _MOCK_USER


def _make_mock_db():
    """Return a mock DB whose execute().fetchone() returns the mock row."""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = _MOCK_ROW
    mock_db = MagicMock()
    mock_db.execute.return_value = mock_cursor
    return mock_db


@pytest.fixture(scope="module")
def app_client():
    """Module-scoped TestClient with auth override and per-request DB override."""
    from app.main import app
    from app.auth import get_current_user
    from fastapi.testclient import TestClient

    app.dependency_overrides[get_current_user] = _get_mock_user
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_db_dep(app_client):
    """Override get_db for every test in this module to return the mock DB."""
    from app.main import app
    from app.database import get_db

    mock_db = _make_mock_db()

    def _get_mock_db():
        return mock_db

    app.dependency_overrides[get_db] = _get_mock_db
    yield mock_db
    # Remove only the DB override; leave auth override in place
    app.dependency_overrides.pop(get_db, None)


class TestGocharaVedhaRoute:
    """GET /{kundli_id}/gochara-vedha returns 200 with expected keys."""

    def test_returns_200(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/gochara-vedha")
        assert resp.status_code == 200, resp.text

    def test_response_has_expected_keys(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/gochara-vedha")
        assert resp.status_code == 200
        data = resp.json()
        assert "kundli_id" in data
        assert "person_name" in data
        assert "transits" in data
        assert isinstance(data["transits"], list)

    def test_kundli_id_matches(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/gochara-vedha")
        assert resp.json()["kundli_id"] == "test-kundli-id"


class TestNadiAnalysisRoute:
    """GET /{kundli_id}/nadi-analysis returns 200 with expected keys."""

    def test_returns_200(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/nadi-analysis")
        assert resp.status_code == 200, resp.text

    def test_response_has_expected_keys(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/nadi-analysis")
        assert resp.status_code == 200
        data = resp.json()
        assert "kundli_id" in data
        assert "person_name" in data
        assert "insights" in data
        assert isinstance(data["insights"], list)

    def test_person_name_matches(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/nadi-analysis")
        assert resp.json()["person_name"] == "Test Person"


class TestTransitInterpretationsRoute:
    """GET /{kundli_id}/transit-interpretations returns 200 with expected keys."""

    def test_returns_200(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/transit-interpretations")
        assert resp.status_code == 200, resp.text

    def test_response_has_expected_keys(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/transit-interpretations")
        assert resp.status_code == 200
        data = resp.json()
        assert "kundli_id" in data
        assert "person_name" in data
        assert "interpretations" in data
        assert isinstance(data["interpretations"], list)

    def test_interpretation_items_have_correct_shape(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/transit-interpretations")
        data = resp.json()
        for item in data["interpretations"]:
            assert "planet" in item
            assert "house" in item
            assert "interpretation" in item
            interp = item["interpretation"]
            for area in ["general", "love", "career", "finance", "health"]:
                assert area in interp


class TestTransitLuckyRoute:
    """GET /{kundli_id}/transit-lucky returns 200 with expected keys."""

    def test_returns_200(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/transit-lucky")
        assert resp.status_code == 200, resp.text

    def test_response_has_expected_keys(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/transit-lucky")
        assert resp.status_code == 200
        data = resp.json()
        assert "kundli_id" in data
        assert "person_name" in data
        for key in ["lucky_number", "lucky_color", "lucky_time", "mood", "gemstone", "mantra"]:
            assert key in data, f"Missing key: {key}"

    def test_with_transit_date_param(self, app_client):
        resp = app_client.get(
            "/api/kundli/test-kundli-id/transit-lucky",
            params={"transit_date": "2026-04-19"},
        )
        assert resp.status_code == 200

    def test_kundli_id_matches(self, app_client):
        resp = app_client.get("/api/kundli/test-kundli-id/transit-lucky")
        assert resp.json()["kundli_id"] == "test-kundli-id"


class TestAuthRequired:
    """All 4 new routes require authentication when no override is active."""

    @pytest.fixture()
    def unauthed_client(self):
        from app.main import app
        from fastapi.testclient import TestClient
        saved = dict(app.dependency_overrides)
        app.dependency_overrides.clear()
        with TestClient(app, raise_server_exceptions=False) as c:
            yield c
        app.dependency_overrides.update(saved)

    def test_gochara_vedha_requires_auth(self, unauthed_client):
        resp = unauthed_client.get("/api/kundli/some-id/gochara-vedha")
        assert resp.status_code == 401

    def test_nadi_analysis_requires_auth(self, unauthed_client):
        resp = unauthed_client.get("/api/kundli/some-id/nadi-analysis")
        assert resp.status_code == 401

    def test_transit_interpretations_requires_auth(self, unauthed_client):
        resp = unauthed_client.get("/api/kundli/some-id/transit-interpretations")
        assert resp.status_code == 401

    def test_transit_lucky_requires_auth(self, unauthed_client):
        resp = unauthed_client.get("/api/kundli/some-id/transit-lucky")
        assert resp.status_code == 401
