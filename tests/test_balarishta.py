"""Tests for Balarishta & Ayu classification — Phaladeepika Adh. 13."""
from app.ayurdaya_engine import (
    check_balarishta,
    classify_ayu,
    is_balarishta_cancelled,
)


def _p(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {"sign": sign, "house": house, "longitude": longitude, "sign_degree": longitude % 30}


# ═══════════════════════════════════════════════════════════════
# BALARISHTA
# ═══════════════════════════════════════════════════════════════

def test_balarishta_moon_in_dusthana_aspected_by_mars():
    # Moon in 8th aspected by Mars (from house 2 → 7th aspect hits 8).
    # Keep Jupiter/Venus/Mercury far from aspecting Moon or Lagna.
    # Jupiter at house 3: aspects 9 (7th), 7 (5th sp), 11 (9th sp) — none aspect 8 ✓
    # Venus at house 11: aspects 5 — not 8 ✓
    # Mercury at house 5: aspects 11 — not 8 ✓
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Capricorn", 10, 280),
            "Moon":    _p("Scorpio", 8, 220),   # Debilitated + Dusthana
            "Mars":    _p("Taurus", 2, 35),     # aspects 8 via 7th
            "Mercury": _p("Leo", 5, 135),
            "Jupiter": _p("Gemini", 3, 65),
            "Venus":   _p("Aquarius", 11, 315),
            "Saturn":  _p("Libra", 7, 190),     # aspects 1 via 7th — malefic on Lagna
            "Rahu":    _p("Scorpio", 8, 225),
            "Ketu":    _p("Taurus", 2, 45),
        },
    }
    r = check_balarishta(chart)
    assert r["has_risk"] is True
    assert r["risk_level"] in ("moderate", "high", "severe")
    assert any("Dusthana" in f for f in r["factors"])


def test_balarishta_sun_in_8th_moon_in_6th():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Scorpio", 8, 220),
            "Moon":    _p("Virgo", 6, 160),
            "Mars":    _p("Aries", 1, 5),
            "Mercury": _p("Libra", 7, 190),
            "Jupiter": _p("Aquarius", 11, 315),
            "Venus":   _p("Taurus", 2, 35),
            "Saturn":  _p("Cancer", 4, 100),
            "Rahu":    _p("Gemini", 3, 65),
            "Ketu":    _p("Sagittarius", 9, 250),
        },
    }
    r = check_balarishta(chart)
    assert r["has_risk"] is True
    assert any("Sun in 8th" in f and "Moon in 6th" in f for f in r["factors"])


def test_balarishta_cancelled_by_strong_jupiter():
    # Sun in 8th + Moon in 6th triggers Rule 4 regardless of aspects.
    # Jupiter in own sign (Pisces, house 12) in Kendra aspects Lagna and Moon.
    # Cancellation Rule 3: strong benefic in Kendra + no malefic on Lagna.
    # Jupiter in house 10 (Kendra) → aspects 4 (7th), 2 (5th), 6 (9th) — aspects Moon!
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Scorpio", 8, 220),       # Rule 4 trigger
            "Moon":    _p("Virgo", 6, 160),         # Rule 4 trigger
            "Mars":    _p("Sagittarius", 9, 250),   # far from Lagna
            "Mercury": _p("Libra", 7, 195),
            "Jupiter": _p("Cancer", 10, 100),       # exalted in Kendra — cancels
            "Venus":   _p("Taurus", 2, 35),
            "Saturn":  _p("Gemini", 3, 65),         # not aspecting Lagna
            "Rahu":    _p("Aquarius", 11, 315),
            "Ketu":    _p("Leo", 5, 135),
        },
    }
    r = check_balarishta(chart)
    # Rule 4 should trigger (Sun in 8 + Moon in 6)
    assert any("Sun in 8" in f for f in r["factors"])
    # Cancellation should fire (strong Jupiter in Kendra, no malefic on Lagna)
    assert r["cancelled"] is True
    assert r["has_risk"] is False


def test_no_balarishta_in_healthy_chart():
    # Moon in Lagna (not Dusthana), benefics well-placed, no Sun-Moon affliction
    chart = {
        "ascendant": {"sign": "Cancer", "longitude": 90},
        "planets": {
            "Sun":     _p("Aries", 10, 5),        # exalted in Kendra
            "Moon":    _p("Cancer", 1, 95),       # own sign in Lagna
            "Mars":    _p("Capricorn", 7, 280),   # exalted
            "Mercury": _p("Virgo", 3, 160),       # exalted
            "Jupiter": _p("Sagittarius", 6, 250), # own sign
            "Venus":   _p("Taurus", 11, 35),      # own sign
            "Saturn":  _p("Libra", 4, 190),       # exalted in Kendra
            "Rahu":    _p("Pisces", 9, 345),
            "Ketu":    _p("Virgo", 3, 165),
        },
    }
    r = check_balarishta(chart)
    assert r["has_risk"] is False
    assert r["risk_level"] == "low"


# ═══════════════════════════════════════════════════════════════
# AYU CLASSIFICATION
# ═══════════════════════════════════════════════════════════════

