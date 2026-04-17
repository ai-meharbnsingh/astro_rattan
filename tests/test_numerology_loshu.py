"""Tests for Lo Shu Grid interpretation — arrows, planes, missing numbers, repeated numbers."""
import pytest


# ---------------------------------------------------------------------------
# 1. Arrow Detection — Strength
# ---------------------------------------------------------------------------

class TestArrowsOfStrength:
    """When ALL 3 numbers of an arrow are present in DOB digits -> strength arrow."""

    def test_determination_arrow_present(self):
        """DOB 1995-05-19 has digits 1,9,9,5,0,5,1,9 -> non-zero {1,5,9} all present."""
        from app.numerology_engine import analyze_loshu_arrows
        dob_digits = [1, 9, 9, 5, 5, 1, 9]  # non-zero digits of 1995-05-19
        result = analyze_loshu_arrows(dob_digits)
        keys = [a["key"] for a in result["arrows_of_strength"]]
        assert "determination" in keys

    def test_intellect_arrow_present(self):
        """DOB with 4, 9, 2 all present -> intellect arrow."""
        from app.numerology_engine import analyze_loshu_arrows
        dob_digits = [2, 4, 9, 1, 9, 8, 2]  # 1992-04-28
        result = analyze_loshu_arrows(dob_digits)
        keys = [a["key"] for a in result["arrows_of_strength"]]
        assert "intellect" in keys

    def test_action_arrow_present(self):
        """DOB with 8, 1, 6 all present -> action arrow."""
        from app.numerology_engine import analyze_loshu_arrows
        dob_digits = [1, 9, 8, 6, 1, 8]  # 1986-01-18
        result = analyze_loshu_arrows(dob_digits)
        keys = [a["key"] for a in result["arrows_of_strength"]]
        assert "action" in keys

    def test_planner_arrow_present(self):
        """DOB with 4, 5, 6 all present -> planner arrow."""
        from app.numerology_engine import analyze_loshu_arrows
        dob_digits = [1, 9, 6, 5, 4, 1, 5]  # 1965-04-15
        result = analyze_loshu_arrows(dob_digits)
        keys = [a["key"] for a in result["arrows_of_strength"]]
        assert "planner" in keys

    def test_prosperity_arrow_present(self):
        """DOB with 2, 5, 8 all present -> prosperity arrow."""
        from app.numerology_engine import analyze_loshu_arrows
        dob_digits = [1, 9, 8, 5, 2, 5]  # 1985-02-25
        result = analyze_loshu_arrows(dob_digits)
        keys = [a["key"] for a in result["arrows_of_strength"]]
        assert "prosperity" in keys

    def test_multiple_arrows_possible(self):
        """DOB with many digits can trigger multiple strength arrows."""
        from app.numerology_engine import analyze_loshu_arrows
        # 1965-04-25 -> digits [1,9,6,5,4,2,5] -> has {1,2,4,5,6,9}
        # determination (1,5,9) YES, intellect (4,9,2) YES, planner (4,5,6) YES,
        # action (8,1,6) NO (missing 8), prosperity (2,5,8) NO (missing 8)
        dob_digits = [1, 9, 6, 5, 4, 2, 5]
        result = analyze_loshu_arrows(dob_digits)
        keys = [a["key"] for a in result["arrows_of_strength"]]
        assert "determination" in keys
        assert "intellect" in keys
        assert "planner" in keys

    def test_strength_arrow_has_bilingual_fields(self):
        """Each strength arrow must have name_hi, meaning, meaning_hi."""
        from app.numerology_engine import analyze_loshu_arrows
        dob_digits = [1, 9, 9, 5, 5, 1, 9]
        result = analyze_loshu_arrows(dob_digits)
        for arrow in result["arrows_of_strength"]:
            assert "name_hi" in arrow, f"Missing name_hi in arrow {arrow['key']}"
            assert "meaning" in arrow, f"Missing meaning in arrow {arrow['key']}"
            assert "meaning_hi" in arrow, f"Missing meaning_hi in arrow {arrow['key']}"


