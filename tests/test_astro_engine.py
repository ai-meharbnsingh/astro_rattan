"""Tests for app.astro_engine -- Vedic Planetary Calculation Engine."""
import pytest
from app.astro_engine import (
    ZODIAC_SIGNS,
    PLANETS,
    NAKSHATRAS,
    get_sign_from_longitude,
    get_nakshatra_from_longitude,
    calculate_planet_positions,
)


class TestZodiacSigns:
    """Validate ZODIAC_SIGNS constant data."""

    def test_zodiac_has_12_signs(self):
        assert len(ZODIAC_SIGNS) == 12

    def test_zodiac_degree_ranges_continuous(self):
        """Signs must cover 0-360 degrees without gaps."""
        for i, sign in enumerate(ZODIAC_SIGNS):
            assert sign["start_degree"] == i * 30
            assert sign["end_degree"] == (i + 1) * 30

    def test_zodiac_first_is_aries(self):
        assert ZODIAC_SIGNS[0]["name"] == "Aries"
        assert ZODIAC_SIGNS[0]["start_degree"] == 0

    def test_zodiac_last_is_pisces(self):
        assert ZODIAC_SIGNS[11]["name"] == "Pisces"
        assert ZODIAC_SIGNS[11]["end_degree"] == 360


class TestPlanets:
    """Validate PLANETS constant mapping."""

    def test_planets_has_8_entries(self):
        # 8 planets: Sun through Rahu (Ketu is derived)
        assert len(PLANETS) == 8

    def test_planets_sun_constant(self):
        assert PLANETS["Sun"] == 0

    def test_planets_moon_constant(self):
        assert PLANETS["Moon"] == 1

    def test_planets_rahu_constant(self):
        assert PLANETS["Rahu"] == 10


class TestNakshatras:
    """Validate NAKSHATRAS constant data."""

    def test_nakshatras_has_27_entries(self):
        assert len(NAKSHATRAS) == 27

    def test_nakshatras_first_is_ashwini(self):
        assert NAKSHATRAS[0]["name"] == "Ashwini"
        assert NAKSHATRAS[0]["lord"] == "Ketu"

    def test_nakshatras_last_is_revati(self):
        assert NAKSHATRAS[26]["name"] == "Revati"
        assert NAKSHATRAS[26]["lord"] == "Mercury"

    def test_nakshatras_continuous(self):
        """All 27 nakshatras should cover 0 to 360 degrees."""
        assert NAKSHATRAS[0]["start_degree"] == 0.0
        last_end = NAKSHATRAS[-1]["end_degree"]
        assert abs(last_end - 360.0) < 0.001


class TestGetSignFromLongitude:
    """Test get_sign_from_longitude function."""

    def test_aries_at_zero(self):
        assert get_sign_from_longitude(0.0) == "Aries"

    def test_aries_at_15(self):
        assert get_sign_from_longitude(15.0) == "Aries"

    def test_taurus_at_30(self):
        assert get_sign_from_longitude(30.0) == "Taurus"

    def test_pisces_at_350(self):
        assert get_sign_from_longitude(350.0) == "Pisces"

    def test_wraparound_at_360(self):
        """360 degrees should wrap to Aries (0 degrees)."""
        assert get_sign_from_longitude(360.0) == "Aries"

    def test_negative_longitude_wraps(self):
        # -30 % 360 = 330 -> Pisces (330-360)
        assert get_sign_from_longitude(-30.0) == "Pisces"

    def test_scorpio_at_225(self):
        # 210-240 = Scorpio
        assert get_sign_from_longitude(225.0) == "Scorpio"


class TestGetNakshatraFromLongitude:
    """Test get_nakshatra_from_longitude function."""

    def test_ashwini_at_zero(self):
        result = get_nakshatra_from_longitude(0.0)
        assert result["name"] == "Ashwini"
        assert result["lord"] == "Ketu"
        assert result["pada"] == 1

    def test_ashwini_pada_2(self):
        # Pada 2 starts at 3.333... degrees
        result = get_nakshatra_from_longitude(4.0)
        assert result["name"] == "Ashwini"
        assert result["pada"] == 2

    def test_bharani(self):
        # Bharani starts at 13.333...
        result = get_nakshatra_from_longitude(14.0)
        assert result["name"] == "Bharani"
        assert result["lord"] == "Venus"

    def test_revati_near_end(self):
        result = get_nakshatra_from_longitude(359.0)
        assert result["name"] == "Revati"
        assert result["lord"] == "Mercury"

    def test_return_has_required_keys(self):
        result = get_nakshatra_from_longitude(100.0)
        assert "name" in result
        assert "pada" in result
        assert "lord" in result
        assert 1 <= result["pada"] <= 4


