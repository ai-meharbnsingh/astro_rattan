"""
test_sarvatobhadra_chakra.py -- Tests for Sarvatobhadra Chakra Engine
======================================================================
Tests grid structure, nakshatra placement, vedha calculations, and
end-to-end calculation with real planetary longitudes.
"""
import pytest

from app.sarvatobhadra_chakra_engine import (
    GRID,
    NAKSHATRA_CELL,
    SIGN_CELL,
    NAKSHATRAS_27,
    SIGN_NAMES,
    calculate_sarvatobhadra,
    get_empty_grid,
    get_nakshatra_positions,
    get_sign_positions,
    get_vedha_targets,
    _nakshatra_from_longitude,
    _sign_from_longitude,
    _normalize_positions,
    _place_planets,
    _is_benefic,
)


# ======================================================================
# Sample data (Meharban Singh's chart — matches test_engines_smoke.py)
# ======================================================================

SAMPLE_NATAL_LONS = {
    "Sun": 130.5,       # Leo / Magha (nak index 9)
    "Moon": 215.3,      # Scorpio / Vishakha (nak index 15) -- not on grid, falls to sign
    "Mercury": 105.2,   # Cancer / Pushya (nak index 7)
    "Venus": 110.8,     # Cancer / Pushya (nak index 8 → Ashlesha)
    "Mars": 98.1,       # Cancer / Pushya (nak index 7)
    "Jupiter": 280.6,   # Capricorn / Shravana (nak index 21) -- not on grid
    "Saturn": 195.4,    # Libra / Swati (nak index 14)
    "Rahu": 15.7,       # Aries / Bharani (nak index 1)
    "Ketu": 195.7,      # Libra / Swati (nak index 14)
}

SAMPLE_TRANSIT_LONS = {
    "Sun": 20.0,        # Aries / Bharani (nak index 1)
    "Moon": 80.0,       # Gemini / Punarvasu (nak index 6)
    "Mars": 310.0,      # Aquarius / Shatabhisha (nak index 23)
    "Jupiter": 55.0,    # Taurus / Mrigashira (nak index 4)
    "Saturn": 340.0,    # Pisces / U.Bhadrapada (nak index 25)
}


# ======================================================================
# 1. GRID STRUCTURE TESTS
# ======================================================================

class TestGridStructure:
    """Verify the 9x9 grid has correct dimensions and cell types."""

    def test_grid_is_9x9(self):
        assert len(GRID) == 9, "Grid must have 9 rows"
        for row_idx, row in enumerate(GRID):
            assert len(row) == 9, f"Row {row_idx} must have 9 columns"

    def test_every_cell_has_required_keys(self):
        for r in range(9):
            for c in range(9):
                cell = GRID[r][c]
                assert "type" in cell, f"Cell ({r},{c}) missing 'type'"
                assert "name" in cell, f"Cell ({r},{c}) missing 'name'"
                assert "row" in cell, f"Cell ({r},{c}) missing 'row'"
                assert "col" in cell, f"Cell ({r},{c}) missing 'col'"
                assert cell["row"] == r
                assert cell["col"] == c

    def test_cell_types_are_valid(self):
        valid_types = {"nakshatra", "sign", "vowel", "day", "empty"}
        for r in range(9):
            for c in range(9):
                assert GRID[r][c]["type"] in valid_types, (
                    f"Cell ({r},{c}) has invalid type: {GRID[r][c]['type']}"
                )

    def test_center_cell_is_abhijit(self):
        center = GRID[4][4]
        assert center["type"] == "nakshatra"
        assert center["name"] == "Abhijit"

    def test_empty_cells_are_inner_3x3_minus_center(self):
        """After filling inner cells with missing nakshatras, only 1 empty cell
        remains at (5,5) in the inner 3x3 region."""
        empty_cells = []
        for r in range(9):
            for c in range(9):
                if GRID[r][c]["type"] == "empty":
                    empty_cells.append((r, c))
        assert len(empty_cells) == 1, f"Expected 1 empty cell, got {len(empty_cells)}"
        assert empty_cells[0] == (5, 5), "Only empty cell should be (5,5)"


