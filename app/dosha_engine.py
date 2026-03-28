"""
dosha_engine.py — Vedic Dosha & Yoga Detection Engine
======================================================
Detects Mangal Dosha, Kaal Sarp Dosha, Sade Sati, Pitra Dosha, Kemdrum Dosha.
Also detects positive Yogas: Gajakesari, Budhaditya, Chandra-Mangal,
and Panch Mahapurusha Yogas.
"""

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

# Malefic planets
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


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


def analyze_yogas_and_doshas(planets: dict) -> dict:
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
    yogas.append(check_gajakesari_yoga(planets))
    yogas.append(check_budhaditya_yoga(planets))
    yogas.append(check_chandra_mangal_yoga(planets))
    yogas.extend(check_panch_mahapurusha(planets))

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
    doshas.append({
        "name": "Pitra Dosha",
        "present": pitra["has_dosha"],
        "description": pitra["description"],
        "severity": pitra["severity"],
        "remedies": pitra["remedies"],
    })

    # Kemdrum Dosha
    kemdrum = check_kemdrum_dosha(planets)
    doshas.append({
        "name": "Kemdrum Dosha",
        "present": kemdrum["has_dosha"],
        "description": kemdrum["description"],
        "severity": kemdrum["severity"],
        "remedies": kemdrum["remedies"],
    })

    return {
        "yogas": yogas,
        "doshas": doshas,
    }
