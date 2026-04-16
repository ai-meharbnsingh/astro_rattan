"""Tests for Lal Kitab Bunyaad, Takkar, and Enemy Presence analysis."""
import pytest

from app.lalkitab_advanced import (
    calculate_bunyaad,
    calculate_takkar,
    calculate_enemy_presence,
    PAKKA_GHAR,
    BUNYAAD_HOUSE,
    LK_ENEMIES,
)


# ─────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def standard_positions():
    """A typical chart with planets spread across houses."""
    return [
        {"planet": "Sun", "house": 1},
        {"planet": "Moon", "house": 4},
        {"planet": "Mars", "house": 3},
        {"planet": "Mercury", "house": 7},
        {"planet": "Jupiter", "house": 2},
        {"planet": "Venus", "house": 7},
        {"planet": "Saturn", "house": 10},
        {"planet": "Rahu", "house": 12},
        {"planet": "Ketu", "house": 6},
    ]


@pytest.fixture
def afflicted_bunyaad_positions():
    """Chart where Jupiter's bunyaad (house 10) has Saturn (enemy)."""
    return [
        {"planet": "Sun", "house": 1},
        {"planet": "Moon", "house": 5},
        {"planet": "Mars", "house": 6},
        {"planet": "Mercury", "house": 3},
        {"planet": "Jupiter", "house": 9},
        {"planet": "Venus", "house": 11},
        {"planet": "Saturn", "house": 10},   # Saturn in house 10 = Jupiter's bunyaad
        {"planet": "Rahu", "house": 10},     # Rahu also enemy of Jupiter
        {"planet": "Ketu", "house": 4},
    ]


@pytest.fixture
def takkar_1_8_positions():
    """Chart with a 1-8 takkar: Saturn in 3, Jupiter in 10 (8th from 3)."""
    return [
        {"planet": "Sun", "house": 1},
        {"planet": "Moon", "house": 4},
        {"planet": "Mars", "house": 5},
        {"planet": "Mercury", "house": 7},
        {"planet": "Jupiter", "house": 10},
        {"planet": "Venus", "house": 11},
        {"planet": "Saturn", "house": 3},     # 8th from 3 = 10 → hits Jupiter
        {"planet": "Rahu", "house": 12},
        {"planet": "Ketu", "house": 6},
    ]


@pytest.fixture
def all_in_one_house():
    """Edge case: all planets in house 1."""
    return [
        {"planet": "Sun", "house": 1},
        {"planet": "Moon", "house": 1},
        {"planet": "Mars", "house": 1},
        {"planet": "Mercury", "house": 1},
        {"planet": "Jupiter", "house": 1},
        {"planet": "Venus", "house": 1},
        {"planet": "Saturn", "house": 1},
        {"planet": "Rahu", "house": 1},
        {"planet": "Ketu", "house": 1},
    ]


@pytest.fixture
def empty_houses_positions():
    """Chart with only 2 planets — many empty houses."""
    return [
        {"planet": "Sun", "house": 1},
        {"planet": "Moon", "house": 7},
    ]


# ─────────────────────────────────────────────────────────────
# 1. BUNYAAD TESTS
# ─────────────────────────────────────────────────────────────