# ---------------------------------------------------------------------------
# 2. Arrow Detection — Weakness
# ---------------------------------------------------------------------------

class TestArrowsOfWeakness:
    """When ALL 3 numbers of an arrow are ABSENT from DOB -> weakness arrow."""

    def test_intellect_weakness(self):
        """DOB missing all of 4, 9, 2 -> intellect weakness."""
        from app.numerology_engine import analyze_loshu_arrows
        # DOB with only 1, 3, 5, 6, 8 -> no 2, no 4, no 9
        dob_digits = [1, 8, 3, 5, 6, 1]
        result = analyze_loshu_arrows(dob_digits)
        weak_keys = [a["key"] for a in result["arrows_of_weakness"]]
        assert "intellect" in weak_keys

    def test_determination_weakness(self):
        """DOB missing all of 1, 5, 9 -> determination weakness."""
        from app.numerology_engine import analyze_loshu_arrows
        # DOB with only 2, 3, 4, 6, 7, 8 -> no 1, no 5, no 9
        dob_digits = [2, 3, 4, 6, 7, 8]
        result = analyze_loshu_arrows(dob_digits)
        weak_keys = [a["key"] for a in result["arrows_of_weakness"]]
        assert "determination" in weak_keys

    def test_no_weakness_when_partial_present(self):
        """If at least 1 number of an arrow is present, it's NOT a weakness."""
        from app.numerology_engine import analyze_loshu_arrows
        # Has 1 but not 5 or 9 -> determination is neither strength nor weakness
        dob_digits = [1, 2, 3, 4, 6, 7, 8]
        result = analyze_loshu_arrows(dob_digits)
        strength_keys = [a["key"] for a in result["arrows_of_strength"]]
        weakness_keys = [a["key"] for a in result["arrows_of_weakness"]]
        assert "determination" not in strength_keys
        assert "determination" not in weakness_keys

    def test_weakness_has_missing_meaning(self):
        """Weakness arrows must include a missing_meaning field."""
        from app.numerology_engine import analyze_loshu_arrows
        dob_digits = [2, 3, 4, 6, 7, 8]  # missing 1,5,9
        result = analyze_loshu_arrows(dob_digits)
        for arrow in result["arrows_of_weakness"]:
            assert "missing_meaning" in arrow, f"Missing missing_meaning in {arrow['key']}"
            assert "missing_meaning_hi" in arrow, f"Missing missing_meaning_hi in {arrow['key']}"


# ---------------------------------------------------------------------------
# 3. Planes Analysis
# ---------------------------------------------------------------------------

