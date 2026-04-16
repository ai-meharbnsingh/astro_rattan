"""
test_planetary_enhanced.py -- Tests for enhanced planetary position fields
=========================================================================
Verifies that calculate_planetary_positions returns all new fields:
  retrograde, nakshatra, nakshatra_hindi, nakshatra_pada,
  rashi_hindi, name_hindi, combusted
"""
import pytest
from app.panchang_engine import calculate_planetary_positions

# Known Julian Day: 2460400.5 = ~2024-04-03 00:00 UT
# This is a fixed reference point for reproducible tests.
TEST_JD = 2460400.5

ALL_PLANET_NAMES = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}

VALID_RASHIS = {
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
}

VALID_RASHI_HINDI = {
    "मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या",
    "तुला", "वृश्चिक", "धनु", "मकर", "कुम्भ", "मीन",
}

VALID_NAKSHATRAS = {
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
}

PLANET_HINDI_EXPECTED = {
    "Sun": "सूर्य", "Moon": "चन्द्र", "Mars": "मंगल", "Mercury": "बुध",
    "Jupiter": "बृहस्पति", "Venus": "शुक्र", "Saturn": "शनि",
    "Rahu": "राहु", "Ketu": "केतु",
}


@pytest.fixture
def planets():
    """Calculate planetary positions once for all tests."""
    return calculate_planetary_positions(TEST_JD)


def _planet_by_name(planets, name):
    """Get a planet dict by name."""
    return next(p for p in planets if p["name"] == name)


class TestAllPlanetsPresent:
    def test_nine_planets_returned(self, planets):
        assert len(planets) == 9

    def test_all_planet_names(self, planets):
        names = {p["name"] for p in planets}
        assert names == ALL_PLANET_NAMES


class TestRetrograde:
    def test_sun_never_retrograde(self, planets):
        sun = _planet_by_name(planets, "Sun")
        assert sun["retrograde"] is False

    def test_rahu_always_retrograde(self, planets):
        rahu = _planet_by_name(planets, "Rahu")
        assert rahu["retrograde"] is True

    def test_ketu_always_retrograde(self, planets):
        ketu = _planet_by_name(planets, "Ketu")
        assert ketu["retrograde"] is True

    def test_retrograde_is_bool(self, planets):
        for p in planets:
            assert isinstance(p["retrograde"], bool), f"{p['name']} retrograde is not bool"


class TestNakshatra:
    def test_nakshatra_present(self, planets):
        for p in planets:
            assert "nakshatra" in p, f"{p['name']} missing nakshatra"
            assert p["nakshatra"] in VALID_NAKSHATRAS, (
                f"{p['name']} has invalid nakshatra: {p['nakshatra']}"
            )

    def test_nakshatra_hindi_present(self, planets):
        for p in planets:
            assert "nakshatra_hindi" in p, f"{p['name']} missing nakshatra_hindi"
            assert isinstance(p["nakshatra_hindi"], str)
            assert len(p["nakshatra_hindi"]) > 0

    def test_nakshatra_pada_range(self, planets):
        for p in planets:
            assert "nakshatra_pada" in p, f"{p['name']} missing nakshatra_pada"
            assert 1 <= p["nakshatra_pada"] <= 4, (
                f"{p['name']} has invalid pada: {p['nakshatra_pada']}"
            )


class TestCombustion:
    def test_combusted_field_present(self, planets):
        for p in planets:
            assert "combusted" in p, f"{p['name']} missing combusted"
            assert isinstance(p["combusted"], bool), f"{p['name']} combusted is not bool"

    def test_sun_not_combusted(self, planets):
        sun = _planet_by_name(planets, "Sun")
        assert sun["combusted"] is False

    def test_rahu_not_combusted(self, planets):
        rahu = _planet_by_name(planets, "Rahu")
        assert rahu["combusted"] is False

    def test_ketu_not_combusted(self, planets):
        ketu = _planet_by_name(planets, "Ketu")
        assert ketu["combusted"] is False


class TestRashiHindi:
    def test_rashi_hindi_present(self, planets):
        for p in planets:
            assert "rashi_hindi" in p, f"{p['name']} missing rashi_hindi"
            assert p["rashi_hindi"] in VALID_RASHI_HINDI, (
                f"{p['name']} has invalid rashi_hindi: {p['rashi_hindi']}"
            )


class TestPlanetHindiNames:
    def test_name_hindi_present(self, planets):
        for p in planets:
            assert "name_hindi" in p, f"{p['name']} missing name_hindi"
            assert p["name_hindi"] == PLANET_HINDI_EXPECTED[p["name"]], (
                f"{p['name']} has wrong name_hindi: {p['name_hindi']}"
            )


class TestOriginalFieldsPreserved:
    """Ensure the enhancement did not break existing fields."""

    def test_longitude_present(self, planets):
        for p in planets:
            assert "longitude" in p
            assert 0.0 <= p["longitude"] < 360.0

    def test_degree_present(self, planets):
        for p in planets:
            assert "degree" in p
            assert 0.0 <= p["degree"] < 30.0

    def test_rashi_present(self, planets):
        for p in planets:
            assert "rashi" in p
            assert p["rashi"] in VALID_RASHIS

    def test_rashi_index_present(self, planets):
        for p in planets:
            assert "rashi_index" in p
            assert 0 <= p["rashi_index"] <= 11
