"""Tests for Apatya (progeny) analysis — Phaladeepika Adhyaya 12."""
from app.apatya_engine import (
    analyze_apatya,
    _is_female_sign,
    _fifth_lord_info,
    _jupiter_info,
)


def _mkplanet(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {"sign": sign, "house": house, "longitude": longitude, "sign_degree": longitude % 30}


# ═══════════════════════════════════════════════════════════════
# Helper tests
# ═══════════════════════════════════════════════════════════════

def test_is_female_sign():
    for s in ("Taurus", "Cancer", "Virgo", "Scorpio", "Capricorn", "Pisces"):
        assert _is_female_sign(s) is True
    for s in ("Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"):
        assert _is_female_sign(s) is False
    assert _is_female_sign("") is False
    assert _is_female_sign("NotASign") is False


def test_fifth_lord_info_basic():
    # Asc Aries → 5th sign = Leo → lord Sun
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun": _mkplanet("Leo", 5, 130),       # strong — own sign + Trikona
            "Jupiter": _mkplanet("Cancer", 4, 100),
        },
    }
    info = _fifth_lord_info(chart)
    assert info["lord"] == "Sun"
    assert info["placement"] == 5
    assert info["fifth_sign"] == "Leo"
    assert info["strength"] == "strong"


def test_jupiter_info_basic():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Jupiter": _mkplanet("Cancer", 4, 100)},  # Cancer = exaltation
    }
    j = _jupiter_info(chart)
    assert j["placement"] == 4
    assert j["sign"] == "Cancer"
    assert j["strength"] == "strong"


def test_jupiter_info_missing():
    j = _jupiter_info({"planets": {}, "ascendant": {"sign": "Aries"}})
    assert j["placement"] == 0
    assert j["strength"] == "unknown"


# ═══════════════════════════════════════════════════════════════
# Return contract
# ═══════════════════════════════════════════════════════════════

def test_return_contract_shape():
    r = analyze_apatya({
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {},
    })
    assert set(r.keys()) >= {
        "fifth_house_analysis", "yogas_detected", "progeny_prospect",
        "recommendations_en", "recommendations_hi",
        "remedies_en", "remedies_hi", "sloka_ref",
    }
    assert r["sloka_ref"] == "Phaladeepika Adh. 12"
    assert isinstance(r["yogas_detected"], list)
    assert r["progeny_prospect"] in ("favorable", "challenging", "mixed")


# ═══════════════════════════════════════════════════════════════
# Per-yoga detection
# ═══════════════════════════════════════════════════════════════

def test_putra_yoga_detected():
    # Asc Aries → 5th lord = Sun. Sun exalted in Aries (Lagna = Kendra+Trikona) → strong.
    # Jupiter in Cancer (exaltation, house 4 = Kendra). 5th house unafflicted.
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 5),         # exalted in Aries (5th lord strong)
            "Jupiter": _mkplanet("Cancer", 4, 100),      # Kendra, exalted
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mars":    _mkplanet("Capricorn", 10, 280),  # exalted — Kendra (aspect 4,7,1)
            "Mercury": _mkplanet("Gemini", 3, 65),
            "Venus":   _mkplanet("Pisces", 12, 345),
            "Saturn":  _mkplanet("Libra", 7, 190),       # exalted — aspects 1,4,9 (NOT 5)
            "Rahu":    _mkplanet("Aquarius", 11, 310),
            "Ketu":    _mkplanet("Leo", 5, 130),         # Ketu in 5 → actually this adds malefic...
        },
    }
    # Ketu in 5 would afflict — remove it by moving it
    chart["planets"]["Ketu"] = _mkplanet("Aquarius", 11, 315)
    # Also need nothing aspecting 5th with malefics
    # Mars at house 10 aspects: 7 (univ), 4+8-1=... let's check: mars special 4,8
    # From house 10: 7th = house 4, +4th = house 1, +8th = house 5. So Mars in 10 DOES aspect 5.
    # Move Mars somewhere else — put Mars in house 2 (Taurus), no longer exalted
    # Actually put Mars in Aries in Lagna — exalted? No Mars exalted in Capricorn.
    # Let's make it simpler: put Mars in house 3 (Gemini). Mars house 3 → 7th=9, +4=6, +8=10. No aspect on 5.
    chart["planets"]["Mars"] = _mkplanet("Gemini", 3, 70)
    chart["planets"]["Mercury"] = _mkplanet("Virgo", 6, 160)   # exalted, house 6 — aspects 12 only
    # Saturn house 7 → aspects: 1 (7th), 9 (3rd), 4 (10th). None on 5. Good.
    # Rahu house 11 → aspects: 5 (7th univ), 3 (5th spec), 7 (9th spec). Rahu DOES aspect 5.
    chart["planets"]["Rahu"] = _mkplanet("Libra", 7, 195)  # together with Saturn — aspects 1,9,4
    chart["planets"]["Ketu"] = _mkplanet("Aries", 1, 10)   # with Sun, aspects 7,5,9? ketu 5/9 special
    # Ketu house 1: aspects 7 (univ), 5 (5th spec), 9 (9th spec). Ketu aspects 5. Bad.
    chart["planets"]["Ketu"] = _mkplanet("Gemini", 3, 75)  # with Mars — aspects 9,7,11

    r = analyze_apatya(chart)
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "putra_yoga" in keys
    yoga = next(y for y in r["yogas_detected"] if y["key"] == "putra_yoga")
    assert yoga["name_hi"] == "पुत्र योग"
    assert yoga["sloka_ref"].startswith("Phaladeepika Adh. 12")


