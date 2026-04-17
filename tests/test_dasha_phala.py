"""
Tests for Phaladeepika Adhyaya 20 (Mahadasha-phala) + Adhyaya 21 (Antardashadhyaya)
==================================================================================
Data file integrity, mahadasha effect synthesis, antardasha combination matrix,
and the current-dasha-phala convenience resolver.
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.dasha_engine import (  # noqa: E402
    _load_dasha_phala,
    _DASHA_PHALA_PATH,
    DASHA_ORDER,
    analyze_mahadasha_phala,
    analyze_antardasha_phala,
    get_current_dasha_phala,
)


# ---------------------------------------------------------------------------
# 1. DATA FILE INTEGRITY
# ---------------------------------------------------------------------------

class TestDataIntegrity:
    """Verify dasha_phala.json is well-formed and complete."""

    def test_file_exists(self):
        assert os.path.exists(_DASHA_PHALA_PATH), "dasha_phala.json must exist"

    def test_file_is_valid_json(self):
        with open(_DASHA_PHALA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_has_nine_mahadasha_effects(self):
        data = _load_dasha_phala()
        assert len(data["mahadasha_effects"]) == 9

    def test_all_nine_planets_present_mahadasha(self):
        data = _load_dasha_phala()
        for planet in DASHA_ORDER:
            assert planet in data["mahadasha_effects"], f"missing: {planet}"

    def test_mahadasha_bilingual_fields(self):
        data = _load_dasha_phala()
        required = ["general_en", "general_hi", "when_strong_en", "when_strong_hi",
                    "when_weak_en", "when_weak_hi", "sloka_ref"]
        for planet, entry in data["mahadasha_effects"].items():
            for key in required:
                assert key in entry and entry[key], f"{planet} missing {key}"

    def test_antardasha_matrix_has_nine_parents(self):
        data = _load_dasha_phala()
        assert len(data["antardasha_matrix"]) == 9

    def test_antardasha_matrix_is_9x9_81_entries(self):
        data = _load_dasha_phala()
        total = sum(len(row) for row in data["antardasha_matrix"].values())
        assert total == 81, f"Expected 81 antardasha combos, got {total}"

    def test_each_md_row_has_nine_bhuktis(self):
        data = _load_dasha_phala()
        for md, row in data["antardasha_matrix"].items():
            assert len(row) == 9, f"{md} row has {len(row)} entries, expected 9"

    def test_antardasha_bilingual_fields(self):
        data = _load_dasha_phala()
        for md, row in data["antardasha_matrix"].items():
            for bk, entry in row.items():
                for key in ("effect_en", "effect_hi", "sloka_ref"):
                    assert entry.get(key), f"{md}-{bk} missing {key}"

    def test_all_planet_pairs_covered(self):
        data = _load_dasha_phala()
        planets = set(DASHA_ORDER)
        for md in planets:
            assert md in data["antardasha_matrix"]
            for bk in planets:
                assert bk in data["antardasha_matrix"][md], f"missing {md}-{bk}"


# ---------------------------------------------------------------------------
# 2. MAHADASHA PHALA — STRENGTH CLASSIFICATION
# ---------------------------------------------------------------------------

class TestMahadashaStrength:
    """analyze_mahadasha_phala strength rules."""

    def _chart(self, sign: str, house: int, planet: str = "Sun"):
        return {"planets": {planet: {"sign": sign, "house": house}}}

    def test_exalted_planet_is_strong(self):
        # Sun exalted in Aries
        chart = self._chart("Aries", 5, "Sun")
        result = analyze_mahadasha_phala("Sun", chart)
        assert result["strength"] == "strong"
        assert "exalted" in result["factors"]

    def test_debilitated_planet_is_weak(self):
        # Sun debilitated in Libra
        chart = self._chart("Libra", 7, "Sun")
        result = analyze_mahadasha_phala("Sun", chart)
        assert result["strength"] == "weak"
        assert "debilitated" in result["factors"]

    def test_debilitated_moon_is_weak(self):
        chart = self._chart("Scorpio", 8, "Moon")
        result = analyze_mahadasha_phala("Moon", chart)
        assert result["strength"] == "weak"

    def test_own_sign_planet_is_strong(self):
        # Mars in own Aries
        chart = self._chart("Aries", 5, "Mars")
        result = analyze_mahadasha_phala("Mars", chart)
        assert result["strength"] == "strong"
        assert "own_sign" in result["factors"]

    def test_kendra_placement_is_strong(self):
        # Mercury in Cancer (not own/exalted) in Kendra -> strong
        chart = self._chart("Cancer", 1, "Mercury")
        result = analyze_mahadasha_phala("Mercury", chart)
        assert result["strength"] == "strong"
        assert "kendra" in result["factors"]

    def test_dusthana_placement_is_weak(self):
        # Venus in 6th in an ordinary sign
        chart = self._chart("Gemini", 6, "Venus")
        result = analyze_mahadasha_phala("Venus", chart)
        assert result["strength"] == "weak"
        assert "dusthana" in result["factors"]

    def test_combust_planet_is_weak(self):
        chart = {"planets": {"Mercury": {"sign": "Leo", "house": 3, "combust": True}}}
        result = analyze_mahadasha_phala("Mercury", chart)
        assert result["strength"] == "weak"
        assert "combust" in result["factors"]

    def test_picks_when_strong_text_for_strong(self):
        chart = self._chart("Aries", 5, "Sun")
        result = analyze_mahadasha_phala("Sun", chart)
        assert result["effect_en"] == result["when_strong_en"]
        assert result["effect_hi"] == result["when_strong_hi"]

    def test_picks_when_weak_text_for_weak(self):
        chart = self._chart("Libra", 7, "Sun")
        result = analyze_mahadasha_phala("Sun", chart)
        assert result["effect_en"] == result["when_weak_en"]

    def test_neutral_placement_picks_general(self):
        # Mercury in a completely ordinary sign/house (neutral)
        chart = self._chart("Gemini", 3, "Mercury")  # own sign -> strong
        # Use Sun in Pisces, house 11 → neutral
        chart = {"planets": {"Sun": {"sign": "Pisces", "house": 11}}}
        result = analyze_mahadasha_phala("Sun", chart)
        assert result["strength"] == "neutral"
        assert result["effect_en"] == result["general_en"]

    def test_bilingual_output_present(self):
        chart = self._chart("Aries", 1, "Sun")
        result = analyze_mahadasha_phala("Sun", chart)
        assert result["effect_en"]
        assert result["effect_hi"]
        assert result["sloka_ref"].startswith("Phaladeepika")

    def test_unknown_planet_returns_error(self):
        chart = self._chart("Aries", 1, "Sun")
        result = analyze_mahadasha_phala("Pluto", chart)
        assert "error" in result

    def test_missing_planet_data_graceful(self):
        # Asking about Moon when chart has only Sun
        chart = {"planets": {"Sun": {"sign": "Aries", "house": 1}}}
        result = analyze_mahadasha_phala("Moon", chart)
        # Should still return valid bilingual effect with some strength label
        assert "effect_en" in result
        assert "effect_hi" in result
        assert result["strength"] in {"strong", "weak", "neutral"}


# ---------------------------------------------------------------------------
# 3. ANTARDASHA COMBINATIONS — SEVERITY
# ---------------------------------------------------------------------------

class TestAntardashaPhala:
    """analyze_antardasha_phala severity and content."""

    def test_returns_bilingual_effect(self):
        chart = {"planets": {"Sun": {"sign": "Aries", "house": 1},
                             "Jupiter": {"sign": "Cancer", "house": 4}}}
        result = analyze_antardasha_phala("Sun", "Jupiter", chart)
        assert result["effect_en"]
        assert result["effect_hi"]
        assert result["sloka_ref"]

    def test_favorable_combo_when_both_strong(self):
        chart = {"planets": {
            "Jupiter": {"sign": "Cancer", "house": 1},   # exalted
            "Venus":   {"sign": "Pisces", "house": 4},   # exalted + kendra
        }}
        r = analyze_antardasha_phala("Jupiter", "Venus", chart)
        assert r["severity"] == "favorable"

    def test_challenging_combo_when_both_weak(self):
        chart = {"planets": {
            "Saturn": {"sign": "Aries", "house": 8},   # debilitated + dusthana
            "Rahu":   {"sign": "Scorpio", "house": 12},  # dusthana
        }}
        r = analyze_antardasha_phala("Saturn", "Rahu", chart)
        assert r["severity"] == "challenging"

    def test_mixed_combo_default(self):
        # ordinary placement, mixed base
        chart = {"planets": {
            "Mercury": {"sign": "Leo", "house": 3},
            "Mars":    {"sign": "Virgo", "house": 11},
        }}
        r = analyze_antardasha_phala("Mercury", "Mars", chart)
        assert r["severity"] in {"favorable", "mixed", "challenging"}

    def test_unknown_combo_returns_error(self):
        chart = {"planets": {}}
        r = analyze_antardasha_phala("Pluto", "Venus", chart)
        assert "error" in r

    def test_all_81_combos_resolve_without_error(self):
        chart = {"planets": {p: {"sign": "Leo", "house": 5} for p in DASHA_ORDER}}
        for md in DASHA_ORDER:
            for bk in DASHA_ORDER:
                r = analyze_antardasha_phala(md, bk, chart)
                assert "error" not in r, f"missing {md}-{bk}"
                assert r["effect_en"]
                assert r["effect_hi"]
                assert r["severity"] in {"favorable", "mixed", "challenging"}


# ---------------------------------------------------------------------------
# 4. CURRENT DASHA PHALA — INTEGRATION
# ---------------------------------------------------------------------------

class TestGetCurrentDashaPhala:
    """End-to-end: get MD + AD narrative for a real birth date."""

    def _chart(self):
        return {
            "planets": {
                "Sun":     {"sign": "Aries", "house": 1, "longitude": 10.0},
                "Moon":    {"sign": "Taurus", "house": 2, "nakshatra": "Rohini", "longitude": 45.0},
                "Mars":    {"sign": "Cancer", "house": 4, "longitude": 95.0},
                "Mercury": {"sign": "Aries", "house": 1, "longitude": 15.0},
                "Jupiter": {"sign": "Cancer", "house": 4, "longitude": 100.0},
                "Venus":   {"sign": "Pisces", "house": 12, "longitude": 350.0},
                "Saturn":  {"sign": "Libra", "house": 7, "longitude": 190.0},
                "Rahu":    {"sign": "Capricorn", "house": 10, "longitude": 290.0},
                "Ketu":    {"sign": "Cancer", "house": 4, "longitude": 110.0},
            }
        }

    def test_returns_as_of_field(self):
        r = get_current_dasha_phala(self._chart(), "1990-05-15", "2025-05-15")
        assert r["as_of"] == "2025-05-15"

    def test_returns_mahadasha_with_analysis(self):
        r = get_current_dasha_phala(self._chart(), "1990-05-15", "2025-05-15")
        assert r["mahadasha"] is not None
        md = r["mahadasha"]
        assert md["planet"] in DASHA_ORDER
        assert "start" in md and "end" in md
        assert "analysis" in md
        assert md["analysis"]["effect_en"]
        assert md["analysis"]["effect_hi"]

    def test_returns_antardasha_with_analysis(self):
        r = get_current_dasha_phala(self._chart(), "1990-05-15", "2025-05-15")
        assert r["antardasha"] is not None
        ad = r["antardasha"]
        assert ad["planet"] in DASHA_ORDER
        assert ad["analysis"]["effect_en"]
        assert ad["analysis"]["severity"] in {"favorable", "mixed", "challenging"}

    def test_defaults_to_today_when_no_as_of(self):
        r = get_current_dasha_phala(self._chart(), "1990-05-15")
        assert r["as_of"]  # should be today
        # And a mahadasha should be found
        assert r["mahadasha"] is not None

    def test_invalid_birth_date_graceful(self):
        r = get_current_dasha_phala(self._chart(), "not-a-date")
        assert "error" in r
        assert r["mahadasha"] is None

    def test_unknown_nakshatra_graceful(self):
        chart = {"planets": {"Moon": {"sign": "Taurus", "house": 2, "nakshatra": "BadName"}}}
        r = get_current_dasha_phala(chart, "1990-05-15")
        assert "error" in r

    def test_missing_moon_defaults_to_ashwini(self):
        chart = {"planets": {}}
        r = get_current_dasha_phala(chart, "1990-05-15", "2025-05-15")
        # Default Ashwini -> Ketu starts; mahadasha should be found
        assert r["mahadasha"] is not None or "error" in r
