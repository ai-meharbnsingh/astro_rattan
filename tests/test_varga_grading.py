"""
Tests for Phaladeepika Adhyaya 3 (Vargadhyaya) varga-strength grading.

Verifies:
  - _varga_sign_for() for known longitudes in D1, D2, D3, D7, D9, D12, D30.
  - _has_dignity_hold() — own/exalted/moolatrikona/friendly checks.
  - Tier assignment by hold-count (Bhedaka..Parvatamsa).
  - calculate_varga_strength() full integration.
  - Edge cases at exact sign boundaries.
"""
from __future__ import annotations

import pytest

from app.varga_grading_engine import (
    CLASSICAL_PLANETS,
    SAPTAVARGA,
    SLOKA_REF,
    _classify_hold,
    _has_dignity_hold,
    _tier_for_count,
    _varga_sign_for,
    calculate_varga_strength,
)


# ==============================================================
# 1. _varga_sign_for — D1 Rasi
# ==============================================================

class TestVargaSignD1:
    def test_aries_0(self):
        sign, idx = _varga_sign_for(0.0, 1)
        assert sign == "Aries"
        assert idx == 0

    def test_leo_0(self):
        sign, idx = _varga_sign_for(120.0, 1)
        assert sign == "Leo"

    def test_pisces_last(self):
        sign, idx = _varga_sign_for(359.99, 1)
        assert sign == "Pisces"
        assert idx == 11


# ==============================================================
# 2. _varga_sign_for — D2 Hora
# ==============================================================

class TestVargaSignD2:
    def test_0_aries_first_half_leo(self):
        """Odd sign 0-15 -> Sun's hora (Leo)."""
        sign, _ = _varga_sign_for(0.0, 2)
        assert sign == "Leo"

    def test_aries_13_34_in_leo(self):
        """13.34° Aries: still in odd-sign first half -> Leo."""
        sign, _ = _varga_sign_for(13.34, 2)
        assert sign == "Leo"

    def test_aries_20_in_cancer(self):
        """20° Aries: odd-sign second half -> Moon's hora (Cancer)."""
        sign, _ = _varga_sign_for(20.0, 2)
        assert sign == "Cancer"

    def test_taurus_first_half_cancer(self):
        """30.0° = 0° Taurus (even), first half -> Moon's hora (Cancer)."""
        sign, _ = _varga_sign_for(30.0, 2)
        assert sign == "Cancer"

    def test_taurus_second_half_leo(self):
        """45° = 15° Taurus (even), second half -> Sun's hora (Leo)."""
        sign, _ = _varga_sign_for(45.0, 2)
        assert sign == "Leo"


# ==============================================================
# 3. _varga_sign_for — D3 Drekkana
# ==============================================================

class TestVargaSignD3:
    def test_aries_3_5_same_sign(self):
        """3.5° Aries: first 10° -> same sign (Aries)."""
        sign, _ = _varga_sign_for(3.5, 3)
        assert sign == "Aries"

    def test_aries_15_fifth_sign(self):
        """15° Aries: 10-20° -> 5th from self (Leo)."""
        sign, _ = _varga_sign_for(15.0, 3)
        assert sign == "Leo"

    def test_aries_25_ninth_sign(self):
        """25° Aries: 20-30° -> 9th from self (Sagittarius)."""
        sign, _ = _varga_sign_for(25.0, 3)
        assert sign == "Sagittarius"


# ==============================================================
# 4. _varga_sign_for — D7 Saptamsa
# ==============================================================

class TestVargaSignD7:
    def test_aries_0_same(self):
        """0° Aries (odd) -> part 0 -> Aries."""
        sign, _ = _varga_sign_for(0.0, 7)
        assert sign == "Aries"

    def test_taurus_0_seventh(self):
        """0° Taurus (even) -> part 0 -> 7th from Taurus = Scorpio."""
        sign, _ = _varga_sign_for(30.0, 7)
        assert sign == "Scorpio"


# ==============================================================
# 5. _varga_sign_for — D9 Navamsa
# ==============================================================

