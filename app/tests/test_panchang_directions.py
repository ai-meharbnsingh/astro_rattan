"""Tests for app.panchang_directions -- Directional & Anandadi Calculations."""
import pytest
from app.panchang_directions import (
    DISHA_SHOOL,
    BAANA_ELEMENTS,
    ANANDADI_YOGAS,
    LUCKY_INDICATORS,
    calculate_disha_shool,
    calculate_baana,
    calculate_anandadi_yoga,
    calculate_lucky_indicators,
    calculate_all_directions,
)


# ============================================================
# Disha Shool
# ============================================================
class TestDishaShool:
    """Validate Disha Shool calculations."""

    def test_disha_shool_has_7_entries(self):
        assert len(DISHA_SHOOL) == 7

    def test_sunday_is_east(self):
        result = calculate_disha_shool(0)
        assert result["direction"] == "East"
        assert result["direction_hindi"] == "पूर्व"

    def test_monday_is_west(self):
        result = calculate_disha_shool(1)
        assert result["direction"] == "West"
        assert result["direction_hindi"] == "पश्चिम"

    def test_tuesday_is_north(self):
        result = calculate_disha_shool(2)
        assert result["direction"] == "North"
        assert result["direction_hindi"] == "उत्तर"

    def test_thursday_is_south(self):
        result = calculate_disha_shool(4)
        assert result["direction"] == "South"
        assert result["direction_hindi"] == "दक्षिण"

    def test_saturday_is_east(self):
        result = calculate_disha_shool(6)
        assert result["direction"] == "East"

    def test_name_fields_present(self):
        result = calculate_disha_shool(0)
        assert result["name"] == "Disha Shool"
        assert result["name_hindi"] == "दिशा शूल"

    def test_weekday_wraps_modulo_7(self):
        """Weekday 7 should wrap to 0 (Sunday)."""
        result = calculate_disha_shool(7)
        assert result["direction"] == "East"


# ============================================================
# Baana
# ============================================================
class TestBaana:
    """Validate Baana element-direction calculations."""

    def test_baana_elements_has_5_entries(self):
        assert len(BAANA_ELEMENTS) == 5

    def test_tithi_1_is_agni_east(self):
        result = calculate_baana(1)
        assert result["element"] == "Agni"
        assert result["element_hindi"] == "अग्नि"
        assert result["direction"] == "East"
        assert result["direction_hindi"] == "पूर्व"

    def test_tithi_2_is_vayu(self):
        result = calculate_baana(2)
        assert result["element"] == "Vayu"
        assert result["element_hindi"] == "वायु"
        assert result["direction"] == "North-West"

    def test_tithi_3_is_jala(self):
        result = calculate_baana(3)
        assert result["element"] == "Jala"
        assert result["direction"] == "West"

    def test_tithi_4_is_prithvi(self):
        result = calculate_baana(4)
        assert result["element"] == "Prithvi"
        assert result["direction"] == "South"

    def test_tithi_5_is_akasha(self):
        result = calculate_baana(5)
        assert result["element"] == "Akasha"
        assert result["element_hindi"] == "आकाश"
        assert result["direction"] == "Overhead"
        assert result["direction_hindi"] == "ऊपर"

    def test_tithi_6_cycles_back_to_agni(self):
        """Tithi 6 should cycle back to Agni (same as tithi 1)."""
        result = calculate_baana(6)
        assert result["element"] == "Agni"

    def test_tithi_11_is_agni(self):
        result = calculate_baana(11)
        assert result["element"] == "Agni"

    def test_tithi_15_is_akasha(self):
        """Purnima (tithi 15) = Akasha."""
        result = calculate_baana(15)
        assert result["element"] == "Akasha"

    def test_tithi_30_is_akasha(self):
        """Amavasya (tithi 30) = Akasha."""
        result = calculate_baana(30)
        assert result["element"] == "Akasha"

    def test_name_fields_present(self):
        result = calculate_baana(1)
        assert result["name"] == "Baana"
        assert result["name_hindi"] == "बाण"


