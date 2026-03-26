"""Tests for dosha_engine.py — Mangal Dosha, Kaal Sarp, Sade Sati."""
import pytest


# ============================================================
# Mangal Dosha Tests
# ============================================================

def test_mangal_dosha_positive_houses():
    """Mars in houses 1, 2, 4, 7, 8, 12 should trigger Mangal Dosha."""
    from app.dosha_engine import check_mangal_dosha
    dosha_houses = [1, 2, 4, 7, 8, 12]
    for house in dosha_houses:
        result = check_mangal_dosha(house)
        assert result["has_dosha"] is True, f"House {house} should have Mangal Dosha"
        assert result["severity"] in {"high", "medium", "mild"}
        assert len(result["remedies"]) > 0


def test_mangal_dosha_negative_houses():
    """Mars in houses 3, 5, 6, 9, 10, 11 should NOT trigger Mangal Dosha."""
    from app.dosha_engine import check_mangal_dosha
    safe_houses = [3, 5, 6, 9, 10, 11]
    for house in safe_houses:
        result = check_mangal_dosha(house)
        assert result["has_dosha"] is False, f"House {house} should NOT have Mangal Dosha"
        assert result["severity"] == "none"
        assert result["remedies"] == []


def test_mangal_dosha_severity_levels():
    """Houses 7/8 = high, 1/4 = medium, 2/12 = mild."""
    from app.dosha_engine import check_mangal_dosha
    assert check_mangal_dosha(7)["severity"] == "high"
    assert check_mangal_dosha(8)["severity"] == "high"
    assert check_mangal_dosha(1)["severity"] == "medium"
    assert check_mangal_dosha(4)["severity"] == "medium"
    assert check_mangal_dosha(2)["severity"] == "mild"
    assert check_mangal_dosha(12)["severity"] == "mild"


# ============================================================
# Kaal Sarp Dosha Tests
# ============================================================

def test_kaal_sarp_all_planets_between_rahu_ketu():
    """All planets on one side of Rahu-Ketu axis = Kaal Sarp Dosha."""
    from app.dosha_engine import check_kaal_sarp
    # Rahu in 1, Ketu in 7 — all planets in houses 1-7
    planet_houses = {
        "Sun": 2, "Moon": 3, "Mars": 4,
        "Mercury": 5, "Jupiter": 5, "Venus": 6, "Saturn": 6,
    }
    result = check_kaal_sarp(1, 7, planet_houses)
    assert result["has_dosha"] is True
    assert len(result["affected_planets"]) == 7
    assert len(result["remedies"]) > 0


def test_kaal_sarp_no_dosha_planets_both_sides():
    """Planets on both sides of axis = no Kaal Sarp Dosha."""
    from app.dosha_engine import check_kaal_sarp
    # Rahu in 1, Ketu in 7 — planets split across both sides
    planet_houses = {
        "Sun": 2, "Moon": 3, "Mars": 4,
        "Mercury": 9, "Jupiter": 10, "Venus": 11, "Saturn": 12,
    }
    result = check_kaal_sarp(1, 7, planet_houses)
    assert result["has_dosha"] is False


def test_kaal_sarp_empty_planets():
    """Empty planet dict should return no dosha."""
    from app.dosha_engine import check_kaal_sarp
    result = check_kaal_sarp(1, 7, {})
    assert result["has_dosha"] is False


# ============================================================
# Sade Sati Tests
# ============================================================

def test_sade_sati_saturn_on_moon():
    """Saturn on Moon sign = peak Sade Sati."""
    from app.dosha_engine import check_sade_sati
    result = check_sade_sati("Aries", "Aries")
    assert result["has_sade_sati"] is True
    assert result["phase"] == "Peak (over Moon sign)"
    assert result["severity"] == "high"


def test_sade_sati_saturn_before_moon():
    """Saturn one sign before Moon = rising Sade Sati."""
    from app.dosha_engine import check_sade_sati
    # Pisces is one sign before Aries
    result = check_sade_sati("Aries", "Pisces")
    assert result["has_sade_sati"] is True
    assert result["phase"] == "Rising (12th from Moon)"


def test_sade_sati_saturn_after_moon():
    """Saturn one sign after Moon = setting Sade Sati."""
    from app.dosha_engine import check_sade_sati
    # Taurus is one sign after Aries
    result = check_sade_sati("Aries", "Taurus")
    assert result["has_sade_sati"] is True
    assert result["phase"] == "Setting (2nd from Moon)"


def test_sade_sati_no_sade_sati():
    """Saturn far from Moon = no Sade Sati."""
    from app.dosha_engine import check_sade_sati
    result = check_sade_sati("Aries", "Libra")
    assert result["has_sade_sati"] is False
    assert result["phase"] == "none"
    assert result["remedies"] == []


def test_sade_sati_wrap_around():
    """Test wrap-around: Moon in Aries (index 0), Saturn in Pisces (index 11)."""
    from app.dosha_engine import check_sade_sati
    # Pisces (11) is before Aries (0) — should be rising
    result = check_sade_sati("Aries", "Pisces")
    assert result["has_sade_sati"] is True

    # Capricorn (9) — should be Aquarius (10) before Pisces (11) — no sade sati for Aries
    result2 = check_sade_sati("Aries", "Sagittarius")
    assert result2["has_sade_sati"] is False


def test_sade_sati_invalid_sign():
    """Invalid sign should return no sade sati with appropriate message."""
    from app.dosha_engine import check_sade_sati
    result = check_sade_sati("InvalidSign", "Aries")
    assert result["has_sade_sati"] is False