class TestVargaSignD9:
    def test_aries_0_navamsa_aries(self):
        """0° Aries (fire) -> part 0 starts from Aries -> Aries."""
        sign, _ = _varga_sign_for(0.0, 9)
        assert sign == "Aries"

    def test_aries_end_of_9th_pada(self):
        """29.99° Aries -> part 8 starts from Aries -> Sagittarius (9th)."""
        sign, _ = _varga_sign_for(29.99, 9)
        assert sign == "Sagittarius"

    def test_capricorn_start_earth(self):
        """270° = 0° Capricorn (earth) -> part 0 from Capricorn -> Capricorn."""
        sign, _ = _varga_sign_for(270.0, 9)
        assert sign == "Capricorn"


# ==============================================================
# 6. _varga_sign_for — D12 Dwadasamsa
# ==============================================================

class TestVargaSignD12:
    def test_aries_0_same(self):
        sign, _ = _varga_sign_for(0.0, 12)
        assert sign == "Aries"

    def test_aries_3_taurus(self):
        """3° Aries (2.5-5.0 range = part 1) -> Taurus."""
        sign, _ = _varga_sign_for(3.0, 12)
        assert sign == "Taurus"

    def test_aries_29_99_pisces(self):
        """29.99° Aries (part 11) -> Pisces (Aries + 11)."""
        sign, _ = _varga_sign_for(29.99, 12)
        assert sign == "Pisces"


# ==============================================================
# 7. _varga_sign_for — D30 Trimsamsa
# ==============================================================

class TestVargaSignD30:
    def test_aries_2_mars(self):
        """2° Aries (odd, 0-5) -> Mars -> Aries."""
        sign, _ = _varga_sign_for(2.0, 30)
        assert sign == "Aries"

    def test_aries_7_saturn(self):
        """7° Aries (odd, 5-10) -> Saturn -> Aquarius."""
        sign, _ = _varga_sign_for(7.0, 30)
        assert sign == "Aquarius"

    def test_aries_15_jupiter(self):
        """15° Aries (odd, 10-18) -> Jupiter -> Sagittarius."""
        sign, _ = _varga_sign_for(15.0, 30)
        assert sign == "Sagittarius"

    def test_aries_20_mercury(self):
        """20° Aries (odd, 18-25) -> Mercury -> Gemini."""
        sign, _ = _varga_sign_for(20.0, 30)
        assert sign == "Gemini"

    def test_aries_27_venus(self):
        """27° Aries (odd, 25-30) -> Venus -> Taurus."""
        sign, _ = _varga_sign_for(27.0, 30)
        assert sign == "Taurus"

    def test_taurus_3_venus_libra(self):
        """3° Taurus (even, 0-5) -> Venus -> Libra."""
        sign, _ = _varga_sign_for(30.0 + 3.0, 30)
        assert sign == "Libra"

    def test_taurus_10_mercury_virgo(self):
        """10° Taurus (even, 5-12) -> Mercury -> Virgo."""
        sign, _ = _varga_sign_for(30.0 + 10.0, 30)
        assert sign == "Virgo"


# ==============================================================
# 8. _varga_sign_for — invalid division
# ==============================================================

class TestVargaSignInvalid:
    def test_invalid_division_raises(self):
        with pytest.raises(ValueError):
            _varga_sign_for(0.0, 4)  # D4 not in Saptavarga


# ==============================================================
# 9. _has_dignity_hold
# ==============================================================

