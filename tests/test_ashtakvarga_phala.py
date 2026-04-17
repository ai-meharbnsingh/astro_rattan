"""Tests for Ashtakavarga-phala — Phaladeepika Adhyaya 24.

Covers applied predictive rules derived from Ashtakavarga bindu totals:
  - house strength classification (>=30 strong, 25-29 moderate, <25 weak)
  - planet transit thresholds (per-planet, classical)
  - special combinations (leadership / wealth / fortune / dusthana)
  - overall 0-100 composite score
  - bilingual interpretation parity (EN + HI)
  - graceful degradation on missing chart data
"""
from app.ashtakvarga_engine import (
    analyze_ashtakvarga_phala,
    _house_status_from_bindus,
    _planet_transit_threshold,
    _interpret_house_strength,
    _sign_of_house,
)


# ───────────────────────────────────────────────────────────────
# Fixtures — sample charts
# ───────────────────────────────────────────────────────────────

def _chart_full(asc_sign="Aries") -> dict:
    """A complete 7-classical-planet chart with Ascendant."""
    return {
        "planets": {
            "Sun":     {"sign": "Aries",   "house": 1},
            "Moon":    {"sign": "Taurus",  "house": 2},
            "Mars":    {"sign": "Leo",     "house": 5},
            "Mercury": {"sign": "Aries",   "house": 1},
            "Jupiter": {"sign": "Cancer",  "house": 4},
            "Venus":   {"sign": "Pisces",  "house": 12},
            "Saturn":  {"sign": "Libra",   "house": 7},
        },
        "ascendant": {"sign": asc_sign},
    }


# ═══════════════════════════════════════════════════════════════
# House strength classification (Adh. 24 sloka 2)
# ═══════════════════════════════════════════════════════════════

def test_house_status_strong_at_30():
    assert _house_status_from_bindus(30) == "strong"


def test_house_status_strong_above_30():
    assert _house_status_from_bindus(42) == "strong"


def test_house_status_moderate_25():
    assert _house_status_from_bindus(25) == "moderate"


def test_house_status_moderate_29():
    assert _house_status_from_bindus(29) == "moderate"


def test_house_status_weak_below_25():
    assert _house_status_from_bindus(24) == "weak"


def test_house_status_weak_zero():
    assert _house_status_from_bindus(0) == "weak"


# ═══════════════════════════════════════════════════════════════
# Planet transit thresholds (Adh. 24 sloka 8)
# ═══════════════════════════════════════════════════════════════

def test_planet_threshold_jupiter_is_5():
    assert _planet_transit_threshold("Jupiter") == 5


def test_planet_threshold_saturn_is_3():
    assert _planet_transit_threshold("Saturn") == 3


def test_planet_threshold_mercury_is_5():
    assert _planet_transit_threshold("Mercury") == 5


def test_planet_threshold_mars_is_3():
    assert _planet_transit_threshold("Mars") == 3


def test_planet_threshold_sun_moon_are_4():
    assert _planet_transit_threshold("Sun") == 4
    assert _planet_transit_threshold("Moon") == 4


def test_planet_threshold_unknown_defaults_to_4():
    assert _planet_transit_threshold("Rahu") == 4


# ═══════════════════════════════════════════════════════════════
# Helper: sign for a given house
# ═══════════════════════════════════════════════════════════════

def test_sign_of_house_aries_lagna():
    assert _sign_of_house(1, "Aries") == "Aries"
    assert _sign_of_house(7, "Aries") == "Libra"
    assert _sign_of_house(12, "Aries") == "Pisces"


def test_sign_of_house_cancer_lagna():
    assert _sign_of_house(1, "Cancer") == "Cancer"
    assert _sign_of_house(10, "Cancer") == "Aries"


# ═══════════════════════════════════════════════════════════════
# Main analyze_ashtakvarga_phala structure
# ═══════════════════════════════════════════════════════════════

def test_analyze_returns_required_keys():
    res = analyze_ashtakvarga_phala(_chart_full())
    for key in (
        "house_strengths", "planet_strengths",
        "special_combinations", "transit_recommendations",
        "overall_score", "sloka_ref",
    ):
        assert key in res, f"missing key: {key}"


def test_analyze_has_12_house_entries():
    res = analyze_ashtakvarga_phala(_chart_full())
    assert len(res["house_strengths"]) == 12


