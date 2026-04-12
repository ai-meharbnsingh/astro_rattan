"""
ashtakvarga_engine.py -- Ashtakvarga Calculation Engine
========================================================
Calculates the Ashtakvarga point system used in Vedic astrology for
transit predictions. Each planet gets 0 or 1 point (bindu) from each
of the 7 contributing planets + Ascendant for each of the 12 signs.

The Sarvashtakvarga is the sum of all individual planet ashtakvargas.
"""
from __future__ import annotations

from typing import Any, Dict, List, Set

# Sign names
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# ============================================================
# BENEFIC POINTS -- Houses from each contributing planet that
# give a benefic point (bindu). Houses are 1-indexed relative
# to the contributing planet's position.
# Format: BENEFIC_POINTS[receiving_planet][contributing_planet] = set of house numbers
# ============================================================

BENEFIC_POINTS: Dict[str, Dict[str, Set[int]]] = {
    "Sun": {
        "Sun":       {1, 2, 4, 7, 8, 9, 10, 11},
        "Moon":      {3, 6, 10, 11},
        "Mars":      {1, 2, 4, 7, 8, 9, 10, 11},
        "Mercury":   {3, 5, 6, 9, 10, 11, 12},
        "Jupiter":   {5, 6, 9, 11},
        "Venus":     {6, 7, 12},
        "Saturn":    {1, 2, 4, 7, 8, 9, 10, 11},
        "Ascendant": {3, 4, 6, 10, 11, 12},
    },
    "Moon": {
        "Sun":       {3, 6, 7, 8, 10, 11},
        "Moon":      {1, 3, 6, 7, 10, 11},
        "Mars":      {2, 3, 5, 6, 9, 10, 11},
        "Mercury":   {1, 3, 4, 5, 7, 8, 10, 11},
        "Jupiter":   {1, 4, 7, 8, 10, 11, 12},
        "Venus":     {3, 4, 5, 7, 9, 10, 11},
        "Saturn":    {3, 5, 6, 11},
        "Ascendant": {3, 6, 10, 11},
    },
    "Mars": {
        "Sun":       {3, 5, 6, 10, 11},
        "Moon":      {3, 6, 11},
        "Mars":      {1, 2, 4, 7, 8, 10, 11},
        "Mercury":   {3, 5, 6, 11},
        "Jupiter":   {6, 10, 11, 12},
        "Venus":     {6, 8, 11, 12},
        "Saturn":    {1, 4, 7, 8, 9, 10, 11},
        "Ascendant": {1, 3, 6, 10, 11},
    },
    "Mercury": {
        "Sun":       {5, 6, 9, 11, 12},
        "Moon":      {2, 4, 6, 8, 10, 11},
        "Mars":      {1, 2, 4, 7, 8, 9, 10, 11},
        "Mercury":   {1, 3, 5, 6, 9, 10, 11, 12},
        "Jupiter":   {6, 8, 11, 12},
        "Venus":     {1, 2, 3, 4, 5, 8, 9, 11},
        "Saturn":    {1, 2, 4, 7, 8, 9, 10, 11},
        "Ascendant": {1, 2, 4, 6, 8, 10, 11},
    },
    "Jupiter": {
        "Sun":       {1, 2, 3, 4, 7, 8, 9, 10, 11},
        "Moon":      {2, 5, 7, 9, 11},
        "Mars":      {1, 2, 4, 7, 8, 10, 11},
        "Mercury":   {1, 2, 4, 5, 6, 9, 10, 11},
        "Jupiter":   {1, 2, 3, 4, 7, 8, 10, 11},
        "Venus":     {2, 5, 6, 9, 10, 11},
        "Saturn":    {3, 5, 6, 12},
        "Ascendant": {1, 2, 4, 5, 6, 7, 9, 10, 11},
    },
    "Venus": {
        "Sun":       {8, 11, 12},
        "Moon":      {1, 2, 3, 4, 5, 8, 9, 11, 12},
        "Mars":      {3, 5, 6, 9, 11, 12},
        "Mercury":   {3, 5, 6, 9, 11},
        "Jupiter":   {5, 8, 9, 10, 11},
        "Venus":     {1, 2, 3, 4, 5, 8, 9, 10, 11},
        "Saturn":    {3, 4, 5, 8, 9, 10, 11},
        "Ascendant": {1, 2, 3, 4, 5, 8, 9, 11},
    },
    "Saturn": {
        "Sun":       {1, 2, 4, 7, 8, 10, 11},
        "Moon":      {3, 6, 11},
        "Mars":      {3, 5, 6, 10, 11, 12},
        "Mercury":   {6, 8, 9, 10, 11, 12},
        "Jupiter":   {5, 6, 11, 12},
        "Venus":     {6, 11, 12},
        "Saturn":    {3, 5, 6, 11},
        "Ascendant": {1, 3, 4, 6, 10, 11},
    },
    # Lagna (Ascendant) Ashtakvarga — benefic houses from each contributor
    "Lagna": {
        "Sun":       {3, 4, 6, 10, 11, 12},
        "Moon":      {3, 6, 10, 11},
        "Mars":      {1, 3, 6, 10, 11},
        "Mercury":   {1, 2, 4, 6, 8, 10, 11},
        "Jupiter":   {1, 2, 4, 5, 6, 7, 9, 10, 11},
        "Venus":     {1, 2, 3, 4, 5, 8, 9, 11},
        "Saturn":    {1, 3, 4, 6, 10, 11},
        "Ascendant": {3, 4, 6, 10, 11, 12},
    },
}


