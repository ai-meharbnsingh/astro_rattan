"""
dosha_engine.py — Vedic Dosha & Yoga Detection Engine
======================================================
Detects Mangal Dosha, Kaal Sarp Dosha, Sade Sati, Pitra Dosha, Kemdrum Dosha.
Also detects positive Yogas: Gajakesari, Budhaditya, Chandra-Mangal,
and Panch Mahapurusha Yogas.
"""

import re
import logging

logger = logging.getLogger(__name__)

# Zodiac signs in order (0-indexed for arithmetic)
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

ZODIAC_INDEX = {sign: i for i, sign in enumerate(ZODIAC_SIGNS)}

# Houses where Mars causes Mangal Dosha
MANGAL_DOSHA_HOUSES = {1, 2, 4, 7, 8, 12}

# Kendra houses (angular houses)
KENDRA_HOUSES = {1, 4, 7, 10}

# Exaltation signs for Panch Mahapurusha Yoga
EXALTATION_SIGNS = {
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra",
}

# Own signs for Panch Mahapurusha Yoga
OWN_SIGNS = {
    "Mars": {"Aries", "Scorpio"},
    "Mercury": {"Gemini", "Virgo"},
    "Jupiter": {"Sagittarius", "Pisces"},
    "Venus": {"Taurus", "Libra"},
    "Saturn": {"Capricorn", "Aquarius"},
}

# Full exaltation/debilitation/own-sign tables for strength computation
_YOGA_EXALT = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
    "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra",
}
_YOGA_DEBIL = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
    "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries",
}
_YOGA_OWN = {
    "Sun": {"Leo"}, "Moon": {"Cancer"},
    "Mars": {"Aries", "Scorpio"}, "Mercury": {"Gemini", "Virgo"},
    "Jupiter": {"Sagittarius", "Pisces"}, "Venus": {"Taurus", "Libra"},
    "Saturn": {"Capricorn", "Aquarius"},
}


def _compute_yoga_strength(yoga: dict, planets: dict) -> str:
    """Compute yoga strength from dignity of its involved planets."""
    involved = yoga.get("planets_involved") or []
    if not involved:
        return "moderate"
    strong = sum(
        1 for p in involved
        if planets.get(p, {}).get("sign") == _YOGA_EXALT.get(p)
    )
    own = sum(
        1 for p in involved
        if planets.get(p, {}).get("sign") in _YOGA_OWN.get(p, set())
    )
    weak = sum(
        1 for p in involved
        if planets.get(p, {}).get("sign") == _YOGA_DEBIL.get(p)
    )
    if strong >= 1:
        return "strong"
    if own >= 1 and weak == 0:
        return "moderate"
    if weak >= 1 and strong == 0:
        return "weak"
    return "moderate"

# Malefic planets
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


_TERM_KEY_OVERRIDES = {
    # Doshas
    "mangal dosha": "DOSHA_MANGAL",
    "kaal sarp dosha": "DOSHA_KAAL_SARP",
    "kal sarp dosha": "DOSHA_KAAL_SARP",
    "sade sati": "DOSHA_SADE_SATI",
    "pitra dosha": "DOSHA_PITRA",
    "kemdrum dosha": "DOSHA_KEMDRUM",
    "kemadrum dosha": "DOSHA_KEMDRUM",
    "angarak dosha": "DOSHA_ANGARAK",
    "guru chandal dosha": "DOSHA_GURU_CHANDAL",
    "vish dosha": "DOSHA_VISH",
    "shrapit dosha": "DOSHA_SHRAPIT",
    "grahan dosha": "DOSHA_GRAHAN",
    "ghatak dosha": "DOSHA_GHATAK",
    "daridra dosha": "DOSHA_DARIDRA",
    # Yogas
    "gajakesari yoga": "YOGA_GAJAKESARI",
    "gaj kesari yoga": "YOGA_GAJAKESARI",
    "budhaditya yoga": "YOGA_BUDHADITYA",
    "chandra mangal yoga": "YOGA_CHANDRA_MANGAL",
    "chandra-mangal yoga": "YOGA_CHANDRA_MANGAL",
    "ruchaka yoga": "YOGA_RUCHAKA",
    "bhadra yoga": "YOGA_BHADRA",
    "hamsa yoga": "YOGA_HAMSA",
    "malavya yoga": "YOGA_MALAVYA",
    "shasha yoga": "YOGA_SHASHA",
    "sunapha yoga": "YOGA_SUNAPHA",
    "anapha yoga": "YOGA_ANAPHA",
    "durudhara yoga": "YOGA_DURUDHARA",
    "shakata yoga": "YOGA_SHAKATA",
    "adhi yoga": "YOGA_ADHI",
    "amala yoga": "YOGA_AMALA",
    "raja yoga": "YOGA_RAJA",
    "lakshmi yoga": "YOGA_LAKSHMI",
    "dhana yoga": "YOGA_DHANA",
    "saraswati yoga": "YOGA_SARASWATI",
    "neecha bhanga raja yoga": "YOGA_NEECHA_BHANGA_RAJA",
    "panch mahapurusha yoga": "YOGA_PANCH_MAHAPURUSHA",
    "viparit raja yoga": "YOGA_VIPARIT_RAJA",
    "danda yoga": "YOGA_DANDA",
    "kemadruma yoga": "YOGA_KEMADRUMA",
    "vasi yoga": "YOGA_VASI",
    "parashari raja yoga": "YOGA_PARASHARI_RAJA",
    "surya in swa rashi": "YOGA_SURYA_IN_SWA_RASHI_SUN_IN_OWN_SIGN",
    "shani uchcha": "YOGA_SHANI_UCHCHA_SATURN_EXALTED",
}


def to_translation_key(prefix: str, text: str) -> str:
    """Create a stable, API-safe translation key from a label."""
    if not text:
        return prefix
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    normalized = re.sub(r"\s+", " ", normalized)
    if normalized in _TERM_KEY_OVERRIDES:
        return _TERM_KEY_OVERRIDES[normalized]

    base = re.sub(r"\s*\([^)]*\)\s*$", "", text.strip())
    slug = re.sub(r"[^A-Za-z0-9]+", "_", base.upper()).strip("_")
    if prefix == "YOGA" and slug.endswith("_YOGA"):
        slug = slug[:-5]
    if prefix == "DOSHA" and slug.endswith("_DOSHA"):
        slug = slug[:-6]
    return f"{prefix}_{slug}" if slug else prefix


def check_mangal_dosha(mars_house: int) -> dict:
    """
    Check if Mars placement causes Mangal (Kuja) Dosha.

    Args:
        mars_house: House number (1-12) where Mars is placed.

    Returns:
        {has_dosha: bool, severity: str, description: str, remedies: [str]}
    """
    has_dosha = mars_house in MANGAL_DOSHA_HOUSES

    if not has_dosha:
        return {
            "has_dosha": False,
            "severity": "none",
            "description": f"Mars in house {mars_house} does not cause Mangal Dosha.",
            "remedies": [],
        }

    # Severity based on house
    if mars_house in {7, 8}:
        severity = "high"
        description = (
            f"Mars in house {mars_house} causes severe Mangal Dosha. "
            "This placement strongly affects marriage and partnerships. "
            "House 7 impacts the spouse directly; house 8 affects longevity and transformation."
        )
    elif mars_house in {1, 4}:
        severity = "medium"
        description = (
            f"Mars in house {mars_house} causes moderate Mangal Dosha. "
            "House 1 affects temperament and aggression; house 4 affects domestic peace."
        )
    else:  # houses 2, 12
        severity = "mild"
        description = (
            f"Mars in house {mars_house} causes mild Mangal Dosha. "
            "House 2 affects family harmony and speech; house 12 affects expenditure and bed pleasures."
        )

    remedies = [
        "Recite Hanuman Chalisa daily, especially on Tuesdays.",
        "Perform Mangal Shanti Puja to pacify Mars energy.",
        "Wear a coral (Moonga) gemstone after consulting an astrologer.",
        "Fast on Tuesdays and donate red items (lentils, cloth).",
        "Marriage between two Manglik individuals cancels the dosha.",
        "Kumbh Vivah — symbolic marriage to a pot or tree before actual marriage.",
    ]

    return {
        "has_dosha": True,
        "severity": severity,
        "description": description,
        "remedies": remedies,
    }


def check_kaal_sarp(rahu_house: int, ketu_house: int, planet_houses: dict) -> dict:
    """
    Check for Kaal Sarp Dosha — all planets between Rahu and Ketu.

    Args:
        rahu_house: House number (1-12) of Rahu.
        ketu_house: House number (1-12) of Ketu.
        planet_houses: Dict of {planet_name: house_number} for the 7 planets
                       (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn).

    Returns:
        {has_dosha: bool, dosha_type: str, description: str, affected_planets: [str], remedies: [str]}
    """
    if not planet_houses:
        return {
            "has_dosha": False,
            "dosha_type": "none",
            "description": "No planet data provided.",
            "affected_planets": [],
            "remedies": [],
        }

    # Determine the arc from Rahu to Ketu (going forward through houses 1-12)
    # All planets must be within this arc for Kaal Sarp
    def _houses_in_arc(start: int, end: int) -> set:
        """Get all houses in the arc from start to end (inclusive, going forward)."""
        houses = set()
        h = start
        while True:
            houses.add(h)
            if h == end:
                break
            h = (h % 12) + 1
        return houses

    # Arc from Rahu to Ketu
    arc_rahu_to_ketu = _houses_in_arc(rahu_house, ketu_house)
    # Arc from Ketu to Rahu
    arc_ketu_to_rahu = _houses_in_arc(ketu_house, rahu_house)

    # Check if all planets fall in one arc
    planet_list = list(planet_houses.items())
    all_in_rahu_to_ketu = all(h in arc_rahu_to_ketu for _, h in planet_list)
    all_in_ketu_to_rahu = all(h in arc_ketu_to_rahu for _, h in planet_list)

    has_dosha = all_in_rahu_to_ketu or all_in_ketu_to_rahu

    if not has_dosha:
        return {
            "has_dosha": False,
            "dosha_type": "none",
            "description": "Planets are distributed on both sides of the Rahu-Ketu axis. No Kaal Sarp Dosha.",
            "affected_planets": [],
            "remedies": [],
        }

    # Determine type
    if all_in_rahu_to_ketu:
        dosha_type = "Ascending (Rahu leading)"
        affected = [p for p, h in planet_list if h in arc_rahu_to_ketu]
    else:
        dosha_type = "Descending (Ketu leading)"
        affected = [p for p, h in planet_list if h in arc_ketu_to_rahu]

    # Named Kaal Sarp types based on Rahu's house
    kaal_sarp_names = {
        1: "Anant", 2: "Kulik", 3: "Vasuki", 4: "Shankhpal",
        5: "Padma", 6: "Mahapadma", 7: "Takshak", 8: "Karkotak",
        9: "Shankhachur", 10: "Ghatak", 11: "Vishdhar", 12: "Sheshnag",
    }
    named_type = kaal_sarp_names.get(rahu_house, "Unknown")

    description = (
        f"{named_type} Kaal Sarp Dosha detected ({dosha_type}). "
        f"All 7 planets are hemmed between Rahu (house {rahu_house}) and Ketu (house {ketu_house}). "
        "This yoga can cause delays, obstacles, and karmic challenges in life."
    )

    remedies = [
        "Perform Kaal Sarp Dosha Nivaran Puja at Trimbakeshwar or Rameswaram.",
        "Recite Rahu Beej Mantra: 'Om Bhram Bhreem Bhroum Sah Rahave Namah' 108 times daily.",
        "Donate black sesame seeds and a black cloth on Saturdays.",
        "Worship Lord Shiva with Abhishek on Mondays.",
        "Wear a Gomed (Hessonite) gemstone for Rahu after consultation.",
    ]

    return {
        "has_dosha": True,
        "dosha_type": f"{named_type} ({dosha_type})",
        "description": description,
        "affected_planets": affected,
        "remedies": remedies,
    }


