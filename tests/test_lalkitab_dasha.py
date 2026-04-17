"""TDD tests for LK Saala Grah Dasha engine."""
import pytest
from datetime import date
from app.lalkitab_dasha import get_saala_grah, get_dasha_timeline


class TestSaalaGrah:
    def test_age_1_is_sun(self):
        result = get_saala_grah(1)
        assert result["planet"] == "Sun"

    def test_age_9_is_mars(self):
        result = get_saala_grah(9)
        assert result["planet"] == "Mars"

    def test_age_10_cycles_back_to_sun(self):
        result = get_saala_grah(10)
        assert result["planet"] == "Sun"

    def test_age_3_is_jupiter(self):
        result = get_saala_grah(3)
        assert result["planet"] == "Jupiter"

    def test_returns_hindi_planet_name(self):
        result = get_saala_grah(1)
        hi = result["planet_hi"]
        assert hi != "Sun"
        has_devanagari = any('\u0900' <= c <= '\u097F' for c in hi)
        assert has_devanagari, f"planet_hi has no Devanagari: {hi}"

    def test_hindi_description_is_hindi(self):
        for age in [1, 5, 9]:
            result = get_saala_grah(age)
            hi_desc = result.get("hi_desc", "")
            assert hi_desc, f"age {age}: hi_desc is empty"
            has_devanagari = any('\u0900' <= c <= '\u097F' for c in hi_desc)
            assert has_devanagari, f"age {age}: hi_desc has no Devanagari: {hi_desc}"


class TestDashaTimeline:
    def test_returns_current_saala_grah(self):
        result = get_dasha_timeline("1990-01-01", "2026-04-17")
        assert "current_saala_grah" in result
        csg = result["current_saala_grah"]
        assert "planet" in csg
        assert "planet_hi" in csg
        assert "started_year" in csg
        assert "ends_year" in csg

    def test_current_age_is_correct(self):
        result = get_dasha_timeline("1990-01-01", "2026-04-17")
        assert result["current_age"] == 36

    def test_life_phase_boundaries(self):
        # Age 36 → phase 2 (past 35)
        result = get_dasha_timeline("1990-01-01", "2026-04-17")
        assert result["life_phase"]["phase"] == 2

    def test_upcoming_periods_has_5_entries(self):
        result = get_dasha_timeline("1990-01-01", "2026-04-17")
        assert len(result["upcoming_periods"]) == 5

    def test_next_saala_grah_present(self):
        result = get_dasha_timeline("1990-01-01", "2026-04-17")
        assert "next_saala_grah" in result
        assert "planet" in result["next_saala_grah"]
