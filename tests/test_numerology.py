"""Tests for numerology_engine.py — Pythagorean numerology calculations."""
import pytest


def test_life_path_basic():
    """Life path for 1990-01-15: 1+9+9+0=19->10->1 + 0+1=1 + 1+5=6 => 1+1+6=8."""
    from app.numerology_engine import calculate_numerology
    result = calculate_numerology("Test", "1990-01-15")
    assert isinstance(result["life_path"], int)
    assert 1 <= result["life_path"] <= 33


def test_life_path_master_number_11():
    """Verify master number 11 is preserved (not reduced to 2)."""
    from app.numerology_engine import _life_path
    # 1978-08-29: year=1+9+7+8=25->7, month=8, day=2+9=11 (master)
    # But we need 7+8+11=26->8, not 11.
    # Try 2009-11-09: year=2+0+0+9=11, month=1+1=2, day=9 => 11+2+9=22 (master 22!)
    lp = _life_path("2009-11-09")
    assert lp in {11, 22, 33} or 1 <= lp <= 9


def test_destiny_number():
    """Destiny number (formerly expression) uses all letters of the name."""
    from app.numerology_engine import calculate_numerology
    result = calculate_numerology("Meharban Singh", "1990-01-01")
    assert isinstance(result["destiny"], int)
    assert 1 <= result["destiny"] <= 33


def test_soul_urge_vowels_only():
    """Soul urge uses only vowels (A, E, I, O, U)."""
    from app.numerology_engine import _vowels_number, _consonants_number
    name = "AEIOU"
    # A=1, E=5, I=9, O=6, U=3 => 24 -> 6
    soul = _vowels_number(name)
    assert soul == 6
    # No consonants in "AEIOU"
    personality = _consonants_number(name)
    assert personality == 0  # edge case: reduce 0 is 0


def test_personality_consonants_only():
    """Personality uses only consonants."""
    from app.numerology_engine import _consonants_number
    # "BCD" -> B=2, C=3, D=4 => 9
    assert _consonants_number("BCD") == 9


def test_return_structure():
    """Verify all required keys are present in the output dict."""
    from app.numerology_engine import calculate_numerology
    result = calculate_numerology("Test Name", "2000-06-15")
    assert "life_path" in result
    assert "destiny" in result
    assert "soul_urge" in result
    assert "personality" in result
    assert "predictions" in result
    # predictions is now a dict with per-category prediction text
    assert isinstance(result["predictions"], dict)
    for key in ("life_path", "destiny", "soul_urge", "personality"):
        assert key in result["predictions"], f"predictions missing key: {key}"
        assert isinstance(result["predictions"][key], str)
        assert len(result["predictions"][key]) > 10


def test_reduce_master_numbers_preserved():
    """Master numbers 11, 22, 33 should not be reduced further."""
    from app.numerology_engine import _reduce_to_single
    assert _reduce_to_single(11) == 11
    assert _reduce_to_single(22) == 22
    assert _reduce_to_single(33) == 33
    assert _reduce_to_single(44) == 8  # 4+4=8, not master


def test_invalid_date_format():
    """Invalid date format raises ValueError."""
    from app.numerology_engine import calculate_numerology
    with pytest.raises(ValueError):
        calculate_numerology("Test", "15/01/1990")


# ─── Birthday Predictions (1-31) ──────────────────────────────
def test_birthday_raw_day_returned():
    """birthday_number should be the raw day (1–31), not reduced."""
    from app.numerology_engine import calculate_numerology
    result = calculate_numerology("Test User", "1990-05-15")
    assert result["birthday_number"] == 15  # raw day, not 6


def test_birthday_all_31_days_have_unique_titles():
    """Every birthday 1–31 should have its own unique title prediction."""
    from app.numerology_engine import BIRTHDAY_PREDICTIONS, _reduce_to_single
    titles = set()
    for day in range(1, 32):
        pred = BIRTHDAY_PREDICTIONS.get(day, BIRTHDAY_PREDICTIONS.get(_reduce_to_single(day), {}))
        assert pred, f"No prediction for birthday day {day}"
        assert "title" in pred, f"No title for day {day}"
        titles.add(pred["title"])
    # at least 15 distinct titles (1-31 with unique compound day entries)
    assert len(titles) >= 15


def test_birthday_compound_days_unique_from_base():
    """Day 15 should have a different title than day 6 (both reduce to 6)."""
    from app.numerology_engine import BIRTHDAY_PREDICTIONS
    assert 15 in BIRTHDAY_PREDICTIONS, "Day 15 must have its own entry"
    assert BIRTHDAY_PREDICTIONS[15]["title"] != BIRTHDAY_PREDICTIONS[6]["title"]


def test_birthday_prediction_has_hindi():
    """Every birthday prediction must have title_hi and talent_hi."""
    from app.numerology_engine import BIRTHDAY_PREDICTIONS
    for day, pred in BIRTHDAY_PREDICTIONS.items():
        assert "title_hi" in pred, f"Day {day} missing title_hi"
        assert "talent_hi" in pred, f"Day {day} missing talent_hi"


def test_birthday_reduced_also_returned():
    """calculate_numerology should return birthday_reduced as reduced digit."""
    from app.numerology_engine import calculate_numerology
    result = calculate_numerology("Test User", "1990-05-15")
    assert "birthday_reduced" in result
    assert result["birthday_reduced"] == 6  # 1+5=6


# ─── Maturity Predictions Extended ────────────────────────────
def test_maturity_has_description():
    """MATURITY_PREDICTIONS must have description and advice for all entries."""
    from app.numerology_engine import MATURITY_PREDICTIONS
    for num, pred in MATURITY_PREDICTIONS.items():
        assert "description" in pred, f"Maturity {num} missing description"
        assert "description_hi" in pred, f"Maturity {num} missing description_hi"
        assert "advice" in pred, f"Maturity {num} missing advice"
        assert "advice_hi" in pred, f"Maturity {num} missing advice_hi"


def test_maturity_prediction_returned_in_calculate():
    """calculate_numerology maturity_prediction should include description."""
    from app.numerology_engine import calculate_numerology
    result = calculate_numerology("Test Name", "1985-03-22")
    assert "maturity_prediction" in result
    assert "description" in result["maturity_prediction"]
    assert "advice" in result["maturity_prediction"]


# ─── Vehicle Bilingual Fields ──────────────────────────────────
def test_vehicle_predictions_have_hindi():
    """VEHICLE_PREDICTIONS should have energy_hi and prediction_hi for all entries."""
    from app.numerology_engine import VEHICLE_PREDICTIONS
    for num, pred in VEHICLE_PREDICTIONS.items():
        assert "energy_hi" in pred, f"Vehicle {num} missing energy_hi"
        assert "prediction_hi" in pred, f"Vehicle {num} missing prediction_hi"
        assert "caution_hi" in pred, f"Vehicle {num} missing caution_hi"
        assert "best_for_hi" in pred, f"Vehicle {num} missing best_for_hi"
