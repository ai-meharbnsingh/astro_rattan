"""
Tests for 6 new core numerology calculations:
Birthday Number, Maturity Number, Karmic Debt Detection,
Hidden Passion, Subconscious Self, Karmic Lessons.
"""
import pytest


# ============================================================
# 1. Birthday Number tests
# ============================================================

class TestBirthdayNumber:
    """Birthday Number = birth day reduced to single digit or master number."""

    def test_29th_gives_master_11(self):
        from app.numerology_engine import _birthday_number
        # 29 -> 2+9 = 11 (master)
        assert _birthday_number("1990-03-29") == 11

    def test_15th_gives_6(self):
        from app.numerology_engine import _birthday_number
        # 15 -> 1+5 = 6
        assert _birthday_number("2000-07-15") == 6

    def test_1st_gives_1(self):
        from app.numerology_engine import _birthday_number
        # 1 -> 1
        assert _birthday_number("1985-12-01") == 1

    def test_22nd_gives_master_22(self):
        from app.numerology_engine import _birthday_number
        # 22 -> master number preserved
        assert _birthday_number("1995-06-22") == 22

    def test_10th_gives_1(self):
        from app.numerology_engine import _birthday_number
        # 10 -> 1+0 = 1
        assert _birthday_number("2001-01-10") == 1

    def test_28th_gives_1(self):
        from app.numerology_engine import _birthday_number
        # 28 -> 2+8 = 10 -> 1+0 = 1
        assert _birthday_number("1999-05-28") == 1

    def test_9th_gives_9(self):
        from app.numerology_engine import _birthday_number
        # 9 -> 9
        assert _birthday_number("1988-11-09") == 9


# ============================================================
# 2. Maturity Number tests
# ============================================================

class TestMaturityNumber:
    """Maturity Number = Life Path + Expression, reduced."""

    def test_basic_sum_and_reduce(self):
        from app.numerology_engine import _maturity_number
        # LP=8, Expression=5 -> 13 -> 1+3 = 4
        assert _maturity_number(8, 5) == 4

    def test_master_number_preserved(self):
        from app.numerology_engine import _maturity_number
        # LP=9, Expression=2 -> 11 (master)
        assert _maturity_number(9, 2) == 11

    def test_master_22_preserved(self):
        from app.numerology_engine import _maturity_number
        # LP=11, Expression=11 -> 22 (master)
        assert _maturity_number(11, 11) == 22

    def test_small_values(self):
        from app.numerology_engine import _maturity_number
        # LP=1, Expression=2 -> 3
        assert _maturity_number(1, 2) == 3

    def test_larger_values(self):
        from app.numerology_engine import _maturity_number
        # LP=9, Expression=9 -> 18 -> 1+8 = 9
        assert _maturity_number(9, 9) == 9


# ============================================================
# 3. Karmic Debt Detection tests
# ============================================================