class TestDignityHold:
    def test_sun_in_leo_own(self):
        assert _has_dignity_hold("Sun", 4) is True

    def test_sun_in_aries_exalted(self):
        assert _has_dignity_hold("Sun", 0) is True

    def test_sun_in_libra_no(self):
        """Libra lord=Venus, enemy of Sun -> no hold."""
        assert _has_dignity_hold("Sun", 6) is False

    def test_moon_in_taurus_moolatrikona(self):
        assert _has_dignity_hold("Moon", 1) is True

    def test_moon_in_cancer_own(self):
        assert _has_dignity_hold("Moon", 3) is True

    def test_jupiter_in_sagittarius_own(self):
        assert _has_dignity_hold("Jupiter", 8) is True

    def test_jupiter_in_gemini_no(self):
        """Gemini lord=Mercury, enemy of Jupiter -> no hold."""
        assert _has_dignity_hold("Jupiter", 2) is False

    def test_saturn_in_aquarius_own(self):
        assert _has_dignity_hold("Saturn", 10) is True

    def test_saturn_in_libra_exalted(self):
        assert _has_dignity_hold("Saturn", 6) is True

    def test_mars_in_leo_friend(self):
        """Leo lord=Sun, friend of Mars -> friendly hold."""
        assert _has_dignity_hold("Mars", 4) is True

    def test_rahu_not_classical(self):
        """Rahu not graded in Saptavarga scheme."""
        assert _has_dignity_hold("Rahu", 0) is False


# ==============================================================
# 10. _classify_hold
# ==============================================================

class TestClassifyHold:
    def test_sun_in_aries_exalted(self):
        assert _classify_hold("Sun", 0) == "exalted"

    def test_sun_in_leo_moolatrikona(self):
        """Leo is both own AND moolatrikona for Sun. Moolatrikona has priority."""
        assert _classify_hold("Sun", 4) == "moolatrikona"

    def test_mars_in_scorpio_own(self):
        assert _classify_hold("Mars", 7) == "own"

    def test_mars_in_leo_friendly(self):
        assert _classify_hold("Mars", 4) == "friendly"

    def test_sun_in_libra_none(self):
        assert _classify_hold("Sun", 6) == "none"


# ==============================================================
# 11. _tier_for_count
# ==============================================================

class TestTierForCount:
    def test_count_0_bhedaka(self):
        assert _tier_for_count(0)["name"] == "Bhedaka"

    def test_count_1_bhedaka(self):
        assert _tier_for_count(1)["name"] == "Bhedaka"

    def test_count_2_parijatamsa(self):
        assert _tier_for_count(2)["name"] == "Parijatamsa"

    def test_count_3_uttamamsa(self):
        assert _tier_for_count(3)["name"] == "Uttamamsa"

    def test_count_5_gopuramsa(self):
        assert _tier_for_count(5)["name"] == "Gopuramsa"

    def test_count_6_simhasanamsa(self):
        assert _tier_for_count(6)["name"] == "Simhasanamsa"

    def test_count_7_parvatamsa(self):
        assert _tier_for_count(7)["name"] == "Parvatamsa"

    def test_hindi_present(self):
        tier = _tier_for_count(7)
        assert tier["name_hi"] == "पर्वतांश"
        assert "description_hi" in tier

    def test_count_clamped_above_7(self):
        assert _tier_for_count(99)["name"] == "Parvatamsa"

    def test_count_clamped_below_0(self):
        assert _tier_for_count(-1)["name"] == "Bhedaka"


# ==============================================================
# 12. calculate_varga_strength — integration
# ==============================================================

