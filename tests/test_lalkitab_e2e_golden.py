"""
Golden-path E2E tests for the Lal Kitab pipeline.

Uses a fixed reference birth (1990-01-15 06:30 IST, Delhi) to verify the
full pipeline produces expected astrological outputs end-to-end. These
tests catch regressions in: ephemeris calculations, house derivations,
dignity classifications, remedy selection, teva type identification,
seven-year cycle routing, and milestone timing.

Unlike the existing unit tests (which validate SHAPE only), these tests
hardcode EXPECTED VALUES derived from running the real ephemeris against
a deterministic input. If the ephemeris drifts (ayanamsa change,
Swiss Ephemeris upgrade, bug fix in house math), these tests will flag
the change — a feature, not a bug.

Reference ephemeris snapshot (swisseph + Lahiri ayanamsa):
  Ascendant: Sagittarius (longitude ~258.349)
  Sun:     Capricorn  / house 2
  Moon:    Leo        / house 9
  Mars:    Scorpio    / house 12
  Mercury: Sagittarius/ house 1  (retrograde)
  Jupiter: Gemini     / house 7  (retrograde)
  Venus:   Capricorn  / house 2  (retrograde)
  Saturn:  Sagittarius/ house 1
  Rahu:    Capricorn  / house 2  (retrograde)
  Ketu:    Cancer     / house 8  (retrograde)
"""
import pytest

from app.astro_engine import calculate_planet_positions
from app.lalkitab_engine import (
    get_remedies,
    get_planet_strength_detailed,
)
from app.lalkitab_advanced import identify_teva_type
from app.lalkitab_milestones import (
    calculate_age_milestones,
    get_seven_year_cycle,
)


# ============================================================
# Reference birth — fixed, deterministic
# ============================================================
REFERENCE_BIRTH = {
    "date": "1990-01-15",
    "time": "06:30:00",
    "lat": 28.6139,
    "lon": 77.2090,
    "tz": 5.5,
}

# Expected positions — derived from actual swisseph run on REFERENCE_BIRTH.
# Update ONLY after a deliberate ephemeris/ayanamsa change.
EXPECTED_POSITIONS = {
    "Sun":     {"sign": "Capricorn",   "house": 2},
    "Moon":    {"sign": "Leo",         "house": 9},
    "Mars":    {"sign": "Scorpio",     "house": 12},
    "Mercury": {"sign": "Sagittarius", "house": 1},
    "Jupiter": {"sign": "Gemini",      "house": 7},
    "Venus":   {"sign": "Capricorn",   "house": 2},
    "Saturn":  {"sign": "Sagittarius", "house": 1},
    "Rahu":    {"sign": "Capricorn",   "house": 2},
    "Ketu":    {"sign": "Cancer",      "house": 8},
}

EXPECTED_ASCENDANT_SIGN = "Sagittarius"

VALID_SIGNS = {
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
}


# ============================================================
# Shared fixtures (computed ONCE per test module — fast)
# ============================================================

@pytest.fixture(scope="module")
def chart():
    """Pre-computed chart for the reference birth. Shared across all tests."""
    return calculate_planet_positions(
        REFERENCE_BIRTH["date"],
        REFERENCE_BIRTH["time"],
        REFERENCE_BIRTH["lat"],
        REFERENCE_BIRTH["lon"],
        REFERENCE_BIRTH["tz"],
    )


@pytest.fixture(scope="module")
def simple_positions(chart):
    """{planet: sign} mapping expected by get_remedies."""
    return {name: info["sign"] for name, info in chart["planets"].items()}


@pytest.fixture(scope="module")
def list_positions(chart):
    """[{planet, house}, ...] list expected by lalkitab_advanced / milestones."""
    return [
        {"planet": name, "house": info["house"]}
        for name, info in chart["planets"].items()
    ]


# ============================================================
# Golden ephemeris — planet positions must match snapshot
# ============================================================

