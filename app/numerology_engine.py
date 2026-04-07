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


# Mobile number vibration predictions keyed by reduced number
MOBILE_PREDICTIONS = {
    1: {
        "prediction": (
            "Your mobile number carries the vibration of leadership and independence. "
            "This number attracts opportunities for new beginnings, self-employment, and pioneering ventures. "
            "Calls and messages received on this number often bring proposals, business leads, and invitations to take charge."
        ),
        "lucky_qualities": ["Leadership", "Independence", "Ambition", "Originality", "Confidence"],
        "challenges": ["Stubbornness", "Isolation", "Over-dominance"],
        "best_for": "Entrepreneurs, CEOs, freelancers, and anyone starting a new venture",
        "compatibility_numbers": [1, 3, 5, 9],
    },
    2: {
        "prediction": (
            "Your mobile number resonates with diplomacy and partnership. "
            "This vibration attracts cooperation, emotional connections, and harmonious relationships. "
            "You may notice an increase in calls related to collaboration, mediation, and heartfelt conversations."
        ),
        "lucky_qualities": ["Diplomacy", "Sensitivity", "Cooperation", "Intuition", "Peacemaking"],
        "challenges": ["Indecisiveness", "Over-sensitivity", "Dependency"],
        "best_for": "Counselors, mediators, artists, and those seeking deep personal relationships",
        "compatibility_numbers": [2, 4, 6, 8],
    },
    3: {
        "prediction": (
            "Your mobile number vibrates with creativity and self-expression. "
            "This number attracts social invitations, artistic opportunities, and joyful communication. "
            "Expect lively conversations, networking calls, and creative collaborations through this number."
        ),
        "lucky_qualities": ["Creativity", "Joy", "Communication", "Optimism", "Social magnetism"],
        "challenges": ["Scattered energy", "Superficiality", "Overspending"],
        "best_for": "Writers, speakers, marketers, social media professionals, and entertainers",
        "compatibility_numbers": [1, 3, 5, 9],
    },
    4: {
        "prediction": (
            "Your mobile number carries the vibration of stability and hard work. "
            "This number attracts steady opportunities, reliable contacts, and structured progress. "
            "Calls received tend to involve practical matters, contracts, and long-term commitments."
        ),
        "lucky_qualities": ["Discipline", "Reliability", "Organization", "Patience", "Loyalty"],
        "challenges": ["Rigidity", "Overthinking", "Resistance to change"],
        "best_for": "Accountants, engineers, project managers, and anyone building long-term foundations",
        "compatibility_numbers": [2, 4, 6, 8],
    },
    5: {
        "prediction": (
            "Your mobile number vibrates with freedom and adventure. "
            "This number attracts exciting news, travel opportunities, and dynamic change. "
            "You may receive unexpected calls that open doors to new experiences and diverse connections."
        ),
        "lucky_qualities": ["Versatility", "Adventure", "Freedom", "Resourcefulness", "Curiosity"],
        "challenges": ["Restlessness", "Impulsiveness", "Lack of commitment"],
        "best_for": "Travelers, sales professionals, journalists, and those in dynamic industries",
        "compatibility_numbers": [1, 3, 5, 7],
    },
    6: {
        "prediction": (
            "Your mobile number resonates with love, family, and responsibility. "
            "This vibration attracts nurturing relationships, domestic harmony, and community connections. "
            "Calls often involve family matters, caregiving, and opportunities to help others."
        ),
        "lucky_qualities": ["Compassion", "Responsibility", "Harmony", "Nurturing", "Aesthetics"],
        "challenges": ["Over-sacrifice", "Worry", "Controlling tendencies"],
        "best_for": "Teachers, healers, interior designers, and family-oriented professionals",
        "compatibility_numbers": [2, 4, 6, 9],
    },
    7: {
        "prediction": (
            "Your mobile number carries the vibration of wisdom and spiritual seeking. "
            "This number attracts thoughtful conversations, research opportunities, and introspective connections. "
            "Calls may bring intellectual stimulation and invitations for deep, meaningful exchanges."
        ),
        "lucky_qualities": ["Wisdom", "Intuition", "Analysis", "Spiritual depth", "Mystery"],
        "challenges": ["Isolation", "Suspicion", "Emotional detachment"],
        "best_for": "Researchers, spiritual practitioners, analysts, and philosophers",
        "compatibility_numbers": [3, 5, 7, 9],
    },
    8: {
        "prediction": (
            "Your mobile number vibrates with abundance and karmic power. "
            "This number attracts financial opportunities, authority, and material success. "
            "Expect calls related to business deals, investments, and positions of influence."
        ),
        "lucky_qualities": ["Authority", "Abundance", "Business acumen", "Determination", "Manifestation"],
        "challenges": ["Workaholism", "Materialism", "Power struggles"],
        "best_for": "Business owners, investors, bankers, and corporate executives",
        "compatibility_numbers": [2, 4, 6, 8],
    },
    9: {
        "prediction": (
            "Your mobile number resonates with humanitarianism and universal love. "
            "This vibration attracts compassionate connections, global opportunities, and service-oriented calls. "
            "You may receive requests for guidance, charity, and cross-cultural collaboration."
        ),
        "lucky_qualities": ["Compassion", "Generosity", "Global vision", "Idealism", "Completion"],
        "challenges": ["Over-idealism", "Emotional burnout", "Difficulty letting go"],
        "best_for": "NGO workers, doctors, teachers, and anyone in humanitarian service",
        "compatibility_numbers": [1, 3, 6, 9],
    },
    11: {
        "prediction": (
            "Master Number 11 — Your mobile number carries the vibration of spiritual illumination and visionary insight. "
            "This is a highly charged number that attracts intuitive messages, inspired connections, and opportunities "
            "for spiritual leadership. Calls may feel synchronistic and deeply meaningful."
        ),
        "lucky_qualities": ["Visionary insight", "Spiritual awareness", "Inspiration", "Charisma", "Enlightenment"],
        "challenges": ["Nervous tension", "Hypersensitivity", "Anxiety"],
        "best_for": "Spiritual leaders, artists, innovators, and visionary entrepreneurs",
        "compatibility_numbers": [2, 4, 6, 11, 22],
    },
    22: {
        "prediction": (
            "Master Number 22 — Your mobile number vibrates with the power of the Master Builder. "
            "This extraordinary number attracts large-scale opportunities, influential contacts, and projects "
            "that can shape communities. Calls received often involve ambitious plans and transformative partnerships."
        ),
        "lucky_qualities": ["Master building", "Practical idealism", "Global impact", "Discipline", "Vision"],
        "challenges": ["Overwhelm", "Perfectionism", "Fear of failure"],
        "best_for": "Architects, city planners, large-scale project leaders, and social reformers",
        "compatibility_numbers": [4, 6, 8, 11, 22],
    },
    33: {
        "prediction": (
            "Master Number 33 — Your mobile number carries the vibration of the Master Teacher. "
            "This sacred number attracts healing relationships, teaching opportunities, and calls for selfless service. "
            "Conversations through this number tend to uplift, heal, and inspire both caller and receiver."
        ),
        "lucky_qualities": ["Healing", "Selfless service", "Master teaching", "Unconditional love", "Upliftment"],
        "challenges": ["Self-sacrifice", "Emotional overwhelm", "Martyrdom"],
        "best_for": "Healers, spiritual teachers, counselors, and humanitarian leaders",
        "compatibility_numbers": [6, 9, 11, 22, 33],
    },
}


