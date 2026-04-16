"""
Tests for app.panchang_misc -- Miscellaneous Panchang Calculations
==================================================================
Covers Mantri Mandala, Kaliyuga/astronomical data, Panchaka Rahita.
"""
import pytest

from app.panchang_misc import (
    calculate_mantri_mandala,
    calculate_astronomical_data,
    calculate_panchaka_rahita,
    calculate_all_misc,
    MANDALA_ROLES,
    GRAHA_ORDER,
    PLANET_NAMES,
    PANCHAKA_NAKSHATRAS,
    _resolve_nakshatra,
    _time_to_minutes,
    _minutes_to_time,
)


# ============================================================
# Mantri Mandala
# ============================================================

class TestMantriMandala:
    def test_returns_ten_roles(self):
        result = calculate_mantri_mandala(2082)
        assert len(result) == 10

    def test_each_entry_has_all_keys(self):
        result = calculate_mantri_mandala(2083)
        for entry in result:
            assert "role" in entry
            assert "role_hindi" in entry
            assert "planet" in entry
            assert "planet_hindi" in entry

    def test_hindi_labels_present(self):
        result = calculate_mantri_mandala(2082)
        for entry in result:
            assert entry["role_hindi"] != ""
            assert entry["planet_hindi"] != ""
            # Hindi strings should contain Devanagari characters
            assert any("\u0900" <= ch <= "\u097f" for ch in entry["role_hindi"])
            assert any("\u0900" <= ch <= "\u097f" for ch in entry["planet_hindi"])

    def test_raja_is_first_role(self):
        result = calculate_mantri_mandala(2082)
        assert result[0]["role"] == "Raja"
        assert result[0]["role_hindi"] == "राजा"

    def test_known_samvat_2082_raja_is_saturn(self):
        result = calculate_mantri_mandala(2082)
        assert result[0]["planet"] == "Saturn"
        assert result[0]["planet_hindi"] == "शनि"

    def test_known_samvat_2083_raja_is_sun(self):
        result = calculate_mantri_mandala(2083)
        assert result[0]["planet"] == "Sun"
        assert result[0]["planet_hindi"] == "सूर्य"

    def test_known_samvat_2084_raja_is_moon(self):
        result = calculate_mantri_mandala(2084)
        assert result[0]["planet"] == "Moon"
        assert result[0]["planet_hindi"] == "चन्द्र"

    def test_unknown_samvat_uses_fallback(self):
        """Year not in SAMVAT_RAJA should still return 10 roles."""
        result = calculate_mantri_mandala(9999)
        assert len(result) == 10
        assert result[0]["role"] == "Raja"

    def test_all_roles_match_definition(self):
        result = calculate_mantri_mandala(2082)
        for entry, (role_en, role_hi) in zip(result, MANDALA_ROLES):
            assert entry["role"] == role_en
            assert entry["role_hindi"] == role_hi

    def test_planets_cycle_from_raja(self):
        """Planets should follow GRAHA_ORDER starting from the Raja planet."""
        result = calculate_mantri_mandala(2083)  # Raja = Sun (index 0)
        for i, entry in enumerate(result):
            expected_planet = GRAHA_ORDER[(0 + i) % 7]
            assert entry["planet"] == expected_planet


# ============================================================
# Kaliyuga & Astronomical Data
# ============================================================

