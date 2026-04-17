"""Tests for Pravrajya (ascetic) yogas — Phaladeepika Adh. 27."""
from app.pravrajya_engine import (
    detect_pravrajya,
    _planets_in_sign,
    _is_drekkana,
)


def _mkplanet(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {"sign": sign, "house": house, "longitude": longitude, "sign_degree": longitude % 30}


# ═══════════════════════════════════════════════════════════════
# Helper tests
# ═══════════════════════════════════════════════════════════════

def test_planets_in_sign():
    planets = {
        "Sun": _mkplanet("Aries", 1),
        "Mars": _mkplanet("Aries", 1),
        "Moon": _mkplanet("Taurus", 2),
    }
    assert sorted(_planets_in_sign(planets, "Aries")) == ["Mars", "Sun"]
    assert _planets_in_sign(planets, "Taurus") == ["Moon"]
    assert _planets_in_sign(planets, "Gemini") == []


def test_is_drekkana_capricorn():
    # Capricorn spans 270-300 absolute longitude
    # 1st drekkana: 270-280, 2nd: 280-290, 3rd: 290-300
    assert _is_drekkana(275.0, 1, "Capricorn") is True
    assert _is_drekkana(285.0, 2, "Capricorn") is True
    assert _is_drekkana(295.0, 3, "Capricorn") is True
    assert _is_drekkana(275.0, 2, "Capricorn") is False
    assert _is_drekkana(100.0, 1, "Capricorn") is False   # not in sign
    assert _is_drekkana(285.0, 2, "Aquarius") is False    # wrong sign


def test_is_drekkana_invalid():
    assert _is_drekkana(100.0, 1, "NotASign") is False
    assert _is_drekkana("bad", 1, "Aries") is False


# ═══════════════════════════════════════════════════════════════
# Per-yoga detection tests
# ═══════════════════════════════════════════════════════════════

def test_paramahamsa_detected():
    # 4 planets (Sun, Jupiter, Mars, Venus) in Aries (Lagna — Kendra)
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 5),
            "Jupiter": _mkplanet("Aries", 1, 12),
            "Mars":    _mkplanet("Aries", 1, 18),
            "Venus":   _mkplanet("Aries", 1, 25),
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mercury": _mkplanet("Gemini", 3, 65),
            "Saturn":  _mkplanet("Cancer", 4, 100),
            "Rahu":    _mkplanet("Leo", 5, 130),
            "Ketu":    _mkplanet("Aquarius", 11, 310),
        },
    }
    r = detect_pravrajya(chart)
    keys = {y["key"] for y in r["yogas_found"]}
    assert "paramahamsa" in keys
    yoga = next(y for y in r["yogas_found"] if y["key"] == "paramahamsa")
    assert yoga["strength"] >= 5
    assert "name_hi" in yoga and yoga["name_hi"] == "परमहंस"
    assert yoga["sloka_ref"] == "Phaladeepika Adh. 27 sloka 1"


def test_paramahamsa_not_in_kendra():
    # 4 planets in one sign but that sign is NOT in a Kendra → no Paramahamsa
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Gemini", 3, 65),
            "Jupiter": _mkplanet("Gemini", 3, 70),
            "Mars":    _mkplanet("Gemini", 3, 75),
            "Venus":   _mkplanet("Gemini", 3, 80),
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mercury": _mkplanet("Aries", 1, 5),
            "Saturn":  _mkplanet("Cancer", 4, 100),
            "Rahu":    _mkplanet("Leo", 5, 130),
            "Ketu":    _mkplanet("Aquarius", 11, 310),
        },
    }
    r = detect_pravrajya(chart)
    assert not any(y["key"] == "paramahamsa" for y in r["yogas_found"])


def test_sannyasi_detected():
    # Moon in Capricorn 2nd drekkana (10-20 within sign → abs 280-290),
    # Saturn aspects Moon: Saturn at house 10, aspects 7th (4th house) AND 3rd/10th specials.
    # Put Saturn 7 houses from Moon so 7th aspect hits Moon.
    # Let Moon be in house 4 (Capricorn if asc=Libra), Saturn in house 10 (Cancer → aspects 4th via 7th).
    chart = {
        "ascendant": {"sign": "Libra", "longitude": 180},
        "planets": {
            "Moon":    _mkplanet("Capricorn", 4, 285),   # 2nd drekkana of Capricorn
            "Saturn":  _mkplanet("Cancer", 10, 100),     # 7th aspect → house 4 (Moon)
            "Sun":     _mkplanet("Aries", 7, 5),
            "Mars":    _mkplanet("Taurus", 8, 35),
            "Mercury": _mkplanet("Gemini", 9, 65),
            "Jupiter": _mkplanet("Leo", 11, 130),
            "Venus":   _mkplanet("Virgo", 12, 160),
            "Rahu":    _mkplanet("Pisces", 6, 345),
            "Ketu":    _mkplanet("Virgo", 12, 165),
        },
    }
    r = detect_pravrajya(chart)
    keys = {y["key"] for y in r["yogas_found"]}
    assert "sannyasi" in keys
    yoga = next(y for y in r["yogas_found"] if y["key"] == "sannyasi")
    assert yoga["name_hi"] == "संन्यासी"


