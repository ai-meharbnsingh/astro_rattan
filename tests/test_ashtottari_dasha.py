"""
Tests for Ashtottari Dasha Engine
"""
import pytest
from datetime import datetime

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.ashtottari_dasha_engine import (
    calculate_ashtottari_dasha,
    ASHTOTTARI_YEARS,
    ASHTOTTARI_ORDER,
    ASHTOTTARI_NAKSHATRA_LORD,
    ASHTOTTARI_TOTAL,
    _get_dasha_sequence,
    _calculate_balance,
)


class TestConstants:
    """Verify Ashtottari constants are correct."""

    def test_total_years_equals_108(self):
        total = sum(ASHTOTTARI_YEARS.values())
        assert total == 108, f"Ashtottari total should be 108, got {total}"

    def test_order_has_8_planets(self):
        assert len(ASHTOTTARI_ORDER) == 8

    def test_no_ketu_in_system(self):
        assert "Ketu" not in ASHTOTTARI_ORDER
        assert "Ketu" not in ASHTOTTARI_YEARS

    def test_all_planets_have_years(self):
        for planet in ASHTOTTARI_ORDER:
            assert planet in ASHTOTTARI_YEARS
            assert ASHTOTTARI_YEARS[planet] > 0

    def test_22_nakshatras_in_scheme(self):
        assert len(ASHTOTTARI_NAKSHATRA_LORD) == 22

    def test_individual_planet_years(self):
        assert ASHTOTTARI_YEARS["Sun"] == 6
        assert ASHTOTTARI_YEARS["Moon"] == 15
        assert ASHTOTTARI_YEARS["Mars"] == 8
        assert ASHTOTTARI_YEARS["Mercury"] == 17
        assert ASHTOTTARI_YEARS["Saturn"] == 10
        assert ASHTOTTARI_YEARS["Jupiter"] == 19
        assert ASHTOTTARI_YEARS["Rahu"] == 12
        assert ASHTOTTARI_YEARS["Venus"] == 21


class TestDashaSequence:
    """Test cyclic sequence generation."""

    def test_sequence_starts_from_given_planet(self):
        seq = _get_dasha_sequence("Mars")
        assert seq[0] == "Mars"

    def test_sequence_has_8_planets(self):
        seq = _get_dasha_sequence("Sun")
        assert len(seq) == 8

    def test_sequence_wraps_around(self):
        seq = _get_dasha_sequence("Venus")
        assert seq[0] == "Venus"
        assert seq[1] == "Sun"  # wraps to beginning

    def test_all_planets_present_in_sequence(self):
        seq = _get_dasha_sequence("Mercury")
        assert set(seq) == set(ASHTOTTARI_ORDER)


class TestBalance:
    """Test balance calculation."""

    def test_no_longitude_returns_full_balance(self):
        balance = _calculate_balance("Ardra", None)
        assert balance == 1.0

    def test_non_ashtottari_nakshatra_returns_full_balance(self):
        # Ashwini is NOT in the Ashtottari scheme
        balance = _calculate_balance("Ashwini", 5.0)
        assert balance == 1.0

    def test_balance_between_0_and_1(self):
        # Ardra starts at nakshatra index 5, so longitude ~66.67
        balance = _calculate_balance("Ardra", 70.0)
        assert 0.0 <= balance <= 1.0

    def test_balance_at_start_of_group_is_near_1(self):
        # Ardra is the first nakshatra in Sun's group
        # Ardra starts at index 5 * 13.333 = 66.667 degrees
        balance = _calculate_balance("Ardra", 66.7)
        assert balance > 0.9

    def test_balance_clamped_to_valid_range(self):
        balance = _calculate_balance("Pushya", 500.0)
        assert 0.0 <= balance <= 1.0


