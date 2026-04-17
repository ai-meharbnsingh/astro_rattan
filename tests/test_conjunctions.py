"""Tests for 45 two-planet conjunctions — Phaladeepika Adh. 18."""
import json
import os
from app.conjunction_engine import (
    detect_conjunctions,
    load_conjunction_data,
    _build_pair_index,
    _degree_separation,
)


def _p(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {"sign": sign, "house": house, "longitude": longitude, "sign_degree": longitude % 30}


# ═══════════════════════════════════════════════════════════════
# Data file integrity
# ═══════════════════════════════════════════════════════════════

def test_data_file_has_exactly_45_entries():
    data = load_conjunction_data()
    assert len(data) == 45


def test_data_file_unique_keys():
    data = load_conjunction_data()
    keys = [e["key"] for e in data]
    assert len(set(keys)) == 45


def test_all_entries_bilingual():
    data = load_conjunction_data()
    for e in data:
        for key in ("name_en", "name_hi", "effect_en", "effect_hi", "sloka_ref"):
            assert key in e, f"Entry {e.get('key')} missing {key}"


def test_data_includes_all_planet_planet_pairs():
    """9 base planets + Lagna → C(9,2)=36 planet-planet + 9 planet-Lagna = 45."""
    data = load_conjunction_data()
    planet_pairs = [e for e in data if "Lagna" not in e["planets"]]
    lagna_pairs = [e for e in data if "Lagna" in e["planets"]]
    assert len(planet_pairs) == 36
    assert len(lagna_pairs) == 9


def test_budhaditya_marked():
    data = load_conjunction_data()
    su_me = next(e for e in data if e["key"] == "sun_mercury")
    assert su_me["special_yoga"] == "Budhaditya"


def test_gajakesari_marked():
    data = load_conjunction_data()
    mo_ju = next(e for e in data if e["key"] == "moon_jupiter")
    assert mo_ju["special_yoga"] == "Gaja-Kesari"


# ═══════════════════════════════════════════════════════════════
# Helper tests
# ═══════════════════════════════════════════════════════════════

def test_degree_separation():
    assert _degree_separation(10, 12) == 2
    assert _degree_separation(358, 2) == 4   # wrap-around
    assert _degree_separation(0, 180) == 180
    assert _degree_separation(170, 200) == 30


def test_pair_index_contains_all_pairs():
    index = _build_pair_index()
    assert len(index) == 45
    assert frozenset(["Sun", "Mercury"]) in index
    assert frozenset(["Moon", "Jupiter"]) in index
    assert frozenset(["Saturn", "Rahu"]) in index
    assert frozenset(["Sun", "Lagna"]) in index


# ═══════════════════════════════════════════════════════════════
# Orb detection
# ═══════════════════════════════════════════════════════════════

def test_conjunct_planets_within_orb():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 10.0),
            "Mercury": _p("Aries", 1, 13.0),   # 3° from Sun — conjunct
        },
    }
    r = detect_conjunctions(chart)
    keys = {c["key"] for c in r}
    assert "sun_mercury" in keys


def test_not_conjunct_when_beyond_orb():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 5.0),
            "Mercury": _p("Aries", 1, 16.0),   # 11° — beyond default 8° orb
        },
    }
    r = detect_conjunctions(chart)
    keys = {c["key"] for c in r}
    assert "sun_mercury" not in keys


def test_not_conjunct_across_signs():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 29.0),
            "Mercury": _p("Taurus", 2, 31.0),   # only 2° apart but different signs
        },
    }
    r = detect_conjunctions(chart)
    assert not any(c["key"] == "sun_mercury" for c in r)


def test_custom_orb():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 5.0),
            "Mercury": _p("Aries", 1, 12.0),   # 7° — within 8° but not within 5°
        },
    }
    assert any(c["key"] == "sun_mercury" for c in detect_conjunctions(chart, orb_degrees=8))
    assert not any(c["key"] == "sun_mercury" for c in detect_conjunctions(chart, orb_degrees=5))


# ═══════════════════════════════════════════════════════════════
# Multi-pair detection
# ═══════════════════════════════════════════════════════════════

def test_triple_conjunction_reports_three_pairs():
    # Sun + Mercury + Jupiter all in Aries within 8°
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 5.0),
            "Mercury": _p("Aries", 1, 8.0),
            "Jupiter": _p("Aries", 1, 12.0),
        },
    }
    r = detect_conjunctions(chart)
    keys = {c["key"] for c in r}
    assert "sun_mercury" in keys
    assert "sun_jupiter" in keys
    assert "mercury_jupiter" in keys


def test_conjunction_picks_up_budhaditya_special_yoga():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 10),
            "Mercury": _p("Aries", 1, 12),
        },
    }
    r = detect_conjunctions(chart)
    budh = next(c for c in r if c["key"] == "sun_mercury")
    assert budh["special_yoga"] == "Budhaditya"
    assert budh["nature"] == "benefic"