def test_tridandi_detected():
    # Jupiter in Lagna (house 1), Saturn aspects house 1.
    # Saturn in house 7 → 7th aspect hits house 1.
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Jupiter": _mkplanet("Aries", 1, 12),
            "Saturn":  _mkplanet("Libra", 7, 190),  # 7th aspect → house 1
            "Sun":     _mkplanet("Taurus", 2, 35),
            "Moon":    _mkplanet("Gemini", 3, 65),
            "Mars":    _mkplanet("Cancer", 4, 100),
            "Mercury": _mkplanet("Leo", 5, 130),
            "Venus":   _mkplanet("Virgo", 6, 160),
            "Rahu":    _mkplanet("Scorpio", 8, 220),
            "Ketu":    _mkplanet("Taurus", 2, 50),
        },
    }
    r = detect_pravrajya(chart)
    keys = {y["key"] for y in r["yogas_found"]}
    assert "tridandi" in keys


def test_bhrugukachcha_detected():
    # Sun, Mars, Saturn all in Kendras/Trikonas
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 5),       # Kendra
            "Mars":    _mkplanet("Leo", 5, 130),       # Trikona
            "Saturn":  _mkplanet("Libra", 7, 190),     # Kendra
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mercury": _mkplanet("Gemini", 3, 65),
            "Jupiter": _mkplanet("Virgo", 6, 160),
            "Venus":   _mkplanet("Scorpio", 8, 220),
            "Rahu":    _mkplanet("Sagittarius", 9, 250),
            "Ketu":    _mkplanet("Gemini", 3, 80),
        },
    }
    r = detect_pravrajya(chart)
    keys = {y["key"] for y in r["yogas_found"]}
    assert "bhrugukachcha" in keys


def test_bhrugukachcha_rejected_when_one_not_in_kendra():
    # Saturn in house 3 (not Kendra/Trikona) → rejected
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 5),
            "Mars":    _mkplanet("Leo", 5, 130),
            "Saturn":  _mkplanet("Gemini", 3, 65),   # Dusthana (for this purpose, not Kendra)
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mercury": _mkplanet("Gemini", 3, 70),
            "Jupiter": _mkplanet("Virgo", 6, 160),
            "Venus":   _mkplanet("Scorpio", 8, 220),
            "Rahu":    _mkplanet("Sagittarius", 9, 250),
            "Ketu":    _mkplanet("Gemini", 3, 80),
        },
    }
    r = detect_pravrajya(chart)
    assert not any(y["key"] == "bhrugukachcha" for y in r["yogas_found"])


def test_vanaprastha_detected():
    # 4 planets in Lagna
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 5),
            "Mercury": _mkplanet("Aries", 1, 12),
            "Venus":   _mkplanet("Aries", 1, 18),
            "Mars":    _mkplanet("Aries", 1, 25),
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Jupiter": _mkplanet("Gemini", 3, 65),
            "Saturn":  _mkplanet("Cancer", 4, 100),
            "Rahu":    _mkplanet("Leo", 5, 130),
            "Ketu":    _mkplanet("Aquarius", 11, 310),
        },
    }
    r = detect_pravrajya(chart)
    keys = {y["key"] for y in r["yogas_found"]}
    assert "vanaprastha" in keys


def test_vriddhasravaka_detected():
    # Moon + Mars in same house (3), Saturn aspects house 3
    # Saturn at house 9 → 7th aspect = house 3
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Moon":    _mkplanet("Gemini", 3, 65),
            "Mars":    _mkplanet("Gemini", 3, 70),
            "Saturn":  _mkplanet("Sagittarius", 9, 250),   # 7th aspect → house 3
            "Sun":     _mkplanet("Aries", 1, 5),
            "Mercury": _mkplanet("Taurus", 2, 35),
            "Jupiter": _mkplanet("Cancer", 4, 100),
            "Venus":   _mkplanet("Leo", 5, 130),
            "Rahu":    _mkplanet("Virgo", 6, 160),
            "Ketu":    _mkplanet("Pisces", 12, 345),
        },
    }
    r = detect_pravrajya(chart)
    keys = {y["key"] for y in r["yogas_found"]}
    assert "vriddhasravaka" in keys