class TestGoldenEphemeris:
    """Validate core ephemeris gives stable, correct positions for ref birth."""

    def test_engine_is_swisseph(self, chart):
        """Reference tests require real Swiss Ephemeris, not the fallback."""
        engine = chart.get("_engine")
        if engine != "swisseph":
            pytest.skip(
                f"Swiss Ephemeris not available (engine={engine}); "
                "golden assertions only valid for swisseph backend."
            )

    def test_chart_has_all_9_planets(self, chart):
        required = set(EXPECTED_POSITIONS.keys())
        actual = set(chart["planets"].keys())
        assert required.issubset(actual), f"Missing planets: {required - actual}"

    def test_every_planet_has_valid_sign_and_house(self, chart):
        for name, info in chart["planets"].items():
            assert info.get("sign") in VALID_SIGNS, f"{name} invalid sign: {info.get('sign')}"
            assert 1 <= info.get("house", 0) <= 12, f"{name} invalid house: {info.get('house')}"

    def test_ascendant_in_sagittarius(self, chart):
        """Ref birth at 6:30 AM Delhi -> Lagna in Sagittarius (sidereal/Lahiri)."""
        if chart.get("_engine") != "swisseph":
            pytest.skip("Ascendant assertion requires swisseph")
        asc = chart.get("ascendant") or {}
        assert asc.get("sign") == EXPECTED_ASCENDANT_SIGN, (
            f"Expected ascendant {EXPECTED_ASCENDANT_SIGN}, got {asc.get('sign')}"
        )
        assert "longitude" in asc

    @pytest.mark.parametrize("planet,expected", sorted(EXPECTED_POSITIONS.items()))
    def test_planet_position_matches_snapshot(self, chart, planet, expected):
        """Each planet must be in the exact sign+house from the ref snapshot."""
        if chart.get("_engine") != "swisseph":
            pytest.skip("Snapshot valid only for swisseph backend")
        info = chart["planets"].get(planet)
        assert info is not None, f"{planet} missing from chart"
        assert info["sign"] == expected["sign"], (
            f"{planet} sign drifted: expected {expected['sign']}, got {info['sign']}"
        )
        assert info["house"] == expected["house"], (
            f"{planet} house drifted: expected {expected['house']}, got {info['house']}"
        )

    def test_mercury_jupiter_venus_retrograde(self, chart):
        """Jan 15 1990: Mercury, Jupiter, Venus known retrograde. Stable check."""
        if chart.get("_engine") != "swisseph":
            pytest.skip("Retrograde accuracy requires swisseph")
        for p in ("Mercury", "Jupiter", "Venus"):
            assert chart["planets"][p].get("retrograde") is True, (
                f"{p} should be retrograde on 1990-01-15"
            )


# ============================================================
# Golden remedies — specific planets must have expected afflictions
# ============================================================

class TestGoldenRemedies:
    """Remedy pipeline must correctly identify weak/afflicted planets."""

    def test_remedies_returned_for_all_9_planets(self, simple_positions):
        result = get_remedies(simple_positions)
        assert set(result.keys()) == set(EXPECTED_POSITIONS.keys())

    def test_sun_flagged_weak_in_enemy_sign(self, chart, simple_positions):
        """Sun in Capricorn (enemy of Saturn's sign) -> dignity=Enemy, needs remedy."""
        if chart.get("_engine") != "swisseph":
            pytest.skip("Requires swisseph for known Sun placement")
        result = get_remedies(simple_positions, chart_data=chart)
        sun = result["Sun"]
        assert sun["dignity"] == "Enemy", f"Sun dignity expected Enemy, got {sun['dignity']}"
        assert sun["has_remedy"] is True, "Sun in Capricorn should need remedy"
        assert "in enemy sign" in sun["afflictions"]

    def test_jupiter_flagged_with_multiple_afflictions(self, chart, simple_positions):
        """Jupiter retrograde in Gemini (Mercury's sign = enemy for Jupiter)."""
        if chart.get("_engine") != "swisseph":
            pytest.skip("Requires swisseph for known Jupiter placement")
        result = get_remedies(simple_positions, chart_data=chart)
        jup = result["Jupiter"]
        assert jup["dignity"] == "Enemy"
        assert jup["has_remedy"] is True
        assert "retrograde" in jup["afflictions"]
        assert "in enemy sign" in jup["afflictions"]

    def test_moon_not_flagged(self, chart, simple_positions):
        """Moon in Leo (Sun's sign — friendly enough to not need remedy)."""
        if chart.get("_engine") != "swisseph":
            pytest.skip("Requires swisseph")
        result = get_remedies(simple_positions, chart_data=chart)
        moon = result["Moon"]
        assert moon["has_remedy"] is False, (
            f"Moon in Leo should be strong enough, got strength={moon['strength']}"
        )

    def test_remedy_bilingual_with_devanagari(self, simple_positions):
        """Remedies have both en and hi keys, and hi contains Devanagari chars."""
        result = get_remedies(simple_positions)
        found_bilingual = False
        for planet, data in result.items():
            rem = data.get("remedy") or {}
            if isinstance(rem, dict) and rem.get("en") and rem.get("hi"):
                en, hi = rem["en"], rem["hi"]
                assert en != hi, f"{planet} remedy en==hi (placeholder): {en}"
                has_devanagari = any("\u0900" <= c <= "\u097f" for c in hi)
                assert has_devanagari, (
                    f"{planet} hi remedy has no Devanagari: {hi!r}"
                )
                found_bilingual = True
        assert found_bilingual, "No remedy had both en/hi populated"

    def test_remedy_structure_backward_compat(self, simple_positions):
        """Each entry has legacy 'remedies' list plus new 'remedy' dict."""
        result = get_remedies(simple_positions)
        for planet, data in result.items():
            assert "remedies" in data, f"{planet} missing legacy 'remedies' key"
            assert isinstance(data["remedies"], list)
            assert "remedy" in data
            assert isinstance(data["remedy"], dict)
            assert "sign" in data
            assert "lk_house" in data
            assert 1 <= data["lk_house"] <= 12


