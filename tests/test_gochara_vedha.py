"""Tests for Gochara Vedhas + Lattas — Phaladeepika Adh. 26."""
import pytest
from app.gochara_vedha_engine import (
    load_vedha_table,
    load_latta_table,
    apply_vedhas,
    apply_lattas,
    enrich_transits,
    _house_from_moon,
    _nakshatra_from_longitude,
    _nakshatra_distance,
    _is_exception_pair,
    NAKSHATRAS,
)


def _natal(moon_sign: str, moon_nakshatra: str = "", moon_longitude: float = 0.0) -> dict:
    return {
        "planets": {
            "Moon": {
                "sign": moon_sign,
                "nakshatra": moon_nakshatra,
                "longitude": moon_longitude,
                "house": 1,
            }
        }
    }


def _t(planet: str, sign: str, nakshatra: str = "", longitude: float = 0.0) -> dict:
    return {
        "planet": planet,
        "current_sign": sign,
        "nakshatra": nakshatra,
        "longitude": longitude,
    }


# ═══════════════════════════════════════════════════════════════
# Data file integrity
# ═══════════════════════════════════════════════════════════════

def test_vedha_table_has_all_planets():
    data = load_vedha_table()
    for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        assert p in data
        assert "good" in data[p]
        assert "vedhas" in data[p]


def test_latta_table_has_all_planets():
    data = load_latta_table()
    for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        assert p in data
        assert "prishta" in data[p]
        assert "pratyak" in data[p]


def test_exception_pairs():
    data = load_vedha_table()
    assert ["Sun", "Moon"] in data["exceptions"] or ["Moon", "Sun"] in data["exceptions"]
    assert ["Moon", "Saturn"] in data["exceptions"] or ["Saturn", "Moon"] in data["exceptions"]


def test_vedha_houses_are_valid():
    data = load_vedha_table()
    for planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        for good_h, vedha_h in data[planet]["vedhas"].items():
            assert 1 <= int(vedha_h) <= 12
            assert int(good_h) in data[planet]["good"]


# ═══════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════

def test_house_from_moon():
    # Moon in Aries, transit in Aries → house 1
    assert _house_from_moon("Aries", "Aries") == 1
    # Moon in Aries, transit in Libra → house 7 (opposite)
    assert _house_from_moon("Aries", "Libra") == 7
    # Moon in Cancer, transit in Pisces → 9 months back = 9 signs ahead from Cancer: 4,5,6,7,8,9,10,11,12 → Pisces is 9th
    assert _house_from_moon("Cancer", "Pisces") == 9


def test_nakshatra_from_longitude():
    # 0° → Ashwini (1st)
    assert _nakshatra_from_longitude(0) == "Ashwini"
    # ~13.34° → Bharani (2nd, starts at 13.33)
    assert _nakshatra_from_longitude(14) == "Bharani"
    # Wrap-around: 360° → Ashwini
    assert _nakshatra_from_longitude(360) == "Ashwini"


def test_nakshatra_distance():
    # Same nakshatra → 1
    assert _nakshatra_distance("Ashwini", "Ashwini") == 1
    # Ashwini → Bharani = 2
    assert _nakshatra_distance("Ashwini", "Bharani") == 2
    # Ashwini → Revati = 27 (wrap-around end)
    assert _nakshatra_distance("Ashwini", "Revati") == 27
    # Revati → Ashwini = 2 (wraps)
    assert _nakshatra_distance("Revati", "Ashwini") == 2


def test_is_exception_pair():
    data = load_vedha_table()
    assert _is_exception_pair("Sun", "Moon", data)
    assert _is_exception_pair("Moon", "Sun", data)
    assert _is_exception_pair("Moon", "Saturn", data)
    assert not _is_exception_pair("Sun", "Mars", data)


# ═══════════════════════════════════════════════════════════════
# Vedha — table-driven rule verification
# ═══════════════════════════════════════════════════════════════

