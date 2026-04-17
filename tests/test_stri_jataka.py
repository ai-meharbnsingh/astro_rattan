"""Tests for Stri-Jataka (women's horoscope) analysis — Phaladeepika Adh. 11."""
from app.stri_jataka_engine import (
    analyze_stri_jataka,
    _seventh_lord_info,
    _venus_afflicted,
    _sign_at_house,
)


def _mkplanet(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {"sign": sign, "house": house, "longitude": longitude, "sign_degree": longitude % 30}


# ═══════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════

def test_sign_at_house():
    assert _sign_at_house("Aries", 1) == "Aries"
    assert _sign_at_house("Aries", 7) == "Libra"
    assert _sign_at_house("Libra", 7) == "Aries"
    assert _sign_at_house("Cancer", 4) == "Libra"
    assert _sign_at_house("Aries", 0) == ""
    assert _sign_at_house("Aries", 13) == ""
    assert _sign_at_house("NotASign", 1) == ""


def test_seventh_lord_info_strong():
    # Lagna Aries → 7th = Libra → 7th lord = Venus
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Venus":  _mkplanet("Taurus", 2),   # own sign → strong
        },
    }
    info = _seventh_lord_info(chart)
    assert info["seventh_lord"] == "Venus"
    assert info["seventh_lord_dignity"] == "own"
    assert info["seventh_lord_strength"] == "strong"
    assert info["seventh_lord_placement"] == 2


def test_seventh_lord_info_weak():
    # Lagna Aries → 7th = Libra → lord Venus. Place Venus debilitated (Virgo) in 6th.
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Venus":  _mkplanet("Virgo", 6),    # debilitated + Dusthana → weak
        },
    }
    info = _seventh_lord_info(chart)
    assert info["seventh_lord"] == "Venus"
    assert info["seventh_lord_dignity"] == "debilitated"
    assert info["seventh_lord_strength"] == "weak"


def test_venus_afflicted_debilitated():
    chart = {
        "ascendant": {"sign": "Aries"},
        "planets": {"Venus": _mkplanet("Virgo", 6)},   # debilitated
    }
    assert _venus_afflicted(chart) is True


def test_venus_not_afflicted_exalted():
    chart = {
        "ascendant": {"sign": "Aries"},
        "planets": {
            "Venus":   _mkplanet("Pisces", 12),   # exalted but in Dusthana → should still be afflicted
        },
    }
    # Dusthana alone makes it afflicted
    assert _venus_afflicted(chart) is True


def test_venus_clean():
    chart = {
        "ascendant": {"sign": "Aries"},
        "planets": {
            "Venus":   _mkplanet("Taurus", 2),    # own sign, not Dusthana
            "Jupiter": _mkplanet("Scorpio", 8),   # aspects 2nd via 7th (benefic aspect)
        },
    }
    assert _venus_afflicted(chart) is False


# ═══════════════════════════════════════════════════════════════
# Per-yoga detection
# ═══════════════════════════════════════════════════════════════

def test_sahagamana_detected():
    # Venus in 7th (Libra if asc=Aries), Jupiter in 1st aspects 7th (5/9 aspect → house 5,9; universal 7th from 1 = 7).
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Venus":   _mkplanet("Libra", 7, 190),
            "Jupiter": _mkplanet("Aries", 1, 10),   # 7th aspect → house 7
            "Sun":     _mkplanet("Taurus", 2, 40),
            "Moon":    _mkplanet("Cancer", 4, 100),
            "Mars":    _mkplanet("Leo", 5, 130),
            "Mercury": _mkplanet("Virgo", 6, 160),
            "Saturn":  _mkplanet("Scorpio", 8, 220),
            "Rahu":    _mkplanet("Gemini", 3, 70),
            "Ketu":    _mkplanet("Sagittarius", 9, 250),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "sahagamana" in keys
    yoga = next(y for y in r["yogas_detected"] if y["key"] == "sahagamana")
    assert yoga["name_hi"] == "सहगमन योग"
    assert yoga["severity"] == "auspicious"
    assert "Phaladeepika Adh. 11" in yoga["sloka_ref"]


