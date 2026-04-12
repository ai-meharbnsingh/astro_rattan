"""
divisional_charts.py -- Vedic Divisional Chart Calculator
==========================================================
Calculates divisional (varga) charts used in Vedic astrology.
Supports all 16 standard divisional charts: D1 through D60.

Each divisional chart maps a planet's longitude in the Rasi (D1) chart
to a sign in the divisional chart based on specific mathematical divisions.
"""
from __future__ import annotations

from typing import Any, Dict, List

# Sign names in order (0-indexed)
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# Supported divisional chart types with display names
DIVISIONAL_CHARTS: Dict[int, str] = {
    1: "Rashi (D1)",
    2: "Hora (D2)",
    3: "Drekkana (D3)",
    4: "Chaturthamsha (D4)",
    7: "Saptamsha (D7)",
    9: "Navamsha (D9)",
    10: "Dashamsha (D10)",
    12: "Dwadashamsha (D12)",
    16: "Shodashamsha (D16)",
    20: "Vimshamsha (D20)",
    24: "Chaturvimshamsha (D24)",
    27: "Bhamsha (D27)",
    30: "Trimshamsha (D30)",
    40: "Khavedamsha (D40)",
    45: "Akshavedamsha (D45)",
    60: "Shashtiamsha (D60)",
}

