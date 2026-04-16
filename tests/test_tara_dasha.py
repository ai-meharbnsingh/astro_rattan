"""
Tests for Tara Dasha Engine
"""
import pytest
from datetime import datetime

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.tara_dasha_engine import (
    calculate_tara_dasha,
    TARA_GROUPS,
    TARA_TOTAL,
    NAKSHATRA_ORDER,
    NAKSHATRA_INDEX,
    _build_tara_nakshatras,
    _calculate_balance,
)


class TestConstants:
    """Verify Tara Dasha constants are correct."""

    def test_total_years_equals_120(self):
        total = sum(g["years"] for g in TARA_GROUPS)
        assert total == 120, f"Tara total should be 120, got {total}"

    def test_9_tara_groups(self):
        assert len(TARA_GROUPS) == 9

    def test_27_nakshatras(self):
        assert len(NAKSHATRA_ORDER) == 27

    def test_tara_group_names(self):
        expected_names = [
            "Janma", "Sampat", "Vipat", "Kshema", "Pratyari",
            "Sadhaka", "Vadha", "Mitra", "Ati-Mitra",
        ]
        actual_names = [g["name"] for g in TARA_GROUPS]
        assert actual_names == expected_names

    def test_tara_group_years(self):
        expected_years = [7, 20, 6, 10, 7, 18, 16, 19, 17]
        actual_years = [g["years"] for g in TARA_GROUPS]
        assert actual_years == expected_years

    def test_tara_group_lords(self):
        expected_lords = [
            "Ketu", "Venus", "Sun", "Moon", "Mars",
            "Rahu", "Jupiter", "Saturn", "Mercury",
        ]
        actual_lords = [g["lord"] for g in TARA_GROUPS]
        assert actual_lords == expected_lords


class TestBuildTaraNakshatras:
    """Test Tara group construction from birth nakshatra."""

    def test_ashwini_groups(self):
        groups = _build_tara_nakshatras("Ashwini")
        # Group 1 (Janma): Ashwini, Bharani, Krittika
        assert groups[0]["nakshatras"] == ["Ashwini", "Bharani", "Krittika"]
        assert groups[0]["name"] == "Janma"

    def test_ashwini_second_group(self):
        groups = _build_tara_nakshatras("Ashwini")
        # Group 2 (Sampat): Rohini, Mrigashira, Ardra
        assert groups[1]["nakshatras"] == ["Rohini", "Mrigashira", "Ardra"]
        assert groups[1]["name"] == "Sampat"

    def test_9_groups_cover_27_nakshatras(self):
        groups = _build_tara_nakshatras("Ashwini")
        all_naks = []
        for g in groups:
            assert len(g["nakshatras"]) == 3
            all_naks.extend(g["nakshatras"])
        assert len(all_naks) == 27
        assert set(all_naks) == set(NAKSHATRA_ORDER)

    def test_wrapping_from_late_nakshatra(self):
        """Starting from Revati (last nakshatra), groups should wrap around."""
        groups = _build_tara_nakshatras("Revati")
        # Group 1 (Janma): Revati, Ashwini, Bharani
        assert groups[0]["nakshatras"] == ["Revati", "Ashwini", "Bharani"]

    def test_each_group_has_correct_metadata(self):
        groups = _build_tara_nakshatras("Magha")
        for i, group in enumerate(groups):
            assert group["name"] == TARA_GROUPS[i]["name"]
            assert group["lord"] == TARA_GROUPS[i]["lord"]
            assert group["years"] == TARA_GROUPS[i]["years"]

    def test_pushya_groups(self):
        groups = _build_tara_nakshatras("Pushya")
        # Pushya is index 7. Group 1: Pushya(7), Ashlesha(8), Magha(9)
        assert groups[0]["nakshatras"] == ["Pushya", "Ashlesha", "Magha"]
        # Group 2: PPhalguni(10), UPhalguni(11), Hasta(12)
        assert groups[1]["nakshatras"] == [
            "Purva Phalguni", "Uttara Phalguni", "Hasta"
        ]


class TestBalance:
    """Test balance calculation."""

    def test_no_longitude_returns_full(self):
        balance = _calculate_balance("Ashwini", None)
        assert balance == 1.0

    def test_unknown_nakshatra_returns_full(self):
        balance = _calculate_balance("FakeNakshatra", 10.0)
        assert balance == 1.0

    def test_balance_between_0_and_1(self):
        balance = _calculate_balance("Ashwini", 5.0)
        assert 0.0 <= balance <= 1.0

    def test_balance_near_start_is_high(self):
        # Ashwini starts at 0 degrees
        balance = _calculate_balance("Ashwini", 0.5)
        assert balance > 0.9

    def test_balance_near_end_is_low(self):
        # Ashwini spans 0 to ~13.333 degrees
        balance = _calculate_balance("Ashwini", 13.0)
        assert balance < 0.1


