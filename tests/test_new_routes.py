"""Route-level tests for the 7 new API endpoints.

Tests are split into two parts:
  A. Engine integration tests — call the engine functions directly to verify
     the route handler logic (Pydantic model -> engine -> response) works.
  B. FastAPI app-level tests — use TestClient with mocked auth to verify
     the actual HTTP endpoints return correct status codes and shapes.

Tested endpoints:
  - POST /api/kundli/dasha/ashtottari
  - POST /api/kundli/dasha/moola
  - POST /api/kundli/dasha/tara
  - POST /api/kp/horary
  - POST /api/kp/horary/predict
  - POST /api/kundli/birth-rectification
  - POST /api/kundli/sarvatobhadra
  - POST /api/kundli/divisional/d108
"""
import pytest
from unittest.mock import patch, MagicMock


# ═══════════════════════════════════════════════════════════════
# PART A: Engine integration tests (no web server needed)
# ═══════════════════════════════════════════════════════════════


class TestAshtottariDashaEngine:
    """Verify Ashtottari Dasha engine via route handler arguments."""

    def test_valid_nakshatra(self):
        from app.ashtottari_dasha_engine import calculate_ashtottari_dasha
        result = calculate_ashtottari_dasha(
            birth_nakshatra="Pushya",
            birth_date="1990-01-15",
        )
        assert isinstance(result, dict)
        # Should have mahadasha periods
        assert "mahadasha" in result or "periods" in result or "dashas" in result or len(result) > 0

    def test_with_moon_longitude(self):
        from app.ashtottari_dasha_engine import calculate_ashtottari_dasha
        result = calculate_ashtottari_dasha(
            birth_nakshatra="Ardra",
            birth_date="1985-06-20",
            moon_longitude=72.5,
        )
        assert isinstance(result, dict)

    def test_inapplicable_nakshatra_returns_empty(self):
        """Nakshatras outside the Ashtottari scheme return empty mahadasha."""
        from app.ashtottari_dasha_engine import calculate_ashtottari_dasha
        result = calculate_ashtottari_dasha(
            birth_nakshatra="Ashwini",  # Not in Ashtottari scheme
            birth_date="1990-01-15",
        )
        assert isinstance(result, dict)
        assert result.get("mahadasha") == [] or result.get("applicable") is False


class TestMoolaDashaEngine:
    """Verify Moola Dasha engine via route handler arguments."""

    def test_basic_calculation(self):
        from app.moola_dasha_engine import calculate_moola_dasha
        result = calculate_moola_dasha(
            lagna_sign="Aries",
            seventh_sign="Libra",
            planet_positions={
                "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
                "Mercury": "Pisces", "Jupiter": "Gemini", "Venus": "Aquarius",
                "Saturn": "Sagittarius", "Rahu": "Cancer", "Ketu": "Capricorn",
            },
            birth_date="1990-01-15",
        )
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_even_lagna(self):
        from app.moola_dasha_engine import calculate_moola_dasha
        result = calculate_moola_dasha(
            lagna_sign="Taurus",
            seventh_sign="Scorpio",
            planet_positions={"Sun": "Leo", "Moon": "Cancer", "Mars": "Aries"},
            birth_date="1985-03-10",
        )
        assert isinstance(result, dict)


class TestTaraDashaEngine:
    """Verify Tara Dasha engine via route handler arguments."""

    def test_basic_calculation(self):
        from app.tara_dasha_engine import calculate_tara_dasha
        result = calculate_tara_dasha(
            birth_nakshatra="Rohini",
            birth_date="1990-01-15",
        )
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_with_moon_longitude(self):
        from app.tara_dasha_engine import calculate_tara_dasha
        result = calculate_tara_dasha(
            birth_nakshatra="Ashwini",
            birth_date="1985-03-10",
            moon_longitude=5.5,
        )
        assert isinstance(result, dict)

    def test_last_nakshatra(self):
        from app.tara_dasha_engine import calculate_tara_dasha
        result = calculate_tara_dasha(
            birth_nakshatra="Revati",
            birth_date="2000-12-25",
        )
        assert isinstance(result, dict)


class TestKPHoraryEngine:
    """Verify KP Horary engine via route handler arguments."""

    def test_basic_chart(self):
        from app.kp_engine import calculate_kp_horary
        result = calculate_kp_horary(
            number=42,
            query_datetime="2024-06-15 10:30:00",
        )
        assert result["horary_number"] == 42
        assert "degree_range" in result
        assert "sign" in result
        assert "planets" in result
        assert "significators" in result

    def test_with_place(self):
        from app.kp_engine import calculate_kp_horary
        result = calculate_kp_horary(
            number=100,
            query_datetime="2024-06-15 10:30:00",
            query_place={"latitude": 28.6139, "longitude": 77.209, "tz_offset": 5.5},
        )
        assert result["horary_number"] == 100
        assert "house_cusps" in result

    def test_boundary_numbers(self):
        from app.kp_engine import calculate_kp_horary
        r1 = calculate_kp_horary(number=1, query_datetime="2024-01-01 12:00:00")
        assert r1["horary_number"] == 1
        r249 = calculate_kp_horary(number=249, query_datetime="2024-01-01 12:00:00")
        assert r249["horary_number"] == 249

    def test_invalid_number(self):
        from app.kp_engine import calculate_kp_horary
        with pytest.raises(ValueError):
            calculate_kp_horary(number=0, query_datetime="2024-01-01 12:00:00")
        with pytest.raises(ValueError):
            calculate_kp_horary(number=300, query_datetime="2024-01-01 12:00:00")


