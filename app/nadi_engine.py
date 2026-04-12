"""
nadi_engine.py -- Nadi Astrology Interpretive Engine
=====================================================
Implements Nadi Astrology principles based on planetary conjunctions
and house relationships. Uses classical Nadi shlokas as interpretive 
overlays for natal charts.
"""

from typing import Any, Dict, List

# ── Classical Nadi Conjunction Rules ──────────────────────────
# Each rule: {planets: set, title_en, title_hi, desc_en, desc_hi}

NADI_RULES = [
    {
        "planets": {"Sun", "Mercury"},
        "title_en": "Budha-Aditya Yoga",
        "title_hi": "बुधादित्य योग",
        "desc_en": "High intelligence, administrative skills, and a career in communication or education.",
        "desc_hi": "उच्च बुद्धि, प्रशासनिक कौशल और संचार या शिक्षा के क्षेत्र में करियर।"
    },
    {
        "planets": {"Jupiter", "Mars"},
        "title_en": "Guru-Mangala Yoga",
        "title_hi": "गुरु-मंगल योग",
        "desc_en": "Noble character, leadership qualities, and success in legal or management fields.",
        "desc_hi": "नेक चरित्र, नेतृत्व गुण और कानूनी या प्रबंधन क्षेत्रों में सफलता।"
    },
    {
        "planets": {"Venus", "Mercury"},
        "title_en": "Lakshmi Yoga",
        "title_hi": "लक्ष्मी योग",
        "desc_en": "Artistic talent, refined speech, and prosperity through creative ventures.",
        "desc_hi": "कलात्मक प्रतिभा, परिष्कृत वाणी और रचनात्मक कार्यों के माध्यम से समृद्धि।"
    },
    {
        "planets": {"Saturn", "Jupiter"},
        "title_en": "Dharma-Karmadhipati Yoga",
        "title_hi": "धर्म-कर्माधिपति योग",
        "desc_en": "Success through ethical conduct, social responsibility, and respected positions.",
        "desc_hi": "नैतिक आचरण, सामाजिक जिम्मेदारी और सम्मानित पदों के माध्यम से सफलता।"
    },
    {
        "planets": {"Mars", "Moon"},
        "title_en": "Chandra-Mangala Yoga",
        "title_hi": "चंद्र-मंगल योग",
        "desc_en": "Courageous mind, success in commerce, and ability to handle complex emotional situations.",
        "desc_hi": "साहसी मन, वाणिज्य में सफलता और जटिल भावनात्मक स्थितियों को संभालने की क्षमता।"
    },
    {
        "planets": {"Sun", "Jupiter"},
        "title_en": "Jiva-Atma Yoga",
        "title_hi": "जीव-आत्मा योग",
        "desc_en": "Spiritual growth, wisdom from elders, and recognition in religious or ethical circles.",
        "desc_hi": "आध्यात्मिक विकास, बड़ों से ज्ञान, और धार्मिक या नैतिक हलकों में पहचान।"
    },
    {
        "planets": {"Saturn", "Mars"},
        "title_en": "Karma-Shakti Yoga",
        "title_hi": "कर्म-शक्ति योग",
        "desc_en": "Intense drive, technical skills, and success through rigorous discipline and hard work.",
        "desc_hi": "तीव्र इच्छाशक्ति, तकनीकी कौशल और कठोर अनुशासन और कड़ी मेहनत के माध्यम से सफलता।"
    }
]

def calculate_nadi_insights(planet_positions: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Identify Nadi shlokas / yogas based on planet placements in the same house.
    """
    # Group planets by house
    house_map: Dict[int, List[str]] = {}
    for planet, info in planet_positions.get("planets", {}).items():
        h = info.get("house")
        if h:
            if h not in house_map: house_map[h] = []
            house_map[h].append(planet)

    insights = []
    
    for house, planets in house_map.items():
        if len(planets) < 2:
            continue
            
        planet_set = set(planets)
        for rule in NADI_RULES:
            if rule["planets"].issubset(planet_set):
                insights.append({
                    "house": house,
                    "title_en": rule["title_en"],
                    "title_hi": rule["title_hi"],
                    "desc_en": rule["desc_en"],
                    "desc_hi": rule["desc_hi"],
                    "planets": list(rule["planets"])
                })
                
    return insights
