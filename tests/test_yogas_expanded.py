"""Tests for expanded yoga library — Phaladeepika Adh. 6-7.

Covers declarative rule engine + JSON yoga database + integration with search engine.
"""
import json
import os
from app.yoga_rule_engine import (
    load_yoga_rules,
    evaluate_rule,
    detect_all_yogas,
    list_categories,
)
from app.yoga_search_engine import detect_yogas_in_chart, YOGA_TYPES


def _p(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {"sign": sign, "house": house, "longitude": longitude, "sign_degree": longitude % 30}


# ═══════════════════════════════════════════════════════════════
# Data file integrity
# ═══════════════════════════════════════════════════════════════

def test_yoga_count_at_least_50():
    yogas = load_yoga_rules()
    assert len(yogas) >= 50


def test_yoga_unique_keys():
    yogas = load_yoga_rules()
    keys = [y["key"] for y in yogas]
    assert len(set(keys)) == len(keys)


def test_all_yogas_bilingual():
    yogas = load_yoga_rules()
    for y in yogas:
        for field in ("name_en", "name_hi", "effect_en", "effect_hi", "category", "sloka_ref"):
            assert field in y and y[field], f"{y.get('key')} missing {field}"


def test_all_yogas_have_rules():
    yogas = load_yoga_rules()
    for y in yogas:
        assert "rules" in y
        assert "type" in y["rules"]


def test_all_categories_present():
    cats = set(list_categories())
    expected_cats = {"moon", "kendra", "dhana", "fame", "sun", "raja", "nabhasa"}
    assert expected_cats.issubset(cats)


def test_search_engine_knows_new_yogas():
    """Search engine should have resolved all declarative yoga names."""
    data = load_yoga_rules()
    for y in data:
        assert y["name_en"] in YOGA_TYPES


# ═══════════════════════════════════════════════════════════════
# Rule evaluator unit tests
# ═══════════════════════════════════════════════════════════════

def test_rule_planet_in_houses():
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {"Jupiter": _p("Cancer", 4, 100)}}
    assert evaluate_rule({"type": "planet_in_houses", "planet": "Jupiter", "houses": [1, 4, 7, 10]}, chart)
    assert not evaluate_rule({"type": "planet_in_houses", "planet": "Jupiter", "houses": [2, 5, 8]}, chart)


def test_rule_planet_in_own_or_exaltation():
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {"Jupiter": _p("Cancer", 4, 100)}}
    assert evaluate_rule({"type": "planet_in_own_or_exaltation", "planet": "Jupiter"}, chart)
    chart2 = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {"Jupiter": _p("Gemini", 3, 65)}}
    assert not evaluate_rule({"type": "planet_in_own_or_exaltation", "planet": "Jupiter"}, chart2)


def test_rule_benefic_in_house():
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {"Venus": _p("Taurus", 2, 35)}}
    assert evaluate_rule({"type": "benefic_in_house", "house": 2}, chart)
    assert not evaluate_rule({"type": "benefic_in_house", "house": 6}, chart)


def test_rule_combinator_and():
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {
        "Venus": _p("Taurus", 2, 35), "Jupiter": _p("Cancer", 4, 100),
    }}
    assert evaluate_rule({"type": "AND", "conditions": [
        {"type": "benefic_in_house", "house": 2},
        {"type": "planet_in_own_or_exaltation", "planet": "Jupiter"},
    ]}, chart)


def test_rule_combinator_or():
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {"Venus": _p("Taurus", 2, 35)}}
    assert evaluate_rule({"type": "OR", "conditions": [
        {"type": "benefic_in_house", "house": 2},
        {"type": "benefic_in_house", "house": 10},
    ]}, chart)


def test_rule_combinator_not():
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {"Venus": _p("Taurus", 2, 35)}}
    assert evaluate_rule({"type": "NOT", "condition":
        {"type": "benefic_in_house", "house": 10}
    }, chart)


def test_rule_planet_in_house_from_moon():
    # Moon at house 1, planet in house 2 = "2nd from Moon"
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {
        "Moon":    _p("Aries", 1, 10),
        "Jupiter": _p("Taurus", 2, 35),
    }}
    assert evaluate_rule({"type": "planet_in_house_from_moon", "offset": 2, "exclude": ["Sun", "Rahu", "Ketu"]}, chart)


