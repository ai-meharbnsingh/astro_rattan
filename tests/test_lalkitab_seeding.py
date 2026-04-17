"""Tests for LK DB seeding — validates data integrity of seed constants.

RED → implement → GREEN protocol.
All tests validate the Python-level data lists (LK_DEBTS, LK_NISHANIYAN,
LK_INTERPRETATIONS) and the seed_lalkitab_tables() function signature.
No live DB connection required.
"""
import inspect
import pytest
from app.database_seed_lalkitab import seed_lalkitab_tables, LK_DEBTS, LK_NISHANIYAN, LK_INTERPRETATIONS


# ─────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────

def _has_devanagari(text: str) -> bool:
    """Return True if text contains at least one Devanagari character (U+0900–U+097F)."""
    return any('\u0900' <= c <= '\u097F' for c in text)


# ─────────────────────────────────────────────────────────────
# TABLE 2: LAL KITAB DEBTS
# ─────────────────────────────────────────────────────────────

class TestDebts:
    def test_debts_count(self):
        assert len(LK_DEBTS) >= 7, f"Expected at least 7 debts, got {len(LK_DEBTS)}"

    def test_debts_have_required_keys(self):
        required = {"debt_type", "planet", "description_hi", "description_en",
                    "indication_hi", "indication_en", "remedy_hi", "remedy_en"}
        for debt in LK_DEBTS:
            missing = required - set(debt.keys())
            assert not missing, f"Debt '{debt.get('debt_type')}' missing keys: {missing}"

    def test_debts_hindi_fields_non_empty(self):
        for debt in LK_DEBTS:
            for field in ["description_hi", "indication_hi", "remedy_hi"]:
                val = debt.get(field, "")
                assert val, f"Debt '{debt.get('debt_type')}': field '{field}' is empty"

    def test_debts_english_fields_non_empty(self):
        for debt in LK_DEBTS:
            for field in ["description_en", "indication_en", "remedy_en"]:
                val = debt.get(field, "")
                assert val, f"Debt '{debt.get('debt_type')}': field '{field}' is empty"

    def test_debts_hindi_is_hindi(self):
        """Hindi fields must contain Devanagari script and differ from English."""
        for debt in LK_DEBTS:
            for field_hi, field_en in [
                ("description_hi", "description_en"),
                ("indication_hi", "indication_en"),
                ("remedy_hi", "remedy_en"),
            ]:
                val_hi = debt.get(field_hi, "")
                val_en = debt.get(field_en, "")
                # Must have Devanagari
                assert _has_devanagari(val_hi), (
                    f"Debt '{debt.get('debt_type')}': '{field_hi}' has no Devanagari: {val_hi!r}"
                )
                # Hindi must not equal English
                assert val_hi != val_en, (
                    f"Debt '{debt.get('debt_type')}': '{field_hi}' == '{field_en}' (same string)"
                )

    def test_debts_planets_are_valid(self):
        valid_planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"}
        for debt in LK_DEBTS:
            planet = debt.get("planet", "")
            assert planet in valid_planets, (
                f"Debt '{debt.get('debt_type')}': invalid planet '{planet}'"
            )

    def test_debts_debt_types_have_devanagari(self):
        for debt in LK_DEBTS:
            dt = debt.get("debt_type", "")
            assert _has_devanagari(dt), (
                f"debt_type has no Devanagari: {dt!r}"
            )

    def test_debts_no_duplicate_debt_types(self):
        types = [d["debt_type"] for d in LK_DEBTS]
        assert len(types) == len(set(types)), f"Duplicate debt_type entries: {types}"


# ─────────────────────────────────────────────────────────────
# TABLE 1: NISHANIYAN MASTER
# ─────────────────────────────────────────────────────────────

