"""Tests for lalkitab_engine.py — Lal Kitab remedies engine."""
import pytest


def test_remedies_dict_has_9_planets():
    """REMEDIES dict must cover all 9 Vedic planets."""
    from app.lalkitab_engine import REMEDIES
    expected = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
    assert set(REMEDIES.keys()) == expected


def test_remedies_per_planet_count():
    """Each planet should have 5-8 remedies."""
    from app.lalkitab_engine import REMEDIES
    for planet, remedies in REMEDIES.items():
        assert 5 <= len(remedies) <= 8, f"{planet} has {len(remedies)} remedies, expected 5-8"


def test_weak_planet_gets_remedies():
    """A debilitated planet (strength < 0.5) should receive remedies."""
    from app.lalkitab_engine import get_remedies
    # Sun debilitated in Libra => strength 0.20
    positions = {"Sun": "Libra", "Moon": "Taurus"}
    result = get_remedies(positions)

    assert "Sun" in result
    assert result["Sun"]["strength"] == 0.20
    assert result["Sun"]["dignity"] == "Debilitated"
    assert len(result["Sun"]["remedies"]) > 0  # should have remedies

    assert "Moon" in result
    assert result["Moon"]["strength"] == 0.95  # exalted
    assert result["Moon"]["remedies"] == []  # no remedies needed


def test_strong_planet_no_remedies():
    """An exalted planet (strength >= 0.5) should NOT receive remedies."""
    from app.lalkitab_engine import get_remedies
    # Jupiter exalted in Cancer => strength 0.95
    positions = {"Jupiter": "Cancer"}
    result = get_remedies(positions)
    assert result["Jupiter"]["strength"] == 0.95
    assert result["Jupiter"]["remedies"] == []


def test_enemy_planet_gets_remedies():
    """A planet in enemy sign (strength 0.35 < 0.5) should receive remedies."""
    from app.lalkitab_engine import get_remedies
    # Sun in Taurus is enemy => strength 0.35
    positions = {"Sun": "Taurus"}
    result = get_remedies(positions)
    assert result["Sun"]["strength"] == 0.35
    assert result["Sun"]["dignity"] == "Enemy"
    assert len(result["Sun"]["remedies"]) > 0


def test_output_structure():
    """Verify the output dict structure for each planet."""
    from app.lalkitab_engine import get_remedies
    positions = {"Sun": "Leo", "Moon": "Scorpio", "Mars": "Cancer"}
    result = get_remedies(positions)

    for planet in positions:
        assert "sign" in result[planet]
        assert "dignity" in result[planet]
        assert "strength" in result[planet]
        assert "remedies" in result[planet]
        assert isinstance(result[planet]["remedies"], list)
