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

# Life path prediction templates keyed by number
LIFE_PATH_PREDICTIONS = {
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

# Destiny number prediction templates (derived from full name)
DESTINY_PREDICTIONS = {
    1: "Your destiny calls you to lead and innovate. You are meant to carve original paths and inspire "
       "others through decisive action. Embrace independence and trust your unique vision to leave a lasting mark.",
    2: "Your destiny is rooted in partnership and diplomacy. You are here to mediate, unite, and bring "
       "balance to those around you. Your greatest achievements come through collaboration and gentle persuasion.",
    3: "Your destiny is one of creative self-expression. Writing, speaking, art, or performance are natural "
       "outlets for your vibrant energy. You uplift others through joy and are meant to inspire with your words.",
    4: "Your destiny demands structure and dedication. You are the architect of lasting systems and "
       "institutions. Through methodical effort and unwavering integrity, you build what endures beyond a lifetime.",
    5: "Your destiny thrives on change and exploration. You are meant to experience the full breadth of life "
       "and share those adventures with others. Adaptability and curiosity are your greatest gifts.",
    6: "Your destiny centers on love, responsibility, and service to family and community. You are a natural "
       "counselor and protector. Your fulfillment comes from creating beauty and harmony in your surroundings.",
    7: "Your destiny lies in the pursuit of truth and wisdom. You are a natural researcher, philosopher, and "
       "spiritual seeker. Depth of understanding, not breadth, is your path to mastery.",
    8: "Your destiny is tied to material achievement and the responsible use of power. You are meant to "
       "build prosperity and influence, but karmic balance demands that you wield authority with fairness.",
    9: "Your destiny is humanitarian service on a grand scale. You are meant to give selflessly and inspire "
       "compassion in others. Letting go of personal attachment frees you to serve your highest calling.",
    11: "Your destiny carries the weight of spiritual illumination. As a master number, you channel higher "
        "truths into the world. Visionary leadership and inspired teaching are your sacred responsibilities.",
    22: "Your destiny is to manifest visionary ideals in concrete form. You possess rare ability to combine "
        "spiritual insight with practical genius. Large-scale projects that serve humanity are your life work.",
    33: "Your destiny is the highest form of loving service. You are called to heal, teach, and uplift on a "
        "profound level. Selfless devotion to others transforms both you and those you touch.",
}

# Soul urge prediction templates (derived from vowels in name)
SOUL_URGE_PREDICTIONS = {
    1: "Deep within, you crave autonomy and the freedom to chart your own course. Your inner drive is to "
       "be first, to originate, and to stand apart. Honoring this need for independence fuels your spirit.",
    2: "Your soul yearns for deep connection and emotional harmony. You find inner peace through loving "
       "partnerships and quiet acts of kindness. Being truly seen and valued by another fulfills you profoundly.",
    3: "At your core, you desire joyful self-expression and creative freedom. Your inner world is vivid and "
       "imaginative. Sharing your ideas, humor, and artistic vision with others nourishes your deepest self.",
    4: "Your soul craves order, security, and a sense of accomplishment. You feel most at peace when life is "
       "stable and your efforts produce tangible results. Building a solid foundation satisfies your inner need.",
    5: "Your innermost desire is for freedom, variety, and sensory experience. Routine stifles your spirit. "
       "You need adventure, travel, and the thrill of the unknown to feel truly alive.",
    6: "Your soul longs to nurture, protect, and create a harmonious home. Love and family are your deepest "
       "motivations. You feel most fulfilled when those you care for are happy and safe.",
    7: "Your inner world craves solitude, reflection, and spiritual understanding. You need time alone to "
       "think, meditate, and explore the mysteries of existence. Inner peace comes through contemplation.",
    8: "Deep down, you desire recognition, achievement, and material security. You are driven to prove your "
       "competence and build something of lasting value. Success and respect satisfy your soul.",
    9: "Your soul urges you toward universal love and selfless giving. You feel most fulfilled when serving "
       "a cause greater than yourself. Compassion and idealism are the wellsprings of your inner life.",
    11: "Your soul carries an intense longing for spiritual truth and inspired purpose. You sense a higher "
        "calling and feel restless until you align with it. Intuition is your most trusted inner guide.",
    22: "Your deepest desire is to build something of lasting significance for humanity. Ordinary ambitions "
        "feel hollow. You are driven by a vision so large that only disciplined mastery can bring it to life.",
    33: "Your soul burns with compassion and a desire to heal the world. You carry the weight of empathy "
        "for all living things. Channeling this love into service brings you the deepest possible fulfillment.",
}

# Personality number prediction templates (derived from consonants in name)
PERSONALITY_PREDICTIONS = {
    1: "Others perceive you as confident, assertive, and self-assured. You project an image of strength and "
       "capability. People naturally look to you for direction and are drawn to your decisive energy.",
    2: "You come across as warm, approachable, and tactful. Others see you as a supportive listener and "
       "a calming presence. Your gentle demeanor invites trust and puts people at ease.",
    3: "You radiate charm, wit, and social magnetism. Others see you as entertaining, expressive, and full "
       "of life. Your outward personality draws people in and makes social situations effortless.",
    4: "Others perceive you as reliable, grounded, and hardworking. You project stability and competence. "
       "People trust you with responsibility because your exterior signals discipline and dependability.",
    5: "You appear dynamic, energetic, and magnetically attractive. Others see you as someone who embraces "
       "life fully. Your outward persona suggests excitement, versatility, and a love of the unconventional.",
    6: "Others see you as caring, responsible, and devoted. You project an aura of warmth and domestic "
       "grace. People turn to you for comfort and counsel, sensing your genuine concern for their well-being.",
    7: "You come across as reserved, intellectual, and somewhat mysterious. Others sense depth beneath "
       "your calm exterior. Your dignified bearing commands respect and invites curiosity rather than casual approach.",
    8: "Others perceive you as powerful, successful, and authoritative. You project an image of material "
       "competence and executive ability. Your presence commands attention in professional settings.",
    9: "You appear compassionate, worldly, and sophisticated. Others see you as someone with broad vision "
       "and generous spirit. Your exterior projects tolerance, wisdom, and a noble bearing.",
    11: "Others perceive you as inspired, charismatic, and slightly otherworldly. You project a luminous "
        "quality that draws attention. People sense your heightened awareness and visionary nature.",
    22: "You come across as exceptionally capable and ambitious on a grand scale. Others see a master "
        "organizer with the power to transform ideas into reality. Your presence inspires confidence in large endeavors.",
    33: "Others perceive you as deeply compassionate and selflessly devoted. You project an almost saintly "
        "warmth that draws people seeking guidance. Your exterior radiates unconditional love and healing energy.",
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
        dict with life_path, destiny, soul_urge, personality, predictions
    """
    life_path = _life_path(birth_date)
    destiny = _name_to_number(name)
    soul_urge = _vowels_number(name)
    personality = _consonants_number(name)

    predictions = {
        "life_path": LIFE_PATH_PREDICTIONS.get(life_path, LIFE_PATH_PREDICTIONS[9]),
        "destiny": DESTINY_PREDICTIONS.get(destiny, DESTINY_PREDICTIONS[9]),
        "soul_urge": SOUL_URGE_PREDICTIONS.get(soul_urge, SOUL_URGE_PREDICTIONS[9]),
        "personality": PERSONALITY_PREDICTIONS.get(personality, PERSONALITY_PREDICTIONS[9]),
    }

    return {
        "life_path": life_path,
        "destiny": destiny,
        "soul_urge": soul_urge,
        "personality": personality,
        "predictions": predictions,
    }
