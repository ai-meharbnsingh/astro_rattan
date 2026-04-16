"""
Tests for D108 (Ashtottaramsa) divisional chart calculation.
Verifies:
  - Calculation accuracy for known positions
  - All 3 sign types (movable, fixed, dual)
  - 108 parts per sign
  - Edge cases (0 deg, 29.999 deg, exact sign boundaries)
  - Analysis function output structure
"""
from __future__ import annotations

import pytest

from app.divisional_charts import (
    _calculate_d108,
    _SIGN_NAMES,
    calculate_d108_analysis,
    calculate_divisional_chart,
    calculate_divisional_chart_detailed,
)


# ----------------------------------------------------------------
# Helper
# ----------------------------------------------------------------
PART_SIZE = 30.0 / 108.0  # ~0.27778 degrees


def _expected_d108_sign(longitude: float) -> str:
    """Reference implementation for expected D108 sign."""
    lon = longitude % 360.0
    rasi_index = int(lon / 30.0) % 12
    degree_in_sign = lon - int(lon / 30.0) * 30.0
    part = min(int(degree_in_sign / PART_SIZE), 107)

    movable = {0, 3, 6, 9}
    fixed = {1, 4, 7, 10}

    if rasi_index in movable:
        start = rasi_index
    elif rasi_index in fixed:
        start = (rasi_index + 8) % 12
    else:
        start = (rasi_index + 4) % 12

    div_sign_index = (start + part) % 12
    return _SIGN_NAMES[div_sign_index]


# ----------------------------------------------------------------
# 1. Movable sign tests  (Aries=0, Cancer=3, Libra=6, Capricorn=9)
# ----------------------------------------------------------------

class TestMovableSigns:
    """Movable signs start counting from the same sign."""

    def test_aries_0_degrees(self):
        """0 deg Aries -> part 0 -> start=Aries(0) -> Aries"""
        result = _calculate_d108({"Sun": 0.0})
        assert result["Sun"]["sign"] == "Aries"

    def test_aries_small_offset(self):
        """Just inside first part of Aries."""
        result = _calculate_d108({"Sun": 0.1})
        assert result["Sun"]["sign"] == "Aries"

    def test_cancer_start(self):
        """0 deg Cancer (longitude 90) -> part 0 -> start=Cancer(3) -> Cancer"""
        result = _calculate_d108({"Sun": 90.0})
        assert result["Sun"]["sign"] == "Cancer"

    def test_libra_start(self):
        """0 deg Libra (longitude 180) -> part 0 -> start=Libra(6) -> Libra"""
        result = _calculate_d108({"Sun": 180.0})
        assert result["Sun"]["sign"] == "Libra"

    def test_capricorn_start(self):
        """0 deg Capricorn (longitude 270) -> part 0 -> start=Capricorn(9) -> Capricorn"""
        result = _calculate_d108({"Sun": 270.0})
        assert result["Sun"]["sign"] == "Capricorn"

    def test_aries_12_parts_forward(self):
        """Part 12 in Aries -> start(0)+12 = 12 mod 12 = 0 -> Aries (wraps)."""
        lon = 12 * PART_SIZE  # ~3.3333 deg in Aries
        result = _calculate_d108({"Mars": lon})
        assert result["Mars"]["sign"] == "Aries"

    def test_aries_part_1(self):
        """Part 1 in Aries -> Taurus."""
        lon = 1 * PART_SIZE + 0.001
        result = _calculate_d108({"Mars": lon})
        assert result["Mars"]["sign"] == "Taurus"


# ----------------------------------------------------------------
# 2. Fixed sign tests  (Taurus=1, Leo=4, Scorpio=7, Aquarius=10)
# ----------------------------------------------------------------

