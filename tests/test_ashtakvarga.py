"""Tests for app.ashtakvarga_engine -- Ashtakvarga Point System."""
import pytest
from app.ashtakvarga_engine import (
    BENEFIC_POINTS,
    calculate_ashtakvarga,
)

# Standard sign names
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


class TestBeneficPoints:
    """Validate BENEFIC_POINTS constant data."""

    def test_has_7_receiving_planets(self):
        expected = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
        assert set(BENEFIC_POINTS.keys()) == expected

    def test_each_planet_has_8_contributors(self):
        """Each receiving planet should have entries from 7 planets + Ascendant."""
        contributors = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                        "Saturn", "Ascendant"}
        for planet, table in BENEFIC_POINTS.items():
            assert set(table.keys()) == contributors, (
                f"{planet} missing contributors: {contributors - set(table.keys())}"
            )

    def test_benefic_houses_in_range(self):
        """All house numbers in benefic points must be 1-12."""
        for recv, contribs in BENEFIC_POINTS.items():
            for contrib, houses in contribs.items():
                for h in houses:
                    assert 1 <= h <= 12, (
                        f"Invalid house {h} in BENEFIC_POINTS[{recv}][{contrib}]"
                    )

    def test_sun_from_sun_has_8_points(self):
        """Sun from Sun should give 8 benefic houses."""
        assert len(BENEFIC_POINTS["Sun"]["Sun"]) == 8


class TestCalculateAshtakvarga:
    """Test ashtakvarga calculation."""

    def test_basic_chart_returns_required_keys(self):
        chart = {
            "Sun": "Leo", "Moon": "Cancer", "Mars": "Aries",
            "Mercury": "Virgo", "Jupiter": "Sagittarius",
            "Venus": "Libra", "Saturn": "Capricorn",
            "Ascendant": "Aries",
        }
        result = calculate_ashtakvarga(chart)
        assert "planet_bindus" in result
        assert "sarvashtakvarga" in result

    def test_planet_bindus_has_7_planets(self):
        chart = {
            "Sun": "Aries", "Moon": "Taurus", "Mars": "Gemini",
            "Mercury": "Cancer", "Jupiter": "Leo",
            "Venus": "Virgo", "Saturn": "Libra",
        }
        result = calculate_ashtakvarga(chart)
        expected = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
        assert set(result["planet_bindus"].keys()) == expected

    def test_each_planet_has_12_signs(self):
        chart = {
            "Sun": "Leo", "Moon": "Scorpio", "Mars": "Cancer",
            "Mercury": "Cancer", "Jupiter": "Capricorn",
            "Venus": "Cancer", "Saturn": "Libra",
            "Ascendant": "Leo",
        }
        result = calculate_ashtakvarga(chart)
        for planet, bindus in result["planet_bindus"].items():
            assert set(bindus.keys()) == set(_SIGN_NAMES), (
                f"{planet} missing signs in ashtakvarga"
            )

    def test_sarvashtakvarga_has_12_signs(self):
        chart = {
            "Sun": "Aries", "Moon": "Taurus", "Mars": "Gemini",
            "Mercury": "Cancer", "Jupiter": "Leo",
            "Venus": "Virgo", "Saturn": "Libra",
        }
        result = calculate_ashtakvarga(chart)
        assert set(result["sarvashtakvarga"].keys()) == set(_SIGN_NAMES)

    def test_sarvashtakvarga_is_sum_of_planets(self):
        """Sarvashtakvarga for each sign must equal sum of all planet bindus."""
        chart = {
            "Sun": "Leo", "Moon": "Scorpio", "Mars": "Cancer",
            "Mercury": "Cancer", "Jupiter": "Capricorn",
            "Venus": "Cancer", "Saturn": "Libra",
            "Ascendant": "Leo",
        }
        result = calculate_ashtakvarga(chart)
        for sign in _SIGN_NAMES:
            expected_sum = sum(
                result["planet_bindus"][planet][sign]
                for planet in result["planet_bindus"]
            )
            assert result["sarvashtakvarga"][sign] == expected_sum, (
                f"Sarvashtakvarga mismatch for {sign}: "
                f"expected {expected_sum}, got {result['sarvashtakvarga'][sign]}"
            )

    def test_sarvashtakvarga_total_is_337(self):
        """
        The total of all Sarvashtakvarga points across 12 signs
        must always equal 337 (standard Ashtakvarga total).
        """
        chart = {
            "Sun": "Leo", "Moon": "Cancer", "Mars": "Aries",
            "Mercury": "Virgo", "Jupiter": "Sagittarius",
            "Venus": "Libra", "Saturn": "Capricorn",
            "Ascendant": "Aries",
        }
        result = calculate_ashtakvarga(chart)
        total = sum(result["sarvashtakvarga"].values())
        assert total == 337, f"Total sarvashtakvarga should be 337, got {total}"

    def test_missing_planet_raises_error(self):
        chart = {
            "Sun": "Leo", "Moon": "Cancer",
            # Missing Mars, Mercury, Jupiter, Venus, Saturn
        }
        with pytest.raises(ValueError, match="Missing planets"):
            calculate_ashtakvarga(chart)

    def test_bindus_are_non_negative(self):
        chart = {
            "Sun": "Pisces", "Moon": "Gemini", "Mars": "Scorpio",
            "Mercury": "Aquarius", "Jupiter": "Taurus",
            "Venus": "Capricorn", "Saturn": "Cancer",
            "Ascendant": "Sagittarius",
        }
        result = calculate_ashtakvarga(chart)
        for planet, bindus in result["planet_bindus"].items():
            for sign, points in bindus.items():
                assert points >= 0, f"Negative bindu: {planet} in {sign} = {points}"
