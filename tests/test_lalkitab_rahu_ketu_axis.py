"""
tests/test_lalkitab_rahu_ketu_axis.py
Tests for detect_rahu_ketu_axis() in app/lalkitab_rahu_ketu_axis.py.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.lalkitab_rahu_ketu_axis import detect_rahu_ketu_axis


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _positions(rahu_house: int, ketu_house: int):
    """Build a minimal planet_positions list with Rahu and Ketu."""
    return [
        {"planet": "Rahu", "house": rahu_house},
        {"planet": "Ketu", "house": ketu_house},
    ]


def _check_common_fields(result: dict, expected_axis_key: str) -> None:
    assert result["source"] == "LK_CANONICAL"
    assert result["lk_ref"] == "2.17"
    assert result["is_symmetric"] is True
    assert result["axis_key"] == expected_axis_key
    assert isinstance(result["life_areas"], list)
    assert len(result["life_areas"]) > 0
    assert isinstance(result["axis_en"], str) and result["axis_en"]
    assert isinstance(result["axis_hi"], str) and result["axis_hi"]
    assert isinstance(result["effect_en"], str) and result["effect_en"]
    assert isinstance(result["effect_hi"], str) and result["effect_hi"]
    assert isinstance(result["remedy_en"], str) and result["remedy_en"]
    assert isinstance(result["remedy_hi"], str) and result["remedy_hi"]


# ---------------------------------------------------------------------------
# Test 1 – Rahu H1, Ketu H7 → axis_key = "1-7"
# ---------------------------------------------------------------------------

def test_rahu_h1_ketu_h7():
    result = detect_rahu_ketu_axis(_positions(1, 7))
    assert result is not None
    assert result["rahu_house"] == 1
    assert result["ketu_house"] == 7
    _check_common_fields(result, "1-7")


# ---------------------------------------------------------------------------
# Test 2 – Rahu H2, Ketu H8 → axis_key = "2-8"
# ---------------------------------------------------------------------------

def test_rahu_h2_ketu_h8():
    result = detect_rahu_ketu_axis(_positions(2, 8))
    assert result is not None
    assert result["rahu_house"] == 2
    assert result["ketu_house"] == 8
    _check_common_fields(result, "2-8")


# ---------------------------------------------------------------------------
# Test 3 – Rahu H6, Ketu H12 → axis_key = "6-12"
# ---------------------------------------------------------------------------

def test_rahu_h6_ketu_h12():
    result = detect_rahu_ketu_axis(_positions(6, 12))
    assert result is not None
    assert result["rahu_house"] == 6
    assert result["ketu_house"] == 12
    _check_common_fields(result, "6-12")


# ---------------------------------------------------------------------------
# Test 4 – Reversed: Ketu H1, Rahu H7 → same axis_key "1-7"
# ---------------------------------------------------------------------------

def test_reversed_ketu_h1_rahu_h7_same_axis_key():
    positions = [
        {"planet": "Ketu", "house": 1},
        {"planet": "Rahu", "house": 7},
    ]
    result = detect_rahu_ketu_axis(positions)
    assert result is not None
    # axis_key must still normalise to "1-7"
    assert result["axis_key"] == "1-7"
    # rahu_house and ketu_house preserve the original values
    assert result["rahu_house"] == 7
    assert result["ketu_house"] == 1
    _check_common_fields(result, "1-7")


# ---------------------------------------------------------------------------
# Test 5 – Missing Rahu → None
# ---------------------------------------------------------------------------

def test_missing_rahu_returns_none():
    positions = [{"planet": "Ketu", "house": 7}]
    assert detect_rahu_ketu_axis(positions) is None


# ---------------------------------------------------------------------------
# Test 6 – Missing Ketu → None
# ---------------------------------------------------------------------------

def test_missing_ketu_returns_none():
    positions = [{"planet": "Rahu", "house": 1}]
    assert detect_rahu_ketu_axis(positions) is None


# ---------------------------------------------------------------------------
# Test 7 – Houses not exactly 6 apart (H1 + H8 = diff 7, not 6) → None
# ---------------------------------------------------------------------------

def test_houses_not_6_apart_returns_none():
    # H1 and H8 are 7 apart — not a valid 1-7 axis
    result = detect_rahu_ketu_axis(_positions(1, 8))
    assert result is None


# ---------------------------------------------------------------------------
# Test 8 – is_symmetric is always True for valid results
# ---------------------------------------------------------------------------

def test_is_symmetric_always_true():
    all_valid_axes = [
        (1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12),
    ]
    for rahu_h, ketu_h in all_valid_axes:
        result = detect_rahu_ketu_axis(_positions(rahu_h, ketu_h))
        assert result is not None, f"Expected valid result for {rahu_h}-{ketu_h}"
        assert result["is_symmetric"] is True


# ---------------------------------------------------------------------------
# Test 9 – life_areas is non-empty list for every valid axis
# ---------------------------------------------------------------------------

def test_life_areas_non_empty_for_all_axes():
    all_valid_axes = [
        (1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12),
    ]
    for rahu_h, ketu_h in all_valid_axes:
        result = detect_rahu_ketu_axis(_positions(rahu_h, ketu_h))
        assert result is not None
        assert isinstance(result["life_areas"], list)
        assert len(result["life_areas"]) > 0, f"life_areas empty for axis {rahu_h}-{ketu_h}"


# ---------------------------------------------------------------------------
# Test 10 – Empty planet list → None
# ---------------------------------------------------------------------------

def test_empty_planet_list_returns_none():
    assert detect_rahu_ketu_axis([]) is None


# ---------------------------------------------------------------------------
# Test 11 – All six axis keys are present and unique
# ---------------------------------------------------------------------------

def test_all_six_axes_return_unique_axis_keys():
    all_valid_axes = [(1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12)]
    keys_seen = set()
    for rahu_h, ketu_h in all_valid_axes:
        result = detect_rahu_ketu_axis(_positions(rahu_h, ketu_h))
        assert result is not None
        keys_seen.add(result["axis_key"])
    assert len(keys_seen) == 6


# ---------------------------------------------------------------------------
# Test 12 – Case-insensitive planet name matching ("rahu" → Rahu)
# ---------------------------------------------------------------------------

def test_case_insensitive_planet_names():
    positions = [
        {"planet": "rahu", "house": 3},
        {"planet": "KETU", "house": 9},
    ]
    result = detect_rahu_ketu_axis(positions)
    assert result is not None
    assert result["axis_key"] == "3-9"


# ---------------------------------------------------------------------------
# Test 13 – Additional planets in the list do not affect result
# ---------------------------------------------------------------------------

def test_extra_planets_ignored():
    positions = [
        {"planet": "Sun",     "house": 1},
        {"planet": "Jupiter", "house": 4},
        {"planet": "Rahu",    "house": 4},
        {"planet": "Ketu",    "house": 10},
    ]
    result = detect_rahu_ketu_axis(positions)
    assert result is not None
    assert result["axis_key"] == "4-10"