def test_sahagamana_not_detected_without_jupiter_aspect():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Venus":   _mkplanet("Libra", 7, 190),
            "Jupiter": _mkplanet("Taurus", 2, 40),   # doesn't aspect 7th
            "Sun":     _mkplanet("Cancer", 4, 100),
            "Moon":    _mkplanet("Gemini", 3, 70),
            "Mars":    _mkplanet("Leo", 5, 130),
            "Mercury": _mkplanet("Virgo", 6, 160),
            "Saturn":  _mkplanet("Pisces", 12, 340),
            "Rahu":    _mkplanet("Capricorn", 10, 280),
            "Ketu":    _mkplanet("Cancer", 4, 110),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    assert not any(y["key"] == "sahagamana" for y in r["yogas_detected"])


def test_vaidhavya_detected_mars_saturn_in_7th():
    # Mars + Saturn in 7th, Venus in 8th (afflicted via Dusthana)
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Mars":    _mkplanet("Libra", 7, 190),
            "Saturn":  _mkplanet("Libra", 7, 200),
            "Venus":   _mkplanet("Scorpio", 8, 220),   # Dusthana
            "Jupiter": _mkplanet("Capricorn", 10, 280),   # debilitated
            "Sun":     _mkplanet("Taurus", 2, 40),
            "Moon":    _mkplanet("Cancer", 4, 100),
            "Mercury": _mkplanet("Virgo", 6, 160),
            "Rahu":    _mkplanet("Gemini", 3, 70),
            "Ketu":    _mkplanet("Sagittarius", 9, 250),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "vaidhavya" in keys


def test_vaidhavya_high_severity_when_both_combos():
    # Both combos: Mars+Saturn in 7th AND 7th-lord (Venus) in 8th debilitated + venus afflicted.
    # But Venus is the 7th lord here — we need Venus debilitated in Dusthana.
    # Lagna Aries → 7th Libra → 7th lord Venus. Place Venus debilitated (Virgo=6, Dusthana).
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Mars":    _mkplanet("Libra", 7, 190),
            "Saturn":  _mkplanet("Libra", 7, 200),
            "Venus":   _mkplanet("Virgo", 6, 170),   # debilitated + Dusthana
            "Jupiter": _mkplanet("Capricorn", 10, 280),
            "Sun":     _mkplanet("Taurus", 2, 40),
            "Moon":    _mkplanet("Cancer", 4, 100),
            "Mercury": _mkplanet("Leo", 5, 130),
            "Rahu":    _mkplanet("Gemini", 3, 70),
            "Ketu":    _mkplanet("Sagittarius", 9, 250),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    vaidhavya = next((y for y in r["yogas_detected"] if y["key"] == "vaidhavya"), None)
    assert vaidhavya is not None
    assert vaidhavya["severity"] == "high"


