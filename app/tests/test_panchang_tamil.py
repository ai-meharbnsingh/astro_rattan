"""Tests for app.panchang_tamil -- Tamil Yoga, Jeevanama & Netrama."""
import pytest
from app.panchang_tamil import (
    TAMIL_SIDDHA_NAKSHATRAS,
    TAMIL_MARANA_NAKSHATRAS,
    calculate_tamil_yoga,
    calculate_jeevanama,
    calculate_netrama,
    calculate_all_tamil,
)


# ============================================================
# TAMIL YOGA TESTS
# ============================================================

class TestTamilYogaData:
    """Validate the Tamil Yoga lookup tables."""

    def test_siddha_table_has_all_weekdays(self):
        for day in range(7):
            assert day in TAMIL_SIDDHA_NAKSHATRAS

    def test_marana_table_has_all_weekdays(self):
        for day in range(7):
            assert day in TAMIL_MARANA_NAKSHATRAS

    def test_siddha_and_marana_do_not_overlap(self):
        """No nakshatra should be both Siddha and Marana on the same day."""
        for day in range(7):
            siddha = set(TAMIL_SIDDHA_NAKSHATRAS[day])
            marana = set(TAMIL_MARANA_NAKSHATRAS[day])
            assert siddha & marana == set(), (
                f"Weekday {day}: overlap between Siddha and Marana nakshatras"
            )

    def test_all_nakshatra_indices_in_valid_range(self):
        for day in range(7):
            for idx in TAMIL_SIDDHA_NAKSHATRAS[day]:
                assert 0 <= idx <= 26, f"Siddha day={day} idx={idx} out of range"
            for idx in TAMIL_MARANA_NAKSHATRAS[day]:
                assert 0 <= idx <= 26, f"Marana day={day} idx={idx} out of range"


class TestCalculateTamilYoga:
    """Test calculate_tamil_yoga() for known combinations."""

    def test_sunday_ashwini_is_siddha(self):
        """Sunday (0) + Ashwini (0) should be Siddha."""
        result = calculate_tamil_yoga(weekday=0, nakshatra_index=0)
        assert result["name"] == "Siddha Yoga"
        assert result["auspicious"] is True

    def test_sunday_krittika_is_marana(self):
        """Sunday (0) + Krittika (2) should be Marana."""
        result = calculate_tamil_yoga(weekday=0, nakshatra_index=2)
        assert result["name"] == "Marana Yoga"
        assert result["auspicious"] is False

    def test_monday_bharani_is_siddha(self):
        """Monday (1) + Bharani (1) should be Siddha."""
        result = calculate_tamil_yoga(weekday=1, nakshatra_index=1)
        assert result["name"] == "Siddha Yoga"
        assert result["auspicious"] is True

    def test_monday_rohini_is_marana(self):
        """Monday (1) + Rohini (3) should be Marana."""
        result = calculate_tamil_yoga(weekday=1, nakshatra_index=3)
        assert result["name"] == "Marana Yoga"
        assert result["auspicious"] is False

    def test_tuesday_krittika_is_siddha(self):
        """Tuesday (2) + Krittika (2) should be Siddha."""
        result = calculate_tamil_yoga(weekday=2, nakshatra_index=2)
        assert result["name"] == "Siddha Yoga"
        assert result["auspicious"] is True

    def test_tuesday_ashwini_is_marana(self):
        """Tuesday (2) + Ashwini (0) should be Marana."""
        result = calculate_tamil_yoga(weekday=2, nakshatra_index=0)
        assert result["name"] == "Marana Yoga"
        assert result["auspicious"] is False

    def test_wednesday_rohini_is_siddha(self):
        """Wednesday (3) + Rohini (3) should be Siddha."""
        result = calculate_tamil_yoga(weekday=3, nakshatra_index=3)
        assert result["name"] == "Siddha Yoga"
        assert result["auspicious"] is True

    def test_wednesday_bharani_is_marana(self):
        """Wednesday (3) + Bharani (1) should be Marana."""
        result = calculate_tamil_yoga(weekday=3, nakshatra_index=1)
        assert result["name"] == "Marana Yoga"
        assert result["auspicious"] is False

    def test_neutral_yoga_for_unlisted_nakshatra(self):
        """Sunday (0) + Bharani (1) is neither Siddha nor Marana → Neutral."""
        result = calculate_tamil_yoga(weekday=0, nakshatra_index=1)
        assert result["name"] == "Neutral"
        assert result["auspicious"] is True

    def test_hindi_name_present(self):
        result = calculate_tamil_yoga(weekday=0, nakshatra_index=0)
        assert "name_hindi" in result
        assert len(result["name_hindi"]) > 0

    def test_tamil_name_present(self):
        result = calculate_tamil_yoga(weekday=0, nakshatra_index=0)
        assert "name_tamil" in result
        assert len(result["name_tamil"]) > 0

    def test_invalid_weekday_raises(self):
        with pytest.raises(ValueError, match="weekday"):
            calculate_tamil_yoga(weekday=7, nakshatra_index=0)

    def test_invalid_nakshatra_raises(self):
        with pytest.raises(ValueError, match="nakshatra_index"):
            calculate_tamil_yoga(weekday=0, nakshatra_index=27)

    def test_negative_weekday_raises(self):
        with pytest.raises(ValueError, match="weekday"):
            calculate_tamil_yoga(weekday=-1, nakshatra_index=0)

    def test_thursday_matches_sunday_pattern(self):
        """Thursday (4) should have same Siddha pattern as Sunday (0)."""
        for idx in TAMIL_SIDDHA_NAKSHATRAS[0]:
            result = calculate_tamil_yoga(weekday=4, nakshatra_index=idx)
            assert result["name"] == "Siddha Yoga", (
                f"Thursday + nakshatra {idx} should be Siddha"
            )

    def test_saturday_matches_tuesday_pattern(self):
        """Saturday (6) should have same Siddha pattern as Tuesday (2)."""
        for idx in TAMIL_SIDDHA_NAKSHATRAS[2]:
            result = calculate_tamil_yoga(weekday=6, nakshatra_index=idx)
            assert result["name"] == "Siddha Yoga", (
                f"Saturday + nakshatra {idx} should be Siddha"
            )


