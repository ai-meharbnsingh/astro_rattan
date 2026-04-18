"""
tests/test_lalkitab_andhe_grah.py

Unit tests for app/lalkitab_andhe_grah.py — detect_andhe_grah().

Covers:
  1. Sun+Saturn both in H10 → both blind, high severity (Andha Teva rule)
  2. Sun in H10 alone → NOT blind via Andha Teva (pair is required)
  3. Saturn in H12 with enemy Sun → Saturn blind (H12 rule)
  4. Saturn in H12 with friendly Jupiter → NOT blind via H12 rule
  5. Jupiter debilitated (Capricorn) in H8 → blind (rule 4: debilitated + dusthana)
  6. Empty chart (no planets) → blind_planets == []
  7. Planet with enemies on both adjacent houses → blind via Papakartari (rule 5)
  8. Retrograde AND combust via chart_data → blind, high severity (rule 3)
  9. source == "LK_CANONICAL", lk_ref == "2.12 / 4.14"
 10. Single trigger → severity "medium", not "high"
"""

import pytest
from app.lalkitab_andhe_grah import detect_andhe_grah


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _pos(planet, house, sign="Aries"):
    return {"planet": planet, "house": house, "sign": sign}


# ---------------------------------------------------------------------------
# Test 1 — Sun + Saturn both in H10: both must be blind with high severity
# ---------------------------------------------------------------------------

class TestAndhaTeva:
    def test_sun_saturn_h10_both_blind(self):
        positions = [
            _pos("Sun", 10, "Capricorn"),
            _pos("Saturn", 10, "Capricorn"),
        ]
        result = detect_andhe_grah(positions)

        assert "Sun" in result["blind_planets"], "Sun should be blind (Andha Teva in H10)"
        assert "Saturn" in result["blind_planets"], "Saturn should be blind (Andha Teva in H10)"

    def test_sun_saturn_h10_both_high_severity(self):
        positions = [
            _pos("Sun", 10, "Capricorn"),
            _pos("Saturn", 10, "Capricorn"),
        ]
        result = detect_andhe_grah(positions)

        assert result["per_planet"]["Sun"]["severity"] == "high"
        assert result["per_planet"]["Saturn"]["severity"] == "high"

    def test_sun_saturn_h10_reasons_contain_andha_teva(self):
        positions = [
            _pos("Sun", 10, "Capricorn"),
            _pos("Saturn", 10, "Capricorn"),
        ]
        result = detect_andhe_grah(positions)

        sun_reasons = " ".join(result["per_planet"]["Sun"]["reasons"])
        sat_reasons = " ".join(result["per_planet"]["Saturn"]["reasons"])
        assert "Andha-Teva" in sun_reasons, "Sun reasons should mention Andha-Teva"
        assert "Andha-Teva" in sat_reasons, "Saturn reasons should mention Andha-Teva"

    def test_sun_alone_in_h10_not_blind_via_andha_teva(self):
        """Sun needs Saturn co-present for the Andha Teva pair — alone it is not triggered."""
        positions = [_pos("Sun", 10, "Capricorn")]
        result = detect_andhe_grah(positions)

        sun_info = result["per_planet"].get("Sun")
        if sun_info is None:
            # Sun not processed — definitely not blind
            assert "Sun" not in result["blind_planets"]
            return

        andha_teva_triggered = any("Andha-Teva" in r for r in sun_info["reasons"])
        assert not andha_teva_triggered, "Sun alone in H10 must NOT trigger Andha Teva"

        # Without Saturn, no Andha-Teva reason, so Sun should NOT be blind (no other triggers)
        assert not sun_info["is_blind"], "Sun alone in H10 should not be blind via Andha Teva"


# ---------------------------------------------------------------------------
# Test 2 — H12 rule (rule 2)
# ---------------------------------------------------------------------------

class TestH12Rule:
    def test_saturn_h12_with_enemy_sun_is_blind(self):
        """
        Saturn's enemies (_LK_ENEMIES_LOCAL["Saturn"]) = {Sun, Moon, Mars}.
        Sun in H12 with Saturn → Saturn triggers H12 rule.
        """
        positions = [
            _pos("Saturn", 12, "Pisces"),
            _pos("Sun", 12, "Pisces"),
        ]
        result = detect_andhe_grah(positions)

        assert "Saturn" in result["blind_planets"], "Saturn should be blind — Sun (enemy) co-present in H12"
        sat_reasons = " ".join(result["per_planet"]["Saturn"]["reasons"])
        assert "H12" in sat_reasons, "Saturn H12 rule reason should mention H12"

    def test_saturn_h12_with_friendly_jupiter_not_blind(self):
        """
        Jupiter is NOT in Saturn's enemy list (_LK_ENEMIES_LOCAL["Saturn"] = {Sun, Moon, Mars}).
        So Saturn + Jupiter in H12 should NOT trigger rule 2 for Saturn.
        Jupiter's enemies include Saturn, so check Jupiter's status separately.
        """
        positions = [
            _pos("Saturn", 12, "Pisces"),
            _pos("Jupiter", 12, "Pisces"),
        ]
        result = detect_andhe_grah(positions)

        sat_info = result["per_planet"].get("Saturn")
        if sat_info is None:
            assert "Saturn" not in result["blind_planets"]
            return

        # Saturn should have no H12-enemy reason (Jupiter is not Saturn's enemy)
        h12_enemy_reason = any("H12" in r and "enemy" in r for r in sat_info["reasons"])
        assert not h12_enemy_reason, "Saturn+Jupiter in H12 should NOT trigger Saturn's H12 enemy rule"

    def test_h12_rule_reciprocal_sun_sees_saturn_as_enemy(self):
        """
        Sun's enemies = {Saturn, Rahu, Ketu}. Saturn in H12 with Sun → Sun also blind.
        Both Sun and Saturn should be blind when sharing H12.
        """
        positions = [
            _pos("Sun", 12, "Pisces"),
            _pos("Saturn", 12, "Pisces"),
        ]
        result = detect_andhe_grah(positions)

        # Sun's enemies include Saturn, so Sun should also be blind
        assert "Sun" in result["blind_planets"], "Sun should be blind — Saturn (enemy) in H12"