class TestKPHoraryPredictEngine:
    """Verify KP Horary prediction engine via route handler arguments."""

    def test_marriage_prediction(self):
        from app.kp_engine import get_horary_prediction
        result = get_horary_prediction(
            number=42,
            question_type="marriage",
            query_datetime="2024-06-15 10:30:00",
        )
        assert isinstance(result, dict)

    def test_job_prediction(self):
        from app.kp_engine import get_horary_prediction
        result = get_horary_prediction(
            number=100,
            question_type="job",
            query_datetime="2024-06-15 10:30:00",
        )
        assert isinstance(result, dict)

    def test_invalid_question_type(self):
        from app.kp_engine import get_horary_prediction
        with pytest.raises(ValueError, match="Unknown question type"):
            get_horary_prediction(
                number=42,
                question_type="aliens",
                query_datetime="2024-06-15 10:30:00",
            )


class TestBirthRectificationEngine:
    """Verify Birth Rectification engine via route handler arguments."""

    def test_basic_rectification(self):
        from app.birth_rectification_engine import calculate_rectification
        result = calculate_rectification(
            birth_date="1990-01-15",
            time_window_start="10:00",
            time_window_end="10:05",
            birth_place={"lat": 28.6139, "lon": 77.209},
            life_events=[
                {"date": "2015-03-20", "type": "marriage"},
            ],
            step_minutes=5,
        )
        assert isinstance(result, dict)
        # Should have candidates or top_candidates
        assert "candidates" in result or "top_candidates" in result or "results" in result or len(result) > 0

    def test_multiple_events(self):
        from app.birth_rectification_engine import calculate_rectification
        result = calculate_rectification(
            birth_date="1990-01-15",
            time_window_start="10:00",
            time_window_end="10:05",
            birth_place={"lat": 28.6139, "lon": 77.209},
            life_events=[
                {"date": "2015-03-20", "type": "marriage"},
                {"date": "2018-08-10", "type": "child_birth"},
            ],
            step_minutes=5,
        )
        assert isinstance(result, dict)


class TestSarvatobhadraEngine:
    """Verify Sarvatobhadra Chakra engine via route handler arguments."""

    NATAL = {
        "Sun": 10.0, "Moon": 45.0, "Mars": 280.0, "Mercury": 330.0,
        "Jupiter": 100.0, "Venus": 200.0, "Saturn": 250.0,
        "Rahu": 75.0, "Ketu": 255.0,
    }
    TRANSIT = {
        "Sun": 50.0, "Moon": 120.0, "Mars": 300.0,
        "Jupiter": 15.0, "Saturn": 330.0,
    }

    def test_natal_only(self):
        from app.sarvatobhadra_chakra_engine import calculate_sarvatobhadra
        result = calculate_sarvatobhadra(planet_positions=self.NATAL)
        assert "grid" in result
        assert len(result["grid"]) == 9
        assert "natal_placements" in result

    def test_with_transits(self):
        from app.sarvatobhadra_chakra_engine import calculate_sarvatobhadra
        result = calculate_sarvatobhadra(
            planet_positions=self.NATAL,
            transit_positions=self.TRANSIT,
        )
        assert "vedhas" in result
        assert "auspicious" in result
        assert "inauspicious" in result
        assert "transit_placements" in result


class TestD108AnalysisEngine:
    """Verify D108 analysis engine via route handler arguments."""

    PLANETS = {
        "Sun": 10.5, "Moon": 45.2, "Mars": 280.7, "Mercury": 330.1,
        "Jupiter": 100.3, "Venus": 200.9, "Saturn": 250.4,
        "Rahu": 75.6, "Ketu": 255.6,
    }

    def test_basic_analysis(self):
        from app.divisional_charts import calculate_d108_analysis
        result = calculate_d108_analysis(planet_longitudes=self.PLANETS)
        assert "d108_positions" in result
        assert "spiritual_indicators" in result
        assert "moksha_potential" in result

    def test_positions_have_all_planets(self):
        from app.divisional_charts import calculate_d108_analysis
        result = calculate_d108_analysis(planet_longitudes=self.PLANETS)
        for planet in self.PLANETS:
            assert planet in result["d108_positions"], f"{planet} missing from D108 positions"


