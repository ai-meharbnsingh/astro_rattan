"""Tests for Vritti (Livelihood / Career) — Phaladeepika Adhyaya 5."""
from app.vritti_engine import (
    analyze_vritti,
    load_vritti_data,
    _navamsa_sign,
    _lord_of_tenth,
    _strongest_luminary,
    _sign_of_house,
    _ordinal,
)


PLANETS_ALL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
               "Saturn", "Rahu", "Ketu"]
HOUSES_ALL = [f"{i}st" if i == 1 else f"{i}nd" if i == 2 else f"{i}rd" if i == 3
              else f"{i}th" for i in range(1, 13)]


def _p(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {
        "sign": sign,
        "house": house,
        "longitude": longitude,
        "sign_degree": longitude % 30,
    }


# ═══════════════════════════════════════════════════════════════
# 1. Data file integrity
# ═══════════════════════════════════════════════════════════════

def test_data_file_loads_and_caches():
    data1 = load_vritti_data()
    data2 = load_vritti_data()
    assert data1 is data2
    assert "navamsa_vocations" in data1
    assert "tenth_lord_placements" in data1
    assert "strongest_luminary_effects" in data1


def test_navamsa_vocations_has_all_nine_planets():
    data = load_vritti_data()
    assert set(data["navamsa_vocations"].keys()) == set(PLANETS_ALL)


def test_tenth_lord_placements_covers_all_12_houses():
    data = load_vritti_data()
    assert set(data["tenth_lord_placements"].keys()) == set(HOUSES_ALL)


def test_strongest_luminary_has_three_keys():
    data = load_vritti_data()
    assert set(data["strongest_luminary_effects"].keys()) == {
        "Sun_strongest", "Moon_strongest", "Lagna_strongest"
    }


def test_navamsa_vocations_bilingual_parity():
    data = load_vritti_data()
    required = ("primary_en", "primary_hi", "secondary_en", "secondary_hi",
                "examples_en", "examples_hi", "sloka_ref")
    for planet in PLANETS_ALL:
        entry = data["navamsa_vocations"][planet]
        for key in required:
            assert key in entry, f"{planet} missing '{key}'"
            assert entry[key], f"{planet} has empty '{key}'"
        assert len(entry["examples_en"]) == len(entry["examples_hi"]), \
            f"{planet} examples en/hi length mismatch"


def test_tenth_lord_placements_bilingual():
    data = load_vritti_data()
    for h in HOUSES_ALL:
        entry = data["tenth_lord_placements"][h]
        for key in ("effect_en", "effect_hi", "sloka_ref"):
            assert key in entry and entry[key], f"House {h} missing '{key}'"


def test_strongest_luminary_bilingual():
    data = load_vritti_data()
    for k, entry in data["strongest_luminary_effects"].items():
        for key in ("implication_en", "implication_hi", "sloka_ref"):
            assert key in entry and entry[key], f"{k} missing '{key}'"


# ═══════════════════════════════════════════════════════════════
# 2. Helper functions
# ═══════════════════════════════════════════════════════════════

def test_ordinal_formatting():
    assert _ordinal(1) == "1st"
    assert _ordinal(2) == "2nd"
    assert _ordinal(3) == "3rd"
    for i in range(4, 13):
        assert _ordinal(i) == f"{i}th"


def test_navamsa_sign_aries_start():
    # Aries (fire) 0° → Aries navamsa (1st part starts from Aries)
    assert _navamsa_sign(0.0) == "Aries"
    # Aries 3°21' (just past part 1) → Taurus navamsa
    assert _navamsa_sign(3.35) == "Taurus"


def test_navamsa_sign_taurus_earth():
    # Taurus (earth) 0° → Capricorn navamsa
    assert _navamsa_sign(30.0) == "Capricorn"


def test_navamsa_sign_leo_fire():
    # Leo (fire) at 0° of Leo (=120°) → Aries navamsa
    assert _navamsa_sign(120.0) == "Aries"


def test_navamsa_sign_invalid_returns_empty():
    assert _navamsa_sign(None) == ""
    assert _navamsa_sign("not-a-number") == ""


def test_sign_of_house_whole_sign():
    chart = {"ascendant": {"sign": "Aries"}}
    assert _sign_of_house(chart, 1) == "Aries"
    assert _sign_of_house(chart, 10) == "Capricorn"
    assert _sign_of_house(chart, 12) == "Pisces"


def test_lord_of_tenth_aries_asc():
    """Aries ascendant → 10th sign = Capricorn → lord Saturn."""
    chart = {"ascendant": {"sign": "Aries"}, "planets": {}}
    assert _lord_of_tenth(chart) == "Saturn"


def test_lord_of_tenth_leo_asc():
    """Leo ascendant → 10th sign = Taurus → lord Venus."""
    chart = {"ascendant": {"sign": "Leo"}, "planets": {}}
    assert _lord_of_tenth(chart) == "Venus"


# ═══════════════════════════════════════════════════════════════
# 3. Luminary strength scoring
# ═══════════════════════════════════════════════════════════════

def test_exalted_sun_wins_over_debilitated_moon():
    """Sun exalted in Aries (1st), Moon debilitated in Scorpio (8th)."""
    chart = {
        "ascendant": {"sign": "Aries"},
        "planets": {
            "Sun": _p("Aries", 1, 5.0),           # exalted
            "Moon": _p("Scorpio", 8, 215.0),      # debilitated
            "Mars": _p("Aries", 1, 10.0),         # lagna lord in lagna
        },
    }
    lum = _strongest_luminary(chart)
    assert lum["strongest"] == "sun"
    assert lum["sun_score"] > lum["moon_score"]


def test_strong_moon_wins_when_sun_debilitated():
    chart = {
        "ascendant": {"sign": "Cancer"},
        "planets": {
            "Sun": _p("Libra", 4, 190.0),         # debilitated
            "Moon": _p("Taurus", 11, 35.0),       # exalted
            "Jupiter": _p("Pisces", 9, 340.0),    # lagna-lord of Cancer = Moon; Moon is already computed
        },
    }
    lum = _strongest_luminary(chart)
    assert lum["strongest"] == "moon"


def test_luminary_reasoning_bilingual():
    chart = {
        "ascendant": {"sign": "Aries"},
        "planets": {
            "Sun": _p("Aries", 1, 5.0),
            "Moon": _p("Taurus", 2, 35.0),
            "Mars": _p("Aries", 1, 10.0),
        },
    }
    lum = _strongest_luminary(chart)
    assert lum["reasoning_en"]
    assert lum["reasoning_hi"]
    assert "सूर्य" in lum["reasoning_hi"] or "चन्द्र" in lum["reasoning_hi"]


# ═══════════════════════════════════════════════════════════════
# 4. analyze_vritti — integration
# ═══════════════════════════════════════════════════════════════

def test_mars_10th_lord_in_leo_navamsa_maps_to_sun_vocation():
    """
    Aries ascendant → 10th sign Capricorn → 10th lord Saturn.
    Put Saturn at a longitude whose navamsa is Leo → navamsa lord Sun.
    Expected: primary vocation text drawn from Sun entry (medicine / metals).
    """
    # Compute a longitude whose navamsa sign is Leo.
    # Capricorn (earth) navamsa starts from Capricorn (0), then Aquarius, Pisces,
    # Aries, Taurus, Gemini, Cancer, Leo (=part 7), Virgo.
    # Capricorn begins at 270°. Each part = 30/9 = 3.333°.
    # Part 7 (0-indexed) starts at 270 + 7*3.333 = 270 + 23.333 = 293.333°.
    sat_lon = 293.8  # within Capricorn, part 7 → Leo navamsa
    chart = {
        "ascendant": {"sign": "Aries"},
        "planets": {
            "Sun":     _p("Aries", 1, 5.0),
            "Moon":    _p("Taurus", 2, 35.0),
            "Mars":    _p("Aries", 1, 10.0),
            "Mercury": _p("Gemini", 3, 65.0),
            "Jupiter": _p("Cancer", 4, 100.0),
            "Venus":   _p("Libra", 7, 190.0),
            "Saturn":  _p("Capricorn", 10, sat_lon),
            "Rahu":    _p("Leo", 5, 130.0),
            "Ketu":    _p("Aquarius", 11, 310.0),
        },
    }
    res = analyze_vritti(chart)
    assert res["tenth_lord_info"]["planet"] == "Saturn"
    assert res["tenth_lord_info"]["navamsa_sign"] == "Leo"
    assert res["tenth_lord_info"]["navamsa_lord"] == "Sun"
    # Primary vocation must come from Sun entry
    assert "medicine" in res["primary_vocation"]["vocation_en"].lower() or \
           "metal" in res["primary_vocation"]["vocation_en"].lower()
    # Hindi narrative present
    assert res["primary_vocation"]["vocation_hi"]
    assert res["primary_vocation"]["sloka_ref"]


def test_leo_asc_venus_tenth_lord_placement_effect():
    """
    Leo ascendant → 10th sign Taurus → 10th lord Venus.
    Place Venus in the 9th house → tenth-lord-in-9th effect attached.
    """
    chart = {
        "ascendant": {"sign": "Leo"},
        "planets": {
            "Sun":    _p("Leo", 1, 125.0),
            "Moon":   _p("Cancer", 12, 100.0),
            "Venus":  _p("Aries", 9, 8.0),     # 9th from Leo = Aries
            "Mars":   _p("Virgo", 2, 155.0),
            "Mercury":_p("Leo", 1, 128.0),
            "Jupiter":_p("Libra", 3, 190.0),
            "Saturn": _p("Capricorn", 6, 275.0),
            "Rahu":   _p("Gemini", 11, 70.0),
            "Ketu":   _p("Sagittarius", 5, 250.0),
        },
    }
    res = analyze_vritti(chart)
    assert res["tenth_lord_info"]["planet"] == "Venus"
    assert res["tenth_lord_info"]["placement_house"] == 9
    assert res["tenth_lord_info"]["placement_effect_en"]
    assert res["tenth_lord_info"]["placement_effect_hi"]
    # 9th-house text should mention Rajayoga / fortune
    low = res["tenth_lord_info"]["placement_effect_en"].lower()
    assert "rajayoga" in low or "fortunate" in low or "dharma" in low


def test_recommended_and_avoid_are_disjoint():
    chart = {
        "ascendant": {"sign": "Aries"},
        "planets": {
            "Sun":     _p("Aries", 1, 5.0),
            "Moon":    _p("Taurus", 2, 35.0),
            "Mars":    _p("Aries", 1, 10.0),
            "Mercury": _p("Gemini", 3, 65.0),
            "Jupiter": _p("Cancer", 4, 100.0),
            "Venus":   _p("Libra", 7, 190.0),
            "Saturn":  _p("Capricorn", 10, 280.0),
            "Rahu":    _p("Leo", 5, 130.0),
            "Ketu":    _p("Aquarius", 11, 310.0),
        },
    }
    res = analyze_vritti(chart)
    rec_en = set(res["recommended_fields_en"])
    avoid_en = set(res["avoid_fields_en"])
    assert rec_en.isdisjoint(avoid_en), \
        "recommended and avoid sets must not overlap"
    # Both should be non-empty
    assert rec_en
    assert avoid_en
    # Hindi lists also populated
    assert res["recommended_fields_hi"]
    assert res["avoid_fields_hi"]


def test_luminary_implication_present_for_strongest():
    chart = {
        "ascendant": {"sign": "Aries"},
        "planets": {
            "Sun":  _p("Aries", 1, 5.0),
            "Moon": _p("Scorpio", 8, 215.0),
            "Mars": _p("Aries", 1, 10.0),
        },
    }
    res = analyze_vritti(chart)
    lum = res["luminary_strength"]
    assert lum["strongest"] in {"sun", "moon", "lagna"}
    assert lum["implication_en"]
    assert lum["implication_hi"]


def test_output_has_top_level_sloka_ref():
    chart = {
        "ascendant": {"sign": "Aries"},
        "planets": {
            "Sun":  _p("Aries", 1, 5.0),
            "Moon": _p("Taurus", 2, 35.0),
            "Mars": _p("Aries", 1, 10.0),
            "Saturn": _p("Capricorn", 10, 280.0),
        },
    }
    res = analyze_vritti(chart)
    assert res["sloka_ref"] == "Phaladeepika Adh. 5"


def test_all_primary_vocation_fields_present():
    chart = {
        "ascendant": {"sign": "Aries"},
        "planets": {
            "Sun":  _p("Aries", 1, 5.0),
            "Moon": _p("Taurus", 2, 35.0),
            "Mars": _p("Aries", 1, 10.0),
            "Saturn": _p("Capricorn", 10, 280.0),
        },
    }
    res = analyze_vritti(chart)
    pv = res["primary_vocation"]
    for k in ("vocation_en", "vocation_hi", "derivation", "sloka_ref"):
        assert k in pv


# ═══════════════════════════════════════════════════════════════
# 5. Graceful degradation
# ═══════════════════════════════════════════════════════════════

def test_empty_chart_returns_safe_structure():
    res = analyze_vritti({})
    assert res["primary_vocation"]["vocation_en"] == ""
    assert res["tenth_lord_info"]["planet"] == ""
    assert res["recommended_fields_en"] == []
    assert res["avoid_fields_en"] == []
    assert res["sloka_ref"] == "Phaladeepika Adh. 5"


def test_none_input_returns_safe_structure():
    res = analyze_vritti(None)
    assert isinstance(res, dict)
    assert res["primary_vocation"]["vocation_en"] == ""


def test_malformed_chart_does_not_crash():
    res = analyze_vritti({"planets": "not-a-dict", "ascendant": None})
    assert isinstance(res, dict)
    assert res["sloka_ref"] == "Phaladeepika Adh. 5"


def test_chart_missing_ascendant_returns_structure():
    chart = {"planets": {"Sun": _p("Aries", 1, 5.0)}}
    res = analyze_vritti(chart)
    # Without ascendant, we cannot compute 10th lord.
    assert res["tenth_lord_info"]["planet"] == ""
    # But the structure stays valid
    assert "luminary_strength" in res