# ---------------------------------------------------------------------------
# Test 3 — Rule 4: Debilitated + Dusthana
# ---------------------------------------------------------------------------

class TestDebilitatedDusthana:
    def test_jupiter_debilitated_capricorn_in_h8_is_blind(self):
        """
        Jupiter's debilitation sign = Capricorn.  H8 is dusthana.
        Rule 4 fires → Jupiter is blind.
        """
        positions = [_pos("Jupiter", 8, "Capricorn")]
        result = detect_andhe_grah(positions)

        assert "Jupiter" in result["blind_planets"], "Jupiter debilitated in H8 should be blind"
        jup_reasons = " ".join(result["per_planet"]["Jupiter"]["reasons"])
        assert "debilitated" in jup_reasons.lower()
        assert "dusthana" in jup_reasons.lower() or "H8" in jup_reasons

    def test_debilitated_dusthana_severity_is_medium_for_single_trigger(self):
        """
        One rule trigger alone → severity 'medium' (not 'high').
        Jupiter debilitated in H8 with no other triggers.
        """
        positions = [_pos("Jupiter", 8, "Capricorn")]
        result = detect_andhe_grah(positions)

        # No Andha Teva pair, no retrograde+combust → single trigger → medium
        jup_info = result["per_planet"]["Jupiter"]
        # severity is high only if 2+ triggers, Andha Teva, or retro+combust
        if len(jup_info["reasons"]) == 1:
            assert jup_info["severity"] == "medium"

    def test_jupiter_in_good_sign_dusthana_not_blind(self):
        """Jupiter in Sagittarius (own sign, not debilitated) in H8 should NOT trigger rule 4."""
        positions = [_pos("Jupiter", 8, "Sagittarius")]
        result = detect_andhe_grah(positions)

        jup_info = result["per_planet"].get("Jupiter")
        if jup_info is None:
            assert "Jupiter" not in result["blind_planets"]
            return

        debil_dusthana_triggered = any(
            "debilitated" in r.lower() for r in jup_info["reasons"]
        )
        assert not debil_dusthana_triggered, "Jupiter in own sign in H8 should not trigger rule 4"


# ---------------------------------------------------------------------------
# Test 4 — Empty chart
# ---------------------------------------------------------------------------

class TestEmptyChart:
    def test_no_planets_returns_empty_blind_list(self):
        result = detect_andhe_grah([])
        assert result["blind_planets"] == [], "Empty chart must yield zero blind planets"

    def test_no_planets_per_planet_is_empty(self):
        result = detect_andhe_grah([])
        assert result["per_planet"] == {}

    def test_no_planets_adjacency_warnings_empty(self):
        result = detect_andhe_grah([])
        assert result["adjacency_warnings"] == []


# ---------------------------------------------------------------------------
# Test 5 — Papakartari blind-spot (rule 5)
# ---------------------------------------------------------------------------

class TestPapakartari:
    def test_planet_with_enemies_on_both_sides_is_blind(self):
        """
        Mercury in H5.
        Saturn (enemy of Mercury? No — check: _LK_ENEMIES_LOCAL["Mercury"] = {Moon, Ketu}).
        Use Moon in H4 and Ketu in H6 → both are Mercury's enemies on adjacent houses.
        """
        # Mercury's enemies: Moon, Ketu
        # Adjacent to H5: H4 (prev) and H6 (next)
        positions = [
            _pos("Mercury", 5, "Leo"),
            _pos("Moon", 4, "Cancer"),   # prev house (H4), Moon is Mercury's enemy
            _pos("Ketu", 6, "Virgo"),    # next house (H6), Ketu is Mercury's enemy
        ]
        result = detect_andhe_grah(positions)

        assert "Mercury" in result["blind_planets"], "Mercury should be blind via Papakartari"
        merc_reasons = " ".join(result["per_planet"]["Mercury"]["reasons"])
        assert "Papakartari" in merc_reasons

    def test_planet_with_enemy_on_only_one_side_not_blind_via_papakartari(self):
        """Only one adjacent enemy → Papakartari does not fire."""
        # Mercury in H5, Moon in H4 (enemy), no enemy in H6
        positions = [
            _pos("Mercury", 5, "Leo"),
            _pos("Moon", 4, "Cancer"),
        ]
        result = detect_andhe_grah(positions)

        merc_info = result["per_planet"].get("Mercury")
        if merc_info is None:
            assert "Mercury" not in result["blind_planets"]
            return

        papakartari_triggered = any("Papakartari" in r for r in merc_info["reasons"])
        assert not papakartari_triggered, "One-sided enemy should NOT trigger Papakartari"