def check_sade_sati(moon_sign: str, saturn_sign: str) -> dict:
    """
    Check for Sade Sati — Saturn transiting over natal Moon sign (+/- 1 sign).
    Also checks for Ashtam Shani (Saturn in 8th house from Moon — Panauti).

    Sade Sati is active when Saturn is in:
    - The sign before the Moon sign (12th from Moon)
    - The Moon sign itself (1st from Moon / Janma Sade Sati)
    - The sign after the Moon sign (2nd from Moon)

    Ashtam Shani is active when Saturn is in the 8th house from Moon sign.

    Args:
        moon_sign: Natal Moon sign (e.g. "Aries", "Scorpio")
        saturn_sign: Current transit sign of Saturn

    Returns:
        {has_sade_sati: bool, phase: str, description: str, severity: str, remedies: [str], ashtam_shani: bool, ashtam_effects: [str] (if applicable)}
    """
    if moon_sign not in ZODIAC_INDEX or saturn_sign not in ZODIAC_INDEX:
        return {
            "has_sade_sati": False,
            "phase": "none",
            "description": f"Invalid sign provided: moon_sign={moon_sign}, saturn_sign={saturn_sign}",
            "severity": "none",
            "remedies": [],
            "ashtam_shani": False,
        }

    moon_idx = ZODIAC_INDEX[moon_sign]
    saturn_idx = ZODIAC_INDEX[saturn_sign]

    # 12th from Moon (sign before)
    sign_before_idx = (moon_idx - 1) % 12
    # Same sign as Moon
    same_idx = moon_idx
    # 2nd from Moon (sign after)
    sign_after_idx = (moon_idx + 1) % 12
    # 8th from Moon (Ashtam Shani / Panauti)
    ashtam_idx = (moon_idx + 7) % 12

    # Check for Ashtam Shani first (more severe)
    ashtam_shani = saturn_idx == ashtam_idx
    if ashtam_shani:
        phase = "Ashtam Shani (8th from Moon)"
        severity = "extreme"
        description = (
            f"⚠️ ASHTAM SHANI ACTIVE — Saturn in {saturn_sign} "
            f"is transiting the 8th house from natal Moon in {moon_sign}. "
            "This is the most challenging Saturn transit (Panauti). "
            "Long-term ailments, accidents, wealth loss, and separation are possible. "
            "Full aspect on 2nd (finances), 5th (children), and 10th (career) houses."
        )
        ashtam_effects = [
            "Called Laghu Kalyani Dhayya along with 4th house transit",
            "Full aspect on 2nd, 5th and 10th house from Moon sign",
            "Possibility of long term ailments and accidents",
            "Fear of being insulted; pain from government servants",
            "Chance of change in work-sphere; business may suffer",
            "Wealth may diminish significantly",
            "Children may suffer pain; possibilities of separation from children",
            "Most challenging period among all Saturn transits"
        ]
    elif saturn_idx == sign_before_idx:
        phase = "Rising (12th from Moon)"
        severity = "medium"
        description = (
            f"Sade Sati ACTIVE — Rising phase. Saturn in {saturn_sign} "
            f"is transiting the 12th house from natal Moon in {moon_sign}. "
            "This phase brings financial pressures and health concerns. "
            "The beginning of the 7.5-year Saturn transit over the Moon."
        )
        ashtam_effects = []
    elif saturn_idx == same_idx:
        phase = "Peak (over Moon sign)"
        severity = "high"
        description = (
            f"Sade Sati ACTIVE — Peak phase. Saturn in {saturn_sign} "
            f"is directly transiting over natal Moon in {moon_sign}. "
            "This is the most intense phase — emotional turbulence, career challenges, "
            "and major life restructuring are common."
        )
        ashtam_effects = []
    elif saturn_idx == sign_after_idx:
        phase = "Setting (2nd from Moon)"
        severity = "medium"
        description = (
            f"Sade Sati ACTIVE — Setting phase. Saturn in {saturn_sign} "
            f"is transiting the 2nd house from natal Moon in {moon_sign}. "
            "This phase affects family, finances, and speech. "
            "The final stretch before Sade Sati ends."
        )
        ashtam_effects = []
    else:
        return {
            "has_sade_sati": False,
            "phase": "none",
            "description": (
                f"No Sade Sati. Saturn in {saturn_sign} is not within one sign "
                f"of natal Moon in {moon_sign}."
            ),
            "severity": "none",
            "remedies": [],
            "ashtam_shani": False,
        }

    remedies = [
        "Recite Shani Beej Mantra: 'Om Sham Shanaishcharaya Namah' 108 times on Saturdays.",
        "Light a sesame oil lamp under a Peepal tree on Saturday evenings.",
        "Donate black items (clothes, sesame, iron) on Saturdays.",
        "Wear a Blue Sapphire (Neelam) only after astrological consultation.",
        "Perform Shani Shanti Puja or Hanuman Puja regularly.",
        "Practice patience, discipline, and service — Saturn rewards hard work.",
    ]

    if ashtam_shani:
        # Add Ashtam-specific remedies
        remedies.extend([
            "Recite Mahamrityunjaya Mantra 108 times daily for protection.",
            "Perform regular Hanuman Puja for strength during this period.",
            "Practice strict discipline and austerity during this period.",
        ])

    result = {
        "has_sade_sati": True,
        "phase": phase,
        "description": description,
        "severity": severity,
        "remedies": remedies,
        "ashtam_shani": ashtam_shani,
    }

    if ashtam_shani:
        result["ashtam_effects"] = ashtam_effects

    return result


# ============================================================
# ADDITIONAL DOSHAS
# ============================================================

def check_pitra_dosha(planets: dict) -> dict:
    """
    Check for Pitra Dosha — Sun afflicted by Rahu/Ketu or Sun in 9th with malefic.

    Args:
        planets: Dict of planet data {name: {house, sign, ...}}
    """
    sun = planets.get("Sun", {})
    rahu = planets.get("Rahu", {})
    ketu = planets.get("Ketu", {})
    sun_house = sun.get("house", 0)
    rahu_house = rahu.get("house", 0)
    ketu_house = ketu.get("house", 0)

    has_dosha = False
    reasons = []

    # Sun conjunct Rahu or Ketu (same house)
    if sun_house == rahu_house and sun_house > 0:
        has_dosha = True
        reasons.append(f"Sun conjunct Rahu in house {sun_house}")
    if sun_house == ketu_house and sun_house > 0:
        has_dosha = True
        reasons.append(f"Sun conjunct Ketu in house {sun_house}")

    # Sun in 9th house with malefic aspect
    if sun_house == 9:
        for malefic in ["Mars", "Saturn", "Rahu", "Ketu"]:
            m = planets.get(malefic, {})
            if m.get("house", 0) == 9:
                has_dosha = True
                reasons.append(f"Sun with {malefic} in 9th house (house of father/dharma)")
                break

    if not has_dosha:
        return {
            "has_dosha": False,
            "severity": "none",
            "description": "No Pitra Dosha detected. Sun is free from Rahu/Ketu affliction.",
            "remedies": [],
        }

    return {
        "has_dosha": True,
        "severity": "medium",
        "description": (
            f"Pitra Dosha detected: {'; '.join(reasons)}. "
            "This indicates ancestral karmic debts affecting the native's fortune and paternal relationships."
        ),
        "remedies": [
            "Perform Pitra Dosh Nivaran Puja or Narayan Nagbali at Trimbakeshwar.",
            "Offer Tarpan to ancestors during Pitru Paksha.",
            "Donate food and clothes to Brahmins on Amavasya.",
            "Recite Surya Mantra and offer water to the Sun at sunrise.",
        ],
    }


