"""Tests for lalkitab_interpretations.py — Lal Kitab house-by-house planet interpretations."""
import pytest

from app.lalkitab_interpretations import (
    LK_PLANET_HOUSE_INTERPRETATIONS,
    LK_VALIDATED_REMEDIES,
    get_lk_house_interpretation,
    get_all_interpretations_for_chart,
    get_lk_validated_remedies,
)

# ─────────────────────────────────────────────────────────────
# All 9 planets expected
# ─────────────────────────────────────────────────────────────
EXPECTED_PLANETS = {"Jupiter", "Moon", "Mars", "Saturn", "Sun", "Mercury", "Venus", "Rahu", "Ketu"}
ALL_HOUSES = list(range(1, 13))


class TestInterpretationsCompleteness:
    """Verify all 108 planet-house combinations exist and are properly structured."""

    def test_all_9_planets_present(self):
        """All 9 Vedic planets must have entries."""
        assert set(LK_PLANET_HOUSE_INTERPRETATIONS.keys()) == EXPECTED_PLANETS

    def test_each_planet_has_12_houses(self):
        """Each planet must have interpretations for all 12 houses."""
        for planet in EXPECTED_PLANETS:
            planet_data = LK_PLANET_HOUSE_INTERPRETATIONS[planet]
            for house in ALL_HOUSES:
                assert house in planet_data, (
                    f"{planet} is missing House {house} interpretation"
                )

    def test_108_total_interpretations(self):
        """Total house interpretations = 9 planets x 12 houses = 108."""
        count = 0
        for planet in EXPECTED_PLANETS:
            for house in ALL_HOUSES:
                if house in LK_PLANET_HOUSE_INTERPRETATIONS[planet]:
                    count += 1
        assert count == 108

    def test_each_entry_has_required_fields(self):
        """Every interpretation entry must have effect_en, effect_hi, nature, keywords."""
        required_fields = {"effect_en", "effect_hi", "nature", "keywords"}
        for planet in EXPECTED_PLANETS:
            for house in ALL_HOUSES:
                entry = LK_PLANET_HOUSE_INTERPRETATIONS[planet][house]
                for field in required_fields:
                    assert field in entry, (
                        f"{planet} House {house} missing '{field}'"
                    )

    def test_nature_values_are_valid(self):
        """nature must be one of: raja, manda, mixed, raja_or_fakir."""
        valid_natures = {"raja", "manda", "mixed", "raja_or_fakir"}
        for planet in EXPECTED_PLANETS:
            for house in ALL_HOUSES:
                nature = LK_PLANET_HOUSE_INTERPRETATIONS[planet][house]["nature"]
                assert nature in valid_natures, (
                    f"{planet} House {house} has invalid nature '{nature}'"
                )

    def test_effect_en_is_nonempty_string(self):
        """English effect text must be a non-empty string."""
        for planet in EXPECTED_PLANETS:
            for house in ALL_HOUSES:
                text = LK_PLANET_HOUSE_INTERPRETATIONS[planet][house]["effect_en"]
                assert isinstance(text, str) and len(text) > 20, (
                    f"{planet} House {house} has empty/short effect_en"
                )

    def test_effect_hi_is_nonempty_string(self):
        """Hindi effect text must be a non-empty string with Devanagari."""
        for planet in EXPECTED_PLANETS:
            for house in ALL_HOUSES:
                text = LK_PLANET_HOUSE_INTERPRETATIONS[planet][house]["effect_hi"]
                assert isinstance(text, str) and len(text) > 10, (
                    f"{planet} House {house} has empty/short effect_hi"
                )
                # Check for at least some Devanagari characters (Unicode block 0x0900-0x097F)
                has_devanagari = any(
                    "\u0900" <= ch <= "\u097F" for ch in text
                )
                assert has_devanagari, (
                    f"{planet} House {house} effect_hi has no Devanagari script"
                )

    def test_keywords_are_nonempty_list(self):
        """Keywords must be a list with at least 2 items."""
        for planet in EXPECTED_PLANETS:
            for house in ALL_HOUSES:
                keywords = LK_PLANET_HOUSE_INTERPRETATIONS[planet][house]["keywords"]
                assert isinstance(keywords, list) and len(keywords) >= 2, (
                    f"{planet} House {house} has insufficient keywords"
                )