class TestFixedSigns:
    """Fixed signs start counting from the 9th sign (rasi + 8)."""

    def test_taurus_0_degrees(self):
        """0 deg Taurus (lon 30) -> part 0 -> start = (1+8)%12 = 9 = Capricorn"""
        result = _calculate_d108({"Moon": 30.0})
        assert result["Moon"]["sign"] == "Capricorn"

    def test_leo_0_degrees(self):
        """0 deg Leo (lon 120) -> part 0 -> start = (4+8)%12 = 0 = Aries"""
        result = _calculate_d108({"Moon": 120.0})
        assert result["Moon"]["sign"] == "Aries"

    def test_scorpio_0_degrees(self):
        """0 deg Scorpio (lon 210) -> part 0 -> start = (7+8)%12 = 3 = Cancer"""
        result = _calculate_d108({"Moon": 210.0})
        assert result["Moon"]["sign"] == "Cancer"

    def test_aquarius_0_degrees(self):
        """0 deg Aquarius (lon 300) -> part 0 -> start = (10+8)%12 = 6 = Libra"""
        result = _calculate_d108({"Moon": 300.0})
        assert result["Moon"]["sign"] == "Libra"

    def test_taurus_part_3(self):
        """Part 3 in Taurus -> start(9)+3 = 12 mod 12 = 0 = Aries"""
        lon = 30.0 + 3 * PART_SIZE + 0.001
        result = _calculate_d108({"Venus": lon})
        assert result["Venus"]["sign"] == "Aries"


# ----------------------------------------------------------------
# 3. Dual sign tests  (Gemini=2, Virgo=5, Sagittarius=8, Pisces=11)
# ----------------------------------------------------------------

class TestDualSigns:
    """Dual signs start counting from the 5th sign (rasi + 4)."""

    def test_gemini_0_degrees(self):
        """0 deg Gemini (lon 60) -> part 0 -> start = (2+4)%12 = 6 = Libra"""
        result = _calculate_d108({"Mercury": 60.0})
        assert result["Mercury"]["sign"] == "Libra"

    def test_virgo_0_degrees(self):
        """0 deg Virgo (lon 150) -> part 0 -> start = (5+4)%12 = 9 = Capricorn"""
        result = _calculate_d108({"Mercury": 150.0})
        assert result["Mercury"]["sign"] == "Capricorn"

    def test_sagittarius_0_degrees(self):
        """0 deg Sagittarius (lon 240) -> part 0 -> start = (8+4)%12 = 0 = Aries"""
        result = _calculate_d108({"Jupiter": 240.0})
        assert result["Jupiter"]["sign"] == "Aries"

    def test_pisces_0_degrees(self):
        """0 deg Pisces (lon 330) -> part 0 -> start = (11+4)%12 = 3 = Cancer"""
        result = _calculate_d108({"Jupiter": 330.0})
        assert result["Jupiter"]["sign"] == "Cancer"

    def test_gemini_part_6(self):
        """Part 6 in Gemini -> start(6)+6 = 12 mod 12 = 0 = Aries"""
        lon = 60.0 + 6 * PART_SIZE + 0.001
        result = _calculate_d108({"Mercury": lon})
        assert result["Mercury"]["sign"] == "Aries"


# ----------------------------------------------------------------
# 4. 108 parts per sign
# ----------------------------------------------------------------

class TestPartCount:
    """Every sign must produce exactly 108 distinct (part -> sign_index) mappings,
    cycling through all 12 signs 9 times (108/12 = 9)."""

    @pytest.mark.parametrize("rasi_index", range(12))
    def test_108_parts_all_signs(self, rasi_index: int):
        """Sample parts 0..107 for each sign and confirm all 12 target signs appear."""
        base_lon = rasi_index * 30.0
        signs_seen = set()
        for p in range(108):
            lon = base_lon + p * PART_SIZE + PART_SIZE * 0.5  # midpoint of each part
            result = _calculate_d108({"P": lon})
            signs_seen.add(result["P"]["sign_index"])
        assert len(signs_seen) == 12, (
            f"Sign {_SIGN_NAMES[rasi_index]}: expected 12 target signs, got {len(signs_seen)}"
        )

    def test_parts_cycle_nine_times(self):
        """108 parts / 12 signs = 9 complete cycles for Aries."""
        sign_counts = [0] * 12
        base = 0.0
        for p in range(108):
            lon = base + p * PART_SIZE + PART_SIZE * 0.5
            result = _calculate_d108({"P": lon})
            sign_counts[result["P"]["sign_index"]] += 1
        assert all(c == 9 for c in sign_counts), f"Expected 9 each, got {sign_counts}"