def _sign_name_to_index(sign_name: str) -> int:
    """Convert sign name to 0-based index."""
    return _SIGN_NAMES.index(sign_name)


def calculate_ashtakvarga(planet_signs: Dict[str, str]) -> Dict[str, Any]:
    """
    Calculate the Ashtakvarga system for a given chart.
    Includes Trikona Shodhana, Ekadhipatya Shodhana and Shodhya Pinda.
    """
    # Validate required planets
    required = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    available = set(planet_signs.keys())
    missing = required - available
    if missing:
        raise ValueError(f"Missing planets for Ashtakvarga: {missing}")

    # Build position map: planet/ascendant -> 0-based sign index
    positions: Dict[str, int] = {}
    for name, sign in planet_signs.items():
        if name in required or name == "Ascendant":
            positions[name] = _sign_name_to_index(sign)

    if "Ascendant" not in positions:
        positions["Ascendant"] = 0

    contributors = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Ascendant"]
    _CONTRIB_DISPLAY = {c: ("Lagna" if c == "Ascendant" else c) for c in contributors}

    planet_bindus: Dict[str, Dict[str, int]] = {}
    planet_details: Dict[str, Dict[str, Any]] = {}
    sarvashtakvarga: Dict[str, int] = {sign: 0 for sign in _SIGN_NAMES}

    # 1. Calculate base Bindus
    for recv_planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]:
        recv_table = BENEFIC_POINTS[recv_planet]
        bindus: Dict[str, int] = {sign: 0 for sign in _SIGN_NAMES}
        contrib_matrix: Dict[str, Dict[str, int]] = {}

        for contrib in contributors:
            display_name = _CONTRIB_DISPLAY[contrib]
            contrib_row: Dict[str, int] = {sign: 0 for sign in _SIGN_NAMES}

            if contrib in recv_table and contrib in positions:
                benefic_houses = recv_table[contrib]
                contrib_sign_index = positions[contrib]

                for house_num in benefic_houses:
                    target_sign_index = (contrib_sign_index + house_num - 1) % 12
                    target_sign = _SIGN_NAMES[target_sign_index]
                    contrib_row[target_sign] = 1
                    bindus[target_sign] += 1

            contrib_matrix[display_name] = contrib_row

        planet_bindus[recv_planet] = bindus
        planet_details[recv_planet] = {
            "contributors": contrib_matrix,
            "totals": bindus,
        }

        if recv_planet != "Lagna":
            for sign in _SIGN_NAMES:
                sarvashtakvarga[sign] += bindus[sign]

    # 2. Purification (Shodhana) for each of the 7 planets
    purified_data: Dict[str, Any] = {}
    for planet in required:
        raw_bindus = list(planet_bindus[planet].values()) # 12 values
        
        # A. Trikona Shodhana (Trine Reduction)
        trikona = _apply_trikona_shodhana(raw_bindus)
        
        # B. Ekadhipatya Shodhana (Lordship Reduction)
        # Needs planet positions to check for occupancy
        ekadhipatya = _apply_ekadhipatya_shodhana(trikona, positions)
        
        # C. Shodhya Pinda (Purified Index)
        shodhya_pinda = _calculate_shodhya_pinda(planet, ekadhipatya, positions)
        
        purified_data[planet] = {
            "trikona": {sign: val for sign, val in zip(_SIGN_NAMES, trikona)},
            "ekadhipatya": {sign: val for sign, val in zip(_SIGN_NAMES, ekadhipatya)},
            "shodhya_pinda": shodhya_pinda
        }

    return {
        "planet_bindus": planet_bindus,
        "sarvashtakvarga": sarvashtakvarga,
        "planet_details": planet_details,
        "purified": purified_data
    }

