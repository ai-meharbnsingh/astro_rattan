"""
Tests for app.panchang_nivas -- Nivas, Homahuti & Kumbha Chakra Calculations
=============================================================================
Covers Chandra Vasa, Agnivasa, Rahu Vasa, Shivavasa, Homahuti, Kumbha Chakra.
"""
import pytest

from app.panchang_nivas import (
    CHANDRA_VASA_RANGES,
    AGNIVASA_ELEMENTS,
    RAHU_VASA,
    SHIVAVASA_LOCATIONS,
    HOMAHUTI_PLANETS,
    HOMAHUTI_HINDI,
    KUMBHA_CHAKRA,
    calculate_chandra_vasa,
    calculate_agnivasa,
    calculate_rahu_vasa,
    calculate_shivavasa,
    calculate_homahuti,
    calculate_kumbha_chakra,
    calculate_all_nivas,
)


# Helper: check Devanagari characters present
def _has_hindi(text: str) -> bool:
    return any("\u0900" <= ch <= "\u097f" for ch in text)


# ============================================================
# Chandra Vasa
# ============================================================
class TestChandraVasa:
    """Validate Chandra Vasa (Moon residence) calculations."""

    def test_ashwini_is_east(self):
        result = calculate_chandra_vasa(0)
        assert result["direction"] == "East"
        assert result["direction_hindi"] == "पूर्व"

    def test_nakshatra_6_is_east(self):
        """Last nakshatra in East group (index 6 = Punarvasu)."""
        result = calculate_chandra_vasa(6)
        assert result["direction"] == "East"

    def test_nakshatra_7_is_south(self):
        """First nakshatra in South group (index 7 = Pushya)."""
        result = calculate_chandra_vasa(7)
        assert result["direction"] == "South"
        assert result["direction_hindi"] == "दक्षिण"

    def test_nakshatra_13_is_south(self):
        result = calculate_chandra_vasa(13)
        assert result["direction"] == "South"

    def test_nakshatra_14_is_west(self):
        """First nakshatra in West group (index 14 = Swati)."""
        result = calculate_chandra_vasa(14)
        assert result["direction"] == "West"
        assert result["direction_hindi"] == "पश्चिम"

    def test_nakshatra_20_is_west(self):
        result = calculate_chandra_vasa(20)
        assert result["direction"] == "West"

    def test_nakshatra_21_is_north(self):
        """First nakshatra in North group (index 21 = Uttara Ashadha)."""
        result = calculate_chandra_vasa(21)
        assert result["direction"] == "North"
        assert result["direction_hindi"] == "उत्तर"

    def test_nakshatra_26_revati_is_north(self):
        """Last nakshatra (index 26 = Revati) in North group."""
        result = calculate_chandra_vasa(26)
        assert result["direction"] == "North"

    def test_name_fields_present(self):
        result = calculate_chandra_vasa(0)
        assert result["name"] == "Chandra Vasa"
        assert result["name_hindi"] == "चन्द्र वास"

    def test_hindi_in_direction(self):
        for idx in [0, 7, 14, 21]:
            result = calculate_chandra_vasa(idx)
            assert _has_hindi(result["direction_hindi"])

    def test_wraps_modulo_27(self):
        """Nakshatra index 27 should wrap to 0 (East)."""
        result = calculate_chandra_vasa(27)
        assert result["direction"] == "East"


# ============================================================
# Agnivasa
# ============================================================
class TestAgnivasa:
    """Validate Agnivasa (fire god residence) calculations."""

    def test_tithi_1_is_prithvi(self):
        result = calculate_agnivasa(1)
        assert result["location"] == "Prithvi"
        assert result["location_hindi"] == "पृथ्वी"

    def test_tithi_5_is_prithvi(self):
        result = calculate_agnivasa(5)
        assert result["location"] == "Prithvi"

    def test_tithi_6_is_jala(self):
        result = calculate_agnivasa(6)
        assert result["location"] == "Jala"
        assert result["location_hindi"] == "जल"

    def test_tithi_10_is_jala(self):
        result = calculate_agnivasa(10)
        assert result["location"] == "Jala"

    def test_tithi_11_is_akasha(self):
        result = calculate_agnivasa(11)
        assert result["location"] == "Akasha"
        assert result["location_hindi"] == "आकाश"

    def test_tithi_15_purnima_is_akasha(self):
        result = calculate_agnivasa(15)
        assert result["location"] == "Akasha"

    def test_tithi_16_is_prithvi(self):
        """Krishna Paksha tithis 16-20 cycle back to Prithvi."""
        result = calculate_agnivasa(16)
        assert result["location"] == "Prithvi"

    def test_tithi_21_is_jala(self):
        result = calculate_agnivasa(21)
        assert result["location"] == "Jala"

    def test_tithi_26_is_akasha(self):
        result = calculate_agnivasa(26)
        assert result["location"] == "Akasha"

    def test_tithi_30_amavasya_is_akasha(self):
        result = calculate_agnivasa(30)
        assert result["location"] == "Akasha"

    def test_name_fields_present(self):
        result = calculate_agnivasa(1)
        assert result["name"] == "Agnivasa"
        assert result["name_hindi"] == "अग्नि वास"

    def test_hindi_present(self):
        for tithi in [1, 6, 11]:
            result = calculate_agnivasa(tithi)
            assert _has_hindi(result["location_hindi"])


