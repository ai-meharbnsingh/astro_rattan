"""Tests for app.panchang_samvat -- Samvat Systems & Pushkara Navamsha."""
import pytest
from app.panchang_samvat import (
    SAMVATSARA_NAMES,
    AMANTA_MONTHS,
    PUSHKARA_NAVAMSHA,
    RASHI_TO_INDEX,
    get_brihaspati_samvatsara,
    get_gujarati_samvat,
    get_month_systems,
    is_pushkara_navamsha,
    check_lagna_pushkara,
    calculate_all_samvat,
)


# ============================================================
# Brihaspati Samvatsara
# ============================================================

class TestBrihaspatiSamvatsara:
    """Validate 60-year Jupiter cycle calculations."""

    def test_samvatsara_table_has_60_entries(self):
        assert len(SAMVATSARA_NAMES) == 60

    def test_vs_2083_is_siddharthi(self):
        """VS 2083: (2083-1) % 60 = 2082 % 60 = 42 → index 42 → Saumya? Let's verify."""
        result = get_brihaspati_samvatsara(2083)
        # (2083 - 1) % 60 = 2082 % 60 = 42 → 0-based index 42 → SAMVATSARA_NAMES[42]
        expected_name, expected_hindi = SAMVATSARA_NAMES[42]
        assert result["name"] == expected_name
        assert result["name_hindi"] == expected_hindi
        assert result["index"] == 43  # 1-based
        assert result["year"] == 2083

    def test_vs_2083_name_is_saumya(self):
        """VS 2083 → index 42 → Saumya (सौम्य)."""
        result = get_brihaspati_samvatsara(2083)
        assert result["name"] == "Saumya"
        assert result["name_hindi"] == "सौम्य"

    def test_first_samvatsara_vs_1(self):
        """VS 1 → index 0 → Prabhava."""
        result = get_brihaspati_samvatsara(1)
        assert result["name"] == "Prabhava"
        assert result["name_hindi"] == "प्रभव"
        assert result["index"] == 1

    def test_cycle_wraps_at_60(self):
        """VS 61 should give same samvatsara as VS 1."""
        r1 = get_brihaspati_samvatsara(1)
        r61 = get_brihaspati_samvatsara(61)
        assert r1["name"] == r61["name"]
        assert r1["name_hindi"] == r61["name_hindi"]
        assert r1["index"] == r61["index"]

    def test_last_samvatsara_vs_60(self):
        """VS 60 → index 59 → Akshaya."""
        result = get_brihaspati_samvatsara(60)
        assert result["name"] == "Akshaya"
        assert result["name_hindi"] == "अक्षय"
        assert result["index"] == 60

    def test_all_names_have_hindi(self):
        """Every entry has both English and Hindi."""
        for eng, hin in SAMVATSARA_NAMES:
            assert eng, "English name should not be empty"
            assert hin, "Hindi name should not be empty"


# ============================================================
# Gujarati Samvat
# ============================================================

class TestGujaratiSamvat:
    """Validate Kartikadi year offset."""

    def test_chaitra_is_before_kartik(self):
        """Chaitra is before Gujarati new year → year - 1."""
        result = get_gujarati_samvat(2083, "Chaitra")
        assert result["year"] == 2082

    def test_kartik_is_same_year(self):
        """Kartik is at/after Gujarati new year → same year."""
        result = get_gujarati_samvat(2083, "Kartik")
        assert result["year"] == 2083

    def test_margashirsha_is_same_year(self):
        """Margashirsha is after Kartik → same year."""
        result = get_gujarati_samvat(2083, "Margashirsha")
        assert result["year"] == 2083

    def test_ashwin_is_before_kartik(self):
        """Ashwin is the last month before Kartik → year - 1."""
        result = get_gujarati_samvat(2083, "Ashwin")
        assert result["year"] == 2082

    def test_samvatsara_included(self):
        """Result should include the samvatsara name for the Gujarati year."""
        result = get_gujarati_samvat(2083, "Kartik")
        assert "samvatsara" in result
        assert "samvatsara_hindi" in result
        assert result["samvatsara"]  # non-empty
        assert result["samvatsara_hindi"]  # non-empty

    def test_all_months_before_kartik(self):
        """All 7 months before Kartik should give VS - 1."""
        before = ["Chaitra", "Vaishakha", "Jyeshtha", "Ashadha",
                  "Shravana", "Bhadrapada", "Ashwin"]
        for m in before:
            result = get_gujarati_samvat(2083, m)
            assert result["year"] == 2082, f"{m} should be VS - 1"

    def test_all_months_from_kartik(self):
        """Months from Kartik onward should give same VS."""
        from_kartik = ["Kartik", "Margashirsha", "Pausha", "Magha", "Phalguna"]
        for m in from_kartik:
            result = get_gujarati_samvat(2083, m)
            assert result["year"] == 2083, f"{m} should be same VS"