class TestGetLkHouseInterpretation:
    """Test the get_lk_house_interpretation() public function."""

    def test_jupiter_house_1(self):
        """Jupiter in House 1 should return raja_or_fakir nature."""
        result = get_lk_house_interpretation("Jupiter", 1)
        assert result["planet"] == "Jupiter"
        assert result["house"] == 1
        assert result["nature"] == "raja_or_fakir"
        assert "illustrious" in result["effect_en"].lower() or "king" in result["effect_en"].lower()
        assert "किस्मत" in result["effect_hi"] or "राजा" in result["effect_hi"]

    def test_jupiter_house_4_exalted(self):
        """Jupiter in House 4 should mention exalted/uchcha."""
        result = get_lk_house_interpretation("Jupiter", 4)
        assert result["nature"] == "raja_or_fakir"
        assert "exalted" in result["effect_en"].lower() or "uchcha" in result["effect_en"].lower()

    def test_jupiter_house_10_debilitated(self):
        """Jupiter in House 10 should mention debilitated."""
        result = get_lk_house_interpretation("Jupiter", 10)
        assert result["nature"] == "mixed"
        assert "debilitated" in result["effect_en"].lower()

    def test_mars_house_12_strongest(self):
        """Mars in House 12 should be its strongest position."""
        result = get_lk_house_interpretation("Mars", 12)
        assert result["nature"] == "raja"
        assert "strongest" in result["effect_en"].lower()

    def test_mars_house_8_blood_risk(self):
        """Mars in House 8 should mention blood disease."""
        result = get_lk_house_interpretation("Mars", 8)
        assert result["nature"] == "manda"
        assert "blood" in result["effect_en"].lower()

    def test_moon_house_4_exalted(self):
        """Moon in House 4 should be exalted."""
        result = get_lk_house_interpretation("Moon", 4)
        assert result["nature"] == "raja"
        assert "exalted" in result["effect_en"].lower()

    def test_moon_house_12_night_troubles(self):
        """Moon in House 12 should mention night troubles."""
        result = get_lk_house_interpretation("Moon", 12)
        assert result["nature"] == "manda"
        assert "night" in result["effect_en"].lower() or "sleep" in result["effect_en"].lower()

    def test_saturn_house_8_own_house(self):
        """Saturn in House 8 should be in own house."""
        result = get_lk_house_interpretation("Saturn", 8)
        assert result["nature"] == "raja"
        assert "own house" in result["effect_en"].lower()

    def test_saturn_house_10_debilitated(self):
        """Saturn in House 10 should be debilitated."""
        result = get_lk_house_interpretation("Saturn", 10)
        assert result["nature"] == "manda"
        assert "debilitated" in result["effect_en"].lower()

    def test_invalid_planet_returns_empty(self):
        """Unknown planet should return empty dict."""
        result = get_lk_house_interpretation("Pluto", 1)
        assert result == {}

    def test_invalid_house_returns_empty(self):
        """House 0 or 13 should return empty dict."""
        result = get_lk_house_interpretation("Jupiter", 0)
        assert result == {}
        result = get_lk_house_interpretation("Jupiter", 13)
        assert result == {}

    def test_return_structure(self):
        """Returned dict must have planet, house, nature, effect_en, effect_hi, conditions, keywords."""
        result = get_lk_house_interpretation("Sun", 5)
        expected_keys = {"planet", "house", "nature", "effect_en", "effect_hi", "conditions", "keywords"}
        assert set(result.keys()) == expected_keys


