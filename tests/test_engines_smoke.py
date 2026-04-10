"""Smoke tests for critical engine modules: varshphal, transit, astro_iogita, dasha.

Each test imports the module, calls the main function with sample data, and asserts
the result is a proper dict/list with expected keys and structure.
"""
import pytest
from datetime import datetime


# ── Sample chart data (Meharban Singh's chart from __main__ in astro_iogita_engine) ──

SAMPLE_PLANETS = {
    "Sun": "Leo",
    "Moon": "Scorpio",
    "Mercury": "Cancer",
    "Venus": "Cancer",
    "Mars": "Cancer",
    "Jupiter": "Capricorn",
    "Saturn": "Libra",
    "Rahu": "Aries",
    "Ketu": "Libra",
}

SAMPLE_NATAL_CHART = {
    "planets": {
        "Sun": {"sign": "Leo", "longitude": 130.5, "house": 1},
        "Moon": {"sign": "Scorpio", "longitude": 215.3, "house": 4},
        "Mercury": {"sign": "Cancer", "longitude": 105.2, "house": 12},
        "Venus": {"sign": "Cancer", "longitude": 110.8, "house": 12},
        "Mars": {"sign": "Cancer", "longitude": 98.1, "house": 12},
        "Jupiter": {"sign": "Capricorn", "longitude": 280.6, "house": 6},
        "Saturn": {"sign": "Libra", "longitude": 195.4, "house": 3},
        "Rahu": {"sign": "Aries", "longitude": 15.7, "house": 9},
        "Ketu": {"sign": "Libra", "longitude": 195.7, "house": 3},
    },
    "ascendant": {"sign": "Leo", "longitude": 125.0},
}


# ======================================================================
# varshphal_engine smoke tests
# ======================================================================

class TestVarshphalEngine:
    """Smoke tests for varshphal_engine.py."""

    def test_calculate_muntha_returns_dict_with_keys(self):
        from app.varshphal_engine import calculate_muntha
        result = calculate_muntha(125.0, 30)
        assert isinstance(result, dict)
        for key in ("sign", "sign_index", "degree", "lord"):
            assert key in result, f"Missing key: {key}"
        assert isinstance(result["sign"], str)
        assert 0 <= result["sign_index"] <= 11
        assert isinstance(result["degree"], float)
        assert result["lord"] in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")

    def test_calculate_muntha_advances_one_sign_per_year(self):
        from app.varshphal_engine import calculate_muntha, ZODIAC_SIGNS
        natal_asc_lon = 130.0  # Leo (index 4)
        result_0 = calculate_muntha(natal_asc_lon, 0)
        result_1 = calculate_muntha(natal_asc_lon, 1)
        # After 0 years = natal sign (Leo=4), after 1 year = next sign (Virgo=5)
        assert result_0["sign_index"] == 4
        assert result_1["sign_index"] == 5
        assert result_0["sign"] == "Leo"
        assert result_1["sign"] == "Virgo"

    def test_calculate_year_lord_returns_valid_planet(self):
        from app.varshphal_engine import calculate_year_lord, DAY_LORDS
        result = calculate_year_lord(2460000.0)
        assert result in DAY_LORDS

    def test_calculate_mudda_dasha_returns_7_periods(self):
        from app.varshphal_engine import calculate_mudda_dasha
        result = calculate_mudda_dasha("Sun", "2025-01-01")
        assert isinstance(result, list)
        assert len(result) == 7  # 7 planets in Tajaka cycle
        for period in result:
            assert "planet" in period
            assert "start_date" in period
            assert "end_date" in period
            assert "days" in period
            assert isinstance(period["days"], int)
            assert period["days"] > 0

    def test_calculate_mudda_dasha_dates_are_contiguous(self):
        from app.varshphal_engine import calculate_mudda_dasha
        result = calculate_mudda_dasha("Venus", "2025-06-15")
        for i in range(len(result) - 1):
            assert result[i]["end_date"] == result[i + 1]["start_date"], (
                f"Gap between period {i} and {i+1}"
            )

    def test_calculate_varshphal_returns_complete_result(self):
        from app.varshphal_engine import calculate_varshphal
        result = calculate_varshphal(
            natal_chart_data=SAMPLE_NATAL_CHART,
            target_year=2025,
            birth_date="1990-08-15",
            latitude=28.6139,
            longitude=77.2090,
            tz_offset=5.5,
        )
        assert isinstance(result, dict)
        # Check top-level keys
        for key in ("year", "completed_years", "solar_return", "chart_data",
                     "muntha", "year_lord", "mudda_dasha"):
            assert key in result, f"Missing key: {key}"

        assert result["year"] == 2025
        assert result["completed_years"] == 35

        # Solar return should have date and time
        sr = result["solar_return"]
        assert "date" in sr
        assert "time" in sr
        assert "julian_day" in sr

        # Muntha should be a dict with sign and house
        muntha = result["muntha"]
        assert "sign" in muntha
        assert "house" in muntha
        assert "favorable" in muntha
        assert isinstance(muntha["favorable"], bool)

        # Year lord should be a valid planet
        assert result["year_lord"] in ("Sun", "Moon", "Mars", "Mercury",
                                        "Jupiter", "Venus", "Saturn")

        # Mudda dasha should have 7 periods
        assert len(result["mudda_dasha"]) == 7


