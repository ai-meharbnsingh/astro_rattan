"""
Tests for Pinnacle Numbers, Challenge Numbers, and Life Cycles
in numerology_engine.py — TDD RED phase.
"""
import pytest
from datetime import date


# ============================================================
# Pinnacle Numbers
# ============================================================

class TestPinnacleCalculation:
    """Pinnacle number calculation for DOB 1990-05-15.

    month = reduce(5)  = 5
    day   = reduce(15) = 6
    year  = reduce(1+9+9+0=19) = 1
    life_path = reduce(5+6+1=12) = 3

    p1 = reduce(month+day) = reduce(11) = 11  (master preserved)
    p2 = reduce(day+year)  = reduce(7)  = 7
    p3 = reduce(p1+p2)     = reduce(18) = 9
    p4 = reduce(month+year)= reduce(6)  = 6
    first_end = max(27, 36-3) = 33
    """

    def test_all_four_pinnacle_numbers(self):
        from app.numerology_engine import _calculate_pinnacles
        result = _calculate_pinnacles("1990-05-15")
        nums = [p["number"] for p in result["pinnacles"]]
        assert nums == [11, 7, 9, 6]

    def test_pinnacle_timing(self):
        from app.numerology_engine import _calculate_pinnacles
        result = _calculate_pinnacles("1990-05-15")
        p = result["pinnacles"]
        # first_end = max(27, 36 - 3) = 33
        assert p[0]["age_end"] == 33
        assert p[1]["age_start"] == 33
        assert p[1]["age_end"] == 42
        assert p[2]["age_start"] == 42
        assert p[2]["age_end"] == 51
        assert p[3]["age_start"] == 51

    def test_current_pinnacle_detection(self):
        """For DOB 1990-05-15, in 2026 age ~35/36 → second pinnacle (33-42)."""
        from app.numerology_engine import _calculate_pinnacles
        result = _calculate_pinnacles("1990-05-15")
        # Age in 2026 = 35 or 36 depending on month
        # Second pinnacle covers 33–42
        assert result["current_pinnacle"] == 2  # 1-indexed

    def test_master_number_preserved_in_pinnacles(self):
        """Pinnacle 1 for 1990-05-15 should be 11 (not reduced to 2)."""
        from app.numerology_engine import _calculate_pinnacles
        result = _calculate_pinnacles("1990-05-15")
        assert result["pinnacles"][0]["number"] == 11

    def test_pinnacle_period_strings(self):
        from app.numerology_engine import _calculate_pinnacles
        result = _calculate_pinnacles("1990-05-15")
        assert "Birth to age 33" in result["pinnacles"][0]["period"]
        assert "Age 51" in result["pinnacles"][3]["period"]

    def test_pinnacle_minimum_age_27(self):
        """First pinnacle end age should be at least 27."""
        from app.numerology_engine import _calculate_pinnacles
        # Life path 1 → 36-1=35, which is >27 → 35
        # Life path 9 → 36-9=27, still ≥27 → 27
        # We need LP > 9 won't happen (LP is 1-9 or master).
        # LP 11 → 36-11=25 → clamp to 27
        # DOB 2009-11-09: LP = reduce(11+2+9=22) = 22 → 36-22=14 → clamp to 27
        result = _calculate_pinnacles("2009-11-09")
        assert result["pinnacles"][0]["age_end"] >= 27


# ============================================================
# Challenge Numbers
# ============================================================

class TestChallengeCalculation:
    """Challenge numbers for DOB 1990-05-15.

    month = reduce(5) = 5
    day   = reduce(15)= 6
    year  = reduce(19)= 1

    c1 = abs(5-6) = 1
    c2 = abs(6-1) = 5
    c3 = abs(1-5) = 4   (main challenge)
    c4 = abs(5-1) = 4
    """

    def test_all_four_challenge_numbers(self):
        from app.numerology_engine import _calculate_challenges
        result = _calculate_challenges("1990-05-15")
        nums = [c["number"] for c in result["challenges"]]
        assert nums == [1, 5, 4, 4]

    def test_challenge_zero_is_valid(self):
        """When month and day reduce to same digit, c1 = 0."""
        from app.numerology_engine import _calculate_challenges
        # DOB 1990-05-05: month=5, day=5 → c1 = abs(5-5) = 0
        result = _calculate_challenges("1990-05-05")
        assert result["challenges"][0]["number"] == 0

    def test_challenge_timing_matches_pinnacles(self):
        from app.numerology_engine import _calculate_challenges
        result = _calculate_challenges("1990-05-15")
        c = result["challenges"]
        # Same timing as pinnacles: first_end = 33
        assert c[0]["age_end"] == 33
        assert c[1]["age_start"] == 33
        assert c[1]["age_end"] == 42

    def test_challenge_has_current(self):
        from app.numerology_engine import _calculate_challenges
        result = _calculate_challenges("1990-05-15")
        assert "current_challenge" in result
        assert isinstance(result["current_challenge"], int)