class TestGetAllInterpretationsForChart:
    """Test the get_all_interpretations_for_chart() function."""

    def test_full_chart_returns_all_planets(self):
        """A chart with all 9 planets should return 9 interpretations."""
        positions = [
            {"planet": "Jupiter", "house": 1},
            {"planet": "Moon", "house": 4},
            {"planet": "Mars", "house": 12},
            {"planet": "Saturn", "house": 8},
            {"planet": "Sun", "house": 10},
            {"planet": "Mercury", "house": 3},
            {"planet": "Venus", "house": 7},
            {"planet": "Rahu", "house": 6},
            {"planet": "Ketu", "house": 12},
        ]
        results = get_all_interpretations_for_chart(positions)
        assert len(results) == 9
        planets_returned = {r["planet"] for r in results}
        assert planets_returned == EXPECTED_PLANETS

    def test_partial_chart(self):
        """A chart with fewer planets returns corresponding count."""
        positions = [
            {"planet": "Jupiter", "house": 2},
            {"planet": "Mars", "house": 3},
        ]
        results = get_all_interpretations_for_chart(positions)
        assert len(results) == 2

    def test_empty_chart(self):
        """Empty positions returns empty list."""
        results = get_all_interpretations_for_chart([])
        assert results == []


class TestValidatedRemedies:
    """Test the validated remedies data and retrieval function."""

    def test_remedies_dict_has_entries(self):
        """Validated remedies must have at least 10 entries."""
        assert len(LK_VALIDATED_REMEDIES) >= 10

    def test_each_remedy_has_required_fields(self):
        """Every validated remedy must have name, procedure, for_planet, validated."""
        required = {"name_en", "name_hi", "for_planet", "procedure_en", "procedure_hi", "validated"}
        for key, remedy in LK_VALIDATED_REMEDIES.items():
            for field in required:
                assert field in remedy, f"Remedy '{key}' missing field '{field}'"

    def test_remedy_procedures_are_nonempty(self):
        """Procedures should be substantial (not just a few words)."""
        for key, remedy in LK_VALIDATED_REMEDIES.items():
            assert len(remedy["procedure_en"]) > 30, f"Remedy '{key}' procedure_en too short"
            assert len(remedy["procedure_hi"]) > 10, f"Remedy '{key}' procedure_hi too short"

    def test_mars_general_remedy_included(self):
        """Mars remedies should be included for any chart with Mars."""
        positions = [{"planet": "Mars", "house": 5}]
        remedies = get_lk_validated_remedies(positions)
        remedy_keys = [r["key"] for r in remedies]
        assert "tuesday_hanuman_halwa" in remedy_keys

    def test_mars_12_specific_remedy(self):
        """Mars in House 12 should trigger the specific meetha remedy."""
        positions = [{"planet": "Mars", "house": 12}]
        remedies = get_lk_validated_remedies(positions)
        remedy_keys = [r["key"] for r in remedies]
        assert "mars_12_meetha" in remedy_keys
        assert "tuesday_hanuman_halwa" in remedy_keys  # general Mars remedy too

    def test_mars_12_specific_not_triggered_for_other_houses(self):
        """Mars in House 5 should NOT trigger the House 12 specific remedy."""
        positions = [{"planet": "Mars", "house": 5}]
        remedies = get_lk_validated_remedies(positions)
        remedy_keys = [r["key"] for r in remedies]
        assert "mars_12_meetha" not in remedy_keys

    def test_universal_remedy_always_included(self):
        """The 'Any' planet remedy (chandra_universal_booster) is always included."""
        positions = [{"planet": "Saturn", "house": 3}]
        remedies = get_lk_validated_remedies(positions)
        remedy_keys = [r["key"] for r in remedies]
        assert "chandra_universal_booster" in remedy_keys

    def test_jupiter_11_kafan_remedy(self):
        """Jupiter in House 11 should trigger kafan donation remedy."""
        positions = [{"planet": "Jupiter", "house": 11}]
        remedies = get_lk_validated_remedies(positions)
        remedy_keys = [r["key"] for r in remedies]
        assert "jupiter_11_kafan_daan" in remedy_keys

    def test_full_chart_remedies(self):
        """A full chart should return general + conditional remedies."""
        positions = [
            {"planet": "Jupiter", "house": 1},
            {"planet": "Moon", "house": 4},
            {"planet": "Mars", "house": 12},
            {"planet": "Saturn", "house": 8},
            {"planet": "Sun", "house": 10},
            {"planet": "Mercury", "house": 3},
            {"planet": "Venus", "house": 7},
            {"planet": "Rahu", "house": 6},
            {"planet": "Ketu", "house": 12},
        ]
        remedies = get_lk_validated_remedies(positions)
        # Should have universal + general per-planet + conditional matches
        assert len(remedies) >= 8  # at minimum: 1 universal + several planet generals + conditionals
        # Check structure
        for r in remedies:
            assert "name_en" in r
            assert "procedure_en" in r
            assert "validated" in r

    def test_empty_positions_returns_universal_only(self):
        """With no planets, only the universal booster should match."""
        remedies = get_lk_validated_remedies([])
        remedy_keys = [r["key"] for r in remedies]
        assert "chandra_universal_booster" in remedy_keys
        # No planet-specific remedies
        assert "tuesday_hanuman_halwa" not in remedy_keys


