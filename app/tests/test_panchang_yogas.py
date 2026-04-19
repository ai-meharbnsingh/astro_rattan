"""
Tests for app.panchang_yogas -- Special Yoga Calculations
=========================================================
Each yoga is tested with known positive and negative cases.
"""
import pytest

from app.panchang_yogas import (
    calculate_sarvartha_siddhi,
    calculate_amrit_siddhi,
    calculate_dwipushkar,
    calculate_tripushkar,
    calculate_ganda_moola,
    calculate_all_special_yogas,
    _normalise_tithi,
)


# ============================================================
# _normalise_tithi helper
# ============================================================

class TestNormaliseTithi:
    def test_shukla_tithis_unchanged(self):
        for i in range(1, 16):
            assert _normalise_tithi(i) == i

    def test_krishna_tithis_normalised(self):
        assert _normalise_tithi(16) == 1   # Krishna Pratipada
        assert _normalise_tithi(22) == 7   # Krishna Saptami
        assert _normalise_tithi(30) == 15  # Amavasya → maps to 15

    def test_invalid_tithi_raises(self):
        with pytest.raises(ValueError):
            _normalise_tithi(0)
        with pytest.raises(ValueError):
            _normalise_tithi(31)
        with pytest.raises(ValueError):
            _normalise_tithi(-1)


# ============================================================
# Sarvartha Siddhi Yoga
# ============================================================

class TestSarvarthaSiddhi:
    def test_active_tithi_match_sunday_dwitiya(self):
        """Sunday (0) + Dwitiya (2) → active via tithi."""
        result = calculate_sarvartha_siddhi(0, 2, "Bharani")
        assert result["active"] is True
        assert result["type"] == "partial"
        assert result["name"] == "Sarvartha Siddhi Yoga"
        assert result["name_hindi"] == "सर्वार्थ सिद्धि योग"

    def test_active_nakshatra_match_sunday_pushya(self):
        """Sunday (0) + Pushya nakshatra → active via nakshatra."""
        result = calculate_sarvartha_siddhi(0, 4, "Pushya")  # tithi 4 not in Sunday list
        assert result["active"] is True
        assert result["type"] == "partial"

    def test_active_both_match_whole_day(self):
        """Sunday (0) + Dwitiya (2) + Hasta → whole_day (both match)."""
        result = calculate_sarvartha_siddhi(0, 2, "Hasta")
        assert result["active"] is True
        assert result["type"] == "whole_day"

    def test_inactive_no_match(self):
        """Sunday (0) + Chaturthi (4) + Bharani → inactive."""
        result = calculate_sarvartha_siddhi(0, 4, "Bharani")
        assert result["active"] is False

    def test_tuesday_tithi_match(self):
        """Tuesday (2) + Pratipada (1) → active via tithi."""
        result = calculate_sarvartha_siddhi(2, 1, "Bharani")
        assert result["active"] is True

    def test_saturday_purnima(self):
        """Saturday (6) + Purnima (15) → active via tithi."""
        result = calculate_sarvartha_siddhi(6, 15, "Bharani")
        assert result["active"] is True

    def test_krishna_paksha_tithi_normalised(self):
        """Sunday (0) + Krishna Dwitiya (17) → normalises to 2 → active."""
        result = calculate_sarvartha_siddhi(0, 17, "Bharani")
        assert result["active"] is True

    def test_wednesday_anuradha(self):
        """Wednesday (3) + Anuradha → active via nakshatra."""
        result = calculate_sarvartha_siddhi(3, 1, "Anuradha")
        assert result["active"] is True

    def test_thursday_revati(self):
        """Thursday (4) + Revati → active via nakshatra."""
        result = calculate_sarvartha_siddhi(4, 1, "Revati")
        assert result["active"] is True


# ============================================================
# Amrit Siddhi Yoga
# ============================================================

class TestAmritSiddhi:
    def test_active_sunday_hasta(self):
        result = calculate_amrit_siddhi(0, "Hasta")
        assert result["active"] is True
        assert result["name"] == "Amrit Siddhi Yoga"
        assert result["name_hindi"] == "अमृत सिद्धि योग"

    def test_active_monday_rohini(self):
        result = calculate_amrit_siddhi(1, "Rohini")
        assert result["active"] is True

    def test_active_tuesday_ashwini(self):
        result = calculate_amrit_siddhi(2, "Ashwini")
        assert result["active"] is True

    def test_active_wednesday_anuradha(self):
        result = calculate_amrit_siddhi(3, "Anuradha")
        assert result["active"] is True

    def test_active_thursday_punarvasu(self):
        result = calculate_amrit_siddhi(4, "Punarvasu")
        assert result["active"] is True

    def test_active_friday_revati(self):
        result = calculate_amrit_siddhi(5, "Revati")
        assert result["active"] is True

    def test_active_saturday_shravana(self):
        result = calculate_amrit_siddhi(6, "Shravana")
        assert result["active"] is True

    def test_inactive_wrong_nakshatra(self):
        """Sunday + Rohini → inactive (needs Hasta)."""
        result = calculate_amrit_siddhi(0, "Rohini")
        assert result["active"] is False

    def test_inactive_wrong_weekday(self):
        """Monday + Hasta → inactive (Monday needs Rohini)."""
        result = calculate_amrit_siddhi(1, "Hasta")
        assert result["active"] is False


