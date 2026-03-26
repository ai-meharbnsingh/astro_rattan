"""
dosha_engine.py — Vedic Dosha Detection Engine
================================================
Detects Mangal Dosha, Kaal Sarp Dosha, and Sade Sati.
"""

# Zodiac signs in order (0-indexed for arithmetic)
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

ZODIAC_INDEX = {sign: i for i, sign in enumerate(ZODIAC_SIGNS)}

# Houses where Mars causes Mangal Dosha
MANGAL_DOSHA_HOUSES = {1, 2, 4, 7, 8, 12}


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

    Sade Sati is active when Saturn is in:
    - The sign before the Moon sign (12th from Moon)
    - The Moon sign itself (1st from Moon / Janma Sade Sati)
    - The sign after the Moon sign (2nd from Moon)

    Args:
        moon_sign: Natal Moon sign (e.g. "Aries", "Scorpio")
        saturn_sign: Current transit sign of Saturn

    Returns:
        {has_sade_sati: bool, phase: str, description: str, severity: str, remedies: [str]}
    """
    if moon_sign not in ZODIAC_INDEX or saturn_sign not in ZODIAC_INDEX:
        return {
            "has_sade_sati": False,
            "phase": "none",
            "description": f"Invalid sign provided: moon_sign={moon_sign}, saturn_sign={saturn_sign}",
            "severity": "none",
            "remedies": [],
        }

    moon_idx = ZODIAC_INDEX[moon_sign]
    saturn_idx = ZODIAC_INDEX[saturn_sign]

    # 12th from Moon (sign before)
    sign_before_idx = (moon_idx - 1) % 12
    # Same sign as Moon
    same_idx = moon_idx
    # 2nd from Moon (sign after)
    sign_after_idx = (moon_idx + 1) % 12

    if saturn_idx == sign_before_idx:
        phase = "Rising (12th from Moon)"
        severity = "medium"
        description = (
            f"Sade Sati ACTIVE — Rising phase. Saturn in {saturn_sign} "
            f"is transiting the 12th house from natal Moon in {moon_sign}. "
            "This phase brings financial pressures and health concerns. "
            "The beginning of the 7.5-year Saturn transit over the Moon."
        )
    elif saturn_idx == same_idx:
        phase = "Peak (over Moon sign)"
        severity = "high"
        description = (
            f"Sade Sati ACTIVE — Peak phase. Saturn in {saturn_sign} "
            f"is directly transiting over natal Moon in {moon_sign}. "
            "This is the most intense phase — emotional turbulence, career challenges, "
            "and major life restructuring are common."
        )
    elif saturn_idx == sign_after_idx:
        phase = "Setting (2nd from Moon)"
        severity = "medium"
        description = (
            f"Sade Sati ACTIVE — Setting phase. Saturn in {saturn_sign} "
            f"is transiting the 2nd house from natal Moon in {moon_sign}. "
            "This phase affects family, finances, and speech. "
            "The final stretch before Sade Sati ends."
        )
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
        }

    remedies = [
        "Recite Shani Beej Mantra: 'Om Sham Shanaishcharaya Namah' 108 times on Saturdays.",
        "Light a sesame oil lamp under a Peepal tree on Saturday evenings.",
        "Donate black items (clothes, sesame, iron) on Saturdays.",
        "Wear a Blue Sapphire (Neelam) only after astrological consultation.",
        "Perform Shani Shanti Puja or Hanuman Puja regularly.",
        "Practice patience, discipline, and service — Saturn rewards hard work.",
    ]

    return {
        "has_sade_sati": True,
        "phase": phase,
        "description": description,
        "severity": severity,
        "remedies": remedies,
    }