class TestBunyaad:
    """Tests for calculate_bunyaad."""

    def test_bunyaad_house_correctness(self):
        """Verify precomputed bunyaad houses match 9th-from-pakka-ghar formula."""
        expected = {
            "Sun": 9,       # 1 + 8 = 9
            "Moon": 12,     # 4 + 8 = 12
            "Mars": 11,     # 3 + 8 = 11
            "Mercury": 3,   # 7 + 8 = 15 % 12 = 3
            "Jupiter": 10,  # 2 + 8 = 10
            "Venus": 3,     # 7 + 8 = 15 % 12 = 3
            "Saturn": 4,    # 8 + 8 = 16 % 12 = 4
            "Rahu": 8,      # 12 + 8 = 20 % 12 = 8
            "Ketu": 2,      # 6 + 8 = 14 % 12 = 2
        }
        for planet, expected_house in expected.items():
            assert BUNYAAD_HOUSE[planet] == expected_house, (
                f"{planet}: expected bunyaad house {expected_house}, got {BUNYAAD_HOUSE[planet]}"
            )

    def test_bunyaad_returns_all_planets(self, standard_positions):
        """Result should have an entry for every planet in the input."""
        result = calculate_bunyaad(standard_positions)
        for p in standard_positions:
            assert p["planet"] in result["planets"]

    def test_bunyaad_afflicted_detection(self, afflicted_bunyaad_positions):
        """Jupiter's bunyaad (house 10) has Saturn and Rahu — should be afflicted."""
        result = calculate_bunyaad(afflicted_bunyaad_positions)
        jup = result["planets"]["Jupiter"]
        assert jup["bunyaad_house"] == 10
        assert jup["bunyaad_status"] == "afflicted"
        assert "Saturn" in jup["enemies_in_bunyaad"]
        assert "Rahu" in jup["enemies_in_bunyaad"]
        assert "Jupiter" in result["collapsed_planets"]

    def test_bunyaad_strong_detection(self, standard_positions):
        """Mars bunyaad is house 11 — Venus is there but not an enemy of Mars."""
        result = calculate_bunyaad(standard_positions)
        mars = result["planets"]["Mars"]
        assert mars["bunyaad_house"] == 11
        # No enemies of Mars in house 11 in the standard positions
        # (house 11 is empty in standard_positions since no planet has house=11)
        assert mars["bunyaad_status"] == "empty"
        assert "Mars" in result["strong_foundations"]

    def test_bunyaad_empty_house(self, empty_houses_positions):
        """With only 2 planets, most bunyaad houses will be empty."""
        result = calculate_bunyaad(empty_houses_positions)
        sun = result["planets"]["Sun"]
        assert sun["bunyaad_status"] == "empty"
        assert sun["planets_in_bunyaad"] == []

    def test_bunyaad_bilingual_interpretation(self, standard_positions):
        """Each planet entry must have both en and hi interpretations."""
        result = calculate_bunyaad(standard_positions)
        for planet_name, data in result["planets"].items():
            assert "interpretation_en" in data, f"{planet_name} missing interpretation_en"
            assert "interpretation_hi" in data, f"{planet_name} missing interpretation_hi"
            assert len(data["interpretation_en"]) > 0
            assert len(data["interpretation_hi"]) > 0

    def test_bunyaad_pakka_ghar_values(self, standard_positions):
        """Each planet's pakka_ghar should match the PAKKA_GHAR constant."""
        result = calculate_bunyaad(standard_positions)
        for planet_name, data in result["planets"].items():
            assert data["pakka_ghar"] == PAKKA_GHAR[planet_name]

    def test_collapsed_and_strong_are_disjoint(self, afflicted_bunyaad_positions):
        """No planet should appear in both collapsed and strong lists."""
        result = calculate_bunyaad(afflicted_bunyaad_positions)
        collapsed = set(result["collapsed_planets"])
        strong = set(result["strong_foundations"])
        assert collapsed.isdisjoint(strong), "A planet cannot be both collapsed and strong"


# ─────────────────────────────────────────────────────────────
# 2. TAKKAR TESTS
# ─────────────────────────────────────────────────────────────