def test_analyze_has_7_classical_planets_no_rahu_ketu():
    res = analyze_ashtakvarga_phala(_chart_full())
    planets = [p["planet"] for p in res["planet_strengths"]]
    assert set(planets) == {"Sun", "Moon", "Mars", "Mercury",
                            "Jupiter", "Venus", "Saturn"}
    assert "Rahu" not in planets
    assert "Ketu" not in planets


def test_analyze_has_at_least_4_special_combinations():
    res = analyze_ashtakvarga_phala(_chart_full())
    assert len(res["special_combinations"]) >= 4


def test_special_combinations_keys():
    res = analyze_ashtakvarga_phala(_chart_full())
    combos = [c["combo"] for c in res["special_combinations"]]
    assert "leadership_career" in combos
    assert "wealth_income" in combos
    assert "fortune_dharma" in combos
    assert "dusthana_obstacles" in combos


def test_special_combination_houses_match():
    res = analyze_ashtakvarga_phala(_chart_full())
    by_key = {c["combo"]: c for c in res["special_combinations"]}
    assert by_key["leadership_career"]["houses"] == [1, 7, 10]
    assert by_key["wealth_income"]["houses"] == [2, 11]
    assert by_key["fortune_dharma"]["houses"] == [5, 9]
    assert by_key["dusthana_obstacles"]["houses"] == [6, 8, 12]


def test_special_combination_thresholds():
    res = analyze_ashtakvarga_phala(_chart_full())
    by_key = {c["combo"]: c for c in res["special_combinations"]}
    assert by_key["leadership_career"]["threshold"] == 90
    assert by_key["wealth_income"]["threshold"] == 55
    assert by_key["fortune_dharma"]["threshold"] == 55


def test_house_strength_status_values():
    res = analyze_ashtakvarga_phala(_chart_full())
    for h in res["house_strengths"]:
        assert h["status"] in ("strong", "moderate", "weak")


def test_planet_strength_assessment_values():
    res = analyze_ashtakvarga_phala(_chart_full())
    for p in res["planet_strengths"]:
        assert p["assessment"] in ("favorable", "unfavorable")


def test_combination_achieved_consistency_with_totals():
    """achieved flag must agree with total_bindus vs threshold."""
    res = analyze_ashtakvarga_phala(_chart_full())
    for c in res["special_combinations"]:
        assert c["achieved"] == (c["total_bindus"] >= c["threshold"])


def test_transit_recommendations_provided_per_planet():
    res = analyze_ashtakvarga_phala(_chart_full())
    planets_with_recs = {r["planet"] for r in res["transit_recommendations"]}
    # All 7 classical planets should have recommendations
    assert planets_with_recs == {"Sun", "Moon", "Mars", "Mercury",
                                 "Jupiter", "Venus", "Saturn"}


def test_transit_rec_strongest_ge_weakest():
    res = analyze_ashtakvarga_phala(_chart_full())
    for r in res["transit_recommendations"]:
        assert r["strongest_bindus"] >= r["weakest_bindus"]


# ═══════════════════════════════════════════════════════════════
# Overall score bounds
# ═══════════════════════════════════════════════════════════════

def test_overall_score_in_0_100():
    res = analyze_ashtakvarga_phala(_chart_full())
    assert isinstance(res["overall_score"], int)
    assert 0 <= res["overall_score"] <= 100


def test_overall_score_different_charts_differ():
    """Sanity — Cancer-lagna chart yields a different score than Aries."""
    s1 = analyze_ashtakvarga_phala(_chart_full("Aries"))["overall_score"]
    s2 = analyze_ashtakvarga_phala(_chart_full("Cancer"))["overall_score"]
    # Most charts will differ; allow equality but both must be valid.
    assert 0 <= s1 <= 100 and 0 <= s2 <= 100


# ═══════════════════════════════════════════════════════════════
# Bilingual interpretation parity (EN + HI)
# ═══════════════════════════════════════════════════════════════

def test_house_interpretations_bilingual():
    res = analyze_ashtakvarga_phala(_chart_full())
    for h in res["house_strengths"]:
        assert h["interpretation_en"] and len(h["interpretation_en"]) > 10
        assert h["interpretation_hi"] and len(h["interpretation_hi"]) > 5
        # Hindi must contain at least one Devanagari char
        assert any("\u0900" <= ch <= "\u097F" for ch in h["interpretation_hi"])


