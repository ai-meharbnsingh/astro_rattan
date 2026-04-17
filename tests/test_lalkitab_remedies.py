"""Tests for Lal Kitab house-based remedies engine."""
import pytest
from app.lalkitab_engine import get_remedies, REMEDIES_BY_HOUSE


class TestRemediesByHouseCoverage:
    def test_all_planets_present(self):
        expected = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
        assert set(REMEDIES_BY_HOUSE.keys()) == expected

    def test_all_12_houses_per_planet(self):
        for planet, houses in REMEDIES_BY_HOUSE.items():
            assert len(houses) == 12, f"{planet} has {len(houses)} houses, expected 12"
            assert set(houses.keys()) == set(range(1, 13)), f"{planet} missing houses"

    def test_hindi_is_actual_hindi_not_english(self):
        """Hindi text must contain Devanagari characters (U+0900-U+097F)."""
        for planet, houses in REMEDIES_BY_HOUSE.items():
            for house, remedy in houses.items():
                hi = remedy.get("hi", "")
                assert hi, f"{planet} H{house}: hi field is empty"
                assert hi != remedy.get("en", ""), f"{planet} H{house}: hi == en (English copied as Hindi)"
                # Check for Devanagari characters
                has_devanagari = any('\u0900' <= c <= '\u097F' for c in hi)
                assert has_devanagari, f"{planet} H{house}: hi has no Devanagari: '{hi}'"

    def test_remedy_has_required_fields(self):
        for planet, houses in REMEDIES_BY_HOUSE.items():
            for house, remedy in houses.items():
                assert "en" in remedy, f"{planet} H{house} missing 'en'"
                assert "hi" in remedy, f"{planet} H{house} missing 'hi'"
                assert "material" in remedy, f"{planet} H{house} missing 'material'"
                assert "day" in remedy, f"{planet} H{house} missing 'day'"

    def test_minimum_108_entries(self):
        """Must have at least 9 planets × 12 houses = 108 entries."""
        total = sum(len(houses) for houses in REMEDIES_BY_HOUSE.values())
        assert total >= 108, f"Only {total} entries, need >= 108"

    def test_en_field_not_empty(self):
        for planet, houses in REMEDIES_BY_HOUSE.items():
            for house, remedy in houses.items():
                assert remedy.get("en", "").strip(), f"{planet} H{house}: en field is empty"

    def test_material_field_not_empty(self):
        for planet, houses in REMEDIES_BY_HOUSE.items():
            for house, remedy in houses.items():
                assert remedy.get("material", "").strip(), f"{planet} H{house}: material field is empty"

    def test_day_field_valid(self):
        valid_days = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}
        for planet, houses in REMEDIES_BY_HOUSE.items():
            for house, remedy in houses.items():
                day = remedy.get("day", "")
                assert day in valid_days, f"{planet} H{house}: invalid day '{day}'"


class TestGetRemediesFunction:
    def test_weak_planet_gets_remedy(self):
        # Saturn in Aries (House 1) — debilitated (strength 0.20 < 0.5)
        result = get_remedies({"Saturn": "Aries"})
        assert "Saturn" in result
        r = result["Saturn"]
        assert r["lk_house"] == 1
        assert r["has_remedy"] == True
        assert r["remedy"]["hi"] != r["remedy"]["en"]

    def test_strong_planet_no_remedy(self):
        # Sun in Aries (House 1) — exalted (strength 0.95 >= 0.5)
        result = get_remedies({"Sun": "Aries"})
        assert result["Sun"]["has_remedy"] == False

    def test_returns_lk_house_not_just_sign(self):
        result = get_remedies({"Moon": "Scorpio"})  # Scorpio = House 8
        assert result["Moon"]["lk_house"] == 8

    def test_all_9_planets_processed(self):
        positions = {
            "Sun": "Aries", "Moon": "Cancer", "Mars": "Capricorn",
            "Mercury": "Gemini", "Jupiter": "Sagittarius", "Venus": "Taurus",
            "Saturn": "Aquarius", "Rahu": "Gemini", "Ketu": "Sagittarius"
        }
        result = get_remedies(positions)
        assert len(result) == 9

    def test_remedy_dict_has_required_fields(self):
        """Each returned planet entry must have lk_house, remedy dict, has_remedy."""
        result = get_remedies({"Mars": "Cancer"})  # Mars debilitated in Cancer
        r = result["Mars"]
        assert "lk_house" in r
        assert "remedy" in r
        assert "has_remedy" in r
        assert "sign" in r
        assert "dignity" in r
        assert "strength" in r

    def test_remedy_dict_inner_fields(self):
        """Remedy dict must have en, hi, material, day."""
        result = get_remedies({"Jupiter": "Capricorn"})  # Jupiter debilitated
        r = result["Jupiter"]
        assert r["has_remedy"] == True
        remedy = r["remedy"]
        assert "en" in remedy
        assert "hi" in remedy
        assert "material" in remedy
        assert "day" in remedy

    def test_backward_compat_remedies_key(self):
        """Old code expects 'remedies' key (list) — must still work."""
        result = get_remedies({"Sun": "Libra"})  # Sun debilitated in Libra
        r = result["Sun"]
        assert "remedies" in r, "backward-compat 'remedies' key missing"
        assert isinstance(r["remedies"], list)
        assert len(r["remedies"]) > 0

    def test_strong_planet_remedies_empty_list(self):
        """Strong planet: remedies list empty (backward compat), has_remedy False."""
        result = get_remedies({"Moon": "Taurus"})  # Moon exalted
        r = result["Moon"]
        assert r["has_remedy"] == False
        assert r["remedies"] == []

    def test_house_specific_remedies_differ(self):
        """Sun in H1 (Aries) vs Sun in H7 (Libra) should have different en remedies."""
        r1 = get_remedies({"Sun": "Aries"})  # H1
        r7 = get_remedies({"Sun": "Libra"})  # H7 — debilitated, will have remedy
        # Both should return remedy dicts (even if has_remedy differs)
        en1 = r1["Sun"]["remedy"]["en"]
        en7 = r7["Sun"]["remedy"]["en"]
        assert en1 != en7, "Sun H1 and Sun H7 remedies should be different"

    def test_sign_to_house_mapping_correct(self):
        """Verify Aries=H1, Cancer=H4, Libra=H7, Capricorn=H10."""
        signs = {"Sun": "Aries", "Moon": "Cancer", "Mars": "Libra", "Mercury": "Capricorn"}
        result = get_remedies(signs)
        assert result["Sun"]["lk_house"] == 1
        assert result["Moon"]["lk_house"] == 4
        assert result["Mars"]["lk_house"] == 7
        assert result["Mercury"]["lk_house"] == 10
