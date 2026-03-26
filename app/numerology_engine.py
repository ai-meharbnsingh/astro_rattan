"""
numerology_engine.py — Vedic Numerology Engine
================================================
Pythagorean numerology: Life Path, Expression, Soul Urge, Personality numbers.
Reduces to single digit (1-9) or master numbers (11, 22, 33).
"""

# Pythagorean number mapping: A=1, B=2, ... I=9, J=1, K=2, ...
PYTHAGOREAN_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8,
}

VOWELS = set('AEIOU')
MASTER_NUMBERS = {11, 22, 33}

# Life path prediction templates keyed by life path number
PREDICTIONS = {
    1: "Natural leader with pioneering spirit. Independent, ambitious, and driven to forge new paths. "
       "This period favors bold initiatives and self-reliance.",
    2: "Diplomat and peacemaker. Cooperation, sensitivity, and partnerships define your journey. "
       "Seek harmony in relationships and trust your intuition.",
    3: "Creative expression and joyful communication. Artistic talents blossom. "
       "Social connections and optimism bring abundance.",
    4: "Builder and organizer. Stability, discipline, and hard work create lasting foundations. "
       "Patience and systematic effort lead to mastery.",
    5: "Freedom seeker and adventurer. Change, travel, and versatility are your allies. "
       "Embrace new experiences while maintaining inner balance.",
    6: "Nurturer and healer. Responsibility to family and community. "
       "Love, beauty, and domestic harmony are your life themes.",
    7: "Spiritual seeker and analyst. Inner wisdom, contemplation, and research. "
       "Solitude and study unlock deeper truths.",
    8: "Material mastery and karmic balance. Business acumen and authority. "
       "Power must be wielded with integrity for lasting success.",
    9: "Humanitarian and universal lover. Compassion, generosity, and completion. "
       "Service to others fulfills your highest purpose.",
    11: "Master Intuitive. Heightened spiritual awareness and visionary insight. "
        "Channel inspiration into tangible form. Avoid nervous tension.",
    22: "Master Builder. Ability to turn grand visions into reality on a massive scale. "
        "Practical idealism and global impact are your calling.",
    33: "Master Teacher. Selfless service, healing, and uplifting humanity. "
        "The highest expression of love in action.",
}


def _reduce_to_single(n: int) -> int:
    """Reduce a number to single digit (1-9) or master number (11, 22, 33)."""
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(d) for d in str(n))
    return n


def _life_path(birth_date: str) -> int:
    """
    Calculate life path number from birth date string (YYYY-MM-DD).
    Reduce each component (year, month, day) separately, then sum and reduce.
    """
    parts = birth_date.split('-')
    if len(parts) != 3:
        raise ValueError(f"Invalid birth_date format: {birth_date}. Expected YYYY-MM-DD.")

    year_str, month_str, day_str = parts

    # Reduce each part individually
    year_sum = _reduce_to_single(sum(int(d) for d in year_str))
    month_sum = _reduce_to_single(int(month_str))
    day_sum = _reduce_to_single(int(day_str))

    return _reduce_to_single(year_sum + month_sum + day_sum)


def _name_to_number(name: str) -> int:
    """Sum all letter values in name using Pythagorean mapping, then reduce."""
    total = 0
    for ch in name.upper():
        if ch in PYTHAGOREAN_MAP:
            total += PYTHAGOREAN_MAP[ch]
    return _reduce_to_single(total)


def _vowels_number(name: str) -> int:
    """Sum vowel letter values in name (Soul Urge), then reduce."""
    total = 0
    for ch in name.upper():
        if ch in VOWELS and ch in PYTHAGOREAN_MAP:
            total += PYTHAGOREAN_MAP[ch]
    return _reduce_to_single(total)


def _consonants_number(name: str) -> int:
    """Sum consonant letter values in name (Personality), then reduce."""
    total = 0
    for ch in name.upper():
        if ch in PYTHAGOREAN_MAP and ch not in VOWELS:
            total += PYTHAGOREAN_MAP[ch]
    return _reduce_to_single(total)


def calculate_numerology(name: str, birth_date: str) -> dict:
    """
    Full numerology calculation.

    Args:
        name: Full name string
        birth_date: Date string in YYYY-MM-DD format

    Returns:
        dict with life_path, expression, soul_urge, personality, predictions
    """
    life_path = _life_path(birth_date)
    expression = _name_to_number(name)
    soul_urge = _vowels_number(name)
    personality = _consonants_number(name)

    prediction = PREDICTIONS.get(life_path, PREDICTIONS[9])

    return {
        "life_path": life_path,
        "expression": expression,
        "soul_urge": soul_urge,
        "personality": personality,
        "predictions": prediction,
    }