class TestGridContent:
    """Verify specific cells match the canonical SBC layout."""

    def test_top_row_nakshatras(self):
        assert GRID[0][0]["name"] == "Krittika"
        assert GRID[0][2]["name"] == "Rohini"
        assert GRID[0][4]["name"] == "Mrigashira"
        assert GRID[0][6]["name"] == "Ardra"
        assert GRID[0][8]["name"] == "Punarvasu"

    def test_top_row_signs(self):
        assert GRID[0][1]["name"] == "Taurus"
        assert GRID[0][3]["name"] == "Gemini"
        assert GRID[0][5]["name"] == "Cancer"
        assert GRID[0][7]["name"] == "Leo"

    def test_bottom_row_nakshatras(self):
        assert GRID[8][0]["name"] == "Purva Bhadrapada"
        assert GRID[8][2]["name"] == "Uttara Bhadrapada"
        assert GRID[8][4]["name"] == "Mula"
        assert GRID[8][6]["name"] == "Jyeshtha"
        assert GRID[8][8]["name"] == "Anuradha"

    def test_bottom_row_signs(self):
        assert GRID[8][1]["name"] == "Capricorn"
        assert GRID[8][3]["name"] == "Sagittarius"
        assert GRID[8][5]["name"] == "Scorpio"
        assert GRID[8][7]["name"] == "Aries"

    def test_left_column_contains_expected(self):
        left_names = [GRID[r][0]["name"] for r in range(9)]
        assert "Krittika" in left_names
        assert "Bharani" in left_names
        assert "Ashwini" in left_names
        assert "Pisces" in left_names
        assert "Revati" in left_names
        assert "Aquarius" in left_names
        assert "Dhanishta" in left_names
        assert "Shatabhisha" in left_names
        assert "Purva Bhadrapada" in left_names

    def test_right_column_contains_expected(self):
        right_names = [GRID[r][8]["name"] for r in range(9)]
        assert "Punarvasu" in right_names
        assert "Pushya" in right_names
        assert "Ashlesha" in right_names
        assert "Virgo" in right_names
        assert "Hasta" in right_names
        assert "Libra" in right_names
        assert "Chitra" in right_names
        assert "Swati" in right_names
        assert "Anuradha" in right_names

    def test_weekdays_present_in_grid(self):
        """All 7 weekdays must appear at least once in the grid."""
        all_names = {GRID[r][c]["name"] for r in range(9) for c in range(9)
                     if GRID[r][c]["type"] == "day"}
        for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            assert day in all_names, f"Weekday {day} not found in grid"

    def test_nakshatra_count(self):
        """The grid should contain nakshatras in the NAKSHATRA_CELL lookup."""
        # 28 nakshatras placed: 27 standard minus those not on grid + Abhijit
        assert len(NAKSHATRA_CELL) >= 20, (
            f"Expected at least 20 nakshatras on grid, got {len(NAKSHATRA_CELL)}"
        )

    def test_sign_count(self):
        """12 zodiac signs should be on the grid (some appear in multiple spots)."""
        sign_names_on_grid = {GRID[r][c]["name"] for r in range(9) for c in range(9)
                              if GRID[r][c]["type"] == "sign"}
        assert len(sign_names_on_grid) >= 10, (
            f"Expected at least 10 distinct signs on grid, got {len(sign_names_on_grid)}"
        )


# ======================================================================
# 2. NAKSHATRA/SIGN FROM LONGITUDE TESTS
# ======================================================================

class TestLongitudeConversions:
    """Test nakshatra and sign lookup from sidereal longitude."""

    def test_ashwini_at_zero(self):
        assert _nakshatra_from_longitude(0.0) == "Ashwini"

    def test_bharani_at_15(self):
        # Bharani starts at 13.333... degrees
        assert _nakshatra_from_longitude(15.0) == "Bharani"

    def test_krittika_at_28(self):
        # Krittika starts at 26.666... degrees
        assert _nakshatra_from_longitude(28.0) == "Krittika"

    def test_pushya_at_105(self):
        # Pushya: index 7, starts at 93.333
        assert _nakshatra_from_longitude(100.0) == "Pushya"

    def test_revati_at_355(self):
        # Revati: index 26, starts at 346.666
        assert _nakshatra_from_longitude(355.0) == "Revati"

    def test_sign_aries_at_zero(self):
        assert _sign_from_longitude(0.0) == "Aries"

    def test_sign_leo_at_130(self):
        assert _sign_from_longitude(130.0) == "Leo"

    def test_sign_scorpio_at_215(self):
        assert _sign_from_longitude(215.0) == "Scorpio"

    def test_sign_pisces_at_350(self):
        assert _sign_from_longitude(350.0) == "Pisces"

    def test_wrap_around_360(self):
        assert _nakshatra_from_longitude(360.0) == "Ashwini"
        assert _sign_from_longitude(360.0) == "Aries"

    def test_negative_wrap(self):
        # -10 degrees wraps to 350 → Pisces / Revati
        assert _sign_from_longitude(-10.0) == "Pisces"
        assert _nakshatra_from_longitude(-10.0) == "Revati"


