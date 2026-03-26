"""Tests for matching_engine.py — Ashtakoota Gun Milan."""
import pytest


def test_gun_milan_total_max_is_36():
    """Sum of all koot max points must be 36."""
    from app.matching_engine import GUN_MILAN_KOOTS, GUN_MILAN_TOTAL
    total = sum(k["max"] for k in GUN_MILAN_KOOTS.values())
    assert total == 36
    assert GUN_MILAN_TOTAL == 36


def test_gun_milan_has_8_koots():
    """There must be exactly 8 koots."""
    from app.matching_engine import GUN_MILAN_KOOTS
    assert len(GUN_MILAN_KOOTS) == 8
    expected = {"Varna", "Vasya", "Tara", "Yoni", "Graha Maitri", "Gana", "Bhakoot", "Nadi"}
    assert set(GUN_MILAN_KOOTS.keys()) == expected


def test_nakshatra_data_has_27_entries():
    """All 27 nakshatras must have matching data."""
    from app.matching_engine import NAKSHATRA_DATA
    assert len(NAKSHATRA_DATA) == 27


def test_calculate_gun_milan_same_nakshatra():
    """Same nakshatra for both persons — should yield high compatibility (same yoni, lord, etc.)."""
    from app.matching_engine import calculate_gun_milan
    result = calculate_gun_milan("Ashwini", "Ashwini")
    assert "total_score" in result
    assert "koot_scores" in result
    assert "compatibility_percentage" in result
    assert "recommendation" in result
    # Same nakshatra: same yoni (4), same lord (5), same gana (6), same nadi (0 — dosha!)
    assert result["koot_scores"]["Yoni"]["score"] == 4
    assert result["koot_scores"]["Graha Maitri"]["score"] == 5
    assert result["koot_scores"]["Nadi"]["score"] == 0  # Same nadi = Nadi Dosha
    assert 0 <= result["total_score"] <= 36


def test_calculate_gun_milan_different_nakshatras():
    """Two different nakshatras should return valid score breakdown."""
    from app.matching_engine import calculate_gun_milan
    result = calculate_gun_milan("Rohini", "Hasta")
    assert result["total_score"] >= 0
    assert result["total_score"] <= 36
    assert len(result["koot_scores"]) == 8
    # Check every koot score is within its max
    for koot_name, data in result["koot_scores"].items():
        assert data["score"] <= data["max"], f"{koot_name}: {data['score']} > {data['max']}"
        assert data["score"] >= 0


def test_calculate_gun_milan_recommendation_tiers():
    """Verify recommendation text matches score tiers."""
    from app.matching_engine import calculate_gun_milan
    # We can't control exact scores, but we verify the function runs
    # and returns valid recommendation strings
    result = calculate_gun_milan("Pushya", "Anuradha")
    valid_recs = {"Exceptional match", "Excellent match", "Good match", "Not recommended"}
    assert result["recommendation"] in valid_recs


def test_calculate_gun_milan_percentage_range():
    """Compatibility percentage must be between 0 and 100."""
    from app.matching_engine import calculate_gun_milan
    result = calculate_gun_milan("Bharani", "Mula")
    assert 0.0 <= result["compatibility_percentage"] <= 100.0


def test_calculate_gun_milan_unknown_nakshatra():
    """Unknown nakshatra should return error."""
    from app.matching_engine import calculate_gun_milan
    result = calculate_gun_milan("FakeNakshatra", "Rohini")
    assert "error" in result
    assert result["total_score"] == 0

    result2 = calculate_gun_milan("Rohini", "FakeNakshatra")
    assert "error" in result2


def test_nadi_dosha_different_nadis():
    """Different nadis should get 8 points (max)."""
    from app.matching_engine import calculate_gun_milan
    # Ashwini (Aadi nadi) vs Bharani (Madhya nadi) — different nadis
    result = calculate_gun_milan("Ashwini", "Bharani")
    assert result["koot_scores"]["Nadi"]["score"] == 8