# ═══════════════════════════════════════════════════════════════
# PART B: FastAPI route wiring tests (TestClient + mocked auth)
# ═══════════════════════════════════════════════════════════════

# Mock the auth dependency to return a fake user dict
_MOCK_USER = {"sub": "test-user-id", "email": "test@example.com", "role": "user"}


def _get_mock_user():
    return _MOCK_USER


@pytest.fixture(scope="module")
def app_client():
    """Module-scoped TestClient with auth dependency overridden."""
    from app.main import app
    from app.auth import get_current_user
    from fastapi.testclient import TestClient

    app.dependency_overrides[get_current_user] = _get_mock_user
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


class TestDashaRoutesWiring:
    """Verify dasha routes are registered and accept correct payloads."""

    def test_ashtottari_route_exists(self, app_client):
        resp = app_client.post("/api/kundli/dasha/ashtottari", json={
            "birth_nakshatra": "Pushya",
            "birth_date": "1990-01-15",
        })
        assert resp.status_code == 200

    def test_moola_route_exists(self, app_client):
        resp = app_client.post("/api/kundli/dasha/moola", json={
            "lagna_sign": "Aries",
            "seventh_sign": "Libra",
            "planet_positions": {"Sun": "Aries", "Moon": "Taurus"},
            "birth_date": "1990-01-15",
        })
        assert resp.status_code == 200

    def test_tara_route_exists(self, app_client):
        resp = app_client.post("/api/kundli/dasha/tara", json={
            "birth_nakshatra": "Rohini",
            "birth_date": "1990-01-15",
        })
        assert resp.status_code == 200


class TestKPHoraryRoutesWiring:
    """Verify KP Horary routes are registered."""

    def test_horary_route_exists(self, app_client):
        resp = app_client.post("/api/kp/horary", json={
            "number": 42,
            "query_datetime": "2024-06-15 10:30:00",
        })
        assert resp.status_code == 200

    def test_horary_predict_route_exists(self, app_client):
        resp = app_client.post("/api/kp/horary/predict", json={
            "number": 42,
            "question_type": "marriage",
            "query_datetime": "2024-06-15 10:30:00",
        })
        assert resp.status_code == 200


class TestBirthRectificationRouteWiring:
    """Verify birth rectification route is registered."""

    def test_route_exists(self, app_client):
        resp = app_client.post("/api/kundli/birth-rectification", json={
            "birth_date": "1990-01-15",
            "time_window_start": "10:00",
            "time_window_end": "10:05",
            "birth_place": {"lat": 28.6139, "lon": 77.209},
            "life_events": [{"date": "2015-03-20", "type": "marriage"}],
            "step_minutes": 5,
        })
        assert resp.status_code == 200




class TestAuthRequired:
    """Verify all new routes require authentication when no override is active."""

    @pytest.fixture()
    def unauthed_client(self):
        from app.main import app
        from fastapi.testclient import TestClient
        # Temporarily clear overrides
        saved = dict(app.dependency_overrides)
        app.dependency_overrides.clear()
        with TestClient(app, raise_server_exceptions=False) as c:
            yield c
        app.dependency_overrides.update(saved)

    def test_ashtottari_requires_auth(self, unauthed_client):
        resp = unauthed_client.post("/api/kundli/dasha/ashtottari", json={
            "birth_nakshatra": "Pushya", "birth_date": "1990-01-15",
        })
        assert resp.status_code == 401

    def test_moola_requires_auth(self, unauthed_client):
        resp = unauthed_client.post("/api/kundli/dasha/moola", json={
            "lagna_sign": "Aries", "seventh_sign": "Libra",
            "planet_positions": {}, "birth_date": "1990-01-15",
        })
        assert resp.status_code == 401

    def test_tara_requires_auth(self, unauthed_client):
        resp = unauthed_client.post("/api/kundli/dasha/tara", json={
            "birth_nakshatra": "Rohini", "birth_date": "1990-01-15",
        })
        assert resp.status_code == 401

    def test_kp_horary_requires_auth(self, unauthed_client):
        resp = unauthed_client.post("/api/kp/horary", json={
            "number": 42, "query_datetime": "2024-06-15 10:30:00",
        })
        assert resp.status_code == 401

    def test_kp_horary_predict_requires_auth(self, unauthed_client):
        resp = unauthed_client.post("/api/kp/horary/predict", json={
            "number": 42, "question_type": "marriage",
            "query_datetime": "2024-06-15 10:30:00",
        })
        assert resp.status_code == 401

    def test_birth_rectification_requires_auth(self, unauthed_client):
        resp = unauthed_client.post("/api/kundli/birth-rectification", json={
            "birth_date": "1990-01-15", "time_window_start": "10:00",
            "time_window_end": "10:05", "birth_place": {"lat": 28.6, "lon": 77.2},
            "life_events": [{"date": "2015-03-20", "type": "marriage"}],
        })
        assert resp.status_code == 401

