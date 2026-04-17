"""Tests for Lagna profile + Moon-Nakshatra predictions — Phaladeepika Adh. 9 + 10."""
from app.lagna_nakshatra_engine import (
    analyze_lagna_profile,
    analyze_moon_nakshatra,
    analyze_janma_predictions,
    load_lagna_profiles,
    load_nakshatra_predictions,
    get_nakshatra_index,
    get_pada,
    ZODIAC_SIGNS,
    NAKSHATRAS,
)


# ═══════════════════════════════════════════════════════════════
# Data-file integrity — 12 Lagnas
# ═══════════════════════════════════════════════════════════════

def test_lagna_data_has_all_twelve_signs():
    data = load_lagna_profiles()
    assert set(data.keys()) == set(ZODIAC_SIGNS)


def test_every_lagna_entry_has_required_fields():
    data = load_lagna_profiles()
    required = (
        "body_type_en", "body_type_hi",
        "temperament_en", "temperament_hi",
        "fortune_en", "fortune_hi",
        "lucky_directions_en", "lucky_directions_hi",
        "sloka_ref",
    )
    for sign, entry in data.items():
        for key in required:
            assert key in entry, f"{sign} missing '{key}'"
            assert entry[key], f"{sign} has empty '{key}'"
        assert isinstance(entry["lucky_directions_en"], list)
        assert isinstance(entry["lucky_directions_hi"], list)
        assert len(entry["lucky_directions_en"]) >= 1
        assert len(entry["lucky_directions_hi"]) >= 1
        assert len(entry["lucky_directions_en"]) == len(entry["lucky_directions_hi"])


def test_every_lagna_entry_is_bilingual():
    """EN and HI must both be non-empty and differ (basic bilingual check)."""
    data = load_lagna_profiles()
    for sign, entry in data.items():
        for en_key, hi_key in (
            ("body_type_en", "body_type_hi"),
            ("temperament_en", "temperament_hi"),
            ("fortune_en", "fortune_hi"),
        ):
            assert entry[en_key] and entry[hi_key]
            assert entry[en_key] != entry[hi_key], f"{sign}: {en_key} equals {hi_key}"


def test_every_lagna_has_sloka_ref_to_adh9():
    data = load_lagna_profiles()
    for sign, entry in data.items():
        assert "Adh. 9" in entry["sloka_ref"], f"{sign} sloka_ref: {entry['sloka_ref']}"


# ═══════════════════════════════════════════════════════════════
# Data-file integrity — 27 Nakshatras
# ═══════════════════════════════════════════════════════════════

def test_nakshatra_data_has_all_27_entries():
    data = load_nakshatra_predictions()
    assert set(data.keys()) == set(NAKSHATRAS)


def test_every_nakshatra_entry_has_required_fields():
    data = load_nakshatra_predictions()
    required = (
        "deity_en", "deity_hi", "symbol_en", "symbol_hi",
        "character_en", "character_hi",
        "strengths_en", "strengths_hi",
        "vulnerabilities_en", "vulnerabilities_hi",
        "career_affinity_en", "career_affinity_hi",
        "sloka_ref",
    )
    for name, entry in data.items():
        for key in required:
            assert key in entry, f"{name} missing '{key}'"
            assert entry[key], f"{name} has empty '{key}'"


def test_every_nakshatra_lists_parity():
    """EN/HI list lengths must match for lists; strengths/vulns/career non-empty."""
    data = load_nakshatra_predictions()
    for name, entry in data.items():
        for en_key, hi_key in (
            ("strengths_en", "strengths_hi"),
            ("vulnerabilities_en", "vulnerabilities_hi"),
            ("career_affinity_en", "career_affinity_hi"),
        ):
            assert isinstance(entry[en_key], list)
            assert isinstance(entry[hi_key], list)
            assert len(entry[en_key]) >= 1, f"{name}: {en_key} empty"
            assert len(entry[en_key]) == len(entry[hi_key]), f"{name}: {en_key}/{hi_key} length mismatch"


def test_every_nakshatra_has_sloka_ref_to_adh10():
    data = load_nakshatra_predictions()
    for name, entry in data.items():
        assert "Adh. 10" in entry["sloka_ref"], f"{name} sloka_ref: {entry['sloka_ref']}"