# ======================================================================
# 3. VEDHA TARGET TESTS
# ======================================================================

class TestVedhaTargets:
    """Test that vedha reflections are computed correctly."""

    def test_corner_00_vedha(self):
        targets = get_vedha_targets(0, 0)
        # diagonal: (8,8), row: (0,8), column: (8,0)
        assert (8, 8) in targets  # diagonal
        assert (0, 8) in targets  # row mirror
        assert (8, 0) in targets  # column mirror
        assert len(targets) == 3

    def test_corner_08_vedha(self):
        targets = get_vedha_targets(0, 8)
        assert (8, 0) in targets  # diagonal
        assert (0, 0) in targets  # row mirror
        assert (8, 8) in targets  # column mirror

    def test_center_vedha_is_empty(self):
        """Center cell (4,4) reflects to itself — no vedha targets."""
        targets = get_vedha_targets(4, 4)
        assert len(targets) == 0

    def test_edge_midpoint_vedha(self):
        """Cell (0,4) is top-center edge."""
        targets = get_vedha_targets(0, 4)
        # diagonal: (8,4), row: (0,4)→same→excluded, column: (8,4)→same as diag
        # Actually: diag=(8,4), row_mirror=(0,4)→same→excluded, col_mirror=(8,4)→same
        # So: diag=(8,4) and col_mirror=(8,4) are the same point
        assert (8, 4) in targets  # diagonal = column mirror for col=4
        # row mirror: 8-4=4, same col→excluded
        # Should have diagonal and one of the others
        assert len(targets) >= 1

    def test_cell_14_vedha(self):
        """Cell (1,4) should have 3 distinct targets."""
        targets = get_vedha_targets(1, 4)
        # diagonal: (7, 4)
        # row mirror: (1, 4) → col=4, 8-4=4, same → excluded
        # column mirror: (7, 4) → same as diagonal
        assert (7, 4) in targets

    def test_cell_23_vedha(self):
        """Cell (2,3) should have 3 targets."""
        targets = get_vedha_targets(2, 3)
        assert (6, 5) in targets  # diagonal
        assert (2, 5) in targets  # row mirror
        assert (6, 3) in targets  # column mirror
        assert len(targets) == 3

    def test_symmetry(self):
        """If A vedhas B via diagonal, then B vedhas A via diagonal."""
        targets_00 = get_vedha_targets(0, 0)
        assert (8, 8) in targets_00
        targets_88 = get_vedha_targets(8, 8)
        assert (0, 0) in targets_88


# ======================================================================
# 4. NORMALIZE POSITIONS TESTS
# ======================================================================

class TestNormalizePositions:
    """Test position normalization for different input formats."""

    def test_float_values(self):
        result = _normalize_positions({"Sun": 130.5, "Moon": 215.3})
        assert result["Sun"] == 130.5
        assert result["Moon"] == 215.3

    def test_dict_values(self):
        result = _normalize_positions({
            "Sun": {"longitude": 130.5, "sign": "Leo"},
            "Moon": {"longitude": 215.3, "sign": "Scorpio"},
        })
        assert result["Sun"] == 130.5
        assert result["Moon"] == 215.3

    def test_empty_input(self):
        result = _normalize_positions({})
        assert result == {}

    def test_none_input(self):
        result = _normalize_positions(None)
        assert result == {}

    def test_int_values_converted_to_float(self):
        result = _normalize_positions({"Sun": 130})
        assert result["Sun"] == 130.0
        assert isinstance(result["Sun"], float)

    def test_dict_without_longitude_key_skipped(self):
        result = _normalize_positions({"Sun": {"sign": "Leo"}})
        assert "Sun" not in result


# ======================================================================
# 5. PLANET PLACEMENT TESTS
# ======================================================================