class TestPlanesAnalysis:
    """Mental (4,9,2), Emotional (3,5,7), Practical (8,1,6) plane scoring."""

    def test_mental_dominant(self):
        """DOB heavy on 4, 9, 2 -> mental plane dominant."""
        from app.numerology_engine import analyze_loshu_planes
        # 1992-04-24 -> digits [1,9,9,2,4,2,4] -> mental(4,9,2)=2+2+2=6, emo(3,5,7)=0, prac(8,1,6)=1
        dob_digits = [1, 9, 9, 2, 4, 2, 4]
        result = analyze_loshu_planes(dob_digits)
        assert result["dominant_plane"] == "mental"
        assert result["mental"]["score"] > result["emotional"]["score"]
        assert result["mental"]["score"] > result["practical"]["score"]

    def test_emotional_dominant(self):
        """DOB heavy on 3, 5, 7 -> emotional plane dominant."""
        from app.numerology_engine import analyze_loshu_planes
        # 1975-03-07 -> digits [1,9,7,5,3,7] -> mental(4,9,2): 9=1, emo(3,5,7)=3+1+2=6-wait
        # Let's be precise: digits are [1,9,7,5,3,7]
        # counts: 1->1, 9->1, 7->2, 5->1, 3->1
        # mental (4,9,2): count(4)=0 + count(9)=1 + count(2)=0 = 1
        # emotional (3,5,7): count(3)=1 + count(5)=1 + count(7)=2 = 4
        # practical (8,1,6): count(8)=0 + count(1)=1 + count(6)=0 = 1
        dob_digits = [1, 9, 7, 5, 3, 7]
        result = analyze_loshu_planes(dob_digits)
        assert result["dominant_plane"] == "emotional"

    def test_practical_dominant(self):
        """DOB heavy on 8, 1, 6 -> practical plane dominant."""
        from app.numerology_engine import analyze_loshu_planes
        # 1986-08-16 -> digits [1,9,8,6,8,1,6] ->
        # counts: 1->2, 9->1, 8->2, 6->2
        # mental(4,9,2): 0+1+0=1
        # emotional(3,5,7): 0+0+0=0
        # practical(8,1,6): 2+2+2=6
        dob_digits = [1, 9, 8, 6, 8, 1, 6]
        result = analyze_loshu_planes(dob_digits)
        assert result["dominant_plane"] == "practical"

    def test_plane_scores_sum_correctly(self):
        """All plane scores should sum to total non-zero DOB digits."""
        from app.numerology_engine import analyze_loshu_planes
        dob_digits = [1, 9, 8, 5, 2, 5]
        result = analyze_loshu_planes(dob_digits)
        total = result["mental"]["score"] + result["emotional"]["score"] + result["practical"]["score"]
        assert total == len(dob_digits)

    def test_plane_percentages_present(self):
        """Each plane must have a percentage field."""
        from app.numerology_engine import analyze_loshu_planes
        dob_digits = [1, 9, 7, 5, 3, 7]
        result = analyze_loshu_planes(dob_digits)
        for plane in ["mental", "emotional", "practical"]:
            assert "percentage" in result[plane]
            assert isinstance(result[plane]["percentage"], int)

    def test_plane_bilingual_interpretation(self):
        """Planes must have bilingual interpretation."""
        from app.numerology_engine import analyze_loshu_planes
        dob_digits = [1, 9, 7, 5, 3, 7]
        result = analyze_loshu_planes(dob_digits)
        assert "interpretation" in result
        assert "interpretation_hi" in result

    def test_plane_numbers_correct(self):
        """Each plane must report its constituent numbers."""
        from app.numerology_engine import analyze_loshu_planes
        dob_digits = [1, 5, 9]
        result = analyze_loshu_planes(dob_digits)
        assert result["mental"]["numbers"] == [4, 9, 2]
        assert result["emotional"]["numbers"] == [3, 5, 7]
        assert result["practical"]["numbers"] == [8, 1, 6]


# ---------------------------------------------------------------------------
# 4. Missing Numbers Interpretation + Remedies
# ---------------------------------------------------------------------------

class TestMissingNumbers:
    """Missing numbers = digits 1-9 not present in DOB."""

    def test_missing_numbers_for_1990_01_01(self):
        """DOB 1990-01-01 -> digits [1,9,9,1,1] (non-zero) -> present={1,9}, missing={2,3,4,5,6,7,8}."""
        from app.numerology_engine import analyze_missing_numbers
        dob_digits = [1, 9, 9, 1, 1]
        missing = analyze_missing_numbers(dob_digits)
        missing_nums = [m["number"] for m in missing]
        assert set(missing_nums) == {2, 3, 4, 5, 6, 7, 8}

    def test_no_missing_when_all_present(self):
        """If DOB has all digits 1-9, nothing is missing."""
        from app.numerology_engine import analyze_missing_numbers
        dob_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        missing = analyze_missing_numbers(dob_digits)
        assert missing == []

    def test_missing_number_has_remedy_fields(self):
        """Each missing number entry must have meaning, remedy, color, gemstone, planet (bilingual)."""
        from app.numerology_engine import analyze_missing_numbers
        dob_digits = [1, 9, 9, 1, 1]
        missing = analyze_missing_numbers(dob_digits)
        for entry in missing:
            assert "number" in entry
            assert "meaning" in entry
            assert "meaning_hi" in entry
            assert "remedy" in entry
            assert "remedy_hi" in entry
            assert "color" in entry
            assert "color_hi" in entry
            assert "gemstone" in entry
            assert "gemstone_hi" in entry
            assert "planet" in entry

    def test_missing_number_1_meaning(self):
        """Missing number 1 should mention confidence."""
        from app.numerology_engine import analyze_missing_numbers
        dob_digits = [2, 3, 4, 5, 6, 7, 8, 9]  # missing 1
        missing = analyze_missing_numbers(dob_digits)
        entry = [m for m in missing if m["number"] == 1][0]
        assert "confidence" in entry["meaning"].lower()

    def test_missing_number_order(self):
        """Missing numbers should be returned in ascending order."""
        from app.numerology_engine import analyze_missing_numbers
        dob_digits = [1, 5, 9]
        missing = analyze_missing_numbers(dob_digits)
        nums = [m["number"] for m in missing]
        assert nums == sorted(nums)