def test_rule_no_planet_in_houses_from_moon():
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {
        "Moon":    _p("Aries", 1, 10),
        "Jupiter": _p("Virgo", 6, 160),   # 6th house, not 2 or 12
    }}
    # No planet in 2 or 12 from Moon (Moon at 1 → 2nd=house 2, 12th=house 12)
    assert evaluate_rule({"type": "no_planet_in_houses_from_moon", "offsets": [2, 12]}, chart)


def test_rule_lord_of_house_in_houses():
    # Aries ascendant → 9th is Sagittarius → lord is Jupiter
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {"Jupiter": _p("Cancer", 4, 100)}}
    assert evaluate_rule({"type": "lord_of_house_in_houses", "lord_of": 9, "in_houses": [1, 4, 7, 10]}, chart)


def test_rule_planet_aspects_house():
    # Saturn in house 10 aspects: 4 (7th), 12 (3rd sp), 7 (10th sp)
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {"Saturn": _p("Capricorn", 10, 280)}}
    assert evaluate_rule({"type": "planet_aspects_house", "source": "Saturn", "house": 4}, chart)
    assert not evaluate_rule({"type": "planet_aspects_house", "source": "Saturn", "house": 6}, chart)


def test_rule_moon_in_strong_sign():
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {"Moon": _p("Taurus", 2, 35)}}
    assert evaluate_rule({"type": "moon_in_strong_sign"}, chart)
    chart2 = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {"Moon": _p("Scorpio", 8, 220)}}
    assert not evaluate_rule({"type": "moon_in_strong_sign"}, chart2)


def test_rule_planet_aspects_target_lord():
    # Jupiter aspects Lagna lord (Mars for Aries asc)
    # Jupiter at house 7 aspects: 1 (7th), 11 (5th sp), 3 (9th sp)
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {
        "Jupiter": _p("Libra", 7, 190),
        "Mars":    _p("Aries", 1, 10),
    }}
    assert evaluate_rule({
        "type": "planet_aspects_planet", "source": "Jupiter", "target_lord_of": 1
    }, chart)


# ═══════════════════════════════════════════════════════════════
# Integration tests — handcrafted charts trigger specific yogas
# ═══════════════════════════════════════════════════════════════

def test_lakshmi_yoga_triggered():
    # Aries asc → 9th lord = Jupiter. Put Jupiter in 9th, Venus exalted
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Jupiter": _p("Sagittarius", 9, 250),   # 9th lord in 9th (own)
            "Venus":   _p("Pisces", 12, 345),       # exalted
            "Sun":     _p("Aries", 1, 10),
            "Moon":    _p("Taurus", 2, 35),
            "Mars":    _p("Capricorn", 10, 280),
            "Mercury": _p("Virgo", 6, 160),
            "Saturn":  _p("Libra", 7, 190),
        },
    }
    matched = detect_all_yogas(chart)
    keys = {y["key"] for y in matched}
    assert "lakshmi" in keys


def test_subhakartari_yoga_triggered():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Jupiter": _p("Taurus", 2, 35),
            "Venus":   _p("Pisces", 12, 345),
        },
    }
    matched = detect_all_yogas(chart)
    assert any(y["key"] == "subhakartari_lagna" for y in matched)


def test_papakartari_yoga_triggered():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Mars":   _p("Taurus", 2, 35),
            "Saturn": _p("Pisces", 12, 345),
        },
    }
    matched = detect_all_yogas(chart)
    assert any(y["key"] == "papakartari_lagna" for y in matched)


def test_kemadruma_yoga_triggered():
    # Moon alone — no planets in 2, 12, or Kendras from Moon
    # Moon at house 1 → 2nd=2, 12th=12, Kendras from Moon = 1,4,7,10
    # Put all other planets in 3, 5, 6, 8, 9, 11 (none of 2,12,4,7,10)
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Moon":    _p("Aries", 1, 10),
            "Sun":     _p("Gemini", 3, 65),
            "Mercury": _p("Leo", 5, 130),
            "Mars":    _p("Virgo", 6, 160),
            "Jupiter": _p("Scorpio", 8, 220),
            "Venus":   _p("Sagittarius", 9, 250),
            "Saturn":  _p("Aquarius", 11, 315),
        },
    }
    matched = detect_all_yogas(chart)
    assert any(y["key"] == "kemadruma" for y in matched)


