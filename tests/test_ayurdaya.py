"""Tests for 3-method Ayurdaya — Phaladeepika Adh. 22."""
from app.ayurdaya_engine import (
    pindayu, nisargayu, amsayu,
    apply_haranas,
    calculate_lifespan,
    _strongest_of_sun_moon_lagna,
    _navamsa_sign,
    _is_combust,
    PINDAYU_MAX_YEARS,
    HUMAN_MAX_LIFESPAN,
)


def _p(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {"sign": sign, "house": house, "longitude": longitude, "sign_degree": longitude % 30}


# ═══════════════════════════════════════════════════════════════
# Helper tests
# ═══════════════════════════════════════════════════════════════

def test_navamsa_of_aries_start():
    # 0° Aries → 1st navamsa → starts at same sign (movable) → Aries
    assert _navamsa_sign(0.0) == "Aries"
    # 3.5° Aries → 2nd navamsa → Taurus
    assert _navamsa_sign(4.0) == "Taurus"


def test_navamsa_of_taurus_fixed():
    # Fixed sign Taurus → navamsa starts from 9th sign (Capricorn)
    # 0° Taurus (abs 30°) → 1st navamsa → Capricorn
    assert _navamsa_sign(30.0) == "Capricorn"


def test_navamsa_of_gemini_dual():
    # Dual sign Gemini → starts from 5th (Libra)
    # 0° Gemini (abs 60°) → 1st navamsa → Libra
    assert _navamsa_sign(60.0) == "Libra"


def test_is_combust():
    planets = {
        "Sun": _p("Aries", 1, 10.0),
        "Mercury": _p("Aries", 1, 15.0),     # 5° from Sun
        "Venus": _p("Taurus", 2, 45.0),      # 35° from Sun — not combust
        "Moon": _p("Cancer", 4, 100.0),
    }
    assert _is_combust("Mercury", planets) is True
    assert _is_combust("Venus", planets) is False
    assert _is_combust("Sun", planets) is False       # never combusts itself


# ═══════════════════════════════════════════════════════════════
# Method tests
# ═══════════════════════════════════════════════════════════════

def test_pindayu_returns_contract():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {p: _p("Aries", 1, 5) for p in PINDAYU_MAX_YEARS},
    }
    # Add nodes so ascendant/planets dict is complete
    chart["planets"]["Rahu"] = _p("Libra", 7, 190)
    chart["planets"]["Ketu"] = _p("Aries", 1, 10)
    r = pindayu(chart)
    assert set(r.keys()) >= {"raw", "after_haranas", "haranas", "breakdown"}
    # Sum of all contributions must be ≤ total max (19+25+15+12+15+21+20 = 127)
    assert r["raw"] <= sum(PINDAYU_MAX_YEARS.values())
    assert r["raw"] > 0
    # breakdown has an entry for every planet
    assert len(r["breakdown"]) == len(PINDAYU_MAX_YEARS)
    assert all("contribution" in b for b in r["breakdown"])


def test_pindayu_exalted_planets_give_max():
    # All planets exalted → ratio ~ 1.0, raw should be near the theoretical max
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 10),         # exalted
            "Moon":    _p("Taurus", 2, 35),        # exalted
            "Mars":    _p("Capricorn", 10, 285),   # exalted (Kendra bonus)
            "Mercury": _p("Virgo", 6, 160),        # exalted
            "Jupiter": _p("Cancer", 4, 100),       # exalted (Kendra bonus)
            "Venus":   _p("Pisces", 12, 345),      # exalted
            "Saturn":  _p("Libra", 7, 190),        # exalted (Kendra bonus)
            "Rahu":    _p("Gemini", 3, 65),
            "Ketu":    _p("Sagittarius", 9, 250),
        },
    }
    r = pindayu(chart)
    # Sum of max years = 127. With all exalted → ≥ 100 expected
    assert r["raw"] >= 100


def test_nisargayu_moon_exalted_kendra():
    chart = {
        "ascendant": {"sign": "Sagittarius", "longitude": 240},
        "planets": {
            "Moon":    _p("Taurus", 6, 35),       # exalted, but in Dusthana
            "Sun":     _p("Aries", 5, 5),
            "Mars":    _p("Capricorn", 2, 280),
            "Mercury": _p("Gemini", 7, 65),
            "Jupiter": _p("Sagittarius", 1, 250),
            "Venus":   _p("Pisces", 4, 345),
            "Saturn":  _p("Libra", 11, 190),
        },
    }
    # Moon exalted but in 6th → Dusthana override kicks in
    r = nisargayu(chart)
    assert r["raw"] > 0
    assert r["raw"] <= HUMAN_MAX_LIFESPAN