# ============================================================
# Rahu Vasa
# ============================================================
class TestRahuVasa:
    """Validate Rahu Vasa (Rahu residence) calculations."""

    def test_rahu_vasa_has_7_entries(self):
        assert len(RAHU_VASA) == 7

    def test_sunday_is_south(self):
        result = calculate_rahu_vasa(0)
        assert result["direction"] == "South"
        assert result["direction_hindi"] == "दक्षिण"

    def test_monday_is_southwest(self):
        result = calculate_rahu_vasa(1)
        assert result["direction"] == "South-West"
        assert result["direction_hindi"] == "नैऋत्य"

    def test_tuesday_is_southeast(self):
        result = calculate_rahu_vasa(2)
        assert result["direction"] == "South-East"
        assert result["direction_hindi"] == "आग्नेय"

    def test_wednesday_is_northwest(self):
        result = calculate_rahu_vasa(3)
        assert result["direction"] == "North-West"
        assert result["direction_hindi"] == "वायव्य"

    def test_thursday_is_northeast(self):
        result = calculate_rahu_vasa(4)
        assert result["direction"] == "North-East"
        assert result["direction_hindi"] == "ईशान"

    def test_friday_is_west(self):
        result = calculate_rahu_vasa(5)
        assert result["direction"] == "West"
        assert result["direction_hindi"] == "पश्चिम"

    def test_saturday_is_east(self):
        result = calculate_rahu_vasa(6)
        assert result["direction"] == "East"
        assert result["direction_hindi"] == "पूर्व"

    def test_name_fields_present(self):
        result = calculate_rahu_vasa(0)
        assert result["name"] == "Rahu Vasa"
        assert result["name_hindi"] == "राहु वास"

    def test_weekday_wraps_modulo_7(self):
        """Weekday 7 should wrap to 0 (Sunday = South)."""
        result = calculate_rahu_vasa(7)
        assert result["direction"] == "South"

    def test_all_hindi_values_are_devanagari(self):
        for day in range(7):
            result = calculate_rahu_vasa(day)
            assert _has_hindi(result["direction_hindi"])


# ============================================================
# Shivavasa
# ============================================================
class TestShivavasa:
    """Validate Shivavasa (Shiva residence) calculations."""

    def test_tithi_1_with_gowri(self):
        result = calculate_shivavasa(1)
        assert result["location"] == "with Gowri"
        assert result["location_hindi"] == "गौरी के साथ"

    def test_tithi_5_with_gowri(self):
        result = calculate_shivavasa(5)
        assert result["location"] == "with Gowri"

    def test_tithi_6_in_kailasha(self):
        result = calculate_shivavasa(6)
        assert result["location"] == "in Kailasha"
        assert result["location_hindi"] == "कैलाश में"

    def test_tithi_10_in_kailasha(self):
        result = calculate_shivavasa(10)
        assert result["location"] == "in Kailasha"

    def test_tithi_11_in_shmashana(self):
        result = calculate_shivavasa(11)
        assert result["location"] == "in Shmashana"
        assert result["location_hindi"] == "श्मशान में"

    def test_tithi_15_in_shmashana(self):
        result = calculate_shivavasa(15)
        assert result["location"] == "in Shmashana"

    def test_tithi_16_cycles_back_to_gowri(self):
        """Krishna Paksha: 16-20 back to Gowri."""
        result = calculate_shivavasa(16)
        assert result["location"] == "with Gowri"

    def test_tithi_21_in_kailasha(self):
        result = calculate_shivavasa(21)
        assert result["location"] == "in Kailasha"

    def test_tithi_30_in_shmashana(self):
        result = calculate_shivavasa(30)
        assert result["location"] == "in Shmashana"

    def test_name_fields_present(self):
        result = calculate_shivavasa(1)
        assert result["name"] == "Shivavasa"
        assert result["name_hindi"] == "शिव वास"

    def test_hindi_present(self):
        for tithi in [1, 6, 11]:
            result = calculate_shivavasa(tithi)
            assert _has_hindi(result["location_hindi"])