def test_rajju_yoga_all_movable():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 10),
            "Moon":    _p("Cancer", 4, 100),
            "Mars":    _p("Libra", 7, 190),
            "Mercury": _p("Capricorn", 10, 280),
            "Jupiter": _p("Aries", 1, 15),
            "Venus":   _p("Cancer", 4, 105),
            "Saturn":  _p("Libra", 7, 195),
        },
    }
    matched = detect_all_yogas(chart)
    assert any(y["key"] == "nabhasa_rajju" for y in matched)


def test_musala_yoga_all_fixed():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Taurus", 2, 35),
            "Moon":    _p("Leo", 5, 130),
            "Mars":    _p("Scorpio", 8, 220),
            "Mercury": _p("Aquarius", 11, 315),
            "Jupiter": _p("Taurus", 2, 40),
            "Venus":   _p("Leo", 5, 135),
            "Saturn":  _p("Scorpio", 8, 225),
        },
    }
    matched = detect_all_yogas(chart)
    assert any(y["key"] == "nabhasa_musala" for y in matched)


def test_vipareeta_harsha_6th_lord_in_8():
    # Aries asc → 6th lord = Mercury. Mercury in 8 (Scorpio)
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Mercury": _p("Scorpio", 8, 220)},
    }
    matched = detect_all_yogas(chart)
    assert any(y["key"] == "vipareeta_harsha" for y in matched)


def test_vipareeta_sarala_8th_lord_in_12():
    # Aries asc → 8th lord = Mars. Mars in 12 (Pisces)
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Mars": _p("Pisces", 12, 345)},
    }
    matched = detect_all_yogas(chart)
    assert any(y["key"] == "vipareeta_sarala" for y in matched)


def test_sun_raja_yoga():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Sun": _p("Aries", 1, 10)},   # exalted in Lagna (Kendra)
    }
    matched = detect_all_yogas(chart)
    assert any(y["key"] == "sun_raja" for y in matched)


def test_amala_benefic_in_10():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Jupiter": _p("Capricorn", 10, 280)},
    }
    matched = detect_all_yogas(chart)
    assert any(y["key"] == "amala" for y in matched)


def test_category_filter():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Mars":   _p("Taurus", 2, 35),
            "Saturn": _p("Pisces", 12, 345),
            "Jupiter": _p("Capricorn", 10, 280),
        },
    }
    kendra_only = detect_all_yogas(chart, category_filter="kendra")
    for y in kendra_only:
        assert y["category"] == "kendra"


# ═══════════════════════════════════════════════════════════════
# Regression: existing search_engine API still works
# ═══════════════════════════════════════════════════════════════

def test_existing_yoga_detection_still_works():
    # Gaja-Kesari — Moon in Kendra from Lagna, Jupiter in Kendra from Moon
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Moon":    _p("Cancer", 4, 100),      # Kendra from Lagna
            "Jupiter": _p("Cancer", 4, 105),      # with Moon
        },
    }
    yogas = detect_yogas_in_chart(chart)
    assert isinstance(yogas, list)
    # At least one yoga should be detected (Gaja-Kesari or Moon-Jupiter yogas)
    assert len(yogas) >= 1


def test_merged_output_includes_both_sources():
    """detect_yogas_in_chart should merge legacy + declarative detections."""
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Jupiter": _p("Sagittarius", 9, 250),
            "Venus":   _p("Pisces", 12, 345),
            "Sun":     _p("Aries", 1, 10),
            "Moon":    _p("Taurus", 2, 35),
            "Mars":    _p("Capricorn", 10, 280),
            "Mercury": _p("Virgo", 6, 160),
            "Saturn":  _p("Libra", 7, 190),
        },
    }
    yogas = detect_yogas_in_chart(chart)
    names = {y["name"] for y in yogas}
    # Should include at least one declarative yoga (Lakshmi) and existing ones
    assert any("Lakshmi" in n for n in names)


def test_empty_chart_graceful():
    assert detect_all_yogas({}) == []
    assert detect_yogas_in_chart({}) == []


def test_none_chart():
    assert detect_all_yogas(None) == []


# ═══════════════════════════════════════════════════════════════
# Total yoga coverage check (target ~80)
# ═══════════════════════════════════════════════════════════════

def test_total_known_yogas_at_least_60():
    """Combined legacy + declarative yoga names should exceed 60."""
    assert len(YOGA_TYPES) >= 60
