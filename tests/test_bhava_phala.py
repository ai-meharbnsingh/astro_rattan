"""Tests for Bhava Phala + Bhava-misra-phala — Phaladeepika Adh. 8 + 16."""
from app.bhava_phala_engine import (
    analyze_bhava_phala,
    load_bhava_phala_data,
    _house_strength,
    _planet_aspects_house,
    _is_strong_planet,
    _is_weak_planet,
)


def _p(sign: str, house: int, longitude: float = 0.0) -> dict:
    return {"sign": sign, "house": house, "longitude": longitude, "sign_degree": longitude % 30}


PLANETS_ALL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


# ═══════════════════════════════════════════════════════════════
# Data file integrity (108 planet×house entries + 12 bhavas)
# ═══════════════════════════════════════════════════════════════

def test_data_file_has_all_nine_planets():
    data = load_bhava_phala_data()
    assert set(data["planets"].keys()) == set(PLANETS_ALL)


def test_data_file_has_108_planet_house_entries():
    data = load_bhava_phala_data()
    count = sum(len(data["planets"][p]) for p in PLANETS_ALL)
    assert count == 108, f"Expected 108 planet×house entries, got {count}"


def test_every_planet_has_twelve_houses():
    data = load_bhava_phala_data()
    for p in PLANETS_ALL:
        houses = set(data["planets"][p].keys())
        assert houses == {str(i) for i in range(1, 13)}, f"{p} missing houses: {houses}"


def test_every_planet_house_entry_is_bilingual_with_sloka_ref():
    data = load_bhava_phala_data()
    for p in PLANETS_ALL:
        for h in range(1, 13):
            entry = data["planets"][p][str(h)]
            for key in ("effect_en", "effect_hi", "sloka_ref"):
                assert key in entry, f"{p}/{h} missing '{key}'"
                assert entry[key], f"{p}/{h} has empty '{key}'"


def test_data_file_has_all_12_bhavas():
    data = load_bhava_phala_data()
    assert set(data["bhavas"].keys()) == {str(i) for i in range(1, 13)}


def test_every_bhava_has_required_fields():
    data = load_bhava_phala_data()
    for h in range(1, 13):
        b = data["bhavas"][str(h)]
        for key in ("name_en", "name_hi", "general_en", "general_hi", "sloka_ref"):
            assert key in b, f"Bhava {h} missing '{key}'"
            assert b[key], f"Bhava {h} has empty '{key}'"


def test_bhava_names_cover_classical_list():
    """Tanu, Dhana, Sahaja, Sukha, Putra, Ari, Yuvati, Randhra, Bhagya, Karma, Labha, Vyaya."""
    data = load_bhava_phala_data()
    expected = ["Tanu", "Dhana", "Sahaja", "Sukha", "Putra", "Ari",
                "Yuvati", "Randhra", "Bhagya", "Karma", "Labha", "Vyaya"]
    for i, name in enumerate(expected, 1):
        assert name in data["bhavas"][str(i)]["name_en"], \
            f"Bhava {i} should contain '{name}' but got '{data['bhavas'][str(i)]['name_en']}'"


# ═══════════════════════════════════════════════════════════════
# Integration — analyze_bhava_phala on handcrafted chart
# ═══════════════════════════════════════════════════════════════

def _handcrafted_chart(ascendant_sign: str = "Aries") -> dict:
    """A full chart for testing: Aries ascendant, standard planet placements."""
    return {
        "ascendant": {"sign": ascendant_sign, "longitude": 0},
        "planets": {
            "Sun":     _p("Aries", 1, 10),     # exalted, in 1st
            "Moon":    _p("Taurus", 2, 35),    # exalted, in 2nd
            "Mars":    _p("Capricorn", 10, 280),  # exalted, in 10th
            "Mercury": _p("Virgo", 6, 160),    # exalted+own, in 6th
            "Jupiter": _p("Cancer", 4, 95),    # exalted, in 4th
            "Venus":   _p("Pisces", 12, 340),  # exalted, in 12th
            "Saturn":  _p("Libra", 7, 190),    # exalted, in 7th
            "Rahu":    _p("Taurus", 2, 40),
            "Ketu":    _p("Scorpio", 8, 220),
        },
    }


def test_analyze_returns_planet_placements_and_bhava_generals():
    chart = _handcrafted_chart()
    result = analyze_bhava_phala(chart)
    assert "planet_placements" in result
    assert "bhava_generals" in result
    assert result["sloka_ref"] == "Phaladeepika Adh. 8 + Adh. 16"
    # 9 planets, all placed
    assert len(result["planet_placements"]) == 9
    # 12 bhavas always
    assert len(result["bhava_generals"]) == 12


