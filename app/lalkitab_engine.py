"""
lalkitab_engine.py — Lal Kitab Remedies Engine
================================================
Provides Lal Kitab remedies for weak or afflicted planets.
Remedies are prescribed only when planet strength < 0.5 (enemy/debilitated).
"""
from app.astro_iogita_engine import get_planet_strength

# ============================================================
# REMEDIES — planet -> list of remedy strings
# 5-8 remedies per planet for all 9 Vedic planets
# ============================================================
REMEDIES = {
    "Sun": [
        "Offer water to the Sun every morning at sunrise facing east",
        "Wear a Ruby (Manik) gemstone in gold on the ring finger on Sunday",
        "Donate wheat, jaggery, and copper on Sundays",
        "Keep a solid square piece of copper in your pocket",
        "Place wheat grains in flowing water on Sundays",
        "Avoid accepting free gifts or charity from others",
        "Maintain good relations with your father and authority figures",
        "Feed jaggery and wheat to monkeys on Sundays",
    ],
    "Moon": [
        "Wear a Pearl (Moti) in silver on the little finger on Monday",
        "Drink water from a silver glass or cup",
        "Keep a square piece of silver with you",
        "Donate white rice, milk, and silver on Mondays",
        "Maintain good relations with your mother",
        "Keep fresh water by your bedside at night and pour it into a plant in the morning",
        "Avoid milk-based business for income",
        "Wear white or cream-colored clothes on Mondays",
    ],
    "Mars": [
        "Donate red lentils (masoor dal) on Tuesdays",
        "Wear a Red Coral (Moonga) in gold or copper on the ring finger on Tuesday",
        "Feed sweet bread (chapati with jaggery) to dogs",
        "Keep a deer skin at your place of worship",
        "Float red masoor dal in flowing water on Tuesdays",
        "Donate blood when possible",
        "Maintain sweet relationships with siblings",
        "Apply saffron (kesar) tilak on forehead",
    ],
    "Mercury": [
        "Wear an Emerald (Panna) in gold on the little finger on Wednesday",
        "Donate green moong dal and green vegetables on Wednesdays",
        "Feed green grass to cows",
        "Keep a square piece of copper with a hole in the center",
        "Fill an earthen pot with honey and bury it in a deserted place",
        "Float green things in flowing water on Wednesdays",
        "Maintain good relations with sisters, aunts, and daughters",
        "Wear green-colored clothes on Wednesdays",
    ],
    "Jupiter": [
        "Wear a Yellow Sapphire (Pukhraj) in gold on the index finger on Thursday",
        "Donate turmeric, yellow cloth, and gold on Thursdays",
        "Apply saffron or turmeric tilak on forehead and navel",
        "Serve and respect your guru, elders, and teachers",
        "Water a banana tree on Thursdays",
        "Feed yellow sweets to Brahmins on Thursdays",
        "Keep a square piece of gold with you",
        "Donate yellow lentils (chana dal) at a temple on Thursdays",
    ],
    "Venus": [
        "Wear a Diamond (Heera) or White Sapphire in platinum/silver on the middle finger on Friday",
        "Donate white rice, white clothes, and ghee on Fridays",
        "Offer white flowers at a Devi temple on Fridays",
        "Use perfume or fragrance regularly",
        "Maintain a clean and beautiful living space",
        "Donate silk or expensive cloth to young women on Fridays",
        "Keep a square piece of silver at home",
        "Feed white sweets to cows on Fridays",
    ],
    "Saturn": [
        "Wear a Blue Sapphire (Neelam) in silver/iron on the middle finger on Saturday",
        "Donate black sesame seeds (til), mustard oil, and iron on Saturdays",
        "Feed crows with cooked rice mixed with sesame oil on Saturdays",
        "Pour mustard oil on a piece of iron and see your reflection, then donate both",
        "Serve the poor, elderly, and disabled",
        "Keep a square piece of iron under your pillow",
        "Donate black blankets or leather shoes to the needy on Saturdays",
        "Avoid alcohol and non-vegetarian food on Saturdays",
    ],
    "Rahu": [
        "Donate black and white sesame seeds (til) on Saturdays",
        "Keep a piece of silver square with you",
        "Store water in the southwest corner of your home",
        "Feed birds daily, especially crows",
        "Donate radishes and coconut at a temple",
        "Wear Gomed (Hessonite) in silver on the middle finger on Saturday",
        "Float coconut in flowing water",
        "Keep fennel (saunf) under your pillow while sleeping",
    ],
    "Ketu": [
        "Donate a black and white blanket to a temple",
        "Feed stray dogs regularly",
        "Wear Cat's Eye (Lehsuniya) in silver on the little finger on Thursday",
        "Keep saffron at your place of worship",
        "Donate sesame seeds and blankets on Tuesdays",
        "Apply saffron tilak on forehead daily",
        "Keep a silver ball in your pocket",
        "Maintain good relations with your maternal grandfather",
    ],
}

# Dignity labels for display
DIGNITY_LABELS = {
    "Exalted": "exalted",
    "Own Sign": "in own sign",
    "Friendly": "in friendly sign",
    "Neutral": "in neutral sign",
    "Enemy": "in enemy sign",
    "Debilitated": "debilitated",
}


def _get_dignity_label(planet: str, sign: str) -> str:
    """Determine dignity label for a planet in a sign."""
    from app.astro_iogita_engine import EXALTED, DEBILITATED, OWN_SIGNS, FRIEND_SIGNS, ENEMY_SIGNS

    if sign == EXALTED.get(planet):
        return "Exalted"
    if sign == DEBILITATED.get(planet):
        return "Debilitated"
    if sign in OWN_SIGNS.get(planet, []):
        return "Own Sign"
    if sign in FRIEND_SIGNS.get(planet, []):
        return "Friendly"
    if sign in ENEMY_SIGNS.get(planet, []):
        return "Enemy"
    return "Neutral"


def get_remedies(planet_positions: dict) -> dict:
    """
    Get Lal Kitab remedies for weak or afflicted planets.

    Args:
        planet_positions: dict of {planet_name: sign_name}

    Returns:
        dict of {planet: {sign, dignity, strength, remedies: [str]}}
        Remedies list is populated only for planets with strength < 0.5
        (enemy or debilitated placements).
    """
    result = {}

    for planet, sign in planet_positions.items():
        strength = get_planet_strength(planet, sign)
        dignity = _get_dignity_label(planet, sign)

        planet_remedies = []
        if strength < 0.5:
            # Planet is weak/afflicted — prescribe remedies
            planet_remedies = REMEDIES.get(planet, [])

        result[planet] = {
            "sign": sign,
            "dignity": dignity,
            "strength": round(strength, 2),
            "remedies": planet_remedies,
        }

    return result