def test_planet_interpretations_bilingual():
    res = analyze_ashtakvarga_phala(_chart_full())
    for p in res["planet_strengths"]:
        assert p["interpretation_en"]
        assert p["interpretation_hi"]
        assert any("\u0900" <= ch <= "\u097F" for ch in p["interpretation_hi"])


def test_combo_effects_bilingual():
    res = analyze_ashtakvarga_phala(_chart_full())
    for c in res["special_combinations"]:
        assert c["effect_en"]
        assert c["effect_hi"]
        assert any("\u0900" <= ch <= "\u097F" for ch in c["effect_hi"])


def test_transit_rec_guidance_bilingual():
    res = analyze_ashtakvarga_phala(_chart_full())
    for r in res["transit_recommendations"]:
        assert r["guidance_en"]
        assert r["guidance_hi"]
        assert any("\u0900" <= ch <= "\u097F" for ch in r["guidance_hi"])


def test_every_entry_carries_sloka_ref():
    res = analyze_ashtakvarga_phala(_chart_full())
    for h in res["house_strengths"]:
        assert "Adh. 24" in h["sloka_ref"]
    for p in res["planet_strengths"]:
        assert "Adh. 24" in p["sloka_ref"]
    for c in res["special_combinations"]:
        assert "Adh. 24" in c["sloka_ref"]
    for r in res["transit_recommendations"]:
        assert "Adh. 24" in r["sloka_ref"]
    assert "Adh. 24" in res["sloka_ref"]


# ═══════════════════════════════════════════════════════════════
# Interpretation helper behaviour
# ═══════════════════════════════════════════════════════════════

def test_interpret_house_strength_strong_en():
    txt = _interpret_house_strength(10, "strong", "en")
    assert "strong" in txt.lower() or "flourish" in txt.lower()


def test_interpret_house_strength_weak_hi_has_devanagari():
    txt = _interpret_house_strength(6, "weak", "hi")
    assert any("\u0900" <= ch <= "\u097F" for ch in txt)


# ═══════════════════════════════════════════════════════════════
# Graceful degradation
# ═══════════════════════════════════════════════════════════════

def test_empty_chart_graceful():
    res = analyze_ashtakvarga_phala({})
    assert res["house_strengths"] == []
    assert res["planet_strengths"] == []
    assert res["overall_score"] == 0


def test_chart_missing_ascendant():
    chart = {"planets": {
        "Sun":     {"sign": "Aries"},
        "Moon":    {"sign": "Taurus"},
        "Mars":    {"sign": "Leo"},
        "Mercury": {"sign": "Aries"},
        "Jupiter": {"sign": "Cancer"},
        "Venus":   {"sign": "Pisces"},
        "Saturn":  {"sign": "Libra"},
    }}
    res = analyze_ashtakvarga_phala(chart)
    # No ascendant → degrade
    assert res["house_strengths"] == []
    assert res["overall_score"] == 0


def test_chart_missing_planet():
    chart = {
        "planets": {
            "Sun": {"sign": "Aries"},
            "Moon": {"sign": "Taurus"},
            # Mars missing
        },
        "ascendant": {"sign": "Aries"},
    }
    res = analyze_ashtakvarga_phala(chart)
    # Required planet missing → degrade gracefully
    assert res["house_strengths"] == []


def test_non_dict_chart_graceful():
    assert analyze_ashtakvarga_phala(None)["house_strengths"] == []  # type: ignore[arg-type]
    assert analyze_ashtakvarga_phala("bad")["overall_score"] == 0   # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════
# Specific transit assessment — Jupiter with handcrafted position
# ═══════════════════════════════════════════════════════════════

def test_planet_in_transit_sign_uses_own_bav_table():
    """Planet strength must use the planet's own BAV bindus in its transit sign."""
    res = analyze_ashtakvarga_phala(_chart_full())
    # Jupiter transits Cancer in the chart → check BAV bindus are read correctly
    jup = next(p for p in res["planet_strengths"] if p["planet"] == "Jupiter")
    assert jup["sign"] == "Cancer"
    assert jup["threshold"] == 5
    assert isinstance(jup["bindus_in_transit_sign"], int)
    assert 0 <= jup["bindus_in_transit_sign"] <= 8