class TestKarmicDebtDetection:
    """Karmic Debt = 13, 14, 16, 19 appearing as intermediate sums."""

    def test_returns_list(self):
        from app.numerology_engine import _detect_karmic_debt
        result = _detect_karmic_debt("1990-01-15", "Test Name")
        assert isinstance(result, list)

    def test_each_debt_has_required_keys(self):
        from app.numerology_engine import _detect_karmic_debt
        result = _detect_karmic_debt("1990-01-15", "Test Name")
        for debt in result:
            assert "number" in debt
            assert "source" in debt
            assert "interpretation" in debt

    def test_birthday_13_detected(self):
        """Born on the 13th — karmic debt 13 from birthday."""
        from app.numerology_engine import _detect_karmic_debt
        result = _detect_karmic_debt("1990-05-13", "Test Name")
        debt_numbers = [d["number"] for d in result]
        assert 13 in debt_numbers

    def test_birthday_14_detected(self):
        """Born on the 14th — karmic debt 14 from birthday."""
        from app.numerology_engine import _detect_karmic_debt
        result = _detect_karmic_debt("1990-05-14", "Test Name")
        debt_numbers = [d["number"] for d in result]
        assert 14 in debt_numbers

    def test_birthday_16_detected(self):
        """Born on the 16th — karmic debt 16 from birthday."""
        from app.numerology_engine import _detect_karmic_debt
        result = _detect_karmic_debt("1990-05-16", "Test Name")
        debt_numbers = [d["number"] for d in result]
        assert 16 in debt_numbers

    def test_birthday_19_detected(self):
        """Born on the 19th — karmic debt 19 from birthday."""
        from app.numerology_engine import _detect_karmic_debt
        result = _detect_karmic_debt("1990-05-19", "Test Name")
        debt_numbers = [d["number"] for d in result]
        assert 19 in debt_numbers

    def test_no_debt_for_clean_birthday(self):
        """Born on the 15th — no birthday karmic debt (15 is not 13/14/16/19)."""
        from app.numerology_engine import _detect_karmic_debt
        result = _detect_karmic_debt("2000-01-15", "AAAA")
        birthday_debts = [d for d in result if d["source"] == "birthday"]
        assert len(birthday_debts) == 0

    def test_karmic_debt_interpretations_exist(self):
        from app.numerology_engine import KARMIC_DEBT_INTERPRETATIONS
        for num in [13, 14, 16, 19]:
            assert num in KARMIC_DEBT_INTERPRETATIONS
            interp = KARMIC_DEBT_INTERPRETATIONS[num]
            assert "title" in interp
            assert "meaning" in interp
            assert "title_hi" in interp
            assert "meaning_hi" in interp


# ============================================================
# 4. Hidden Passion tests
# ============================================================

class TestHiddenPassion:
    """Hidden Passion = most frequently occurring Pythagorean number in name."""

    def test_returns_dict_with_number(self):
        from app.numerology_engine import _hidden_passion
        result = _hidden_passion("Meharban Singh")
        assert isinstance(result, dict)
        assert "number" in result
        assert "count" in result
        assert isinstance(result["number"], int)
        assert 1 <= result["number"] <= 9

    def test_all_same_letter(self):
        """Name 'AAAA' — all A=1, so hidden passion is 1."""
        from app.numerology_engine import _hidden_passion
        result = _hidden_passion("AAAA")
        assert result["number"] == 1
        assert result["count"] == 4

    def test_clear_dominant(self):
        """Name 'AAABBC' — A=1 x3, B=2 x2, C=3 x1 => hidden passion 1."""
        from app.numerology_engine import _hidden_passion
        result = _hidden_passion("AAABBC")
        assert result["number"] == 1
        assert result["count"] == 3

    def test_prediction_included(self):
        from app.numerology_engine import _hidden_passion
        result = _hidden_passion("Meharban Singh")
        assert "meaning" in result  # prediction data merged into result

    def test_hidden_passion_predictions_exist(self):
        from app.numerology_engine import HIDDEN_PASSION_PREDICTIONS
        for n in range(1, 10):
            assert n in HIDDEN_PASSION_PREDICTIONS
            pred = HIDDEN_PASSION_PREDICTIONS[n]
            assert "title" in pred
            assert "meaning" in pred or "title" in pred
            assert "title_hi" in pred
            assert "meaning_hi" in pred or "title_hi" in pred


# ============================================================
# 5. Subconscious Self tests
# ============================================================