class TestCalculateAshtottariDasha:
    """Test the main calculation function."""

    def test_non_applicable_nakshatra_returns_not_applicable(self):
        result = calculate_ashtottari_dasha("Ashwini", "1990-01-15")
        assert result["applicable"] is False
        assert len(result["mahadasha"]) == 0
        assert "error" in result

    def test_applicable_nakshatra_returns_periods(self):
        result = calculate_ashtottari_dasha("Ardra", "1990-01-15")
        assert result["applicable"] is True
        assert len(result["mahadasha"]) > 0

    def test_ardra_starts_with_sun(self):
        """Ardra is ruled by Sun in Ashtottari. First dasha should be Sun."""
        result = calculate_ashtottari_dasha("Ardra", "1990-01-15")
        assert result["mahadasha"][0]["planet"] == "Sun"

    def test_shatabhisha_starts_with_rahu(self):
        """Shatabhisha is ruled by Rahu in Ashtottari."""
        result = calculate_ashtottari_dasha("Shatabhisha", "1990-01-15")
        assert result["mahadasha"][0]["planet"] == "Rahu"

    def test_revati_starts_with_venus(self):
        """Revati is ruled by Venus in Ashtottari."""
        result = calculate_ashtottari_dasha("Revati", "1985-06-20")
        assert result["mahadasha"][0]["planet"] == "Venus"

    def test_first_period_starts_on_birth_date(self):
        result = calculate_ashtottari_dasha("Magha", "1992-03-10")
        assert result["mahadasha"][0]["start"] == "1992-03-10"

    def test_periods_are_contiguous(self):
        """Each period's end should be the next period's start."""
        result = calculate_ashtottari_dasha("Hasta", "1990-01-15")
        periods = result["mahadasha"]
        for i in range(len(periods) - 1):
            assert periods[i]["end"] == periods[i + 1]["start"], (
                f"Gap between period {i} end ({periods[i]['end']}) "
                f"and period {i+1} start ({periods[i+1]['start']})"
            )

    def test_first_cycle_has_8_periods(self):
        """First 8 periods should cover the first cycle."""
        result = calculate_ashtottari_dasha("Swati", "1990-01-15")
        # At least 8 periods should exist
        assert len(result["mahadasha"]) >= 8

    def test_total_years_approximately_108_for_full_cycle(self):
        """With no balance offset (moon_longitude=None), first 8 periods ~ 108 years."""
        result = calculate_ashtottari_dasha("Ardra", "1900-01-01")
        first_cycle_years = sum(p["years"] for p in result["mahadasha"][:8])
        assert abs(first_cycle_years - 108) < 0.1, (
            f"First cycle total should be ~108, got {first_cycle_years}"
        )

    def test_balance_reduces_first_period(self):
        """When moon_longitude is provided, first period should be shorter."""
        full = calculate_ashtottari_dasha("Ardra", "1990-01-15", moon_longitude=None)
        partial = calculate_ashtottari_dasha("Ardra", "1990-01-15", moon_longitude=72.0)
        assert partial["mahadasha"][0]["years"] <= full["mahadasha"][0]["years"]

    def test_antardasha_present_in_periods(self):
        result = calculate_ashtottari_dasha("Vishakha", "1990-01-15")
        for period in result["mahadasha"]:
            assert "antardasha" in period
            assert len(period["antardasha"]) == 8  # 8 planets, no Ketu

    def test_antardasha_periods_are_contiguous(self):
        result = calculate_ashtottari_dasha("Anuradha", "1990-01-15")
        for md in result["mahadasha"][:3]:
            ads = md["antardasha"]
            for i in range(len(ads) - 1):
                assert ads[i]["end"] == ads[i + 1]["start"]

    def test_current_dasha_is_identified(self):
        result = calculate_ashtottari_dasha("Pushya", "1990-01-15")
        # For someone born in 1990, current dasha should not be Unknown
        assert result["current_dasha"] != "Unknown"
        assert result["current_dasha"] in ASHTOTTARI_ORDER

    def test_current_antardasha_is_identified(self):
        result = calculate_ashtottari_dasha("Jyeshtha", "1990-01-15")
        assert result["current_antardasha"] != "Unknown"
        assert result["current_antardasha"] in ASHTOTTARI_ORDER

    def test_pratyantardasha_present_for_current(self):
        """Current antardasha should have pratyantardasha periods."""
        result = calculate_ashtottari_dasha("Mula", "1990-01-15")
        found_pratyantar = False
        for md in result["mahadasha"]:
            if md["is_current"]:
                for ad in md["antardasha"]:
                    if ad["is_current"]:
                        assert len(ad["pratyantar"]) == 8
                        found_pratyantar = True
                        break
                break
        assert found_pratyantar, "Should have pratyantardasha for current period"

    def test_unknown_nakshatra_returns_error(self):
        result = calculate_ashtottari_dasha("FakeNakshatra", "1990-01-15")
        assert result["applicable"] is False
        assert "error" in result

    def test_multiple_nakshatras_produce_valid_results(self):
        """Test a spread of nakshatras to ensure robustness."""
        test_nakshatras = [
            "Ardra", "Pushya", "Magha", "Hasta", "Swati",
            "Jyeshtha", "Uttara Ashadha", "Shatabhisha", "Revati",
        ]
        for nak in test_nakshatras:
            result = calculate_ashtottari_dasha(nak, "1985-07-04")
            assert result["applicable"] is True, f"Failed for {nak}"
            assert len(result["mahadasha"]) >= 8, f"Too few periods for {nak}"
            assert result["current_dasha"] in ASHTOTTARI_ORDER, f"Bad current dasha for {nak}"
