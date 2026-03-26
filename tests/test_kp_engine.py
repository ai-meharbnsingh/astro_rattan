"""Tests for app.kp_engine -- Krishnamurti Paddhati Engine."""
import pytest
from app.kp_engine import (
    VIMSHOTTARI_SEQUENCE,
    KP_SUB_LORDS,
    get_sub_lord,
    calculate_kp_cuspal,
)


class TestVimshottariSequence:
    """Validate Vimshottari Dasha constants."""

    def test_sequence_has_9_planets(self):
        assert len(VIMSHOTTARI_SEQUENCE) == 9

    def test_total_years_is_120(self):
        total = sum(years for _, years in VIMSHOTTARI_SEQUENCE)
        assert total == 120.0

    def test_first_is_ketu(self):
        assert VIMSHOTTARI_SEQUENCE[0] == ("Ketu", 7.0)

    def test_last_is_mercury(self):
        assert VIMSHOTTARI_SEQUENCE[8] == ("Mercury", 17.0)


class TestKPSubLords:
    """Validate the pre-built KP sub-lord table."""

    def test_table_has_entries(self):
        """Must have 27 nakshatras * 9 subs = 243 entries."""
        assert len(KP_SUB_LORDS) == 27 * 9

    def test_covers_full_zodiac(self):
        """First entry starts at 0, last entry ends at ~360."""
        assert KP_SUB_LORDS[0]["start_degree"] == 0.0
        last_end = KP_SUB_LORDS[-1]["end_degree"]
        assert abs(last_end - 360.0) < 0.01

    def test_entries_are_continuous(self):
        """Each entry's end should equal the next entry's start."""
        for i in range(len(KP_SUB_LORDS) - 1):
            assert abs(KP_SUB_LORDS[i]["end_degree"] - KP_SUB_LORDS[i + 1]["start_degree"]) < 0.001, (
                f"Gap at entry {i}: {KP_SUB_LORDS[i]['end_degree']} != {KP_SUB_LORDS[i+1]['start_degree']}"
            )

    def test_first_entry_star_lord_is_ketu(self):
        """First nakshatra (Ashwini) lord is Ketu."""
        assert KP_SUB_LORDS[0]["star_lord"] == "Ketu"

    def test_first_entry_sub_lord_is_ketu(self):
        """Ashwini's first sub = its own lord (Ketu)."""
        assert KP_SUB_LORDS[0]["sub_lord"] == "Ketu"


class TestGetSubLord:
    """Test get_sub_lord function."""

    def test_zero_degrees(self):
        result = get_sub_lord(0.0)
        assert result["star_lord"] == "Ketu"
        assert result["sub_lord"] == "Ketu"

    def test_returns_required_keys(self):
        result = get_sub_lord(123.45)
        assert "star_lord" in result
        assert "sub_lord" in result

    def test_near_360(self):
        """Near 360 degrees should return valid result (Revati nakshatra)."""
        result = get_sub_lord(359.9)
        assert result["star_lord"] == "Mercury"  # Revati lord

    def test_wraparound(self):
        """360+ should wrap to 0-360 range."""
        result_0 = get_sub_lord(1.0)
        result_360 = get_sub_lord(361.0)
        assert result_0 == result_360

    def test_sub_lord_is_valid_planet(self):
        valid_planets = {"Ketu", "Venus", "Sun", "Moon", "Mars",
                         "Rahu", "Jupiter", "Saturn", "Mercury"}
        for deg in [0, 30, 60, 90, 120, 180, 240, 300, 350]:
            result = get_sub_lord(float(deg))
            assert result["sub_lord"] in valid_planets
            assert result["star_lord"] in valid_planets


class TestCalculateKPCuspal:
    """Test KP cuspal chart calculation."""

    def test_returns_required_keys(self):
        planet_lons = {
            "Sun": 120.0, "Moon": 200.0, "Mars": 45.0,
            "Mercury": 150.0, "Jupiter": 270.0,
            "Venus": 80.0, "Saturn": 310.0,
            "Rahu": 15.0, "Ketu": 195.0,
        }
        house_cusps = [float(i * 30) for i in range(12)]
        result = calculate_kp_cuspal(planet_lons, house_cusps)
        assert "cusps" in result
        assert "planets" in result
        assert "significators" in result

    def test_cusps_has_12_entries(self):
        planet_lons = {"Sun": 120.0, "Moon": 200.0}
        house_cusps = [float(i * 30) for i in range(12)]
        result = calculate_kp_cuspal(planet_lons, house_cusps)
        assert len(result["cusps"]) == 12

    def test_cusp_has_star_and_sub_lord(self):
        planet_lons = {"Sun": 120.0}
        house_cusps = [float(i * 30) for i in range(12)]
        result = calculate_kp_cuspal(planet_lons, house_cusps)
        for cusp in result["cusps"]:
            assert "house" in cusp
            assert "sign" in cusp
            assert "star_lord" in cusp
            assert "sub_lord" in cusp

    def test_planet_has_star_and_sub_lord(self):
        planet_lons = {"Sun": 120.0, "Moon": 200.0, "Mars": 45.0}
        house_cusps = [float(i * 30) for i in range(12)]
        result = calculate_kp_cuspal(planet_lons, house_cusps)
        for pname, pdata in result["planets"].items():
            assert "longitude" in pdata
            assert "star_lord" in pdata
            assert "sub_lord" in pdata

    def test_significators_has_entries_for_each_planet(self):
        planet_lons = {
            "Sun": 120.0, "Moon": 200.0, "Mars": 45.0,
            "Mercury": 150.0, "Venus": 80.0,
        }
        house_cusps = [float(i * 30) for i in range(12)]
        result = calculate_kp_cuspal(planet_lons, house_cusps)
        for pname in planet_lons:
            assert pname in result["significators"]
            assert isinstance(result["significators"][pname], list)
            # Each planet must signify at least 1 house (the one it occupies)
            assert len(result["significators"][pname]) >= 1

    def test_significator_houses_in_range(self):
        planet_lons = {
            "Sun": 15.0, "Moon": 75.0, "Mars": 135.0,
            "Jupiter": 225.0, "Saturn": 315.0,
        }
        house_cusps = [float(i * 30) for i in range(12)]
        result = calculate_kp_cuspal(planet_lons, house_cusps)
        for pname, houses in result["significators"].items():
            for h in houses:
                assert 1 <= h <= 12, f"{pname} signifies invalid house {h}"