class TestNishaniyan:
    def test_nishaniyan_count(self):
        assert len(LK_NISHANIYAN) >= 63, (
            f"Expected at least 63 nishaniyan (9 planets × 7 houses min), got {len(LK_NISHANIYAN)}"
        )

    def test_nishaniyan_full_108(self):
        assert len(LK_NISHANIYAN) >= 108, (
            f"Expected 108 nishaniyan (9 planets × 12 houses), got {len(LK_NISHANIYAN)}"
        )

    def test_nishaniyan_structure(self):
        """Each row must be a 6-tuple: (planet, house, nishani_hi, nishani_en, category, severity)."""
        for i, row in enumerate(LK_NISHANIYAN):
            assert len(row) == 6, f"Row {i} has {len(row)} elements, expected 6: {row}"
            planet, house, nishani_hi, nishani_en, category, severity = row
            assert isinstance(planet, str) and planet, f"Row {i}: planet is empty"
            assert isinstance(house, int) and 1 <= house <= 12, f"Row {i}: invalid house {house}"
            assert nishani_hi, f"Row {i}: nishani_text (Hindi) is empty"
            assert nishani_en, f"Row {i}: nishani_text_en (English) is empty"

    def test_nishaniyan_hindi_is_hindi(self):
        """First 10 rows must have Devanagari in nishani_text."""
        for row in LK_NISHANIYAN[:10]:
            planet, house, nishani_hi, nishani_en, category, severity = row
            assert _has_devanagari(nishani_hi), (
                f"Nishani {planet}/{house} nishani_text has no Devanagari: {nishani_hi!r}"
            )

    def test_all_nishaniyan_have_devanagari(self):
        """All rows must have Devanagari in nishani_text."""
        for row in LK_NISHANIYAN:
            planet, house, nishani_hi, nishani_en, category, severity = row
            assert _has_devanagari(nishani_hi), (
                f"Nishani {planet}/{house} has no Devanagari: {nishani_hi!r}"
            )

    def test_nishaniyan_hindi_ne_english(self):
        """nishani_text (Hindi) must not equal nishani_text_en (English)."""
        for row in LK_NISHANIYAN:
            planet, house, nishani_hi, nishani_en, category, severity = row
            assert nishani_hi != nishani_en, (
                f"Nishani {planet}/{house}: Hindi text == English text"
            )

    def test_nishaniyan_all_9_planets(self):
        planets = {row[0] for row in LK_NISHANIYAN}
        expected = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"}
        assert expected.issubset(planets), f"Missing planets in nishaniyan: {expected - planets}"

    def test_nishaniyan_all_12_houses_per_planet(self):
        from collections import defaultdict
        planet_houses = defaultdict(set)
        for row in LK_NISHANIYAN:
            planet, house = row[0], row[1]
            planet_houses[planet].add(house)
        for planet, houses in planet_houses.items():
            assert set(range(1, 13)) == houses, (
                f"Planet '{planet}' is missing houses: {set(range(1,13)) - houses}"
            )

    def test_nishaniyan_valid_categories(self):
        valid_categories = {"physical", "home", "family", "events", "general", "health",
                            "marriage", "wealth", "career"}
        for row in LK_NISHANIYAN:
            planet, house, _, __, category, ___ = row
            assert category in valid_categories, (
                f"Nishani {planet}/{house}: invalid category '{category}'"
            )

    def test_nishaniyan_valid_severities(self):
        valid_severities = {"mild", "moderate", "strong", "critical", "warning", "info"}
        for row in LK_NISHANIYAN:
            planet, house, _, __, ___, severity = row
            assert severity in valid_severities, (
                f"Nishani {planet}/{house}: invalid severity '{severity}'"
            )


# ─────────────────────────────────────────────────────────────
# TABLE 3: LK_INTERPRETATIONS
# ─────────────────────────────────────────────────────────────