def test_nisargayu_moon_in_dusthana_lower():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Moon":    _p("Gemini", 6, 65),      # Dusthana
            "Mars":    _p("Taurus", 2, 35),      # aspects 8th not Moon
            "Sun":     _p("Leo", 5, 130),
            "Mercury": _p("Cancer", 4, 100),
            "Jupiter": _p("Sagittarius", 9, 250),
            "Venus":   _p("Libra", 7, 190),
            "Saturn":  _p("Capricorn", 10, 280),
        },
    }
    r = nisargayu(chart)
    assert r["raw"] < 70  # Dusthana placement pulls it below 70


def test_nisargayu_missing_moon():
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {}}
    r = nisargayu(chart)
    assert r["raw"] > 0


def test_amsayu_returns_contract():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 10),
            "Moon":    _p("Taurus", 2, 35),
            "Mars":    _p("Capricorn", 10, 285),
            "Mercury": _p("Virgo", 6, 160),
            "Jupiter": _p("Cancer", 4, 100),
            "Venus":   _p("Pisces", 12, 345),
            "Saturn":  _p("Libra", 7, 190),
        },
    }
    r = amsayu(chart)
    assert set(r.keys()) >= {"raw", "after_haranas", "haranas", "breakdown"}
    assert r["raw"] > 0
    # breakdown should cover 7 planets when all present
    assert len(r["breakdown"]) == 7
    for b in r["breakdown"]:
        assert {"planet", "navamsa", "factor", "contribution"}.issubset(b.keys())


# ═══════════════════════════════════════════════════════════════
# Harana tests
# ═══════════════════════════════════════════════════════════════

def test_apply_haranas_no_reduction_when_clean():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 10),
            "Moon":    _p("Taurus", 2, 35),
            "Mars":    _p("Capricorn", 10, 285),
            "Mercury": _p("Gemini", 3, 65),
            "Jupiter": _p("Sagittarius", 9, 250),
            "Venus":   _p("Taurus", 2, 40),
            "Saturn":  _p("Libra", 7, 190),
        },
    }
    r = apply_haranas(100.0, chart)
    # Clean chart should apply few or no haranas
    assert r["final_years"] >= 70  # minimal reduction
    assert isinstance(r["haranas_applied"], list)


def test_raja_harana_when_lagna_lord_debilitated():
    # Asc = Aries, lord = Mars. Mars in Cancer (debilitated) in 4th, no benefic aspect.
    # Keep all benefics away from aspecting house 4:
    # Jupiter at house 11 → aspects 5, 3, 7 (none = 4)
    # Venus at house 1 → aspects 7 (not 4)
    # Mercury at house 5 → aspects 11 (not 4)
    # Moon at house 10 → aspects 4 via 7th ❌. Put Moon at 2 → aspects 8. Good.
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Leo", 5, 135),
            "Moon":    _p("Taurus", 2, 35),
            "Mars":    _p("Cancer", 4, 100),     # debilitated Lagna lord in Kendra-ish but debilitated
            "Mercury": _p("Leo", 5, 130),
            "Jupiter": _p("Aquarius", 11, 315),  # aspects 5,3,7 — none hit Mars in 4
            "Venus":   _p("Aries", 1, 5),
            "Saturn":  _p("Scorpio", 8, 220),
            "Rahu":    _p("Virgo", 6, 160),
            "Ketu":    _p("Pisces", 12, 340),
        },
    }
    # Mars in 4 (Kendra) but debilitated — Raja Harana requires debilitated OR in Dusthana.
    # Our Lagna lord is in 4 (not Dusthana) but IS debilitated. Rule should fire.
    r = apply_haranas(90.0, chart)
    assert any(h["name"] == "Raja Harana" for h in r["haranas_applied"])


def test_astangata_harana_for_combust():
    # Two combust planets — must show reduction
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 10.0),
            "Mercury": _p("Aries", 1, 13.0),    # 3° from Sun — combust
            "Venus":   _p("Aries", 1, 18.0),    # 8° from Sun — combust
            "Moon":    _p("Taurus", 2, 40.0),
            "Mars":    _p("Capricorn", 10, 285.0),
            "Jupiter": _p("Sagittarius", 9, 250.0),
            "Saturn":  _p("Libra", 7, 190.0),
        },
    }
    r = apply_haranas(100.0, chart)
    assert any(h["name"] == "Astangata Harana" for h in r["haranas_applied"])


def test_haranas_floor_at_zero():
    # Impossible combo that would reduce below 0 — must clamp at 0
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Libra", 7, 190),       # debilitated
            "Moon":    _p("Scorpio", 8, 220),     # Dusthana debil
            "Mars":    _p("Cancer", 4, 100),      # debilitated
            "Mercury": _p("Pisces", 12, 345),     # debilitated, Dusthana
            "Jupiter": _p("Capricorn", 10, 280),  # debilitated
            "Venus":   _p("Virgo", 6, 160),       # debilitated, Dusthana
            "Saturn":  _p("Aries", 1, 5),         # debilitated
        },
    }
    r = apply_haranas(10.0, chart)
    assert r["final_years"] >= 0


