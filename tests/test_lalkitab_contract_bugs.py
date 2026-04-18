"""
tests/test_lalkitab_contract_bugs.py
====================================
TDD tests for contract bugs discovered in the LK Validation Report (2026-04-19).

Each test starts RED (fails against unfixed code), then passes GREEN after the fix.

Bug IDs match validation report priority levels:
  BUG-1  lalkitab_dasha.get_dasha_timeline() crashes on DD/MM/YYYY format
  BUG-2  lalkitab_dasha._calc_age() crashes on DD/MM/YYYY format
  BUG-3  lalkitab_chakar.detect_chakar_cycle() silently returns wrong 35yr
         result when first arg is not a string (should raise TypeError)
  BUG-4  lalkitab_prediction_studio.build_prediction_studio() crashes
         AttributeError when planet_positions is a list instead of dict
  BUG-5  lalkitab_milestones.calculate_age_milestones() crashes on DD/MM/YYYY
"""
import pytest


# ──────────────────────────────────────────────────────────────────────────────
# BUG-1 / BUG-2 — lalkitab_dasha date format robustness
# ──────────────────────────────────────────────────────────────────────────────

class TestDashaDateFormat:
    """get_dasha_timeline() and _calc_age() must accept DD/MM/YYYY gracefully."""

    def test_dasha_timeline_iso_format_works(self):
        from app.lalkitab_dasha import get_dasha_timeline
        result = get_dasha_timeline("1985-08-23", "2026-04-19")
        assert result["current_age"] == 40
        csg = result["current_saala_grah"]
        assert csg["planet"] in {"Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"}

    def test_dasha_timeline_ddmmyyyy_does_not_crash(self):
        """BUG-1: DD/MM/YYYY input must not raise ValueError — should normalise."""
        from app.lalkitab_dasha import get_dasha_timeline
        # Must not raise, must return same result as ISO version
        result = get_dasha_timeline("23/08/1985", "19/04/2026")
        assert result["current_age"] == 40

    def test_dasha_timeline_ddmmyyyy_matches_iso(self):
        """DD/MM/YYYY and ISO inputs for same date must produce identical results."""
        from app.lalkitab_dasha import get_dasha_timeline
        iso_result = get_dasha_timeline("1985-08-23", "2026-04-19")
        dmy_result = get_dasha_timeline("23/08/1985", "19/04/2026")
        assert iso_result["current_age"] == dmy_result["current_age"]
        assert iso_result["current_saala_grah"]["planet"] == dmy_result["current_saala_grah"]["planet"]

    def test_dasha_timeline_invalid_date_raises_value_error(self):
        """Genuinely invalid dates must raise ValueError (not crash with AttributeError)."""
        from app.lalkitab_dasha import get_dasha_timeline
        with pytest.raises(ValueError):
            get_dasha_timeline("99/99/9999", "2026-04-19")

    def test_dasha_saala_grah_at_age_40_is_rahu(self):
        """For birth 1985-08-23, age 40 (2025-2026) the Saala Grah is Rahu."""
        from app.lalkitab_dasha import get_dasha_timeline
        result = get_dasha_timeline("1985-08-23", "2026-04-19")
        assert result["current_saala_grah"]["planet"] == "Rahu"

    def test_dasha_timeline_current_date_ddmmyyyy(self):
        """Current date in DD/MM/YYYY must also be accepted."""
        from app.lalkitab_dasha import get_dasha_timeline
        result = get_dasha_timeline("1985-08-23", "19/04/2026")
        assert result["current_age"] == 40


# ──────────────────────────────────────────────────────────────────────────────
# BUG-3 — detect_chakar_cycle() type-safety
# ──────────────────────────────────────────────────────────────────────────────

class TestChakarTypeGuard:
    """detect_chakar_cycle() must raise TypeError when first arg is not a string."""

    def test_chakar_string_input_works(self):
        from app.lalkitab_chakar import detect_chakar_cycle
        result = detect_chakar_cycle("Taurus", ["Rahu"])
        assert result["cycle_length"] == 36
        assert result["trigger"] == "shadow_in_h1"

    def test_chakar_list_as_first_arg_raises_type_error(self):
        """BUG-3: list passed as ascendant_sign must raise TypeError, not silently
        return 35-year cycle with 'unknown_sign' trigger."""
        from app.lalkitab_chakar import detect_chakar_cycle
        with pytest.raises(TypeError, match="ascendant_sign"):
            detect_chakar_cycle([{"planet": "Rahu", "house": 1}], [])

    def test_chakar_dict_as_first_arg_raises_type_error(self):
        """dict passed as ascendant_sign must also raise TypeError."""
        from app.lalkitab_chakar import detect_chakar_cycle
        with pytest.raises(TypeError, match="ascendant_sign"):
            detect_chakar_cycle({"sign": "Taurus"}, [])

    def test_chakar_int_as_first_arg_raises_type_error(self):
        """int passed as ascendant_sign must raise TypeError."""
        from app.lalkitab_chakar import detect_chakar_cycle
        with pytest.raises(TypeError, match="ascendant_sign"):
            detect_chakar_cycle(2, [])

    def test_chakar_none_returns_unknown_sign(self):
        """None is a plausible 'not available' value — keep existing graceful degradation."""
        from app.lalkitab_chakar import detect_chakar_cycle
        result = detect_chakar_cycle(None)
        # None should still degrade gracefully (existing behaviour was correct for None)
        assert result["cycle_length"] == 35
        assert result["trigger"] == "unknown_sign"

    def test_chakar_empty_string_returns_unknown_sign(self):
        """Empty string should degrade gracefully (already correct)."""
        from app.lalkitab_chakar import detect_chakar_cycle
        result = detect_chakar_cycle("")
        assert result["cycle_length"] == 35
        assert result["trigger"] == "unknown_sign"

    def test_chakar_taurus_rahu_in_h1_is_36_sala(self):
        """Meharban Singh chart: Taurus asc + Rahu in H1 → 36-Sala."""
        from app.lalkitab_chakar import detect_chakar_cycle
        result = detect_chakar_cycle("Taurus", ["Rahu"])
        assert result["cycle_length"] == 36
        assert result["trigger"] == "shadow_in_h1"
        assert result["ascendant_lord"] == "Rahu"