def check_kemdrum_dosha(planets: dict) -> dict:
    """
    Check for Kemdrum Dosha — no planets in 2nd and 12th from Moon.

    Args:
        planets: Dict of planet data {name: {house, sign, ...}}
    """
    moon = planets.get("Moon", {})
    moon_house = moon.get("house", 0)
    if moon_house == 0:
        return {
            "has_dosha": False,
            "severity": "none",
            "description": "Moon house data not available.",
            "remedies": [],
        }

    # Houses 2nd and 12th from Moon
    house_2nd = ((moon_house - 1 + 1) % 12) + 1  # moon_house + 1, wrapped
    house_12th = ((moon_house - 1 - 1) % 12) + 1  # moon_house - 1, wrapped

    # Check if any planet (excluding Rahu/Ketu) is in those houses
    check_planets = ["Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    planets_in_2nd = [p for p in check_planets if planets.get(p, {}).get("house") == house_2nd]
    planets_in_12th = [p for p in check_planets if planets.get(p, {}).get("house") == house_12th]

    has_dosha = len(planets_in_2nd) == 0 and len(planets_in_12th) == 0

    if not has_dosha:
        return {
            "has_dosha": False,
            "severity": "none",
            "description": (
                f"No Kemdrum Dosha. Planets found near Moon: "
                f"2nd house ({house_2nd}): {', '.join(planets_in_2nd) or 'none'}, "
                f"12th house ({house_12th}): {', '.join(planets_in_12th) or 'none'}."
            ),
            "remedies": [],
        }

    return {
        "has_dosha": True,
        "severity": "high",
        "description": (
            f"Kemdrum Dosha detected. No planets in house {house_2nd} (2nd from Moon) "
            f"or house {house_12th} (12th from Moon). Moon is isolated, "
            "causing financial instability, loneliness, and mental distress."
        ),
        "remedies": [
            "Recite Chandra Beej Mantra: 'Om Shram Shreem Shroum Sah Chandraya Namah'.",
            "Wear a Pearl (Moti) gemstone after astrological consultation.",
            "Fast on Mondays and offer milk to Shiva Linga.",
            "Donate white items (rice, milk, white cloth) on Mondays.",
            "Worship Goddess Parvati for emotional stability.",
        ],
    }


# ============================================================
# YOGA DETECTION (Positive Combinations)
# ============================================================

def check_gajakesari_yoga(planets: dict) -> dict:
    """
    Gajakesari Yoga: Jupiter in kendra (1,4,7,10) from Moon.
    """
    moon = planets.get("Moon", {})
    jupiter = planets.get("Jupiter", {})
    moon_house = moon.get("house", 0)
    jupiter_house = jupiter.get("house", 0)

    if moon_house == 0 or jupiter_house == 0:
        return {"name": "Gajakesari Yoga", "present": False,
                "description": "Cannot determine — planet data missing.",
                "planets_involved": []}

    # Calculate house distance from Moon to Jupiter
    distance = ((jupiter_house - moon_house) % 12)
    # Kendra positions from Moon: 0 (same), 3 (4th), 6 (7th), 9 (10th)
    is_kendra = distance in {0, 3, 6, 9}

    if is_kendra:
        return {
            "name": "Gajakesari Yoga",
            "present": True,
            "description": (
                f"Jupiter in house {jupiter_house} is in kendra from Moon in house {moon_house}. "
                "This powerful yoga bestows wisdom, wealth, fame, and leadership qualities. "
                "The native commands respect and achieves high positions."
            ),
            "planets_involved": ["Moon", "Jupiter"],
        }
    return {
        "name": "Gajakesari Yoga",
        "present": False,
        "description": "Jupiter is not in kendra from Moon. Gajakesari Yoga is not formed.",
        "planets_involved": [],
    }


def check_budhaditya_yoga(planets: dict) -> dict:
    """
    Budhaditya Yoga: Sun and Mercury in the same house.
    """
    sun = planets.get("Sun", {})
    mercury = planets.get("Mercury", {})
    sun_house = sun.get("house", 0)
    mercury_house = mercury.get("house", 0)

    if sun_house > 0 and sun_house == mercury_house:
        return {
            "name": "Budhaditya Yoga",
            "present": True,
            "description": (
                f"Sun and Mercury conjunct in house {sun_house}. "
                "Budhaditya Yoga grants sharp intellect, eloquence, and analytical ability. "
                "The native excels in communication, education, and logical reasoning."
            ),
            "planets_involved": ["Sun", "Mercury"],
        }
    return {
        "name": "Budhaditya Yoga",
        "present": False,
        "description": "Sun and Mercury are not in the same house.",
        "planets_involved": [],
    }


def check_chandra_mangal_yoga(planets: dict) -> dict:
    """
    Chandra-Mangal Yoga: Moon and Mars in the same house.
    """
    moon = planets.get("Moon", {})
    mars = planets.get("Mars", {})
    moon_house = moon.get("house", 0)
    mars_house = mars.get("house", 0)

    if moon_house > 0 and moon_house == mars_house:
        return {
            "name": "Chandra-Mangal Yoga",
            "present": True,
            "description": (
                f"Moon and Mars conjunct in house {moon_house}. "
                "This yoga gives the native strong willpower, courage, and financial acumen. "
                "Excellent for business success and material prosperity."
            ),
            "planets_involved": ["Moon", "Mars"],
        }
    return {
        "name": "Chandra-Mangal Yoga",
        "present": False,
        "description": "Moon and Mars are not in the same house.",
        "planets_involved": [],
    }


def check_panch_mahapurusha(planets: dict) -> list:
    """
    Panch Mahapurusha Yogas: Mars/Mercury/Jupiter/Venus/Saturn in kendra AND in own/exalted sign.
    Returns list of yoga dicts for each that is present.
    """
    yoga_names = {
        "Mars": "Ruchaka",
        "Mercury": "Bhadra",
        "Jupiter": "Hamsa",
        "Venus": "Malavya",
        "Saturn": "Shasha",
    }
    yoga_descriptions = {
        "Mars": "Ruchaka Yoga grants valor, commanding personality, and military/leadership success.",
        "Mercury": "Bhadra Yoga grants intellectual brilliance, business acumen, and persuasive speech.",
        "Jupiter": "Hamsa Yoga grants spiritual wisdom, noble character, and high social status.",
        "Venus": "Malavya Yoga grants beauty, luxury, artistic talent, and a comfortable life.",
        "Saturn": "Shasha Yoga grants discipline, authority, organizational power, and longevity.",
    }

    results = []
    for planet_name in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        p = planets.get(planet_name, {})
        house = p.get("house", 0)
        sign = p.get("sign", "")

        in_kendra = house in KENDRA_HOUSES
        in_own = sign in OWN_SIGNS.get(planet_name, set())
        in_exalted = sign == EXALTATION_SIGNS.get(planet_name, "")
        present = in_kendra and (in_own or in_exalted)

        results.append({
            "name": f"{yoga_names[planet_name]} Yoga ({planet_name})",
            "present": present,
            "description": (
                f"{planet_name} in house {house} ({sign}) — "
                f"{'in kendra' if in_kendra else 'not in kendra'}, "
                f"{'own/exalted sign' if (in_own or in_exalted) else 'not in own/exalted sign'}. "
                + (yoga_descriptions[planet_name] if present else f"{yoga_names[planet_name]} Yoga is not formed.")
            ),
            "planets_involved": [planet_name] if present else [],
        })

    return results


def check_sun_in_own_sign(planets: dict) -> dict:
    """Check if Sun is in its own sign (Leo)."""
    sun = planets.get("Sun", {})
    if sun.get("sign") == "Leo":
        return {
            "name": "Surya in Swa Rashi (Sun in Own Sign)",
            "present": True,
            "description": f"Sun in its own sign Leo in house {sun.get('house')}. Grants authority, leadership qualities, government favors, and strong vitality. Native has commanding presence and administrative abilities.",
            "planets_involved": ["Sun"],
        }
    return {
        "name": "Surya in Swa Rashi (Sun in Own Sign)",
        "present": False,
        "description": "Sun is not in its own sign.",
        "planets_involved": [],
    }


def check_saturn_exalted(planets: dict) -> dict:
    """Check if Saturn is exalted (in Libra)."""
    saturn = planets.get("Saturn", {})
    if saturn.get("sign") == "Libra":
        return {
            "name": "Shani Uchcha (Saturn Exalted)",
            "present": True,
            "description": f"Saturn is exalted in Libra in house {saturn.get('house')}. Grants discipline, hard work, organizational abilities, and success through perseverance. Even without Shasha Yoga, this is a very favorable position for career and longevity.",
            "planets_involved": ["Saturn"],
        }
    return {
        "name": "Shani Uchcha (Saturn Exalted)",
        "present": False,
        "description": "Saturn is not exalted.",
        "planets_involved": [],
    }


def check_neecha_bhanga(planets: dict) -> dict:
    """
    Check for Neecha Bhanga Raj Yoga - cancellation of debilitation.
    If a planet is debilitated but its dispositor is in kendra from Moon or Lagna,
    or the debilitated planet is conjunct with/aspected by its dispositor.
    """
    neecha_planets = []
    debilitation_signs = {
        "Sun": "Libra",
        "Moon": "Scorpio",
        "Mars": "Cancer",
        "Mercury": "Pisces",
        "Jupiter": "Capricorn",
        "Venus": "Virgo",
        "Saturn": "Aries",
    }
    
    # Sign lords (dispositors)
    sign_lords = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
        "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
        "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
        "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
    }
    
    for planet_name, deb_sign in debilitation_signs.items():
        p = planets.get(planet_name, {})
        if p.get("sign") == deb_sign:
            # Planet is debilitated, check for cancellation
            deb_house = p.get("house", 0)
            dispositor_sign = deb_sign
            dispositor = sign_lords.get(dispositor_sign)
            
            if dispositor and dispositor in planets:
                disp_house = planets[dispositor].get("house", 0)
                moon_house = planets.get("Moon", {}).get("house", 0)
                
                # Check if dispositor is in kendra from debilitated planet, Moon, or Lagna
                kendra_from_deb = ((disp_house - deb_house) % 12) in [0, 3, 6, 9]
                kendra_from_moon = ((disp_house - moon_house) % 12) in [0, 3, 6, 9] if moon_house else False
                kendra_from_lagna = ((disp_house - 1) % 12) in [0, 3, 6, 9]  # Lagna = house 1

                if kendra_from_deb or kendra_from_moon or kendra_from_lagna:
                    neecha_planets.append({
                        "planet": planet_name,
                        "sign": deb_sign,
                        "house": deb_house,
                        "dispositor": dispositor,
                        "cancelled": True
                    })
    
    if neecha_planets:
        planet_names = [p["planet"] for p in neecha_planets]
        return {
            "name": "Neecha Bhanga Raj Yoga",
            "present": True,
            "description": f"Debilitation cancelled for: {', '.join(planet_names)}. The negative effects of debilitation are nullified, and the planet(s) can give excellent results like a king. Native overcomes early struggles and rises to prominence.",
            "planets_involved": planet_names,
        }
    
    return {
        "name": "Neecha Bhanga Raj Yoga",
        "present": False,
        "description": "No debilitated planets with cancellation found.",
        "planets_involved": [],
    }


# ============================================================
# NEECHA BHANGA VARIANTS — per-planet (Phaladeepika Adh. 7)
# ============================================================
# Per-planet Neechabhanga conditions (Phaladeepika Adh. 7 slokas 8–14):
#   For each debilitated planet, cancellation occurs when ANY of:
#   1. Lord of the debilitation sign is in kendra from lagna or Moon.
#   2. Lord of the exaltation sign of the debilitated planet is in kendra from lagna or Moon.
#   3. The planet that exalts IN the debilitation sign is in kendra from lagna or Moon.
#   4. The debilitated planet itself is in kendra from lagna or Moon.
_NBRY_PLANET_DATA = {
    # planet: (debil_sign, dispositor, exalt_sign_lord, exalts_in_debil_lord)
    "Sun":     ("Libra",     "Venus",   "Mars",    "Saturn"),   # Sun exalts in Aries (Mars); Saturn exalts in Libra
    "Moon":    ("Scorpio",   "Mars",    "Venus",   None),       # Moon exalts in Taurus (Venus); nothing exalts in Scorpio
    "Mars":    ("Cancer",    "Moon",    "Saturn",  "Jupiter"),  # Mars exalts in Capricorn (Saturn); Jupiter exalts in Cancer
    "Mercury": ("Pisces",    "Jupiter", "Mercury", "Venus"),    # Mercury exalts in Virgo (itself); Venus exalts in Pisces
    "Jupiter": ("Capricorn", "Saturn",  "Moon",    "Mars"),     # Jupiter exalts in Cancer (Moon); Mars exalts in Capricorn
    "Venus":   ("Virgo",     "Mercury", "Jupiter", "Mercury"),  # Venus exalts in Pisces (Jupiter); Mercury exalts in Virgo
    "Saturn":  ("Aries",     "Mars",    "Venus",   "Sun"),      # Saturn exalts in Libra (Venus); Sun exalts in Aries
}


def check_neecha_bhanga_variants(planets: dict, asc_sign: str) -> list:
    """
    Per-planet Neechabhanga Raj Yoga (Phaladeepika Adh. 7 slokas 8–14).

    For each debilitated planet checks 4 cancellation conditions and returns
    a detailed result with which specific condition(s) triggered the cancellation.

    Returns list of yoga dicts (one per debilitated planet with cancellation).
    """
    results = []

    moon_house = planets.get("Moon", {}).get("house", 0)
    lagna_house = 1  # whole-sign lagna

    def _in_kendra_from(planet_name: str, ref_house: int) -> bool:
        ph = planets.get(planet_name, {}).get("house", 0)
        if ph == 0 or ref_house == 0:
            return False
        return ((ph - ref_house) % 12) in {0, 3, 6, 9}

    def _planet_in_kendra_abs(planet_name: str) -> bool:
        """Kendra from lagna (house 1,4,7,10)."""
        return planets.get(planet_name, {}).get("house", 0) in KENDRA_HOUSES

    for planet, (debil_sign, dispositor, exalt_lord, exalts_in_debil) in _NBRY_PLANET_DATA.items():
        p_data = planets.get(planet, {})
        if p_data.get("sign") != debil_sign:
            continue  # not debilitated

        p_house = p_data.get("house", 0)
        conditions_met = []

        # Condition 1: Dispositor in kendra from lagna or Moon
        if dispositor:
            if _in_kendra_from(dispositor, lagna_house) or _in_kendra_from(dispositor, moon_house):
                loc = planets.get(dispositor, {}).get("house", "?")
                conditions_met.append(
                    f"Dispositor {dispositor} in kendra from {'lagna' if _in_kendra_from(dispositor, lagna_house) else 'Moon'} (H{loc})"
                )

        # Condition 2: Exaltation sign lord in kendra from lagna or Moon
        if exalt_lord and exalt_lord != dispositor:
            if _in_kendra_from(exalt_lord, lagna_house) or _in_kendra_from(exalt_lord, moon_house):
                loc = planets.get(exalt_lord, {}).get("house", "?")
                conditions_met.append(
                    f"Exaltation lord {exalt_lord} in kendra from {'lagna' if _in_kendra_from(exalt_lord, lagna_house) else 'Moon'} (H{loc})"
                )

        # Condition 3: Planet that exalts IN the debilitation sign is in kendra
        if exalts_in_debil and exalts_in_debil not in (dispositor, exalt_lord):
            if _in_kendra_from(exalts_in_debil, lagna_house) or _in_kendra_from(exalts_in_debil, moon_house):
                loc = planets.get(exalts_in_debil, {}).get("house", "?")
                conditions_met.append(
                    f"{exalts_in_debil} (exalts in {debil_sign}) in kendra (H{loc})"
                )

        # Condition 4: Debilitated planet itself in kendra from lagna or Moon
        if _in_kendra_from(planet, lagna_house) or _in_kendra_from(planet, moon_house):
            conditions_met.append(
                f"{planet} itself in kendra (H{p_house})"
            )

        if conditions_met:
            results.append({
                "name": f"Neecha Bhanga Raj Yoga ({planet})",
                "present": True,
                "description": (
                    f"{planet} is debilitated in {debil_sign} (H{p_house}) but cancellation applies — "
                    + "; ".join(conditions_met)
                    + ". The debilitation is cancelled; the planet rises to give results exceeding a strong planet."
                ),
                "description_hi": (
                    f"{planet} {debil_sign} (भाव {p_house}) में नीच है किन्तु भंग हो रहा है — "
                    + "; ".join(conditions_met)
                    + "। नीच-भंग से यह ग्रह उच्च ग्रह से भी उत्तम फल देता है।"
                ),
                "planets_involved": list({planet, dispositor, exalt_lord, exalts_in_debil} - {None}),
                "sloka_ref": "Phaladeepika Adh. 7 slokas 8–14",
                "category": "Raja Yoga (Neecha Bhanga)",
                "cancellation_conditions": conditions_met,
            })

    return results