# ============================================================
# Amanta / Purnimanta Month Systems
# ============================================================

class TestMonthSystems:
    """Validate Amant/Purnimant conversions."""

    def test_amanta_months_has_12_entries(self):
        assert len(AMANTA_MONTHS) == 12

    def test_shukla_paksha_same_month_both_systems(self):
        """In Shukla paksha, both systems show the same month."""
        result = get_month_systems("Chaitra", "Shukla")
        assert result["purnimant"]["month"] == "Chaitra"
        assert result["amant"]["month"] == "Chaitra"

    def test_krishna_paksha_purnimant_shifts_to_next(self):
        """In Krishna paksha, Purnimant system shifts to next month."""
        result = get_month_systems("Chaitra", "Krishna")
        assert result["amant"]["month"] == "Chaitra"
        assert result["purnimant"]["month"] == "Vaishakha"

    def test_krishna_paksha_ashwin_to_kartik(self):
        """Ashwin Krishna → Purnimant = Kartik."""
        result = get_month_systems("Ashwin", "Krishna")
        assert result["purnimant"]["month"] == "Kartik"
        assert result["amant"]["month"] == "Ashwin"

    def test_krishna_paksha_phalguna_wraps_to_chaitra(self):
        """Phalguna Krishna → Purnimant wraps to Chaitra."""
        result = get_month_systems("Phalguna", "Krishna")
        assert result["purnimant"]["month"] == "Chaitra"

    def test_hindi_names_present(self):
        """Hindi translations should be present for both systems."""
        result = get_month_systems("Vaishakha", "Shukla")
        assert result["purnimant"]["month_hindi"] == "वैशाख"
        assert result["amant"]["month_hindi"] == "वैशाख"
        assert result["purnimant"]["system_hindi"] == "पूर्णिमान्त"
        assert result["amant"]["system_hindi"] == "अमान्त"

    def test_all_12_months_have_hindi(self):
        """Every Amanta month has both English and Hindi."""
        for eng, hin in AMANTA_MONTHS:
            assert eng, "English month should not be empty"
            assert hin, "Hindi month should not be empty"


# ============================================================
# Pushkara Navamsha
# ============================================================

class TestPushkaraNavamsha:
    """Validate Pushkara Navamsha boundary checks."""

    def test_pushkara_table_covers_12_signs(self):
        assert len(PUSHKARA_NAVAMSHA) == 12

    def test_aries_pushkara_at_21_degrees(self):
        """Aries (Mesha) Pushkara is 20.0 - 23.333°."""
        assert is_pushkara_navamsha(0, 21.0) is True

    def test_aries_not_pushkara_at_10_degrees(self):
        """10° in Aries is outside Pushkara range."""
        assert is_pushkara_navamsha(0, 10.0) is False

    def test_boundary_start_inclusive(self):
        """Start degree is inclusive."""
        assert is_pushkara_navamsha(0, 20.0) is True

    def test_boundary_end_exclusive(self):
        """End degree is exclusive."""
        assert is_pushkara_navamsha(0, 23.333) is False

    def test_libra_pushkara_at_start_of_sign(self):
        """Libra (Tula) Pushkara is 0.0 - 3.333°."""
        assert is_pushkara_navamsha(6, 1.5) is True

    def test_libra_not_pushkara_at_5_degrees(self):
        assert is_pushkara_navamsha(6, 5.0) is False

    def test_leo_pushkara_near_end_of_sign(self):
        """Leo (Simha) Pushkara is 26.667 - 30.0°."""
        assert is_pushkara_navamsha(4, 28.0) is True

    def test_invalid_rashi_index(self):
        """Invalid rashi index returns False."""
        assert is_pushkara_navamsha(-1, 15.0) is False
        assert is_pushkara_navamsha(12, 15.0) is False

    def test_each_sign_has_pushkara(self):
        """Every sign (0-11) should have a Pushkara navamsha defined."""
        for i in range(12):
            start, end = PUSHKARA_NAVAMSHA[i]
            assert 0 <= start < end <= 30, f"Sign {i} range invalid: {start}-{end}"
            # Midpoint should test as True
            mid = (start + end) / 2
            assert is_pushkara_navamsha(i, mid) is True