# ============================================================
# Mobile Numerology — Comprehensive Analysis (Batraa Reference)
# ============================================================

# Planetary friendship/enemy table
# Key = digit, value = dict with 'friends' and 'enemies' sets
PLANET_RELATIONSHIPS = {
    1: {"friends": {2, 3, 9}, "enemies": {4, 6, 8}},       # Sun
    2: {"friends": {1, 3}, "enemies": {4, 5, 8}},           # Moon
    3: {"friends": {1, 2, 9}, "enemies": {4, 5, 6, 8}},     # Jupiter
    4: {"friends": {5, 6, 7}, "enemies": {1, 2, 8, 9}},     # Rahu
    5: {"friends": {4, 6}, "enemies": {2, 3}},               # Mercury
    6: {"friends": {4, 5, 7, 8}, "enemies": {1, 3}},        # Venus
    7: {"friends": {4, 6}, "enemies": {1, 2, 8, 9}},        # Ketu
    8: {"friends": {5, 6}, "enemies": {1, 2, 4, 7, 9}},     # Saturn
    9: {"friends": {1, 2, 3}, "enemies": {4, 5, 8}},        # Mars
}


def _build_pair_combination_table():
    """Build the 00-99 digit-pair combination table (Benefic/Neutral/Malefic).

    Rules:
    - If BOTH digits consider each other friends (mutual) -> Benefic
    - If EITHER digit considers the other an enemy -> Malefic
    - Otherwise -> Neutral
    - Pairs with 0 are always Neutral (0 has no planetary ruler)
    - Same-digit pairs: Benefic if digit has friends with itself concept,
      otherwise Neutral. By convention same-digit pairs are Benefic for
      1,3,5,6,9 and Neutral for 2,4,7,8.
    """
    table = {}
    for i in range(10):
        for j in range(10):
            pair_str = f"{i}{j}"
            if i == 0 or j == 0:
                table[pair_str] = "Neutral"
                continue
            if i == j:
                # Same digit — Benefic for strong/friendly numbers, Neutral for others
                if i in {1, 3, 5, 6, 9}:
                    table[pair_str] = "Benefic"
                else:
                    table[pair_str] = "Neutral"
                continue

            rel_i = PLANET_RELATIONSHIPS[i]
            rel_j = PLANET_RELATIONSHIPS[j]

            # If either considers the other an enemy -> Malefic
            if j in rel_i["enemies"] or i in rel_j["enemies"]:
                table[pair_str] = "Malefic"
            # If both consider each other friends -> Benefic
            elif j in rel_i["friends"] and i in rel_j["friends"]:
                table[pair_str] = "Benefic"
            else:
                table[pair_str] = "Neutral"
    return table