# ============================================================
# Sign lords (dispositors) — needed for Raja Yoga, Dhana Yoga
# ============================================================
SIGN_LORDS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

TRIKONA_HOUSES = {1, 5, 9}
TRIK_HOUSES = {6, 8, 12}
BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}


def _h(planet_name: str, planets: dict) -> int:
    """Get house of a planet (0 if missing)."""
    return planets.get(planet_name, {}).get("house", 0)


def _sign(planet_name: str, planets: dict) -> str:
    """Get sign of a planet."""
    return planets.get(planet_name, {}).get("sign", "")


def _conjunct(p1: str, p2: str, planets: dict) -> bool:
    """Check if two planets are in the same house."""
    h1, h2 = _h(p1, planets), _h(p2, planets)
    return h1 > 0 and h1 == h2


def _house_lord(house_num: int, asc_sign: str) -> str:
    """Get lord of a house given ascendant sign."""
    asc_idx = ZODIAC_INDEX.get(asc_sign, 0)
    sign_on_house = ZODIAC_SIGNS[(asc_idx + house_num - 1) % 12]
    return SIGN_LORDS.get(sign_on_house, "")


# ============================================================
# NEW YOGAS
# ============================================================

def check_sunapha_yoga(planets: dict) -> dict:
    """Sunapha Yoga: Any planet (excl. Sun, Rahu, Ketu) in 2nd from Moon."""
    moon_h = _h("Moon", planets)
    if moon_h == 0:
        return {"name": "Sunapha Yoga", "present": False, "description": "Moon data missing.", "planets_involved": []}
    h2 = (moon_h % 12) + 1
    found = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if _h(p, planets) == h2]
    if found:
        return {"name": "Sunapha Yoga", "present": True,
                "description": f"{', '.join(found)} in 2nd from Moon (house {h2}). Grants self-earned wealth, intelligence, and good reputation.",
                "planets_involved": ["Moon"] + found}
    return {"name": "Sunapha Yoga", "present": False, "description": "No planets in 2nd from Moon.", "planets_involved": []}


def check_anapha_yoga(planets: dict) -> dict:
    """Anapha Yoga: Any planet (excl. Sun, Rahu, Ketu) in 12th from Moon."""
    moon_h = _h("Moon", planets)
    if moon_h == 0:
        return {"name": "Anapha Yoga", "present": False, "description": "Moon data missing.", "planets_involved": []}
    h12 = ((moon_h - 2) % 12) + 1
    found = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if _h(p, planets) == h12]
    if found:
        return {"name": "Anapha Yoga", "present": True,
                "description": f"{', '.join(found)} in 12th from Moon (house {h12}). Grants good health, comfort, and a pleasant personality.",
                "planets_involved": ["Moon"] + found}
    return {"name": "Anapha Yoga", "present": False, "description": "No planets in 12th from Moon.", "planets_involved": []}


def check_durudhara_yoga(planets: dict) -> dict:
    """Durudhara Yoga: Planets in both 2nd AND 12th from Moon."""
    moon_h = _h("Moon", planets)
    if moon_h == 0:
        return {"name": "Durudhara Yoga", "present": False, "description": "Moon data missing.", "planets_involved": []}
    h2 = (moon_h % 12) + 1
    h12 = ((moon_h - 2) % 12) + 1
    check = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    in_2 = [p for p in check if _h(p, planets) == h2]
    in_12 = [p for p in check if _h(p, planets) == h12]
    if in_2 and in_12:
        return {"name": "Durudhara Yoga", "present": True,
                "description": f"Planets in 2nd ({', '.join(in_2)}) and 12th ({', '.join(in_12)}) from Moon. Grants wealth, vehicles, generosity, and a comfortable life.",
                "planets_involved": ["Moon"] + in_2 + in_12}
    return {"name": "Durudhara Yoga", "present": False, "description": "Planets not on both sides of Moon.", "planets_involved": []}


def check_shakata_yoga(planets: dict) -> dict:
    """Shakata Yoga: Moon in 6th or 8th from Jupiter — inauspicious."""
    moon_h, jup_h = _h("Moon", planets), _h("Jupiter", planets)
    if moon_h == 0 or jup_h == 0:
        return {"name": "Shakata Yoga", "present": False, "description": "Data missing.", "planets_involved": []}
    dist = (moon_h - jup_h) % 12
    if dist in {5, 7}:  # 6th or 8th
        return {"name": "Shakata Yoga", "present": True,
                "description": f"Moon in {'6th' if dist == 5 else '8th'} from Jupiter. Causes fluctuating fortune — periods of prosperity followed by sudden setbacks.",
                "planets_involved": ["Moon", "Jupiter"]}
    return {"name": "Shakata Yoga", "present": False, "description": "Moon not in 6th/8th from Jupiter.", "planets_involved": []}


def check_adhi_yoga(planets: dict) -> dict:
    """Adhi Yoga: Benefics in 6th, 7th, 8th from Moon."""
    moon_h = _h("Moon", planets)
    if moon_h == 0:
        return {"name": "Adhi Yoga", "present": False, "description": "Moon data missing.", "planets_involved": []}
    h6 = ((moon_h + 4) % 12) + 1
    h7 = ((moon_h + 5) % 12) + 1
    h8 = ((moon_h + 6) % 12) + 1
    found = []
    for p in ["Jupiter", "Venus", "Mercury"]:
        ph = _h(p, planets)
        if ph in {h6, h7, h8}:
            found.append(p)
    if found:
        return {"name": "Adhi Yoga", "present": True,
                "description": f"{', '.join(found)} in 6th/7th/8th from Moon. Grants power, authority, leadership, and command over others.",
                "planets_involved": ["Moon"] + found}
    return {"name": "Adhi Yoga", "present": False, "description": "No benefics in 6/7/8 from Moon.", "planets_involved": []}


def check_amala_yoga(planets: dict) -> dict:
    """Amala Yoga: A natural benefic in 10th from Lagna or 10th from Moon."""
    found_lagna = []
    found_moon = []
    moon_house = _h("Moon", planets)
    # 10th from Lagna = absolute house 10 (Lagna is always house 1)
    house_10_lagna = 10
    # 10th from Moon
    house_10_moon = ((moon_house + 9 - 1) % 12) + 1 if moon_house else 0
    for p in ["Jupiter", "Venus", "Mercury", "Moon"]:
        ph = _h(p, planets)
        if ph == house_10_lagna:
            found_lagna.append(p)
        if house_10_moon and ph == house_10_moon:
            found_moon.append(p)
    found = list(dict.fromkeys(found_lagna + found_moon))  # dedupe, preserve order
    if found:
        sources = []
        if found_lagna:
            sources.append(f"{', '.join(found_lagna)} in 10th from Lagna")
        if found_moon:
            sources.append(f"{', '.join(found_moon)} in 10th from Moon (house {house_10_moon})")
        desc = "; ".join(sources) + ". Grants spotless reputation, fame, and virtuous conduct in career."
        return {"name": "Amala Yoga", "present": True,
                "description": desc,
                "planets_involved": found}
    return {"name": "Amala Yoga", "present": False, "description": "No benefic in 10th from Lagna or Moon.", "planets_involved": []}


def check_vesi_yoga(planets: dict) -> dict:
    """Vesi Yoga: Any planet (excl. Moon, Rahu, Ketu) in 2nd from Sun."""
    sun_h = _h("Sun", planets)
    if sun_h == 0:
        return {"name": "Vesi Yoga", "present": False, "description": "Sun data missing.", "planets_involved": []}
    h2 = (sun_h % 12) + 1
    found = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if _h(p, planets) == h2]
    if found:
        return {"name": "Vesi Yoga", "present": True,
                "description": f"{', '.join(found)} in 2nd from Sun (house {h2}). Grants wealth, status, and truthful nature.",
                "planets_involved": ["Sun"] + found}
    return {"name": "Vesi Yoga", "present": False, "description": "No planets in 2nd from Sun.", "planets_involved": []}


def check_vasi_yoga(planets: dict) -> dict:
    """Vasi Yoga: Any planet (excl. Moon, Rahu, Ketu) in 12th from Sun."""
    sun_h = _h("Sun", planets)
    if sun_h == 0:
        return {"name": "Vasi Yoga", "present": False, "description": "Sun data missing.", "planets_involved": []}
    h12 = ((sun_h - 2) % 12) + 1
    found = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if _h(p, planets) == h12]
    if found:
        return {"name": "Vasi Yoga", "present": True,
                "description": f"{', '.join(found)} in 12th from Sun (house {h12}). Grants generous nature, prosperity, and charitable disposition.",
                "planets_involved": ["Sun"] + found}
    return {"name": "Vasi Yoga", "present": False, "description": "No planets in 12th from Sun.", "planets_involved": []}


def check_ubhayachari_yoga(planets: dict) -> dict:
    """Ubhayachari Yoga: Planets in both 2nd AND 12th from Sun."""
    sun_h = _h("Sun", planets)
    if sun_h == 0:
        return {"name": "Ubhayachari Yoga", "present": False, "description": "Sun data missing.", "planets_involved": []}
    h2 = (sun_h % 12) + 1
    h12 = ((sun_h - 2) % 12) + 1
    check = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    in_2 = [p for p in check if _h(p, planets) == h2]
    in_12 = [p for p in check if _h(p, planets) == h12]
    if in_2 and in_12:
        return {"name": "Ubhayachari Yoga", "present": True,
                "description": f"Planets in 2nd ({', '.join(in_2)}) and 12th ({', '.join(in_12)}) from Sun. Grants eloquence, wealth, kingly status, and influential personality.",
                "planets_involved": ["Sun"] + in_2 + in_12}
    return {"name": "Ubhayachari Yoga", "present": False, "description": "Planets not on both sides of Sun.", "planets_involved": []}


def check_viparita_raja_yoga(planets: dict, asc_sign: str) -> list:
    """Viparita Raja Yoga: Lord of 6th in 8th/12th, lord of 8th in 6th/12th, lord of 12th in 6th/8th."""
    results = []
    if not asc_sign:
        return results
    trik_map = {6: {8, 12}, 8: {6, 12}, 12: {6, 8}}
    names = {6: "Harsha", 8: "Sarala", 12: "Vimala"}
    for house_num, target_houses in trik_map.items():
        lord = _house_lord(house_num, asc_sign)
        if lord:
            lord_h = _h(lord, planets)
            if lord_h in target_houses:
                results.append({
                    "name": f"{names[house_num]} Viparita Raja Yoga",
                    "present": True,
                    "description": f"Lord of {house_num}th house ({lord}) placed in {lord_h}th house. Grants success through adversity, defeat of enemies, and unexpected gains.",
                    "planets_involved": [lord],
                })
    return results


def check_dhana_yoga(planets: dict, asc_sign: str) -> dict:
    """Dhana Yoga: Lords of 2nd and 11th conjunct, or lords of 5th and 9th conjunct."""
    if not asc_sign:
        return {"name": "Dhana Yoga", "present": False, "description": "Ascendant data missing.", "planets_involved": []}
    lord2 = _house_lord(2, asc_sign)
    lord5 = _house_lord(5, asc_sign)
    lord9 = _house_lord(9, asc_sign)
    lord11 = _house_lord(11, asc_sign)
    combos = [
        (lord2, lord11, "2nd and 11th"),
        (lord5, lord9, "5th and 9th"),
        (lord2, lord5, "2nd and 5th"),
        (lord2, lord9, "2nd and 9th"),
    ]
    for la, lb, label in combos:
        if la and lb and la != lb and _conjunct(la, lb, planets):
            return {"name": "Dhana Yoga", "present": True,
                    "description": f"Lords of {label} houses ({la} and {lb}) conjunct in house {_h(la, planets)}. Grants significant wealth and financial prosperity.",
                    "planets_involved": [la, lb]}
    # Also: Jupiter in 2, 5, 9, or 11
    jup_h = _h("Jupiter", planets)
    if jup_h in {2, 5, 9, 11}:
        return {"name": "Dhana Yoga", "present": True,
                "description": f"Jupiter in house {jup_h} — a wealth-giving position. Grants financial stability and growth through righteous means.",
                "planets_involved": ["Jupiter"]}
    return {"name": "Dhana Yoga", "present": False, "description": "No Dhana Yoga combinations found.", "planets_involved": []}