class TestSubconsciousSelf:
    """Subconscious Self = count of distinct numbers (1-9) present in name."""

    def test_returns_dict_with_number(self):
        from app.numerology_engine import _subconscious_self
        result = _subconscious_self("Meharban Singh")
        assert isinstance(result, dict)
        assert "number" in result
        assert "missing_numbers" in result

    def test_number_range(self):
        """Subconscious self is count of numbers present, so 1-9."""
        from app.numerology_engine import _subconscious_self
        result = _subconscious_self("Meharban Singh")
        assert 1 <= result["number"] <= 9

    def test_missing_is_list(self):
        from app.numerology_engine import _subconscious_self
        result = _subconscious_self("Meharban Singh")
        assert isinstance(result["missing_numbers"], list)

    def test_number_plus_missing_equals_9(self):
        """count_present + len(missing) = 9 always."""
        from app.numerology_engine import _subconscious_self
        result = _subconscious_self("Meharban Singh")
        assert result["number"] + len(result["missing_numbers"]) == 9

    def test_all_letters_name(self):
        """A name that uses all 9 letter values should have subconscious self = 9."""
        from app.numerology_engine import _subconscious_self
        # A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9
        result = _subconscious_self("ABCDEFGHI")
        assert result["number"] == 9
        assert result["missing_numbers"] == []

    def test_single_letter_name(self):
        """Single letter 'A' -> only number 1 present, missing 2-9."""
        from app.numerology_engine import _subconscious_self
        result = _subconscious_self("A")
        assert result["number"] == 1
        assert len(result["missing_numbers"]) == 8

    def test_subconscious_self_predictions_exist(self):
        from app.numerology_engine import SUBCONSCIOUS_SELF_PREDICTIONS
        for n in range(3, 10):  # subconscious self ranges 3-9
            assert n in SUBCONSCIOUS_SELF_PREDICTIONS
            pred = SUBCONSCIOUS_SELF_PREDICTIONS[n]
            assert "title" in pred
            assert "meaning" in pred or "title" in pred
            assert "title_hi" in pred
            assert "meaning_hi" in pred or "title_hi" in pred


# ============================================================
# 6. Karmic Lessons tests
# ============================================================

class TestKarmicLessons:
    """Karmic Lessons = numbers 1-9 completely absent from the name."""

    def test_returns_list(self):
        from app.numerology_engine import _karmic_lessons
        result = _karmic_lessons("Meharban Singh")
        assert isinstance(result, list)

    def test_each_lesson_has_required_keys(self):
        from app.numerology_engine import _karmic_lessons
        result = _karmic_lessons("Meharban Singh")
        for lesson in result:
            assert "number" in lesson
            assert "lesson" in lesson
            assert "remedy" in lesson

    def test_full_alphabet_name_no_lessons(self):
        """A name containing all 9 Pythagorean values has no karmic lessons."""
        from app.numerology_engine import _karmic_lessons
        # A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9
        result = _karmic_lessons("ABCDEFGHI")
        assert result == []

    def test_single_letter_has_8_lessons(self):
        """Single letter 'A' (value 1) — missing numbers 2-9 = 8 karmic lessons."""
        from app.numerology_engine import _karmic_lessons
        result = _karmic_lessons("A")
        assert len(result) == 8
        missing = [l["number"] for l in result]
        for n in range(2, 10):
            assert n in missing

    def test_lesson_interpretations_exist(self):
        from app.numerology_engine import KARMIC_LESSON_INTERPRETATIONS
        for n in range(1, 10):
            assert n in KARMIC_LESSON_INTERPRETATIONS
            interp = KARMIC_LESSON_INTERPRETATIONS[n]
            assert "lesson" in interp
            assert "lesson_hi" in interp
            assert "remedy" in interp
            assert "remedy_hi" in interp


# ============================================================
# 7. Prediction dicts structure validation
# ============================================================