def test_aputra_yoga_detected():
    # Asc Aries → 5th lord = Sun. Put Sun debilitated (Libra), in 7th (Kendra but not dusthana).
    # Make Sun weak AND aspected by malefic. 5th house afflicted by Saturn+Rahu.
    # Jupiter debilitated in Capricorn (house 10).
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Libra", 7, 190),         # debilitated → weak
            "Jupiter": _mkplanet("Capricorn", 10, 280),    # debilitated
            "Saturn":  _mkplanet("Leo", 5, 130),           # malefic in 5th
            "Rahu":    _mkplanet("Leo", 5, 135),           # malefic in 5th
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mars":    _mkplanet("Virgo", 6, 160),
            "Mercury": _mkplanet("Gemini", 3, 65),
            "Venus":   _mkplanet("Pisces", 12, 345),
            "Ketu":    _mkplanet("Aquarius", 11, 310),
        },
    }
    r = analyze_apatya(chart)
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "aputra_yoga" in keys
    yoga = next(y for y in r["yogas_detected"] if y["key"] == "aputra_yoga")
    assert yoga["name_hi"] == "अपुत्र योग"
    assert yoga["probability"] == "high"


def test_dattaka_yoga_detected():
    # Asc Aries → 5th lord Sun. Sun in 8th house (Scorpio = Dusthana).
    # Malefic (Mars) in 5th. Jupiter weak.
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Scorpio", 8, 220),
            "Mars":    _mkplanet("Leo", 5, 130),          # malefic in 5th
            "Jupiter": _mkplanet("Capricorn", 10, 280),   # debilitated → weak
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mercury": _mkplanet("Gemini", 3, 65),
            "Venus":   _mkplanet("Pisces", 12, 345),
            "Saturn":  _mkplanet("Virgo", 6, 160),
            "Rahu":    _mkplanet("Aquarius", 11, 310),
            "Ketu":    _mkplanet("Leo", 5, 135),
        },
    }
    r = analyze_apatya(chart)
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "dattaka_yoga" in keys


def test_kanya_yoga_detected():
    # 5th sign must be female. Pisces asc → 5th = Cancer (female). Lord = Moon.
    # Moon in female sign + Venus in 5th.
    chart = {
        "ascendant": {"sign": "Pisces", "longitude": 330},
        "planets": {
            "Moon":    _mkplanet("Scorpio", 9, 220),      # female sign
            "Venus":   _mkplanet("Cancer", 5, 100),       # Venus in 5th (Cancer, female)
            "Jupiter": _mkplanet("Sagittarius", 10, 250),
            "Sun":     _mkplanet("Aries", 2, 5),
            "Mars":    _mkplanet("Taurus", 3, 35),
            "Mercury": _mkplanet("Gemini", 4, 65),
            "Saturn":  _mkplanet("Libra", 8, 190),
            "Rahu":    _mkplanet("Leo", 6, 130),
            "Ketu":    _mkplanet("Aquarius", 12, 310),
        },
    }
    r = analyze_apatya(chart)
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "kanya_yoga" in keys


def test_putra_hani_yoga_detected_saturn_rahu_in_5():
    # Saturn + Rahu together in 5th house
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Saturn":  _mkplanet("Leo", 5, 130),
            "Rahu":    _mkplanet("Leo", 5, 135),
            "Sun":     _mkplanet("Aries", 1, 5),
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mars":    _mkplanet("Gemini", 3, 65),
            "Mercury": _mkplanet("Cancer", 4, 100),
            "Jupiter": _mkplanet("Virgo", 6, 160),
            "Venus":   _mkplanet("Libra", 7, 190),
            "Ketu":    _mkplanet("Aquarius", 11, 310),
        },
    }
    r = analyze_apatya(chart)
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "putra_hani_yoga" in keys


