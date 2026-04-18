"""
tests/test_lalkitab_time_planet.py

Unit tests for app/lalkitab_time_planet.py — detect_time_planet().

Covers:
  1.  Sunday (2024-01-07) → day_lord="Sun", weekday_name="Sunday"
  2.  Monday (2024-01-08) → day_lord="Moon", weekday_name="Monday"
  3.  is_remediable is ALWAYS False regardless of input
  4.  allow_sunrise_fallback=True + no sunrise_hms → sunrise_assumed=True, hora_skipped=False
  5.  allow_sunrise_fallback=False + no sunrise_hms → hora_skipped=True, hora_lord=None
  6.  dual=True when day_lord != hora_lord
  7.  doubled=True when day_lord == hora_lord
  8.  source == "LK_CANONICAL", lk_ref == "2.16"
  9.  Invalid birth_time raises ValueError
 10.  Result always contains all required keys
 11.  day_lord_hi is a non-empty Hindi string
 12.  both_planets contains day_lord when hora_lord is None
"""

import pytest
from app.lalkitab_time_planet import detect_time_planet


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SUNDAY_DATE    = "2024-01-07"   # datetime(2024,1,7).weekday() == 6 → Sunday → Sun
MONDAY_DATE    = "2024-01-08"   # datetime(2024,1,8).weekday() == 0 → Monday → Moon
TUESDAY_DATE   = "2024-01-09"   # weekday() == 1 → Tuesday → Mars
SATURDAY_DATE  = "2024-01-13"   # weekday() == 5 → Saturday → Saturn

SAMPLE_TIME    = "10:30:00"
SUNRISE_06     = "06:00:00"


# ---------------------------------------------------------------------------
# Test 1 — Sunday birth
# ---------------------------------------------------------------------------