# ============================================================
# Golden strength model — afflictions are correctly identified
# ============================================================

class TestGoldenStrengthModel:
    """get_planet_strength_detailed must correctly score ref positions."""

    def test_sun_enemy_capricorn_house2(self):
        """Sun in Capricorn (enemy sign), house 2 — no kendra/trikona bonus applied.

        Source rule (lalkitab_engine.py:925): only houses {1,4,5,7,9,10} get +0.10
        bonus; house 2 is neutral. So score = 0.25 base + 0 house + 0 retro/combust.
        """
        r = get_planet_strength_detailed(
            planet="Sun", sign="Capricorn", house=2,
            is_retrograde=False, is_combust=False,
        )
        assert r["dignity"] == "Enemy"
        assert r["strength_score"] == pytest.approx(0.25, abs=0.001)
        assert "in enemy sign" in r["afflictions"]

    def test_sun_enemy_capricorn_house1_gets_kendra_bonus(self):
        """Same Sun/sign, but in house 1 (kendra) -> +0.10 bonus applied."""
        r = get_planet_strength_detailed(
            planet="Sun", sign="Capricorn", house=1,
            is_retrograde=False, is_combust=False,
        )
        assert r["dignity"] == "Enemy"
        # 0.25 base + 0.10 kendra bonus
        assert r["strength_score"] == pytest.approx(0.35, abs=0.001)

    def test_mars_own_sign_scorpio_dusthana12(self):
        """Mars in own Scorpio, house 12 (dusthana) -> 0.85 - 0.15 = 0.70."""
        r = get_planet_strength_detailed(
            planet="Mars", sign="Scorpio", house=12,
            is_retrograde=False, is_combust=False,
        )
        assert r["dignity"] == "Own Sign"
        assert r["strength_score"] == pytest.approx(0.70, abs=0.001)
        assert "in dusthana house 12" in r["afflictions"]
        assert r["is_afflicted"] is False

    def test_venus_combust_retrograde_accumulates_afflictions(self):
        """Venus combust+retro in Capricorn (friend), house 2.

        Source rule: house 2 gets no bonus. Score = 0.65 base - 0.20 combust
        - 0.10 retrograde = 0.35.
        """
        r = get_planet_strength_detailed(
            planet="Venus", sign="Capricorn", house=2,
            is_retrograde=True, is_combust=True,
        )
        assert r["dignity"] == "Friendly"
        assert "combust" in r["afflictions"]
        assert "retrograde" in r["afflictions"]
        assert r["strength_score"] == pytest.approx(0.35, abs=0.001)

    def test_all_ref_planets_produce_valid_scores(self, chart):
        """Every real chart planet yields a well-formed strength dict."""
        for name, info in chart["planets"].items():
            r = get_planet_strength_detailed(
                planet=name,
                sign=info["sign"],
                house=info["house"],
                is_retrograde=info.get("retrograde", False) or False,
                is_combust=info.get("combust", False) or False,
            )
            assert "dignity" in r
            assert "strength_score" in r
            assert 0.0 <= r["strength_score"] <= 1.0
            assert "afflictions" in r and isinstance(r["afflictions"], list)
            assert "is_afflicted" in r and isinstance(r["is_afflicted"], bool)


# ============================================================
# Golden teva — chart type classification
# ============================================================

