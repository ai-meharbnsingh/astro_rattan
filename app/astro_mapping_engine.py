"""
astro_mapping_engine.py -- Astro-Cartography / Locational Astrology
===================================================================
For a given birth chart, calculates how planetary influences change
across different geographic locations.

Core concept:
  For any birth moment, each planet occupies a specific sidereal longitude.
  At different locations on Earth the Local Sidereal Time (and therefore
  the Ascendant) differs — so those same planets land in different houses.
  A planet in the 10th house (career) in Delhi may fall in the 4th house
  (home/comfort) in New York.

Standalone — does NOT import Swiss Ephemeris.

Provides:
  - calculate_astro_map(birth_date, birth_time, birth_tz_offset,
                        planet_longitudes, cities) -> full analysis
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple


# ── Sign helpers ─────────────────────────────────────────────

_SIGN_NAMES: List[str] = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def _sign_from_longitude(longitude: float) -> str:
    """Return zodiac sign for a sidereal longitude (0-360)."""
    return _SIGN_NAMES[int(longitude % 360.0 / 30.0)]


def _degree_in_sign(longitude: float) -> float:
    """Return the degree within its sign (0-30)."""
    return round(longitude % 30.0, 2)


# ── Pre-defined cities with coordinates ──────────────────────

MAJOR_CITIES: Dict[str, Tuple[float, float]] = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "London": (51.5074, -0.1278),
    "New York": (40.7128, -74.0060),
    "Los Angeles": (34.0522, -118.2437),
    "San Francisco": (37.7749, -122.4194),
    "Toronto": (43.6532, -79.3832),
    "Dubai": (25.2048, 55.2708),
    "Singapore": (1.3521, 103.8198),
    "Sydney": (-33.8688, 151.2093),
    "Berlin": (52.5200, 13.4050),
    "Paris": (48.8566, 2.3522),
    "Tokyo": (35.6762, 139.6503),
}

# ── Planet significance by house placement ───────────────────

PLANET_HOUSE_SIGNIFICANCE: Dict[int, str] = {
    1: "personality_boost",
    2: "wealth",
    4: "home_comfort",
    5: "creativity_children",
    7: "relationships",
    9: "fortune_travel",
    10: "career_fame",
    11: "gains_social",
}

# Angular / trine / upachaya houses
_ANGULAR_HOUSES = {1, 4, 7, 10}
_TRINE_HOUSES = {1, 5, 9}
_UPACHAYA_HOUSES = {3, 6, 10, 11}
_DUSTHANA_HOUSES = {6, 8, 12}

# Planet categories
_BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
_MALEFICS = {"Saturn", "Mars", "Rahu", "Ketu"}
_ALL_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

# Lahiri ayanamsa approximation (valid ~2000-2030, error < 0.3 deg)
_LAHIRI_AYANAMSA_J2000 = 23.856
_AYANAMSA_RATE_PER_YEAR = 0.01396  # precession rate deg/year


# ── Ascendant calculation ────────────────────────────────────

def _julian_day(year: int, month: int, day: int, ut_hours: float) -> float:
    """
    Compute Julian Day Number for a date + UT fractional hours.
    Meeus, Astronomical Algorithms (Ch. 7).
    """
    if month <= 2:
        year -= 1
        month += 12
    A = int(year / 100)
    B = 2 - A + int(A / 4)
    return (
        int(365.25 * (year + 4716))
        + int(30.6001 * (month + 1))
        + day
        + ut_hours / 24.0
        + B
        - 1524.5
    )


def _gmst_hours(jd: float) -> float:
    """
    Greenwich Mean Sidereal Time in hours for a given Julian Day.
    IAU 1982 formula (accurate to ~0.1 s for modern dates).
    """
    T = (jd - 2451545.0) / 36525.0
    # GMST at 0h UT in seconds of time
    gmst_sec = (
        24110.54841
        + 8640184.812866 * T
        + 0.093104 * T * T
        - 6.2e-6 * T * T * T
    )
    # Convert to hours
    gmst_hours = (gmst_sec / 3600.0) % 24.0
    return gmst_hours


def _lst_hours(gmst_h: float, longitude: float) -> float:
    """Local Sidereal Time in hours from GMST and geographic longitude."""
    lst = (gmst_h + longitude / 15.0) % 24.0
    if lst < 0:
        lst += 24.0
    return lst


def _obliquity_deg(jd: float) -> float:
    """Mean obliquity of ecliptic in degrees (Laskar, valid +-10 000 yr)."""
    T = (jd - 2451545.0) / 36525.0
    return 23.439291 - 0.0130042 * T - 1.64e-7 * T * T + 5.04e-7 * T * T * T


def _lahiri_ayanamsa(year: float) -> float:
    """Approximate Lahiri ayanamsa for a given decimal year."""
    return _LAHIRI_AYANAMSA_J2000 + _AYANAMSA_RATE_PER_YEAR * (year - 2000.0)


def calculate_ascendant_for_location(
    birth_date: str,
    birth_time: str,
    latitude: float,
    longitude: float,
    tz_offset: float,
) -> float:
    """
    Calculate the sidereal ascendant degree for a given location at birth time.

    Uses the classical formula:
      tan(Asc) = cos(RAMC) / -(sin(e)*tan(lat) + cos(e)*sin(RAMC))
    where RAMC = LST in degrees, e = obliquity.

    Returns ascendant longitude in degrees (0-360), Lahiri sidereal.
    """
    # Parse date and time
    try:
        dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # Try without seconds
        dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")

    # Convert local time to UT using proper datetime arithmetic
    ut_hours_raw = dt.hour + dt.minute / 60.0 + dt.second / 3600.0 - tz_offset
    # Use timedelta to handle day rollover correctly (avoids month-boundary bugs)
    ut_dt = datetime(dt.year, dt.month, dt.day) + timedelta(hours=ut_hours_raw)
    ut_hours = ut_dt.hour + ut_dt.minute / 60.0 + ut_dt.second / 3600.0

    jd = _julian_day(ut_dt.year, ut_dt.month, ut_dt.day, ut_hours)

    # Sidereal time
    gmst = _gmst_hours(jd)
    lst = _lst_hours(gmst, longitude)

    # RAMC (Right Ascension of the Midheaven) in degrees
    ramc_deg = lst * 15.0
    ramc_rad = math.radians(ramc_deg)

    # Obliquity
    eps_deg = _obliquity_deg(jd)
    eps_rad = math.radians(eps_deg)

    lat_rad = math.radians(latitude)

    # Classical ascendant formula
    # Asc = atan2(cos(RAMC), -(sin(e)*tan(lat) + cos(e)*sin(RAMC)))
    numerator = math.cos(ramc_rad)
    denominator = -(math.sin(eps_rad) * math.tan(lat_rad) + math.cos(eps_rad) * math.sin(ramc_rad))

    # atan2 gives us the correct quadrant
    asc_rad = math.atan2(numerator, denominator)
    asc_deg = math.degrees(asc_rad) % 360.0

    # Convert tropical to sidereal (Lahiri)
    decimal_year = ut_dt.year + (ut_dt.month - 1) / 12.0 + ut_dt.day / 365.25
    ayanamsa = _lahiri_ayanamsa(decimal_year)
    asc_sidereal = (asc_deg - ayanamsa) % 360.0

    return round(asc_sidereal, 4)


# ── House calculation (whole-sign) ───────────────────────────

def calculate_houses_for_location(ascendant_degree: float) -> List[float]:
    """
    Calculate whole-sign house cusps from the ascendant.
    In whole-sign, each house = the sign the ascendant falls in (house 1),
    next sign (house 2), etc.  Cusp = start of that sign.

    Returns list of 12 house cusp degrees.
    """
    first_sign_index = int(ascendant_degree / 30.0) % 12
    return [((first_sign_index + i) % 12) * 30.0 for i in range(12)]


def get_planet_house(planet_longitude: float, house_cusps: List[float]) -> int:
    """
    Determine which house (1-12) a planet falls in given whole-sign house cusps.
    """
    planet_sign_index = int((planet_longitude % 360.0) / 30.0)
    first_house_sign = int(house_cusps[0] / 30.0) % 12
    house_number = ((planet_sign_index - first_house_sign) % 12) + 1
    return house_number


# ── Scoring helpers ──────────────────────────────────────────

def _score_planet_in_house(planet: str, house: int) -> Tuple[float, List[str], List[str]]:
    """
    Score a single planet's placement in a house.
    Returns (score_delta, strengths_list, cautions_list).
    """
    strengths: List[str] = []
    cautions: List[str] = []
    score = 0.0

    is_benefic = planet in _BENEFICS
    is_malefic = planet in _MALEFICS
    is_angular = house in _ANGULAR_HOUSES
    is_trine = house in _TRINE_HOUSES
    is_dusthana = house in _DUSTHANA_HOUSES

    # ── Benefics in good houses ──
    if is_benefic and is_angular:
        score += 1.5
        label = PLANET_HOUSE_SIGNIFICANCE.get(house, "strong placement")
        strengths.append(f"{label.replace('_', ' ').title()} ({planet} in {_ordinal(house)} house)")

    if is_benefic and is_trine and not is_angular:
        score += 1.0
        label = PLANET_HOUSE_SIGNIFICANCE.get(house, "fortunate placement")
        strengths.append(f"{label.replace('_', ' ').title()} ({planet} in {_ordinal(house)} house)")

    # ── Malefics in angular houses — mixed / cautionary ──
    if is_malefic and is_angular:
        score -= 0.5
        cautions.append(f"Intensity from {planet} in {_ordinal(house)} house — channel carefully")

    # ── Malefics in upachaya — growth ──
    if is_malefic and house in _UPACHAYA_HOUSES and not is_angular:
        score += 0.5
        strengths.append(f"Growth energy ({planet} in {_ordinal(house)} house)")

    # ── Dusthana placement ──
    if is_benefic and is_dusthana:
        score -= 0.5
        cautions.append(f"{planet} weakened in {_ordinal(house)} house — {_dusthana_label(house)}")

    if is_malefic and is_dusthana:
        score -= 1.0
        cautions.append(f"Health/loss watch ({planet} in {_ordinal(house)} house)")

    # ── Specific high-impact combos ──
    if planet == "Sun" and house == 10:
        score += 2.0
        strengths.append(f"Career fame city (Sun in 10th house)")
    if planet == "Venus" and house == 7:
        score += 2.0
        strengths.append(f"Relationship city (Venus in 7th house)")
    if planet == "Jupiter" and house in {2, 11}:
        score += 1.5
        strengths.append(f"Wealth city (Jupiter in {_ordinal(house)} house)")
    if planet == "Jupiter" and house == 10:
        score += 2.0
        strengths.append(f"Career boost (Jupiter in 10th house)")
    if planet == "Saturn" and house in {6, 8}:
        score -= 1.5
        cautions.append(f"Health caution city (Saturn in {_ordinal(house)} house)")
    if planet == "Mars" and house == 1:
        score -= 0.5
        cautions.append(f"Mangal influence on self (Mars in 1st house)")
    if planet == "Rahu" and house == 10:
        score += 0.5
        strengths.append(f"Unconventional career gains (Rahu in 10th house)")
    if planet == "Moon" and house == 4:
        score += 1.5
        strengths.append(f"Emotional peace city (Moon in 4th house)")
    if planet == "Mercury" and house == 10:
        score += 1.0
        strengths.append(f"Communication/business city (Mercury in 10th house)")

    return score, strengths, cautions


def _ordinal(n: int) -> str:
    """1 -> '1st', 2 -> '2nd', etc."""
    if 11 <= n % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def _dusthana_label(house: int) -> str:
    """Human label for dusthana houses."""
    return {6: "enemies/health issues", 8: "obstacles/transformation", 12: "losses/isolation"}.get(house, "challenge")


# ── Category scorers for best-cities ranking ─────────────────

_CATEGORY_RULES: Dict[str, List[Tuple[str, int, float, str]]] = {
    # category: [(planet, house, bonus, reason), ...]
    "career": [
        ("Sun", 10, 3.0, "Sun in 10th — fame and authority"),
        ("Jupiter", 10, 2.5, "Jupiter in 10th — expansion in career"),
        ("Mercury", 10, 2.0, "Mercury in 10th — business acumen"),
        ("Mars", 10, 1.5, "Mars in 10th — drive and ambition"),
        ("Rahu", 10, 1.0, "Rahu in 10th — unconventional success"),
        ("Saturn", 10, 0.5, "Saturn in 10th — slow but lasting career"),
        ("Sun", 1, 1.5, "Sun in 1st — strong personality and presence"),
    ],
    "relationships": [
        ("Venus", 7, 3.0, "Venus in 7th — harmonious partnerships"),
        ("Jupiter", 7, 2.0, "Jupiter in 7th — blessed relationships"),
        ("Moon", 7, 1.5, "Moon in 7th — emotional bonds"),
        ("Venus", 1, 1.0, "Venus in 1st — personal charm"),
        ("Venus", 5, 1.5, "Venus in 5th — romantic creativity"),
    ],
    "wealth": [
        ("Jupiter", 2, 3.0, "Jupiter in 2nd — abundant wealth"),
        ("Jupiter", 11, 2.5, "Jupiter in 11th — large gains"),
        ("Venus", 2, 2.0, "Venus in 2nd — luxury and comfort"),
        ("Mercury", 2, 1.5, "Mercury in 2nd — smart finances"),
        ("Moon", 11, 1.0, "Moon in 11th — steady gains"),
        ("Sun", 11, 1.0, "Sun in 11th — recognition brings gains"),
    ],
    "health": [
        ("Jupiter", 1, 2.0, "Jupiter in 1st — vitality and protection"),
        ("Sun", 1, 1.5, "Sun in 1st — strong constitution"),
        ("Moon", 4, 1.5, "Moon in 4th — emotional well-being"),
        ("Venus", 4, 1.0, "Venus in 4th — comfortable living"),
    ],
    "spiritual": [
        ("Jupiter", 9, 3.0, "Jupiter in 9th — guru and dharma blessings"),
        ("Ketu", 12, 2.0, "Ketu in 12th — moksha and liberation"),
        ("Moon", 9, 1.5, "Moon in 9th — spiritual inclination"),
        ("Sun", 9, 1.5, "Sun in 9th — righteous path"),
        ("Jupiter", 12, 1.0, "Jupiter in 12th — charitable and transcendental"),
    ],
}


# ── Planetary line detection ─────────────────────────────────

def _detect_planetary_lines(
    planet_houses: Dict[str, int],
    city_name: str,
) -> Dict[str, str]:
    """
    Detect if any planet is near an angular cusp for this city.
    Returns dict of line_name -> city_name for planets on angular cusps.
    """
    lines: Dict[str, str] = {}
    cusp_labels = {1: "ASC", 4: "IC", 7: "DSC", 10: "MC"}
    for planet, house in planet_houses.items():
        if house in cusp_labels:
            line_key = f"{planet}_{cusp_labels[house]}"
            lines[line_key] = city_name
    return lines


# ── Main calculation ─────────────────────────────────────────

def calculate_astro_map(
    birth_date: str,
    birth_time: str,
    birth_tz_offset: float,
    planet_longitudes: Dict[str, float],
    cities: Optional[Dict[str, Tuple[float, float]]] = None,
) -> Dict[str, Any]:
    """
    Main Astro-Cartography calculation.

    For each city, calculate the local ascendant, determine which house
    each planet falls in, score the city for different life areas, and
    rank best/worst cities.

    Parameters
    ----------
    birth_date : str
        Birth date in YYYY-MM-DD format.
    birth_time : str
        Birth time in HH:MM:SS format.
    birth_tz_offset : float
        Timezone offset in hours (e.g. 5.5 for IST).
    planet_longitudes : dict
        Sidereal longitudes for each planet, e.g. {"Sun": 126.87, ...}.
    cities : dict or None
        City name -> (lat, lon).  Defaults to MAJOR_CITIES.

    Returns
    -------
    dict
        Full analysis: city_analysis, best_cities, planetary_lines.
    """
    if cities is None:
        cities = MAJOR_CITIES

    city_analysis: Dict[str, Any] = {}
    # Aggregate planetary lines across cities: line_key -> [city_names]
    planetary_lines: Dict[str, List[str]] = {}
    # Category scores per city for ranking
    category_scores: Dict[str, Dict[str, Tuple[float, str]]] = {
        cat: {} for cat in _CATEGORY_RULES
    }

    for city_name, (lat, lon) in cities.items():
        try:
            asc_deg = calculate_ascendant_for_location(
                birth_date, birth_time, lat, lon, birth_tz_offset,
            )
        except Exception:
            # Skip city if calculation fails
            continue

        house_cusps = calculate_houses_for_location(asc_deg)

        # Determine planet houses and sign info
        planet_houses_map: Dict[str, Dict[str, Any]] = {}
        planet_house_numbers: Dict[str, int] = {}
        total_score = 5.0  # base score out of 10
        all_strengths: List[str] = []
        all_cautions: List[str] = []

        for planet_name in _ALL_PLANETS:
            plon = planet_longitudes.get(planet_name)
            if plon is None:
                continue
            plon = float(plon) % 360.0
            house = get_planet_house(plon, house_cusps)
            sign = _sign_from_longitude(plon)
            planet_houses_map[planet_name] = {
                "house": house,
                "sign": sign,
                "longitude": round(plon, 2),
            }
            planet_house_numbers[planet_name] = house

            # Score
            delta, strengths, cautions = _score_planet_in_house(planet_name, house)
            total_score += delta
            all_strengths.extend(strengths)
            all_cautions.extend(cautions)

        # Clamp overall score to 0-10
        overall_score = round(max(0.0, min(10.0, total_score)), 1)

        # Ascendant info
        asc_sign = _sign_from_longitude(asc_deg)
        asc_in_sign = _degree_in_sign(asc_deg)

        city_analysis[city_name] = {
            "ascendant": {
                "sign": asc_sign,
                "degree": round(asc_deg, 2),
                "degree_in_sign": asc_in_sign,
            },
            "planet_houses": planet_houses_map,
            "strengths": all_strengths,
            "cautions": all_cautions,
            "overall_score": overall_score,
        }

        # Planetary lines
        lines = _detect_planetary_lines(planet_house_numbers, city_name)
        for line_key, cname in lines.items():
            planetary_lines.setdefault(line_key, []).append(cname)

        # Category scoring
        for category, rules in _CATEGORY_RULES.items():
            cat_score = 0.0
            reasons: List[str] = []
            for planet, target_house, bonus, reason in rules:
                if planet_house_numbers.get(planet) == target_house:
                    cat_score += bonus
                    reasons.append(reason)
            if cat_score > 0:
                category_scores[category][city_name] = (cat_score, "; ".join(reasons))

    # Build best_cities rankings
    best_cities: Dict[str, List[Tuple[str, float, str]]] = {}
    for category, city_scores in category_scores.items():
        ranked = sorted(city_scores.items(), key=lambda x: x[1][0], reverse=True)
        best_cities[category] = [
            (cname, round(sc, 1), reason)
            for cname, (sc, reason) in ranked[:5]
        ]

    return {
        "birth_planets": {
            p: round(float(v), 2)
            for p, v in planet_longitudes.items()
        },
        "city_analysis": city_analysis,
        "best_cities": best_cities,
        "planetary_lines": planetary_lines,
    }