# ============================================================
# JEEVANAMA TESTS
# ============================================================

class TestCalculateJeevanama:
    """Test calculate_jeevanama() for each tithi range."""

    @pytest.mark.parametrize("tithi", [1, 2, 3, 4, 5])
    def test_shukla_tithis_1_to_5_full_life(self, tithi):
        result = calculate_jeevanama(tithi)
        assert result["status"] == "Full Life"
        assert result["favorable"] is True

    @pytest.mark.parametrize("tithi", [6, 7, 8, 9, 10])
    def test_shukla_tithis_6_to_10_half_life(self, tithi):
        result = calculate_jeevanama(tithi)
        assert result["status"] == "Half Life"
        assert result["favorable"] is True

    @pytest.mark.parametrize("tithi", [11, 12, 13, 14])
    def test_shukla_tithis_11_to_14_weak_life(self, tithi):
        result = calculate_jeevanama(tithi)
        assert result["status"] == "Weak Life"
        assert result["favorable"] is False

    def test_purnima_full_life(self):
        result = calculate_jeevanama(15)
        assert result["status"] == "Full Life"
        assert result["favorable"] is True

    def test_amavasya_lifeless(self):
        result = calculate_jeevanama(30)
        assert result["status"] == "Lifeless"
        assert result["favorable"] is False

    @pytest.mark.parametrize("tithi", [16, 17, 18, 19, 20])
    def test_krishna_tithis_1_to_5_full_life(self, tithi):
        """Krishna Pratipada to Panchami (16-20) normalise to 1-5 → Full Life."""
        result = calculate_jeevanama(tithi)
        assert result["status"] == "Full Life"
        assert result["favorable"] is True

    @pytest.mark.parametrize("tithi", [21, 22, 23, 24, 25])
    def test_krishna_tithis_6_to_10_half_life(self, tithi):
        """Krishna Shashthi to Dashami (21-25) normalise to 6-10 → Half Life."""
        result = calculate_jeevanama(tithi)
        assert result["status"] == "Half Life"
        assert result["favorable"] is True

    @pytest.mark.parametrize("tithi", [26, 27, 28, 29])
    def test_krishna_tithis_11_to_14_weak_life(self, tithi):
        """Krishna Ekadashi to Chaturdashi (26-29) normalise to 11-14 → Weak Life."""
        result = calculate_jeevanama(tithi)
        assert result["status"] == "Weak Life"
        assert result["favorable"] is False

    def test_hindi_status_present(self):
        result = calculate_jeevanama(1)
        assert "status_hindi" in result
        assert len(result["status_hindi"]) > 0

    def test_tamil_status_present(self):
        result = calculate_jeevanama(1)
        assert "status_tamil" in result
        assert len(result["status_tamil"]) > 0

    def test_invalid_tithi_zero_raises(self):
        with pytest.raises(ValueError, match="tithi_index"):
            calculate_jeevanama(0)

    def test_invalid_tithi_31_raises(self):
        with pytest.raises(ValueError, match="tithi_index"):
            calculate_jeevanama(31)

    def test_invalid_negative_tithi_raises(self):
        with pytest.raises(ValueError, match="tithi_index"):
            calculate_jeevanama(-1)


# ============================================================
# NETRAMA TESTS
# ============================================================