class TestAstronomicalData:
    def test_kaliyuga_year_for_2026(self):
        result = calculate_astronomical_data("2026-04-17")
        assert result["kaliyuga_year"] == 5127

    def test_kaliyuga_year_for_2025(self):
        result = calculate_astronomical_data("2025-01-15")
        assert result["kaliyuga_year"] == 5126

    def test_all_expected_keys_present(self):
        result = calculate_astronomical_data("2026-04-17", jd=2461413.5, ayanamsha=24.2)
        expected_keys = [
            "kaliyuga_year",
            "kaliyuga_year_label",
            "kaliyuga_year_label_hindi",
            "kali_ahargana",
            "kali_ahargana_label",
            "kali_ahargana_label_hindi",
            "rata_die",
            "rata_die_label",
            "rata_die_label_hindi",
            "julian_day",
            "julian_day_label",
            "julian_day_label_hindi",
            "modified_julian_day",
            "modified_julian_day_label",
            "modified_julian_day_label_hindi",
            "ayanamsha",
            "ayanamsha_label",
            "ayanamsha_label_hindi",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_hindi_labels_for_kaliyuga(self):
        result = calculate_astronomical_data("2026-04-17")
        assert "वर्ष" in result["kaliyuga_year_label_hindi"]

    def test_kali_ahargana_with_jd(self):
        jd = 2461413.5
        result = calculate_astronomical_data("2026-04-17", jd=jd)
        expected = int(jd - 588465.5)
        assert result["kali_ahargana"] == expected

    def test_rata_die_with_jd(self):
        jd = 2461413.5
        result = calculate_astronomical_data("2026-04-17", jd=jd)
        expected = int(jd - 1721424.5)
        assert result["rata_die"] == expected

    def test_modified_julian_day_with_jd(self):
        jd = 2461413.5
        result = calculate_astronomical_data("2026-04-17", jd=jd)
        expected = int(jd - 2400000.5)
        assert result["modified_julian_day"] == expected

    def test_ayanamsha_label_contains_lahiri(self):
        result = calculate_astronomical_data("2026-04-17", ayanamsha=24.200123)
        assert "Lahiri" in result["ayanamsha_label"]
        assert "लाहिरी" in result["ayanamsha_label_hindi"]

    def test_zero_values_when_no_jd(self):
        result = calculate_astronomical_data("2026-04-17")
        assert result["kali_ahargana"] == 0
        assert result["rata_die"] == 0
        assert result["modified_julian_day"] == 0
        assert result["julian_day"] == 0

    def test_zero_ayanamsha_when_none(self):
        result = calculate_astronomical_data("2026-04-17")
        assert result["ayanamsha"] == 0
        assert result["ayanamsha_label"] == ""


# ============================================================
# Panchaka Rahita Muhurta
# ============================================================

class TestPanchakaRahita:
    def test_non_panchaka_nakshatra_returns_none(self):
        result = calculate_panchaka_rahita("Rohini", "14:30", "06:10", "18:30")
        assert result is None

    def test_ashwini_returns_none(self):
        result = calculate_panchaka_rahita("Ashwini", "12:00", "06:00", "18:00")
        assert result is None

    def test_dhanishta_triggers_panchaka(self):
        result = calculate_panchaka_rahita("Dhanishta", "14:30", "06:10", "18:30")
        assert result is not None
        assert result["active"] is True
        assert result["type"] == "Mrityu Panchaka"
        assert result["type_hindi"] == "मृत्यु पंचक"

    def test_shatabhisha_triggers_agni_panchaka(self):
        result = calculate_panchaka_rahita("Shatabhisha", "15:00", "06:00", "18:00")
        assert result is not None
        assert result["type"] == "Agni Panchaka"

    def test_purva_bhadrapada_is_safe_for_govt(self):
        result = calculate_panchaka_rahita("Purva Bhadrapada", "14:00", "06:00", "18:00")
        assert result is not None
        assert result["safe_for_govt"] is True

    def test_other_panchaka_not_safe_for_govt(self):
        result = calculate_panchaka_rahita("Dhanishta", "14:00", "06:00", "18:00")
        assert result is not None
        assert result["safe_for_govt"] is False

    def test_unsafe_window_present(self):
        result = calculate_panchaka_rahita("Revati", "14:00", "06:00", "18:00")
        assert result is not None
        assert "unsafe_window" in result
        assert result["unsafe_window"]["start"] == "06:00"
        assert result["unsafe_window"]["end"] == "14:00"

    def test_safe_window_when_nakshatra_ends_before_sunset(self):
        result = calculate_panchaka_rahita("Dhanishta", "14:00", "06:00", "18:00")
        assert result is not None
        assert result["safe_window"] is not None
        assert result["safe_window"]["start"] == "14:00"
        assert result["safe_window"]["end"] == "18:00"

    def test_no_safe_window_when_nakshatra_extends_past_sunset(self):
        result = calculate_panchaka_rahita("Dhanishta", "19:00", "06:00", "18:00")
        assert result is not None
        assert result["safe_window"] is None
        assert "कोई शुभ समय नहीं" in result["safe_window_label_hindi"]

    def test_nakshatra_ending_before_sunrise_returns_none(self):
        result = calculate_panchaka_rahita("Dhanishta", "05:00", "06:00", "18:00")
        assert result is None

    def test_hindi_labels_in_result(self):
        result = calculate_panchaka_rahita("Uttara Bhadrapada", "15:00", "06:00", "18:30")
        assert result is not None
        assert "अशुभ" in result["unsafe_window_label_hindi"]
        assert "शुभ" in result["safe_window_label_hindi"]

    def test_alias_spelling_dhanista(self):
        result = calculate_panchaka_rahita("Dhanista", "14:00", "06:00", "18:00")
        assert result is not None
        assert result["type"] == "Mrityu Panchaka"


# ============================================================
# Helper functions
# ============================================================

class TestHelpers:
    def test_resolve_nakshatra_known_alias(self):
        assert _resolve_nakshatra("Dhanista") == "Dhanishta"
        assert _resolve_nakshatra("Satabhisha") == "Shatabhisha"
        assert _resolve_nakshatra("Poorva Bhadrapada") == "Purva Bhadrapada"

    def test_resolve_nakshatra_passthrough(self):
        assert _resolve_nakshatra("Rohini") == "Rohini"
        assert _resolve_nakshatra("Ashwini") == "Ashwini"

    def test_time_to_minutes(self):
        assert _time_to_minutes("00:00") == 0
        assert _time_to_minutes("06:30") == 390
        assert _time_to_minutes("18:00") == 1080

    def test_minutes_to_time(self):
        assert _minutes_to_time(0) == "00:00"
        assert _minutes_to_time(390) == "06:30"
        assert _minutes_to_time(1080) == "18:00"


# ============================================================
# Master function — calculate_all_misc
# ============================================================

class TestCalculateAllMisc:
    def test_returns_all_three_keys(self):
        result = calculate_all_misc("2026-04-17", vikram_samvat=2083)
        assert "mantri_mandala" in result
        assert "astronomical" in result
        assert "panchaka_rahita" in result

    def test_mantri_mandala_has_ten_entries(self):
        result = calculate_all_misc("2026-04-17", vikram_samvat=2083)
        assert len(result["mantri_mandala"]) == 10

    def test_panchaka_none_without_nakshatra(self):
        result = calculate_all_misc("2026-04-17", vikram_samvat=2083)
        assert result["panchaka_rahita"] is None

    def test_panchaka_active_when_dhanishta(self):
        result = calculate_all_misc(
            "2026-04-17",
            vikram_samvat=2083,
            nakshatra_name="Dhanishta",
            nakshatra_end_time="14:00",
            sunrise="06:00",
            sunset="18:00",
        )
        assert result["panchaka_rahita"] is not None
        assert result["panchaka_rahita"]["active"] is True

    def test_astronomical_kaliyuga(self):
        result = calculate_all_misc("2026-04-17", vikram_samvat=2083)
        assert result["astronomical"]["kaliyuga_year"] == 5127

    def test_astronomical_with_jd(self):
        result = calculate_all_misc(
            "2026-04-17",
            vikram_samvat=2083,
            jd=2461413.5,
            ayanamsha=24.2,
        )
        assert result["astronomical"]["kali_ahargana"] > 0
        assert result["astronomical"]["ayanamsha"] > 0