PAIR_COMBINATION_TABLE = _build_pair_combination_table()


# Lucky colors per mobile total
LUCKY_COLORS = {
    1: ["Red", "Orange", "Gold"],
    2: ["White", "Silver", "Cream"],
    3: ["Yellow", "Orange", "Gold"],
    4: ["Blue", "Grey"],
    5: ["Green", "Light Green"],
    6: ["Pink", "White", "Light Blue"],
    7: ["Green", "Yellow", "White"],
    8: ["Black", "Dark Blue", "Dark Grey"],
    9: ["Red", "Orange", "Pink", "Coral"],
    11: ["White", "Silver", "Cream"],      # same as 2 (1+1)
    22: ["Blue", "Grey"],                   # same as 4 (2+2)
    33: ["Pink", "White", "Light Blue"],    # same as 6 (3+3)
}

# Unlucky colors per mobile total (opposite energy)
UNLUCKY_COLORS = {
    1: ["Black", "Dark Grey"],
    2: ["Red", "Dark Red"],
    3: ["Black", "Dark Blue"],
    4: ["Red", "Orange"],
    5: ["Red", "Orange"],
    6: ["Black", "Dark Grey"],
    7: ["Black", "Dark Red"],
    8: ["Red", "Orange", "Gold"],
    9: ["Black", "Dark Blue"],
    11: ["Red", "Dark Red"],
    22: ["Red", "Orange"],
    33: ["Black", "Dark Grey"],
}


# Lucky / Unlucky / Neutral numbers per mobile total (based on friendship table)
def _build_number_affinities():
    """For each mobile total (1-9, 11, 22, 33), classify digits 1-9."""
    affinities = {}
    for total in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        rel = PLANET_RELATIONSHIPS[total]
        affinities[total] = {
            "lucky": sorted(rel["friends"]),
            "unlucky": sorted(rel["enemies"]),
            "neutral": sorted({1, 2, 3, 4, 5, 6, 7, 8, 9} - rel["friends"] - rel["enemies"] - {total}),
        }
    # Master numbers map to their root
    affinities[11] = affinities[2]
    affinities[22] = affinities[4]
    affinities[33] = affinities[6]
    return affinities


NUMBER_AFFINITIES = _build_number_affinities()


# Recommended totals based on DOB life path number
RECOMMENDED_TOTALS = {
    1: [1, 3, 5, 9],
    2: [1, 2, 3, 7],
    3: [1, 3, 5, 9],
    4: [4, 5, 6, 7],
    5: [1, 5, 6, 9],
    6: [4, 5, 6, 8],
    7: [4, 6, 7],
    8: [5, 6, 8],
    9: [1, 3, 5, 9],
    11: [1, 2, 3, 7],   # same as 2
    22: [4, 5, 6, 7],   # same as 4
    33: [4, 5, 6, 8],   # same as 6
}


# Standard Loshu Magic Square layout (positions for digits 1-9)
LOSHU_GRID_LAYOUT = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]

# Vedic Grid layout
VEDIC_GRID_LAYOUT = [
    [3, 1, 9],
    [0, 7, 0],   # 0 = empty position
    [2, 8, 0],   # 0 = empty position
]