class TestTakkar:
    """Tests for calculate_takkar."""

    def test_1_8_takkar_detected(self, takkar_1_8_positions):
        """Saturn in 3, Jupiter in 10 (8th from 3) — should detect 1-8 takkar."""
        result = calculate_takkar(takkar_1_8_positions)
        axis_18 = [c for c in result["collisions"] if c["axis"] == "1-8"]
        # Find the Saturn → Jupiter collision
        sat_jup = [
            c for c in axis_18
            if c["attacker"] == "Saturn" and c["receiver"] == "Jupiter"
        ]
        assert len(sat_jup) == 1, "Expected Saturn→Jupiter 1-8 takkar"
        assert sat_jup[0]["severity"] == "destructive"  # Saturn is enemy of Jupiter
        assert sat_jup[0]["are_enemies"] is True

    def test_non_enemy_collision_is_mild(self):
        """Two non-enemy planets in 1-8 axis should have mild severity."""
        positions = [
            {"planet": "Sun", "house": 1},
            {"planet": "Jupiter", "house": 8},   # 8th from house 1
        ]
        result = calculate_takkar(positions)
        axis_18 = [c for c in result["collisions"] if c["axis"] == "1-8"]
        # Sun and Jupiter are not enemies of each other
        sun_jup = [
            c for c in axis_18
            if c["attacker"] == "Sun" and c["receiver"] == "Jupiter"
        ]
        assert len(sun_jup) == 1
        assert sun_jup[0]["severity"] == "mild"

    def test_destructive_count(self, takkar_1_8_positions):
        """Destructive count should match the number of destructive collisions."""
        result = calculate_takkar(takkar_1_8_positions)
        actual_destructive = sum(1 for c in result["collisions"] if c["severity"] == "destructive")
        assert result["destructive_count"] == actual_destructive

    def test_mild_count(self, takkar_1_8_positions):
        """Mild count should match the number of mild collisions."""
        result = calculate_takkar(takkar_1_8_positions)
        actual_mild = sum(1 for c in result["collisions"] if c["severity"] == "mild")
        assert result["mild_count"] == actual_mild

    def test_safe_planets_no_attacks(self, empty_houses_positions):
        """With Sun in 1 and Moon in 7: 1-8 axis would be houses 1→8, 7→2. No collision."""
        result = calculate_takkar(empty_houses_positions)
        # Sun is in 1, Moon in 7. 8th from 1 = 8, 8th from 7 = 2. No match.
        assert "Sun" in result["safe_planets"] or "Moon" in result["safe_planets"]

    def test_all_in_one_house_no_1_8_collision(self, all_in_one_house):
        """All planets in house 1: no 1-8 axis collision (need different houses)."""
        result = calculate_takkar(all_in_one_house)
        axis_18 = [c for c in result["collisions"] if c["axis"] == "1-8"]
        assert len(axis_18) == 0, "Same-house planets cannot have 1-8 collision"

    def test_takkar_bilingual_interpretation(self, takkar_1_8_positions):
        """Each collision entry must have both en and hi interpretations."""
        result = calculate_takkar(takkar_1_8_positions)
        for collision in result["collisions"]:
            assert "interpretation_en" in collision
            assert "interpretation_hi" in collision
            assert len(collision["interpretation_en"]) > 0
            assert len(collision["interpretation_hi"]) > 0

    def test_1_6_axis_detected(self):
        """Saturn in 1 and Mars in 6 — 6th from 1 is 6. Saturn and Mars are enemies."""
        positions = [
            {"planet": "Saturn", "house": 1},
            {"planet": "Mars", "house": 6},   # 6th from house 1
        ]
        result = calculate_takkar(positions)
        axis_16 = [
            c for c in result["collisions"]
            if c["axis"] == "1-6" and c["attacker"] == "Saturn" and c["receiver"] == "Mars"
        ]
        assert len(axis_16) == 1
        assert axis_16[0]["are_enemies"] is True
        assert axis_16[0]["severity"] == "destructive"

    def test_most_attacked_planet(self):
        """Planet receiving the most hits should be identified."""
        # Jupiter in 8 (8th from 1). Sun in 1 attacks Jupiter. Mars in 1 also attacks.
        positions = [
            {"planet": "Sun", "house": 1},
            {"planet": "Mars", "house": 1},
            {"planet": "Jupiter", "house": 8},
        ]
        result = calculate_takkar(positions)
        # Jupiter receives from both Sun and Mars on 1-8 axis
        assert result["most_attacked_planet"] == "Jupiter"