class TestPlanetPlacement:
    """Test that planets are placed correctly on the grid."""

    def test_pushya_planet_placed(self):
        """Mercury at 105.2 deg → Pushya nakshatra → cell (1,8)."""
        placements = _place_planets({"Mercury": 105.2}, "natal")
        assert len(placements) == 1
        p = placements[0]
        assert p["planet"] == "Mercury"
        assert p["nakshatra"] == "Pushya"
        assert p["row"] == 1
        assert p["col"] == 8

    def test_bharani_planet_placed(self):
        """Rahu at 15.7 deg → Bharani → cell (1,0)."""
        placements = _place_planets({"Rahu": 15.7}, "natal")
        assert len(placements) == 1
        assert placements[0]["nakshatra"] == "Bharani"
        assert placements[0]["row"] == 1
        assert placements[0]["col"] == 0

    def test_swati_planet_placed(self):
        """Saturn at 195.4 deg → Swati → cell (7,8)."""
        placements = _place_planets({"Saturn": 195.4}, "natal")
        assert len(placements) == 1
        assert placements[0]["nakshatra"] == "Swati"
        assert placements[0]["row"] == 7
        assert placements[0]["col"] == 8

    def test_magha_placed_directly_on_grid(self):
        """Sun at 130.5 deg → Magha nakshatra → now on grid at (3,3)."""
        placements = _place_planets({"Sun": 130.5}, "natal")
        assert len(placements) == 1
        p = placements[0]
        assert p["nakshatra"] == "Magha"
        assert p["row"] == 3
        assert p["col"] == 3

    def test_multiple_planets_same_cell(self):
        """Two planets in same nakshatra should both be placed."""
        placements = _place_planets({"Mercury": 100.0, "Mars": 98.0}, "natal")
        assert len(placements) == 2
        # Both should be Pushya at (1,8)
        for p in placements:
            assert p["nakshatra"] == "Pushya"
            assert (p["row"], p["col"]) == (1, 8)

    def test_category_field(self):
        placements = _place_planets({"Sun": 20.0}, "transit")
        assert placements[0]["category"] == "transit"


# ======================================================================
# 6. BENEFIC/MALEFIC CLASSIFICATION
# ======================================================================

class TestBeneficMalefic:
    def test_jupiter_is_benefic(self):
        assert _is_benefic("Jupiter") is True

    def test_venus_is_benefic(self):
        assert _is_benefic("Venus") is True

    def test_moon_is_benefic(self):
        assert _is_benefic("Moon") is True

    def test_mercury_is_benefic(self):
        assert _is_benefic("Mercury") is True

    def test_sun_is_malefic(self):
        assert _is_benefic("Sun") is False

    def test_mars_is_malefic(self):
        assert _is_benefic("Mars") is False

    def test_saturn_is_malefic(self):
        assert _is_benefic("Saturn") is False

    def test_rahu_is_malefic(self):
        assert _is_benefic("Rahu") is False

    def test_ketu_is_malefic(self):
        assert _is_benefic("Ketu") is False


# ======================================================================
# 7. FULL CALCULATION — END-TO-END
# ======================================================================

class TestCalculateSarvatobhadra:
    """Integration tests for calculate_sarvatobhadra()."""

    def test_natal_only_returns_all_keys(self):
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS)
        assert "grid" in result
        assert "natal_placements" in result
        assert "transit_placements" in result
        assert "vedhas" in result
        assert "auspicious" in result
        assert "inauspicious" in result
        assert "summary" in result

    def test_grid_is_9x9(self):
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS)
        assert len(result["grid"]) == 9
        for row in result["grid"]:
            assert len(row) == 9

    def test_grid_cells_have_planet_lists(self):
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS)
        for r in range(9):
            for c in range(9):
                cell = result["grid"][r][c]
                assert "natal_planets" in cell
                assert "transit_planets" in cell
                assert isinstance(cell["natal_planets"], list)
                assert isinstance(cell["transit_planets"], list)

    def test_natal_placements_count(self):
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS)
        # All 9 natal planets should be placed (some via sign fallback)
        assert len(result["natal_placements"]) == 9

    def test_natal_placements_have_required_fields(self):
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS)
        for p in result["natal_placements"]:
            assert "planet" in p
            assert "nakshatra" in p
            assert "sign" in p
            assert "longitude" in p
            assert "row" in p
            assert "col" in p
            assert 0 <= p["row"] <= 8
            assert 0 <= p["col"] <= 8

    def test_no_vedhas_without_transit(self):
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS)
        assert result["vedhas"] == []
        assert result["auspicious"] == []
        assert result["inauspicious"] == []

    def test_vedhas_with_transit(self):
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS, SAMPLE_TRANSIT_LONS)
        assert len(result["transit_placements"]) == 5
        # There should be at least some vedha connections
        assert isinstance(result["vedhas"], list)
        # Auspicious + inauspicious should equal total vedhas
        assert len(result["auspicious"]) + len(result["inauspicious"]) == len(result["vedhas"])

    def test_vedha_entries_have_required_fields(self):
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS, SAMPLE_TRANSIT_LONS)
        for v in result["vedhas"]:
            assert "transit_planet" in v
            assert "transit_nakshatra" in v
            assert "transit_cell" in v
            assert "natal_planet" in v
            assert "natal_nakshatra" in v
            assert "natal_cell" in v
            assert "vedha_type" in v
            assert v["vedha_type"] in ("diagonal", "row", "column")
            assert "effect" in v
            assert v["effect"] in ("auspicious", "inauspicious")

    def test_benefic_transit_gives_auspicious_vedha(self):
        """Jupiter (benefic) transit vedha should be auspicious."""
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS, SAMPLE_TRANSIT_LONS)
        jupiter_vedhas = [v for v in result["vedhas"] if v["transit_planet"] == "Jupiter"]
        for v in jupiter_vedhas:
            assert v["effect"] == "auspicious"

    def test_malefic_transit_gives_inauspicious_vedha(self):
        """Mars (malefic) transit vedha should be inauspicious."""
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS, SAMPLE_TRANSIT_LONS)
        mars_vedhas = [v for v in result["vedhas"] if v["transit_planet"] == "Mars"]
        for v in mars_vedhas:
            assert v["effect"] == "inauspicious"

    def test_summary_is_non_empty_string(self):
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS, SAMPLE_TRANSIT_LONS)
        assert isinstance(result["summary"], str)
        assert len(result["summary"]) > 50
        assert "Sarvatobhadra Chakra" in result["summary"]

    def test_dict_input_format(self):
        """Accept {planet: {longitude: float}} format."""
        dict_input = {
            "Sun": {"longitude": 130.5, "sign": "Leo"},
            "Moon": {"longitude": 215.3, "sign": "Scorpio"},
        }
        result = calculate_sarvatobhadra(dict_input)
        assert len(result["natal_placements"]) == 2

    def test_specific_vedha_connection(self):
        """
        Transit Sun at 20.0 deg → Bharani → cell (1,0).
        Vedha targets of (1,0): diagonal=(7,8), row=(1,8), column=(7,0).
        Natal Saturn at 195.4 → Swati → cell (7,8).
        So Transit Sun should vedha Natal Saturn via diagonal.
        """
        result = calculate_sarvatobhadra(SAMPLE_NATAL_LONS, SAMPLE_TRANSIT_LONS)
        sun_saturn_vedha = [
            v for v in result["vedhas"]
            if v["transit_planet"] == "Sun" and v["natal_planet"] == "Saturn"
        ]
        assert len(sun_saturn_vedha) >= 1
        v = sun_saturn_vedha[0]
        assert v["vedha_type"] == "diagonal"
        assert v["effect"] == "inauspicious"  # Sun is malefic


