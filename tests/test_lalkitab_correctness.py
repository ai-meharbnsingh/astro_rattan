"""
Correctness smoke tests for Lal Kitab — validate that real calculations
produce expected output for known inputs. These tests catch fraud patterns
(hardcoded results, fabricated data, algorithmic errors).

NOTE: In this codebase, `app.astro_iogita_engine.get_planet_strength()` returns
a FLOAT (0.0–1.0), not a dignity string. The string dignity label is produced
by `get_planet_strength_detailed()` (which returns a dict with "dignity" key).
Tests below use the detailed function for dignity-name assertions.
"""
import pytest

from app.lalkitab_engine import (
    get_planet_strength,            # float 0.0–1.0
    get_planet_strength_detailed,   # dict with dignity / score / afflictions
    get_remedies,
)
from app.lalkitab_milestones import calculate_age_milestones


# ---------------------------------------------------------------------------
# Test 1: Classical dignity rules are correct
# ---------------------------------------------------------------------------
def test_exaltation_dignity_is_correct():
    """Sun in Aries should be Exalted, not something else."""
    # Dignity label via detailed function (the public string dignity API)
    assert get_planet_strength_detailed("Sun", "Aries")["dignity"] == "Exalted"
    assert get_planet_strength_detailed("Moon", "Taurus")["dignity"] == "Exalted"
    assert get_planet_strength_detailed("Jupiter", "Cancer")["dignity"] == "Exalted"
    assert get_planet_strength_detailed("Saturn", "Libra")["dignity"] == "Exalted"
    # Debilitations
    assert get_planet_strength_detailed("Sun", "Libra")["dignity"] == "Debilitated"
    assert get_planet_strength_detailed("Jupiter", "Capricorn")["dignity"] == "Debilitated"

    # Numeric strength also matches classical rules
    assert get_planet_strength("Sun", "Aries") == pytest.approx(0.95)
    assert get_planet_strength("Sun", "Libra") == pytest.approx(0.20)


# ---------------------------------------------------------------------------
# Test 2: Detailed strength respects combustion
# ---------------------------------------------------------------------------
def test_detailed_strength_penalizes_combustion():
    """A planet in its own sign but combust should score lower than non-combust."""
    normal = get_planet_strength_detailed("Mercury", "Gemini", house=3, is_combust=False)
    combust = get_planet_strength_detailed("Mercury", "Gemini", house=3, is_combust=True)
    assert combust["strength_score"] < normal["strength_score"]
    assert "combust" in combust["afflictions"]
    assert "combust" not in normal["afflictions"]


# ---------------------------------------------------------------------------
# Test 3: Detailed strength recognizes dusthana (6/8/12)
# ---------------------------------------------------------------------------
def test_detailed_strength_penalizes_dusthana():
    """Even an exalted planet in 8th house should have affliction noted."""
    result = get_planet_strength_detailed("Sun", "Aries", house=8)
    assert "in dusthana house 8" in result["afflictions"]
    # Dignity label still reports Exalted (sign-level) but score is reduced
    assert result["dignity"] == "Exalted"
    assert result["strength_score"] < 1.0


# ---------------------------------------------------------------------------
# Test 4: Milestones require valid birth_date (no silent default to age 30)
# ---------------------------------------------------------------------------
def test_milestones_raises_on_bad_birth_date():
    """calculate_age_milestones must raise on empty / malformed birth_date."""
    with pytest.raises(ValueError, match="Invalid birth_date"):
        calculate_age_milestones("", [{"planet": "Sun", "house": 1}])
    with pytest.raises(ValueError, match="Invalid birth_date"):
        calculate_age_milestones("not-a-date", [])


# ---------------------------------------------------------------------------
# Test 5: Remedies return real Hindi (Devanagari), distinct from English
# ---------------------------------------------------------------------------
def test_remedies_have_distinct_hindi():
    """After fix, remedy.hi should be real Devanagari Hindi (not duplicated English)."""
    # Mercury in Pisces is Debilitated → should generate a remedy.
    # Saturn in Aries is Debilitated → also triggers remedy. Use both to be sure.
    positions = {
        "Mercury": "Pisces",   # debilitated, strength 0.20
        "Saturn": "Aries",     # debilitated, strength 0.20
        "Sun": "Aries",        # exalted — sanity check (no remedy)
    }
    result = get_remedies(positions)

    # At least one planet should be afflicted and therefore flagged has_remedy
    flagged = [p for p, d in result.items() if d.get("has_remedy")]
    assert flagged, f"Expected ≥1 has_remedy=True for {positions}, got {result}"

    # For each flagged planet the remedy dict must have real Devanagari Hindi
    for planet in flagged:
        remedy = result[planet].get("remedy", {})
        assert isinstance(remedy, dict), f"{planet}: remedy is not a dict"
        hi = remedy.get("hi", "")
        en = remedy.get("en", "")
        assert hi, f"{planet}: remedy.hi is empty"
        # Must not be identical to English
        assert hi != en, f"{planet}: remedy.hi == remedy.en ({hi!r})"
        # Must contain actual Devanagari characters (U+0900–U+097F)
        has_devanagari = any("\u0900" <= c <= "\u097f" for c in hi)
        assert has_devanagari, f"{planet}: remedy.hi has no Devanagari: {hi!r}"


# ---------------------------------------------------------------------------
# Bonus: get_remedies enriched path exposes afflictions when chart_data given
# ---------------------------------------------------------------------------
def test_remedies_enriched_exposes_afflictions():
    """When chart_data is provided, the per-planet result must include afflictions."""
    chart_data = {
        "planets": {
            "Mercury": {"house": 8, "combust": True, "retrograde": True},
        }
    }
    result = get_remedies({"Mercury": "Pisces"}, chart_data=chart_data)
    entry = result["Mercury"]
    assert "afflictions" in entry, "enriched path must expose afflictions list"
    afflictions = entry["afflictions"]
    # Mercury in Pisces is debilitated, 8th house is dusthana, plus combust and retrograde
    assert "debilitated" in afflictions
    assert "in dusthana house 8" in afflictions
    assert "combust" in afflictions
    assert "retrograde" in afflictions