class TestGoldenTeva:
    """Validate teva type classification for ref chart."""

    def test_teva_returns_expected_flags(self, list_positions, chart):
        """Ref chart: Jupiter h7, Saturn h1 -> Dharmi teva triggered."""
        if chart.get("_engine") != "swisseph":
            pytest.skip("Teva golden assertion needs swisseph positions")
        result = identify_teva_type(list_positions)
        assert result["is_dharmi"] is True, (
            "Jupiter in 7 + Saturn in 1 should trigger Dharmi teva (PDF 2.1.2)"
        )
        assert result["is_andha"] is False
        assert result["is_ratondha"] is False
        assert result["is_khali"] is False
        assert "dharmi" in result["active_types"]

    def test_teva_description_bilingual(self, list_positions):
        result = identify_teva_type(list_positions)
        desc = result.get("description", {})
        for type_key in ("andha", "ratondha", "dharmi", "nabalig", "khali"):
            assert type_key in desc
            assert "en" in desc[type_key]
            assert "hi" in desc[type_key]


# ============================================================
# Golden milestones — age-driven structure
# ============================================================

class TestGoldenMilestones:
    """Validate milestone timing & shape (age depends on today, so check structure)."""

    def test_milestones_structure(self, list_positions):
        result = calculate_age_milestones(REFERENCE_BIRTH["date"], list_positions)
        assert isinstance(result, dict)
        assert "current_age" in result
        assert isinstance(result["current_age"], int)
        assert result["current_age"] >= 0
        assert result["birth_date"] == REFERENCE_BIRTH["date"]
        assert isinstance(result["milestones"], list)
        assert len(result["milestones"]) >= 7  # multiple classical milestones

    def test_milestone_entries_have_required_fields(self, list_positions):
        result = calculate_age_milestones(REFERENCE_BIRTH["date"], list_positions)
        for ms in result["milestones"]:
            for key in ("age", "ruler", "ruler_house", "ruler_status",
                        "prediction_en", "prediction_hi", "is_past"):
                assert key in ms, f"Milestone missing {key}: {ms}"
            assert ms["ruler_status"] in ("strong", "weak", "moderate")

    def test_milestones_invalid_birthdate_raises(self, list_positions):
        with pytest.raises(ValueError):
            calculate_age_milestones("not-a-date", list_positions)


# ============================================================
# Golden 7-year cycle — deterministic on fixed input age
# ============================================================

class TestGoldenSevenYearCycle:
    """Pass a fixed age so the test is deterministic (independent of today)."""

    def test_age_36_is_saturn_cycle(self, list_positions):
        """Age 36 -> cycle 6 (35-42), ruler Saturn."""
        result = get_seven_year_cycle(36, list_positions)
        ac = result["active_cycle"]
        assert ac["cycle_number"] == 6
        assert ac["ruler"] == "Saturn"
        assert ac["age_range"] == [35, 42]
        # Saturn in house 1 per ref chart
        assert ac["ruler_house"] == 1
        assert ac["years_into_cycle"] == 1
        assert ac["years_remaining"] == 6

    def test_age_10_is_mercury_cycle(self, list_positions):
        """Age 10 -> cycle 2 (7-14), ruler Mercury."""
        result = get_seven_year_cycle(10, list_positions)
        ac = result["active_cycle"]
        assert ac["cycle_number"] == 2
        assert ac["ruler"] == "Mercury"
        assert ac["age_range"] == [7, 14]

    def test_cycle_has_prev_and_next_mid_range(self, list_positions):
        """Mid-range age should have both previous and next cycles populated."""
        result = get_seven_year_cycle(25, list_positions)
        assert result["previous_cycle"] is not None
        assert result["next_cycle"] is not None
        assert "domain" in result["previous_cycle"]
        assert "ruler" in result["next_cycle"]


# ============================================================
# Golden regression — ephemeris drift canary
# ============================================================

class TestGoldenRegression:
    """Single aggregate signature — flips if ANY ref planet drifts."""

    def test_reference_chart_signature_stable(self, chart):
        """Aggregate (planet, sign, house) tuple must exactly match snapshot."""
        if chart.get("_engine") != "swisseph":
            pytest.skip("Signature check valid only for swisseph backend")
        actual_sig = tuple(
            (name, chart["planets"][name]["sign"], chart["planets"][name]["house"])
            for name in sorted(EXPECTED_POSITIONS.keys())
        )
        expected_sig = tuple(
            (name, EXPECTED_POSITIONS[name]["sign"], EXPECTED_POSITIONS[name]["house"])
            for name in sorted(EXPECTED_POSITIONS.keys())
        )
        assert actual_sig == expected_sig, (
            "Ref chart drifted. Update EXPECTED_POSITIONS only after deliberate "
            "ephemeris/ayanamsa change."
        )