def check_dhana_yogas(planets: dict, asc_sign: str) -> list:
    """
    Classical Dhana Yogas — up to 30 combinations from Phaladeepika, BPHS, and Jataka Parijata.
    Returns a list of detected yoga dicts, one per combination found.
    """
    if not asc_sign:
        return []
    results = []

    def _yoga(name, desc, involved):
        return {"name": name, "present": True, "description": desc, "planets_involved": involved,
                "sloka_ref": "Phaladeepika Adh. 11"}

    # Wealth house lords
    lord1  = _house_lord(1,  asc_sign)
    lord2  = _house_lord(2,  asc_sign)
    lord5  = _house_lord(5,  asc_sign)
    lord9  = _house_lord(9,  asc_sign)
    lord11 = _house_lord(11, asc_sign)
    lord4  = _house_lord(4,  asc_sign)
    lord7  = _house_lord(7,  asc_sign)

    def _conj(a, b):
        return a and b and a != b and _conjunct(a, b, planets)

    def _in_kendra_trikona(p):
        return _h(p, planets) in (KENDRA_HOUSES | TRIKONA_HOUSES) if p else False

    def _strong(p):
        """Planet is strong: in own sign, exalted, or in kendra/trikona."""
        if not p:
            return False
        s = _sign(p, planets)
        return (s in OWN_SIGNS.get(p, set())
                or s == EXALTATION_SIGNS.get(p, "")
                or _in_kendra_trikona(p))

    def _in_house(p, h):
        return _h(p, planets) == h if p else False

    # ── Lord pairs: conjunction combinations ──────────────────────────────────
    pairs_wealth = [
        (lord2, lord11, "2nd and 11th lords",   "Primary Dhana Yoga"),
        (lord5, lord9,  "5th and 9th lords",     "Lakshmi-Dhana Yoga"),
        (lord2, lord5,  "2nd and 5th lords",     "Dhana Yoga"),
        (lord2, lord9,  "2nd and 9th lords",     "Bhagya-Dhana Yoga"),
        (lord1, lord2,  "1st and 2nd lords",     "Svamsha-Dhana Yoga"),
        (lord1, lord5,  "1st and 5th lords",     "Putra-Dhana Yoga"),
        (lord1, lord9,  "1st and 9th lords",     "Bhagya-Lagna Yoga"),
        (lord1, lord11, "1st and 11th lords",    "Labha-Lagna Yoga"),
        (lord5, lord11, "5th and 11th lords",    "Putra-Labha Dhana Yoga"),
        (lord9, lord11, "9th and 11th lords",    "Dharma-Labha Dhana Yoga"),
        (lord2, lord7,  "2nd and 7th lords",     "Kalatra-Dhana Yoga"),
        (lord4, lord9,  "4th and 9th lords",     "Sukha-Bhagya Dhana Yoga"),
    ]
    for la, lb, label, name in pairs_wealth:
        if _conj(la, lb):
            h = _h(la, planets)
            results.append(_yoga(name,
                f"Lords of {label} ({la} and {lb}) conjunct in house {h}. "
                f"Grants significant wealth and financial prosperity through the merger of wealth-house significations.",
                [la, lb]))

    # ── Lords of wealth houses placed in each other's houses ──────────────────
    if lord2 and lord11 and _in_house(lord2, 11):
        results.append(_yoga("Dhana Yoga (2L in 11th)",
            f"2nd lord {lord2} placed in 11th house — wealth lord in gains house. Strong accumulation through earnings and income.",
            [lord2]))
    if lord2 and lord11 and _in_house(lord11, 2):
        results.append(_yoga("Dhana Yoga (11L in 2nd)",
            f"11th lord {lord11} placed in 2nd house — gains lord strengthening the treasury. Wealth from multiple income sources.",
            [lord11]))
    if lord5 and _in_house(lord5, 9):
        results.append(_yoga("Dharma-Putra Dhana Yoga",
            f"5th lord {lord5} in 9th house — creative intelligence meets fortune. Wealth through speculation, children, or righteous actions.",
            [lord5]))
    if lord9 and _in_house(lord9, 5):
        results.append(_yoga("Bhagya-Putra Dhana Yoga",
            f"9th lord {lord9} in 5th house — fortune lord in the house of intelligence. Wealth through divine grace and creative enterprise.",
            [lord9]))
    if lord1 and _in_house(lord1, 11):
        results.append(_yoga("Lagna-Labha Dhana Yoga",
            f"Lagna lord {lord1} placed in 11th house of gains. The native's personal initiative directly creates income and profit.",
            [lord1]))

    # ── Jupiter-based Dhana Yogas ──────────────────────────────────────────────
    jup_h = _h("Jupiter", planets)
    if jup_h in {2, 5, 9, 11}:
        results.append(_yoga("Guru-Dhana Yoga",
            f"Jupiter in house {jup_h} — the planet of wealth and wisdom in a natural wealth-giving house. "
            f"Grants financial stability and growth through righteous, lawful, and dharmic means.",
            ["Jupiter"]))
    if _strong("Jupiter") and _in_kendra_trikona("Jupiter"):
        results.append(_yoga("Brihat-Guru Dhana Yoga",
            f"Jupiter strong (exalted/own sign) in kendra or trikona. Exceptional dharmic wealth; the native becomes a pillar of prosperity for the family.",
            ["Jupiter"]))

    # ── Venus-based ───────────────────────────────────────────────────────────
    ven_h = _h("Venus", planets)
    if ven_h in {2, 7, 11}:
        results.append(_yoga("Shukra-Dhana Yoga",
            f"Venus in house {ven_h} — the planet of luxury and refinement in a wealth-sustaining house. "
            f"Wealth through arts, beauty, relationships, and pleasurable enterprise.",
            ["Venus"]))

    # ── Moon-Jupiter (Gaja-Kesari as Dhana Yoga) ─────────────────────────────
    if _conj("Moon", "Jupiter"):
        h = _h("Moon", planets)
        results.append(_yoga("Gaja-Kesari Dhana Yoga",
            f"Moon and Jupiter conjunct in house {h} — Gaja-Kesari formation also creates wealth, as the "
            f"conjunction of the Moon's nurturing with Jupiter's expansion generates abundance and prosperity.",
            ["Moon", "Jupiter"]))
    elif jup_h in KENDRA_HOUSES and _h("Moon", planets) > 0:
        results.append(_yoga("Gaja-Kesari Dhana Yoga",
            f"Jupiter in kendra from Lagna — Gaja-Kesari Yoga grants wealth, fame, and long-term prosperity through wisdom and social standing.",
            ["Jupiter", "Moon"]))

    # ── Moon-Venus ────────────────────────────────────────────────────────────
    if _conj("Moon", "Venus"):
        h = _h("Moon", planets)
        results.append(_yoga("Chandra-Shukra Dhana Yoga",
            f"Moon and Venus conjunct in house {h}. Grants wealth through commerce, aesthetic goods, luxury trade, and female-dominated markets.",
            ["Moon", "Venus"]))

    # ── Sun in 11th ───────────────────────────────────────────────────────────
    if _h("Sun", planets) == 11:
        results.append(_yoga("Surya-Labha Yoga",
            "Sun in 11th house — the solar force in the house of gains. Wealth through government, administration, gold trade, or paternal inheritance. Steady income from authority positions.",
            ["Sun"]))

    # ── Saturn in 11th ────────────────────────────────────────────────────────
    if _h("Saturn", planets) == 11:
        results.append(_yoga("Shani-Labha Yoga",
            "Saturn in 11th house — the karmic accumulator in the house of gains. Slow but steady wealth through service, labor, real estate, iron, or oil industries. Increases with age.",
            ["Saturn"]))

    # ── Mercury in 2nd or 11th (Budha-Dhana) ─────────────────────────────────
    if _h("Mercury", planets) in {2, 11}:
        h = _h("Mercury", planets)
        results.append(_yoga("Budha-Dhana Yoga",
            f"Mercury in house {h} — planet of commerce and intellect in a wealth house. Wealth through trade, communication, writing, finance, or information services.",
            ["Mercury"]))

    # ── All 5 wealth lords (1,2,5,9,11) in kendra/trikona ────────────────────
    wealth_lords = [l for l in [lord1, lord2, lord5, lord9, lord11] if l and _in_kendra_trikona(l)]
    if len(wealth_lords) >= 4:
        results.append(_yoga("Pancha-Dhana Yoga",
            f"Four or more wealth-house lords ({', '.join(wealth_lords)}) placed in kendra or trikona. "
            f"Extraordinary and multi-sourced wealth; the native becomes a great accumulator of prosperity.",
            wealth_lords))

    # ── 2nd lord exalted or in own sign ──────────────────────────────────────
    if lord2 and _strong(lord2) and _in_kendra_trikona(lord2):
        results.append(_yoga("Dhanesh-Bala Yoga",
            f"2nd lord {lord2} strong (exalted/own sign) in kendra or trikona. "
            f"The lord of the treasury is at peak power, ensuring robust and growing financial resources.",
            [lord2]))

    # ── 11th lord exalted or in own sign ─────────────────────────────────────
    if lord11 and _strong(lord11):
        results.append(_yoga("Labhesh-Bala Yoga",
            f"11th lord {lord11} strong (exalted/own sign). "
            f"The planet of gains is at full strength — income, profits, and fulfillment of desires flow naturally.",
            [lord11]))

    return results


def check_raja_yoga(planets: dict, asc_sign: str) -> dict:
    """Parashari Raja Yoga: Lord of any kendra conjunct lord of any trikona."""
    if not asc_sign:
        return {"name": "Parashari Raja Yoga", "present": False, "description": "Ascendant data missing.", "planets_involved": []}
    kendra_lords = {_house_lord(h, asc_sign) for h in KENDRA_HOUSES} - {""}
    trikona_lords = {_house_lord(h, asc_sign) for h in TRIKONA_HOUSES} - {""}
    for kl in kendra_lords:
        for tl in trikona_lords:
            if kl != tl and _conjunct(kl, tl, planets):
                return {"name": "Parashari Raja Yoga", "present": True,
                        "description": f"Kendra lord ({kl}) conjunct trikona lord ({tl}) in house {_h(kl, planets)}. Grants power, authority, fame, and high position in life.",
                        "planets_involved": [kl, tl]}
            # Also check mutual kendra placement
            if kl != tl:
                dist = (_h(kl, planets) - _h(tl, planets)) % 12
                if dist in {0, 3, 6, 9} and _h(kl, planets) > 0:
                    return {"name": "Parashari Raja Yoga", "present": True,
                            "description": f"Kendra lord ({kl}, H{_h(kl, planets)}) and trikona lord ({tl}, H{_h(tl, planets)}) in mutual kendra. Grants power and high position.",
                            "planets_involved": [kl, tl]}
    return {"name": "Parashari Raja Yoga", "present": False, "description": "No kendra-trikona lord association found.", "planets_involved": []}


def check_lakshmi_yoga(planets: dict, asc_sign: str) -> dict:
    """Lakshmi Yoga: Lord of 9th strong (own/exalted) and in kendra or trikona."""
    if not asc_sign:
        return {"name": "Lakshmi Yoga", "present": False, "description": "Ascendant data missing.", "planets_involved": []}
    lord9 = _house_lord(9, asc_sign)
    if not lord9:
        return {"name": "Lakshmi Yoga", "present": False, "description": "Cannot determine 9th lord.", "planets_involved": []}
    lord9_sign = _sign(lord9, planets)
    lord9_house = _h(lord9, planets)
    in_own = lord9_sign in OWN_SIGNS.get(lord9, set())
    in_exalted = lord9_sign == EXALTATION_SIGNS.get(lord9, "")
    in_good_house = lord9_house in (KENDRA_HOUSES | TRIKONA_HOUSES)
    if (in_own or in_exalted) and in_good_house:
        return {"name": "Lakshmi Yoga", "present": True,
                "description": f"9th lord {lord9} is {'exalted' if in_exalted else 'in own sign'} in house {lord9_house}. Grants immense wealth, fortune, luxury, and divine blessings.",
                "planets_involved": [lord9]}
    return {"name": "Lakshmi Yoga", "present": False, "description": "9th lord not strong in kendra/trikona.", "planets_involved": []}