class TestCheckLagnaPushkara:
    """Validate lagna-level Pushkara check with named rashis."""

    def test_tula_in_pushkara(self):
        """Tula (Libra) at 1.5° is in Pushkara."""
        result = check_lagna_pushkara("Tula", 1.5)
        assert result["active"] is True
        assert result["name"] == "Pushkara Navamsha"
        assert result["name_hindi"] == "पुष्कर नवांश"
        assert result["lagna"] == "Tula"

    def test_tula_outside_pushkara(self):
        """Tula at 15° is NOT in Pushkara."""
        result = check_lagna_pushkara("Tula", 15.0)
        assert result["active"] is False

    def test_unknown_lagna_returns_inactive(self):
        """Unknown rashi name should return inactive."""
        result = check_lagna_pushkara("InvalidRashi", 10.0)
        assert result["active"] is False

    def test_absolute_longitude_mod_30(self):
        """Degree > 30 is handled via mod 30."""
        # Mesha Pushkara is 20-23.333°; absolute longitude 201.0 → 201%30=21.0
        # But 201° is in Tula (index 6), so test with a Tula-appropriate call
        # Tula Pushkara is 0-3.333°; 181.5 → 181.5%30 = 1.5
        result = check_lagna_pushkara("Tula", 181.5)
        assert result["active"] is True

    def test_hindi_translations_in_result(self):
        """Result should include Hindi lagna name."""
        result = check_lagna_pushkara("Mesha", 21.0)
        assert result["lagna_hindi"] == "मेष"
        assert result["active"] is True


# ============================================================
# Master function
# ============================================================

class TestCalculateAllSamvat:
    """Validate the master calculation function."""

    def test_returns_all_keys(self):
        result = calculate_all_samvat(2083, "Chaitra", "Shukla", "Mesha", 21.0)
        assert "brihaspati" in result
        assert "gujarati" in result
        assert "month_systems" in result
        assert "pushkara" in result

    def test_brihaspati_in_master(self):
        result = calculate_all_samvat(2083, "Kartik", "Shukla")
        assert result["brihaspati"]["name"] == "Saumya"

    def test_gujarati_offset_in_master(self):
        result = calculate_all_samvat(2083, "Chaitra", "Shukla")
        assert result["gujarati"]["year"] == 2082

    def test_month_systems_in_master(self):
        result = calculate_all_samvat(2083, "Ashwin", "Krishna")
        assert result["month_systems"]["purnimant"]["month"] == "Kartik"
        assert result["month_systems"]["amant"]["month"] == "Ashwin"

    def test_pushkara_active_in_master(self):
        result = calculate_all_samvat(2083, "Chaitra", "Shukla", "Tula", 1.5)
        assert result["pushkara"]["active"] is True

    def test_pushkara_inactive_when_no_lagna(self):
        """When lagna_name is empty, pushkara should be inactive."""
        result = calculate_all_samvat(2083, "Chaitra", "Shukla")
        assert result["pushkara"]["active"] is False
        assert result["pushkara"]["name_hindi"] == "पुष्कर नवांश"

    def test_hindi_present_everywhere(self):
        """All sub-dicts should contain Hindi strings."""
        result = calculate_all_samvat(2083, "Vaishakha", "Shukla", "Kanya", 15.0)
        assert result["brihaspati"]["name_hindi"]
        assert result["gujarati"]["samvatsara_hindi"]
        assert result["month_systems"]["purnimant"]["month_hindi"]
        assert result["month_systems"]["amant"]["system_hindi"]
        assert result["pushkara"]["name_hindi"]