# ============================================================
# D60 SHASHTIAMSA SANSKRIT NAMES & NATURE
# Reference: PDF 1.1.3 (Ancient Vedic Logic)
# ============================================================
D60_NAMES = [
    {"name": "Ghora", "nature": "Malefic", "hi": "घोर", "desc": "Terrible, intense suffering"},
    {"name": "Rakshasa", "nature": "Malefic", "hi": "राक्षस", "desc": "Demonic, cruel tendencies"},
    {"name": "Deva", "nature": "Benefic", "hi": "देव", "desc": "Divine, virtuous, enlightened"},
    {"name": "Kubera", "nature": "Benefic", "hi": "कुबेर", "desc": "Wealthy, lord of riches"},
    {"name": "Yaksha", "nature": "Mixed", "hi": "यक्ष", "desc": "Protector of wealth, mystical"},
    {"name": "Kinnara", "nature": "Benefic", "hi": "किन्नर", "desc": "Artistic, musical, harmonious"},
    {"name": "Bhrashta", "nature": "Malefic", "hi": "भ्रष्ट", "desc": "Fallen, corrupt, loss of status"},
    {"name": "Kulaghna", "nature": "Malefic", "hi": "कुलघ्न", "desc": "Destroyer of lineage"},
    {"name": "Garala", "nature": "Malefic", "hi": "गरल", "desc": "Poisonous, toxic environments"},
    {"name": "Vahni", "nature": "Malefic", "hi": "वह्नि", "desc": "Fire, burning, digestive issues"},
    {"name": "Maya", "nature": "Mixed", "hi": "माया", "desc": "Illusion, deceptive success"},
    {"name": "Purishaka", "nature": "Malefic", "hi": "पुरीषक", "desc": "Impure, difficult circumstances"},
    {"name": "Apampati", "nature": "Benefic", "hi": "अपाम्पति", "desc": "Lord of waters, calm, stable"},
    {"name": "Marutvan", "nature": "Benefic", "hi": "मरुत्वान्", "desc": "Lord of winds, influential"},
    {"name": "Kaala", "nature": "Malefic", "hi": "काल", "desc": "Time, end, restrictive"},
    {"name": "Sarpa", "nature": "Malefic", "hi": "सर्प", "desc": "Serpentine, hidden enemies"},
    {"name": "Amrita", "nature": "Benefic", "hi": "अमृत", "desc": "Nectar, immortality, great health"},
    {"name": "Indu", "nature": "Benefic", "hi": "इन्दु", "desc": "Moon-like, peaceful, nourishing"},
    {"name": "Mridu", "nature": "Benefic", "hi": "मृदु", "desc": "Soft, gentle, kind"},
    {"name": "Komala", "nature": "Benefic", "hi": "कोमल", "desc": "Delicate, refined, aesthetic"},
    {"name": "Heramba", "nature": "Benefic", "hi": "हेरम्ब", "desc": "Ganesha-like, removing obstacles"},
    {"name": "Brahma", "nature": "Benefic", "hi": "ब्रह्मा", "desc": "Creative, knowledge-oriented"},
    {"name": "Vishnu", "nature": "Benefic", "hi": "विष्णु", "desc": "Protective, expansive, lucky"},
    {"name": "Maheshwara", "nature": "Benefic", "hi": "महेश्वर", "desc": "Powerful, transformative, grand"},
    {"name": "Devadeva", "nature": "Benefic", "hi": "देवदेव", "desc": "Lord of lords, supreme status"},
    {"name": "Ardra", "nature": "Mixed", "hi": "आर्द्रा", "desc": "Moist, emotional, sensitive"},
    {"name": "Kalinasa", "nature": "Benefic", "hi": "कलिनाश", "desc": "Destroyer of strife"},
    {"name": "Kshiteeshwara", "nature": "Benefic", "hi": "क्षितीश्वर", "desc": "Ruler of earth, landed property"},
    {"name": "Kamalakara", "nature": "Benefic", "hi": "कमलाकर", "desc": "Lotus-like, purity, beauty"},
    {"name": "Gulika", "nature": "Malefic", "hi": "गुलिका", "desc": "Saturn's son, karmic delays"},
    {"name": "Mrityu", "nature": "Malefic", "hi": "मृत्यु", "desc": "Death-like, end of cycles"},
    {"name": "Kaala", "nature": "Malefic", "hi": "काल", "desc": "Time, finite, ending"},
    {"name": "Davagni", "nature": "Malefic", "hi": "दवाग्नि", "desc": "Forest fire, sudden destruction"},
    {"name": "Ghora", "nature": "Malefic", "hi": "घोर", "desc": "Intense, terrible"},
    {"name": "Adhama", "nature": "Malefic", "hi": "अधम", "desc": "Lowly, degraded results"},
    {"name": "Kantaka", "nature": "Malefic", "hi": "कंटक", "desc": "Thorn, painful obstacles"},
    {"name": "Sudha", "nature": "Benefic", "hi": "सुधा", "desc": "Nectar, pure, satisfying"},
    {"name": "Amrita", "nature": "Benefic", "hi": "अमृत", "desc": "Immortality, nectar"},
    {"name": "Poornachandra", "nature": "Benefic", "hi": "पूर्णचन्द्र", "desc": "Full moon, abundance, fame"},
    {"name": "Vishadagdha", "nature": "Malefic", "hi": "विषदिग्ध", "desc": "Consumed by poison"},
    {"name": "Kulanasa", "nature": "Malefic", "hi": "कुलनाश", "desc": "Linage destroyer"},
    {"name": "Vamshakshaya", "nature": "Malefic", "hi": "वंशक्षय", "desc": "Family decay"},
    {"name": "Utpata", "nature": "Malefic", "hi": "उत्पात", "desc": "Calamity, sudden upheaval"},
    {"name": "Kaala", "nature": "Malefic", "hi": "काल", "desc": "Time constraint"},
    {"name": "Saumya", "nature": "Benefic", "hi": "सौम्य", "desc": "Gentle, benefic results"},
    {"name": "Komala", "nature": "Benefic", "hi": "कोमल", "desc": "Soft, pleasant"},
    {"name": "Sheetala", "nature": "Benefic", "hi": "शीतल", "desc": "Cool, soothing"},
    {"name": "Karaladamshstra", "nature": "Malefic", "hi": "करालदंष्ट्र", "desc": "Fierce teeth, aggressive"},
    {"name": "Chandramukhi", "nature": "Benefic", "hi": "चन्द्रमुखी", "desc": "Moon-faced, attractive"},
    {"name": "Praveena", "nature": "Benefic", "hi": "प्रवीण", "desc": "Skilled, expert"},
    {"name": "Kalapavaka", "nature": "Malefic", "hi": "कालपावक", "desc": "Fire of time"},
    {"name": "Dandayudha", "nature": "Malefic", "hi": "दंडायुध", "desc": "Staff-bearing, punishment"},
    {"name": "Nirmala", "nature": "Benefic", "hi": "निर्मल", "desc": "Pure, stainless"},
    {"name": "Saumya", "nature": "Benefic", "hi": "सौम्य", "desc": "Gentle"},
    {"name": "Kshura", "nature": "Malefic", "hi": "क्षुर", "desc": "Razor-sharp, cutting"},
    {"name": "Atisheetala", "nature": "Benefic", "hi": "अतिशीतल", "desc": "Very cool, highly soothing"},
    {"name": "Amrita", "nature": "Benefic", "hi": "अमृत", "desc": "Nectar"},
    {"name": "Payodhi", "nature": "Benefic", "hi": "पयोधि", "desc": "Ocean, depth, vast wealth"},
    {"name": "Bhramana", "nature": "Mixed", "hi": "भ्रमण", "desc": "Wandering, travel"},
    {"name": "Chandrarekha", "nature": "Benefic", "hi": "चन्द्ररेखा", "desc": "Moon-streak, fame, soft aura"},
]