# ─────────────────────────────────────────────────────────────
# 3. ENEMY PRESENCE TESTS
# ─────────────────────────────────────────────────────────────

class TestEnemyPresence:
    """Tests for calculate_enemy_presence."""

    def test_returns_all_planets(self, standard_positions):
        """Result should have an entry for every planet."""
        result = calculate_enemy_presence(standard_positions)
        for p in standard_positions:
            assert p["planet"] in result["planets"]

    def test_enemies_in_pakka_ghar(self):
        """Mercury's pakka ghar is 7. If Moon is in 7, Moon is Mercury's enemy."""
        positions = [
            {"planet": "Mercury", "house": 3},
            {"planet": "Moon", "house": 7},      # Moon in Mercury's pakka ghar (7)
        ]
        result = calculate_enemy_presence(positions)
        merc = result["planets"]["Mercury"]
        assert "Moon" in merc["enemies_in_pakka_ghar"]

    def test_enemies_in_current_house(self):
        """Saturn in house 5 with Sun (enemy) also in house 5."""
        positions = [
            {"planet": "Saturn", "house": 5},
            {"planet": "Sun", "house": 5},        # Sun is enemy of Saturn
        ]
        result = calculate_enemy_presence(positions)
        sat = result["planets"]["Saturn"]
        assert "Sun" in sat["enemies_in_current_house"]

    def test_siege_level_severe(self):
        """Jupiter with 3+ enemies across key houses should be 'severe'."""
        positions = [
            {"planet": "Jupiter", "house": 1},
            {"planet": "Mercury", "house": 2},    # enemy in pakka ghar (2)
            {"planet": "Venus", "house": 1},       # enemy in current house
            {"planet": "Rahu", "house": 7},        # enemy in aspected house (Jupiter in 1 aspects 7)
        ]
        result = calculate_enemy_presence(positions)
        jup = result["planets"]["Jupiter"]
        assert jup["enemy_siege_level"] == "severe"
        assert jup["total_enemies"] >= 3

    def test_siege_level_none(self, empty_houses_positions):
        """Sun with no enemies nearby should have siege level 'none'."""
        # Sun enemies: Saturn, Rahu, Ketu — none present
        result = calculate_enemy_presence(empty_houses_positions)
        sun = result["planets"]["Sun"]
        assert sun["enemy_siege_level"] in ("none", "mild")

    def test_most_and_least_besieged(self, standard_positions):
        """most_besieged and least_besieged should be valid planet names."""
        result = calculate_enemy_presence(standard_positions)
        assert result["most_besieged"] in [p["planet"] for p in standard_positions]
        assert result["least_besieged"] in [p["planet"] for p in standard_positions]

    def test_bilingual_interpretation(self, standard_positions):
        """Each planet entry must have en and hi interpretations."""
        result = calculate_enemy_presence(standard_positions)
        for planet_name, data in result["planets"].items():
            assert "interpretation_en" in data
            assert "interpretation_hi" in data
            assert len(data["interpretation_en"]) > 0
            assert len(data["interpretation_hi"]) > 0

    def test_all_in_one_house_enemy_detection(self, all_in_one_house):
        """All planets in same house: enemies in current house should be detected."""
        result = calculate_enemy_presence(all_in_one_house)
        # Saturn has enemies Sun, Moon, Mars — all are in house 1 with Saturn
        sat = result["planets"]["Saturn"]
        assert "Sun" in sat["enemies_in_current_house"]
        assert "Moon" in sat["enemies_in_current_house"]
        assert "Mars" in sat["enemies_in_current_house"]

    def test_self_not_counted_as_enemy(self, standard_positions):
        """A planet should never appear as its own enemy."""
        result = calculate_enemy_presence(standard_positions)
        for planet_name, data in result["planets"].items():
            all_enemies = (
                data["enemies_in_pakka_ghar"]
                + data["enemies_in_current_house"]
                + data["enemies_in_aspected_houses"]
            )
            assert planet_name not in all_enemies, f"{planet_name} counted as its own enemy"
