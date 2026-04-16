"""
Tests for Moola (Jaimini) Dasha Engine
"""
import pytest
from datetime import datetime

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.moola_dasha_engine import (
    calculate_moola_dasha,
    MOOLA_BASE_YEARS,
    SIGNS,
    SIGN_INDEX,
    ODD_SIGNS,
    EVEN_SIGNS,
    _is_odd_sign,
    _get_dasha_sign_sequence,
    _sign_strength,
)


# Standard planet positions for testing
SAMPLE_POSITIONS = {
    "Sun": "Aries",
    "Moon": "Cancer",
    "Mars": "Leo",
    "Mercury": "Gemini",
    "Jupiter": "Sagittarius",
    "Venus": "Taurus",
    "Saturn": "Capricorn",
    "Rahu": "Virgo",
    "Ketu": "Pisces",
}


class TestConstants:
    """Verify Moola Dasha constants are correct."""

    def test_12_signs_defined(self):
        assert len(SIGNS) == 12

    def test_all_signs_have_base_years(self):
        for sign in SIGNS:
            assert sign in MOOLA_BASE_YEARS
            assert MOOLA_BASE_YEARS[sign] > 0

    def test_base_years_values(self):
        assert MOOLA_BASE_YEARS["Aries"] == 8
        assert MOOLA_BASE_YEARS["Taurus"] == 9
        assert MOOLA_BASE_YEARS["Gemini"] == 10
        assert MOOLA_BASE_YEARS["Cancer"] == 11
        assert MOOLA_BASE_YEARS["Leo"] == 12
        assert MOOLA_BASE_YEARS["Virgo"] == 1
        assert MOOLA_BASE_YEARS["Libra"] == 2
        assert MOOLA_BASE_YEARS["Scorpio"] == 3
        assert MOOLA_BASE_YEARS["Sagittarius"] == 4
        assert MOOLA_BASE_YEARS["Capricorn"] == 5
        assert MOOLA_BASE_YEARS["Aquarius"] == 6
        assert MOOLA_BASE_YEARS["Pisces"] == 7

    def test_total_base_years(self):
        total = sum(MOOLA_BASE_YEARS.values())
        assert total == 78, f"Total base years should be 78, got {total}"

    def test_odd_even_sign_coverage(self):
        assert len(ODD_SIGNS) == 6
        assert len(EVEN_SIGNS) == 6
        assert ODD_SIGNS | EVEN_SIGNS == set(SIGNS)
        assert ODD_SIGNS & EVEN_SIGNS == set()


class TestSignNature:
    """Test odd/even sign classification."""

    def test_aries_is_odd(self):
        assert _is_odd_sign("Aries") is True

    def test_taurus_is_even(self):
        assert _is_odd_sign("Taurus") is False

    def test_all_fire_signs_are_odd(self):
        for sign in ["Aries", "Leo", "Sagittarius"]:
            assert _is_odd_sign(sign) is True

    def test_all_water_signs_are_even(self):
        for sign in ["Cancer", "Scorpio", "Pisces"]:
            assert _is_odd_sign(sign) is False


class TestDashaSignSequence:
    """Test sign sequence generation."""

    def test_odd_sign_goes_forward(self):
        seq = _get_dasha_sign_sequence("Aries")
        assert seq[0] == "Aries"
        assert seq[1] == "Taurus"
        assert seq[11] == "Pisces"

    def test_even_sign_goes_reverse(self):
        seq = _get_dasha_sign_sequence("Taurus")
        assert seq[0] == "Taurus"
        assert seq[1] == "Aries"
        assert seq[2] == "Pisces"

    def test_sequence_has_12_signs(self):
        seq = _get_dasha_sign_sequence("Leo")
        assert len(seq) == 12

    def test_sequence_contains_all_signs(self):
        seq = _get_dasha_sign_sequence("Scorpio")
        assert set(seq) == set(SIGNS)

    def test_gemini_forward(self):
        seq = _get_dasha_sign_sequence("Gemini")
        assert seq[0] == "Gemini"
        assert seq[1] == "Cancer"

    def test_cancer_reverse(self):
        seq = _get_dasha_sign_sequence("Cancer")
        assert seq[0] == "Cancer"
        assert seq[1] == "Gemini"


class TestSignStrength:
    """Test sign strength calculation."""

    def test_sign_with_planets_is_stronger(self):
        positions = {"Sun": "Aries", "Mars": "Aries", "Moon": "Libra"}
        aries_str = _sign_strength("Aries", positions)
        libra_str = _sign_strength("Libra", positions)
        assert aries_str > libra_str

    def test_sign_with_own_lord_gets_bonus(self):
        # Mars is lord of Aries; Mars placed in Aries
        positions_with_lord = {"Mars": "Aries"}
        positions_without_lord = {"Mars": "Taurus"}
        str_with = _sign_strength("Aries", positions_with_lord)
        str_without = _sign_strength("Aries", positions_without_lord)
        assert str_with > str_without

    def test_empty_positions_gives_zero(self):
        strength = _sign_strength("Leo", {})
        assert strength == 0