def check_saraswati_yoga(planets: dict) -> dict:
    """Saraswati Yoga: Jupiter, Venus, Mercury all in kendra, trikona, or 2nd house."""
    good = KENDRA_HOUSES | TRIKONA_HOUSES | {2}
    all_in = all(_h(p, planets) in good for p in ["Jupiter", "Venus", "Mercury"])
    if all_in:
        return {"name": "Saraswati Yoga", "present": True,
                "description": f"Jupiter (H{_h('Jupiter', planets)}), Venus (H{_h('Venus', planets)}), Mercury (H{_h('Mercury', planets)}) all in kendra/trikona/2nd house. Grants exceptional learning, wisdom, artistic talent, and mastery of scriptures.",
                "planets_involved": ["Jupiter", "Venus", "Mercury"]}
    return {"name": "Saraswati Yoga", "present": False, "description": "Jupiter, Venus, Mercury not all in favorable houses.", "planets_involved": []}


def check_danda_yoga(planets: dict) -> dict:
    """Danda Yoga: All planets in 10th, 11th, and 12th houses only (rod-shaped distribution)."""
    check_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    houses = {_h(p, planets) for p in check_planets if _h(p, planets) > 0}
    if houses and houses.issubset({10, 11, 12}):
        return {"name": "Danda Yoga", "present": True,
                "description": "All planets concentrated in houses 10, 11, 12 — rod-shaped distribution. Can indicate a life of service, authority, but also potential for isolation or rigidity.",
                "planets_involved": check_planets}
    return {"name": "Danda Yoga", "present": False, "description": "Planets not concentrated in 10/11/12.", "planets_involved": []}


# ============================================================
# ADH. 6 YOGAS — Items 7, 8, 9
# ============================================================

# Helpers used by the new functions
_DUAL_SIGNS = {"Gemini", "Virgo", "Sagittarius", "Pisces"}

_NATURAL_FRIENDS = {
    "Sun":     {"Jupiter", "Mars", "Moon"},
    "Moon":    {"Sun", "Mercury"},
    "Mars":    {"Sun", "Moon", "Jupiter"},
    "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"},
    "Venus":   {"Mercury", "Saturn"},
    "Saturn":  {"Mercury", "Venus"},
}

_PLANET_OWN_SIGNS = {
    "Sun":     {"Leo"},
    "Moon":    {"Cancer"},
    "Mars":    {"Aries", "Scorpio"},
    "Mercury": {"Gemini", "Virgo"},
    "Jupiter": {"Sagittarius", "Pisces"},
    "Venus":   {"Taurus", "Libra"},
    "Saturn":  {"Capricorn", "Aquarius"},
}

_NATURAL_MALEFICS_ADH6 = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
_NATURAL_BENEFICS_ADH6 = {"Jupiter", "Venus", "Moon", "Mercury"}

_CLASSICAL_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


# ── Item 7 ────────────────────────────────────────────────────

def check_chimana_yoga(planets: dict) -> dict:
    """Chimana Yoga: Benefic planets occupy ALL four kendra houses (1, 4, 7, 10)."""
    kendra_list = [1, 4, 7, 10]
    benefic_planets = ["Jupiter", "Venus", "Moon", "Mercury"]
    covered = {}
    for p in benefic_planets:
        ph = _h(p, planets)
        if ph in kendra_list:
            covered[ph] = covered.get(ph, []) + [p]
    if set(covered.keys()) == set(kendra_list):
        involved = [p for plist in covered.values() for p in plist]
        detail = "; ".join(f"H{k}: {', '.join(v)}" for k, v in sorted(covered.items()))
        return {
            "name": "Chimana Yoga",
            "present": True,
            "description": (
                f"Benefic planets in all four kendras — {detail}. "
                "Grants wealth, fame, royal patronage, and abundant progeny."
            ),
            "description_hi": "चार केन्द्र भावों में शुभ ग्रह — यश, सम्पत्ति और राजकीय सम्मान।",
            "planets_involved": involved,
            "sloka_ref": "Phaladeepika Adh. 6 sloka 17",
        }
    return {
        "name": "Chimana Yoga",
        "present": False,
        "description": "Benefics do not occupy all four kendra houses simultaneously.",
        "description_hi": "चार केन्द्र भावों में शुभ ग्रह नहीं हैं।",
        "planets_involved": [],
        "sloka_ref": "Phaladeepika Adh. 6 sloka 17",
    }


def check_surya_yoga(planets: dict) -> dict:
    """Surya Yoga: Sun in 10th house in own sign (Leo) or exalted (Aries), no malefic conjunction."""
    sun_h = _h("Sun", planets)
    sun_sign = _sign("Sun", planets)
    if sun_h != 10:
        return {
            "name": "Surya Yoga",
            "present": False,
            "description": "Sun not in 10th house.",
            "description_hi": "सूर्य दशम भाव में नहीं है।",
            "planets_involved": [],
            "sloka_ref": "Phaladeepika Adh. 6 sloka 19",
        }
    in_own = sun_sign == "Leo"
    in_exalt = sun_sign == "Aries"
    if not (in_own or in_exalt):
        return {
            "name": "Surya Yoga",
            "present": False,
            "description": "Sun in 10th but not in own sign (Leo) or exaltation (Aries).",
            "description_hi": "सूर्य दशम भाव में है, किन्तु स्वराशि/उच्च में नहीं।",
            "planets_involved": [],
            "sloka_ref": "Phaladeepika Adh. 6 sloka 19",
        }
    malefic_conj = [p for p in ["Mars", "Saturn", "Rahu", "Ketu"] if _h(p, planets) == 10]
    if malefic_conj:
        return {
            "name": "Surya Yoga",
            "present": False,
            "description": (
                f"Sun in 10th in {'own sign Leo' if in_own else 'exaltation Aries'} but "
                f"afflicted by malefic conjunction: {', '.join(malefic_conj)}."
            ),
            "description_hi": "सूर्य दशम में शुभ है, किन्तु पापी ग्रह साथ होने से योग भंग।",
            "planets_involved": ["Sun"] + malefic_conj,
            "sloka_ref": "Phaladeepika Adh. 6 sloka 19",
        }
    label = "own sign Leo" if in_own else "exaltation Aries"
    return {
        "name": "Surya Yoga",
        "present": True,
        "description": (
            f"Sun in 10th house in {label}, unafflicted by malefics. "
            "Grants high authority, royal honors, government service, and fame in profession."
        ),
        "description_hi": "सूर्य दशम भाव में स्वराशि/उच्च — उच्च पद, राजकीय सम्मान, व्यावसायिक यश।",
        "planets_involved": ["Sun"],
        "sloka_ref": "Phaladeepika Adh. 6 sloka 19",
    }


def check_jalatha_yoga(planets: dict) -> dict:
    """Jalatha Yoga: All 7 classical planets placed in dual (Dvisvabhava) signs."""
    missing = [p for p in _CLASSICAL_PLANETS if _h(p, planets) == 0]
    if missing:
        return {
            "name": "Jalatha Yoga",
            "present": False,
            "description": f"Planet data missing for: {', '.join(missing)}.",
            "description_hi": "ग्रह डेटा अनुपलब्ध।",
            "planets_involved": [],
            "sloka_ref": "Phaladeepika Adh. 6 sloka 21",
        }
    not_dual = [p for p in _CLASSICAL_PLANETS if _sign(p, planets) not in _DUAL_SIGNS]
    if not not_dual:
        return {
            "name": "Jalatha Yoga",
            "present": True,
            "description": (
                "All 7 classical planets are in dual signs (Gemini, Virgo, Sagittarius, Pisces). "
                "Grants prosperity, good learning, dual income sources, and success in commerce."
            ),
            "description_hi": "सभी सात ग्रह द्विस्वभाव राशियों में — समृद्धि, व्यापार में सफलता।",
            "planets_involved": _CLASSICAL_PLANETS[:],
            "sloka_ref": "Phaladeepika Adh. 6 sloka 21",
        }
    return {
        "name": "Jalatha Yoga",
        "present": False,
        "description": f"Not all 7 planets in dual signs. Outside dual signs: {', '.join(not_dual)}.",
        "description_hi": "सभी ग्रह द्विस्वभाव राशियों में नहीं हैं।",
        "planets_involved": [],
        "sloka_ref": "Phaladeepika Adh. 6 sloka 21",
    }


def check_chattra_yoga(planets: dict) -> dict:
    """Chattra Yoga: All 7 classical planets exclusively in houses 1-7."""
    missing = [p for p in _CLASSICAL_PLANETS if _h(p, planets) == 0]
    if missing:
        return {
            "name": "Chattra Yoga",
            "present": False,
            "description": f"Planet data missing for: {', '.join(missing)}.",
            "description_hi": "ग्रह डेटा अनुपलब्ध।",
            "planets_involved": [],
            "sloka_ref": "Phaladeepika Adh. 6 sloka 23",
        }
    outside = [p for p in _CLASSICAL_PLANETS if _h(p, planets) > 7]
    if not outside:
        return {
            "name": "Chattra Yoga",
            "present": True,
            "description": (
                "All 7 classical planets occupy houses 1-7 (first hemisphere) — umbrella/parasol shape. "
                "Grants protection, shelter, leadership, and support from the government."
            ),
            "description_hi": "सभी ग्रह प्रथम सात भावों में — संरक्षण, नेतृत्व, सरकारी सहयोग।",
            "planets_involved": _CLASSICAL_PLANETS[:],
            "sloka_ref": "Phaladeepika Adh. 6 sloka 23",
        }
    return {
        "name": "Chattra Yoga",
        "present": False,
        "description": f"Planets outside houses 1-7: {', '.join(outside)}.",
        "description_hi": "सभी ग्रह प्रथम सात भावों में नहीं हैं।",
        "planets_involved": [],
        "sloka_ref": "Phaladeepika Adh. 6 sloka 23",
    }


def check_apta_yoga(planets: dict) -> dict:
    """Apta Yoga: 3 or more planets in the sign of their natural friend."""
    in_friend_sign = []
    for planet in _CLASSICAL_PLANETS:
        ph = _h(planet, planets)
        if ph == 0:
            continue
        ps = _sign(planet, planets)
        if not ps:
            continue
        sign_owner = next(
            (owner for owner, signs in _PLANET_OWN_SIGNS.items() if ps in signs),
            None,
        )
        if sign_owner and sign_owner != planet and sign_owner in _NATURAL_FRIENDS.get(planet, set()):
            in_friend_sign.append(planet)
    if len(in_friend_sign) >= 3:
        return {
            "name": "Apta Yoga",
            "present": True,
            "description": (
                f"{', '.join(in_friend_sign)} occupy the sign of their natural friend. "
                "Grants fulfillment of desires, support from allies, and social respect."
            ),
            "description_hi": "तीन या अधिक ग्रह मित्र राशि में — इच्छापूर्ति, सामाजिक प्रतिष्ठा।",
            "planets_involved": in_friend_sign,
            "sloka_ref": "Phaladeepika Adh. 6 sloka 25",
        }
    return {
        "name": "Apta Yoga",
        "present": False,
        "description": (
            f"Only {len(in_friend_sign)} planet(s) in friend's sign "
            f"({', '.join(in_friend_sign) if in_friend_sign else 'none'}); need 3 or more."
        ),
        "description_hi": "मित्र राशि में तीन से कम ग्रह — अप्त योग नहीं।",
        "planets_involved": in_friend_sign,
        "sloka_ref": "Phaladeepika Adh. 6 sloka 25",
    }