def test_dirghayu_strong_jupiter_and_lagna_lord():
    # Asc = Cancer (lord = Moon). Moon exalted in Taurus. Jupiter exalted in Cancer (Lagna).
    # 8th lord of Cancer = Saturn. Saturn in own sign (Capricorn) in 7th.
    chart = {
        "ascendant": {"sign": "Cancer", "longitude": 90},
        "planets": {
            "Sun":     _p("Aries", 10, 5),         # exalted
            "Moon":    _p("Taurus", 11, 35),       # exalted
            "Mars":    _p("Capricorn", 7, 280),    # exalted
            "Mercury": _p("Virgo", 3, 160),        # exalted
            "Jupiter": _p("Cancer", 1, 100),       # exalted in Lagna (Kendra + Trikona)
            "Venus":   _p("Pisces", 9, 345),       # exalted
            "Saturn":  _p("Capricorn", 7, 285),    # own sign in Kendra (8th lord)
            "Rahu":    _p("Aquarius", 8, 315),
            "Ketu":    _p("Leo", 2, 135),
        },
    }
    r = classify_ayu(chart)
    # Either Dirghayu or Purnayu are valid outcomes
    assert r["category"] in ("Dirghayu", "Purnayu")
    assert r["dirghayu_score"] >= 4
    assert len(r["matched_rules"]) >= 2


def test_purnayu_exceptional_case():
    # Exalted Lagna lord + Jupiter in Kendra/Trikona + strong Dirghayu score
    # Asc = Aries (lord Mars). Mars exalted in Capricorn → but Mars must be exalted AND in chart.
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 10),         # exalted
            "Moon":    _p("Taurus", 2, 35),        # exalted
            "Mars":    _p("Capricorn", 10, 285),   # exalted (Lagna lord in house 10 — Kendra)
            "Mercury": _p("Virgo", 6, 160),        # exalted
            "Jupiter": _p("Cancer", 4, 100),       # exalted in Kendra
            "Venus":   _p("Pisces", 12, 345),      # exalted
            "Saturn":  _p("Libra", 7, 190),        # exalted in Kendra
            "Rahu":    _p("Scorpio", 8, 220),
            "Ketu":    _p("Taurus", 2, 50),
        },
    }
    r = classify_ayu(chart)
    assert r["category"] == "Purnayu"
    assert "100+" in r["years_range"]


def test_alpayu_malefic_lagna_no_benefic():
    # Multiple Alpayu factors: Saturn+Mars+Moon in Lagna, Lagna lord in 8th
    # Asc = Aries (lord Mars). Mars in Lagna but not alone. Put Lagna lord in 8th instead.
    chart = {
        "ascendant": {"sign": "Leo", "longitude": 120},  # lord Sun
        "planets": {
            "Sun":     _p("Pisces", 8, 345),       # Lagna lord (Sun) in 8th house = Alpayu factor
            "Moon":    _p("Leo", 1, 125),
            "Mars":    _p("Leo", 1, 130),
            "Saturn":  _p("Leo", 1, 135),
            "Mercury": _p("Virgo", 2, 160),
            "Jupiter": _p("Capricorn", 6, 280),   # debilitated, in Dusthana
            "Venus":   _p("Scorpio", 4, 220),
            "Rahu":    _p("Cancer", 12, 100),
            "Ketu":    _p("Capricorn", 6, 285),
        },
    }
    r = classify_ayu(chart)
    assert r["category"] == "Alpayu"
    assert r["alpayu_score"] >= 3


def test_madhyayu_balanced_chart():
    # Balanced chart — neither strong Dirghayu nor Alpayu signals dominate
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Gemini", 3, 65),
            "Moon":    _p("Libra", 7, 190),
            "Mars":    _p("Leo", 5, 130),
            "Mercury": _p("Cancer", 4, 100),
            "Jupiter": _p("Virgo", 6, 160),       # Dusthana, debilitation nearby
            "Venus":   _p("Taurus", 2, 35),
            "Saturn":  _p("Sagittarius", 9, 250),
            "Rahu":    _p("Aquarius", 11, 315),
            "Ketu":    _p("Leo", 5, 135),
        },
    }
    r = classify_ayu(chart)
    assert r["category"] == "Madhyayu"
    assert "32" in r["years_range"]


# ═══════════════════════════════════════════════════════════════
# Graceful degradation
# ═══════════════════════════════════════════════════════════════

def test_empty_chart_balarishta():
    r = check_balarishta({})
    assert r["has_risk"] is False
    assert r["factors"] == []


def test_empty_chart_ayu():
    r = classify_ayu({})
    assert r["category"] == "Madhyayu"  # safe default
    assert r["dirghayu_score"] == 0
    assert r["alpayu_score"] == 0


def test_none_input():
    r = check_balarishta(None)  # type: ignore[arg-type]
    assert r["has_risk"] is False
    r2 = classify_ayu(None)  # type: ignore[arg-type]
    assert r2["category"] == "Madhyayu"


def test_balarishta_return_contract():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Sun": _p("Aries", 1, 5)},
    }
    r = check_balarishta(chart)
    assert set(r.keys()) >= {
        "has_risk", "risk_level", "factors",
        "remedies_recommended", "sloka_ref", "cancelled",
    }
    assert r["risk_level"] in ("low", "moderate", "high", "severe")


def test_ayu_return_contract():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {"Sun": _p("Aries", 1, 5)},
    }
    r = classify_ayu(chart)
    assert set(r.keys()) >= {
        "category", "category_en", "category_hi", "years_range",
        "reasoning_en", "reasoning_hi", "matched_rules", "sloka_ref",
        "dirghayu_score", "alpayu_score",
    }
    assert r["category"] in ("Alpayu", "Madhyayu", "Dirghayu", "Purnayu")
