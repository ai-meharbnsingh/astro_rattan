"""Tests for Bhava-phala-vichara — Phaladeepika Adhyaya 15."""
from app.bhava_vichara_engine import (
    analyze_bhava_vichara,
    _bhava_karakas,
    _analyze_karaka_as_lagna,
    _house_lord,
    _assess_bhava,
    _planet_aspects_house,
    _is_exalted,
    _is_debilitated,
    BHAVA_TOPIC_EN,
    BHAVA_TOPIC_HI,
)


def _p(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {"sign": sign, "house": house, "longitude": longitude, "sign_degree": longitude % 30}


def _aries_chart(planets: dict) -> dict:
    return {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": planets}


# ═══════════════════════════════════════════════════════════════
# Karaka table integrity
# ═══════════════════════════════════════════════════════════════

def test_bhava_karakas_has_all_12_houses():
    k = _bhava_karakas()
    assert set(k.keys()) == set(range(1, 13))
    for h in range(1, 13):
        assert k[h], f"House {h} has empty karaka"


def test_bhava_karakas_classical_mapping():
    k = _bhava_karakas()
    # Classical mandatory ones
    assert k[1] == "Sun"
    assert k[2] == "Jupiter"
    assert k[3] == "Mars"
    assert k[4] == "Moon"
    assert k[5] == "Jupiter"
    assert k[7] == "Venus"
    assert k[8] == "Saturn"
    assert k[9] == "Jupiter"
    assert k[11] == "Jupiter"
    assert k[12] == "Saturn"
    # Dual karakas
    assert "/" in k[6]
    assert "/" in k[10]


# ═══════════════════════════════════════════════════════════════
# analyze_bhava_vichara structure
# ═══════════════════════════════════════════════════════════════

def test_analyze_returns_12_bhava_assessments():
    result = analyze_bhava_vichara(_aries_chart({}))
    assert "bhava_assessments" in result
    assert len(result["bhava_assessments"]) == 12
    for i, a in enumerate(result["bhava_assessments"], 1):
        assert a["house"] == i


def test_analyze_has_required_top_level_fields():
    result = analyze_bhava_vichara(_aries_chart({}))
    for k in (
        "bhava_assessments", "overall_strongest", "overall_weakest", "sloka_ref"
    ):
        assert k in result
    assert result["sloka_ref"] == "Phaladeepika Adh. 15"


def test_each_assessment_has_required_fields():
    chart = _aries_chart({"Mars": _p("Capricorn", 10, 280)})
    result = analyze_bhava_vichara(chart)
    for a in result["bhava_assessments"]:
        for key in (
            "house", "name_en", "name_hi", "lord", "lord_placement",
            "karaka", "flourishing", "destruction_risk",
            "reasons_en", "reasons_hi",
            "karaka_as_lagna_analysis_en", "karaka_as_lagna_analysis_hi",
            "sloka_ref",
        ):
            assert key in a, f"house {a['house']} missing {key}"
        assert isinstance(a["flourishing"], bool)
        assert isinstance(a["destruction_risk"], bool)
        assert isinstance(a["reasons_en"], list)
        assert isinstance(a["reasons_hi"], list)


def test_bilingual_reasons_parity():
    """Whenever a reason appears in EN it must also appear in HI."""
    chart = _aries_chart({
        "Mars": _p("Capricorn", 10, 280),    # Aries lagna lord, exalted, in 10th
        "Jupiter": _p("Cancer", 4, 95),       # exalted + benefic in 4th
        "Saturn": _p("Cancer", 6, 100),       # malefic in 6th
        "Moon": _p("Scorpio", 8, 220),        # debilitated Moon in 8th
    })
    result = analyze_bhava_vichara(chart)
    for a in result["bhava_assessments"]:
        assert len(a["reasons_en"]) == len(a["reasons_hi"]), (
            f"House {a['house']}: EN/HI reasons length mismatch "
            f"{len(a['reasons_en'])} vs {len(a['reasons_hi'])}"
        )


# ═══════════════════════════════════════════════════════════════
# House-lord computation
# ═══════════════════════════════════════════════════════════════

def test_house_lord_aries_lagna():
    chart = _aries_chart({})
    # Aries → Mars lord; 2nd = Taurus → Venus; 7th = Libra → Venus
    assert _house_lord(1, chart) == "Mars"
    assert _house_lord(2, chart) == "Venus"
    assert _house_lord(7, chart) == "Venus"
    assert _house_lord(10, chart) == "Saturn"  # Capricorn


def test_house_lord_cancer_lagna():
    chart = {"ascendant": {"sign": "Cancer"}, "planets": {}}
    assert _house_lord(1, chart) == "Moon"       # Cancer
    assert _house_lord(4, chart) == "Venus"      # Libra
    assert _house_lord(10, chart) == "Mars"      # Aries


# ═══════════════════════════════════════════════════════════════
# Destruction rules
# ═══════════════════════════════════════════════════════════════

def test_destruction_lord_in_dusthana():
    """Aries Lagna: 4th=Cancer → Moon. Place Moon in 6th → lord in dusthana → destruction."""
    chart = _aries_chart({
        "Moon": _p("Virgo", 6, 160),      # 4th lord in 6th (dusthana)
    })
    result = analyze_bhava_vichara(chart)
    b4 = next(a for a in result["bhava_assessments"] if a["house"] == 4)
    assert b4["destruction_risk"] is True
    assert b4["flourishing"] is False
    assert any("Dusthana" in r for r in b4["reasons_en"])


def test_destruction_multiple_malefics_aspect_no_benefic():
    """Malefics Sun + Saturn + Mars aspecting the same house with no benefic support."""
    chart = _aries_chart({
        "Sun": _p("Aries", 1, 10),          # in 1st aspects 7th
        "Saturn": _p("Gemini", 3, 70),      # in 3rd: 3rd aspect = 5th, 10th from 3 = 12th, 7th aspect = 9th. NOT 7th.
        "Mars": _p("Leo", 5, 130),          # in 5th aspects 11 (7th) & via 8-aspect = 12, via 4-aspect = 8
    })
    # Let's target a specific house instead — house 7 aspected by Sun (from 1st) + Saturn (from 4 via 10th aspect? no) + Mars
    # Simpler: House 7 aspected by Sun from 1 (7th aspect), Mars from 1 too, Saturn from 4 (10th aspect)
    chart = _aries_chart({
        "Sun": _p("Aries", 1, 10),        # aspects 7
        "Mars": _p("Aries", 1, 15),       # aspects 7 (universal 7th) AND 4,8 (specials)
        "Saturn": _p("Cancer", 4, 100),   # 3rd aspect=6, 10th aspect=1, 7th aspect=10. NOT 7.
    })
    # Mars in 1 aspects 4,7,8 — so house 7 has Sun + Mars malefic aspects. 2 malefics → destruction.
    # Ensure no benefics around house 7 (Libra) — lord Venus missing → no lord-in-dusthana trigger
    result = analyze_bhava_vichara(chart)
    b7 = next(a for a in result["bhava_assessments"] if a["house"] == 7)
    assert b7["destruction_risk"] is True
    # EN reason must mention multiple malefics
    assert any("malefic" in r.lower() for r in b7["reasons_en"])


def test_destruction_karaka_combust_and_afflicted():
    """Karaka of 9th = Jupiter. Place Jupiter combust (within 10° of Sun) AND afflicted (in 6/8/12)."""
    chart = _aries_chart({
        "Sun": _p("Capricorn", 10, 280),       # Sun longitude 280
        "Jupiter": _p("Capricorn", 10, 285),   # 5° from Sun = combust; debilitated in Capricorn
    })
    # Jupiter is combust and debilitated. That satisfies "combust AND afflicted".
    # Placing in 10th is not dusthana but debilitation is affliction per code.
    result = analyze_bhava_vichara(chart)
    b9 = next(a for a in result["bhava_assessments"] if a["house"] == 9)
    assert b9["destruction_risk"] is True
    assert any("combust" in r.lower() for r in b9["reasons_en"])


# ═══════════════════════════════════════════════════════════════
# Flourishing rules
# ═══════════════════════════════════════════════════════════════

def test_flourishing_lord_exalted_in_kendra():
    """Aries Lagna; lord Mars exalted (Capricorn) in 10th (Kendra) → Lagna flourishes."""
    chart = _aries_chart({
        "Mars": _p("Capricorn", 10, 280),
    })
    result = analyze_bhava_vichara(chart)
    b1 = next(a for a in result["bhava_assessments"] if a["house"] == 1)
    assert b1["flourishing"] is True
    assert b1["destruction_risk"] is False


def test_flourishing_benefic_occupant_still_flags():
    """Jupiter in 5th (own-ish territory); 5th lord absent. Benefic occupant → flourishing."""
    chart = _aries_chart({
        "Jupiter": _p("Leo", 5, 130),
    })
    result = analyze_bhava_vichara(chart)
    b5 = next(a for a in result["bhava_assessments"] if a["house"] == 5)
    assert b5["flourishing"] is True


# ═══════════════════════════════════════════════════════════════
# Karaka-as-Lagna narrative
# ═══════════════════════════════════════════════════════════════

def test_karaka_as_lagna_returns_bilingual_tuple():
    chart = _aries_chart({
        "Jupiter": _p("Cancer", 4, 95),
    })
    en, hi = _analyze_karaka_as_lagna("Jupiter", BHAVA_TOPIC_EN[2], BHAVA_TOPIC_HI[2], chart)
    assert isinstance(en, str) and en
    assert isinstance(hi, str) and hi
    assert "Karaka-as-Lagna" in en
    assert "कारक-से-लग्न" in hi


def test_karaka_as_lagna_marks_exalted():
    chart = _aries_chart({
        "Jupiter": _p("Cancer", 4, 95),    # exalted
    })
    en, hi = _analyze_karaka_as_lagna("Jupiter", "wealth", "धन", chart)
    assert "exalted" in en.lower()


def test_karaka_as_lagna_missing_karaka():
    chart = _aries_chart({})
    en, hi = _analyze_karaka_as_lagna("Jupiter", "wealth", "धन", chart)
    assert "not present" in en.lower()


def test_assessment_includes_karaka_as_lagna_narrative():
    chart = _aries_chart({
        "Venus": _p("Pisces", 12, 340),  # exalted in 12 — karaka of 7th
    })
    a7 = _assess_bhava(7, chart)
    assert "exalted" in a7["karaka_as_lagna_analysis_en"].lower()


# ═══════════════════════════════════════════════════════════════
# Overall strongest/weakest
# ═══════════════════════════════════════════════════════════════

def test_overall_lists_include_matching_houses():
    chart = _aries_chart({
        "Mars": _p("Capricorn", 10, 280),    # lagna-lord exalted in Kendra → 1 flourishes
        "Moon": _p("Virgo", 6, 160),         # 4th-lord in dusthana → 4 destroyed
    })
    result = analyze_bhava_vichara(chart)
    assert 1 in result["overall_strongest"]
    assert 4 in result["overall_weakest"]


# ═══════════════════════════════════════════════════════════════
# Defensive edge cases
# ═══════════════════════════════════════════════════════════════

def test_none_input_returns_12_houses():
    result = analyze_bhava_vichara(None)
    assert len(result["bhava_assessments"]) == 12
    assert result["sloka_ref"] == "Phaladeepika Adh. 15"


def test_empty_chart_returns_12_houses_with_no_flags():
    result = analyze_bhava_vichara({})
    assert len(result["bhava_assessments"]) == 12
    # No planets → nothing flourishes or is destroyed by occupancy/aspect
    # but also no ascendant → lord = "" → lord-in-dusthana check false
    assert result["overall_strongest"] == []
    assert result["overall_weakest"] == []


def test_sloka_ref_on_each_assessment():
    result = analyze_bhava_vichara(_aries_chart({}))
    for a in result["bhava_assessments"]:
        assert "Phaladeepika Adh. 15" in a["sloka_ref"]


# ═══════════════════════════════════════════════════════════════
# Helper sanity
# ═══════════════════════════════════════════════════════════════

def test_planet_aspects_house_seventh():
    assert _planet_aspects_house("Sun", 1, 7)
    assert _planet_aspects_house("Jupiter", 1, 5)   # 5th-aspect
    assert _planet_aspects_house("Jupiter", 1, 9)   # 9th-aspect
    assert not _planet_aspects_house("Sun", 1, 2)


def test_is_exalted_and_debilitated():
    assert _is_exalted("Sun", "Aries")
    assert _is_debilitated("Sun", "Libra")
    assert not _is_exalted("Sun", "Libra")
    assert not _is_debilitated("Sun", "")