# ======================================================================
# transit_engine smoke tests
# ======================================================================

class TestTransitEngine:
    """Smoke tests for transit_engine.py."""

    def test_house_from_moon_same_sign_is_1(self):
        from app.transit_engine import _house_from_moon
        assert _house_from_moon("Aries", "Aries") == 1
        assert _house_from_moon("Scorpio", "Scorpio") == 1

    def test_house_from_moon_next_sign_is_2(self):
        from app.transit_engine import _house_from_moon
        assert _house_from_moon("Aries", "Taurus") == 2
        assert _house_from_moon("Pisces", "Aries") == 2

    def test_house_from_moon_wraps_around(self):
        from app.transit_engine import _house_from_moon
        # Aries(0) to Pisces(11) should be house 12
        assert _house_from_moon("Aries", "Pisces") == 12

    def test_check_sade_sati_active_peak(self):
        from app.transit_engine import _check_sade_sati
        # Saturn in same sign as Moon = peak phase (house 1)
        result = _check_sade_sati("Scorpio", "Scorpio")
        assert result["active"] is True
        assert "Peak" in result["phase"]

    def test_check_sade_sati_active_rising(self):
        from app.transit_engine import _check_sade_sati
        # Saturn in 12th from Moon = rising phase
        # Moon in Aries(0), Saturn in Pisces(11) = house 12
        result = _check_sade_sati("Aries", "Pisces")
        assert result["active"] is True
        assert "Rising" in result["phase"]

    def test_check_sade_sati_not_active(self):
        from app.transit_engine import _check_sade_sati
        # Saturn in 6th from Moon is NOT Sade Sati
        # Moon Aries(0), Saturn Virgo(5) = house 6
        result = _check_sade_sati("Aries", "Virgo")
        assert result["active"] is False

    def test_calculate_transits_returns_required_structure(self):
        from app.transit_engine import calculate_transits
        result = calculate_transits(
            natal_chart_data=SAMPLE_NATAL_CHART,
            latitude=28.6139,
            longitude=77.2090,
            transit_date="2025-06-15",
            transit_time="12:00:00",
        )
        assert isinstance(result, dict)
        assert "transits" in result
        assert "sade_sati" in result
        assert "transit_date" in result
        assert "natal_moon_sign" in result

        # Should have 9 planet transits
        transits = result["transits"]
        assert isinstance(transits, list)
        assert len(transits) == 9

        planet_names = [t["planet"] for t in transits]
        for expected in ("Sun", "Moon", "Mars", "Mercury", "Jupiter",
                         "Venus", "Saturn", "Rahu", "Ketu"):
            assert expected in planet_names

        # Each transit must have required keys
        for t in transits:
            assert "current_sign" in t
            assert "natal_house_from_moon" in t
            assert "effect" in t
            assert t["effect"] in ("favorable", "unfavorable")
            assert "description" in t
            assert isinstance(t["description"], str)
            assert len(t["description"]) > 10  # Not empty

    def test_gochara_favorable_has_all_planets(self):
        from app.transit_engine import GOCHARA_FAVORABLE
        expected_planets = {"Sun", "Moon", "Mars", "Mercury", "Jupiter",
                            "Venus", "Saturn", "Rahu", "Ketu"}
        assert set(GOCHARA_FAVORABLE.keys()) == expected_planets