def calculate_d60_analysis(planet_longitudes: Dict[str, float]) -> Dict[str, Any]:
    """
    Identifies the D60 Shashtiamsa division for each planet and its meaning.
    Reference: PDF 1.1.3
    """
    analysis = {}
    for planet, lon in planet_longitudes.items():
        # D60 = 30 / 60 = 0.5 degrees per division
        # 1. Degrees within sign
        deg_in_sign = lon % 30.0
        # 2. Shashtiamsa unit (0-59)
        unit = int(deg_in_sign * 2) # 0.5 deg = 1 unit, so 1 deg = 2 units
        
        # 3. Determine if sign is ODD or EVEN
        sign_idx = int(lon / 30.0) % 12
        is_odd = (sign_idx % 2 == 0) # 0=Aries (odd), 1=Taurus (even)
        
        # 4. Map to D60 name
        # If ODD: 1 to 60 directly
        # If EVEN: Reverse (60 to 1)
        if is_odd:
            name_idx = unit
        else:
            name_idx = 59 - unit
            
        if 0 <= name_idx < 60:
            info = D60_NAMES[name_idx]
            analysis[planet] = {
                "unit": unit + 1,
                "name": info["name"],
                "name_hi": info["hi"],
                "nature": info["nature"],
                "description": info["desc"]
            }
            
    return analysis


def _sign_index(sign_name: str) -> int:
    """Return the 0-based index of a zodiac sign."""
    return _SIGN_NAMES.index(sign_name)


# ============================================================
# D2 -- Hora
# ============================================================

def _calculate_d2(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Hora (D2): divide each sign into 2 halves (15 deg each).
    Odd signs: first half -> Leo (Sun), second half -> Cancer (Moon).
    Even signs: first half -> Cancer (Moon), second half -> Leo (Sun).
    """
    result: Dict[str, Dict[str, Any]] = {}
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = 0 if degree_in_sign < 15.0 else 1
        sign_number = rasi_index + 1  # 1-indexed
        if sign_number % 2 == 1:  # Odd sign
            div_sign_index = 4 if part == 0 else 3  # Leo or Cancer
        else:  # Even sign
            div_sign_index = 3 if part == 0 else 4  # Cancer or Leo
        degree_within = (degree_in_sign % 15.0) * 2.0  # Scale to 0-30
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D3 -- Drekkana
# ============================================================

def _calculate_d3(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Drekkana (D3): divide each sign into 3 parts (10 deg each).
    Part 0 -> same sign, Part 1 -> 5th from sign, Part 2 -> 9th from sign.
    """
    result: Dict[str, Dict[str, Any]] = {}
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / 10.0), 2)
        offsets = [0, 4, 8]  # same, 5th, 9th (0-indexed offsets)
        div_sign_index = (rasi_index + offsets[part]) % 12
        degree_within = (degree_in_sign % 10.0) * 3.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D4 -- Chaturthamsha
# ============================================================

def _calculate_d4(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Chaturthamsha (D4): divide each sign into 4 parts (7.5 deg each).
    Starts from same sign, then advances by 3 signs (quadrants).
    """
    result: Dict[str, Dict[str, Any]] = {}
    part_size = 7.5
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / part_size), 3)
        div_sign_index = (rasi_index + part * 3) % 12
        degree_within = (degree_in_sign % part_size) * 4.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D7 -- Saptamsha
# ============================================================

def _calculate_d7(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Saptamsha (D7): divide each sign into 7 parts (4deg 17min 8.57sec each).
    Odd signs: start from same sign. Even signs: start from 7th from sign.
    """
    result: Dict[str, Dict[str, Any]] = {}
    part_size = 30.0 / 7.0
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / part_size), 6)
        sign_number = rasi_index + 1
        if sign_number % 2 == 1:
            start = rasi_index
        else:
            start = (rasi_index + 6) % 12
        div_sign_index = (start + part) % 12
        degree_within = (degree_in_sign % part_size) * 7.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D9 -- Navamsa