class TestInterpretations:
    def test_interpretations_count(self):
        assert len(LK_INTERPRETATIONS) >= 108, (
            f"Expected at least 108 interpretations (9 planets × 12 houses), got {len(LK_INTERPRETATIONS)}"
        )

    def test_interpretations_have_required_keys(self):
        required = {"planet", "house", "interpretation_hi", "interpretation_en", "category"}
        for i, interp in enumerate(LK_INTERPRETATIONS):
            missing = required - set(interp.keys())
            assert not missing, f"Interpretation[{i}] missing keys: {missing}"

    def test_all_9_planets_in_interpretations(self):
        planets = {i["planet"] for i in LK_INTERPRETATIONS}
        expected = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"}
        assert expected.issubset(planets), f"Missing planets in interpretations: {expected - planets}"

    def test_all_12_houses_in_interpretations(self):
        houses = {i["house"] for i in LK_INTERPRETATIONS}
        assert set(range(1, 13)).issubset(houses), (
            f"Missing houses in interpretations: {set(range(1,13)) - houses}"
        )

    def test_all_12_houses_per_planet(self):
        from collections import defaultdict
        planet_houses = defaultdict(set)
        for interp in LK_INTERPRETATIONS:
            planet_houses[interp["planet"]].add(interp["house"])
        for planet, houses in planet_houses.items():
            assert set(range(1, 13)) == houses, (
                f"Planet '{planet}' missing interpretation houses: {set(range(1,13)) - houses}"
            )

    def test_interpretations_hindi_is_hindi(self):
        """interpretation_hi must contain Devanagari characters."""
        for interp in LK_INTERPRETATIONS:
            hi = interp.get("interpretation_hi", "")
            assert hi, f"interpretation_hi is empty for {interp.get('planet')}/{interp.get('house')}"
            assert _has_devanagari(hi), (
                f"Planet {interp['planet']} H{interp['house']}: interpretation_hi has no Devanagari: {hi!r}"
            )

    def test_interpretations_hindi_ne_english(self):
        """interpretation_hi must differ from interpretation_en."""
        for interp in LK_INTERPRETATIONS:
            hi = interp.get("interpretation_hi", "")
            en = interp.get("interpretation_en", "")
            assert hi != en, (
                f"Planet {interp['planet']} H{interp['house']}: interpretation_hi == interpretation_en"
            )

    def test_interpretations_english_non_empty(self):
        for interp in LK_INTERPRETATIONS:
            en = interp.get("interpretation_en", "")
            assert en, f"interpretation_en is empty for {interp.get('planet')}/{interp.get('house')}"

    def test_no_duplicate_planet_house(self):
        seen = set()
        for interp in LK_INTERPRETATIONS:
            key = (interp["planet"], interp["house"])
            assert key not in seen, f"Duplicate interpretation for {key}"
            seen.add(key)


# ─────────────────────────────────────────────────────────────
# FUNCTION SIGNATURE
# ─────────────────────────────────────────────────────────────

class TestSeedFunction:
    def test_seed_function_exists(self):
        assert callable(seed_lalkitab_tables), "seed_lalkitab_tables must be a callable"

    def test_seed_function_has_db_param(self):
        sig = inspect.signature(seed_lalkitab_tables)
        assert "db" in sig.parameters, (
            f"seed_lalkitab_tables must have a 'db' parameter. Got: {list(sig.parameters)}"
        )

    def test_seed_is_idempotent_mock(self):
        """
        Calling seed twice with a mock DB must not raise an error.
        Verifies idempotency contract (ON CONFLICT DO NOTHING logic).
        """
        from unittest.mock import MagicMock

        mock_db = MagicMock()
        # execute() returns a mock cursor; fetchone() returns None (simulates empty DB)
        mock_db.execute.return_value.fetchone.return_value = None
        # First call
        seed_lalkitab_tables(mock_db)
        # Second call — must not raise
        seed_lalkitab_tables(mock_db)
        # execute must have been called multiple times (once per seed row)
        assert mock_db.execute.call_count > 10, (
            f"Expected many execute() calls, got {mock_db.execute.call_count}"
        )
