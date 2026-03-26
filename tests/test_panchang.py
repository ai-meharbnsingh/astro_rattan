"""Tests for app.panchang_engine -- Vedic Panchang Calculator."""
import pytest
from app.panchang_engine import (
    TITHIS,
    YOGAS,
    KARANAS,
    calculate_panchang,
    calculate_rahu_kaal,
    calculate_choghadiya,
)


class TestTithisData:
    """Validate TITHIS constant data."""

    def test_tithis_has_30_entries(self):
        assert len(TITHIS) == 30

    def test_first_tithi_is_pratipada_shukla(self):
        assert TITHIS[0]["name"] == "Pratipada"
        assert TITHIS[0]["paksha"] == "Shukla"

    def test_last_tithi_is_amavasya(self):
        assert TITHIS[29]["name"] == "Amavasya"
        assert TITHIS[29]["paksha"] == "Krishna"

    def test_purnima_is_15th(self):
        purnima = TITHIS[14]
        assert purnima["name"] == "Purnima"
        assert purnima["number"] == 15

    def test_shukla_has_15_tithis(self):
        shukla = [t for t in TITHIS if t["paksha"] == "Shukla"]
        assert len(shukla) == 15

    def test_krishna_has_15_tithis(self):
        krishna = [t for t in TITHIS if t["paksha"] == "Krishna"]
        assert len(krishna) == 15


class TestYogasData:
    def test_yogas_has_27_entries(self):
        assert len(YOGAS) == 27

    def test_first_yoga_is_vishkambha(self):
        assert YOGAS[0] == "Vishkambha"

    def test_last_yoga_is_vaidhriti(self):
        assert YOGAS[26] == "Vaidhriti"


class TestKaranasData:
    def test_karanas_has_11_entries(self):
        assert len(KARANAS) == 11

    def test_karanas_contains_bava(self):
        assert "Bava" in KARANAS

    def test_karanas_contains_vishti(self):
        assert "Vishti" in KARANAS

    def test_karanas_contains_kimstughna(self):
        assert "Kimstughna" in KARANAS


class TestCalculatePanchang:
    """Test panchang calculation."""

    def test_returns_required_keys(self):
        result = calculate_panchang(
            date="2024-01-15",
            latitude=28.6139,
            longitude=77.2090,
        )
        required_keys = {"tithi", "nakshatra", "yoga", "karana", "sunrise", "sunset"}
        assert set(result.keys()) == required_keys

    def test_tithi_has_name_and_number(self):
        result = calculate_panchang("2024-01-15", 28.6139, 77.2090)
        tithi = result["tithi"]
        assert "name" in tithi
        assert "number" in tithi
        assert "paksha" in tithi
        assert tithi["paksha"] in ("Shukla", "Krishna")

    def test_nakshatra_has_required_fields(self):
        result = calculate_panchang("2024-06-21", 13.0827, 80.2707)
        nak = result["nakshatra"]
        assert "name" in nak
        assert "pada" in nak
        assert "lord" in nak
        assert 1 <= nak["pada"] <= 4

    def test_yoga_has_name_and_number(self):
        result = calculate_panchang("2024-03-14", 19.0760, 72.8777)
        yoga = result["yoga"]
        assert "name" in yoga
        assert "number" in yoga
        assert 1 <= yoga["number"] <= 27
        assert yoga["name"] in YOGAS

    def test_sunrise_sunset_format(self):
        result = calculate_panchang("2024-09-22", 28.6139, 77.2090)
        # Format: "HH:MM"
        assert len(result["sunrise"].split(":")) == 2
        assert len(result["sunset"].split(":")) == 2

    def test_sunset_after_sunrise(self):
        result = calculate_panchang("2024-06-15", 28.6139, 77.2090)
        sr_h, sr_m = map(int, result["sunrise"].split(":"))
        ss_h, ss_m = map(int, result["sunset"].split(":"))
        sr_total = sr_h * 60 + sr_m
        ss_total = ss_h * 60 + ss_m
        assert ss_total > sr_total, "Sunset must be after sunrise"


class TestRahuKaal:
    """Test Rahu Kaal calculation."""

    def test_returns_start_and_end(self):
        result = calculate_rahu_kaal(weekday=0, sunrise="06:00", sunset="18:00")
        assert "start" in result
        assert "end" in result

    def test_rahu_kaal_monday(self):
        """Monday Rahu Kaal: slot 2 of 8 (equal day)."""
        result = calculate_rahu_kaal(weekday=0, sunrise="06:00", sunset="18:00")
        # Day duration = 12h = 720min, each slot = 90min
        # Slot 2: 06:00 + 90min = 07:30 to 09:00
        assert result["start"] == "07:30"
        assert result["end"] == "09:00"

    def test_rahu_kaal_sunday(self):
        """Sunday Rahu Kaal: slot 8 of 8."""
        result = calculate_rahu_kaal(weekday=6, sunrise="06:00", sunset="18:00")
        # Slot 8: 06:00 + 7*90min = 06:00 + 630min = 16:30 to 18:00
        assert result["start"] == "16:30"
        assert result["end"] == "18:00"

    def test_rahu_kaal_within_day(self):
        """Rahu Kaal must be between sunrise and sunset."""
        result = calculate_rahu_kaal(weekday=3, sunrise="05:45", sunset="18:30")
        sr_min = 5 * 60 + 45
        ss_min = 18 * 60 + 30
        start_parts = result["start"].split(":")
        start_min = int(start_parts[0]) * 60 + int(start_parts[1])
        end_parts = result["end"].split(":")
        end_min = int(end_parts[0]) * 60 + int(end_parts[1])
        assert start_min >= sr_min
        assert end_min <= ss_min + 1  # +1 for rounding


class TestChoghadiya:
    """Test Choghadiya calculation."""

    def test_returns_8_periods(self):
        result = calculate_choghadiya(weekday=0, sunrise="06:00", sunset="18:00")
        assert len(result) == 8

    def test_each_period_has_required_fields(self):
        result = calculate_choghadiya(weekday=2, sunrise="06:00", sunset="18:00")
        for period in result:
            assert "name" in period
            assert "quality" in period
            assert "start" in period
            assert "end" in period

    def test_periods_cover_daytime(self):
        """First period starts at sunrise, last ends at sunset."""
        result = calculate_choghadiya(weekday=4, sunrise="06:00", sunset="18:00")
        assert result[0]["start"] == "06:00"
        assert result[-1]["end"] == "18:00"

    def test_valid_quality_values(self):
        valid_qualities = {"Best", "Good", "Neutral", "Inauspicious", "Unknown"}
        result = calculate_choghadiya(weekday=5, sunrise="06:00", sunset="18:00")
        for period in result:
            assert period["quality"] in valid_qualities, f"Invalid quality: {period['quality']}"