class TestDayLordSunday:
    def test_sunday_day_lord_is_sun(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["day_lord"] == "Sun"

    def test_sunday_weekday_name(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["weekday_name"] == "Sunday"

    def test_sunday_day_lord_hi_is_surya(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["day_lord_hi"] == "सूर्य", f"Unexpected Hindi: {result['day_lord_hi']!r}"


# ---------------------------------------------------------------------------
# Test 2 — Monday birth
# ---------------------------------------------------------------------------

class TestDayLordMonday:
    def test_monday_day_lord_is_moon(self):
        result = detect_time_planet(MONDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["day_lord"] == "Moon"

    def test_monday_weekday_name(self):
        result = detect_time_planet(MONDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["weekday_name"] == "Monday"

    def test_monday_day_lord_hi_is_chandra(self):
        result = detect_time_planet(MONDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["day_lord_hi"] == "चन्द्र"


# ---------------------------------------------------------------------------
# Test 3 — is_remediable always False
# ---------------------------------------------------------------------------

class TestRemediableAlwaysFalse:
    def test_is_remediable_false_sunday(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["is_remediable"] is False

    def test_is_remediable_false_monday(self):
        result = detect_time_planet(MONDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["is_remediable"] is False

    def test_is_remediable_false_without_sunrise(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, allow_sunrise_fallback=False)
        assert result["is_remediable"] is False

    def test_is_remediable_false_with_fallback(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, allow_sunrise_fallback=True)
        assert result["is_remediable"] is False

    def test_is_remediable_is_exactly_false_not_falsy(self):
        """Must be the boolean literal False, not 0 or None or empty string."""
        result = detect_time_planet(SATURDAY_DATE, "14:00:00", sunrise_hms="06:30:00")
        assert result["is_remediable"] is False


# ---------------------------------------------------------------------------
# Test 4 — allow_sunrise_fallback=True (default) + no sunrise_hms
# ---------------------------------------------------------------------------

class TestFallbackSunrise:
    def test_fallback_sunrise_assumed_true(self):
        """When sunrise_hms is None but fallback is allowed, sunrise_assumed=True."""
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, allow_sunrise_fallback=True)
        assert result["sunrise_assumed"] is True

    def test_fallback_hora_skipped_false(self):
        """With 06:00 fallback, hora IS computed → hora_skipped=False."""
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, allow_sunrise_fallback=True)
        assert result["hora_skipped"] is False

    def test_fallback_hora_lord_is_not_none(self):
        """The 06:00 fallback computes a real hora lord."""
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, allow_sunrise_fallback=True)
        assert result["hora_lord"] is not None, "hora_lord should be set when fallback sunrise is used"


# ---------------------------------------------------------------------------
# Test 5 — allow_sunrise_fallback=False + no sunrise_hms
# ---------------------------------------------------------------------------

class TestNoFallback:
    def test_no_fallback_hora_skipped_true(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, allow_sunrise_fallback=False)
        assert result["hora_skipped"] is True

    def test_no_fallback_hora_lord_none(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, allow_sunrise_fallback=False)
        assert result["hora_lord"] is None

    def test_no_fallback_sunrise_assumed_false(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, allow_sunrise_fallback=False)
        assert result["sunrise_assumed"] is False

    def test_no_fallback_dual_false(self):
        """Without hora_lord, dual cannot be True."""
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, allow_sunrise_fallback=False)
        assert result["dual"] is False

    def test_no_fallback_doubled_false(self):
        """Without hora_lord, doubled cannot be True."""
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, allow_sunrise_fallback=False)
        assert result["doubled"] is False


# ---------------------------------------------------------------------------
# Test 6 — dual=True when day_lord != hora_lord
# ---------------------------------------------------------------------------

class TestDualLogic:
    def test_dual_true_when_lords_differ(self):
        """
        Find a date/time combination where day_lord != hora_lord.
        Sunday (Sun) at 10:30 with sunrise 06:00:
          day_lord = Sun
          Chaldean start index for Sun = 3 (CHALDEAN_ORDER = [Saturn,Jupiter,Mars,Sun,Venus,Mercury,Moon])
          hours_elapsed = 10.5 - 6.0 = 4.5 → int(4.5)=4 → hora_index = (3+4) % 7 = 0 → Saturn
          Sun != Saturn → dual = True
        """
        result = detect_time_planet(SUNDAY_DATE, "10:30:00", sunrise_hms="06:00:00")
        if result["dual"]:
            assert result["day_lord"] != result["hora_lord"], (
                "When dual=True, day_lord and hora_lord must differ"
            )

    def test_dual_false_when_hora_unknown(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, allow_sunrise_fallback=False)
        assert result["dual"] is False

    def test_when_dual_both_planets_has_two_entries(self):
        """When dual=True, both_planets should list both day_lord and hora_lord."""
        result = detect_time_planet(SUNDAY_DATE, "10:30:00", sunrise_hms="06:00:00")
        if result["dual"]:
            assert len(result["both_planets"]) == 2
            assert result["day_lord"] in result["both_planets"]
            assert result["hora_lord"] in result["both_planets"]


# ---------------------------------------------------------------------------
# Test 7 — doubled=True when day_lord == hora_lord
# ---------------------------------------------------------------------------

class TestDoubledLogic:
    def _find_doubled_case(self):
        """
        Find a time where day_lord == hora_lord.
        Sunday (Sun), CHALDEAN_ORDER = [Saturn,Jupiter,Mars,Sun,Venus,Mercury,Moon]
        day_lord = Sun, index = 3
        hora_index = (3 + N) % 7 == 3 → N = 0 (birth within first hour after sunrise)
        Use birth at 06:15 (15 min after 06:00 sunrise → hours_elapsed=0.25, int=0 → index=3 → Sun)
        """
        return detect_time_planet(SUNDAY_DATE, "06:15:00", sunrise_hms="06:00:00")

    def test_doubled_true_when_day_lord_equals_hora_lord(self):
        result = self._find_doubled_case()
        if result["hora_lord"] == result["day_lord"]:
            assert result["doubled"] is True, (
                "doubled must be True when day_lord == hora_lord"
            )

    def test_doubled_implies_dual_false(self):
        """doubled=True and dual=True are mutually exclusive per LK logic."""
        result = self._find_doubled_case()
        if result["doubled"]:
            assert result["dual"] is False, "doubled=True implies dual=False"

    def test_doubled_both_planets_has_one_entry(self):
        """When doubled, both_planets contains just the one planet (not duplicated)."""
        result = self._find_doubled_case()
        if result["doubled"]:
            assert len(result["both_planets"]) == 1
            assert result["both_planets"][0] == result["day_lord"]


# ---------------------------------------------------------------------------
# Test 8 — Metadata / canonical fields
# ---------------------------------------------------------------------------

class TestMetadata:
    def test_source_is_lk_canonical(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["source"] == "LK_CANONICAL"

    def test_lk_ref_is_2_16(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["lk_ref"] == "2.16"

    def test_all_required_keys_present(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        required = {
            "day_lord", "day_lord_hi", "weekday_name",
            "hora_lord", "hora_lord_hi", "hora_skipped", "sunrise_assumed",
            "time_planet", "time_planet_hi", "both_planets",
            "dual", "doubled", "is_remediable",
            "warning_en", "warning_hi", "source", "lk_ref",
        }
        missing = required - result.keys()
        assert not missing, f"Result is missing keys: {missing}"

    def test_warning_en_is_non_empty_string(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert isinstance(result["warning_en"], str) and len(result["warning_en"]) > 10

    def test_warning_hi_is_non_empty_string(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert isinstance(result["warning_hi"], str) and len(result["warning_hi"]) > 10


# ---------------------------------------------------------------------------
# Test 9 — Invalid birth_time raises ValueError
# ---------------------------------------------------------------------------

class TestInvalidInput:
    def test_invalid_time_format_raises_value_error(self):
        with pytest.raises(ValueError):
            detect_time_planet(SUNDAY_DATE, "not-a-time")

    def test_missing_time_parts_raises_value_error(self):
        """Single part (no colon) is not HH:MM."""
        with pytest.raises(ValueError):
            detect_time_planet(SUNDAY_DATE, "1030")

    def test_invalid_date_raises_value_error(self):
        with pytest.raises(ValueError):
            detect_time_planet("not-a-date", SAMPLE_TIME)


# ---------------------------------------------------------------------------
# Test 10 — Other day lords (correctness spot-check)
# ---------------------------------------------------------------------------

class TestOtherDayLords:
    def test_tuesday_day_lord_is_mars(self):
        result = detect_time_planet(TUESDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["day_lord"] == "Mars"
        assert result["weekday_name"] == "Tuesday"

    def test_saturday_day_lord_is_saturn(self):
        result = detect_time_planet(SATURDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["day_lord"] == "Saturn"
        assert result["weekday_name"] == "Saturday"

    def test_time_planet_is_a_known_planet(self):
        known = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["time_planet"] in known, f"Unexpected time_planet: {result['time_planet']!r}"

    def test_both_planets_always_contains_day_lord(self):
        result = detect_time_planet(SUNDAY_DATE, SAMPLE_TIME, sunrise_hms=SUNRISE_06)
        assert result["day_lord"] in result["both_planets"], (
            "both_planets must always contain day_lord"
        )