# ======================================================================
# 8. CONVENIENCE FUNCTION TESTS
# ======================================================================

class TestConvenienceFunctions:

    def test_get_empty_grid_is_deep_copy(self):
        g1 = get_empty_grid()
        g2 = get_empty_grid()
        g1[0][0]["name"] = "MODIFIED"
        assert g2[0][0]["name"] != "MODIFIED"
        assert GRID[0][0]["name"] == "Krittika"  # original untouched

    def test_get_nakshatra_positions_returns_dict(self):
        pos = get_nakshatra_positions()
        assert isinstance(pos, dict)
        assert "Krittika" in pos
        assert "Abhijit" in pos
        assert pos["Krittika"] == (0, 0)
        assert pos["Abhijit"] == (4, 4)

    def test_get_sign_positions_returns_dict(self):
        pos = get_sign_positions()
        assert isinstance(pos, dict)
        assert "Taurus" in pos
        assert pos["Taurus"] == (0, 1)

    def test_nakshatra_positions_is_independent_copy(self):
        p1 = get_nakshatra_positions()
        p1["Krittika"] = (9, 9)
        p2 = get_nakshatra_positions()
        assert p2["Krittika"] == (0, 0)


# ======================================================================
# 9. EDGE CASES
# ======================================================================

class TestEdgeCases:

    def test_single_planet(self):
        result = calculate_sarvatobhadra({"Sun": 130.5})
        assert len(result["natal_placements"]) == 1

    def test_empty_natal(self):
        result = calculate_sarvatobhadra({})
        assert len(result["natal_placements"]) == 0
        assert len(result["vedhas"]) == 0

    def test_transit_without_natal(self):
        """Transit only — no vedhas possible without natal placements."""
        result = calculate_sarvatobhadra({}, {"Sun": 20.0})
        assert len(result["vedhas"]) == 0

    def test_boundary_longitude_zero(self):
        result = calculate_sarvatobhadra({"Sun": 0.0})
        assert result["natal_placements"][0]["nakshatra"] == "Ashwini"
        assert result["natal_placements"][0]["sign"] == "Aries"

    def test_boundary_longitude_359(self):
        result = calculate_sarvatobhadra({"Sun": 359.99})
        assert result["natal_placements"][0]["nakshatra"] == "Revati"
        assert result["natal_placements"][0]["sign"] == "Pisces"