def test_bahu_putra_yoga_detected():
    # Multiple benefics in 5th + Jupiter in Kendra + 5th lord strong
    # Asc Aries → 5th lord Sun. Sun exalted in Aries (Lagna) → strong.
    # Jupiter in Cancer (house 4 = Kendra, exalted).
    # Benefics in 5th: Venus, Mercury, Moon.
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 5),           # 5th lord strong
            "Jupiter": _mkplanet("Cancer", 4, 100),        # Kendra
            "Venus":   _mkplanet("Leo", 5, 130),
            "Mercury": _mkplanet("Leo", 5, 135),
            "Moon":    _mkplanet("Leo", 5, 128),
            "Mars":    _mkplanet("Virgo", 6, 160),
            "Saturn":  _mkplanet("Libra", 7, 190),
            "Rahu":    _mkplanet("Scorpio", 8, 220),
            "Ketu":    _mkplanet("Taurus", 2, 50),
        },
    }
    r = analyze_apatya(chart)
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "bahu_putra_yoga" in keys


def test_jyeshta_putra_yoga_detected():
    # Sun in 5th + Jupiter aspects 5th
    # Jupiter in house 9 → 7th aspect = house 3 (no); Jupiter 5/9 → house 1, house 5. So Jupiter house 9 aspects house 5 (via 9th special from 9 = 9+9-1)... let's verify.
    # Jupiter in house 9: aspects = [7th univ = 3], 5th special = 9+5-1 mod 12 +1 = 1; 9th special = 9+9-1 mod 12 +1 = 5. YES Jupiter in 9 aspects 5.
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Leo", 5, 130),
            "Jupiter": _mkplanet("Sagittarius", 9, 250),
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mars":    _mkplanet("Capricorn", 10, 280),
            "Mercury": _mkplanet("Gemini", 3, 65),
            "Venus":   _mkplanet("Pisces", 12, 345),
            "Saturn":  _mkplanet("Aquarius", 11, 310),
            "Rahu":    _mkplanet("Cancer", 4, 100),
            "Ketu":    _mkplanet("Capricorn", 10, 285),
        },
    }
    r = analyze_apatya(chart)
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "jyeshta_putra_yoga" in keys


def test_delayed_progeny_yoga_saturn_in_5():
    # Saturn in 5th house
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Saturn":  _mkplanet("Leo", 5, 130),
            "Sun":     _mkplanet("Aries", 1, 5),
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mars":    _mkplanet("Gemini", 3, 65),
            "Mercury": _mkplanet("Cancer", 4, 100),
            "Jupiter": _mkplanet("Virgo", 6, 160),
            "Venus":   _mkplanet("Libra", 7, 190),
            "Rahu":    _mkplanet("Scorpio", 8, 220),
            "Ketu":    _mkplanet("Taurus", 2, 50),
        },
    }
    r = analyze_apatya(chart)
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "delayed_progeny_yoga" in keys


def test_delayed_progeny_yoga_lord_in_saturn_sign():
    # Asc Leo → 5th sign = Sagittarius → lord Jupiter.
    # Put Jupiter in Capricorn (Saturn's sign).
    chart = {
        "ascendant": {"sign": "Leo", "longitude": 120},
        "planets": {
            "Jupiter": _mkplanet("Capricorn", 6, 280),
            "Sun":     _mkplanet("Leo", 1, 125),
            "Moon":    _mkplanet("Virgo", 2, 160),
            "Mars":    _mkplanet("Libra", 3, 190),
            "Mercury": _mkplanet("Scorpio", 4, 220),
            "Venus":   _mkplanet("Sagittarius", 5, 250),
            "Saturn":  _mkplanet("Aquarius", 7, 310),
            "Rahu":    _mkplanet("Pisces", 8, 345),
            "Ketu":    _mkplanet("Virgo", 2, 170),
        },
    }
    r = analyze_apatya(chart)
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "delayed_progeny_yoga" in keys


# ═══════════════════════════════════════════════════════════════
# Prospect assessment
# ═══════════════════════════════════════════════════════════════

def test_prospect_favorable():
    # Same as putra_yoga chart → favorable
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 5),
            "Jupiter": _mkplanet("Cancer", 4, 100),
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mars":    _mkplanet("Gemini", 3, 70),
            "Mercury": _mkplanet("Virgo", 6, 160),
            "Venus":   _mkplanet("Pisces", 12, 345),
            "Saturn":  _mkplanet("Libra", 7, 190),
            "Rahu":    _mkplanet("Libra", 7, 195),
            "Ketu":    _mkplanet("Gemini", 3, 75),
        },
    }
    r = analyze_apatya(chart)
    assert r["progeny_prospect"] == "favorable"


