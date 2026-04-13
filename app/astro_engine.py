"""
astro_engine.py -- Vedic Astrology Planetary Calculation Engine
===============================================================
Wrapper around Swiss Ephemeris (swisseph). Falls back to pure-math
approximations when swisseph is not installed.

Provides:
  - ZODIAC_SIGNS, PLANETS, NAKSHATRAS data tables
  - calculate_planet_positions(birth_date, birth_time, lat, lon, tz_offset)
  - get_sign_from_longitude(longitude)
  - get_nakshatra_from_longitude(longitude)
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from app.divisional_charts import _calculate_d9

# ---------- Try to import Swiss Ephemeris ----------
try:
    import swisseph as swe

    _HAS_SWE = True
    # Set ephemeris data path if configured (env var EPHE_PATH)
    import os as _os
    _ephe_path = _os.getenv("EPHE_PATH", "")
    if _ephe_path:
        swe.set_ephe_path(_ephe_path)
    swe.set_sid_mode(swe.SIDM_LAHIRI)  # Lahiri ayanamsa (default for Vedic)
except ImportError:
    _HAS_SWE = False

# ============================================================
# ZODIAC_SIGNS -- 12 signs, each spanning 30 degrees
# ============================================================
ZODIAC_SIGNS: List[Dict[str, Any]] = [
    {"index": i, "name": name, "start_degree": i * 30, "end_degree": (i + 1) * 30}
    for i, name in enumerate(
        [
            "Aries", "Taurus", "Gemini", "Cancer",
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces",
        ]
    )
]

_SIGN_NAMES = [s["name"] for s in ZODIAC_SIGNS]

# ============================================================
# PLANETS -- swisseph constant mapping
# ============================================================
# SE constants (same numeric values as swisseph)
SE_SUN = 0
SE_MOON = 1
SE_MERCURY = 2
SE_VENUS = 3
SE_MARS = 4
SE_JUPITER = 5
SE_SATURN = 6
SE_MEAN_NODE = 10  # Rahu (mean node); Ketu = Rahu + 180
SE_TRUE_NODE = 11  # Rahu (true/osculating node)

PLANETS: Dict[str, int] = {
    "Sun": SE_SUN,
    "Moon": SE_MOON,
    "Mars": SE_MARS,
    "Mercury": SE_MERCURY,
    "Jupiter": SE_JUPITER,
    "Venus": SE_VENUS,
    "Saturn": SE_SATURN,
    "Rahu": SE_MEAN_NODE,
    # Ketu is derived: longitude = Rahu + 180
}

# ============================================================
# NAKSHATRAS -- 27 lunar mansions, 13deg20' each
# ============================================================
_NAKSHATRA_DATA: List[Tuple[str, str]] = [
    ("Ashwini", "Ketu"),
    ("Bharani", "Venus"),
    ("Krittika", "Sun"),
    ("Rohini", "Moon"),
    ("Mrigashira", "Mars"),
    ("Ardra", "Rahu"),
    ("Punarvasu", "Jupiter"),
    ("Pushya", "Saturn"),
    ("Ashlesha", "Mercury"),
    ("Magha", "Ketu"),
    ("Purva Phalguni", "Venus"),
    ("Uttara Phalguni", "Sun"),
    ("Hasta", "Moon"),
    ("Chitra", "Mars"),
    ("Swati", "Rahu"),
    ("Vishakha", "Jupiter"),
    ("Anuradha", "Saturn"),
    ("Jyeshtha", "Mercury"),
    ("Mula", "Ketu"),
    ("Purva Ashadha", "Venus"),
    ("Uttara Ashadha", "Sun"),
    ("Shravana", "Moon"),
    ("Dhanishta", "Mars"),
    ("Shatabhisha", "Rahu"),
    ("Purva Bhadrapada", "Jupiter"),
    ("Uttara Bhadrapada", "Saturn"),
    ("Revati", "Mercury"),
]

NAKSHATRA_SPAN = 360.0 / 27.0  # 13 deg 20 min = 13.3333...
PADA_SPAN = NAKSHATRA_SPAN / 4.0  # 3 deg 20 min

NAKSHATRAS: List[Dict[str, Any]] = []
for _i, (_nname, _lord) in enumerate(_NAKSHATRA_DATA):
    NAKSHATRAS.append(
        {
            "index": _i,
            "name": _nname,
            "start_degree": _i * NAKSHATRA_SPAN,
            "end_degree": (_i + 1) * NAKSHATRA_SPAN,
            "lord": _lord,
        }
    )


# ============================================================
# PUBLIC FUNCTIONS
# ============================================================

def get_sign_from_longitude(longitude: float) -> str:
    """Return the zodiac sign name for a given sidereal longitude (0-360)."""
    longitude = longitude % 360.0
    index = int(longitude / 30.0)
    return _SIGN_NAMES[index]


def get_nakshatra_from_longitude(longitude: float) -> Dict[str, Any]:
    """
    Return nakshatra info for a given sidereal longitude.
    Returns: {name, pada (1-4), lord}
    """
    longitude = longitude % 360.0
    nak_index = int(longitude / NAKSHATRA_SPAN)
    if nak_index >= 27:
        nak_index = 26
    nak = NAKSHATRAS[nak_index]
    offset_in_nak = longitude - nak["start_degree"]
    pada = int(offset_in_nak / PADA_SPAN) + 1
    if pada > 4:
        pada = 4
    return {"name": nak["name"], "pada": pada, "lord": nak["lord"], "index": nak_index}


def calculate_planet_positions(
    birth_date: str,
    birth_time: str,
    latitude: float,
    longitude: float,
    tz_offset: float,
    ayanamsa: str = "lahiri",
    node_type: str = "mean",
) -> Dict[str, Any]:
    """
    Calculate Vedic (sidereal) planet positions for a birth chart.

    Args:
        birth_date: ISO date string  "YYYY-MM-DD"
        birth_time: Time string      "HH:MM" or "HH:MM:SS"
        latitude:   Birth latitude   (-90 to 90)
        longitude:  Birth longitude  (-180 to 180)
        tz_offset:  Hours from UTC   (e.g. 5.5 for IST)
        ayanamsa:   Ayanamsa system  "lahiri" (default) or "kp" (Krishnamurti)
        node_type:  "mean" (default) uses SE_MEAN_NODE for Rahu;
                    "true" uses SE_TRUE_NODE (osculating node).
                    Ketu is always Rahu + 180.

    Returns:
        {
            "planets": {name: {longitude, sign, sign_degree, nakshatra, nakshatra_pada, house}},
            "ascendant": {longitude, sign},
            "houses": [{number, sign, degree}],
            "ayanamsa_system": "lahiri" | "kp",
        }
    """
    # Parse date + time  ->  UTC datetime
    dt_local = _parse_datetime(birth_date, birth_time, tz_offset)

    if _HAS_SWE:
        result = _calculate_swe(dt_local, latitude, longitude, ayanamsa=ayanamsa, node_type=node_type)
        result["_engine"] = "swisseph"
        result["_debug_jd"] = result.get("julian_day")
        result["_debug_ayanamsa"] = result.get("ayanamsa")
        return result
    else:
        result = _calculate_fallback(dt_local, latitude, longitude)
        result["_engine"] = "fallback"
        result["ayanamsa_system"] = ayanamsa
        return result


# ============================================================
# INTERNAL: datetime parsing
# ============================================================

def _parse_datetime(date_str: str, time_str: str, tz_offset: float) -> datetime:
    """Parse date + time + tz_offset into a UTC datetime."""
    parts = date_str.split("-")
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])

    time_parts = time_str.split(":")
    hour = int(time_parts[0])
    minute = int(time_parts[1]) if len(time_parts) > 1 else 0
    second = int(time_parts[2]) if len(time_parts) > 2 else 0

    tz = timezone(timedelta(hours=tz_offset))
    local_dt = datetime(year, month, day, hour, minute, second, tzinfo=tz)
    return local_dt.astimezone(timezone.utc)


# ============================================================
# INTERNAL: Swiss Ephemeris path
# ============================================================

def _datetime_to_jd(dt_utc: datetime) -> float:
    """Convert a UTC datetime to Julian Day Number."""
    if _HAS_SWE:
        return swe.julday(
            dt_utc.year, dt_utc.month, dt_utc.day,
            dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0,
        )
    # Manual Julian Day calculation (Meeus algorithm)
    y = dt_utc.year
    m = dt_utc.month
    d = dt_utc.day + (dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0) / 24.0

    if m <= 2:
        y -= 1
        m += 12

    a = int(y / 100)
    b = 2 - a + int(a / 4)
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5


def _calculate_swe(dt_utc: datetime, lat: float, lon: float, ayanamsa: str = "lahiri", node_type: str = "mean") -> Dict[str, Any]:
    """Full calculation using Swiss Ephemeris."""
    # Set ayanamsa mode: KP (Krishnamurti) or Lahiri (default for Vedic)
    ayanamsa_system = ayanamsa  # preserve system name before numeric override
    original_mode = swe.get_sid_mode()
    try:
        if ayanamsa_system == "kp":
            swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
        else:
            swe.set_sid_mode(swe.SIDM_LAHIRI)
        jd = _datetime_to_jd(dt_utc)

        # Ayanamsa for sidereal
        ayanamsa = swe.get_ayanamsa(jd)

        # Ascendant (use Placidus just for Ascendant degree, then Whole Sign houses)
        cusps, ascmc = swe.houses(jd, lat, lon, b"P")
        asc_sid = (ascmc[0] - ayanamsa) % 360.0

        # Whole Sign house system (Vedic standard): House 1 = Ascendant's sign
        asc_sign_index = int(asc_sid // 30)
        houses = []
        for i in range(12):
            sign_index = (asc_sign_index + i) % 12
            sign_degree = float(sign_index * 30)
            houses.append(
                {
                    "number": i + 1,
                    "sign": _SIGN_NAMES[sign_index],
                    "degree": round(sign_degree, 4),
                }
            )

        # Store Placidus cusps for KP system (needs unequal cusps)
        placidus_cusps = []
        for i in range(12):
            cusp_sid = (cusps[i] - ayanamsa) % 360.0
            placidus_cusps.append(round(cusp_sid, 4))

        # Resolve Rahu node constant based on node_type parameter
        rahu_node_id = SE_TRUE_NODE if node_type == "true" else SE_MEAN_NODE

        # Planets — use Whole Sign house assignment
        # First pass: compute longitudes and retrograde (need Sun longitude for combust)
        planets_result: Dict[str, Dict[str, Any]] = {}
        planet_longitudes: Dict[str, float] = {}
        planet_retrograde: Dict[str, bool] = {}

        for pname, pid in PLANETS.items():
            # Override Rahu's planet ID based on node_type
            if pname == "Rahu":
                pid = rahu_node_id
            pos, _ret = swe.calc_ut(jd, pid)
            trop_lon = pos[0]
            daily_speed = pos[3]  # daily speed in longitude
            sid_lon = (trop_lon - ayanamsa) % 360.0
            planet_longitudes[pname] = sid_lon

            # Retrograde: negative daily speed means the planet appears to move backward
            # Rahu (mean node) is always retrograde by nature
            is_retrograde = daily_speed < 0 or pname == "Rahu"
            planet_retrograde[pname] = is_retrograde

        # Ketu longitude
        rahu_lon = planet_longitudes["Rahu"]
        ketu_lon = (rahu_lon + 180.0) % 360.0
        planet_longitudes["Ketu"] = ketu_lon
        planet_retrograde["Ketu"] = True

        # Get Sun longitude for combust checks
        sun_lon = planet_longitudes.get("Sun", 0.0)

        # Second pass: compute combust, vargottama, build full result
        for pname in list(PLANETS.keys()) + ["Ketu"]:
            sid_lon = planet_longitudes[pname]
            is_retrograde = planet_retrograde[pname]

            nak = get_nakshatra_from_longitude(sid_lon)
            sign = get_sign_from_longitude(sid_lon)
            sign_deg = sid_lon % 30.0
            planet_sign_index = int(sid_lon // 30)
            house = ((planet_sign_index - asc_sign_index) % 12) + 1

            combust = _is_combust(pname, sid_lon, sun_lon, is_retrograde)
            vargottama = _is_vargottama(sid_lon)
            sandhi = sign_deg < 1.0 or sign_deg > 29.0

            planets_result[pname] = {
                "longitude": round(sid_lon, 4),
                "sign": sign,
                "sign_degree": round(sign_deg, 4),
                "nakshatra": nak["name"],
                "nakshatra_pada": nak["pada"],
                "house": house,
                "retrograde": is_retrograde,
                "is_combust": combust,
                "is_vargottama": vargottama,
                "is_sandhi": sandhi,
                "status": _build_status(pname, sign, is_retrograde, combust, vargottama, sandhi),
            }

        return {
            "planets": planets_result,
            "ascendant": {
                "longitude": round(asc_sid, 4),
                "sign": get_sign_from_longitude(asc_sid),
                "sign_degree": round(asc_sid % 30.0, 4),
            },
            "houses": houses,
            "placidus_cusps": placidus_cusps,
            "ayanamsa_value": round(ayanamsa, 6),
            "ayanamsa_system": ayanamsa_system,
        }
    finally:
        swe.set_sid_mode(original_mode)


# ============================================================
# INTERNAL: Pure-math FALLBACK (no swisseph)
# ============================================================

# Lahiri ayanamsa approximation (linear model, epoch J2000.0 = JD 2451545.0)
_AYANAMSA_J2000 = 23.856          # degrees at J2000
_AYANAMSA_RATE = 50.2788 / 3600.0  # degrees per year (precession rate)

def _approx_ayanamsa(jd: float) -> float:
    """Approximate Lahiri ayanamsa for a given Julian Day."""
    years_from_j2000 = (jd - 2451545.0) / 365.25
    return _AYANAMSA_J2000 + _AYANAMSA_RATE * years_from_j2000


def _approx_sun_longitude(jd: float) -> float:
    """Approximate tropical Sun longitude (low-precision formula)."""
    # Days from J2000
    d = jd - 2451545.0
    # Mean longitude
    l0 = (280.46646 + 0.9856474 * d) % 360.0
    # Mean anomaly
    m = math.radians((357.52911 + 0.9856003 * d) % 360.0)
    # Equation of center
    c = 1.9146 * math.sin(m) + 0.02 * math.sin(2 * m)
    return (l0 + c) % 360.0


def _approx_moon_longitude(jd: float) -> float:
    """Approximate tropical Moon longitude."""
    d = jd - 2451545.0
    # Mean longitude
    l0 = (218.3165 + 13.176396 * d) % 360.0
    # Mean anomaly
    m_moon = math.radians((134.963 + 13.06499 * d) % 360.0)
    m_sun = math.radians((357.529 + 0.98560 * d) % 360.0)
    # Mean elongation
    dd = math.radians((297.850 + 12.19075 * d) % 360.0)
    # Corrections
    corr = (
        6.289 * math.sin(m_moon)
        - 1.274 * math.sin(2 * dd - m_moon)
        + 0.658 * math.sin(2 * dd)
        + 0.214 * math.sin(2 * m_moon)
        - 0.186 * math.sin(m_sun)
    )
    return (l0 + corr) % 360.0


def _approx_planet_longitude(jd: float, planet_name: str) -> float:
    """
    Very rough approximation for planetary tropical longitudes.
    Uses simplified mean-longitude + single-harmonic correction.
    Accuracy: ~2-5 degrees for inner planets, ~1-3 for outer.
    """
    d = jd - 2451545.0

    # Mean orbital elements at J2000 + rates (degrees, degrees/day)
    _ELEMENTS = {
        "Mercury": (252.251, 4.09233445, 0.387098, 23.44, 77.456),
        "Venus":   (181.980, 1.60213049, 0.723330, 0.615, 131.564),
        "Mars":    (355.433, 0.52402068, 1.523688, 10.69, 336.060),
        "Jupiter": ( 34.351, 0.08308529, 5.202560, 5.55, 14.331),
        "Saturn":  ( 50.077, 0.03344414, 9.554747, 6.92, 93.057),
    }

    if planet_name in ("Sun",):
        return _approx_sun_longitude(jd)
    if planet_name in ("Moon",):
        return _approx_moon_longitude(jd)
    if planet_name in ("Rahu",):
        return _approx_rahu_longitude(jd)

    if planet_name not in _ELEMENTS:
        return 0.0

    l0, rate, _au, eqn_amp, omega = _ELEMENTS[planet_name]

    # Mean anomaly of planet
    mean_lon = (l0 + rate * d) % 360.0
    m_planet = math.radians((mean_lon - omega) % 360.0)

    # Equation of center (simplified single-term)
    corr = eqn_amp * math.sin(m_planet)

    # Earth's position (for geocentric conversion)
    sun_lon = _approx_sun_longitude(jd)
    # Very rough geocentric: heliocentric + parallax approximation
    helio = (mean_lon + corr) % 360.0

    # Convert heliocentric to geocentric (simplified)
    if planet_name in ("Mercury", "Venus"):
        # Inner planets: approximate geocentric elongation
        diff = helio - sun_lon
        geo = (sun_lon + diff * 0.8) % 360.0
    else:
        # Outer planets: rough approximation
        geo = helio  # Close enough for fallback

    return geo % 360.0


def _approx_rahu_longitude(jd: float) -> float:
    """Approximate mean lunar node (Rahu) tropical longitude."""
    d = jd - 2451545.0
    # Mean longitude of ascending node (retrograde)
    return (125.044 - 0.0529539 * d) % 360.0


def _approx_ascendant(jd: float, lat: float, lon: float) -> float:
    """
    Approximate the tropical Ascendant (rising sign).
    Uses local sidereal time + obliquity.
    """
    d = jd - 2451545.0
    # Greenwich Mean Sidereal Time (degrees)
    gmst = (280.46061837 + 360.98564736629 * d) % 360.0
    # Local sidereal time
    lst = (gmst + lon) % 360.0
    lst_rad = math.radians(lst)

    # Obliquity of ecliptic
    eps = math.radians(23.4393 - 0.0000004 * d)
    lat_rad = math.radians(lat)

    # Ascendant formula
    y_val = -math.cos(lst_rad)
    x_val = math.sin(eps) * math.tan(lat_rad) + math.cos(eps) * math.sin(lst_rad)

    asc = math.degrees(math.atan2(y_val, x_val)) % 360.0
    return asc


def _calculate_fallback(dt_utc: datetime, lat: float, lon: float) -> Dict[str, Any]:
    """Fallback calculation using pure-math approximations (no swisseph)."""
    jd = _datetime_to_jd(dt_utc)
    ayanamsa = _approx_ayanamsa(jd)

    # Ascendant
    asc_trop = _approx_ascendant(jd, lat, lon)
    asc_sid = (asc_trop - ayanamsa) % 360.0

    # Houses (equal house system from ascendant)
    houses = []
    for i in range(12):
        cusp = (asc_sid + i * 30.0) % 360.0
        houses.append(
            {
                "number": i + 1,
                "sign": get_sign_from_longitude(cusp),
                "degree": round(cusp, 4),
            }
        )

    # Planet longitudes
    _PLANET_FUNCS = {
        "Sun": lambda: _approx_sun_longitude(jd),
        "Moon": lambda: _approx_moon_longitude(jd),
        "Mercury": lambda: _approx_planet_longitude(jd, "Mercury"),
        "Venus": lambda: _approx_planet_longitude(jd, "Venus"),
        "Mars": lambda: _approx_planet_longitude(jd, "Mars"),
        "Jupiter": lambda: _approx_planet_longitude(jd, "Jupiter"),
        "Saturn": lambda: _approx_planet_longitude(jd, "Saturn"),
        "Rahu": lambda: _approx_rahu_longitude(jd),
    }

    # First pass: compute all sidereal longitudes
    planet_lons: Dict[str, float] = {}
    for pname in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu"]:
        trop_lon = _PLANET_FUNCS[pname]()
        planet_lons[pname] = (trop_lon - ayanamsa) % 360.0

    # Ketu = Rahu + 180
    planet_lons["Ketu"] = (planet_lons["Rahu"] + 180.0) % 360.0

    sun_lon = planet_lons["Sun"]
    cusp_degrees = [h["degree"] for h in houses]

    planets_result: Dict[str, Dict[str, Any]] = {}
    for pname in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]:
        sid_lon = planet_lons[pname]

        nak = get_nakshatra_from_longitude(sid_lon)
        sign = get_sign_from_longitude(sid_lon)
        sign_deg = sid_lon % 30.0
        house = _find_house(sid_lon, cusp_degrees)

        # Fallback path cannot determine retrograde from speed;
        # Rahu and Ketu are always retrograde by nature, others default to False
        is_retrograde = pname in ("Rahu", "Ketu")

        combust = _is_combust(pname, sid_lon, sun_lon, is_retrograde)
        vargottama = _is_vargottama(sid_lon)
        sandhi = sign_deg < 1.0 or sign_deg > 29.0

        planets_result[pname] = {
            "longitude": round(sid_lon, 4),
            "sign": sign,
            "sign_degree": round(sign_deg, 4),
            "nakshatra": nak["name"],
            "nakshatra_pada": nak["pada"],
            "house": house,
            "retrograde": is_retrograde,
            "is_combust": combust,
            "is_vargottama": vargottama,
            "is_sandhi": sandhi,
            "status": _build_status(pname, sign, is_retrograde, combust, vargottama, sandhi),
        }

    return {
        "planets": planets_result,
        "ascendant": {
            "longitude": round(asc_sid, 4),
            "sign": get_sign_from_longitude(asc_sid),
            "sign_degree": round(asc_sid % 30.0, 4),
        },
        "houses": houses,
    }


# ============================================================
# INTERNAL: Planetary dignity & status
# ============================================================

# Exaltation signs for each planet
_EXALTATION_SIGN: Dict[str, str] = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
    "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces",
    "Saturn": "Libra", "Rahu": "Gemini", "Ketu": "Sagittarius",
}

# Debilitation signs (opposite of exaltation)
_DEBILITATION_SIGN: Dict[str, str] = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
    "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo",
    "Saturn": "Aries", "Rahu": "Sagittarius", "Ketu": "Gemini",
}

# Own signs (Moolatrikona / Swakshetra)
_OWN_SIGN: Dict[str, List[str]] = {
    "Sun": ["Leo"],
    "Moon": ["Cancer"],
    "Mars": ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Venus": ["Taurus", "Libra"],
    "Saturn": ["Capricorn", "Aquarius"],
}


# Combustion orbs — max angular distance from Sun for combustion (degrees)
# Standard Vedic combustion orbs (planet-specific)
_COMBUST_ORB: Dict[str, float] = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": 14.0,   # 12° when retrograde, handled in code
    "Jupiter": 11.0,
    "Venus": 10.0,      # 8° when retrograde, handled in code
    "Saturn": 15.0,
}


def _is_combust(planet: str, planet_lon: float, sun_lon: float, is_retrograde: bool) -> bool:
    """Check if a planet is combust (too close to the Sun)."""
    if planet not in _COMBUST_ORB:
        return False
    orb = _COMBUST_ORB[planet]
    # Mercury and Venus have tighter orbs when retrograde
    if is_retrograde:
        if planet == "Mercury":
            orb = 12.0
        elif planet == "Venus":
            orb = 8.0
    # Angular distance on the ecliptic (handle wrap-around)
    diff = abs(planet_lon - sun_lon)
    if diff > 180.0:
        diff = 360.0 - diff
    return diff <= orb


def _is_vargottama(planet_lon: float) -> bool:
    """Check if a planet is vargottama (same sign in D1 and D9 Navamsha)."""
    d1_sign_index = int((planet_lon % 360.0) / 30.0)
    d9_info = _calculate_d9({"-": planet_lon})
    d9_sign_index = d9_info["-"]["sign_index"]
    return d1_sign_index == d9_sign_index


def _build_status(planet: str, sign: str, is_retrograde: bool, is_combust: bool = False, is_vargottama: bool = False, is_sandhi: bool = False) -> str:
    """
    Build a human-readable status string combining dignity, retrograde, combust, vargottama.

    Examples: "Exalted", "Retrograde", "Exalted, Retrograde", "Combust, Vargottama"
    Returns empty string when the planet has no special status.
    """
    parts: List[str] = []

    # Check dignity
    if sign == _EXALTATION_SIGN.get(planet):
        parts.append("Exalted")
    elif sign == _DEBILITATION_SIGN.get(planet):
        parts.append("Debilitated")
    elif sign in _OWN_SIGN.get(planet, []):
        parts.append("Own Sign")

    # Retrograde flag
    if is_retrograde:
        parts.append("Retrograde")

    # Combust flag
    if is_combust:
        parts.append("Combust")

    # Vargottama flag
    if is_vargottama:
        parts.append("Vargottama")

    # Sandhi flag (planet at sign boundary)
    if is_sandhi:
        parts.append("Sandhi")

    return ", ".join(parts)


def _find_house(planet_lon: float, cusp_degrees: List[float]) -> int:
    """Determine which house (1-12) a planet falls in given house cusp degrees."""
    planet_lon = planet_lon % 360.0
    for i in range(12):
        cusp_start = cusp_degrees[i]
        cusp_end = cusp_degrees[(i + 1) % 12]

        if cusp_end < cusp_start:
            # Wraps around 360
            if planet_lon >= cusp_start or planet_lon < cusp_end:
                return i + 1
        else:
            if cusp_start <= planet_lon < cusp_end:
                return i + 1

    return 1  # Default to 1st house