def check_rama_yoga(planets: dict) -> dict:
    """Rama Yoga: Venus in own sign (Taurus/Libra) AND in a kendra, AND Jupiter aspects or is in kendra."""
    ven_h = _h("Venus", planets)
    ven_sign = _sign("Venus", planets)
    in_own = ven_sign in {"Taurus", "Libra"}
    in_kendra = ven_h in KENDRA_HOUSES
    if not (in_own and in_kendra):
        return {
            "name": "Rama Yoga",
            "present": False,
            "description": "Venus must be in own sign (Taurus/Libra) and in a kendra house.",
            "description_hi": "शुक्र स्वराशि और केन्द्र में नहीं — राम योग नहीं।",
            "planets_involved": [],
            "sloka_ref": "Phaladeepika Adh. 6 sloka 27",
        }
    jup_h = _h("Jupiter", planets)
    # Jupiter aspects Venus: conjunction (0), 5th (4), 7th (6), or 9th (8) counted from Venus house
    jup_aspects_venus = jup_h > 0 and (jup_h - ven_h) % 12 in {0, 4, 6, 8}
    jup_in_kendra = jup_h in KENDRA_HOUSES
    if jup_aspects_venus or jup_in_kendra:
        jup_detail = "Jupiter aspects Venus" if jup_aspects_venus else f"Jupiter in kendra (H{jup_h})"
        return {
            "name": "Rama Yoga",
            "present": True,
            "description": (
                f"Venus in own sign ({ven_sign}) in kendra H{ven_h}, and {jup_detail}. "
                "Grants prosperity, beautiful spouse, artistic talent, and fame."
            ),
            "description_hi": "शुक्र स्वराशि केन्द्र में, बृहस्पति की दृष्टि — समृद्धि, कला, सुंदर जीवनसाथी।",
            "planets_involved": ["Venus", "Jupiter"],
            "sloka_ref": "Phaladeepika Adh. 6 sloka 27",
        }
    return {
        "name": "Rama Yoga",
        "present": False,
        "description": (
            f"Venus in own sign in kendra (H{ven_h}) but Jupiter neither aspects Venus nor is in kendra."
        ),
        "description_hi": "शुक्र स्वराशि केन्द्र में है, किन्तु बृहस्पति की दृष्टि/स्थिति अनुकूल नहीं।",
        "planets_involved": ["Venus"],
        "sloka_ref": "Phaladeepika Adh. 6 sloka 27",
    }


# ── Item 8 ────────────────────────────────────────────────────

def check_abhibhava_yoga(planets: dict) -> dict:
    """Abhibhava Yoga: A stronger malefic occupies the same house as a benefic, overpowering it."""
    found_pairs = []
    for benefic in ["Jupiter", "Venus", "Moon", "Mercury"]:
        bh = _h(benefic, planets)
        if bh == 0:
            continue
        b_sign = _sign(benefic, planets)
        b_strong = (b_sign in _PLANET_OWN_SIGNS.get(benefic, set())
                    or b_sign == EXALTATION_SIGNS.get(benefic, ""))
        for malefic in ["Saturn", "Mars", "Sun", "Rahu"]:
            mh = _h(malefic, planets)
            if mh != bh:
                continue
            m_sign = _sign(malefic, planets)
            m_strong = (m_sign in _PLANET_OWN_SIGNS.get(malefic, set())
                        or m_sign == EXALTATION_SIGNS.get(malefic, ""))
            if m_strong and not b_strong:
                found_pairs.append((malefic, benefic, bh))
    if found_pairs:
        desc_parts = [f"{mal} overpowers {ben} in H{h}" for mal, ben, h in found_pairs]
        involved = list({p for pair in found_pairs for p in pair[:2]})
        return {
            "name": "Abhibhava Yoga",
            "present": True,
            "description": (
                f"{'; '.join(desc_parts)}. "
                "Malefic significations dominate; benefic's promises remain unfulfilled."
            ),
            "description_hi": "पापी ग्रह शुभ ग्रह को दबाता है — पापी फल प्रबल, शुभ-फल अवरुद्ध।",
            "planets_involved": involved,
            "sloka_ref": "Phaladeepika Adh. 6 sloka 31",
        }
    return {
        "name": "Abhibhava Yoga",
        "present": False,
        "description": "No stronger malefic found conjunct a weaker benefic in the same house.",
        "description_hi": "कोई पापी ग्रह शुभ ग्रह को नहीं दबा रहा।",
        "planets_involved": [],
        "sloka_ref": "Phaladeepika Adh. 6 sloka 31",
    }


def check_papakartari_yoga(planets: dict) -> list:
    """Papakartari Yoga: Malefics flank a planet — one in house-1 and one in house+1."""
    results = []
    for planet in _CLASSICAL_PLANETS:
        ph = _h(planet, planets)
        if ph == 0:
            continue
        prev_h = ((ph - 2) % 12) + 1
        next_h = (ph % 12) + 1
        prev_malefics = [p for p in _NATURAL_MALEFICS_ADH6 if _h(p, planets) == prev_h]
        next_malefics = [p for p in _NATURAL_MALEFICS_ADH6 if _h(p, planets) == next_h]
        if prev_malefics and next_malefics:
            results.append({
                "name": f"Papakartari Yoga ({planet})",
                "present": True,
                "description": (
                    f"{planet} (H{ph}) is flanked by malefics: "
                    f"{', '.join(prev_malefics)} in H{prev_h} and "
                    f"{', '.join(next_malefics)} in H{next_h}. "
                    "Causes obstruction, poverty, and struggle for this planet's significations."
                ),
                "description_hi": f"पापी ग्रह दोनों ओर से {planet} को घेरते हैं — बाधा, कठिनाई।",
                "planets_involved": [planet] + prev_malefics + next_malefics,
                "sloka_ref": "Phaladeepika Adh. 6 sloka 33",
            })
    return results


def check_subhakartari_yoga(planets: dict) -> list:
    """Subhakartari Yoga: Benefics flank a planet — one in house-1 and one in house+1."""
    results = []
    for planet in _CLASSICAL_PLANETS:
        ph = _h(planet, planets)
        if ph == 0:
            continue
        prev_h = ((ph - 2) % 12) + 1
        next_h = (ph % 12) + 1
        prev_benefics = [p for p in ["Jupiter", "Venus", "Moon", "Mercury"] if _h(p, planets) == prev_h]
        next_benefics = [p for p in ["Jupiter", "Venus", "Moon", "Mercury"] if _h(p, planets) == next_h]
        if prev_benefics and next_benefics:
            results.append({
                "name": f"Subhakartari Yoga ({planet})",
                "present": True,
                "description": (
                    f"{planet} (H{ph}) is protected by benefics: "
                    f"{', '.join(prev_benefics)} in H{prev_h} and "
                    f"{', '.join(next_benefics)} in H{next_h}. "
                    "Grants protection, prosperity, and fulfillment of this planet's significations."
                ),
                "description_hi": f"शुभ ग्रह दोनों ओर से {planet} की रक्षा करते हैं — समृद्धि, सुरक्षा।",
                "planets_involved": [planet] + prev_benefics + next_benefics,
                "sloka_ref": "Phaladeepika Adh. 6 sloka 35",
            })
    return results


# ── Item 9 ────────────────────────────────────────────────────

def check_subhamala_yoga(planets: dict) -> dict:
    """Subhamala Yoga: Benefic planets occupy all three of houses 6, 7, and 8."""
    needed = {6, 7, 8}
    covered = {}
    for p in ["Jupiter", "Venus", "Moon", "Mercury"]:
        ph = _h(p, planets)
        if ph in needed:
            covered[ph] = covered.get(ph, []) + [p]
    if set(covered.keys()) == needed:
        involved = [p for plist in covered.values() for p in plist]
        detail = "; ".join(f"H{k}: {', '.join(v)}" for k, v in sorted(covered.items()))
        return {
            "name": "Subhamala Yoga",
            "present": True,
            "description": (
                f"Benefics form a garland around the descendant axis — {detail}. "
                "Grants protection from enemies, good marriage, longevity, and protection from chronic illness."
            ),
            "description_hi": "भाव 6, 7, 8 में शुभ ग्रह — शत्रु-नाश, विवाह-सुख, दीर्घायु।",
            "planets_involved": involved,
            "sloka_ref": "Phaladeepika Adh. 6 sloka 37",
        }
    return {
        "name": "Subhamala Yoga",
        "present": False,
        "description": "Benefics do not occupy all three of houses 6, 7, and 8 simultaneously.",
        "description_hi": "भाव 6, 7, 8 में शुभ ग्रह नहीं हैं।",
        "planets_involved": [],
        "sloka_ref": "Phaladeepika Adh. 6 sloka 37",
    }


def check_arabha_yoga(planets: dict) -> dict:
    """
    Arabha Yoga: Two variants.
    Variant 1: 5+ planets in houses 1-6 — entrepreneurial drive, early success.
    Variant 2: All 7 planets in houses 7-12 — success after relocation, recognition abroad.
    """
    missing = [p for p in _CLASSICAL_PLANETS if _h(p, planets) == 0]
    if missing:
        return {
            "name": "Arabha Yoga",
            "present": False,
            "description": f"Planet data missing for: {', '.join(missing)}.",
            "description_hi": "ग्रह डेटा अनुपलब्ध।",
            "planets_involved": [],
            "sloka_ref": "Phaladeepika Adh. 6 sloka 39",
        }
    in_first_six = [p for p in _CLASSICAL_PLANETS if 1 <= _h(p, planets) <= 6]
    if len(in_first_six) >= 5:
        return {
            "name": "Arabha Yoga",
            "present": True,
            "description": (
                f"{len(in_first_six)} planets ({', '.join(in_first_six)}) in houses 1-6 "
                "(Arabha Yoga, Variant 1). Grants entrepreneurial drive, initiative, and early success in life."
            ),
            "description_hi": "पाँच या अधिक ग्रह प्रथम 6 भावों में — उद्यमशीलता, जल्दी सफलता।",
            "planets_involved": in_first_six,
            "sloka_ref": "Phaladeepika Adh. 6 sloka 39",
        }
    above_horizon = [p for p in _CLASSICAL_PLANETS if _h(p, planets) >= 7]
    if len(above_horizon) == 7:
        return {
            "name": "Arabha Yoga",
            "present": True,
            "description": (
                "All 7 planets above the horizon (houses 7-12) "
                "(Arabha Yoga, Variant 2). Grants recognition in foreign lands and success after relocation."
            ),
            "description_hi": "सभी ग्रह सप्तम से द्वादश भाव में — विदेश में सफलता, स्थानांतरण के बाद यश।",
            "planets_involved": _CLASSICAL_PLANETS[:],
            "sloka_ref": "Phaladeepika Adh. 6 sloka 39",
        }
    return {
        "name": "Arabha Yoga",
        "present": False,
        "description": (
            f"Arabha Yoga absent: {len(in_first_six)} planets in H1-6 (need 5+); "
            f"{len(above_horizon)} planets in H7-12 (need all 7)."
        ),
        "description_hi": "अरब योग नहीं — न पर्याप्त ग्रह प्रथम छह भावों में, न सभी ऊपरी भावों में।",
        "planets_involved": [],
        "sloka_ref": "Phaladeepika Adh. 6 sloka 39",
    }


# ============================================================
# NEW DOSHAS
# ============================================================

def check_angarak_dosha(planets: dict) -> dict:
    """Angarak Dosha: Mars conjunct Rahu or Ketu."""
    if _conjunct("Mars", "Rahu", planets):
        h = _h("Mars", planets)
        sev = "high" if h in TRIK_HOUSES else "medium"
        return {"name": "Angarak Dosha", "present": True, "severity": sev,
                "description": f"Mars conjunct Rahu in house {h}. Causes aggression, accidents, legal issues, and financial instability.",
                "remedies": ["Recite Hanuman Chalisa daily.", "Donate red items on Tuesdays.", "Perform Mangal-Rahu Shanti Puja."]}
    if _conjunct("Mars", "Ketu", planets):
        h = _h("Mars", planets)
        return {"name": "Angarak Dosha", "present": True, "severity": "medium",
                "description": f"Mars conjunct Ketu in house {h}. Can cause sudden conflicts, surgical issues, and impulsive decisions.",
                "remedies": ["Recite Hanuman Chalisa daily.", "Donate red items on Tuesdays."]}
    return {"name": "Angarak Dosha", "present": False, "severity": "none", "description": "Mars not conjunct Rahu or Ketu.", "remedies": []}