def test_charaka_detected():
    # Ketu in Lagna + Moon debilitated (Scorpio) + in Dusthana (8th)
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Ketu":    _mkplanet("Aries", 1, 10),
            "Moon":    _mkplanet("Scorpio", 8, 220),       # debilitated + Dusthana
            "Sun":     _mkplanet("Taurus", 2, 35),
            "Mars":    _mkplanet("Gemini", 3, 65),
            "Mercury": _mkplanet("Cancer", 4, 100),
            "Jupiter": _mkplanet("Leo", 5, 130),
            "Venus":   _mkplanet("Virgo", 6, 160),
            "Saturn":  _mkplanet("Libra", 7, 190),
            "Rahu":    _mkplanet("Libra", 7, 195),
        },
    }
    r = detect_pravrajya(chart)
    keys = {y["key"] for y in r["yogas_found"]}
    assert "charaka" in keys
    yoga = next(y for y in r["yogas_found"] if y["key"] == "charaka")
    assert yoga["strength"] >= 6


# ═══════════════════════════════════════════════════════════════
# Normal chart should trigger ZERO yogas
# ═══════════════════════════════════════════════════════════════

def test_normal_chart_no_yogas():
    # Scattered planets — no ascetic patterns
    chart = {
        "ascendant": {"sign": "Libra", "longitude": 180},
        "planets": {
            "Sun":     _mkplanet("Taurus", 8, 35),
            "Moon":    _mkplanet("Gemini", 9, 65),
            "Mars":    _mkplanet("Virgo", 12, 160),
            "Mercury": _mkplanet("Aries", 7, 5),
            "Jupiter": _mkplanet("Cancer", 10, 100),
            "Venus":   _mkplanet("Leo", 11, 130),
            "Saturn":  _mkplanet("Pisces", 6, 345),
            "Rahu":    _mkplanet("Scorpio", 2, 220),
            "Ketu":    _mkplanet("Taurus", 8, 50),
        },
    }
    r = detect_pravrajya(chart)
    assert r["count"] == 0
    assert r["has_ascetic_tendency"] is False
    assert r["yogas_found"] == []


# ═══════════════════════════════════════════════════════════════
# Graceful degradation — missing/empty inputs
# ═══════════════════════════════════════════════════════════════

def test_empty_chart():
    r = detect_pravrajya({})
    assert r["count"] == 0
    assert r["has_ascetic_tendency"] is False


def test_none_input():
    r = detect_pravrajya(None)  # type: ignore[arg-type]
    assert r["count"] == 0
    assert r["has_ascetic_tendency"] is False


def test_missing_planets():
    # Only Sun provided — no error, no yogas triggered
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Sun": _mkplanet("Aries", 1, 5)},
    }
    r = detect_pravrajya(chart)
    assert r["count"] == 0
    assert isinstance(r["yogas_found"], list)


def test_missing_ascendant():
    # No ascendant info — Paramahamsa check should degrade gracefully
    chart = {
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 5),
            "Jupiter": _mkplanet("Aries", 1, 12),
            "Mars":    _mkplanet("Aries", 1, 18),
            "Venus":   _mkplanet("Aries", 1, 25),
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mercury": _mkplanet("Gemini", 3, 65),
            "Saturn":  _mkplanet("Cancer", 4, 100),
            "Rahu":    _mkplanet("Leo", 5, 130),
            "Ketu":    _mkplanet("Aquarius", 11, 310),
        },
    }
    r = detect_pravrajya(chart)
    # Should not crash; may still detect Vanaprastha via house field alone
    assert isinstance(r["yogas_found"], list)


# ═══════════════════════════════════════════════════════════════
# Return-contract shape
# ═══════════════════════════════════════════════════════════════

def test_return_contract():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 5),
            "Mercury": _mkplanet("Aries", 1, 12),
            "Venus":   _mkplanet("Aries", 1, 18),
            "Mars":    _mkplanet("Aries", 1, 25),
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Jupiter": _mkplanet("Gemini", 3, 65),
            "Saturn":  _mkplanet("Cancer", 4, 100),
            "Rahu":    _mkplanet("Leo", 5, 130),
            "Ketu":    _mkplanet("Aquarius", 11, 310),
        },
    }
    r = detect_pravrajya(chart)
    assert set(r.keys()) >= {"yogas_found", "count", "has_ascetic_tendency"}
    assert isinstance(r["count"], int)
    assert r["count"] == len(r["yogas_found"])
    for yoga in r["yogas_found"]:
        assert set(yoga.keys()) >= {
            "key", "name_en", "name_hi", "strength",
            "effect_en", "effect_hi", "sloka_ref", "supporting_factors",
        }
        assert 1 <= yoga["strength"] <= 10
        assert isinstance(yoga["supporting_factors"], list)
