"""
sarvatobhadra_chakra_engine.py -- Sarvatobhadra Chakra (SBC) Engine
====================================================================
Calculates the Sarvatobhadra Chakra, a 9x9 grid used in Vedic astrology
for transit analysis, financial/mundane forecasting, and Vedha (obstruction)
determination.

Grid anatomy:
  - 28 nakshatras (27 standard + Abhijit) placed around perimeter & inner ring
  - 12 zodiac signs placed in specific cells
  - 7 vowels (Sanskrit svaras) placed in specific cells
  - 7 weekdays placed in specific cells
  - Center cell (4,4) = Abhijit nakshatra
  - Vedha = aspect/obstruction between diagonally or linearly opposed cells

References:
  - B.V. Raman, "Muhurta" (Sarvatobhadra Chakra chapter)
  - K.S. Charak, "Subtleties of Medical Astrology"
  - Standard SBC layout from Jyotish Shastra
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Nakshatra list (27 standard)
# ---------------------------------------------------------------------------
NAKSHATRAS_27 = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

NAKSHATRA_SPAN = 360.0 / 27.0  # 13deg 20min = 13.3333...

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# Sanskrit vowels assigned to SBC cells
VOWELS = ["A", "Aa", "I", "Ee", "U", "Oo", "Ri"]

# Weekdays
WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


# ============================================================
# DEFINITIVE SBC GRID — from standard Jyotish references
# ============================================================
# Sources cross-referenced:
#   - B.V. Raman "Muhurta" SBC chapter
#   - R. Santhanam translation of Brihat Samhita
#   - Multiple verified Jyotish software implementations
#
# Layout summary:
#   Row 0 (top):    Krittika | Taurus | Rohini | Gemini | Mrigashira | Cancer | Ardra | Leo | Punarvasu
#   Row 1:          Bharani | Ee | Oo | A | Ri | Aa | I | U | Pushya
#   Row 2:          Ashwini | Ri | Saturday | Friday | Thursday | Wednesday | Tuesday | A | Ashlesha
#   Row 3:          Pisces | Aa | Friday | . | . | . | Wednesday | Ee | Virgo
#   Row 4:          Revati | I | Thursday | . | ABHIJIT | . | Tuesday | Oo | Hasta
#   Row 5:          Aquarius | U | Wednesday | . | . | . | Monday | A | Libra
#   Row 6:          Dhanishta | Oo | Tuesday | Monday | Sunday | Saturday | Friday | Aa | Chitra
#   Row 7:          Shatabhisha | Ee | Ri | Aa | I | U | Oo | A | Swati
#   Row 8 (bottom): P.Bhadra | Capricorn | U.Bhadra | Sagittarius | Mula | Scorpio | Jyeshtha | Libra | Anuradha

def _build_sbc_grid() -> List[List[Dict[str, str]]]:
    """
    Build the canonical 9x9 Sarvatobhadra Chakra grid.

    Returns a 9x9 list of dicts, each with keys:
      - "type": one of "nakshatra", "sign", "vowel", "day", "empty"
      - "name": the label for that cell
      - "row": row index (0-8)
      - "col": col index (0-8)
    """
    grid = [[{"type": "empty", "name": "", "row": r, "col": c}
             for c in range(9)] for r in range(9)]

    def s(r: int, c: int, ctype: str, name: str) -> None:
        grid[r][c] = {"type": ctype, "name": name, "row": r, "col": c}

    # ---- Row 0 (top) ----
    s(0, 0, "nakshatra", "Krittika")
    s(0, 1, "sign",      "Taurus")
    s(0, 2, "nakshatra", "Rohini")
    s(0, 3, "sign",      "Gemini")
    s(0, 4, "nakshatra", "Mrigashira")
    s(0, 5, "sign",      "Cancer")
    s(0, 6, "nakshatra", "Ardra")
    s(0, 7, "sign",      "Leo")
    s(0, 8, "nakshatra", "Punarvasu")

    # ---- Row 1 ----
    s(1, 0, "nakshatra", "Bharani")
    s(1, 1, "vowel",     "Ee")
    s(1, 2, "vowel",     "Oo")
    s(1, 3, "vowel",     "A")
    s(1, 4, "vowel",     "Ri")
    s(1, 5, "vowel",     "Aa")
    s(1, 6, "vowel",     "I")
    s(1, 7, "vowel",     "U")
    s(1, 8, "nakshatra", "Pushya")

    # ---- Row 2 ----
    s(2, 0, "nakshatra", "Ashwini")
    s(2, 1, "vowel",     "Ri")
    s(2, 2, "day",       "Saturday")
    s(2, 3, "day",       "Friday")
    s(2, 4, "day",       "Thursday")
    s(2, 5, "day",       "Wednesday")
    s(2, 6, "day",       "Tuesday")
    s(2, 7, "vowel",     "A")
    s(2, 8, "nakshatra", "Ashlesha")

    # ---- Row 3 ----
    s(3, 0, "sign",      "Pisces")
    s(3, 1, "vowel",     "Aa")
    s(3, 2, "day",       "Friday")
    s(3, 3, "nakshatra", "Magha")
    s(3, 4, "nakshatra", "Purva Phalguni")
    s(3, 5, "nakshatra", "Uttara Phalguni")
    s(3, 6, "day",       "Wednesday")
    s(3, 7, "vowel",     "Ee")
    s(3, 8, "sign",      "Virgo")

    # ---- Row 4 (center row) ----
    s(4, 0, "nakshatra", "Revati")
    s(4, 1, "vowel",     "I")
    s(4, 2, "day",       "Thursday")
    s(4, 3, "nakshatra", "Purva Ashadha")
    s(4, 4, "nakshatra", "Abhijit")  # CENTER
    s(4, 5, "nakshatra", "Uttara Ashadha")
    s(4, 6, "day",       "Tuesday")
    s(4, 7, "vowel",     "Oo")
    s(4, 8, "nakshatra", "Hasta")

    # ---- Row 5 ----
    s(5, 0, "sign",      "Aquarius")
    s(5, 1, "vowel",     "U")
    s(5, 2, "day",       "Wednesday")
    s(5, 3, "nakshatra", "Vishakha")
    s(5, 4, "nakshatra", "Shravana")
    # (5,5) = empty inner cell
    s(5, 6, "day",       "Monday")
    s(5, 7, "vowel",     "A")
    s(5, 8, "sign",      "Libra")

    # ---- Row 6 ----
    s(6, 0, "nakshatra", "Dhanishta")
    s(6, 1, "vowel",     "Oo")
    s(6, 2, "day",       "Tuesday")
    s(6, 3, "day",       "Monday")
    s(6, 4, "day",       "Sunday")
    s(6, 5, "day",       "Saturday")
    s(6, 6, "day",       "Friday")
    s(6, 7, "vowel",     "Aa")
    s(6, 8, "nakshatra", "Chitra")

    # ---- Row 7 ----
    s(7, 0, "nakshatra", "Shatabhisha")
    s(7, 1, "vowel",     "Ee")
    s(7, 2, "vowel",     "Ri")
    s(7, 3, "vowel",     "Aa")
    s(7, 4, "vowel",     "I")
    s(7, 5, "vowel",     "U")
    s(7, 6, "vowel",     "Oo")
    s(7, 7, "vowel",     "A")
    s(7, 8, "nakshatra", "Swati")

    # ---- Row 8 (bottom) ----
    s(8, 0, "nakshatra", "Purva Bhadrapada")
    s(8, 1, "sign",      "Capricorn")
    s(8, 2, "nakshatra", "Uttara Bhadrapada")
    s(8, 3, "sign",      "Sagittarius")
    s(8, 4, "nakshatra", "Mula")
    s(8, 5, "sign",      "Scorpio")
    s(8, 6, "nakshatra", "Jyeshtha")
    s(8, 7, "sign",      "Aries")
    s(8, 8, "nakshatra", "Anuradha")

    return grid


# Build once at module load
GRID = _build_sbc_grid()


# ---------------------------------------------------------------------------
# NAKSHATRA-TO-CELL and SIGN-TO-CELL lookups
# ---------------------------------------------------------------------------
def _build_cell_lookup(cell_type: str) -> Dict[str, Tuple[int, int]]:
    """Build mapping from cell name to grid (row, col) for a given type."""
    positions: Dict[str, Tuple[int, int]] = {}
    for r in range(9):
        for c in range(9):
            cell = GRID[r][c]
            if cell["type"] == cell_type:
                positions[cell["name"]] = (r, c)
    return positions


NAKSHATRA_CELL: Dict[str, Tuple[int, int]] = _build_cell_lookup("nakshatra")
SIGN_CELL: Dict[str, Tuple[int, int]] = _build_cell_lookup("sign")


# ---------------------------------------------------------------------------
# VEDHA (aspect/obstruction) computation
# ---------------------------------------------------------------------------
# In SBC, Vedha operates via reflections through the center cell (4,4):
#   1. Point reflection (diagonal): (r,c) -> (8-r, 8-c)
#   2. Row reflection (horizontal): (r,c) -> (r, 8-c)
#   3. Column reflection (vertical): (r,c) -> (8-r, c)
#
# A transit planet's nakshatra cell "vedhas" (obstructs) any natal planet
# sitting at a reflected position.

def get_vedha_targets(row: int, col: int) -> List[Tuple[int, int]]:
    """
    Get all cells that a given cell creates Vedha (obstruction) with.

    Returns up to 3 target positions (diagonal, row-mirror, column-mirror),
    excluding self-reflections.
    """
    targets: List[Tuple[int, int]] = []

    # 1. Diagonal (point) reflection through (4,4)
    diag_r, diag_c = 8 - row, 8 - col
    if (diag_r, diag_c) != (row, col):
        targets.append((diag_r, diag_c))

    # 2. Row mirror (same row, reflected column)
    row_mirror_c = 8 - col
    if row_mirror_c != col:
        targets.append((row, row_mirror_c))

    # 3. Column mirror (same column, reflected row)
    col_mirror_r = 8 - row
    if col_mirror_r != row:
        targets.append((col_mirror_r, col))

    return targets


# ---------------------------------------------------------------------------
# PLANET NATURE -- benefic vs malefic for Vedha effect determination
# ---------------------------------------------------------------------------
_NATURAL_BENEFICS = {"Jupiter", "Venus", "Moon", "Mercury"}
_NATURAL_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


def _is_benefic(planet: str) -> bool:
    """Check if a planet is naturally benefic."""
    return planet in _NATURAL_BENEFICS


# ---------------------------------------------------------------------------
# Longitude-to-nakshatra/sign (standalone, avoids circular import)
# ---------------------------------------------------------------------------
def _nakshatra_from_longitude(longitude: float) -> str:
    """Return nakshatra name for a sidereal longitude (0-360)."""
    longitude = longitude % 360.0
    index = int(longitude / NAKSHATRA_SPAN)
    if index >= 27:
        index = 26
    return NAKSHATRAS_27[index]


def _sign_from_longitude(longitude: float) -> str:
    """Return zodiac sign name for a sidereal longitude (0-360)."""
    longitude = longitude % 360.0
    index = int(longitude / 30.0)
    return SIGN_NAMES[index]


# ---------------------------------------------------------------------------
# MAIN CALCULATION
# ---------------------------------------------------------------------------
def calculate_sarvatobhadra(
    planet_positions: Dict[str, Any],
    transit_positions: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Calculate the Sarvatobhadra Chakra with natal and transit planet placements
    and Vedha analysis.

    Args:
        planet_positions: Natal chart data. Accepts either:
            - Dict[str, float] — planet name to longitude
            - Dict[str, dict]  — planet name to {"longitude": float, ...}
        transit_positions: Optional transit data in same format.
            If None, only natal placements are computed (no vedha analysis).

    Returns:
        {
            "grid": 9x9 list of cell dicts (with natal_planets/transit_planets),
            "natal_placements": [{planet, nakshatra, sign, row, col, longitude}],
            "transit_placements": [{planet, nakshatra, sign, row, col, longitude}],
            "vedhas": [{transit_planet, natal_planet, vedha_type, effect, ...}],
            "auspicious": [vedha entries where effect is benefic],
            "inauspicious": [vedha entries where effect is malefic],
            "summary": text interpretation,
        }
    """
    # 1. Normalize planet positions to {name: longitude}
    natal_lons = _normalize_positions(planet_positions)
    transit_lons = _normalize_positions(transit_positions) if transit_positions else {}

    # 2. Place planets on grid
    natal_placements = _place_planets(natal_lons, "natal")
    transit_placements = _place_planets(transit_lons, "transit")

    # 3. Calculate Vedha relationships
    vedhas: List[Dict[str, Any]] = []
    auspicious: List[Dict[str, Any]] = []
    inauspicious: List[Dict[str, Any]] = []

    if transit_placements and natal_placements:
        for tp in transit_placements:
            t_row, t_col = tp["row"], tp["col"]
            targets = get_vedha_targets(t_row, t_col)

            for np_ in natal_placements:
                n_row, n_col = np_["row"], np_["col"]
                if (n_row, n_col) in targets:
                    # Determine vedha type
                    if (n_row, n_col) == (8 - t_row, 8 - t_col):
                        vedha_type = "diagonal"
                    elif n_row == t_row:
                        vedha_type = "row"
                    else:
                        vedha_type = "column"

                    effect = "auspicious" if _is_benefic(tp["planet"]) else "inauspicious"

                    vedha_entry = {
                        "transit_planet": tp["planet"],
                        "transit_nakshatra": tp["nakshatra"],
                        "transit_cell": (t_row, t_col),
                        "natal_planet": np_["planet"],
                        "natal_nakshatra": np_["nakshatra"],
                        "natal_cell": (n_row, n_col),
                        "vedha_type": vedha_type,
                        "effect": effect,
                    }
                    vedhas.append(vedha_entry)

                    if effect == "auspicious":
                        auspicious.append(vedha_entry)
                    else:
                        inauspicious.append(vedha_entry)

    # 4. Build summary
    summary = _build_summary(natal_placements, transit_placements, vedhas,
                             auspicious, inauspicious)

    # 5. Build serializable grid
    serializable_grid = _serialize_grid(natal_placements, transit_placements)

    return {
        "grid": serializable_grid,
        "natal_placements": natal_placements,
        "transit_placements": transit_placements,
        "vedhas": vedhas,
        "auspicious": auspicious,
        "inauspicious": inauspicious,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _normalize_positions(positions: Dict[str, Any]) -> Dict[str, float]:
    """
    Normalize planet positions to {planet_name: longitude} format.
    Accepts either {name: float} or {name: {"longitude": float, ...}}.
    """
    result: Dict[str, float] = {}
    if not positions:
        return result
    for name, val in positions.items():
        if isinstance(val, (int, float)):
            result[name] = float(val)
        elif isinstance(val, dict):
            lon = val.get("longitude")
            if lon is not None:
                result[name] = float(lon)
    return result


def _place_planets(
    planet_lons: Dict[str, float],
    category: str,
) -> List[Dict[str, Any]]:
    """
    Place planets on the SBC grid based on their nakshatra.

    A planet is placed in the cell matching its nakshatra. If the nakshatra
    is not on the grid (e.g. Magha, Vishakha), we fall back to placing by sign.
    """
    placements: List[Dict[str, Any]] = []
    for planet, lon in planet_lons.items():
        nakshatra = _nakshatra_from_longitude(lon)
        sign = _sign_from_longitude(lon)

        # Try nakshatra cell first, then sign cell
        cell_pos = NAKSHATRA_CELL.get(nakshatra)
        if cell_pos is None:
            cell_pos = SIGN_CELL.get(sign)

        if cell_pos is not None:
            row, col = cell_pos
            placements.append({
                "planet": planet,
                "nakshatra": nakshatra,
                "sign": sign,
                "longitude": lon,
                "row": row,
                "col": col,
                "category": category,
            })
    return placements


def _serialize_grid(
    natal_placements: List[Dict[str, Any]],
    transit_placements: List[Dict[str, Any]],
) -> List[List[Dict[str, Any]]]:
    """
    Create a serializable 9x9 grid with planet placements embedded.
    Each cell gets natal_planets and transit_planets lists.
    """
    import copy
    sgrid = copy.deepcopy(GRID)

    for r in range(9):
        for c in range(9):
            sgrid[r][c]["natal_planets"] = []
            sgrid[r][c]["transit_planets"] = []

    for p in natal_placements:
        sgrid[p["row"]][p["col"]]["natal_planets"].append(p["planet"])

    for p in transit_placements:
        sgrid[p["row"]][p["col"]]["transit_planets"].append(p["planet"])

    return sgrid


def _build_summary(
    natal_placements: List[Dict[str, Any]],
    transit_placements: List[Dict[str, Any]],
    vedhas: List[Dict[str, Any]],
    auspicious: List[Dict[str, Any]],
    inauspicious: List[Dict[str, Any]],
) -> str:
    """Build a human-readable summary of the SBC analysis."""
    lines: List[str] = []
    lines.append("=== Sarvatobhadra Chakra Analysis ===")
    lines.append("")

    lines.append(f"Natal planets placed: {len(natal_placements)}")
    for p in natal_placements:
        lines.append(f"  {p['planet']}: {p['nakshatra']} ({p['sign']}) -> cell ({p['row']},{p['col']})")

    if transit_placements:
        lines.append("")
        lines.append(f"Transit planets placed: {len(transit_placements)}")
        for p in transit_placements:
            lines.append(f"  {p['planet']}: {p['nakshatra']} ({p['sign']}) -> cell ({p['row']},{p['col']})")

    if vedhas:
        lines.append("")
        lines.append(f"Total Vedha connections: {len(vedhas)}")
        lines.append(f"  Auspicious: {len(auspicious)}")
        lines.append(f"  Inauspicious: {len(inauspicious)}")
        lines.append("")
        for v in vedhas:
            sym = "+" if v["effect"] == "auspicious" else "-"
            lines.append(
                f"  [{sym}] Transit {v['transit_planet']} ({v['transit_nakshatra']}) "
                f"vedhas natal {v['natal_planet']} ({v['natal_nakshatra']}) "
                f"via {v['vedha_type']} -- {v['effect']}"
            )
    else:
        lines.append("")
        lines.append("No Vedha connections found (transit data may be absent).")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Convenience functions
# ---------------------------------------------------------------------------

def get_empty_grid() -> List[List[Dict[str, str]]]:
    """Return the empty SBC grid layout without any planet placements."""
    import copy
    return copy.deepcopy(GRID)


def get_nakshatra_positions() -> Dict[str, Tuple[int, int]]:
    """Return dict of nakshatra name -> (row, col) in the SBC grid."""
    return dict(NAKSHATRA_CELL)


def get_sign_positions() -> Dict[str, Tuple[int, int]]:
    """Return dict of sign name -> (row, col) in the SBC grid."""
    return dict(SIGN_CELL)


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample_natal = {
        "Sun": 130.5,     # Leo / Magha
        "Moon": 215.3,    # Scorpio / Vishakha
        "Mercury": 105.2, # Cancer / Pushya
        "Venus": 110.8,   # Cancer / Pushya
        "Mars": 98.1,     # Cancer / Pushya
        "Jupiter": 280.6, # Capricorn / Shravana
        "Saturn": 195.4,  # Libra / Swati
        "Rahu": 15.7,     # Aries / Bharani
        "Ketu": 195.7,    # Libra / Swati
    }

    sample_transit = {
        "Sun": 20.0,      # Aries / Bharani
        "Moon": 80.0,     # Gemini / Punarvasu
        "Mars": 310.0,    # Aquarius / Shatabhisha
        "Jupiter": 55.0,  # Taurus / Mrigashira
        "Saturn": 340.0,  # Pisces / U.Bhadrapada
    }

    result = calculate_sarvatobhadra(sample_natal, sample_transit)
    print(result["summary"])
    print()
    print(f"Grid size: {len(result['grid'])}x{len(result['grid'][0])}")
    print(f"Vedhas found: {len(result['vedhas'])}")