def check_guru_chandal_dosha(planets: dict) -> dict:
    """Guru Chandal Dosha: Jupiter conjunct Rahu or Ketu."""
    if _conjunct("Jupiter", "Rahu", planets):
        h = _h("Jupiter", planets)
        return {"name": "Guru Chandal Dosha", "present": True, "severity": "medium",
                "description": f"Jupiter conjunct Rahu in house {h}. Causes moral confusion, disrespect for tradition, education obstacles, and wrong guidance.",
                "remedies": ["Worship Lord Vishnu on Thursdays.", "Donate yellow items.", "Perform Guru Graha Shanti Puja."]}
    if _conjunct("Jupiter", "Ketu", planets):
        h = _h("Jupiter", planets)
        return {"name": "Guru Chandal Dosha", "present": True, "severity": "mild",
                "description": f"Jupiter conjunct Ketu in house {h}. Can give spiritual tendencies but also confusion in worldly matters.",
                "remedies": ["Worship Lord Vishnu on Thursdays.", "Donate yellow items."]}
    return {"name": "Guru Chandal Dosha", "present": False, "severity": "none", "description": "Jupiter not conjunct Rahu or Ketu.", "remedies": []}


def check_vish_dosha(planets: dict) -> dict:
    """Vish Dosha: Saturn conjunct Moon."""
    if _conjunct("Saturn", "Moon", planets):
        h = _h("Moon", planets)
        sev = "high" if h in {1, 4, 7, 8} else "medium"
        return {"name": "Vish Dosha (Vish Yoga)", "present": True, "severity": sev,
                "description": f"Saturn conjunct Moon in house {h}. Causes depression, chronic anxiety, emotional instability, and pessimistic outlook.",
                "remedies": ["Perform Shani Shanti and Chandra Puja.", "Donate black items on Saturdays and white items on Mondays.", "Wear a Pearl after consultation."]}
    return {"name": "Vish Dosha (Vish Yoga)", "present": False, "severity": "none", "description": "Saturn not conjunct Moon.", "remedies": []}


def check_shrapit_dosha(planets: dict) -> dict:
    """Shrapit Dosha: Saturn conjunct Rahu."""
    if _conjunct("Saturn", "Rahu", planets):
        h = _h("Saturn", planets)
        sev = "high" if h in {1, 5, 7, 9} else "medium"
        return {"name": "Shrapit Dosha", "present": True, "severity": sev,
                "description": f"Saturn conjunct Rahu in house {h}. Indicates past-life karmic debts, chronic delays, repeated failures, and obstruction in fortune.",
                "remedies": ["Perform Shani-Rahu Shanti Puja.", "Rudrabhishek on Mondays.", "Donate black items on Saturdays."]}
    return {"name": "Shrapit Dosha", "present": False, "severity": "none", "description": "Saturn not conjunct Rahu.", "remedies": []}


def check_grahan_dosha(planets: dict) -> dict:
    """Grahan Dosha: Sun or Moon conjunct Rahu/Ketu (eclipse yoga)."""
    results = []
    if _conjunct("Sun", "Rahu", planets):
        results.append(f"Sun conjunct Rahu in H{_h('Sun', planets)} (Surya Grahan)")
    if _conjunct("Sun", "Ketu", planets):
        results.append(f"Sun conjunct Ketu in H{_h('Sun', planets)} (Surya Grahan)")
    if _conjunct("Moon", "Rahu", planets):
        results.append(f"Moon conjunct Rahu in H{_h('Moon', planets)} (Chandra Grahan)")
    if _conjunct("Moon", "Ketu", planets):
        results.append(f"Moon conjunct Ketu in H{_h('Moon', planets)} (Chandra Grahan)")
    if results:
        return {"name": "Grahan Dosha", "present": True, "severity": "high",
                "description": f"Eclipse affliction: {'; '.join(results)}. Weakens the luminary, causing ego/emotional issues, father/mother health concerns.",
                "remedies": ["Surya Grahan: Surya Namaskar, donate copper.", "Chandra Grahan: Chandra Puja, donate white items.", "Recite Maha Mrityunjaya Mantra."]}
    return {"name": "Grahan Dosha", "present": False, "severity": "none", "description": "Sun/Moon not eclipsed by Rahu/Ketu.", "remedies": []}


def check_ghatak_dosha(planets: dict) -> dict:
    """Ghatak Yoga/Dosha: Saturn conjunct Mars."""
    if _conjunct("Saturn", "Mars", planets):
        h = _h("Mars", planets)
        sev = "high" if h in {1, 4, 7, 8} else "medium"
        return {"name": "Ghatak Yoga", "present": True, "severity": sev,
                "description": f"Saturn conjunct Mars in house {h}. Risk of accidents, injuries, surgical operations, and aggressive tendencies.",
                "remedies": ["Hanuman Puja on Tuesdays.", "Shani Shanti Puja on Saturdays.", "Avoid risky activities on Tuesdays/Saturdays."]}
    return {"name": "Ghatak Yoga", "present": False, "severity": "none", "description": "Saturn not conjunct Mars.", "remedies": []}


def check_daridra_dosha(planets: dict, asc_sign: str) -> dict:
    """Daridra Dosha: Lord of 11th in trik house (6/8/12)."""
    if not asc_sign:
        return {"name": "Daridra Dosha", "present": False, "severity": "none", "description": "Ascendant data missing.", "remedies": []}
    lord11 = _house_lord(11, asc_sign)
    lord2 = _house_lord(2, asc_sign)
    reasons = []
    if lord11 and _h(lord11, planets) in TRIK_HOUSES:
        reasons.append(f"11th lord ({lord11}) in house {_h(lord11, planets)}")
    if lord2 and _h(lord2, planets) in TRIK_HOUSES:
        reasons.append(f"2nd lord ({lord2}) in house {_h(lord2, planets)}")
    if reasons:
        sev = "high" if len(reasons) > 1 else "medium"
        return {"name": "Daridra Dosha", "present": True, "severity": sev,
                "description": f"Wealth house lords afflicted: {'; '.join(reasons)}. Can cause financial difficulties, debts, and poverty cycles.",
                "remedies": ["Perform Lakshmi Puja on Fridays.", "Donate on Fridays.", "Recite Shri Suktam daily."]}
    return {"name": "Daridra Dosha", "present": False, "severity": "none", "description": "Wealth lords not in trik houses.", "remedies": []}


def analyze_yogas_and_doshas(planets: dict, asc_sign: str = "") -> dict:
    """
    Comprehensive Yoga & Dosha analysis.

    Args:
        planets: Dict of planet data {name: {house, sign, longitude, ...}}

    Returns:
        {
            yogas: [{name, description, present, planets_involved}],
            doshas: [{name, description, present, severity, remedies}]
        }
    """
    # ── Yogas ──
    yogas = []

    # Panch Mahapurusha Yogas (5)
    yogas.extend(check_panch_mahapurusha(planets))

    # Moon-based Yogas
    yogas.append(check_gajakesari_yoga(planets))
    yogas.append(check_sunapha_yoga(planets))
    yogas.append(check_anapha_yoga(planets))
    yogas.append(check_durudhara_yoga(planets))
    yogas.append(check_shakata_yoga(planets))
    yogas.append(check_adhi_yoga(planets))
    yogas.append(check_amala_yoga(planets))
    yogas.append(check_chandra_mangal_yoga(planets))

    # Sun-based Yogas
    yogas.append(check_budhaditya_yoga(planets))
    yogas.append(check_vesi_yoga(planets))
    yogas.append(check_vasi_yoga(planets))
    yogas.append(check_ubhayachari_yoga(planets))
    yogas.append(check_sun_in_own_sign(planets))
    yogas.append(check_saturn_exalted(planets))

    # Raja Yogas (need ascendant)
    yogas.append(check_neecha_bhanga(planets))
    yogas.extend(check_neecha_bhanga_variants(planets, asc_sign))  # per-planet Adh. 7 variants
    yogas.extend(check_viparita_raja_yoga(planets, asc_sign))
    yogas.append(check_raja_yoga(planets, asc_sign))
    yogas.append(check_lakshmi_yoga(planets, asc_sign))
    yogas.extend(check_dhana_yogas(planets, asc_sign))

    # Adhyaya 7 Raja Yogas (12 additional)
    try:
        from app.raja_yoga_engine import detect_adh7_raja_yogas
        yogas.extend(detect_adh7_raja_yogas(planets, asc_sign))
    except Exception:
        logger.exception("Adh. 7 Raja Yoga detection failed; continuing without these yogas")

    # Special Yogas
    yogas.append(check_saraswati_yoga(planets))
    yogas.append(check_danda_yoga(planets))

    # Adh. 6 Special Yogas (Items 7, 8, 9)
    yogas.append(check_chimana_yoga(planets))
    yogas.append(check_surya_yoga(planets))
    yogas.append(check_jalatha_yoga(planets))
    yogas.append(check_chattra_yoga(planets))
    yogas.append(check_apta_yoga(planets))
    yogas.append(check_rama_yoga(planets))
    yogas.append(check_subhamala_yoga(planets))
    yogas.append(check_arabha_yoga(planets))
    yogas.append(check_abhibhava_yoga(planets))
    yogas.extend(check_papakartari_yoga(planets))
    yogas.extend(check_subhakartari_yoga(planets))

    # ── Doshas ──
    doshas = []

    # Mangal Dosha
    mars_house = planets.get("Mars", {}).get("house", 0)
    mangal = check_mangal_dosha(mars_house)
    doshas.append({
        "name": "Mangal Dosha",
        "present": mangal["has_dosha"],
        "description": mangal["description"],
        "severity": mangal["severity"],
        "remedies": mangal["remedies"],
    })

    # Kaal Sarp Dosha
    rahu_house = planets.get("Rahu", {}).get("house", 0)
    ketu_house = planets.get("Ketu", {}).get("house", 0)
    planet_houses = {}
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if p in planets:
            planet_houses[p] = planets[p].get("house", 1)
    kaal_sarp = check_kaal_sarp(rahu_house, ketu_house, planet_houses)
    doshas.append({
        "name": "Kaal Sarp Dosha",
        "present": kaal_sarp["has_dosha"],
        "description": kaal_sarp["description"],
        "severity": "high" if kaal_sarp["has_dosha"] else "none",
        "remedies": kaal_sarp["remedies"],
    })

    # Pitra Dosha
    pitra = check_pitra_dosha(planets)
    doshas.append({"name": "Pitra Dosha", "present": pitra["has_dosha"],
                   "description": pitra["description"], "severity": pitra["severity"], "remedies": pitra["remedies"]})

    # Kemdrum Dosha
    kemdrum = check_kemdrum_dosha(planets)
    doshas.append({"name": "Kemdrum Dosha", "present": kemdrum["has_dosha"],
                   "description": kemdrum["description"], "severity": kemdrum["severity"], "remedies": kemdrum["remedies"]})

    # NEW Doshas
    doshas.append(check_angarak_dosha(planets))
    doshas.append(check_guru_chandal_dosha(planets))
    doshas.append(check_vish_dosha(planets))
    doshas.append(check_shrapit_dosha(planets))
    doshas.append(check_grahan_dosha(planets))
    doshas.append(check_ghatak_dosha(planets))
    doshas.append(check_daridra_dosha(planets, asc_sign))

    for yoga in yogas:
        yoga_name = yoga.get("name")
        if isinstance(yoga_name, str) and yoga_name and "name_key" not in yoga:
            yoga["name_key"] = to_translation_key("YOGA", yoga_name)
        if not yoga.get("strength"):
            yoga["strength"] = _compute_yoga_strength(yoga, planets)
        if yoga.get("trigger_houses") is None:
            yoga["trigger_houses"] = sorted({
                planets.get(p, {}).get("house", 0)
                for p in (yoga.get("planets_involved") or [])
                if planets.get(p, {}).get("house", 0)
            })

    for dosha in doshas:
        dosha_name = dosha.get("name")
        if isinstance(dosha_name, str) and dosha_name and "name_key" not in dosha:
            dosha["name_key"] = to_translation_key("DOSHA", dosha_name)

    return {
        "yogas": yogas,
        "doshas": doshas,
    }