@pytest.mark.parametrize("transit_planet, good_house, vedha_house", [
    ("Sun",     3,  9),
    ("Sun",     6,  12),
    ("Sun",     10, 4),
    ("Sun",     11, 5),
    ("Mars",    3,  12),
    ("Mars",    6,  9),
    ("Mars",    11, 5),
    ("Jupiter", 2,  12),
    ("Jupiter", 5,  4),
    ("Jupiter", 11, 8),
    ("Saturn",  3,  12),
    ("Saturn",  6,  9),
    ("Saturn",  11, 5),
])
def test_vedha_cancellation_table(transit_planet, good_house, vedha_house):
    """For each (planet, good_house, vedha_house) entry, verify cancellation fires."""
    # Moon in Aries. House N from Aries = Aries(1), Taurus(2), ...
    # Put transit_planet in sign at good_house, a canceller (non-exception) in sign at vedha_house.
    from app.gochara_vedha_engine import ZODIAC
    moon_sign = "Aries"
    good_sign = ZODIAC[(0 + good_house - 1) % 12]
    vedha_sign = ZODIAC[(0 + vedha_house - 1) % 12]
    # Pick a canceller that isn't an exception for transit_planet
    if transit_planet in ("Sun", "Moon"):
        canceller = "Mars"
    elif transit_planet == "Saturn":
        canceller = "Mars"
    else:
        canceller = "Saturn"

    transits = [
        _t(transit_planet, good_sign),
        _t(canceller, vedha_sign),
    ]
    result = apply_vedhas(transits, _natal(moon_sign))
    t_entry = next(t for t in result if t["planet"] == transit_planet)
    assert t_entry["vedha_active"] is True, f"{transit_planet} at house {good_house} should be cancelled by {canceller} at house {vedha_house}"
    assert t_entry["vedha_by"]["planet"] == canceller


def test_vedha_sun_moon_exception():
    """Sun and Moon don't vedha each other (Adh. 26 sloka 33)."""
    # Moon in Aries (natal). Sun transits Gemini (house 3 from Moon — good).
    # Moon transits Sagittarius (house 9 — would be Sun's vedha) but exception.
    moon_sign = "Aries"
    transits = [
        _t("Sun", "Gemini"),        # house 3
        _t("Moon", "Sagittarius"),  # house 9 — would vedha Sun
    ]
    result = apply_vedhas(transits, _natal(moon_sign))
    sun_entry = next(t for t in result if t["planet"] == "Sun")
    # Should NOT be cancelled (Moon is exception)
    assert sun_entry["vedha_active"] is False


def test_vedha_moon_saturn_exception():
    """Moon and Saturn don't vedha each other."""
    moon_sign = "Aries"
    # Moon transits house 3 (Gemini) — good for Moon; Saturn transits house 9 (Sagittarius)
    transits = [
        _t("Moon", "Gemini"),
        _t("Saturn", "Sagittarius"),
    ]
    result = apply_vedhas(transits, _natal(moon_sign))
    moon_entry = next(t for t in result if t["planet"] == "Moon")
    assert moon_entry["vedha_active"] is False


def test_vedha_not_triggered_when_transit_not_in_good_house():
    """If transit is not in a good house, vedha doesn't apply (no cancellation)."""
    moon_sign = "Aries"
    # Sun at house 2 (not in Sun's good list [3,6,10,11])
    transits = [
        _t("Sun", "Taurus"),         # house 2 — not good
        _t("Mars", "Sagittarius"),   # house 9
    ]
    result = apply_vedhas(transits, _natal(moon_sign))
    sun_entry = next(t for t in result if t["planet"] == "Sun")
    assert sun_entry["vedha_active"] is False


def test_multiple_vedhas_still_cancels():
    """Multiple planets in the vedha house — still just one cancellation (first found)."""
    moon_sign = "Aries"
    # Sun at house 3 (good), both Mars AND Saturn at house 9 (vedha)
    transits = [
        _t("Sun", "Gemini"),         # house 3 good
        _t("Mars", "Sagittarius"),   # house 9 vedha
        _t("Saturn", "Sagittarius"), # house 9 vedha
    ]
    result = apply_vedhas(transits, _natal(moon_sign))
    sun_entry = next(t for t in result if t["planet"] == "Sun")
    assert sun_entry["vedha_active"] is True


# ═══════════════════════════════════════════════════════════════
# Latta
# ═══════════════════════════════════════════════════════════════