# ============================================================
# Dwipushkar Yoga
# ============================================================

class TestDwipushkar:
    # Dwipushkar tithis corrected to [3,8,13] (Tritiya/Ashtami/Trayodashi)
    # verified: Drik Panchang fires Tripushkar (not Dwipushkar) for Dwitiya+Krittika+Sunday (Apr 19 2026)
    def test_active_sunday_tritiya_chitra(self):
        """Sunday (0) + Tritiya (3) + Chitra → active."""
        result = calculate_dwipushkar(0, 3, "Chitra")
        assert result["active"] is True
        assert result["name"] == "Dwipushkar Yoga"
        assert result["name_hindi"] == "द्विपुष्कर योग"

    def test_active_tuesday_ashtami_mrigashira(self):
        """Tuesday (2) + Ashtami (8) + Mrigashira → active."""
        result = calculate_dwipushkar(2, 8, "Mrigashira")
        assert result["active"] is True

    def test_active_saturday_trayodashi_vishakha(self):
        """Saturday (6) + Trayodashi (13) + Vishakha → active."""
        result = calculate_dwipushkar(6, 13, "Vishakha")
        assert result["active"] is True

    def test_inactive_wrong_weekday(self):
        """Monday (1) + Tritiya (3) + Chitra → inactive (Monday not valid)."""
        result = calculate_dwipushkar(1, 3, "Chitra")
        assert result["active"] is False

    def test_inactive_wrong_tithi(self):
        """Sunday (0) + Dwitiya (2) + Chitra → inactive (Dwitiya not in Dwipushkar tithis)."""
        result = calculate_dwipushkar(0, 2, "Chitra")
        assert result["active"] is False

    def test_inactive_wrong_nakshatra(self):
        """Sunday (0) + Tritiya (3) + Rohini → inactive (wrong nakshatra)."""
        result = calculate_dwipushkar(0, 3, "Rohini")
        assert result["active"] is False

    def test_krishna_paksha_normalised(self):
        """Sunday (0) + Krishna Tritiya (18) + Chitra → active (18 normalises to 3)."""
        result = calculate_dwipushkar(0, 18, "Chitra")
        assert result["active"] is True

    def test_purva_ashadha(self):
        """Tuesday (2) + Ashtami (8) + Purva Ashadha → active."""
        result = calculate_dwipushkar(2, 8, "Purva Ashadha")
        assert result["active"] is True


# ============================================================
# Tripushkar Yoga
# ============================================================

class TestTripushkar:
    # Tripushkar tithis corrected to [2,7,12] (Dwitiya/Saptami/Dwadashi)
    # verified: Drik Panchang fires Tripushkar for Dwitiya+Krittika+Sunday (Apr 19 2026, Delhi)
    def test_active_sunday_dwitiya_krittika(self):
        """Sunday (0) + Dwitiya (2) + Krittika → active."""
        result = calculate_tripushkar(0, 2, "Krittika")
        assert result["active"] is True
        assert result["name"] == "Tripushkar Yoga"
        assert result["name_hindi"] == "त्रिपुष्कर योग"

    def test_active_tuesday_saptami_punarvasu(self):
        """Tuesday (2) + Saptami (7) + Punarvasu → active."""
        result = calculate_tripushkar(2, 7, "Punarvasu")
        assert result["active"] is True

    def test_active_saturday_dwadashi_vishakha(self):
        """Saturday (6) + Dwadashi (12) + Vishakha → active."""
        result = calculate_tripushkar(6, 12, "Vishakha")
        assert result["active"] is True

    def test_inactive_wrong_weekday(self):
        """Thursday (4) + Dwitiya (2) + Krittika → inactive (Thursday not valid)."""
        result = calculate_tripushkar(4, 2, "Krittika")
        assert result["active"] is False

    def test_inactive_wrong_tithi(self):
        """Sunday (0) + Tritiya (3) + Krittika → inactive (Tritiya not in Tripushkar tithis)."""
        result = calculate_tripushkar(0, 3, "Krittika")
        assert result["active"] is False

    def test_inactive_wrong_nakshatra(self):
        """Sunday (0) + Dwitiya (2) + Rohini → inactive (wrong nakshatra)."""
        result = calculate_tripushkar(0, 2, "Rohini")
        assert result["active"] is False

    def test_krishna_paksha_normalised(self):
        """Sunday (0) + Krishna Dwitiya (17) + Krittika → active (17 normalises to 2)."""
        result = calculate_tripushkar(0, 17, "Krittika")
        assert result["active"] is True

    def test_uttara_ashadha(self):
        """Tuesday (2) + Saptami (7) + Uttara Ashadha → active."""
        result = calculate_tripushkar(2, 7, "Uttara Ashadha")
        assert result["active"] is True