def _apply_trikona_shodhana(bindus: List[int]) -> List[int]:
    """
    Reduces bindus in trine signs.
    Trines: (0,4,8), (1,5,9), (2,6,10), (3,7,11)
    """
    res = list(bindus)
    trines = [(0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)]
    for t in trines:
        v1, v2, v3 = res[t[0]], res[t[1]], res[t[2]]
        if v1 == 0 or v2 == 0 or v3 == 0:
            continue
        m = min(v1, v2, v3)
        res[t[0]] -= m
        res[t[1]] -= m
        res[t[2]] -= m
    return res

def _apply_ekadhipatya_shodhana(bindus: List[int], positions: Dict[str, int]) -> List[int]:
    """
    Lordship reduction for pairs of signs owned by the same planet.
    """
    res = list(bindus)
    # Pairs of sign indices: Mars(0,7), Mercury(2,5), Jupiter(8,11), Venus(1,6), Saturn(9,10)
    pairs = [(0, 7), (2, 5), (8, 11), (1, 6), (9, 10)]
    
    # Check occupancy
    occupied = set(positions.values())
    
    for s1, s2 in pairs:
        v1, v2 = res[s1], res[s2]
        occ1, occ2 = s1 in occupied, s2 in occupied
        
        if v1 > 0 and v2 > 0:
            if not occ1 and not occ2:
                # Both unoccupied: subtract smaller from both
                m = min(v1, v2)
                res[s1] -= m
                res[s2] -= m
            elif occ1 and occ2:
                # Both occupied: No reduction
                pass
            elif occ1 and not occ2:
                # Sign 1 occupied, Sign 2 unoccupied
                if v2 > v1: res[s2] = v1
                else: res[s2] = 0
            elif not occ1 and occ2:
                # Sign 2 occupied, Sign 1 unoccupied
                if v1 > v2: res[s1] = v2
                else: res[s1] = 0
        elif (v1 > 0 and v2 == 0) or (v1 == 0 and v2 > 0):
            # One is zero
            idx = s1 if v1 > 0 else s2
            if idx not in occupied:
                # Unoccupied sign with bindus: potentially reduce based on other sign's trines?
                # Simplified scriptural rule: if one is 0 and other is unoccupied, reduce to 0
                res[idx] = 0
                
    return res

def _calculate_shodhya_pinda(planet: str, purified: List[int], positions: Dict[str, int]) -> int:
    """
    Calculate Shodhya Pinda (Purified Index).
    """
    sign_multipliers = [7, 10, 8, 4, 10, 5, 7, 8, 9, 5, 11, 12]
    planet_multipliers = {
        "Sun": 5, "Moon": 5, "Mars": 8, "Mercury": 5, 
        "Jupiter": 10, "Venus": 7, "Saturn": 5
    }
    
    # 1. Rashi Pinda
    rashi_pinda = sum(p * m for p, m in zip(purified, sign_multipliers))
    
    # 2. Graha Pinda
    # Sum of (Purified points in sign where planet X is) * (Multiplier of planet X)
    graha_pinda = 0
    for p_name, sign_idx in positions.items():
        if p_name in planet_multipliers:
            graha_pinda += purified[sign_idx] * planet_multipliers[p_name]
            
    return rashi_pinda + graha_pinda