# Affirmations for areas of struggle
AFFIRMATIONS = {
    "health": (
        "I am healthy and full of energy. Every cell in my body vibrates with "
        "health and vitality. I nourish my body with wholesome food and pure water. "
        "I exercise regularly and my body responds with strength and endurance. "
        "I release all tension and stress from my body. I sleep deeply and wake "
        "refreshed. My immune system is strong and protects me from illness. "
        "I am grateful for my healthy body and treat it with love and respect. "
        "Every day, in every way, I am getting healthier and stronger."
    ),
    "relationship": (
        "I deserve real and authentic love. I attract loving, kind, and supportive "
        "people into my life. My relationships are built on mutual respect, trust, "
        "and genuine affection. I communicate openly and honestly with my partner. "
        "I release all past hurts and open my heart to new love. I am worthy of "
        "deep, meaningful connections. I give love freely and receive it graciously. "
        "My relationships bring joy, growth, and fulfillment to my life. "
        "I am surrounded by people who truly care about me."
    ),
    "career": (
        "There are so many great career opportunities available to me right now. "
        "I am confident in my skills and abilities. I attract success and abundance "
        "in my professional life. My work is meaningful and fulfilling. I am "
        "recognized and appreciated for my contributions. I grow and advance in "
        "my career with ease. I am open to new possibilities and embrace change "
        "as an opportunity for growth. My career path aligns with my purpose "
        "and passion. I create value wherever I go."
    ),
    "money": (
        "I experience wealth as a key part of my life. Money flows to me easily "
        "and abundantly. I am a magnet for financial prosperity. I manage my "
        "finances wisely and make sound investment decisions. I release all "
        "limiting beliefs about money and abundance. I deserve to be financially "
        "free and secure. Multiple streams of income flow into my life. I am "
        "grateful for the abundance that surrounds me. Wealth comes to me from "
        "expected and unexpected sources. I use my prosperity to create good "
        "in the world."
    ),
    "job": (
        "I am excited that every action I take moves me towards my perfect career. "
        "I attract the ideal job that matches my skills, values, and aspirations. "
        "My workplace is supportive and inspiring. I am valued and respected by "
        "my colleagues and superiors. I perform my duties with excellence and "
        "enthusiasm. Opportunities for advancement come to me naturally. I enjoy "
        "going to work each day. My job provides me with financial security and "
        "personal satisfaction. I am exactly where I need to be in my career "
        "journey, and the best is yet to come."
    ),
}