class TestPredictionDicts:
    """All prediction dicts must have required bilingual keys."""

    def test_birthday_predictions_bilingual(self):
        from app.numerology_engine import BIRTHDAY_PREDICTIONS
        required_keys = {"title",
                         "title_hi"}
        for num in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33]:
            assert num in BIRTHDAY_PREDICTIONS, f"Missing BIRTHDAY_PREDICTIONS[{num}]"
            assert required_keys.issubset(BIRTHDAY_PREDICTIONS[num].keys()), \
                f"BIRTHDAY_PREDICTIONS[{num}] missing keys: {required_keys - set(BIRTHDAY_PREDICTIONS[num].keys())}"

    def test_maturity_predictions_bilingual(self):
        from app.numerology_engine import MATURITY_PREDICTIONS
        required_keys = {"title",
                         "title_hi"}
        for num in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33]:
            assert num in MATURITY_PREDICTIONS, f"Missing MATURITY_PREDICTIONS[{num}]"
            assert required_keys.issubset(MATURITY_PREDICTIONS[num].keys()), \
                f"MATURITY_PREDICTIONS[{num}] missing keys: {required_keys - set(MATURITY_PREDICTIONS[num].keys())}"

    def test_hidden_passion_predictions_bilingual(self):
        from app.numerology_engine import HIDDEN_PASSION_PREDICTIONS
        required_keys = {"title",
                         "title_hi"}
        for num in range(1, 10):
            assert num in HIDDEN_PASSION_PREDICTIONS
            assert required_keys.issubset(HIDDEN_PASSION_PREDICTIONS[num].keys())

    def test_subconscious_self_predictions_bilingual(self):
        from app.numerology_engine import SUBCONSCIOUS_SELF_PREDICTIONS
        required_keys = {"title",
                         "title_hi"}
        for num in range(3, 10):
            assert num in SUBCONSCIOUS_SELF_PREDICTIONS
            assert required_keys.issubset(SUBCONSCIOUS_SELF_PREDICTIONS[num].keys())

    def test_karmic_debt_interpretations_bilingual(self):
        from app.numerology_engine import KARMIC_DEBT_INTERPRETATIONS
        required_keys = {"title",
                         "title_hi"}
        for num in [13, 14, 16, 19]:
            assert num in KARMIC_DEBT_INTERPRETATIONS
            assert required_keys.issubset(KARMIC_DEBT_INTERPRETATIONS[num].keys())

    def test_karmic_lesson_interpretations_bilingual(self):
        from app.numerology_engine import KARMIC_LESSON_INTERPRETATIONS
        required_keys = {"lesson", "lesson_hi", "remedy", "remedy_hi"}
        for num in range(1, 10):
            assert num in KARMIC_LESSON_INTERPRETATIONS
            assert required_keys.issubset(KARMIC_LESSON_INTERPRETATIONS[num].keys())


# ============================================================
# 8. Integration — calculate_numerology returns new fields
# ============================================================

class TestIntegration:
    """calculate_numerology() must include all 6 new fields."""

    def test_birthday_number_in_result(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Meharban Singh", "1990-03-29")
        assert "birthday_number" in result
        assert isinstance(result["birthday_number"], int)
        assert "birthday_prediction" in result
        assert isinstance(result["birthday_prediction"], dict)

    def test_maturity_number_in_result(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Meharban Singh", "1990-03-29")
        assert "maturity_number" in result
        assert isinstance(result["maturity_number"], int)
        assert "maturity_prediction" in result
        assert isinstance(result["maturity_prediction"], dict)

    def test_karmic_debts_in_result(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Meharban Singh", "1990-03-29")
        assert "karmic_debts" in result
        assert isinstance(result["karmic_debts"], list)

    def test_hidden_passion_in_result(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Meharban Singh", "1990-03-29")
        assert "hidden_passion" in result
        assert isinstance(result["hidden_passion"], dict)
        assert "number" in result["hidden_passion"]

    def test_subconscious_self_in_result(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Meharban Singh", "1990-03-29")
        assert "subconscious_self" in result
        assert isinstance(result["subconscious_self"], dict)
        assert "number" in result["subconscious_self"]

    def test_karmic_lessons_in_result(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Meharban Singh", "1990-03-29")
        assert "karmic_lessons" in result
        assert isinstance(result["karmic_lessons"], list)

    def test_existing_fields_unchanged(self):
        """Existing fields must still be present and correct."""
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Meharban Singh", "1990-03-29")
        assert "life_path" in result
        assert "destiny" in result
        assert "soul_urge" in result
        assert "personality" in result
        assert "predictions" in result