# ============================================================
# Homahuti
# ============================================================
class TestHomahuti:
    """Validate Homahuti (homa planet) calculations."""

    def test_planets_list_has_9_entries(self):
        assert len(HOMAHUTI_PLANETS) == 9
        assert len(HOMAHUTI_HINDI) == 9

    def test_ashwini_is_sun(self):
        """Nakshatra 0 => index 0 => Sun."""
        result = calculate_homahuti(0)
        assert result["planet"] == "Sun"
        assert result["planet_hindi"] == "सूर्य"

    def test_bharani_is_moon(self):
        """Nakshatra 1 => index 1 => Moon."""
        result = calculate_homahuti(1)
        assert result["planet"] == "Moon"
        assert result["planet_hindi"] == "चन्द्र"

    def test_nakshatra_8_is_ketu(self):
        """Nakshatra 8 => index 8 => Ketu."""
        result = calculate_homahuti(8)
        assert result["planet"] == "Ketu"
        assert result["planet_hindi"] == "केतु"

    def test_nakshatra_9_cycles_to_sun(self):
        """Nakshatra 9 => 9%9=0 => Sun."""
        result = calculate_homahuti(9)
        assert result["planet"] == "Sun"

    def test_nakshatra_26_revati(self):
        """Nakshatra 26 => 26%9=8 => Ketu."""
        result = calculate_homahuti(26)
        assert result["planet"] == "Ketu"

    def test_nakshatra_4_is_jupiter(self):
        """Nakshatra 4 => Jupiter."""
        result = calculate_homahuti(4)
        assert result["planet"] == "Jupiter"
        assert result["planet_hindi"] == "बृहस्पति"

    def test_name_fields_present(self):
        result = calculate_homahuti(0)
        assert result["name"] == "Homahuti"
        assert result["name_hindi"] == "होमाहुति"

    def test_all_planets_have_hindi(self):
        for idx in range(9):
            result = calculate_homahuti(idx)
            assert _has_hindi(result["planet_hindi"])

    def test_full_cycle_covers_all_planets(self):
        """Nakshatras 0-8 should cover all 9 planets."""
        planets = [calculate_homahuti(i)["planet"] for i in range(9)]
        assert planets == HOMAHUTI_PLANETS


# ============================================================
# Kumbha Chakra
# ============================================================
class TestKumbhaChakra:
    """Validate Kumbha Chakra calculations."""

    def test_kumbha_chakra_has_7_entries(self):
        assert len(KUMBHA_CHAKRA) == 7

    def test_sunday_feet_inauspicious(self):
        result = calculate_kumbha_chakra(0)
        assert result["body_part"] == "Feet"
        assert result["body_part_hindi"] == "पैर"
        assert result["auspicious"] is False

    def test_monday_head_auspicious(self):
        result = calculate_kumbha_chakra(1)
        assert result["body_part"] == "Head"
        assert result["body_part_hindi"] == "सिर"
        assert result["auspicious"] is True

    def test_tuesday_face_inauspicious(self):
        result = calculate_kumbha_chakra(2)
        assert result["body_part"] == "Face"
        assert result["body_part_hindi"] == "मुख"
        assert result["auspicious"] is False

    def test_wednesday_chest_auspicious(self):
        result = calculate_kumbha_chakra(3)
        assert result["body_part"] == "Chest"
        assert result["body_part_hindi"] == "छाती"
        assert result["auspicious"] is True

    def test_thursday_navel_auspicious(self):
        result = calculate_kumbha_chakra(4)
        assert result["body_part"] == "Navel"
        assert result["body_part_hindi"] == "नाभि"
        assert result["auspicious"] is True

    def test_friday_throat_auspicious(self):
        result = calculate_kumbha_chakra(5)
        assert result["body_part"] == "Throat"
        assert result["body_part_hindi"] == "कण्ठ"
        assert result["auspicious"] is True

    def test_saturday_waist_inauspicious(self):
        result = calculate_kumbha_chakra(6)
        assert result["body_part"] == "Waist"
        assert result["body_part_hindi"] == "कमर"
        assert result["auspicious"] is False

    def test_name_fields_present(self):
        result = calculate_kumbha_chakra(0)
        assert result["name"] == "Kumbha Chakra"
        assert result["name_hindi"] == "कुम्भ चक्र"

    def test_weekday_wraps_modulo_7(self):
        """Weekday 7 should wrap to 0 (Sunday)."""
        result = calculate_kumbha_chakra(7)
        assert result["body_part"] == "Feet"

    def test_auspicious_count(self):
        """4 auspicious (Mon, Wed, Thu, Fri) and 3 inauspicious (Sun, Tue, Sat)."""
        auspicious = sum(1 for d in range(7) if KUMBHA_CHAKRA[d][2])
        assert auspicious == 4
        assert 7 - auspicious == 3

    def test_all_hindi_values_are_devanagari(self):
        for day in range(7):
            result = calculate_kumbha_chakra(day)
            assert _has_hindi(result["body_part_hindi"])