# ═══════════════════════════════════════════════════════════════
# Selector tests
# ═══════════════════════════════════════════════════════════════

def test_selector_sun_strongest():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 10),       # exalted in Kendra
            "Moon":    _p("Virgo", 6, 160),      # weak
            "Mars":    _p("Gemini", 3, 65),      # not great for Lagna lord
        },
    }
    assert _strongest_of_sun_moon_lagna(chart) == "sun"


def test_selector_moon_strongest():
    chart = {
        "ascendant": {"sign": "Sagittarius", "longitude": 240},
        "planets": {
            "Moon":    _p("Taurus", 6, 35),      # exalted (even in 6, still high score)
            "Sun":     _p("Libra", 11, 190),     # debilitated
            "Jupiter": _p("Virgo", 10, 160),     # neutral placement — Lagna lord
        },
    }
    # Moon exalted (3) + 6th (Dusthana -1) = 2; Sun debil (-2); Jupiter in Kendra (1.5) = 1.5
    assert _strongest_of_sun_moon_lagna(chart) == "moon"


def test_selector_lagna_strongest():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun":     _p("Libra", 7, 190),      # debilitated
            "Moon":    _p("Scorpio", 8, 220),    # debil + Dusthana
            "Mars":    _p("Capricorn", 10, 285), # Lagna lord exalted in Kendra
        },
    }
    assert _strongest_of_sun_moon_lagna(chart) == "lagna"


# ═══════════════════════════════════════════════════════════════
# Integration test — calculate_lifespan
# ═══════════════════════════════════════════════════════════════

def test_calculate_lifespan_full_chart():
    chart = {
        "ascendant": {"sign": "Cancer", "longitude": 90},
        "planets": {
            "Sun":     _p("Aries", 10, 5),
            "Moon":    _p("Taurus", 11, 35),
            "Mars":    _p("Capricorn", 7, 280),
            "Mercury": _p("Virgo", 3, 160),
            "Jupiter": _p("Cancer", 1, 100),
            "Venus":   _p("Pisces", 9, 345),
            "Saturn":  _p("Libra", 4, 190),
            "Rahu":    _p("Aquarius", 8, 315),
            "Ketu":    _p("Leo", 2, 135),
        },
    }
    r = calculate_lifespan(chart)
    assert set(r.keys()) >= {
        "pindayu", "nisargayu", "amsayu",
        "selected_method", "selection_reason_en", "selection_reason_hi",
        "final_years", "classification", "sloka_ref",
    }
    assert r["selected_method"] in ("pindayu", "nisargayu", "amsayu")
    assert r["classification"] in ("Alpayu", "Madhyayu", "Dirghayu", "Purnayu")
    assert 0 <= r["final_years"] <= HUMAN_MAX_LIFESPAN


def test_lifespan_capped_at_108():
    # Construct a chart that would produce very high raw years
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {p: _p("Aries", 1, 10) for p in PINDAYU_MAX_YEARS},
    }
    r = calculate_lifespan(chart)
    assert r["final_years"] <= HUMAN_MAX_LIFESPAN


def test_calculate_lifespan_gandhi_range():
    # Gandhi lived to 78.4 — approximate positions (for contract test, not exact match)
    chart = {
        "ascendant": {"sign": "Libra", "longitude": 180},
        "planets": {
            "Sun":     _p("Virgo", 12, 170),
            "Moon":    _p("Scorpio", 2, 220),
            "Mars":    _p("Scorpio", 2, 225),    # own sign
            "Mercury": _p("Virgo", 12, 165),     # exalted
            "Jupiter": _p("Sagittarius", 3, 250),
            "Venus":   _p("Libra", 1, 190),      # own sign in Lagna
            "Saturn":  _p("Sagittarius", 3, 255),
            "Rahu":    _p("Aries", 7, 5),
            "Ketu":    _p("Libra", 1, 195),
        },
    }
    r = calculate_lifespan(chart)
    # All three methods produce non-negative, capped values
    for method in ("pindayu", "nisargayu", "amsayu"):
        years = r[method]["after_haranas"]
        assert 0 <= years <= HUMAN_MAX_LIFESPAN, f"{method} out of range: {years}"
    # Final selection should give some meaningful lifespan
    assert r["final_years"] > 0


# ═══════════════════════════════════════════════════════════════
# Graceful degradation
# ═══════════════════════════════════════════════════════════════

def test_lifespan_empty_chart():
    r = calculate_lifespan({})
    assert r["final_years"] >= 0
    assert r["classification"] in ("Alpayu", "Madhyayu", "Dirghayu", "Purnayu")


def test_lifespan_none_input():
    r = calculate_lifespan(None)  # type: ignore[arg-type]
    assert r["final_years"] >= 0
