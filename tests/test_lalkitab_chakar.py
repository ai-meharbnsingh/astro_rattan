"""
tests/test_lalkitab_chakar.py
Tests for detect_chakar_cycle() in app/lalkitab_chakar.py.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.lalkitab_chakar import detect_chakar_cycle


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _check_common_fields(result: dict) -> None:
    """Assert every result carries the mandatory invariant fields."""
    assert result["source"] == "LK_CANONICAL"
    assert result["lk_ref"] == "3.04"
    assert result["cycle_length"] in (35, 36)
    assert result["trigger"] in ("visible_lord", "shadow_in_h1", "unknown_sign")
    assert isinstance(result["reason_en"], str) and result["reason_en"]
    assert isinstance(result["reason_hi"], str) and result["reason_hi"]


# ---------------------------------------------------------------------------
# Test 1 – Leo ascendant → 35-Sala, lord = Sun, trigger = visible_lord
# ---------------------------------------------------------------------------

def test_leo_ascendant_sun_lord_35_sala():
    result = detect_chakar_cycle("Leo")
    assert result["cycle_length"] == 35
    assert result["ascendant_lord"] == "Sun"
    assert result["trigger"] == "visible_lord"
    assert result["ascendant_sign"] == "Leo"
    assert result["shadow_year_en"] is None
    assert result["shadow_year_hi"] is None
    _check_common_fields(result)


# ---------------------------------------------------------------------------
# Test 2 – Scorpio ascendant → 35-Sala, lord = Mars
# ---------------------------------------------------------------------------

def test_scorpio_ascendant_mars_lord_35_sala():
    result = detect_chakar_cycle("Scorpio")
    assert result["cycle_length"] == 35
    assert result["ascendant_lord"] == "Mars"
    assert result["trigger"] == "visible_lord"
    assert result["shadow_year_en"] is None
    _check_common_fields(result)


# ---------------------------------------------------------------------------
# Test 3 – Aquarius ascendant with Rahu in H1 → 36-Sala, trigger = shadow_in_h1
# ---------------------------------------------------------------------------

def test_aquarius_rahu_in_h1_36_sala():
    result = detect_chakar_cycle("Aquarius", planets_in_h1=["Rahu"])
    assert result["cycle_length"] == 36
    assert result["ascendant_lord"] == "Rahu"
    assert result["trigger"] == "shadow_in_h1"
    assert result["ascendant_sign"] == "Aquarius"
    # shadow_year fields must be populated for 36-Sala
    assert result["shadow_year_en"] is not None
    assert result["shadow_year_hi"] is not None
    assert len(result["shadow_year_en"]) > 0
    _check_common_fields(result)


# ---------------------------------------------------------------------------
# Test 4 – Cancer ascendant with Ketu in H1 → 36-Sala
# ---------------------------------------------------------------------------

def test_cancer_ketu_in_h1_36_sala():
    result = detect_chakar_cycle("Cancer", planets_in_h1=["Ketu"])
    assert result["cycle_length"] == 36
    assert result["ascendant_lord"] == "Ketu"
    assert result["trigger"] == "shadow_in_h1"
    assert result["shadow_year_en"] is not None
    _check_common_fields(result)


# ---------------------------------------------------------------------------
# Test 5 – Both Rahu and Ketu in H1 → Rahu wins, 36-Sala
# ---------------------------------------------------------------------------

def test_rahu_ketu_both_in_h1_rahu_wins():
    result = detect_chakar_cycle("Aries", planets_in_h1=["Ketu", "Rahu"])
    assert result["cycle_length"] == 36
    assert result["ascendant_lord"] == "Rahu"   # Rahu wins over Ketu (canonical)
    assert result["trigger"] == "shadow_in_h1"
    _check_common_fields(result)


# ---------------------------------------------------------------------------
# Test 6 – Unknown sign → trigger = unknown_sign, 35-Sala, empty lord
# ---------------------------------------------------------------------------

def test_unknown_sign_defaults_to_35_sala():
    result = detect_chakar_cycle("Ophiuchus")
    assert result["cycle_length"] == 35
    assert result["trigger"] == "unknown_sign"
    assert result["ascendant_lord"] == ""
    assert result["ascendant_lord_hi"] == ""
    assert result["shadow_year_en"] is None
    assert result["shadow_year_hi"] is None
    _check_common_fields(result)


# ---------------------------------------------------------------------------
# Test 7 – Case-insensitive input: "leo" → same as "Leo"
# ---------------------------------------------------------------------------

def test_lowercase_sign_normalised():
    result_lower = detect_chakar_cycle("leo")
    result_title = detect_chakar_cycle("Leo")
    assert result_lower["cycle_length"] == result_title["cycle_length"]
    assert result_lower["ascendant_lord"] == result_title["ascendant_lord"]
    assert result_lower["trigger"] == result_title["trigger"]
    # The echoed sign should be normalised to title-case
    assert result_lower["ascendant_sign"] == "Leo"


# ---------------------------------------------------------------------------
# Test 8 – shadow_year fields populated for 36-Sala, None for 35-Sala
# ---------------------------------------------------------------------------

def test_shadow_year_only_for_36_sala():
    # 36-Sala case
    result_36 = detect_chakar_cycle("Gemini", planets_in_h1=["Rahu"])
    assert result_36["cycle_length"] == 36
    assert result_36["shadow_year_en"] is not None
    assert result_36["shadow_year_hi"] is not None

    # 35-Sala case (no shadow planet in H1)
    result_35 = detect_chakar_cycle("Gemini")
    assert result_35["cycle_length"] == 35
    assert result_35["shadow_year_en"] is None
    assert result_35["shadow_year_hi"] is None


# ---------------------------------------------------------------------------
# Test 9 – Hindi fields present for known signs and planets
# ---------------------------------------------------------------------------

def test_hindi_fields_populated_for_known_sign():
    result = detect_chakar_cycle("Aries")
    assert result["ascendant_sign_hi"] == "मेष"
    assert result["ascendant_lord"] == "Mars"
    assert result["ascendant_lord_hi"] == "मंगल"


# ---------------------------------------------------------------------------
# Test 10 – Visible-planet lords for several signs (spot-check the mapping)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("sign,expected_lord", [
    ("Taurus",      "Venus"),
    ("Gemini",      "Mercury"),
    ("Virgo",       "Mercury"),
    ("Libra",       "Venus"),
    ("Sagittarius", "Jupiter"),
    ("Capricorn",   "Saturn"),
    ("Pisces",      "Jupiter"),
    ("Cancer",      "Moon"),
])
def test_sign_lord_mapping(sign, expected_lord):
    result = detect_chakar_cycle(sign)
    assert result["cycle_length"] == 35
    assert result["ascendant_lord"] == expected_lord
    assert result["trigger"] == "visible_lord"


# ---------------------------------------------------------------------------
# Test 11 – Empty planets_in_h1 list still returns 35-Sala for normal sign
# ---------------------------------------------------------------------------

def test_empty_h1_planets_returns_35_sala():
    result = detect_chakar_cycle("Leo", planets_in_h1=[])
    assert result["cycle_length"] == 35
    assert result["trigger"] == "visible_lord"


# ---------------------------------------------------------------------------
# Test 12 – Non-shadow planets in H1 do not trigger 36-Sala
# ---------------------------------------------------------------------------

def test_visible_planet_in_h1_does_not_trigger_36_sala():
    # Jupiter sitting in H1 of a Leo ascendant chart — should not change cycle
    result = detect_chakar_cycle("Leo", planets_in_h1=["Jupiter", "Mars"])
    assert result["cycle_length"] == 35
    assert result["trigger"] == "visible_lord"
    assert result["ascendant_lord"] == "Sun"
