"""Tests for Classical Roga (disease) Phalam — Phaladeepika Adh. 14."""
from app.roga_engine import analyze_diseases, load_roga_data


def _p(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {"sign": sign, "house": house, "longitude": longitude, "sign_degree": longitude % 30}


# ═══════════════════════════════════════════════════════════════
# Data file integrity
# ═══════════════════════════════════════════════════════════════

def test_data_loads_all_planets():
    data = load_roga_data()
    for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        assert p in data["planet_diseases"]
        assert "en" in data["planet_diseases"][p]
        assert "hi" in data["planet_diseases"][p]
        assert len(data["planet_diseases"][p]["en"]) > 0


def test_data_has_all_12_houses():
    data = load_roga_data()
    for h in range(1, 13):
        assert str(h) in data["body_part_by_house"]


def test_data_has_special_yogas():
    # P1 #15 expanded from 7 to 15 special yogas; original 7 must still be present
    data = load_roga_data()
    assert len(data["special_yogas"]) >= 16
    original_keys = {"leprosy", "epilepsy", "diabetes", "jaundice", "tuberculosis", "insanity", "blindness"}
    actual_keys = {y["key"] for y in data["special_yogas"]}
    assert original_keys.issubset(actual_keys)
    new_keys = {"cancer_tumor", "heart_disease", "liver_disease", "kidney_disease",
                "accidents_wounds", "paralysis", "venereal_disease", "manner_of_death",
                "eye_ear_disease"}
    assert new_keys.issubset(actual_keys)


# ═══════════════════════════════════════════════════════════════
# General tendencies — planets in 6/8/12
# ═══════════════════════════════════════════════════════════════

def test_mars_in_6th_triggers_wounds():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Mars": _p("Virgo", 6, 160)},
    }
    r = analyze_diseases(chart)
    assert any(t["planet"] == "Mars" and t["house"] == 6 for t in r["general_tendencies"])
    mars_entry = next(t for t in r["general_tendencies"] if t["planet"] == "Mars")
    assert any("Wounds" in d or "Accidents" in d for d in mars_entry["diseases_en"])


def test_saturn_in_8th_chronic():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Saturn": _p("Scorpio", 8, 220)},
    }
    r = analyze_diseases(chart)
    entry = next((t for t in r["general_tendencies"] if t["planet"] == "Saturn"), None)
    assert entry is not None
    assert entry["severity"] == "severe"


def test_jupiter_in_12_benefic_reduces_severity():
    # Jupiter (benefic) in 12 → chronic demoted to moderate
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Jupiter": _p("Pisces", 12, 345)},
    }
    r = analyze_diseases(chart)
    entry = next((t for t in r["general_tendencies"] if t["planet"] == "Jupiter"), None)
    assert entry is not None
    assert entry["severity"] == "moderate"  # was chronic, demoted by benefic rule


def test_body_parts_populated():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Mars": _p("Virgo", 6, 160)},
    }
    r = analyze_diseases(chart)
    assert len(r["body_parts_affected"]) >= 1
    part = r["body_parts_affected"][0]
    assert part["house"] == 6
    assert part["part_en"] != ""
    assert part["part_hi"] != ""


def test_timing_indicators_generated():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Mars":   _p("Virgo", 6, 160),
            "Moon":   _p("Cancer", 4, 100),
        },
    }
    r = analyze_diseases(chart)
    # Should mention Mars mahadasha + 6th/8th lord + Saturn transit
    text = " ".join(t["en"] for t in r["timing_indicators"])
    assert "Mars" in text
    assert "Saturn transit" in text


# ═══════════════════════════════════════════════════════════════
# Special Yogas
# ═══════════════════════════════════════════════════════════════

def test_leprosy_detected():
    # Moon + Rahu in Lagna, no Jupiter aspect
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Moon": _p("Aries", 1, 5),
            "Rahu": _p("Aries", 1, 8),
            "Jupiter": _p("Virgo", 6, 160),  # far from Lagna
            "Venus": _p("Libra", 7, 190),
        },
    }
    r = analyze_diseases(chart)
    keys = {y["key"] for y in r["special_yogas_detected"]}
    assert "leprosy" in keys


def test_leprosy_cancelled_by_jupiter_aspect():
    # Same setup but Jupiter in 7th → aspects Lagna via 7th
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Moon": _p("Aries", 1, 5),
            "Rahu": _p("Aries", 1, 8),
            "Jupiter": _p("Libra", 7, 190),   # 7th → aspects house 1
        },
    }
    r = analyze_diseases(chart)
    assert not any(y["key"] == "leprosy" for y in r["special_yogas_detected"])


def test_epilepsy_detected():
    # Saturn + Moon in Lagna, Mars aspects Lagna
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Saturn": _p("Aries", 1, 5),
            "Moon":   _p("Aries", 1, 8),
            "Mars":   _p("Libra", 7, 190),   # 7th aspect → Lagna
        },
    }
    r = analyze_diseases(chart)
    keys = {y["key"] for y in r["special_yogas_detected"]}
    assert "epilepsy" in keys