def test_enhanced_flag_in_kendra():
    # Sun-Mars in 10th (Kendra) — should mark enhanced=True
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":  _p("Capricorn", 10, 280),
            "Mars": _p("Capricorn", 10, 282),
        },
    }
    r = detect_conjunctions(chart)
    s_m = next(c for c in r if c["key"] == "sun_mars")
    assert s_m["enhanced"] is True


# ═══════════════════════════════════════════════════════════════
# Lagna-planet conjunctions
# ═══════════════════════════════════════════════════════════════

def test_moon_lagna_conjunction():
    chart = {
        "ascendant": {"sign": "Cancer", "longitude": 90},
        "planets": {
            "Moon": _p("Cancer", 1, 95),
        },
    }
    r = detect_conjunctions(chart)
    keys = {c["key"] for c in r}
    assert "moon_lagna" in keys
    ml = next(c for c in r if c["key"] == "moon_lagna")
    assert "Lagna" in ml["planets"]


def test_planet_in_other_house_not_lagna_conjunction():
    chart = {
        "ascendant": {"sign": "Cancer", "longitude": 90},
        "planets": {
            "Moon": _p("Taurus", 11, 35),   # in 11th, not Lagna
        },
    }
    r = detect_conjunctions(chart)
    assert not any(c["key"] == "moon_lagna" for c in r)


def test_lagna_conjunction_different_sign_rejected():
    # Planet in house 1 but sign doesn't match ascendant — still rejected
    chart = {
        "ascendant": {"sign": "Cancer", "longitude": 90},
        "planets": {
            "Sun": _p("Leo", 1, 130),   # different sign from Cancer ascendant
        },
    }
    r = detect_conjunctions(chart)
    assert not any(c["key"] == "sun_lagna" for c in r)


# ═══════════════════════════════════════════════════════════════
# Base pairs — quick smoke test each of 10 planets involved
# ═══════════════════════════════════════════════════════════════

def test_all_major_pairs_recognizable():
    # Build a chart with everyone stacked in Aries — exaggerated but verifies data coverage
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 4),
            "Moon":    _p("Aries", 1, 6),
            "Mars":    _p("Aries", 1, 8),
            "Mercury": _p("Aries", 1, 10),
            "Jupiter": _p("Aries", 1, 9),
            "Venus":   _p("Aries", 1, 7),
            "Saturn":  _p("Aries", 1, 5),
        },
    }
    r = detect_conjunctions(chart)
    keys = {c["key"] for c in r}
    # All C(7,2)=21 planet-planet + 7 planet-Lagna = 28 conjunctions
    for expected in (
        "sun_moon", "sun_mars", "sun_mercury", "sun_jupiter", "sun_venus", "sun_saturn",
        "moon_mars", "moon_mercury", "moon_jupiter", "moon_venus", "moon_saturn",
        "mars_mercury", "mars_jupiter", "mars_venus", "mars_saturn",
        "mercury_jupiter", "mercury_venus", "mercury_saturn",
        "jupiter_venus", "jupiter_saturn", "venus_saturn",
        "sun_lagna", "moon_lagna", "mars_lagna", "mercury_lagna",
        "jupiter_lagna", "venus_lagna", "saturn_lagna",
    ):
        assert expected in keys, f"Missing {expected}"


def test_node_pairs_recognizable():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":  _p("Leo", 5, 130),
            "Rahu": _p("Leo", 5, 133),
        },
    }
    r = detect_conjunctions(chart)
    assert any(c["key"] == "sun_rahu" for c in r)


def test_jupiter_rahu_guru_chandal():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Jupiter": _p("Leo", 5, 130),
            "Rahu":    _p("Leo", 5, 132),
        },
    }
    r = detect_conjunctions(chart)
    jr = next(c for c in r if c["key"] == "jupiter_rahu")
    assert jr["special_yoga"] == "Guru-Chandal"


# ═══════════════════════════════════════════════════════════════
# Graceful degradation
# ═══════════════════════════════════════════════════════════════

def test_empty_chart():
    assert detect_conjunctions({}) == []


def test_none_input():
    assert detect_conjunctions(None) == []


def test_missing_sign():
    chart = {
        "ascendant": {"sign": "", "longitude": 0},
        "planets": {
            "Sun": {"house": 1, "longitude": 5},   # no sign field
            "Moon": _p("Aries", 1, 6),
        },
    }
    # Should not crash; may return empty
    r = detect_conjunctions(chart)
    assert isinstance(r, list)


def test_sorting_stable():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 5),
            "Mercury": _p("Aries", 1, 7),   # closer
            "Jupiter": _p("Virgo", 6, 160),
            "Venus":   _p("Virgo", 6, 165),
        },
    }
    r = detect_conjunctions(chart)
    houses = [c["house"] for c in r]
    assert houses == sorted(houses)