class TestCalculatePlanetPositions:
    """Test full planet position calculation."""

    def test_returns_required_keys(self):
        """Result must have planets, ascendant, and houses."""
        result = calculate_planet_positions(
            birth_date="1990-08-15",
            birth_time="10:30",
            latitude=28.6139,
            longitude=77.2090,
            tz_offset=5.5,
        )
        assert "planets" in result
        assert "ascendant" in result
        assert "houses" in result

    def test_returns_9_planets(self):
        """Must return 9 planets including Ketu."""
        result = calculate_planet_positions(
            birth_date="1990-08-15",
            birth_time="10:30",
            latitude=28.6139,
            longitude=77.2090,
            tz_offset=5.5,
        )
        expected_planets = {"Sun", "Moon", "Mercury", "Venus", "Mars",
                            "Jupiter", "Saturn", "Rahu", "Ketu"}
        assert set(result["planets"].keys()) == expected_planets

    def test_returns_12_houses(self):
        result = calculate_planet_positions(
            birth_date="1990-08-15",
            birth_time="10:30",
            latitude=28.6139,
            longitude=77.2090,
            tz_offset=5.5,
        )
        assert len(result["houses"]) == 12

    def test_planet_has_required_fields(self):
        """Each planet entry must have specific fields."""
        result = calculate_planet_positions(
            birth_date="2000-01-01",
            birth_time="12:00",
            latitude=13.0827,
            longitude=80.2707,
            tz_offset=5.5,
        )
        sun = result["planets"]["Sun"]
        required_fields = {"longitude", "sign", "sign_degree", "nakshatra",
                           "nakshatra_pada", "house", "retrograde", "status"}
        assert set(sun.keys()) == required_fields

    def test_ketu_opposite_rahu(self):
        """Ketu must be 180 degrees from Rahu."""
        result = calculate_planet_positions(
            birth_date="1995-06-21",
            birth_time="14:00",
            latitude=28.6139,
            longitude=77.2090,
            tz_offset=5.5,
        )
        rahu_lon = result["planets"]["Rahu"]["longitude"]
        ketu_lon = result["planets"]["Ketu"]["longitude"]
        diff = abs((ketu_lon - rahu_lon + 180) % 360 - 180)
        assert abs(diff - 180.0) < 0.01 or abs(diff) < 0.01
        # The difference should be ~180 or effectively 0 when using modular arithmetic
        actual_diff = abs(rahu_lon - ketu_lon) % 360.0
        assert abs(actual_diff - 180.0) < 0.1

    def test_ascendant_has_sign(self):
        result = calculate_planet_positions(
            birth_date="1985-03-20",
            birth_time="06:00",
            latitude=19.0760,
            longitude=72.8777,
            tz_offset=5.5,
        )
        asc = result["ascendant"]
        assert "longitude" in asc
        assert "sign" in asc
        assert asc["sign"] in [s["name"] for s in ZODIAC_SIGNS]

    def test_all_longitudes_in_range(self):
        """All planet longitudes must be 0-360."""
        result = calculate_planet_positions(
            birth_date="2024-01-01",
            birth_time="00:00",
            latitude=0.0,
            longitude=0.0,
            tz_offset=0.0,
        )
        for pname, pdata in result["planets"].items():
            assert 0 <= pdata["longitude"] < 360, f"{pname} longitude out of range: {pdata['longitude']}"

    def test_sign_degree_under_30(self):
        """sign_degree should be 0-30 for every planet."""
        result = calculate_planet_positions(
            birth_date="2024-06-15",
            birth_time="18:00",
            latitude=40.7128,
            longitude=-74.0060,
            tz_offset=-4.0,
        )
        for pname, pdata in result["planets"].items():
            assert 0 <= pdata["sign_degree"] < 30.001, f"{pname} sign_degree out of range"