class TestCalculateTaraDasha:
    """Test the main calculation function."""

    def test_basic_calculation_returns_periods(self):
        result = calculate_tara_dasha("Ashwini", "1990-01-15")
        assert len(result["mahadasha"]) > 0

    def test_9_periods_per_cycle(self):
        result = calculate_tara_dasha("Rohini", "1990-01-15")
        # 2 cycles = 18 periods
        assert len(result["mahadasha"]) == 18

    def test_tara_groups_returned(self):
        result = calculate_tara_dasha("Hasta", "1990-01-15")
        assert len(result["tara_groups"]) == 9

    def test_first_period_is_janma(self):
        result = calculate_tara_dasha("Magha", "1990-01-15")
        assert result["mahadasha"][0]["tara"] == "Janma"

    def test_first_period_starts_on_birth_date(self):
        result = calculate_tara_dasha("Swati", "1992-03-10")
        assert result["mahadasha"][0]["start"] == "1992-03-10"

    def test_periods_are_contiguous(self):
        result = calculate_tara_dasha("Chitra", "1990-01-15")
        periods = result["mahadasha"]
        for i in range(len(periods) - 1):
            assert periods[i]["end"] == periods[i + 1]["start"], (
                f"Gap between period {i} and {i+1}"
            )

    def test_total_years_approximately_120_for_full_cycle(self):
        """With no balance offset, first 9 periods should total ~120 years."""
        result = calculate_tara_dasha("Ashwini", "1900-01-01")
        first_cycle_years = sum(p["years"] for p in result["mahadasha"][:9])
        assert abs(first_cycle_years - 120) < 0.1, (
            f"First cycle total should be ~120, got {first_cycle_years}"
        )

    def test_balance_reduces_first_period(self):
        full = calculate_tara_dasha("Ashwini", "1990-01-15", moon_longitude=None)
        partial = calculate_tara_dasha("Ashwini", "1990-01-15", moon_longitude=5.0)
        assert partial["mahadasha"][0]["years"] <= full["mahadasha"][0]["years"]

    def test_nakshatras_included_in_periods(self):
        result = calculate_tara_dasha("Bharani", "1990-01-15")
        for period in result["mahadasha"]:
            assert "nakshatras" in period
            assert len(period["nakshatras"]) == 3

    def test_sub_periods_present(self):
        result = calculate_tara_dasha("Ardra", "1990-01-15")
        for period in result["mahadasha"]:
            assert "sub_periods" in period
            assert len(period["sub_periods"]) == 9

    def test_sub_periods_are_contiguous(self):
        result = calculate_tara_dasha("Punarvasu", "1990-01-15")
        for md in result["mahadasha"][:3]:
            sps = md["sub_periods"]
            for i in range(len(sps) - 1):
                assert sps[i]["end"] == sps[i + 1]["start"]

    def test_current_dasha_identified(self):
        result = calculate_tara_dasha("Mrigashira", "1990-01-15")
        tara_names = [g["name"] for g in TARA_GROUPS]
        assert result["current_dasha"] != "Unknown"
        assert result["current_dasha"] in tara_names

    def test_current_sub_period_identified(self):
        result = calculate_tara_dasha("Krittika", "1990-01-15")
        tara_names = [g["name"] for g in TARA_GROUPS]
        assert result["current_sub_period"] != "Unknown"
        assert result["current_sub_period"] in tara_names

    def test_unknown_nakshatra_returns_error(self):
        result = calculate_tara_dasha("FakeNakshatra", "1990-01-15")
        assert "error" in result
        assert result["current_dasha"] == "Unknown"

    def test_lord_field_in_periods(self):
        result = calculate_tara_dasha("Ashwini", "1990-01-15")
        expected_lords = ["Ketu", "Venus", "Sun", "Moon", "Mars",
                         "Rahu", "Jupiter", "Saturn", "Mercury"]
        for i, period in enumerate(result["mahadasha"][:9]):
            assert period["lord"] == expected_lords[i], (
                f"Period {i} lord should be {expected_lords[i]}, got {period['lord']}"
            )

    def test_multiple_nakshatras_produce_valid_results(self):
        """Test various nakshatras for robustness."""
        test_nakshatras = [
            "Ashwini", "Rohini", "Ardra", "Magha", "Hasta",
            "Vishakha", "Mula", "Shravana", "Revati",
        ]
        tara_names = [g["name"] for g in TARA_GROUPS]
        for nak in test_nakshatras:
            result = calculate_tara_dasha(nak, "1985-07-04")
            assert len(result["mahadasha"]) == 18, f"Wrong period count for {nak}"
            assert result["current_dasha"] in tara_names, f"Bad current for {nak}"

    def test_revati_wrapping_groups(self):
        """Revati (last nakshatra) should wrap groups correctly."""
        result = calculate_tara_dasha("Revati", "1990-01-15")
        first_group_naks = result["mahadasha"][0]["nakshatras"]
        assert first_group_naks[0] == "Revati"
        assert first_group_naks[1] == "Ashwini"  # wraps to beginning
        assert first_group_naks[2] == "Bharani"