# ----------------------------------------------------------------
# 5. Edge cases
# ----------------------------------------------------------------

class TestEdgeCases:

    def test_zero_longitude(self):
        """0.0 degrees = 0 deg Aries."""
        result = _calculate_d108({"X": 0.0})
        assert result["X"]["sign"] == "Aries"

    def test_just_below_30(self):
        """29.999 deg in Aries -> part 107 -> start(0)+107 = 107 mod 12 = 11 = Pisces"""
        result = _calculate_d108({"X": 29.999})
        # part = int(29.999 / PART_SIZE) -> int(29.999 / 0.27778) = int(107.9964) = 107
        expected = _expected_d108_sign(29.999)
        assert result["X"]["sign"] == expected

    def test_exact_sign_boundary_30(self):
        """Exactly 30.0 degrees = 0 deg Taurus (fixed sign)."""
        result = _calculate_d108({"X": 30.0})
        # Taurus: start = (1+8)%12 = 9 = Capricorn, part 0
        assert result["X"]["sign"] == "Capricorn"

    def test_exact_360(self):
        """360.0 wraps to 0.0 = 0 deg Aries."""
        result = _calculate_d108({"X": 360.0})
        assert result["X"]["sign"] == "Aries"

    def test_large_longitude(self):
        """Longitude > 360 wraps correctly."""
        result_wrapped = _calculate_d108({"X": 15.5})
        result_large = _calculate_d108({"X": 375.5})
        assert result_wrapped["X"]["sign"] == result_large["X"]["sign"]
        assert result_wrapped["X"]["degree"] == result_large["X"]["degree"]

    def test_negative_longitude_not_expected(self):
        """Negative input still produces valid output (mod 360)."""
        # -10 deg -> 350 deg -> Pisces territory
        result = _calculate_d108({"X": -10.0})
        expected = _expected_d108_sign(-10.0)
        assert result["X"]["sign"] == expected

    def test_part_boundary_exact(self):
        """Exactly on a part boundary (e.g. part_size * 50)."""
        lon = 50 * PART_SIZE
        result = _calculate_d108({"X": lon})
        expected = _expected_d108_sign(lon)
        assert result["X"]["sign"] == expected


# ----------------------------------------------------------------
# 6. Dispatcher integration
# ----------------------------------------------------------------

class TestDispatcher:

    def test_calculate_divisional_chart_d108(self):
        """calculate_divisional_chart(planets, 108) returns {planet: sign}."""
        planets = {"Sun": 0.0, "Moon": 90.0}
        result = calculate_divisional_chart(planets, 108)
        assert result["Sun"] == "Aries"
        assert result["Moon"] == "Cancer"

    def test_calculate_divisional_chart_detailed_d108(self):
        """Detailed API returns sign, sign_index, degree."""
        planets = {"Sun": 0.0}
        result = calculate_divisional_chart_detailed(planets, 108)
        assert "sign" in result["Sun"]
        assert "sign_index" in result["Sun"]
        assert "degree" in result["Sun"]


# ----------------------------------------------------------------
# 7. Reference check: match against independent computation
# ----------------------------------------------------------------