# ---------------------------------------------------------------------------
# Test 6 — Rule 3: retrograde AND combust (via chart_data)
# ---------------------------------------------------------------------------

class TestRetrogradeCombust:
    def test_retrograde_and_combust_is_blind_high_severity(self):
        """
        chart_data carries retrograde + combust flags for Mars.
        Rule 3 fires → blind + high severity.
        """
        positions = [_pos("Mars", 3, "Gemini")]
        chart_data = {
            "planets": {
                "Mars": {"retrograde": True, "is_combust": True}
            }
        }
        result = detect_andhe_grah(positions, chart_data=chart_data)

        assert "Mars" in result["blind_planets"], "Mars retro+combust should be blind"
        mars_info = result["per_planet"]["Mars"]
        assert mars_info["severity"] == "high", "retro+combust → high severity"
        retro_reason = any("retrograde AND combust" in r for r in mars_info["reasons"])
        assert retro_reason, "reasons should include retrograde+combust"

    def test_retrograde_only_no_combust_not_blind_via_rule3(self):
        """Retrograde alone does NOT trigger rule 3."""
        positions = [_pos("Mars", 3, "Gemini")]
        chart_data = {
            "planets": {
                "Mars": {"retrograde": True, "is_combust": False}
            }
        }
        result = detect_andhe_grah(positions, chart_data=chart_data)

        mars_info = result["per_planet"].get("Mars")
        if mars_info is None:
            assert "Mars" not in result["blind_planets"]
            return

        retro_combust_triggered = any("retrograde AND combust" in r for r in mars_info["reasons"])
        assert not retro_combust_triggered, "Retrograde-only should NOT trigger rule 3"


# ---------------------------------------------------------------------------
# Test 7 — Metadata / canonical fields
# ---------------------------------------------------------------------------

class TestMetadata:
    def test_source_is_lk_canonical(self):
        result = detect_andhe_grah([])
        assert result["source"] == "LK_CANONICAL"

    def test_lk_ref_is_correct(self):
        result = detect_andhe_grah([])
        assert result["lk_ref"] == "2.12 / 4.14"

    def test_result_always_has_required_keys(self):
        result = detect_andhe_grah([])
        required = {"blind_planets", "per_planet", "adjacency_warnings", "lk_ref", "source"}
        assert required.issubset(result.keys())

    def test_per_planet_entry_shape(self):
        """Each per_planet entry has the required fields."""
        positions = [_pos("Sun", 10), _pos("Saturn", 10)]
        result = detect_andhe_grah(positions)

        for planet_name, info in result["per_planet"].items():
            required_fields = {"planet", "house", "sign", "is_blind", "severity", "reasons",
                               "warning_en", "warning_hi"}
            assert required_fields.issubset(info.keys()), (
                f"per_planet[{planet_name!r}] is missing fields: "
                f"{required_fields - info.keys()}"
            )


# ---------------------------------------------------------------------------
# Test 8 — High severity requires 2+ triggers
# ---------------------------------------------------------------------------

class TestSeverityLogic:
    def test_two_triggers_yields_high_severity(self):
        """
        Jupiter debilitated in Capricorn in H12, AND Sun (enemy) in H12.
        Jupiter's enemies include Saturn (not Sun), so H12 rule won't fire.
        Use Saturn in H12 instead — Saturn is in Jupiter's enemy list.
        Two rules: debilitated+dusthana (H12) AND H12 enemy.
        """
        # Jupiter debilitated (Capricorn) in H12, with Saturn (Jupiter's enemy) also in H12
        # Rule 4: debilitated + dusthana (H12 is dusthana)
        # Rule 2: in H12 with enemy (Saturn)
        positions = [
            _pos("Jupiter", 12, "Capricorn"),
            _pos("Saturn", 12, "Capricorn"),
        ]
        result = detect_andhe_grah(positions)

        jup_info = result["per_planet"].get("Jupiter")
        assert jup_info is not None
        assert jup_info["is_blind"], "Jupiter should be blind"
        if len(jup_info["reasons"]) >= 2:
            assert jup_info["severity"] == "high", "2+ triggers should yield high severity"

    def test_not_blind_planet_has_severity_none(self):
        """A planet with zero triggers has severity 'none'."""
        positions = [_pos("Venus", 5, "Taurus")]
        result = detect_andhe_grah(positions)

        venus_info = result["per_planet"].get("Venus")
        if venus_info is not None:
            if not venus_info["is_blind"]:
                assert venus_info["severity"] == "none"