# Detailed predictions per mobile total (Batraa-style comprehensive readings)
MOBILE_PREDICTIONS_DETAILED = {
    1: (
        "Mobile Total 1 — The Leader's Number (Sun)\n\n"
        "Personality: You are a born leader with a magnetic personality. People are naturally "
        "drawn to your confidence and decisiveness. You have a strong sense of self and prefer "
        "to forge your own path rather than follow others.\n\n"
        "Career: This number is excellent for entrepreneurs, CEOs, government officials, and "
        "anyone in a leadership role. Calls received on this number often bring business "
        "proposals, partnership offers, and invitations to take charge of new projects.\n\n"
        "Relationships: You attract partners who admire your strength, but must guard against "
        "dominating relationships. Mutual respect is key. Family members look up to you for "
        "guidance and decision-making.\n\n"
        "Health: Strong vitality and constitution. Watch for stress-related issues due to "
        "overwork. Heart and eyes need attention. Regular breaks and meditation help maintain "
        "your energy.\n\n"
        "Finance: Money comes through personal effort and initiative. You are likely to build "
        "wealth through your own ventures rather than inheritance or luck. Investments in gold "
        "and government bonds suit you."
    ),
    2: (
        "Mobile Total 2 — The Diplomat's Number (Moon)\n\n"
        "Personality: You are sensitive, intuitive, and deeply empathetic. Your greatest "
        "strength lies in understanding others' emotions and mediating conflicts. You prefer "
        "harmony over confrontation.\n\n"
        "Career: Ideal for counselors, therapists, artists, musicians, and diplomats. This "
        "number attracts calls related to emotional support, creative collaboration, and "
        "partnership opportunities. Team-based work suits you best.\n\n"
        "Relationships: Deeply romantic and devoted. You form intense emotional bonds and "
        "value loyalty above all. Guard against mood swings and over-dependency on your "
        "partner's validation.\n\n"
        "Health: Pay attention to digestive health, water retention, and emotional well-being. "
        "The Moon's influence makes you susceptible to stress-induced ailments. Meditation, "
        "water therapy, and creative expression are healing.\n\n"
        "Finance: Wealth comes through partnerships and collaborative ventures rather than "
        "solo efforts. Investments in silver, pearls, and real estate near water bodies are "
        "auspicious."
    ),
    3: (
        "Mobile Total 3 — The Creative's Number (Jupiter)\n\n"
        "Personality: Optimistic, expressive, and socially magnetic. You light up any room "
        "you enter. Your natural charisma and communication skills make you an excellent "
        "networker and influencer.\n\n"
        "Career: Perfect for writers, speakers, marketers, teachers, and entertainers. This "
        "number attracts social invitations, media opportunities, and creative projects. "
        "You excel in roles that require public interaction.\n\n"
        "Relationships: Charming and popular, you attract many admirers. Romantic life is "
        "vibrant but you must guard against superficial connections. Seek depth over quantity "
        "in relationships.\n\n"
        "Health: Generally robust health blessed by Jupiter. Watch for liver-related issues, "
        "weight gain, and skin conditions. An active social life can lead to overindulgence — "
        "moderation is key.\n\n"
        "Finance: Jupiter blesses you with abundance and opportunities. Money comes through "
        "creative ventures, teaching, and advisory roles. Yellow sapphire and gold investments "
        "are favorable."
    ),
    4: (
        "Mobile Total 4 — The Builder's Number (Rahu)\n\n"
        "Personality: Unconventional, hardworking, and deeply analytical. You see the world "
        "differently and often challenge established norms. Rahu gives you a unique perspective "
        "and intense determination.\n\n"
        "Career: Suited for technology, research, occult sciences, and unconventional fields. "
        "This number attracts calls related to technical projects, innovation, and problem-solving. "
        "You may face sudden changes in career direction.\n\n"
        "Relationships: Relationships can be intense and sometimes unpredictable. You need a "
        "partner who understands your need for independence and can handle your unconventional "
        "nature. Loyalty runs deep once committed.\n\n"
        "Health: Rahu's influence can bring mysterious or hard-to-diagnose ailments. Mental "
        "health, nervous system, and sleep quality need attention. Grounding practices, "
        "routine, and nature walks are beneficial.\n\n"
        "Finance: Financial life may have sudden ups and downs. Wealth can come through "
        "technology, speculation (with caution), and unconventional business models. "
        "Avoid impulsive financial decisions."
    ),
    5: (
        "Mobile Total 5 — The Communicator's Number (Mercury)\n\n"
        "Personality: Quick-witted, versatile, and intellectually curious. You are a natural "
        "communicator who thrives on variety and mental stimulation. Adaptability is your "
        "superpower.\n\n"
        "Career: Excellent for sales, marketing, journalism, travel, trading, and any field "
        "requiring communication skills. This number attracts dynamic opportunities, travel "
        "plans, and networking calls. Business-related contacts increase.\n\n"
        "Relationships: You need intellectual stimulation in relationships. Boredom is your "
        "enemy. A partner who can match your mental agility and love of adventure will keep "
        "the spark alive.\n\n"
        "Health: Mercury governs the nervous system and respiratory tract. Watch for anxiety, "
        "skin allergies, and speech-related issues. Mental relaxation techniques and breathing "
        "exercises are recommended.\n\n"
        "Finance: Excellent business acumen. Money comes through trade, communication, and "
        "intellectual property. Green emerald and investments in communication or technology "
        "sectors are auspicious."
    ),
    6: (
        "Mobile Total 6 — The Lover's Number (Venus)\n\n"
        "Personality: Charming, artistic, and deeply devoted to beauty and harmony. Venus "
        "blesses you with aesthetic sensibility and a warm, loving nature. People find comfort "
        "in your presence.\n\n"
        "Career: Ideal for artists, designers, luxury goods, hospitality, beauty industry, "
        "and entertainment. This number attracts calls related to creative projects, romantic "
        "connections, and aesthetic endeavors.\n\n"
        "Relationships: Love is central to your life. You are a devoted partner who creates "
        "beautiful, harmonious relationships. Guard against possessiveness and the tendency "
        "to sacrifice too much for others.\n\n"
        "Health: Venus governs the reproductive system, kidneys, and throat. Maintain "
        "balance in diet and lifestyle. Luxury and indulgence can lead to health issues. "
        "Yoga and artistic expression are therapeutic.\n\n"
        "Finance: Wealth comes through beauty, art, luxury, and creative ventures. Diamond "
        "and white sapphire investments are favorable. Income through partnerships and "
        "marriage is also indicated."
    ),
    7: (
        "Mobile Total 7 — The Mystic's Number (Ketu)\n\n"
        "Personality: Deeply spiritual, introspective, and intuitive. Ketu gives you access "
        "to hidden knowledge and metaphysical understanding. You often feel like an old soul "
        "with wisdom beyond your years.\n\n"
        "Career: Suited for research, spiritual guidance, healing arts, astrology, and any "
        "field requiring deep analysis. This number attracts calls related to spiritual "
        "matters, research projects, and meaningful conversations.\n\n"
        "Relationships: You need a partner who respects your need for solitude and spiritual "
        "growth. Surface-level connections leave you unfulfilled. Deep, soulful bonds are "
        "what you seek.\n\n"
        "Health: Ketu can bring mysterious symptoms and psychosomatic conditions. Digestive "
        "system and nervous system need attention. Meditation, fasting, and spiritual "
        "practices are deeply healing for you.\n\n"
        "Finance: Material wealth is not your primary driver, yet it comes through spiritual "
        "or research-oriented work. Cat's eye gemstone is favorable. Avoid speculation and "
        "stick to stable investments."
    ),
    8: (
        "Mobile Total 8 — The Powerhouse Number (Saturn)\n\n"
        "Personality: Disciplined, ambitious, and enduring. Saturn gives you the resilience "
        "to overcome any obstacle. You are a late bloomer who achieves great success through "
        "persistent effort and patience.\n\n"
        "Career: Excellent for law, real estate, construction, mining, oil, and large-scale "
        "industries. This number attracts calls related to serious business matters, legal "
        "affairs, and long-term projects. Success comes after struggle.\n\n"
        "Relationships: Relationships may start slow but grow deeper with time. Saturn "
        "tests your bonds. Those who endure the initial challenges build unbreakable "
        "partnerships. Patience with your partner is essential.\n\n"
        "Health: Bones, joints, teeth, and chronic conditions fall under Saturn. Regular "
        "exercise, calcium-rich diet, and discipline in daily routine are essential. "
        "Avoid overwork — burnout is a real risk.\n\n"
        "Finance: Wealth accumulates slowly but surely. Saturn rewards patience and "
        "discipline. Blue sapphire (with caution) and investments in real estate, "
        "infrastructure, and established industries are favorable."
    ),
    9: (
        "Mobile Total 9 — The Warrior's Number (Mars)\n\n"
        "Personality: Courageous, passionate, and fiercely independent. Mars gives you "
        "tremendous energy, drive, and the fighting spirit to overcome any challenge. "
        "You are a natural protector and defender.\n\n"
        "Career: Ideal for military, police, sports, surgery, engineering, and any field "
        "requiring courage and physical energy. This number attracts calls related to "
        "competitive opportunities, physical activities, and leadership roles.\n\n"
        "Relationships: Passionate and intense in love. You need a partner who can match "
        "your energy and isn't intimidated by your strong personality. Channel Mars energy "
        "into protecting and supporting your loved ones.\n\n"
        "Health: Mars governs blood, muscles, and the head. Watch for injuries, "
        "inflammation, blood pressure, and anger-related stress. Regular physical exercise "
        "is essential to channel Mars energy constructively.\n\n"
        "Finance: Wealth comes through courage, competition, and leadership. Red coral "
        "and investments in real estate, land, and defense-related sectors are favorable. "
        "Avoid impulsive spending."
    ),
    11: (
        "Mobile Total 11 — Master Intuitive (Moon Amplified)\n\n"
        "Personality: You carry the heightened sensitivity of the Moon doubled. Master Number "
        "11 is one of the most intuitive vibrations in numerology. You possess visionary "
        "insight, spiritual awareness, and the ability to inspire others with your ideas.\n\n"
        "Career: Suited for spiritual leadership, counseling, art, music, and visionary "
        "entrepreneurship. This number attracts synchronistic calls and deeply meaningful "
        "connections that advance your life purpose.\n\n"
        "Relationships: Intensely emotional and spiritual bonds. You need a partner who "
        "understands your sensitivity and supports your higher calling. Guard against "
        "nervous tension and anxiety in relationships.\n\n"
        "Health: Heightened sensitivity means heightened vulnerability to stress. Nervous "
        "system, eyes, and emotional well-being need constant attention. Meditation and "
        "creative expression are non-negotiable.\n\n"
        "Finance: Money comes through inspired ideas and visionary projects. You may "
        "experience feast-or-famine cycles until you learn to ground your visions in "
        "practical reality."
    ),
    22: (
        "Mobile Total 22 — Master Builder (Rahu Amplified)\n\n"
        "Personality: The most powerful number in numerology. Master Number 22 combines "
        "the vision of 11 with the practical ability of 4. You can turn the grandest "
        "dreams into tangible reality.\n\n"
        "Career: Destined for large-scale projects — architecture, city planning, "
        "international business, and social reform. This number attracts contacts with "
        "influential people and opportunities to shape communities.\n\n"
        "Relationships: You need a partner who shares your grand vision or at least "
        "supports it. Ordinary domestic life may feel constraining. Find someone who "
        "understands your mission.\n\n"
        "Health: The intensity of this number can lead to exhaustion and burnout. "
        "Balance between work and rest is critical. Nervous system and mental health "
        "need proactive care.\n\n"
        "Finance: Massive wealth potential through large-scale ventures. Patience is "
        "key — your projects take time to bear fruit but the rewards are extraordinary."
    ),
    33: (
        "Mobile Total 33 — Master Teacher (Jupiter Amplified)\n\n"
        "Personality: The most spiritually evolved number. Master Number 33 embodies "
        "selfless love, healing wisdom, and the desire to uplift all of humanity. You "
        "are a natural healer and teacher.\n\n"
        "Career: Called to healing, teaching, counseling, and humanitarian service. This "
        "number attracts people seeking guidance, wisdom, and comfort. Your words carry "
        "profound healing power.\n\n"
        "Relationships: Unconditional love is your natural state, but guard against "
        "martyrdom. You must learn to receive love as freely as you give it. Set healthy "
        "boundaries.\n\n"
        "Health: Your health is tied to your emotional state. When you give too much "
        "without replenishing, burnout follows. Heart, thyroid, and immune system need "
        "attention. Self-care is not selfish.\n\n"
        "Finance: Money comes through service and teaching. You are not driven by "
        "material gain, yet the universe provides abundantly when you serve your "
        "highest purpose."
    ),
}