# ======================================================================
# astro_iogita_engine smoke tests
# ======================================================================

class TestAstroIogitaEngine:
    """Smoke tests for astro_iogita_engine.py."""

    def test_build_atom_vector_returns_16_floats(self):
        from app.astro_iogita_engine import build_atom_vector
        vec = build_atom_vector(SAMPLE_PLANETS, "Venus")
        assert isinstance(vec, list)
        assert len(vec) == 16
        for v in vec:
            assert isinstance(v, float)

    def test_build_atom_vector_normalized_to_unit(self):
        from app.astro_iogita_engine import build_atom_vector
        vec = build_atom_vector(SAMPLE_PLANETS, "Venus")
        max_abs = max(abs(v) for v in vec)
        assert max_abs <= 1.0 + 1e-10, f"Max absolute value {max_abs} exceeds 1.0"

    def test_build_atom_vector_empty_planets_returns_zeros(self):
        from app.astro_iogita_engine import build_atom_vector
        vec = build_atom_vector({}, "Sun")
        assert all(v == 0.0 for v in vec)

    def test_identify_basin_returns_valid_basin(self):
        from app.astro_iogita_engine import build_atom_vector, identify_basin, BASIN_DEFINITIONS
        vec = build_atom_vector(SAMPLE_PLANETS, "Venus")
        basin = identify_basin(vec)
        assert basin["basin_name"] in BASIN_DEFINITIONS
        assert isinstance(basin["basin_hindi"], str)
        assert len(basin["basin_hindi"]) > 0
        assert isinstance(basin["description"], str)
        assert len(basin["description"]) > 20
        assert isinstance(basin["escape_possible"], bool)
        assert 20 <= basin["trajectory_steps"] <= 80

    def test_identify_basin_top_3_atoms(self):
        from app.astro_iogita_engine import build_atom_vector, identify_basin
        vec = build_atom_vector(SAMPLE_PLANETS, "Venus")
        basin = identify_basin(vec)
        assert "top_3_atoms" in basin
        assert len(basin["top_3_atoms"]) == 3
        for name, val in basin["top_3_atoms"]:
            assert isinstance(name, str)
            assert isinstance(val, float)

    def test_run_astro_analysis_full_pipeline(self):
        from app.astro_iogita_engine import run_astro_analysis
        result = run_astro_analysis(SAMPLE_PLANETS, "Venus", "Test Person")
        assert isinstance(result, dict)

        # Check top-level keys
        for key in ("person_name", "planet_positions", "current_dasha",
                     "planet_strengths", "atom_activations", "atom_vector",
                     "basin", "normal_astrology", "iogita_insight",
                     "engine_params", "version"):
            assert key in result, f"Missing key: {key}"

        assert result["person_name"] == "Test Person"
        assert result["current_dasha"] == "Venus"
        assert result["version"] == "2.0"

        # Planet strengths for all 9 planets
        assert len(result["planet_strengths"]) == 9
        for planet, info in result["planet_strengths"].items():
            assert "sign" in info
            assert "strength" in info
            assert "dignity" in info
            assert 0.0 <= info["strength"] <= 1.0

        # Atom activations for all 16 atoms
        assert len(result["atom_activations"]) == 16

        # Basin result
        basin = result["basin"]
        assert "name" in basin
        assert "hindi" in basin
        assert "description" in basin
        assert "top_3_atoms" in basin

        # Normal astrology has 4 bullet points
        assert len(result["normal_astrology"]) == 4

        # io-gita insight is a non-empty string
        assert isinstance(result["iogita_insight"], str)
        assert len(result["iogita_insight"]) > 50

    def test_get_planet_strength_covers_all_dignities(self):
        from app.astro_iogita_engine import get_planet_strength
        # Exalted
        assert get_planet_strength("Sun", "Aries") == 0.95
        # Debilitated
        assert get_planet_strength("Mars", "Cancer") == 0.20
        # Own sign
        assert get_planet_strength("Sun", "Leo") == 0.85
        # Friendly
        assert get_planet_strength("Sun", "Sagittarius") == 0.65
        # Enemy
        assert get_planet_strength("Sun", "Taurus") == 0.35
        # Neutral
        assert get_planet_strength("Sun", "Gemini") == 0.50


# ======================================================================
# dasha_engine smoke tests
# ======================================================================