class TestCalculateNetrama:
    """Test calculate_netrama() for each pada."""

    def test_pada_1_seeing(self):
        result = calculate_netrama(nakshatra_index=0, pada=1)
        assert result["status"] == "Seeing"
        assert result["favorable"] is True

    def test_pada_2_seeing(self):
        result = calculate_netrama(nakshatra_index=0, pada=2)
        assert result["status"] == "Seeing"
        assert result["favorable"] is True

    def test_pada_3_half_blind(self):
        result = calculate_netrama(nakshatra_index=0, pada=3)
        assert result["status"] == "Half Blind"
        assert result["favorable"] is True

    def test_pada_4_blind(self):
        result = calculate_netrama(nakshatra_index=0, pada=4)
        assert result["status"] == "Blind"
        assert result["favorable"] is False

    def test_different_nakshatra_same_pada_result(self):
        """Netrama depends on pada, not nakshatra identity."""
        r1 = calculate_netrama(nakshatra_index=5, pada=1)
        r2 = calculate_netrama(nakshatra_index=20, pada=1)
        assert r1["status"] == r2["status"] == "Seeing"

    def test_hindi_status_present(self):
        result = calculate_netrama(nakshatra_index=0, pada=1)
        assert "status_hindi" in result
        assert len(result["status_hindi"]) > 0

    def test_tamil_status_present(self):
        result = calculate_netrama(nakshatra_index=0, pada=1)
        assert "status_tamil" in result
        assert len(result["status_tamil"]) > 0

    def test_invalid_pada_zero_raises(self):
        with pytest.raises(ValueError, match="pada"):
            calculate_netrama(nakshatra_index=0, pada=0)

    def test_invalid_pada_5_raises(self):
        with pytest.raises(ValueError, match="pada"):
            calculate_netrama(nakshatra_index=0, pada=5)

    def test_invalid_nakshatra_raises(self):
        with pytest.raises(ValueError, match="nakshatra_index"):
            calculate_netrama(nakshatra_index=27, pada=1)


# ============================================================
# MASTER FUNCTION TESTS
# ============================================================

class TestCalculateAllTamil:
    """Test the master calculate_all_tamil() function."""

    def test_returns_all_three_keys(self):
        result = calculate_all_tamil(
            weekday=0, tithi_index=1, nakshatra_index=0, pada=1
        )
        assert "tamil_yoga" in result
        assert "jeevanama" in result
        assert "netrama" in result

    def test_tamil_yoga_matches_direct_call(self):
        result = calculate_all_tamil(
            weekday=0, tithi_index=1, nakshatra_index=0, pada=1
        )
        direct = calculate_tamil_yoga(weekday=0, nakshatra_index=0)
        assert result["tamil_yoga"] == direct

    def test_jeevanama_matches_direct_call(self):
        result = calculate_all_tamil(
            weekday=0, tithi_index=7, nakshatra_index=0, pada=1
        )
        direct = calculate_jeevanama(tithi_index=7)
        assert result["jeevanama"] == direct

    def test_netrama_matches_direct_call(self):
        result = calculate_all_tamil(
            weekday=0, tithi_index=1, nakshatra_index=5, pada=3
        )
        direct = calculate_netrama(nakshatra_index=5, pada=3)
        assert result["netrama"] == direct

    def test_default_pada_is_1(self):
        """When pada is omitted, default to 1 → Seeing."""
        result = calculate_all_tamil(
            weekday=0, tithi_index=1, nakshatra_index=0
        )
        assert result["netrama"]["status"] == "Seeing"

    def test_full_combo_sunday_ashwini_pratipada_pada1(self):
        """Sunday + Ashwini + Pratipada + Pada 1 should give:
        Siddha Yoga, Full Life, Seeing."""
        result = calculate_all_tamil(
            weekday=0, tithi_index=1, nakshatra_index=0, pada=1
        )
        assert result["tamil_yoga"]["name"] == "Siddha Yoga"
        assert result["tamil_yoga"]["auspicious"] is True
        assert result["jeevanama"]["status"] == "Full Life"
        assert result["jeevanama"]["favorable"] is True
        assert result["netrama"]["status"] == "Seeing"
        assert result["netrama"]["favorable"] is True

    def test_full_combo_inauspicious(self):
        """Sunday + Krittika (Marana) + Amavasya (Lifeless) + Pada 4 (Blind)."""
        result = calculate_all_tamil(
            weekday=0, tithi_index=30, nakshatra_index=2, pada=4
        )
        assert result["tamil_yoga"]["name"] == "Marana Yoga"
        assert result["tamil_yoga"]["auspicious"] is False
        assert result["jeevanama"]["status"] == "Lifeless"
        assert result["jeevanama"]["favorable"] is False
        assert result["netrama"]["status"] == "Blind"
        assert result["netrama"]["favorable"] is False

    def test_all_results_have_hindi_translations(self):
        result = calculate_all_tamil(
            weekday=1, tithi_index=5, nakshatra_index=1, pada=2
        )
        assert "name_hindi" in result["tamil_yoga"]
        assert "status_hindi" in result["jeevanama"]
        assert "status_hindi" in result["netrama"]

    def test_all_results_have_tamil_translations(self):
        result = calculate_all_tamil(
            weekday=1, tithi_index=5, nakshatra_index=1, pada=2
        )
        assert "name_tamil" in result["tamil_yoga"]
        assert "status_tamil" in result["jeevanama"]
        assert "status_tamil" in result["netrama"]