# ============================================================
# Ganda Moola
# ============================================================

class TestGandaMoola:
    def test_active_ashwini(self):
        result = calculate_ganda_moola("Ashwini")
        assert result["active"] is True
        assert result["nakshatra"] == "Ashwini"
        assert result["name"] == "Ganda Moola"
        assert result["name_hindi"] == "गण्ड मूल"

    def test_active_ashlesha(self):
        result = calculate_ganda_moola("Ashlesha")
        assert result["active"] is True

    def test_active_magha(self):
        result = calculate_ganda_moola("Magha")
        assert result["active"] is True

    def test_active_jyeshtha(self):
        result = calculate_ganda_moola("Jyeshtha")
        assert result["active"] is True

    def test_active_moola(self):
        result = calculate_ganda_moola("Moola")
        assert result["active"] is True

    def test_active_revati(self):
        result = calculate_ganda_moola("Revati")
        assert result["active"] is True

    def test_inactive_rohini(self):
        result = calculate_ganda_moola("Rohini")
        assert result["active"] is False
        assert result["nakshatra"] == "Rohini"

    def test_inactive_pushya(self):
        result = calculate_ganda_moola("Pushya")
        assert result["active"] is False

    def test_inactive_hasta(self):
        result = calculate_ganda_moola("Hasta")
        assert result["active"] is False


# ============================================================
# Master function — calculate_all_special_yogas
# ============================================================

class TestCalculateAllSpecialYogas:
    def test_returns_all_keys(self):
        result = calculate_all_special_yogas(0, 1, "Rohini")
        expected_keys = {
            "sarvartha_siddhi",
            "amrit_siddhi",
            "dwipushkar",
            "tripushkar",
            "ganda_moola",
        }
        assert set(result.keys()) == expected_keys

    def test_each_value_is_dict_with_active(self):
        result = calculate_all_special_yogas(0, 1, "Rohini")
        for key, val in result.items():
            assert isinstance(val, dict), f"{key} should be a dict"
            assert "active" in val, f"{key} should have 'active' key"

    def test_sunday_dwitiya_hasta_multiple_active(self):
        """Sunday + Dwitiya + Hasta → Sarvartha (whole_day) + Amrit Siddhi both active."""
        result = calculate_all_special_yogas(0, 2, "Hasta")
        assert result["sarvartha_siddhi"]["active"] is True
        assert result["sarvartha_siddhi"]["type"] == "whole_day"
        assert result["amrit_siddhi"]["active"] is True

    def test_all_inactive_scenario(self):
        """Monday (1) + Chaturthi (4) + Bharani → nothing active."""
        result = calculate_all_special_yogas(1, 4, "Bharani")
        assert result["sarvartha_siddhi"]["active"] is False
        assert result["amrit_siddhi"]["active"] is False
        assert result["dwipushkar"]["active"] is False
        assert result["tripushkar"]["active"] is False
        assert result["ganda_moola"]["active"] is False

    def test_ganda_moola_active_with_ashwini(self):
        """Tuesday (2) + any tithi + Ashwini → at least ganda_moola active."""
        result = calculate_all_special_yogas(2, 5, "Ashwini")
        assert result["ganda_moola"]["active"] is True

    def test_dwipushkar_active_scenario(self):
        """Sunday (0) + Tritiya (3) + Chitra → dwipushkar active."""
        result = calculate_all_special_yogas(0, 3, "Chitra")
        assert result["dwipushkar"]["active"] is True

    def test_tripushkar_active_scenario(self):
        """Saturday (6) + Dwadashi (12) + Vishakha → tripushkar active."""
        result = calculate_all_special_yogas(6, 12, "Vishakha")
        assert result["tripushkar"]["active"] is True