class TestDashaEngine:
    """Smoke tests for dasha_engine.py."""

    def test_calculate_dasha_basic(self):
        from app.dasha_engine import calculate_dasha
        result = calculate_dasha("Ashwini", "1990-08-15")
        assert isinstance(result, dict)
        assert "mahadasha_periods" in result
        assert "current_dasha" in result
        assert "current_antardasha" in result
        # Design change: dasha now covers at least 240 years (2 full cycles)
        # to handle dates beyond the first 120-year cycle.
        # With no moon_longitude (full balance), expect exactly 18 periods (2 cycles).
        assert len(result["mahadasha_periods"]) == 18

    def test_calculate_dasha_total_years_240(self):
        """Design change: dasha now covers 2 full 120-year cycles = 240 years total."""
        from app.dasha_engine import calculate_dasha
        result = calculate_dasha("Rohini", "1995-01-01")
        total = sum(p["years"] for p in result["mahadasha_periods"])
        assert total == 240

    def test_calculate_dasha_with_moon_longitude(self):
        """When moon_longitude is given, first dasha balance is partial.

        Design change: dasha now covers at least 240 years from birth.
        With partial first period, total will be slightly less than 240
        but additional full cycles are appended to reach the 240-year
        coverage threshold, so total may exceed 240.
        """
        from app.dasha_engine import calculate_dasha
        # Ashwini spans 0 to 13.333 degrees. Moon at 6.666 = halfway through
        result = calculate_dasha("Ashwini", "1990-01-15", moon_longitude=6.666)
        periods = result["mahadasha_periods"]
        # First period (Ketu, full=7 years) should be roughly half
        assert periods[0]["planet"] == "Ketu"
        assert periods[0]["years"] < 7  # Less than full
        assert periods[0]["years"] > 0  # More than zero
        # Total covers at least 240 years from birth (partial first + full cycles)
        total = sum(p["years"] for p in periods)
        assert total > 240  # Partial first dasha means an extra cycle is needed
        assert total < 360  # But not more than 3 cycles

    def test_calculate_dasha_current_is_valid_planet(self):
        from app.dasha_engine import calculate_dasha, DASHA_ORDER
        result = calculate_dasha("Pushya", "2000-03-10")
        assert result["current_dasha"] in DASHA_ORDER
        assert result["current_antardasha"] in DASHA_ORDER

    def test_calculate_extended_dasha_has_antardasha(self):
        from app.dasha_engine import calculate_extended_dasha
        result = calculate_extended_dasha("Hasta", "1990-06-15")
        assert isinstance(result, dict)
        assert "mahadasha" in result
        assert "current_dasha" in result
        assert "current_antardasha" in result
        assert "current_pratyantar" in result

        # Each mahadasha should have antardasha sub-periods
        for md in result["mahadasha"]:
            assert "planet" in md
            assert "start" in md
            assert "end" in md
            assert "antardasha" in md
            assert isinstance(md["antardasha"], list)
            assert len(md["antardasha"]) == 9  # 9 sub-periods per mahadasha

    def test_calculate_extended_dasha_current_is_marked(self):
        from app.dasha_engine import calculate_extended_dasha
        result = calculate_extended_dasha("Swati", "1995-03-20")
        # Exactly one mahadasha should be current
        current_count = sum(1 for md in result["mahadasha"] if md["is_current"])
        assert current_count == 1

    def test_calculate_dasha_unknown_nakshatra_returns_error(self):
        from app.dasha_engine import calculate_dasha
        result = calculate_dasha("NonExistent", "1990-01-01")
        assert "error" in result
        assert result["current_dasha"] == "Unknown"
        assert len(result["mahadasha_periods"]) == 0

    def test_calculate_dasha_periods_are_chronological(self):
        from app.dasha_engine import calculate_dasha
        result = calculate_dasha("Mrigashira", "1985-11-30")
        periods = result["mahadasha_periods"]
        for i in range(len(periods) - 1):
            end_i = datetime.strptime(periods[i]["end_date"], "%Y-%m-%d")
            start_next = datetime.strptime(periods[i + 1]["start_date"], "%Y-%m-%d")
            assert abs((end_i - start_next).days) <= 1, (
                f"Gap between period {i} ({periods[i]['planet']}) and {i+1} ({periods[i+1]['planet']})"
            )