class TestReferenceComputation:
    """Cross-check _calculate_d108 against the test-local reference implementation
    for a spread of longitudes across all 12 signs."""

    @pytest.mark.parametrize("longitude", [
        0.0, 5.5, 15.0, 29.5,          # Aries
        30.0, 42.7, 59.9,               # Taurus
        60.0, 75.3, 89.5,               # Gemini
        90.0, 105.0, 119.9,             # Cancer
        120.0, 135.0, 149.9,            # Leo
        150.0, 165.0, 179.9,            # Virgo
        180.0, 195.0, 209.9,            # Libra
        210.0, 225.0, 239.9,            # Scorpio
        240.0, 255.0, 269.9,            # Sagittarius
        270.0, 285.0, 299.9,            # Capricorn
        300.0, 315.0, 329.9,            # Aquarius
        330.0, 345.0, 359.9,            # Pisces
    ])
    def test_matches_reference(self, longitude: float):
        result = _calculate_d108({"P": longitude})
        expected_sign = _expected_d108_sign(longitude)
        assert result["P"]["sign"] == expected_sign, (
            f"lon={longitude}: got {result['P']['sign']}, expected {expected_sign}"
        )


# ----------------------------------------------------------------
# 8. Analysis function
# ----------------------------------------------------------------

class TestD108Analysis:

    @pytest.fixture
    def sample_planets(self) -> dict:
        return {
            "Sun": 120.5,       # Leo
            "Moon": 45.3,       # Taurus
            "Mars": 275.0,      # Capricorn
            "Mercury": 165.2,   # Virgo
            "Jupiter": 330.8,   # Pisces
            "Venus": 15.0,      # Aries
            "Saturn": 210.0,    # Scorpio
            "Rahu": 60.0,       # Gemini
            "Ketu": 240.0,      # Sagittarius
        }

    def test_returns_required_keys(self, sample_planets):
        result = calculate_d108_analysis(sample_planets)
        assert "d108_positions" in result
        assert "spiritual_indicators" in result
        assert "moksha_potential" in result
        assert "past_life_karma" in result
        assert "interpretation" in result

    def test_d108_positions_structure(self, sample_planets):
        result = calculate_d108_analysis(sample_planets)
        for planet in sample_planets:
            assert planet in result["d108_positions"]
            pos = result["d108_positions"][planet]
            assert "sign" in pos
            assert "degree" in pos

    def test_moksha_potential_structure(self, sample_planets):
        result = calculate_d108_analysis(sample_planets)
        mp = result["moksha_potential"]
        assert "score" in mp
        assert "factors" in mp
        assert 0 <= mp["score"] <= 100

    def test_spiritual_indicators_list(self, sample_planets):
        result = calculate_d108_analysis(sample_planets)
        assert isinstance(result["spiritual_indicators"], list)

    def test_interpretation_is_string(self, sample_planets):
        result = calculate_d108_analysis(sample_planets)
        assert isinstance(result["interpretation"], str)
        assert len(result["interpretation"]) > 20

    def test_past_life_karma_has_rahu_ketu(self, sample_planets):
        result = calculate_d108_analysis(sample_planets)
        rahu_ketu_entries = [
            e for e in result["past_life_karma"] if e.get("axis") == "Rahu-Ketu"
        ]
        assert len(rahu_ketu_entries) == 1

    def test_exalted_planet_detected(self):
        """Sun at 0 deg Aries in D108 -> D108 sign = Aries -> Sun exalted in Aries."""
        result = calculate_d108_analysis({"Sun": 0.0})
        exalted = [
            i for i in result["spiritual_indicators"]
            if i["planet"] == "Sun" and i["condition"] == "exalted"
        ]
        assert len(exalted) == 1
        assert exalted[0]["sign"] == "Aries"

    def test_score_capped_at_100(self):
        """Even with many dignified planets, score must not exceed 100."""
        # Construct a case with many planets in exaltation/own signs in D108
        # (the actual D108 positions depend on the math, but the cap is enforced)
        planets = {
            "Sun": 0.0, "Moon": 30.0, "Mars": 270.0, "Mercury": 150.0,
            "Jupiter": 90.0, "Venus": 330.0, "Saturn": 180.0,
            "Rahu": 30.0, "Ketu": 210.0,
        }
        result = calculate_d108_analysis(planets)
        assert result["moksha_potential"]["score"] <= 100