def test_planet_placement_payload_fields():
    chart = _handcrafted_chart()
    result = analyze_bhava_phala(chart)
    for pp in result["planet_placements"]:
        for key in ("planet", "house", "sign", "effect_en", "effect_hi", "sloka_ref"):
            assert key in pp
            assert pp[key] != "" or key == "sign"
        assert 1 <= pp["house"] <= 12


def test_bhava_generals_payload_fields():
    chart = _handcrafted_chart()
    result = analyze_bhava_phala(chart)
    for b in result["bhava_generals"]:
        for key in ("house", "name_en", "name_hi", "general_en", "general_hi", "sloka_ref", "status"):
            assert key in b
        assert b["status"] in {"strong", "weak", "neutral"}


def test_sun_in_1st_picks_classical_effect():
    chart = _handcrafted_chart()
    result = analyze_bhava_phala(chart)
    sun = next(p for p in result["planet_placements"] if p["planet"] == "Sun")
    assert sun["house"] == 1
    # Classical indicators
    assert "bilious" in sun["effect_en"].lower() or "short-tempered" in sun["effect_en"].lower()
    assert sun["sloka_ref"].startswith("Phaladeepika Adh. 8")


def test_jupiter_in_7th_virtuous_spouse():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Jupiter": _p("Libra", 7, 190),
        },
    }
    result = analyze_bhava_phala(chart)
    jup = next(p for p in result["planet_placements"] if p["planet"] == "Jupiter")
    assert jup["house"] == 7
    # Look for virtuous/learned spouse language
    effect = jup["effect_en"].lower()
    assert "spouse" in effect


# ═══════════════════════════════════════════════════════════════
# Bhava status — strong / weak / neutral
# ═══════════════════════════════════════════════════════════════

def test_lagna_strong_when_jupiter_aspects_and_lagna_lord_exalted():
    """Aries Lagna; Jupiter in 5th (Leo) aspects Lagna (9th aspect); Lagna lord
    Mars in Capricorn (exalted). Expect status of 1st = strong."""
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Mars":    _p("Capricorn", 10, 280),  # Lagna lord Mars, exalted → strong
            "Jupiter": _p("Leo", 5, 130),          # Jupiter aspects 9th from itself = Lagna (1st)
        },
    }
    # Jupiter in house 5 with special aspect of 9 hits house (5-1+9)%12+1 = 14%12+1 = 2+1 = 3
    # Hmm need to recompute: (5-1+9)%12 = 13%12 = 1, +1 = 2. Not Lagna.
    # Need Jupiter in house that aspects 1st: universal 7th from house means 1st is aspected from house 7.
    # Or Jupiter in house 9 has 5th aspect onto (9-1+5)%12+1 = 13%12+1 = 2. No.
    # Jupiter special aspects: 5,9. So Jupiter in H5 aspects H9 (via 5th) and H1 (via 9th aspect: (5-1+9)%12+1=2). Wrong.
    # Let me just re-check: planet in house X aspects house ((X-1+offset)%12)+1.
    # To aspect H1: ((X-1+offset)%12)+1 = 1 → (X-1+offset)%12 = 0 → X-1+offset ≡ 0 mod 12 → offset = 13-X mod 12.
    # For Jupiter with offsets {5,7,9}: X=8 gives offset 5; X=6 gives offset 7; X=4 gives offset 9.
    # So Jupiter in H4 has 9th aspect on H1 (Lagna). Or H6 has 7th. Or H8 has 5th.
    # Simplest: Jupiter in 7th house → universal 7th aspect onto H1.
    chart["planets"]["Jupiter"] = _p("Libra", 7, 190)  # 7th aspect → Lagna
    result = analyze_bhava_phala(chart)
    b1 = next(b for b in result["bhava_generals"] if b["house"] == 1)
    assert b1["status"] == "strong", \
        f"Expected strong Lagna with Jupiter aspect + Mars exalted, got {b1['status']}"