class TestCalculateMoolaDasha:
    """Test the main calculation function."""

    def test_basic_calculation_returns_periods(self):
        result = calculate_moola_dasha("Aries", "Libra", SAMPLE_POSITIONS, "1990-01-15")
        assert len(result["mahadasha"]) > 0

    def test_starting_sign_is_reported(self):
        result = calculate_moola_dasha("Aries", "Libra", SAMPLE_POSITIONS, "1990-01-15")
        assert result["starting_sign"] in SIGNS

    def test_direction_is_reported(self):
        result = calculate_moola_dasha("Aries", "Libra", SAMPLE_POSITIONS, "1990-01-15")
        assert result["direction"] in ("forward", "reverse")

    def test_odd_starting_sign_gives_forward_direction(self):
        # Force Aries (odd) to be stronger by placing planets there
        positions = {"Sun": "Aries", "Mars": "Aries", "Moon": "Aries"}
        result = calculate_moola_dasha("Aries", "Libra", positions, "1990-01-15")
        assert result["starting_sign"] == "Aries"
        assert result["direction"] == "forward"

    def test_even_starting_sign_gives_reverse_direction(self):
        # Force Cancer (even) to be stronger
        positions = {"Sun": "Cancer", "Moon": "Cancer", "Mars": "Cancer", "Jupiter": "Cancer"}
        result = calculate_moola_dasha("Capricorn", "Cancer", positions, "1990-01-15")
        assert result["starting_sign"] == "Cancer"
        assert result["direction"] == "reverse"

    def test_first_period_starts_on_birth_date(self):
        result = calculate_moola_dasha("Leo", "Aquarius", SAMPLE_POSITIONS, "1992-03-10")
        assert result["mahadasha"][0]["start"] == "1992-03-10"

    def test_periods_are_contiguous(self):
        result = calculate_moola_dasha("Aries", "Libra", SAMPLE_POSITIONS, "1990-01-15")
        periods = result["mahadasha"]
        for i in range(len(periods) - 1):
            assert periods[i]["end"] == periods[i + 1]["start"], (
                f"Gap between period {i} and {i+1}"
            )

    def test_24_periods_for_2_cycles(self):
        result = calculate_moola_dasha("Aries", "Libra", SAMPLE_POSITIONS, "1990-01-15")
        assert len(result["mahadasha"]) == 24  # 12 signs x 2 cycles

    def test_sub_periods_present(self):
        result = calculate_moola_dasha("Aries", "Libra", SAMPLE_POSITIONS, "1990-01-15")
        for period in result["mahadasha"]:
            assert "sub_periods" in period
            assert len(period["sub_periods"]) == 12

    def test_sub_periods_are_contiguous(self):
        result = calculate_moola_dasha("Leo", "Aquarius", SAMPLE_POSITIONS, "1990-01-15")
        for md in result["mahadasha"][:3]:
            sps = md["sub_periods"]
            for i in range(len(sps) - 1):
                assert sps[i]["end"] == sps[i + 1]["start"]

    def test_current_dasha_identified(self):
        result = calculate_moola_dasha("Aries", "Libra", SAMPLE_POSITIONS, "1990-01-15")
        assert result["current_dasha"] != "Unknown"
        assert result["current_dasha"] in SIGNS

    def test_current_sub_period_identified(self):
        result = calculate_moola_dasha("Aries", "Libra", SAMPLE_POSITIONS, "1990-01-15")
        assert result["current_sub_period"] != "Unknown"
        assert result["current_sub_period"] in SIGNS

    def test_unknown_lagna_returns_error(self):
        result = calculate_moola_dasha("FakeSign", "Libra", SAMPLE_POSITIONS, "1990-01-15")
        assert "error" in result
        assert result["current_dasha"] == "Unknown"

    def test_unknown_seventh_returns_error(self):
        result = calculate_moola_dasha("Aries", "FakeSign", SAMPLE_POSITIONS, "1990-01-15")
        assert "error" in result

    def test_period_years_match_base_years(self):
        """Each period should use the correct base years for its sign."""
        result = calculate_moola_dasha("Aries", "Libra", SAMPLE_POSITIONS, "1990-01-15")
        for period in result["mahadasha"]:
            sign = period["sign"]
            assert period["years"] == MOOLA_BASE_YEARS[sign], (
                f"{sign} should have {MOOLA_BASE_YEARS[sign]} years, got {period['years']}"
            )

    def test_multiple_lagna_signs(self):
        """Test with various lagna signs to ensure robustness."""
        for sign in ["Aries", "Taurus", "Cancer", "Leo", "Scorpio", "Pisces"]:
            opp_idx = (SIGN_INDEX[sign] + 6) % 12
            seventh = SIGNS[opp_idx]
            result = calculate_moola_dasha(sign, seventh, SAMPLE_POSITIONS, "1985-07-04")
            assert len(result["mahadasha"]) == 24, f"Failed for lagna={sign}"
            assert result["current_dasha"] in SIGNS, f"Bad current dasha for lagna={sign}"