def test_punarbhu_dual_sign_seventh_lord():
    # Lagna Sagittarius → 7th = Gemini → 7th lord Mercury. Place Mercury in Gemini (dual sign).
    chart = {
        "ascendant": {"sign": "Sagittarius", "longitude": 240},
        "planets": {
            "Mercury": _mkplanet("Gemini", 7, 70),    # dual sign
            "Sun":     _mkplanet("Capricorn", 2, 280),
            "Moon":    _mkplanet("Pisces", 4, 340),
            "Mars":    _mkplanet("Aries", 5, 10),
            "Venus":   _mkplanet("Taurus", 6, 40),
            "Jupiter": _mkplanet("Cancer", 8, 100),
            "Saturn":  _mkplanet("Leo", 9, 130),
            "Rahu":    _mkplanet("Virgo", 10, 160),
            "Ketu":    _mkplanet("Pisces", 4, 350),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "punarbhu" in keys


def test_punarbhu_venus_rahu_in_7th():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Venus":   _mkplanet("Libra", 7, 190),
            "Rahu":    _mkplanet("Libra", 7, 195),
            "Sun":     _mkplanet("Taurus", 2, 40),
            "Moon":    _mkplanet("Cancer", 4, 100),
            "Mars":    _mkplanet("Leo", 5, 130),
            "Mercury": _mkplanet("Virgo", 6, 160),
            "Jupiter": _mkplanet("Taurus", 2, 50),
            "Saturn":  _mkplanet("Pisces", 12, 340),
            "Ketu":    _mkplanet("Aries", 1, 15),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "punarbhu" in keys


def test_punarbhu_multiple_malefics_in_7th():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Mars":    _mkplanet("Libra", 7, 190),
            "Saturn":  _mkplanet("Libra", 7, 200),
            "Rahu":    _mkplanet("Libra", 7, 205),
            "Sun":     _mkplanet("Taurus", 2, 40),
            "Moon":    _mkplanet("Cancer", 4, 100),
            "Venus":   _mkplanet("Leo", 5, 130),
            "Mercury": _mkplanet("Virgo", 6, 160),
            "Jupiter": _mkplanet("Taurus", 2, 50),
            "Ketu":    _mkplanet("Aries", 1, 15),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "punarbhu" in keys


def test_bhartri_sukha_detected():
    # Lagna Aries → 7th Libra → lord Venus. Venus in Pisces (exalted) in 12 — but we need Venus in KENDRA.
    # Alternate: Lagna Taurus → 7th Scorpio → lord Mars. Place Mars exalted in Capricorn (9th from Taurus=Capricorn→ house 9, Trikona, not Kendra).
    # Lagna Leo → 7th Aquarius → lord Saturn. Saturn exalted in Libra = 3rd from Leo (not Kendra/Trikona either — just need lord exalted).
    # Choose: Lagna Capricorn → 7th Cancer → lord Moon. Moon exalted in Taurus. Taurus from Capricorn = 5th.
    # Venus must be in Kendra (1,4,7,10) from Capricorn. Capricorn=1, Aries=4, Cancer=7, Libra=10.
    # Jupiter aspects 7th (Cancer).
    chart = {
        "ascendant": {"sign": "Capricorn", "longitude": 270},
        "planets": {
            "Moon":    _mkplanet("Taurus", 5, 40),      # 7th lord, exalted
            "Venus":   _mkplanet("Aries", 4, 10),       # Kendra (4th)
            "Jupiter": _mkplanet("Capricorn", 1, 275),  # aspects 7th (1→7)
            "Sun":     _mkplanet("Gemini", 6, 70),
            "Mars":    _mkplanet("Leo", 8, 130),
            "Mercury": _mkplanet("Gemini", 6, 75),
            "Saturn":  _mkplanet("Virgo", 9, 160),
            "Rahu":    _mkplanet("Libra", 10, 190),
            "Ketu":    _mkplanet("Aries", 4, 20),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "bhartri_sukha" in keys


def test_putravati_detected():
    # Lagna Aries → 5th=Leo → 5th lord Sun. Place Sun exalted in Aries (1=Kendra).
    # Jupiter in Kendra/Trikona — put Jupiter in Cancer (exalted), house 4 (Kendra).
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 10),     # 5th lord exalted, Kendra
            "Jupiter": _mkplanet("Cancer", 4, 100),   # Jupiter in Kendra
            "Moon":    _mkplanet("Taurus", 2, 40),
            "Mars":    _mkplanet("Gemini", 3, 70),
            "Mercury": _mkplanet("Leo", 5, 130),
            "Venus":   _mkplanet("Virgo", 6, 160),
            "Saturn":  _mkplanet("Libra", 7, 190),
            "Rahu":    _mkplanet("Scorpio", 8, 220),
            "Ketu":    _mkplanet("Taurus", 2, 50),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "putravati" in keys


def test_pativrata_detected():
    # Jupiter in Lagna (Aries), Moon in Cancer (own sign), no malefic in 7th.
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Jupiter": _mkplanet("Aries", 1, 10),
            "Moon":    _mkplanet("Cancer", 4, 100),    # own sign
            "Sun":     _mkplanet("Taurus", 2, 40),
            "Mars":    _mkplanet("Leo", 5, 130),       # not in 7th
            "Mercury": _mkplanet("Virgo", 6, 160),
            "Venus":   _mkplanet("Libra", 7, 190),     # benefic in 7th — OK
            "Saturn":  _mkplanet("Capricorn", 10, 280),
            "Rahu":    _mkplanet("Gemini", 3, 70),
            "Ketu":    _mkplanet("Sagittarius", 9, 250),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "pativrata" in keys


def test_pativrata_rejected_malefic_in_7th():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Jupiter": _mkplanet("Aries", 1, 10),
            "Moon":    _mkplanet("Cancer", 4, 100),
            "Mars":    _mkplanet("Libra", 7, 190),    # malefic in 7th — rejects
            "Sun":     _mkplanet("Taurus", 2, 40),
            "Mercury": _mkplanet("Virgo", 6, 160),
            "Venus":   _mkplanet("Scorpio", 8, 220),
            "Saturn":  _mkplanet("Capricorn", 10, 280),
            "Rahu":    _mkplanet("Gemini", 3, 70),
            "Ketu":    _mkplanet("Sagittarius", 9, 250),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    assert not any(y["key"] == "pativrata" for y in r["yogas_detected"])


def test_sevaka_detected():
    # Saturn in Lagna + Jupiter debilitated + Venus in Dusthana
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Saturn":  _mkplanet("Aries", 1, 5),        # in Lagna (also debilitated, but placement matters)
            "Jupiter": _mkplanet("Capricorn", 10, 280), # debilitated
            "Venus":   _mkplanet("Virgo", 6, 160),      # Dusthana
            "Sun":     _mkplanet("Taurus", 2, 40),
            "Moon":    _mkplanet("Gemini", 3, 70),
            "Mars":    _mkplanet("Leo", 5, 130),
            "Mercury": _mkplanet("Virgo", 6, 170),
            "Rahu":    _mkplanet("Scorpio", 8, 220),
            "Ketu":    _mkplanet("Taurus", 2, 50),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    keys = {y["key"] for y in r["yogas_detected"]}
    assert "sevaka" in keys
    yoga = next(y for y in r["yogas_detected"] if y["key"] == "sevaka")
    assert yoga["severity"] == "challenging"


# ═══════════════════════════════════════════════════════════════
# Gender filter
# ═══════════════════════════════════════════════════════════════

def test_gender_male_returns_not_applicable():
    chart = {
        "ascendant": {"sign": "Aries"},
        "planets": {"Venus": _mkplanet("Libra", 7)},
    }
    r = analyze_stri_jataka(chart, gender="male")
    assert r["applicable"] is False
    assert "reason" in r
    assert r["yogas_detected"] == []


def test_gender_other_returns_not_applicable():
    chart = {"ascendant": {"sign": "Aries"}, "planets": {}}
    r = analyze_stri_jataka(chart, gender="other")
    assert r["applicable"] is False


def test_gender_female_case_insensitive():
    chart = {"ascendant": {"sign": "Aries"}, "planets": {}}
    r = analyze_stri_jataka(chart, gender="Female")
    assert r["applicable"] is True


# ═══════════════════════════════════════════════════════════════
# Return contract + graceful degradation
# ═══════════════════════════════════════════════════════════════

def test_return_contract_complete():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _mkplanet("Aries", 1, 10),
            "Jupiter": _mkplanet("Cancer", 4, 100),
            "Moon":    _mkplanet("Taurus", 2, 40),
            "Mars":    _mkplanet("Gemini", 3, 70),
            "Mercury": _mkplanet("Leo", 5, 130),
            "Venus":   _mkplanet("Virgo", 6, 160),
            "Saturn":  _mkplanet("Libra", 7, 190),
            "Rahu":    _mkplanet("Scorpio", 8, 220),
            "Ketu":    _mkplanet("Taurus", 2, 50),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    expected_keys = {
        "applicable", "yogas_detected", "seventh_house_analysis",
        "marital_prospect", "recommendations_en", "recommendations_hi", "sloka_ref",
    }
    assert expected_keys.issubset(set(r.keys()))
    assert r["applicable"] is True
    assert isinstance(r["yogas_detected"], list)
    assert r["marital_prospect"] in ("favorable", "challenging", "mixed")
    sa = r["seventh_house_analysis"]
    for k in ("seventh_lord", "seventh_lord_placement", "seventh_lord_strength",
              "malefics_in_7th", "benefics_in_7th", "jupiter_aspects_7th",
              "venus_position", "interpretation_en", "interpretation_hi"):
        assert k in sa


def test_yoga_shape():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Venus":   _mkplanet("Libra", 7, 190),
            "Jupiter": _mkplanet("Aries", 1, 10),
            "Sun":     _mkplanet("Taurus", 2, 40),
            "Moon":    _mkplanet("Cancer", 4, 100),
            "Mars":    _mkplanet("Leo", 5, 130),
            "Mercury": _mkplanet("Virgo", 6, 160),
            "Saturn":  _mkplanet("Scorpio", 8, 220),
            "Rahu":    _mkplanet("Gemini", 3, 70),
            "Ketu":    _mkplanet("Sagittarius", 9, 250),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    for y in r["yogas_detected"]:
        assert {"key", "name_en", "name_hi", "effect_en", "effect_hi",
                "severity", "sloka_ref"}.issubset(y.keys())
        assert y["severity"] in ("auspicious", "moderate", "challenging", "high")


def test_empty_chart():
    r = analyze_stri_jataka({}, gender="female")
    assert r["applicable"] is True
    assert r["yogas_detected"] == []
    assert "seventh_house_analysis" in r


def test_none_chart():
    r = analyze_stri_jataka(None, gender="female")   # type: ignore[arg-type]
    assert r["applicable"] is True
    assert r["yogas_detected"] == []


def test_minimal_chart_no_crash():
    chart = {"ascendant": {"sign": "Aries"}, "planets": {"Sun": _mkplanet("Aries", 1, 5)}}
    r = analyze_stri_jataka(chart, gender="female")
    assert r["applicable"] is True
    assert isinstance(r["yogas_detected"], list)
    assert isinstance(r["recommendations_en"], list)
    assert isinstance(r["recommendations_hi"], list)


def test_prospect_favorable_with_positive_yogas():
    # Chart with sahagamana + pativrata → expect favorable
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Venus":   _mkplanet("Libra", 7, 190),
            "Jupiter": _mkplanet("Aries", 1, 10),
            "Moon":    _mkplanet("Cancer", 4, 100),    # own sign
            "Sun":     _mkplanet("Taurus", 2, 40),
            "Mars":    _mkplanet("Leo", 5, 130),       # not in 7th
            "Mercury": _mkplanet("Virgo", 6, 160),
            "Saturn":  _mkplanet("Capricorn", 10, 280),
            "Rahu":    _mkplanet("Gemini", 3, 70),
            "Ketu":    _mkplanet("Sagittarius", 9, 250),
        },
    }
    r = analyze_stri_jataka(chart, gender="female")
    assert r["marital_prospect"] == "favorable"


def test_recommendations_always_non_empty_when_applicable():
    chart = {"ascendant": {"sign": "Aries"}, "planets": {}}
    r = analyze_stri_jataka(chart, gender="female")
    assert len(r["recommendations_en"]) >= 1
    assert len(r["recommendations_hi"]) >= 1
    assert len(r["recommendations_en"]) == len(r["recommendations_hi"])