def test_house_weak_when_malefic_in_dusthana_with_weak_lord():
    """4th house weak: Saturn (malefic) in 4th, Moon (Lagna-lord-ish context)
    with no benefic aspect, and house lord (Moon for Aries → Cancer 4th) debilitated."""
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            # 4th house from Aries = Cancer → lord Moon.
            # Moon debilitated in Scorpio (placed in some house ≠ 4) → lord_weak
            "Moon":    _p("Scorpio", 8, 220),       # debilitated → lord weak + in dusthana
            "Saturn":  _p("Cancer", 4, 100),        # malefic occupant in 4th
            "Mars":    _p("Cancer", 4, 95),         # another malefic in 4th
        },
    }
    # No benefic occupant/aspect on 4th
    result = analyze_bhava_phala(chart)
    b4 = next(b for b in result["bhava_generals"] if b["house"] == 4)
    assert b4["status"] == "weak", \
        f"Expected weak 4th with malefic+weak lord, got {b4['status']}"


def test_house_neutral_when_no_strong_signal():
    """Empty 11th house, Jupiter (Aquarius→lord Saturn) in neutral position."""
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            # 11th from Aries = Aquarius → lord Saturn (not exalted/debilitated here)
            "Saturn":  _p("Gemini", 3, 70),   # neutral sign, no dusthana
        },
    }
    result = analyze_bhava_phala(chart)
    b11 = next(b for b in result["bhava_generals"] if b["house"] == 11)
    assert b11["status"] == "neutral"


# ═══════════════════════════════════════════════════════════════
# Helper tests
# ═══════════════════════════════════════════════════════════════

def test_planet_aspects_house_universal_seventh():
    # Planet in 1 aspects 7; in 4 aspects 10; in 7 aspects 1
    assert _planet_aspects_house("Sun", 1, 7)
    assert _planet_aspects_house("Sun", 4, 10)
    assert _planet_aspects_house("Sun", 7, 1)
    assert not _planet_aspects_house("Sun", 1, 2)


def test_planet_aspects_house_jupiter_special():
    # Jupiter in 1 has special aspects on 5 and 9
    assert _planet_aspects_house("Jupiter", 1, 5)
    assert _planet_aspects_house("Jupiter", 1, 9)
    assert _planet_aspects_house("Jupiter", 1, 7)  # universal
    assert not _planet_aspects_house("Jupiter", 1, 3)


def test_planet_aspects_house_saturn_special():
    # Saturn in 1 has special aspects on 3 and 10
    assert _planet_aspects_house("Saturn", 1, 3)
    assert _planet_aspects_house("Saturn", 1, 10)


def test_is_strong_planet():
    assert _is_strong_planet("Sun", "Aries")      # exalted
    assert _is_strong_planet("Sun", "Leo")        # own
    assert _is_strong_planet("Mars", "Capricorn") # exalted
    assert _is_strong_planet("Mars", "Aries")     # own
    assert not _is_strong_planet("Sun", "Libra")  # debilitated
    assert not _is_strong_planet("Sun", "")       # empty


def test_is_weak_planet():
    assert _is_weak_planet("Sun", "Libra")
    assert _is_weak_planet("Moon", "Scorpio")
    assert not _is_weak_planet("Sun", "Aries")


# ═══════════════════════════════════════════════════════════════
# Graceful degradation
# ═══════════════════════════════════════════════════════════════

def test_empty_chart_returns_12_bhavas_neutral():
    result = analyze_bhava_phala({})
    assert result["planet_placements"] == []
    assert len(result["bhava_generals"]) == 12
    assert all(b["status"] == "neutral" for b in result["bhava_generals"])


def test_none_input_returns_12_bhavas_neutral():
    result = analyze_bhava_phala(None)
    assert result["planet_placements"] == []
    assert len(result["bhava_generals"]) == 12


def test_missing_sign_or_house_skipped():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun": {"longitude": 10},             # missing house/sign
            "Moon": _p("Taurus", 2, 35),
        },
    }
    result = analyze_bhava_phala(chart)
    # Moon entry present; Sun skipped
    planets_out = {p["planet"] for p in result["planet_placements"]}
    assert "Moon" in planets_out
    assert "Sun" not in planets_out


def test_invalid_house_out_of_range_skipped():
    chart = {
        "ascendant": {"sign": "Aries", "longitude": 0},
        "planets": {
            "Sun": _p("Aries", 0, 5),          # invalid house
            "Moon": _p("Taurus", 13, 35),      # invalid house
            "Mars": _p("Aries", 1, 15),
        },
    }
    result = analyze_bhava_phala(chart)
    planets_out = {p["planet"] for p in result["planet_placements"]}
    assert "Mars" in planets_out
    assert "Sun" not in planets_out
    assert "Moon" not in planets_out
