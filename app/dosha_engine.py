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
                
                # Check if dispositor is in kendra from debilitated planet or Moon
                kendra_from_deb = ((deb_house - disp_house) % 12) in [0, 3, 6, 9]
                kendra_from_moon = ((moon_house - disp_house) % 12) in [0, 3, 6, 9]
                
                if kendra_from_deb or kendra_from_moon:
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
    """Amala Yoga: A natural benefic in 10th from Lagna or Moon."""
    found = []
    for p in ["Jupiter", "Venus", "Mercury", "Moon"]:
        if _h(p, planets) == 10:
            found.append(p)
    if found:
        return {"name": "Amala Yoga", "present": True,
                "description": f"{', '.join(found)} in 10th house. Grants spotless reputation, fame, and virtuous conduct in career.",
                "planets_involved": found}
    return {"name": "Amala Yoga", "present": False, "description": "No benefic in 10th house.", "planets_involved": []}


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
    yogas.extend(check_viparita_raja_yoga(planets, asc_sign))
    yogas.append(check_raja_yoga(planets, asc_sign))
    yogas.append(check_lakshmi_yoga(planets, asc_sign))
    yogas.append(check_dhana_yoga(planets, asc_sign))

    # Special Yogas
    yogas.append(check_saraswati_yoga(planets))
    yogas.append(check_danda_yoga(planets))

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

    return {
        "yogas": yogas,
        "doshas": doshas,
    }