# ============================================================
# Life Cycles
# ============================================================

class TestLifeCycles:
    """Life cycles for DOB 1990-05-15.

    month_cycle = reduce(5)  = 5  (Early Life)
    day_cycle   = reduce(15) = 6  (Middle Life)
    year_cycle  = reduce(19) = 1  (Later Life)
    """

    def test_three_cycle_numbers(self):
        from app.numerology_engine import _calculate_life_cycles
        result = _calculate_life_cycles("1990-05-15")
        nums = [c["number"] for c in result["cycles"]]
        assert nums == [5, 6, 1]

    def test_cycle_periods_present(self):
        from app.numerology_engine import _calculate_life_cycles
        result = _calculate_life_cycles("1990-05-15")
        assert len(result["cycles"]) == 3
        for cycle in result["cycles"]:
            assert "number" in cycle
            assert "period" in cycle
            assert "theme" in cycle

    def test_current_cycle_detection(self):
        """Age ~36 in 2026 → Middle Life cycle."""
        from app.numerology_engine import _calculate_life_cycles
        result = _calculate_life_cycles("1990-05-15")
        assert result["current_cycle"] == 2  # 1-indexed: 1=early, 2=middle, 3=later


# ============================================================
# Integration with calculate_numerology()
# ============================================================

class TestIntegration:
    def test_calculate_numerology_has_pinnacles(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Test Name", "1990-05-15")
        assert "pinnacles" in result
        assert "pinnacles" in result["pinnacles"]

    def test_calculate_numerology_has_challenges(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Test Name", "1990-05-15")
        assert "challenges" in result
        assert "challenges" in result["challenges"]

    def test_calculate_numerology_has_life_cycles(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Test Name", "1990-05-15")
        assert "life_cycles" in result
        assert "cycles" in result["life_cycles"]


# ============================================================
# Prediction Data — Bilingual Keys
# ============================================================

class TestPredictionData:
    def test_pinnacle_predictions_bilingual(self):
        from app.numerology_engine import PINNACLE_PREDICTIONS
        required_keys = {"title", "title_hi", "opportunity", "opportunity_hi", "lesson", "lesson_hi"}
        # Check all expected numbers: 0-9, 11, 22, 33
        for num in list(range(10)) + [11, 22, 33]:
            assert num in PINNACLE_PREDICTIONS, f"Missing pinnacle prediction for {num}"
            assert required_keys.issubset(PINNACLE_PREDICTIONS[num].keys()), \
                f"Missing bilingual keys for pinnacle {num}"

    def test_challenge_predictions_bilingual(self):
        from app.numerology_engine import CHALLENGE_PREDICTIONS
        required_keys = {"title", "title_hi", "obstacle", "obstacle_hi", "growth", "growth_hi"}
        for num in range(10):
            assert num in CHALLENGE_PREDICTIONS, f"Missing challenge prediction for {num}"
            assert required_keys.issubset(CHALLENGE_PREDICTIONS[num].keys()), \
                f"Missing bilingual keys for challenge {num}"

    def test_life_cycle_predictions_bilingual(self):
        from app.numerology_engine import LIFE_CYCLE_PREDICTIONS
        required_keys = {"title", "title_hi", "theme", "theme_hi", "advice", "advice_hi"}
        for num in list(range(1, 10)) + [11, 22, 33]:
            assert num in LIFE_CYCLE_PREDICTIONS, f"Missing life cycle prediction for {num}"
            assert required_keys.issubset(LIFE_CYCLE_PREDICTIONS[num].keys()), \
                f"Missing bilingual keys for life cycle {num}"

    def test_pinnacle_prediction_lookup_in_result(self):
        """Each pinnacle in the result should have its prediction attached."""
        from app.numerology_engine import _calculate_pinnacles
        result = _calculate_pinnacles("1990-05-15")
        for p in result["pinnacles"]:
            assert "prediction" in p
            assert "title" in p["prediction"]
            assert "title_hi" in p["prediction"]

    def test_challenge_prediction_lookup_in_result(self):
        from app.numerology_engine import _calculate_challenges
        result = _calculate_challenges("1990-05-15")
        for c in result["challenges"]:
            assert "prediction" in c
            assert "title" in c["prediction"]

    def test_life_cycle_prediction_lookup_in_result(self):
        from app.numerology_engine import _calculate_life_cycles
        result = _calculate_life_cycles("1990-05-15")
        for c in result["cycles"]:
            assert "prediction" in c
            assert "title" in c["prediction"]
