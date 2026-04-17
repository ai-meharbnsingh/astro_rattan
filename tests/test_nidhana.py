"""Tests for Nidhana-phala — Phaladeepika Adhyaya 17.

Important: Adh. 17 is about end-of-life matters. The engine frames its output
as **longevity indicators + karmic transitions** — NOT specific death/age
predictions. These tests verify both the correctness of the classical rules
AND the soft, philosophical framing.
"""
import re

from app.nidhana_engine import (
    analyze_longevity_indicators,
    _lord_of,
    _maraka_assessment,
    _planet_strength,
    _overall_strength,
    _eighth_house_section,
    _saturn_section,
    _maraka_planets_section,
)


def _p(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {"sign": sign, "house": house, "longitude": longitude, "sign_degree": longitude % 30}


def _aries_chart(planets: dict) -> dict:
    return {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": planets}


# ═══════════════════════════════════════════════════════════════
# Structure
# ═══════════════════════════════════════════════════════════════

def test_top_level_required_fields():
    result = analyze_longevity_indicators(_aries_chart({}))
    for key in (
        "overall_longevity_strength",
        "maraka_planets",
        "eighth_house_analysis",
        "saturn_longevity_assessment",
        "karmic_transitions_en", "karmic_transitions_hi",
        "life_chapters_en", "life_chapters_hi",
        "sloka_ref",
    ):
        assert key in result, f"missing {key}"
    assert result["sloka_ref"] == "Phaladeepika Adh. 17"


def test_overall_strength_enum():
    result = analyze_longevity_indicators(_aries_chart({}))
    assert result["overall_longevity_strength"] in {"strong", "moderate", "weak"}


def test_eighth_house_analysis_fields():
    chart = _aries_chart({"Mars": _p("Capricorn", 10, 280)})
    result = analyze_longevity_indicators(chart)
    e = result["eighth_house_analysis"]
    for key in (
        "eighth_lord", "eighth_lord_placement", "eighth_lord_strength",
        "planets_in_8th", "interpretation_en", "interpretation_hi",
    ):
        assert key in e
    assert isinstance(e["planets_in_8th"], list)


def test_saturn_section_fields():
    chart = _aries_chart({"Saturn": _p("Libra", 7, 190)})
    result = analyze_longevity_indicators(chart)
    s = result["saturn_longevity_assessment"]
    for key in (
        "saturn_placement", "saturn_strength",
        "interpretation_en", "interpretation_hi",
    ):
        assert key in s


def test_life_chapters_has_three_phases():
    result = analyze_longevity_indicators(_aries_chart({}))
    assert len(result["life_chapters_en"]) == 3
    assert len(result["life_chapters_hi"]) == 3
    for ch in result["life_chapters_en"]:
        assert isinstance(ch, str) and ch


# ═══════════════════════════════════════════════════════════════
# SENSITIVITY — philosophical framing
# ═══════════════════════════════════════════════════════════════

_AGE_PATTERN = re.compile(r"\bage\s*\d+|\b\d+\s*years? of age|\bat\s+age\s+\d+|\bdies\b|\bdeath\s+at\b", re.IGNORECASE)
_YEAR_PATTERN = re.compile(r"\bin\s+(19|20)\d{2}\b|\bby\s+(19|20)\d{2}\b")


def _all_narrative_text(result: dict) -> str:
    parts = [
        result["karmic_transitions_en"], result["karmic_transitions_hi"],
        result["eighth_house_analysis"]["interpretation_en"],
        result["eighth_house_analysis"]["interpretation_hi"],
        result["saturn_longevity_assessment"]["interpretation_en"],
        result["saturn_longevity_assessment"]["interpretation_hi"],
    ]
    parts.extend(result["life_chapters_en"])
    parts.extend(result["life_chapters_hi"])
    for m in result["maraka_planets"]:
        parts.extend([m["notes_en"], m["notes_hi"]])
    return " ".join(parts)


def test_no_specific_age_predictions():
    chart = _aries_chart({
        "Mars": _p("Capricorn", 10, 280),
        "Saturn": _p("Libra", 7, 190),
        "Venus": _p("Pisces", 12, 340),
        "Moon": _p("Taurus", 2, 35),
    })
    result = analyze_longevity_indicators(chart)
    text = _all_narrative_text(result)
    assert not _AGE_PATTERN.search(text), f"Found age-specific phrase in narrative: {text[:200]}"


def test_no_specific_year_predictions():
    chart = _aries_chart({
        "Saturn": _p("Aries", 1, 10),  # debilitated
    })
    result = analyze_longevity_indicators(chart)
    text = _all_narrative_text(result)
    assert not _YEAR_PATTERN.search(text), f"Found year-specific phrase: {text[:200]}"


def test_philosophical_framing_words_present():
    """Ensures narrative uses philosophical language and disclaimers."""
    chart = _aries_chart({
        "Mars": _p("Aries", 1, 10),    # own sign Lagna lord → strong
    })
    result = analyze_longevity_indicators(chart)
    karmic = result["karmic_transitions_en"].lower()
    # Soft narrative indicators
    assert any(w in karmic for w in ("not a prediction", "guidance", "philosophical", "dharma"))


def test_disclaimer_phrase_in_hi_narrative():
    result = analyze_longevity_indicators(_aries_chart({}))
    hi = result["karmic_transitions_hi"]
    # Presence of at least one key philosophical HI phrase
    assert any(p in hi for p in ("भविष्यवाणी नहीं", "दार्शनिक", "मार्गदर्शन"))


# ═══════════════════════════════════════════════════════════════
# _lord_of correctness
# ═══════════════════════════════════════════════════════════════

def test_lord_of_aries_lagna():
    chart = _aries_chart({})
    assert _lord_of(2, chart) == "Venus"    # Taurus
    assert _lord_of(7, chart) == "Venus"    # Libra
    assert _lord_of(8, chart) == "Mars"     # Scorpio


def test_lord_of_no_ascendant_returns_empty():
    assert _lord_of(2, {}) == ""
    assert _lord_of(2, {"ascendant": {}}) == ""


# ═══════════════════════════════════════════════════════════════
# Maraka identification
# ═══════════════════════════════════════════════════════════════

def test_marakas_always_two_entries_when_lagna_set():
    chart = _aries_chart({
        "Venus": _p("Taurus", 2, 35),   # 2nd AND 7th lord for Aries
    })
    result = analyze_longevity_indicators(chart)
    # Aries: 2nd=Taurus (Venus), 7th=Libra (Venus). Same planet, two roles → 2 entries.
    assert len(result["maraka_planets"]) == 2
    roles = {m["role"] for m in result["maraka_planets"]}
    assert roles == {"2nd lord", "7th lord"}


def test_maraka_assessment_bucket_labels():
    chart = _aries_chart({
        "Venus": _p("Taurus", 2, 35),   # Kendra/Trikona? 2 = neither. But own sign. Not kendra. Check assessment.
    })
    # Venus in house 2 → moderate (2 is neither kendra nor dusthana)
    assert _maraka_assessment(2, chart) == "moderate"
    assert _maraka_assessment(1, chart) == "strong"    # Kendra+Trikona
    assert _maraka_assessment(8, chart) == "weak"
    assert _maraka_assessment(0, chart) == "unknown"


def test_maraka_entry_has_bilingual_notes():
    chart = _aries_chart({"Venus": _p("Taurus", 2, 35)})
    result = analyze_longevity_indicators(chart)
    for m in result["maraka_planets"]:
        assert m["notes_en"]
        assert m["notes_hi"]
        assert m["planet"]
        assert m["role"]
        assert m["strength"] in {"strong", "moderate", "weak", "unknown"}


# ═══════════════════════════════════════════════════════════════
# 8th house analysis
# ═══════════════════════════════════════════════════════════════

def test_eighth_lord_strong_when_exalted():
    # Aries lagna → 8th = Scorpio → lord Mars. Place Mars exalted (Capricorn) in Kendra
    chart = _aries_chart({"Mars": _p("Capricorn", 10, 280)})
    e = _eighth_house_section(chart)
    assert e["eighth_lord"] == "Mars"
    assert e["eighth_lord_strength"] == "strong"
    assert "positive longevity" in e["interpretation_en"].lower() or "strong" in e["interpretation_en"].lower()


def test_eighth_lord_weak_when_debilitated():
    # Mars debilitated in Cancer, in 4th (neutral house) — still weak due to debilitation
    chart = _aries_chart({"Mars": _p("Cancer", 4, 95)})
    e = _eighth_house_section(chart)
    assert e["eighth_lord_strength"] == "weak"


def test_planets_in_8th_lists_occupants():
    chart = _aries_chart({
        "Mars": _p("Capricorn", 10, 280),
        "Ketu": _p("Scorpio", 8, 220),
        "Saturn": _p("Scorpio", 8, 225),
    })
    e = _eighth_house_section(chart)
    assert "Ketu" in e["planets_in_8th"]
    assert "Saturn" in e["planets_in_8th"]


# ═══════════════════════════════════════════════════════════════
# Saturn section
# ═══════════════════════════════════════════════════════════════

def test_saturn_strong_exalted_in_libra():
    chart = _aries_chart({"Saturn": _p("Libra", 7, 190)})
    s = _saturn_section(chart)
    assert s["saturn_strength"] == "strong"
    assert "longevity" in s["interpretation_en"].lower() or "resilience" in s["interpretation_en"].lower()


def test_saturn_weak_debilitated_in_aries():
    chart = _aries_chart({"Saturn": _p("Aries", 1, 10)})
    s = _saturn_section(chart)
    assert s["saturn_strength"] == "weak"


def test_saturn_missing_returns_missing():
    chart = _aries_chart({})
    s = _saturn_section(chart)
    assert s["saturn_strength"] == "missing"


# ═══════════════════════════════════════════════════════════════
# Overall strength synthesis
# ═══════════════════════════════════════════════════════════════

def test_overall_strong_with_strong_8th_lord_and_saturn():
    # Aries lagna; 8th=Scorpio → Mars exalted (Capricorn, 10th); Saturn exalted (Libra, 7th)
    chart = _aries_chart({
        "Mars": _p("Capricorn", 10, 280),
        "Saturn": _p("Libra", 7, 190),
        # Weak marakas: place Venus (2nd+7th lord) in dusthana
        "Venus": _p("Virgo", 6, 160),
    })
    result = analyze_longevity_indicators(chart)
    assert result["overall_longevity_strength"] == "strong"


def test_overall_weak_with_afflictions():
    # 8th lord debilitated + Saturn debilitated + strong maraka
    chart = _aries_chart({
        "Mars": _p("Cancer", 4, 95),          # 8th-lord debilitated
        "Saturn": _p("Aries", 1, 10),         # debilitated
        "Venus": _p("Aries", 1, 15),          # 2nd/7th lord in Kendra+Trikona → strong maraka
    })
    result = analyze_longevity_indicators(chart)
    assert result["overall_longevity_strength"] == "weak"


def test_moderate_when_balanced():
    """Empty chart with no ascendant → neither strong nor weak indicators."""
    result = analyze_longevity_indicators({})
    assert result["overall_longevity_strength"] == "moderate"


# ═══════════════════════════════════════════════════════════════
# Defensive edge cases
# ═══════════════════════════════════════════════════════════════

def test_none_input_returns_structure():
    result = analyze_longevity_indicators(None)
    assert "overall_longevity_strength" in result
    assert result["sloka_ref"] == "Phaladeepika Adh. 17"


def test_empty_chart_returns_structure():
    result = analyze_longevity_indicators({})
    assert "eighth_house_analysis" in result
    assert result["eighth_house_analysis"]["eighth_lord"] == ""


def test_narrative_text_is_nonempty():
    result = analyze_longevity_indicators(_aries_chart({}))
    assert result["karmic_transitions_en"].strip()
    assert result["karmic_transitions_hi"].strip()