def test_diabetes_jupiter_in_6():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Jupiter": _p("Virgo", 6, 160)},
    }
    r = analyze_diseases(chart)
    keys = {y["key"] for y in r["special_yogas_detected"]}
    assert "diabetes" in keys


def test_diabetes_venus_saturn_in_6():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Venus":  _p("Virgo", 6, 162),
            "Saturn": _p("Virgo", 6, 168),
        },
    }
    r = analyze_diseases(chart)
    keys = {y["key"] for y in r["special_yogas_detected"]}
    assert "diabetes" in keys


def test_jaundice_detected():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":  _p("Virgo", 6, 162),
            "Mars": _p("Virgo", 6, 168),
        },
    }
    r = analyze_diseases(chart)
    keys = {y["key"] for y in r["special_yogas_detected"]}
    assert "jaundice" in keys


def test_tuberculosis_detected():
    # Moon in 8th + Mars aspect + weak Lagna lord (Mars in 8th = debilitated Lagna lord)
    # Actually Mars is Lagna lord for Aries. Mars in Scorpio is own sign (strong). Need different.
    # Use Libra ascendant (Venus lord). Put Venus in Virgo (debilitated) in 12th.
    chart = {
        "ascendant": {"sign": "Libra", "longitude": 180},
        "planets": {
            "Moon":   _p("Taurus", 8, 35),     # 8th house
            "Mars":   _p("Taurus", 8, 40),     # same house → aspects Moon (in own sign)
            "Venus":  _p("Virgo", 12, 160),    # Lagna lord debilitated in 12th
            "Saturn": _p("Aries", 7, 5),       # debilitated, but not needed for detection
        },
    }
    r = analyze_diseases(chart)
    keys = {y["key"] for y in r["special_yogas_detected"]}
    assert "tuberculosis" in keys


def test_insanity_detected():
    # Moon + Saturn + Rahu all in 12th
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Moon":   _p("Pisces", 12, 345),
            "Saturn": _p("Pisces", 12, 348),
            "Rahu":   _p("Pisces", 12, 350),
        },
    }
    r = analyze_diseases(chart)
    keys = {y["key"] for y in r["special_yogas_detected"]}
    assert "insanity" in keys


def test_blindness_detected():
    # Sun debilitated (Libra) + Moon debilitated (Scorpio) + no benefic aspect on either
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":    _p("Libra", 7, 190),
            "Moon":   _p("Scorpio", 8, 220),
            "Saturn": _p("Capricorn", 10, 280),  # malefic, not benefic
        },
    }
    r = analyze_diseases(chart)
    keys = {y["key"] for y in r["special_yogas_detected"]}
    assert "blindness" in keys


def test_blindness_cancelled_by_jupiter():
    # Same but Jupiter aspects Sun (from 1st → 7th aspect)
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":    _p("Libra", 7, 190),
            "Moon":   _p("Scorpio", 8, 220),
            "Jupiter": _p("Aries", 1, 10),   # aspects 7th (Sun)
        },
    }
    r = analyze_diseases(chart)
    assert not any(y["key"] == "blindness" for y in r["special_yogas_detected"])


# ═══════════════════════════════════════════════════════════════
# Return contract + graceful degradation
# ═══════════════════════════════════════════════════════════════

def test_empty_chart_no_crash():
    r = analyze_diseases({})
    assert r["general_tendencies"] == []
    assert r["special_yogas_detected"] == []


def test_none_input():
    r = analyze_diseases(None)  # type: ignore[arg-type]
    assert r["general_tendencies"] == []


def test_return_contract():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Saturn": _p("Scorpio", 8, 220)},
    }
    r = analyze_diseases(chart)
    assert set(r.keys()) >= {
        "general_tendencies", "special_yogas_detected", "timing_indicators",
        "body_parts_affected", "remedy_suggestions", "sloka_ref",
    }
    for t in r["general_tendencies"]:
        assert {"planet", "house", "severity", "diseases_en", "diseases_hi",
                "body_part_en", "body_part_hi", "reason_en", "reason_hi"}.issubset(t.keys())


def test_healthy_chart_no_special_yogas():
    chart = {
        "ascendant": {"sign": "Cancer", "longitude": 90},
        "planets": {
            "Sun":     _p("Aries", 10, 5),
            "Moon":    _p("Cancer", 1, 95),
            "Mars":    _p("Capricorn", 7, 280),
            "Mercury": _p("Virgo", 3, 160),
            "Jupiter": _p("Sagittarius", 6, 250),
            "Venus":   _p("Taurus", 11, 35),
            "Saturn":  _p("Libra", 4, 190),
            "Rahu":    _p("Pisces", 9, 345),
            "Ketu":    _p("Virgo", 3, 165),
        },
    }
    r = analyze_diseases(chart)
    # Jupiter is in 6th house → triggers diabetes yoga
    keys = {y["key"] for y in r["special_yogas_detected"]}
    # Other yogas (leprosy, epilepsy, etc.) should not fire
    assert "leprosy" not in keys
    assert "epilepsy" not in keys
    assert "insanity" not in keys
    assert "blindness" not in keys