# ============================================================

def _calculate_d9(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Navamsa (D9): divide each sign into 9 parts (3deg 20min each).
    Fire signs start from Aries, Earth from Capricorn,
    Air from Libra, Water from Cancer.
    """
    result: Dict[str, Dict[str, Any]] = {}
    part_size = 30.0 / 9.0
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / part_size), 8)
        element = rasi_index % 4  # 0=Fire, 1=Earth, 2=Air, 3=Water
        start_signs = {0: 0, 1: 9, 2: 6, 3: 3}
        start = start_signs[element]
        div_sign_index = (start + part) % 12
        degree_within = (degree_in_sign % part_size) * 9.0
        degree_within = degree_within % 30.0  # clamp float boundary: 30.0 → 0.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D10 -- Dasamsa
# ============================================================

def _calculate_d10(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Dasamsa (D10): divide each sign into 10 parts (3 deg each).
    Odd signs: start from same sign. Even signs: start from 9th sign.
    """
    result: Dict[str, Dict[str, Any]] = {}
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / 3.0), 9)
        sign_number = rasi_index + 1
        if sign_number % 2 == 1:
            start = rasi_index
        else:
            start = (rasi_index + 8) % 12  # 9th sign = +8 in 0-indexed
        div_sign_index = (start + part) % 12
        degree_within = (degree_in_sign % 3.0) * 10.0
        degree_within = degree_within % 30.0  # clamp float boundary: 30.0 → 0.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D12 -- Dwadashamsha
# ============================================================