# ============================================================
# Anandadi Yoga
# ============================================================
class TestAnandadiYoga:
    """Validate Anandadi Yoga calculations."""

    def test_anandadi_has_28_entries(self):
        assert len(ANANDADI_YOGAS) == 28

    def test_sunday_ashwini_is_ananda(self):
        """Sunday (0) + Ashwini (0) => (0*7+0)%28 = 0 => Ananda."""
        result = calculate_anandadi_yoga(0, 0)
        assert result["name"] == "Ananda"
        assert result["name_hindi"] == "आनन्द"
        assert result["auspicious"] is True
        assert result["index"] == 0

    def test_monday_ashwini_is_mitra(self):
        """Monday (1) + Ashwini (0) => (1*7+0)%28 = 7 => Mitra."""
        result = calculate_anandadi_yoga(1, 0)
        assert result["name"] == "Mitra"
        assert result["index"] == 7
        assert result["auspicious"] is True

    def test_sunday_bharani_is_kaldanda(self):
        """Sunday (0) + Bharani (1) => (0*7+1)%28 = 1 => Kaldanda."""
        result = calculate_anandadi_yoga(0, 1)
        assert result["name"] == "Kaldanda"
        assert result["auspicious"] is False

    def test_tuesday_ashwini_is_siddhi(self):
        """Tuesday (2) + Ashwini (0) => (2*7+0)%28 = 14 => Siddhi."""
        result = calculate_anandadi_yoga(2, 0)
        assert result["name"] == "Siddhi"
        assert result["index"] == 14
        assert result["auspicious"] is True

    def test_saturday_revati_wraps(self):
        """Saturday (6) + Revati (26) => (6*7+26)%28 = 68%28 = 12 => Mrityu."""
        result = calculate_anandadi_yoga(6, 26)
        assert result["name"] == "Mrityu"
        assert result["index"] == 12
        assert result["auspicious"] is False

    def test_all_entries_have_hindi(self):
        """Every yoga in the table must have a non-empty Hindi name."""
        for name, name_hindi, auspicious in ANANDADI_YOGAS:
            assert len(name) > 0
            assert len(name_hindi) > 0
            assert isinstance(auspicious, bool)

    def test_auspicious_count(self):
        """Exactly 14 auspicious and 14 inauspicious yogas."""
        auspicious_count = sum(1 for _, _, a in ANANDADI_YOGAS if a)
        assert auspicious_count == 14
        assert len(ANANDADI_YOGAS) - auspicious_count == 14


# ============================================================
# Lucky Indicators
# ============================================================
class TestLuckyIndicators:
    """Validate Lucky Day Indicator calculations."""

    def test_lucky_indicators_has_7_entries(self):
        assert len(LUCKY_INDICATORS) == 7

    def test_sunday_copper_1_east(self):
        result = calculate_lucky_indicators(0)
        assert result["color"] == "Copper"
        assert result["color_hindi"] == "ताम्र"
        assert result["number"] == 1
        assert result["direction"] == "East"
        assert result["direction_hindi"] == "पूर्व"

    def test_tuesday_red_9_south(self):
        result = calculate_lucky_indicators(2)
        assert result["color"] == "Red"
        assert result["color_hindi"] == "लाल"
        assert result["number"] == 9
        assert result["direction"] == "South"

    def test_thursday_yellow_3_northeast(self):
        result = calculate_lucky_indicators(4)
        assert result["color"] == "Yellow"
        assert result["number"] == 3
        assert result["direction"] == "North-East"
        assert result["direction_hindi"] == "ईशान"

    def test_saturday_black_8_west(self):
        result = calculate_lucky_indicators(6)
        assert result["color"] == "Black"
        assert result["color_hindi"] == "काला"
        assert result["number"] == 8
        assert result["direction"] == "West"

    def test_name_fields_present(self):
        result = calculate_lucky_indicators(0)
        assert result["name"] == "Lucky Indicators"
        assert result["name_hindi"] == "शुभ संकेत"

    def test_weekday_wraps_modulo_7(self):
        result = calculate_lucky_indicators(7)
        assert result["color"] == "Copper"  # Same as Sunday (0)


# ============================================================
# Master Function
# ============================================================
class TestCalculateAllDirections:
    """Validate the master calculate_all_directions function."""

    def test_returns_all_four_keys(self):
        result = calculate_all_directions(weekday=0, tithi_index=1, nakshatra_index=0)
        assert "disha_shool" in result
        assert "baana" in result
        assert "anandadi_yoga" in result
        assert "lucky" in result

    def test_disha_shool_nested_correctly(self):
        result = calculate_all_directions(weekday=4, tithi_index=1, nakshatra_index=0)
        assert result["disha_shool"]["direction"] == "South"
        assert result["disha_shool"]["name"] == "Disha Shool"

    def test_baana_nested_correctly(self):
        result = calculate_all_directions(weekday=0, tithi_index=3, nakshatra_index=0)
        assert result["baana"]["element"] == "Jala"
        assert result["baana"]["name"] == "Baana"

    def test_anandadi_nested_correctly(self):
        result = calculate_all_directions(weekday=0, tithi_index=1, nakshatra_index=0)
        assert result["anandadi_yoga"]["name"] == "Ananda"
        assert result["anandadi_yoga"]["auspicious"] is True

    def test_lucky_nested_correctly(self):
        result = calculate_all_directions(weekday=6, tithi_index=1, nakshatra_index=0)
        assert result["lucky"]["color"] == "Black"
        assert result["lucky"]["number"] == 8

    def test_hindi_present_in_all_sections(self):
        """Every section must contain Hindi translations."""
        result = calculate_all_directions(weekday=3, tithi_index=7, nakshatra_index=10)
        assert "direction_hindi" in result["disha_shool"]
        assert "element_hindi" in result["baana"]
        assert "name_hindi" in result["anandadi_yoga"]
        assert "color_hindi" in result["lucky"]