# ---------------------------------------------------------------------------
# 5. Repeated Numbers Significance
# ---------------------------------------------------------------------------

class TestRepeatedNumbers:
    """Numbers appearing 2+ times in DOB have special significance."""

    def test_repeated_1_detected(self):
        """DOB with multiple 1s -> repeated 1 detected."""
        from app.numerology_engine import analyze_repeated_numbers
        dob_digits = [1, 9, 9, 1, 1]  # 1990-01-01 non-zero
        result = analyze_repeated_numbers(dob_digits)
        nums = [r["number"] for r in result]
        assert 1 in nums
        entry = [r for r in result if r["number"] == 1][0]
        assert entry["count"] == 3

    def test_repeated_9_detected(self):
        """DOB with multiple 9s -> repeated 9 detected."""
        from app.numerology_engine import analyze_repeated_numbers
        dob_digits = [1, 9, 9, 1, 1]
        result = analyze_repeated_numbers(dob_digits)
        nums = [r["number"] for r in result]
        assert 9 in nums
        entry = [r for r in result if r["number"] == 9][0]
        assert entry["count"] == 2

    def test_no_repeated_when_all_unique(self):
        """If all digits appear once, no repeated numbers."""
        from app.numerology_engine import analyze_repeated_numbers
        dob_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = analyze_repeated_numbers(dob_digits)
        assert result == []

    def test_repeated_has_interpretation(self):
        """Repeated number entries must include interpretation and bilingual fields."""
        from app.numerology_engine import analyze_repeated_numbers
        dob_digits = [1, 9, 9, 1, 1]
        result = analyze_repeated_numbers(dob_digits)
        for entry in result:
            assert "number" in entry
            assert "count" in entry
            assert "meaning" in entry
            assert "meaning_hi" in entry

    def test_repeated_count_4_capped(self):
        """If count > max defined interpretation, use highest available."""
        from app.numerology_engine import analyze_repeated_numbers
        dob_digits = [1, 1, 1, 1, 1]  # 5 ones
        result = analyze_repeated_numbers(dob_digits)
        entry = [r for r in result if r["number"] == 1][0]
        assert entry["count"] == 5
        # Should still have a meaning (capped at highest defined)
        assert "meaning" in entry
        assert len(entry["meaning"]) > 0


# ---------------------------------------------------------------------------
# 6. Integration — calculate_numerology includes Lo Shu interpretation
# ---------------------------------------------------------------------------