# ═══════════════════════════════════════════════════════════════
# Pada / nakshatra index from longitude
# ═══════════════════════════════════════════════════════════════

def test_get_nakshatra_index_ashwini_at_zero():
    assert get_nakshatra_index(0.0) == 0


def test_get_nakshatra_index_ashwini_near_end():
    assert get_nakshatra_index(13.3) == 0


def test_get_nakshatra_index_bharani_at_boundary():
    assert get_nakshatra_index(13.3334) == 1


def test_get_nakshatra_index_revati_end():
    assert get_nakshatra_index(359.99) == 26


def test_get_nakshatra_index_wraps_mod_360():
    assert get_nakshatra_index(360.0) == 0
    assert get_nakshatra_index(720.5) == get_nakshatra_index(0.5)


def test_get_pada_1_at_zero():
    assert get_pada(0.0) == 1


def test_get_pada_2_at_3p333():
    assert get_pada(3.334) == 2


def test_get_pada_3_at_6p667():
    assert get_pada(6.6667) == 3


def test_get_pada_4_at_10():
    assert get_pada(10.0) == 4


def test_get_pada_wraps_to_next_nakshatra_pada1():
    assert get_pada(13.3334) == 1


# ═══════════════════════════════════════════════════════════════
# analyze_lagna_profile
# ═══════════════════════════════════════════════════════════════

def test_analyze_lagna_profile_aries():
    chart = {"ascendant": {"sign": "Aries", "longitude": 0}, "planets": {}}
    result = analyze_lagna_profile(chart)
    assert result["lagna_sign"] == "Aries"
    assert result["lagna_sign_hi"] == "मेष"
    assert result["body_type_en"]
    assert result["body_type_hi"]
    assert result["temperament_en"]
    assert result["temperament_hi"]
    assert result["fortune_en"]
    assert result["fortune_hi"]
    assert len(result["lucky_directions_en"]) >= 1
    assert "Adh. 9" in result["sloka_ref"]


def test_analyze_lagna_profile_pisces():
    chart = {"ascendant": {"sign": "Pisces", "longitude": 340}, "planets": {}}
    result = analyze_lagna_profile(chart)
    assert result["lagna_sign"] == "Pisces"
    assert result["lagna_sign_hi"] == "मीन"
    assert "Adh. 9" in result["sloka_ref"]


def test_analyze_lagna_profile_unknown_sign_graceful():
    chart = {"ascendant": {"sign": "NotASign", "longitude": 0}, "planets": {}}
    result = analyze_lagna_profile(chart)
    assert result["lagna_sign"] == "NotASign"
    assert result["body_type_en"] == ""
    assert result["lucky_directions_en"] == []


def test_analyze_lagna_profile_empty_chart_graceful():
    result = analyze_lagna_profile({})
    assert result["lagna_sign"] == ""
    assert result["body_type_en"] == ""
    assert result["sloka_ref"]  # default preserved


# ═══════════════════════════════════════════════════════════════
# analyze_moon_nakshatra
# ═══════════════════════════════════════════════════════════════

def test_analyze_moon_nakshatra_ashwini_pada1_at_zero():
    chart = {"planets": {"Moon": {"longitude": 0.0, "sign": "Aries", "sign_degree": 0.0}}}
    result = analyze_moon_nakshatra(chart)
    assert result["nakshatra"] == "Ashwini"
    assert result["pada"] == 1
    assert result["deity_en"].startswith("Ashwini Kumaras")
    assert "अश्विनी" in result["deity_hi"]
    assert len(result["strengths_en"]) >= 1
    assert len(result["strengths_hi"]) == len(result["strengths_en"])
    assert "Adh. 10" in result["sloka_ref"]


def test_analyze_moon_nakshatra_pada_progression():
    """Within Ashwini (0..13.333°), padas 1→4 step every 3.333°."""
    def _chart(lon: float) -> dict:
        return {"planets": {"Moon": {"longitude": lon}}}

    assert analyze_moon_nakshatra(_chart(0.0))["pada"] == 1
    assert analyze_moon_nakshatra(_chart(3.334))["pada"] == 2
    assert analyze_moon_nakshatra(_chart(6.667))["pada"] == 3
    assert analyze_moon_nakshatra(_chart(10.0))["pada"] == 4
    for lon in (0.0, 3.334, 6.667, 10.0):
        assert analyze_moon_nakshatra(_chart(lon))["nakshatra"] == "Ashwini"