def _compute_loshu_grid(dob_digits: list) -> dict:
    """Compute Loshu Grid values from DOB digits.

    Returns dict with:
      - 'grid': the 3x3 Loshu layout [[4,9,2],[3,5,7],[8,1,6]]
      - 'values': {digit: repeated_string} e.g. {7: "77", 9: "9", 4: ""}
    """
    from collections import Counter
    counts = Counter(dob_digits)

    values = {}
    for d in range(1, 10):
        count = counts.get(d, 0)
        values[d] = str(d) * count if count > 0 else ""

    return {
        "grid": [row[:] for row in LOSHU_GRID_LAYOUT],
        "values": values,
    }


def _compute_vedic_grid(dob_digits: list) -> dict:
    """Compute Vedic Grid values from DOB digits.

    Returns dict with:
      - 'grid': the Vedic layout [[3,1,9],[0,7,0],[2,8,0]]
      - 'values': {digit: count} for digits present in the layout
    """
    from collections import Counter
    counts = Counter(dob_digits)

    # Vedic grid positions: only certain digits have slots
    vedic_positions = {3, 1, 9, 7, 2, 8}  # digits with slots in Vedic grid
    values = {}
    for d in range(0, 10):
        if d in vedic_positions:
            count = counts.get(d, 0)
            values[d] = str(d) * count if count > 0 else ""
        elif d == 0:
            values[d] = ""
        else:
            count = counts.get(d, 0)
            values[d] = str(d) * count if count > 0 else ""

    # Build the grid with DOB digit counts filling the positions
    grid = []
    for row in VEDIC_GRID_LAYOUT:
        grid_row = []
        for cell in row:
            if cell == 0:
                grid_row.append(0)
            else:
                grid_row.append(counts.get(cell, 0))
        grid.append(grid_row)

    return {
        "grid": grid,
        "values": values,
    }