class TestIntegrationCalculateNumerology:
    """Lo Shu interpretation fields added to calculate_numerology return."""

    def test_calculate_numerology_has_loshu_arrows(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Test Name", "1995-05-19")
        assert "loshu_arrows" in result
        assert "arrows_of_strength" in result["loshu_arrows"]
        assert "arrows_of_weakness" in result["loshu_arrows"]

    def test_calculate_numerology_has_loshu_planes(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Test Name", "1995-05-19")
        assert "loshu_planes" in result
        assert "mental" in result["loshu_planes"]
        assert "emotional" in result["loshu_planes"]
        assert "practical" in result["loshu_planes"]

    def test_calculate_numerology_has_missing_numbers(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Test Name", "1990-01-01")
        assert "missing_numbers" in result
        assert isinstance(result["missing_numbers"], list)
        # 1990-01-01 non-zero digits: {1,9} -> missing 2,3,4,5,6,7,8
        missing_nums = [m["number"] for m in result["missing_numbers"]]
        assert 2 in missing_nums
        assert 3 in missing_nums

    def test_calculate_numerology_has_repeated_numbers(self):
        from app.numerology_engine import calculate_numerology
        result = calculate_numerology("Test Name", "1990-01-01")
        assert "repeated_numbers" in result
        assert isinstance(result["repeated_numbers"], list)


# ---------------------------------------------------------------------------
# 7. Integration — mobile numerology includes Lo Shu interpretation
# ---------------------------------------------------------------------------

class TestIntegrationMobileNumerology:
    """Lo Shu interpretation fields added to mobile numerology when DOB provided."""

    def test_mobile_numerology_has_loshu_arrows(self):
        from app.numerology_engine import calculate_mobile_numerology
        result = calculate_mobile_numerology("9876543210", birth_date="1995-05-19")
        assert "loshu_arrows" in result

    def test_mobile_numerology_has_loshu_planes(self):
        from app.numerology_engine import calculate_mobile_numerology
        result = calculate_mobile_numerology("9876543210", birth_date="1995-05-19")
        assert "loshu_planes" in result

    def test_mobile_numerology_has_missing_numbers(self):
        from app.numerology_engine import calculate_mobile_numerology
        result = calculate_mobile_numerology("9876543210", birth_date="1990-01-01")
        assert "missing_numbers" in result

    def test_mobile_numerology_has_repeated_numbers(self):
        from app.numerology_engine import calculate_mobile_numerology
        result = calculate_mobile_numerology("9876543210", birth_date="1995-05-19")
        assert "repeated_numbers" in result

    def test_mobile_no_loshu_interpretation_without_dob(self):
        """Without DOB, Lo Shu interpretation should NOT be present."""
        from app.numerology_engine import calculate_mobile_numerology
        result = calculate_mobile_numerology("9876543210")
        assert "loshu_arrows" not in result
        assert "loshu_planes" not in result


# ---------------------------------------------------------------------------
# 8. Edge Cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge case handling for Lo Shu interpretation."""

    def test_all_nine_digits_present(self):
        """DOB with all 9 digits -> no missing, many arrows, no weakness."""
        from app.numerology_engine import (
            analyze_loshu_arrows,
            analyze_missing_numbers,
            analyze_loshu_planes,
        )
        dob_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        arrows = analyze_loshu_arrows(dob_digits)
        missing = analyze_missing_numbers(dob_digits)
        planes = analyze_loshu_planes(dob_digits)

        # All arrows should be strength, none weakness
        assert len(arrows["arrows_of_weakness"]) == 0
        assert len(arrows["arrows_of_strength"]) > 0
        assert missing == []
        # All planes equal
        assert planes["mental"]["score"] == 3
        assert planes["emotional"]["score"] == 3
        assert planes["practical"]["score"] == 3

    def test_single_digit_dob(self):
        """DOB with very few unique digits still works."""
        from app.numerology_engine import analyze_loshu_arrows, analyze_missing_numbers
        dob_digits = [1, 1, 1, 1]
        arrows = analyze_loshu_arrows(dob_digits)
        missing = analyze_missing_numbers(dob_digits)
        assert isinstance(arrows["arrows_of_strength"], list)
        assert isinstance(arrows["arrows_of_weakness"], list)
        assert len(missing) == 8  # missing 2-9

    def test_empty_dob_digits(self):
        """Empty digit list -> all missing, no arrows."""
        from app.numerology_engine import analyze_loshu_arrows, analyze_missing_numbers
        dob_digits = []
        arrows = analyze_loshu_arrows(dob_digits)
        missing = analyze_missing_numbers(dob_digits)
        assert len(arrows["arrows_of_strength"]) == 0
        assert len(missing) == 9  # all 1-9 missing