# ──────────────────────────────────────────────────────────────────────────────
# BUG-4 — build_prediction_studio() type-safety
# ──────────────────────────────────────────────────────────────────────────────

class TestPredictionStudioTypeGuard:
    """build_prediction_studio() must raise TypeError when planet_positions is not a dict."""

    _MEHARBAN_POSITIONS = {
        "Sun": 5, "Moon": 8, "Mars": 4, "Mercury": 4,
        "Jupiter": 10, "Venus": 4, "Saturn": 7, "Rahu": 1, "Ketu": 7,
    }

    def test_prediction_studio_dict_input_works(self):
        from app.lalkitab_prediction_studio import build_prediction_studio
        result = build_prediction_studio(self._MEHARBAN_POSITIONS)
        assert "areas" in result
        assert len(result["areas"]) > 0

    def test_prediction_studio_list_raises_type_error(self):
        """BUG-4: list passed as planet_positions must raise TypeError, not AttributeError."""
        from app.lalkitab_prediction_studio import build_prediction_studio
        with pytest.raises(TypeError, match="planet_positions"):
            build_prediction_studio([{"planet": "Sun", "house": 5}])

    def test_prediction_studio_none_raises_type_error(self):
        """None as planet_positions must raise TypeError."""
        from app.lalkitab_prediction_studio import build_prediction_studio
        with pytest.raises(TypeError, match="planet_positions"):
            build_prediction_studio(None)

    def test_prediction_studio_string_raises_type_error(self):
        """string as planet_positions must raise TypeError."""
        from app.lalkitab_prediction_studio import build_prediction_studio
        with pytest.raises(TypeError, match="planet_positions"):
            build_prediction_studio("Sun:5,Moon:8")

    def test_prediction_studio_areas_non_empty(self):
        from app.lalkitab_prediction_studio import build_prediction_studio
        result = build_prediction_studio(self._MEHARBAN_POSITIONS)
        assert len(result["areas"]) >= 5

    def test_prediction_studio_score_in_range(self):
        from app.lalkitab_prediction_studio import build_prediction_studio
        result = build_prediction_studio(self._MEHARBAN_POSITIONS)
        for area in result["areas"]:
            assert 0 <= area["score"] <= 100, f"score out of range: {area}"

    def test_prediction_studio_has_source_field(self):
        from app.lalkitab_prediction_studio import build_prediction_studio
        result = build_prediction_studio(self._MEHARBAN_POSITIONS)
        # "PRODUCT" is the correct tag — prediction studio is a composite UX feature
        assert result.get("source") == "PRODUCT"


# ──────────────────────────────────────────────────────────────────────────────
# BUG-5 — calculate_age_milestones() date format robustness
# ──────────────────────────────────────────────────────────────────────────────

class TestMilestonesDateFormat:
    _POSITIONS = [
        {"planet": "Sun", "house": 5},
        {"planet": "Moon", "house": 8},
        {"planet": "Saturn", "house": 7},
    ]

    def test_milestones_iso_format_works(self):
        from app.lalkitab_milestones import calculate_age_milestones
        result = calculate_age_milestones("1985-08-23", self._POSITIONS)
        assert "milestones" in result
        assert "current_age" in result
        assert result["current_age"] == 40

    def test_milestones_ddmmyyyy_does_not_crash(self):
        """BUG-5: DD/MM/YYYY must not crash — should normalise."""
        from app.lalkitab_milestones import calculate_age_milestones
        result = calculate_age_milestones("23/08/1985", self._POSITIONS)
        assert result["current_age"] == 40

    def test_milestones_ddmmyyyy_matches_iso(self):
        from app.lalkitab_milestones import calculate_age_milestones
        iso_result = calculate_age_milestones("1985-08-23", self._POSITIONS)
        dmy_result = calculate_age_milestones("23/08/1985", self._POSITIONS)
        assert iso_result["current_age"] == dmy_result["current_age"]

    def test_milestones_invalid_date_raises_value_error(self):
        from app.lalkitab_milestones import calculate_age_milestones
        with pytest.raises(ValueError):
            calculate_age_milestones("99/99/9999", self._POSITIONS)