def test_latta_prishta_detected():
    """Sun's prishta distance = 12. If natal Moon in Ashwini (1st nak) and Sun transits 12th nak → +25%."""
    # 12th nakshatra = Uttara Phalguni (index 11)
    natal = _natal("Aries", moon_nakshatra="Ashwini", moon_longitude=0)
    # Transit Sun at start of Uttara Phalguni → ~147° abs
    transits = [_t("Sun", "Leo", nakshatra="Uttara Phalguni", longitude=147.0)]
    result = apply_lattas(transits, natal)
    sun = result[0]
    assert sun["latta_type"] == "prishta"
    assert sun["latta_modifier"] == 1.25


def test_latta_pratyak_detected():
    """Sun's pratyak distance = 16. Natal Ashwini → transit at 16th nak → −25%."""
    # 16th nakshatra = Vishakha (index 15)
    natal = _natal("Aries", moon_nakshatra="Ashwini", moon_longitude=0)
    transits = [_t("Sun", "Libra", nakshatra="Vishakha", longitude=200.0)]
    result = apply_lattas(transits, natal)
    sun = result[0]
    assert sun["latta_type"] == "pratyak"
    assert sun["latta_modifier"] == 0.75


def test_latta_no_match_normal():
    """If transit nakshatra doesn't hit prishta or pratyak distance → modifier = 1.0."""
    natal = _natal("Aries", moon_nakshatra="Ashwini")
    # Sun at 3rd nak (Krittika) — neither 12 nor 16 for Sun
    transits = [_t("Sun", "Aries", nakshatra="Krittika", longitude=28.0)]
    result = apply_lattas(transits, natal)
    assert result[0]["latta_modifier"] == 1.0
    assert result[0]["latta_type"] is None


def test_latta_all_planets_have_entries():
    """Every classical planet should get latta fields applied."""
    natal = _natal("Aries", moon_nakshatra="Ashwini")
    transits = [
        _t("Sun",     "Leo",    "Magha",      120),
        _t("Moon",    "Taurus", "Rohini",     40),
        _t("Mars",    "Cancer", "Pushya",     100),
        _t("Mercury", "Virgo",  "Hasta",      160),
        _t("Jupiter", "Cancer", "Pushya",     100),
        _t("Venus",   "Libra",  "Chitra",     180),
        _t("Saturn",  "Capricorn", "Shravana", 280),
    ]
    result = apply_lattas(transits, natal)
    for t in result:
        assert "latta_modifier" in t
        assert "latta_type" in t


# ═══════════════════════════════════════════════════════════════
# enrich_transits — integration
# ═══════════════════════════════════════════════════════════════

def test_enrich_transits_applies_both():
    """Full enrichment should include vedha + latta + sloka_ref fields."""
    natal = _natal("Aries", moon_nakshatra="Ashwini")
    transits = [
        _t("Sun", "Gemini", nakshatra="Mrigashira", longitude=65),   # house 3 from Aries-Moon
        _t("Mars", "Sagittarius", nakshatra="Mula", longitude=245),  # house 9 — Sun's vedha
    ]
    result = enrich_transits(transits, natal)
    sun = next(t for t in result if t["planet"] == "Sun")
    assert "vedha_active" in sun
    assert "latta_modifier" in sun
    assert "sloka_ref" in sun


def test_enrich_empty_transits():
    assert enrich_transits([], {}) == []


def test_enrich_no_natal_moon_graceful():
    """Without natal Moon, vedha/latta shouldn't crash — just no cancellations."""
    transits = [_t("Sun", "Gemini", nakshatra="Mrigashira")]
    result = enrich_transits(transits, {})
    assert result[0]["vedha_active"] is False
    assert result[0].get("latta_modifier") == 1.0


def test_vedha_preserves_original_fields():
    """apply_vedhas should not destroy original transit dict fields."""
    natal = _natal("Aries")
    t_input = _t("Sun", "Gemini")
    t_input["custom_field"] = "keep_me"
    result = apply_vedhas([t_input], natal)
    assert result[0]["custom_field"] == "keep_me"


def test_return_contract():
    natal = _natal("Aries", moon_nakshatra="Ashwini")
    transits = [_t("Sun", "Gemini", "Mrigashira", 65)]
    result = enrich_transits(transits, natal)
    for t in result:
        assert "planet" in t
        assert "effect_base" in t
        assert "effect_final" in t
        assert "vedha_active" in t
        assert "latta_modifier" in t
        assert "sloka_ref" in t