class TestCalculateVargaStrength:
    def test_structure(self):
        result = calculate_varga_strength({"Sun": 5.0, "Moon": 40.0})
        assert "sloka_ref" in result
        assert result["sloka_ref"] == SLOKA_REF
        assert result["scheme"] == "Saptavarga"
        assert result["vargas"] == list(SAPTAVARGA)
        assert "planets" in result
        assert "summary" in result

    def test_sun_at_0_aries_all_7_holds(self):
        """
        Sun at 0° Aries: exalted in D1.
        Compute manually for the 7 vargas:
          D1 -> Aries (exalted, hold)
          D2 -> Leo (own, hold)
          D3 -> Aries (exalted, hold)
          D7 -> Aries (exalted, hold)
          D9 -> Aries (exalted, hold)
          D12 -> Aries (exalted, hold)
          D30 -> Aries (exalted, hold)
        Count = 7 -> Parvatamsa.
        """
        result = calculate_varga_strength({"Sun": 0.0})
        sun_data = result["planets"]["Sun"]
        assert sun_data["count"] == 7
        assert sun_data["tier"]["name"] == "Parvatamsa"
        # all 7 vargas in own_vargas
        assert set(sun_data["own_vargas"]) == set(SAPTAVARGA)
        assert sun_data["sloka_ref"] == SLOKA_REF

    def test_rahu_ignored(self):
        """Rahu is not one of the 7 classical planets for this grading."""
        result = calculate_varga_strength({"Sun": 0.0, "Rahu": 100.0})
        assert "Sun" in result["planets"]
        assert "Rahu" not in result["planets"]

    def test_holds_structure(self):
        """Each planet's holds dict has one entry per Saptavarga division."""
        result = calculate_varga_strength({"Sun": 0.0})
        sun = result["planets"]["Sun"]
        for div in SAPTAVARGA:
            assert div in sun["holds"]
            entry = sun["holds"][div]
            assert "sign" in entry
            assert "sign_index" in entry
            assert "hold" in entry
            assert "category" in entry
            assert "varga" in entry
            assert "division" in entry

    def test_summary_strongest_weakest(self):
        """Summary should identify strongest and weakest planet counts."""
        # Sun at 0° Aries: all 7 holds (exalted).
        # Saturn at 0° Aries: debilitated, check actual count.
        result = calculate_varga_strength({
            "Sun": 0.0,
            "Saturn": 0.0,
        })
        assert "Sun" in result["summary"]["strongest"]
        counts = result["summary"]["counts"]
        assert counts["Sun"] >= counts["Saturn"]

    def test_all_7_classical_planets_supported(self):
        positions = {p: 0.0 for p in CLASSICAL_PLANETS}
        result = calculate_varga_strength(positions)
        for p in CLASSICAL_PLANETS:
            assert p in result["planets"]
            assert 0 <= result["planets"][p]["count"] <= 7
            assert "tier" in result["planets"][p]


# ==============================================================
# 13. Edge cases — exact boundaries
# ==============================================================

class TestBoundaries:
    def test_d9_aries_exact_9th_part(self):
        """29.9999...° Aries still produces a sign in D9 (Sagittarius)."""
        sign, _ = _varga_sign_for(29.999999, 9)
        assert sign == "Sagittarius"

    def test_d30_aries_exactly_5_degrees(self):
        """Exactly 5° Aries: boundary falls into Saturn block (>=5 < 10)."""
        sign, _ = _varga_sign_for(5.0, 30)
        assert sign == "Aquarius"

    def test_d30_aries_exactly_10_degrees(self):
        """Exactly 10° Aries: boundary falls into Jupiter block (>=10 < 18)."""
        sign, _ = _varga_sign_for(10.0, 30)
        assert sign == "Sagittarius"

    def test_longitude_wraps_modulo_360(self):
        """721° = 1° Aries -> same as 1° Aries."""
        sign1, _ = _varga_sign_for(1.0, 1)
        sign2, _ = _varga_sign_for(721.0, 1)
        assert sign1 == sign2


# ==============================================================
# 14. Integration with calculate_divisional_chart_detailed
# ==============================================================

class TestRouteIntegration:
    """
    Integration test: verify varga_strength can be computed alongside
    the detailed divisional chart output without breaking.
    """

    def test_varga_strength_alongside_divisional_chart(self):
        from app.divisional_charts import calculate_divisional_chart_detailed

        positions = {
            "Sun": 15.0,
            "Moon": 45.0,
            "Mars": 75.0,
            "Mercury": 105.0,
            "Jupiter": 135.0,
            "Venus": 165.0,
            "Saturn": 195.0,
        }

        # Verify original API still works
        chart_d9 = calculate_divisional_chart_detailed(positions, 9)
        assert "Sun" in chart_d9
        assert "sign" in chart_d9["Sun"]

        # And compute varga_strength separately
        strength = calculate_varga_strength(positions)
        assert strength["sloka_ref"] == SLOKA_REF
        assert len(strength["planets"]) == 7
        for planet in CLASSICAL_PLANETS:
            assert 0 <= strength["planets"][planet]["count"] <= 7