def test_prospect_challenging():
    # Aputra yoga → challenging
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Libra", 7, 190),
            "Jupiter": _mkplanet("Capricorn", 10, 280),
            "Saturn":  _mkplanet("Leo", 5, 130),
            "Rahu":    _mkplanet("Leo", 5, 135),
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mars":    _mkplanet("Virgo", 6, 160),
            "Mercury": _mkplanet("Gemini", 3, 65),
            "Venus":   _mkplanet("Pisces", 12, 345),
            "Ketu":    _mkplanet("Aquarius", 11, 310),
        },
    }
    r = analyze_apatya(chart)
    assert r["progeny_prospect"] == "challenging"


# ═══════════════════════════════════════════════════════════════
# Content checks
# ═══════════════════════════════════════════════════════════════

def test_bilingual_fields_present():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 5),
            "Jupiter": _mkplanet("Cancer", 4, 100),
            "Moon":    _mkplanet("Taurus", 2, 35),
            "Mars":    _mkplanet("Gemini", 3, 70),
            "Mercury": _mkplanet("Virgo", 6, 160),
            "Venus":   _mkplanet("Pisces", 12, 345),
            "Saturn":  _mkplanet("Libra", 7, 190),
            "Rahu":    _mkplanet("Libra", 7, 195),
            "Ketu":    _mkplanet("Gemini", 3, 75),
        },
    }
    r = analyze_apatya(chart)
    assert r["fifth_house_analysis"]["interpretation_en"]
    assert r["fifth_house_analysis"]["interpretation_hi"]
    assert len(r["recommendations_en"]) >= 1
    assert len(r["recommendations_hi"]) >= 1
    assert len(r["remedies_en"]) >= 1
    assert len(r["remedies_hi"]) >= 1
    for y in r["yogas_detected"]:
        assert set(y.keys()) >= {
            "key", "name_en", "name_hi", "effect_en", "effect_hi",
            "probability", "sloka_ref",
        }
        assert y["probability"] in ("high", "moderate", "low")


def test_fifth_house_analysis_fields():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Leo", 5, 130),
            "Jupiter": _mkplanet("Cancer", 4, 100),
        },
    }
    r = analyze_apatya(chart)
    f = r["fifth_house_analysis"]
    assert f["fifth_lord"] == "Sun"
    assert f["fifth_lord_placement"] == 5
    assert f["jupiter_placement"] == 4
    assert "Sun" in f["planets_in_5th"]
    assert isinstance(f["benefics_in_5th"], list)
    assert isinstance(f["malefics_in_5th"], list)


# ═══════════════════════════════════════════════════════════════
# Graceful degradation
# ═══════════════════════════════════════════════════════════════

def test_empty_chart():
    r = analyze_apatya({})
    assert r["yogas_detected"] == []
    assert r["progeny_prospect"] in ("favorable", "challenging", "mixed")
    assert r["sloka_ref"] == "Phaladeepika Adh. 12"


def test_none_input():
    r = analyze_apatya(None)  # type: ignore[arg-type]
    assert r["yogas_detected"] == []


def test_missing_planets():
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {}}
    r = analyze_apatya(chart)
    assert isinstance(r["yogas_detected"], list)
    assert r["fifth_house_analysis"]["fifth_sign"] == "Leo"
    assert r["fifth_house_analysis"]["fifth_lord"] == "Sun"


def test_missing_ascendant():
    chart = {"planets": {"Jupiter": _mkplanet("Cancer", 4, 100)}}
    r = analyze_apatya(chart)
    # Should not crash
    assert "yogas_detected" in r
    assert "fifth_house_analysis" in r


def test_normal_chart_no_extreme_yogas():
    # Benign scattered chart — may have delayed_progeny if lord in Cap/Aqu, but
    # otherwise should not trigger aputra/putra_hani extremes.
    chart = {
        "ascendant": {"sign": "Gemini", "longitude": 60},
        "planets": {
            "Sun":     _mkplanet("Aries", 11, 5),
            "Moon":    _mkplanet("Taurus", 12, 35),
            "Mars":    _mkplanet("Cancer", 2, 100),
            "Mercury": _mkplanet("Gemini", 1, 65),
            "Jupiter": _mkplanet("Leo", 3, 130),
            "Venus":   _mkplanet("Virgo", 4, 160),
            "Saturn":  _mkplanet("Sagittarius", 7, 250),
            "Rahu":    _mkplanet("Pisces", 10, 345),
            "Ketu":    _mkplanet("Virgo", 4, 170),
        },
    }
    r = analyze_apatya(chart)
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "aputra_yoga" not in keys
    assert "putra_hani_yoga" not in keys