def _extract_dob_digits(birth_date: str) -> list:
    """Extract individual digits from a YYYY-MM-DD date string, excluding 0."""
    return [int(ch) for ch in birth_date if ch.isdigit()]


def _extract_dob_digits_nonzero(birth_date: str) -> list:
    """Extract individual non-zero digits from a YYYY-MM-DD date string."""
    return [int(ch) for ch in birth_date if ch.isdigit() and ch != '0']


def calculate_mobile_numerology(
    phone_number: str,
    name: str = "",
    birth_date: str = "",
    areas_of_struggle: list = None,
) -> dict:
    """
    Comprehensive mobile number numerology analysis (Batraa reference style).

    Args:
        phone_number: Phone number string (any format — digits extracted automatically)
        name: Optional full name for personalization
        birth_date: Optional date of birth in YYYY-MM-DD format (enables DOB features)
        areas_of_struggle: Optional list of areas like ["health", "career", "money"]

    Returns:
        dict with compound_number, mobile_total, prediction, loshu_grid, vedic_grid,
        recommended_totals, lucky/unlucky analysis, missing_numbers,
        mobile_combinations, affirmations, and more.
    """
    if areas_of_struggle is None:
        areas_of_struggle = []

    # Strip all non-digit characters
    cleaned = ''.join(ch for ch in phone_number if ch.isdigit())
    if not cleaned:
        raise ValueError("Phone number must contain at least one digit.")

    # --- Compound number & mobile total ---
    compound_number = sum(int(d) for d in cleaned)

    mobile_total = compound_number
    while mobile_total > 9 and mobile_total not in MASTER_NUMBERS:
        mobile_total = sum(int(d) for d in str(mobile_total))

    # --- Prediction ---
    prediction = MOBILE_PREDICTIONS_DETAILED.get(
        mobile_total, MOBILE_PREDICTIONS_DETAILED[9]
    )

    # Also include the legacy structured prediction for backward compat
    legacy_entry = MOBILE_PREDICTIONS.get(mobile_total, MOBILE_PREDICTIONS[9])

    # --- Missing numbers (digits 0-9 not present in phone number) ---
    phone_digit_set = set(int(d) for d in cleaned)
    missing_numbers = sorted([d for d in range(10) if d not in phone_digit_set])

    # --- Mobile combinations (consecutive digit pairs) ---
    mobile_combinations = []
    for i in range(len(cleaned) - 1):
        pair = cleaned[i:i+2]
        combo_type = PAIR_COMBINATION_TABLE.get(pair, "Neutral")
        mobile_combinations.append({"pair": pair, "type": combo_type})

    has_malefic = any(c["type"] == "Malefic" for c in mobile_combinations)
    benefic_count = sum(1 for c in mobile_combinations if c["type"] == "Benefic")
    malefic_count = sum(1 for c in mobile_combinations if c["type"] == "Malefic")

    if has_malefic:
        recommendation = (
            "This Mobile Number is Not Recommended Because It Contains "
            "Malefic Combinations."
        )
    elif benefic_count >= len(mobile_combinations) // 2:
        recommendation = (
            "This Mobile Number is Highly Recommended. It Contains Mostly "
            "Benefic Combinations."
        )
    else:
        recommendation = (
            "This Mobile Number is Acceptable. It Contains Mostly Neutral "
            "Combinations With No Malefic Pairs."
        )

    # --- Lucky / Unlucky colors and numbers ---
    lucky_colors = LUCKY_COLORS.get(mobile_total, LUCKY_COLORS[9])
    unlucky_colors = UNLUCKY_COLORS.get(mobile_total, UNLUCKY_COLORS[9])
    affinities = NUMBER_AFFINITIES.get(mobile_total, NUMBER_AFFINITIES[9])
    lucky_numbers = affinities["lucky"]
    unlucky_numbers = affinities["unlucky"]
    neutral_numbers = affinities["neutral"]

    # --- DOB-based features (only if birth_date provided) ---
    loshu_data = None
    vedic_data = None
    recommended_totals = None
    is_recommended = None
    life_path = None

    if birth_date and '-' in birth_date:
        try:
            dob_all_digits = _extract_dob_digits(birth_date)
            dob_nonzero = _extract_dob_digits_nonzero(birth_date)

            # Loshu grid uses all DOB digits (including 0 handling in grid)
            loshu_data = _compute_loshu_grid(dob_nonzero)
            vedic_data = _compute_vedic_grid(dob_all_digits)

            # Life path for recommended totals
            life_path = _life_path(birth_date)
            recommended_totals = RECOMMENDED_TOTALS.get(
                life_path, RECOMMENDED_TOTALS[9]
            )
            is_recommended = mobile_total in recommended_totals
        except (ValueError, IndexError):
            # Invalid date — skip DOB features silently
            pass

    # --- Affirmations ---
    affirmations = {}
    valid_areas = {"health", "relationship", "career", "money", "job"}
    if areas_of_struggle:
        for area in areas_of_struggle:
            area_lower = area.lower().strip()
            if area_lower in valid_areas:
                affirmations[area_lower] = AFFIRMATIONS[area_lower]
    else:
        # Return all affirmations if no specific areas requested
        affirmations = dict(AFFIRMATIONS)

    # --- Build result ---
    result = {
        "phone_number": cleaned,
        "compound_number": compound_number,
        "mobile_total": mobile_total,
        "prediction": prediction,

        # Lucky / Unlucky analysis
        "lucky_colors": lucky_colors,
        "unlucky_colors": unlucky_colors,
        "lucky_numbers": lucky_numbers,
        "unlucky_numbers": unlucky_numbers,
        "neutral_numbers": neutral_numbers,

        # Missing numbers
        "missing_numbers": missing_numbers,

        # Mobile combinations
        "mobile_combinations": mobile_combinations,
        "has_malefic": has_malefic,
        "benefic_count": benefic_count,
        "malefic_count": malefic_count,
        "recommendation": recommendation,

        # Affirmations
        "affirmations": affirmations,

        # Legacy fields for backward compatibility
        "vibration_number": mobile_total,
        "total_sum": compound_number,
        "lucky_qualities": legacy_entry["lucky_qualities"],
        "challenges": legacy_entry["challenges"],
        "best_for": legacy_entry["best_for"],
        "compatibility_numbers": legacy_entry["compatibility_numbers"],
    }

    # DOB-based features (only present when birth_date provided)
    if loshu_data is not None:
        result["loshu_grid"] = loshu_data["grid"]
        result["loshu_values"] = loshu_data["values"]
    if vedic_data is not None:
        result["vedic_grid"] = vedic_data["grid"]
        result["vedic_values"] = vedic_data["values"]
    if recommended_totals is not None:
        result["recommended_totals"] = recommended_totals
        result["is_recommended"] = is_recommended
    if life_path is not None:
        result["life_path"] = life_path

    return result


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