# ============================================================
# Master Function -- calculate_all_nivas
# ============================================================
class TestCalculateAllNivas:
    """Validate the master calculate_all_nivas function."""

    def test_returns_all_six_keys(self):
        result = calculate_all_nivas(weekday=0, tithi_index=1, nakshatra_index=0)
        assert "chandra_vasa" in result
        assert "agnivasa" in result
        assert "rahu_vasa" in result
        assert "shivavasa" in result
        assert "homahuti" in result
        assert "kumbha_chakra" in result

    def test_exactly_six_keys(self):
        result = calculate_all_nivas(weekday=0, tithi_index=1, nakshatra_index=0)
        assert len(result) == 6

    def test_chandra_vasa_nested_correctly(self):
        result = calculate_all_nivas(weekday=0, tithi_index=1, nakshatra_index=0)
        assert result["chandra_vasa"]["direction"] == "East"
        assert result["chandra_vasa"]["name"] == "Chandra Vasa"

    def test_agnivasa_nested_correctly(self):
        result = calculate_all_nivas(weekday=0, tithi_index=6, nakshatra_index=0)
        assert result["agnivasa"]["location"] == "Jala"
        assert result["agnivasa"]["name"] == "Agnivasa"

    def test_rahu_vasa_nested_correctly(self):
        result = calculate_all_nivas(weekday=4, tithi_index=1, nakshatra_index=0)
        assert result["rahu_vasa"]["direction"] == "North-East"
        assert result["rahu_vasa"]["name"] == "Rahu Vasa"

    def test_shivavasa_nested_correctly(self):
        result = calculate_all_nivas(weekday=0, tithi_index=6, nakshatra_index=0)
        assert result["shivavasa"]["location"] == "in Kailasha"
        assert result["shivavasa"]["name"] == "Shivavasa"

    def test_homahuti_nested_correctly(self):
        result = calculate_all_nivas(weekday=0, tithi_index=1, nakshatra_index=4)
        assert result["homahuti"]["planet"] == "Jupiter"
        assert result["homahuti"]["name"] == "Homahuti"

    def test_kumbha_chakra_nested_correctly(self):
        result = calculate_all_nivas(weekday=6, tithi_index=1, nakshatra_index=0)
        assert result["kumbha_chakra"]["body_part"] == "Waist"
        assert result["kumbha_chakra"]["auspicious"] is False

    def test_hindi_present_in_all_sections(self):
        """Every section must contain Hindi translations."""
        result = calculate_all_nivas(weekday=3, tithi_index=7, nakshatra_index=10)
        assert _has_hindi(result["chandra_vasa"]["direction_hindi"])
        assert _has_hindi(result["agnivasa"]["location_hindi"])
        assert _has_hindi(result["rahu_vasa"]["direction_hindi"])
        assert _has_hindi(result["shivavasa"]["location_hindi"])
        assert _has_hindi(result["homahuti"]["planet_hindi"])
        assert _has_hindi(result["kumbha_chakra"]["body_part_hindi"])

    def test_boundary_tithi_1(self):
        result = calculate_all_nivas(weekday=0, tithi_index=1, nakshatra_index=0)
        assert result["agnivasa"]["location"] == "Prithvi"
        assert result["shivavasa"]["location"] == "with Gowri"

    def test_boundary_tithi_15(self):
        result = calculate_all_nivas(weekday=0, tithi_index=15, nakshatra_index=0)
        assert result["agnivasa"]["location"] == "Akasha"
        assert result["shivavasa"]["location"] == "in Shmashana"

    def test_boundary_tithi_30(self):
        result = calculate_all_nivas(weekday=0, tithi_index=30, nakshatra_index=0)
        assert result["agnivasa"]["location"] == "Akasha"
        assert result["shivavasa"]["location"] == "in Shmashana"

    def test_all_weekdays(self):
        """Master function should work for all 7 weekdays without error."""
        for day in range(7):
            result = calculate_all_nivas(weekday=day, tithi_index=1, nakshatra_index=0)
            assert len(result) == 6