def _calculate_d12(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Dwadashamsha (D12): divide each sign into 12 parts (2.5 deg each).
    Starts from same sign, advances through all 12 signs.
    """
    result: Dict[str, Dict[str, Any]] = {}
    part_size = 2.5
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part = min(int(degree_in_sign / part_size), 11)
        div_sign_index = (rasi_index + part) % 12
        degree_within = (degree_in_sign % part_size) * 12.0
        degree_within = degree_within % 30.0  # clamp float boundary: 30.0 → 0.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# D30 -- Trimshamsha
# ============================================================

def _calculate_d30(planet_longitudes: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Trimshamsha (D30): 1 deg per division.
    Odd signs: 0-5 Mars, 5-10 Saturn, 10-18 Jupiter, 18-25 Mercury, 25-30 Venus.
    Even signs: reversed order.
    """
    # Odd sign boundaries and lords
    odd_ranges = [(5, 4), (10, 6), (18, 5), (25, 2), (30, 3)]   # (end, sign_index for lord)
    even_ranges = [(5, 3), (12, 2), (20, 5), (25, 6), (30, 4)]  # BPHS even: 5,7,8,5,5 degrees
    # Mars=Aries(0)/Scorpio(7), Saturn=Cap(9)/Aqu(10), Jupiter=Sag(8)/Pisces(11),
    # Mercury=Gem(2)/Virgo(5), Venus=Tau(1)/Libra(6)
    odd_signs = [0, 10, 8, 2, 1]   # Mars=Aries, Saturn=Aquarius, Jupiter=Sag, Mercury=Gemini, Venus=Taurus
    even_signs = [6, 5, 11, 9, 7]  # Venus=Libra, Mercury=Virgo, Jupiter=Pisces, Saturn=Cap, Mars=Scorpio

    result: Dict[str, Dict[str, Any]] = {}
    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        sign_number = rasi_index + 1

        if sign_number % 2 == 1:
            signs_list = odd_signs
            ranges = odd_ranges
        else:
            signs_list = even_signs
            ranges = even_ranges

        div_sign_index = signs_list[0]
        prev_end = 0.0
        for i, (end, _) in enumerate(ranges):
            if degree_in_sign < end:
                div_sign_index = signs_list[i]
                break
            prev_end = end

        degree_within = degree_in_sign  # 1:1 mapping for D30
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# GENERIC -- For D16, D20, D24, D27, D40, D45, D60
# ============================================================

def _calculate_generic(
    planet_longitudes: Dict[str, float], division: int,
) -> Dict[str, Dict[str, Any]]:
    """
    Generic divisional chart using cyclic formula.
    part_index = floor(degree_in_sign / (30/division))
    result_sign = (rasi_index * division + part_index) mod 12
    """
    result: Dict[str, Dict[str, Any]] = {}
    part_size = 30.0 / division

    for planet, lon in planet_longitudes.items():
        lon = lon % 360.0
        rasi_index = int(lon / 30.0)
        degree_in_sign = lon - rasi_index * 30.0
        part_index = min(int(degree_in_sign / part_size), division - 1)
        div_sign_index = (rasi_index * division + part_index) % 12
        degree_within = (degree_in_sign % part_size) * division
        degree_within = degree_within % 30.0  # clamp float boundary: 30.0 → 0.0
        result[planet] = {
            "sign": _SIGN_NAMES[div_sign_index],
            "sign_index": div_sign_index,
            "degree": round(degree_within, 4),
        }
    return result


# ============================================================
# PUBLIC API
# ============================================================

def calculate_divisional_chart(
    planet_longitudes: Dict[str, float], division: int,
) -> Dict[str, str]:
    """
    Calculate a divisional chart. Returns simple {planet: sign} mapping.
    Backward-compatible API.
    """
    detailed = calculate_divisional_chart_detailed(planet_longitudes, division)
    return {planet: info["sign"] for planet, info in detailed.items()}


def calculate_divisional_chart_detailed(
    planet_longitudes: Dict[str, float], division: int,
) -> Dict[str, Dict[str, Any]]:
    """
    Calculate a divisional chart with detailed info per planet.

    Returns:
        {planet_name: {sign, sign_index, degree}}
    """
    if division < 1:
        raise ValueError("Division must be >= 1")
    if division == 1:
        # D1 = Rashi chart, just return as-is
        result: Dict[str, Dict[str, Any]] = {}
        for planet, lon in planet_longitudes.items():
            lon = lon % 360.0
            rasi_index = int(lon / 30.0)
            result[planet] = {
                "sign": _SIGN_NAMES[rasi_index],
                "sign_index": rasi_index,
                "degree": round(lon % 30.0, 4),
            }
        return result

    dispatch = {
        2: _calculate_d2,
        3: _calculate_d3,
        4: _calculate_d4,
        7: _calculate_d7,
        9: _calculate_d9,
        10: _calculate_d10,
        12: _calculate_d12,
        30: _calculate_d30,
    }

    if division in dispatch:
        return dispatch[division](planet_longitudes)
    return _calculate_generic(planet_longitudes, division)


def calculate_divisional_ascendant(
    ascendant_longitude: float, division: int,
) -> Dict[str, Any]:
    """
    Calculate the divisional chart ascendant by passing the natal ascendant
    longitude through the same divisional formula used for planets.

    Returns:
        {sign, sign_index, degree}
    """
    detailed = calculate_divisional_chart_detailed(
        {"_Ascendant": ascendant_longitude}, division,
    )
    return detailed["_Ascendant"]


def calculate_divisional_houses(
    ascendant_longitude: float, division: int,
) -> List[Dict[str, Any]]:
    """
    Build the 12-house mapping for a divisional chart, relative to the
    divisional ascendant.

    The divisional ascendant's sign becomes House 1, the next sign
    becomes House 2, and so on through all 12 houses.

    Returns:
        [{number: 1, sign: "Libra"}, {number: 2, sign: "Scorpio"}, ...]
    """
    asc_info = calculate_divisional_ascendant(ascendant_longitude, division)
    asc_sign_index = asc_info["sign_index"]
    return [
        {
            "number": i + 1,
            "sign": _SIGN_NAMES[(asc_sign_index + i) % 12],
        }
        for i in range(12)
    ]


# Backward-compatible named functions
def calculate_d9_navamsa(planet_longitudes: Dict[str, float]) -> Dict[str, str]:
    """Calculate Navamsa (D9) sign for each planet. Returns {planet: sign}."""
    detailed = _calculate_d9(planet_longitudes)
    return {planet: info["sign"] for planet, info in detailed.items()}


def calculate_d10_dasamsa(planet_longitudes: Dict[str, float]) -> Dict[str, str]:
    """Calculate Dasamsa (D10) sign for each planet. Returns {planet: sign}."""
    detailed = _calculate_d10(planet_longitudes)
    return {planet: info["sign"] for planet, info in detailed.items()}