class TestSpecificLalKitabTeachings:
    """Validate specific Lal Kitab teachings are accurately represented."""

    def test_jupiter_house_2_jagat_guru(self):
        """Jupiter in House 2 should reference 'Jagat Guru'."""
        result = get_lk_house_interpretation("Jupiter", 2)
        assert "jagat guru" in result["effect_en"].lower() or "jagat_guru" in str(result["keywords"])

    def test_jupiter_house_8_sone_ki_lanka(self):
        """Jupiter in House 8 should reference 'Sone ki Lanka'."""
        result = get_lk_house_interpretation("Jupiter", 8)
        assert "sone ki lanka" in result["effect_en"].lower()

    def test_jupiter_house_11_saap_sajda(self):
        """Jupiter in House 11 should reference 'Saap bhi sajda kare'."""
        result = get_lk_house_interpretation("Jupiter", 11)
        assert "saap" in result["effect_en"].lower() or "snakes bow" in result["effect_en"].lower()

    def test_jupiter_house_6_manda(self):
        """Jupiter in House 6 must be manda (weak)."""
        result = get_lk_house_interpretation("Jupiter", 6)
        assert result["nature"] == "manda"

    def test_jupiter_house_12_pataal(self):
        """Jupiter in House 12 should mention pataal."""
        result = get_lk_house_interpretation("Jupiter", 12)
        assert "pataal" in result["effect_en"].lower() or "pataal" in str(result["keywords"])

    def test_mars_house_8_widow_warning(self):
        """Mars in House 8 must warn about exploiting widows."""
        result = get_lk_house_interpretation("Mars", 8)
        assert "widow" in result["effect_en"].lower()

    def test_mars_house_12_hanuman_halwa(self):
        """Mars in House 12 should mention Hanuman halwa remedy."""
        result = get_lk_house_interpretation("Mars", 12)
        assert "hanuman" in result["effect_en"].lower()

    def test_moon_house_12_ketu_combos(self):
        """Moon in House 12 should document Ketu in 2 and Ketu in 4 combos."""
        result = get_lk_house_interpretation("Moon", 12)
        assert "ketu" in result["effect_en"].lower()
        assert "ketu" in result["conditions"].lower() or "ketu_combo" in str(result["keywords"])

    def test_saturn_nishaniyan_exists(self):
        """Saturn should have the _nishaniyan cross-reference."""
        saturn = LK_PLANET_HOUSE_INTERPRETATIONS["Saturn"]
        assert "_nishaniyan" in saturn
        assert "roof" in saturn["_nishaniyan"]["signs_en"].lower()

    def test_jupiter_house_10_mitti_sona(self):
        """Jupiter in House 10 should contain the 'mitti sona' saying."""
        result = get_lk_house_interpretation("Jupiter", 10)
        assert "mitti" in result["effect_en"].lower() or "gold" in result["effect_en"].lower()
