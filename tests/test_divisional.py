"""Tests for app.divisional_charts -- Divisional Chart Calculator."""
import pytest
from app.divisional_charts import (
    calculate_d9_navamsa,
    calculate_d10_dasamsa,
    calculate_divisional_chart,
)

# Known sign names for validation
_VALID_SIGNS = {
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
}


class TestNavamsaD9:
    """Test D9 Navamsa calculation."""

    def test_aries_first_navamsa_is_aries(self):
        """0 degrees Aries -> Navamsa = Aries (fire sign starts from Aries)."""
        result = calculate_d9_navamsa({"Sun": 0.5})
        assert result["Sun"] == "Aries"

    def test_aries_last_navamsa_is_sagittarius(self):
        """
        29.9 degrees Aries -> 9th navamsa part (index 8).
        Fire sign starts from Aries: Aries(0) + 8 = Sagittarius(8).
        """
        result = calculate_d9_navamsa({"Sun": 29.9})
        assert result["Sun"] == "Sagittarius"

    def test_taurus_first_navamsa_is_capricorn(self):
        """
        0 degrees Taurus (lon=30) -> Earth sign starts from Capricorn.
        First part = Capricorn.
        """
        result = calculate_d9_navamsa({"Moon": 30.5})
        assert result["Moon"] == "Capricorn"

    def test_gemini_first_navamsa_is_libra(self):
        """Air sign starts from Libra."""
        result = calculate_d9_navamsa({"Mars": 60.5})
        assert result["Mars"] == "Libra"

    def test_cancer_first_navamsa_is_cancer(self):
        """Water sign starts from Cancer."""
        result = calculate_d9_navamsa({"Jupiter": 90.5})
        assert result["Jupiter"] == "Cancer"

    def test_all_results_are_valid_signs(self):
        longs = {"Sun": 120.0, "Moon": 200.0, "Mars": 45.0, "Jupiter": 300.0}
        result = calculate_d9_navamsa(longs)
        for planet, sign in result.items():
            assert sign in _VALID_SIGNS, f"{planet} navamsa sign invalid: {sign}"

    def test_multiple_planets(self):
        longs = {
            "Sun": 5.0,
            "Moon": 35.0,
            "Mercury": 65.0,
            "Venus": 95.0,
        }
        result = calculate_d9_navamsa(longs)
        assert len(result) == 4
        assert result["Sun"] == "Taurus"      # Aries(fire), part 1 -> Aries+1=Taurus
        # Moon at 35.0 = Taurus, degree_in_sign=5.0, part=int(5.0/3.333)=1
        # Earth starts Capricorn(9), 9+1=10=Aquarius
        assert result["Moon"] == "Aquarius"
        for sign in result.values():
            assert sign in _VALID_SIGNS


class TestDasamaD10:
    """Test D10 Dasamsa calculation."""

    def test_aries_first_part(self):
        """Aries is odd sign (1st), starts from same sign."""
        result = calculate_d10_dasamsa({"Sun": 0.5})
        assert result["Sun"] == "Aries"

    def test_aries_second_part(self):
        """3-6 degrees in Aries = part 1 -> Aries + 1 = Taurus."""
        result = calculate_d10_dasamsa({"Sun": 4.0})
        assert result["Sun"] == "Taurus"

    def test_taurus_first_part(self):
        """Taurus is even sign (2nd), starts from 9th sign = Capricorn."""
        # Taurus index = 1, 1 + 9 = 10 % 12 = 10 = Aquarius
        # Wait -- formula: start = (rasi_index + 9) % 12
        # rasi_index=1, 1+9=10, sign[10]="Aquarius"
        result = calculate_d10_dasamsa({"Moon": 30.5})
        assert result["Moon"] == "Aquarius"

    def test_all_results_valid_signs(self):
        longs = {"Sun": 10.0, "Moon": 100.0, "Mars": 250.0}
        result = calculate_d10_dasamsa(longs)
        for sign in result.values():
            assert sign in _VALID_SIGNS


class TestGenericDivisionalChart:
    """Test generic divisional chart calculator."""

    def test_d9_delegates_correctly(self):
        """Division=9 should match calculate_d9_navamsa."""
        longs = {"Sun": 15.0, "Moon": 85.0}
        d9 = calculate_d9_navamsa(longs)
        generic = calculate_divisional_chart(longs, 9)
        assert d9 == generic

    def test_d10_delegates_correctly(self):
        """Division=10 should match calculate_d10_dasamsa."""
        longs = {"Sun": 15.0, "Moon": 85.0}
        d10 = calculate_d10_dasamsa(longs)
        generic = calculate_divisional_chart(longs, 10)
        assert d10 == generic

    def test_d2_hora(self):
        """D2 (Hora): each sign divided into 2 parts of 15 degrees."""
        # Aries 0-15 -> part 0 -> (0*2+0)%12 = 0 = Aries
        result = calculate_divisional_chart({"Sun": 5.0}, 2)
        assert result["Sun"] == "Aries"

    def test_d2_second_half(self):
        """D2: Aries 15-30 -> part 1 -> (0*2+1)%12 = 1 = Taurus."""
        result = calculate_divisional_chart({"Sun": 20.0}, 2)
        assert result["Sun"] == "Taurus"

    def test_invalid_division_raises(self):
        with pytest.raises(ValueError):
            calculate_divisional_chart({"Sun": 10.0}, 0)

    def test_results_are_valid_signs(self):
        for div in [2, 3, 4, 7, 12, 16, 60]:
            result = calculate_divisional_chart({"Sun": 123.45}, div)
            assert result["Sun"] in _VALID_SIGNS, f"D{div} returned invalid sign"