def test_analyze_moon_nakshatra_bharani_pada1_at_13p333():
    chart = {"planets": {"Moon": {"longitude": 13.334}}}
    result = analyze_moon_nakshatra(chart)
    assert result["nakshatra"] == "Bharani"
    assert result["pada"] == 1


def test_analyze_moon_nakshatra_revati_at_end():
    chart = {"planets": {"Moon": {"longitude": 359.0}}}
    result = analyze_moon_nakshatra(chart)
    assert result["nakshatra"] == "Revati"
    assert 1 <= result["pada"] <= 4


def test_analyze_moon_nakshatra_reconstruct_from_sign_and_sign_degree():
    """When only sign + sign_degree are present, reconstruct longitude."""
    # Moon in Taurus at 5° = 30 + 5 = 35° → nakshatra idx = 35 / 13.333... = 2 (Krittika)
    chart = {"planets": {"Moon": {"sign": "Taurus", "sign_degree": 5.0}}}
    result = analyze_moon_nakshatra(chart)
    assert result["nakshatra"] == "Krittika"


def test_analyze_moon_nakshatra_missing_moon_graceful():
    result = analyze_moon_nakshatra({"planets": {}})
    assert result["nakshatra"] == ""
    assert result["pada"] == 0
    assert result["strengths_en"] == []
    assert result["sloka_ref"]


def test_analyze_moon_nakshatra_empty_chart_graceful():
    result = analyze_moon_nakshatra({})
    assert result["nakshatra"] == ""
    assert result["pada"] == 0


def test_analyze_moon_nakshatra_none_input_graceful():
    result = analyze_moon_nakshatra(None)
    assert result["nakshatra"] == ""
    assert result["pada"] == 0


# ═══════════════════════════════════════════════════════════════
# Integration — analyze_janma_predictions
# ═══════════════════════════════════════════════════════════════

def test_analyze_janma_predictions_combined_output():
    chart = {
        "ascendant": {"sign": "Leo", "longitude": 125.0},
        "planets": {
            "Moon": {"longitude": 45.0, "sign": "Taurus", "sign_degree": 15.0},
        },
    }
    result = analyze_janma_predictions(chart)
    assert "lagna_profile" in result
    assert "moon_nakshatra" in result
    assert result["lagna_profile"]["lagna_sign"] == "Leo"
    # 45° → nakshatra idx = 45 / 13.333 = 3 (Rohini)
    assert result["moon_nakshatra"]["nakshatra"] == "Rohini"
    assert result["combined_narrative_en"]
    assert result["combined_narrative_hi"]
    assert "Leo" in result["combined_narrative_en"]
    assert "Rohini" in result["combined_narrative_en"]
    assert "Adh. 9 + Adh. 10" in result["sloka_ref"]


def test_analyze_janma_predictions_empty_chart_graceful():
    result = analyze_janma_predictions({})
    assert result["lagna_profile"]["lagna_sign"] == ""
    assert result["moon_nakshatra"]["nakshatra"] == ""
    assert result["combined_narrative_en"] == ""
    assert result["combined_narrative_hi"] == ""
    assert "Adh. 9 + Adh. 10" in result["sloka_ref"]


def test_analyze_janma_predictions_lagna_only_narrative():
    chart = {"ascendant": {"sign": "Scorpio"}, "planets": {}}
    result = analyze_janma_predictions(chart)
    assert result["lagna_profile"]["lagna_sign"] == "Scorpio"
    assert result["moon_nakshatra"]["nakshatra"] == ""
    assert "Scorpio" in result["combined_narrative_en"]


def test_analyze_janma_predictions_moon_only_narrative():
    chart = {"planets": {"Moon": {"longitude": 0.0}}}
    result = analyze_janma_predictions(chart)
    assert result["lagna_profile"]["lagna_sign"] == ""
    assert result["moon_nakshatra"]["nakshatra"] == "Ashwini"
    assert "Ashwini" in result["combined_narrative_en"]
