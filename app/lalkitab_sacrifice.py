"""
lalkitab_sacrifice.py — Bali Ka Bakra (Sacrificial Lamb Logic)
===============================================================
Sometimes a planet doesn't suffer itself but kills the significations
of another planet. The app shows:
"Your [PlanetA] is sacrificing [PlanetB]. Your [life_area_A]
is growing at the cost of your [life_area_B]."
"""
from typing import List, Dict, Any, Optional

# Life areas per planet
PLANET_LIFE_AREAS: Dict[str, Dict[str, str]] = {
    "Sun":     {"en": "soul, authority, father, career",     "hi": "आत्मा, अधिकार, पिता, करियर"},
    "Moon":    {"en": "mother, mental peace, emotions",       "hi": "माता, मानसिक शांति, भावनाएं"},
    "Mars":    {"en": "courage, siblings, property",          "hi": "साहस, भाई-बहन, संपत्ति"},
    "Mercury": {"en": "speech, intellect, wealth, trade",     "hi": "वाणी, बुद्धि, धन, व्यापार"},
    "Jupiter": {"en": "wisdom, children, dharma, guru",       "hi": "बुद्धि, संतान, धर्म, गुरु"},
    "Venus":   {"en": "wife, luxury, relationships, arts",    "hi": "पत्नी, विलासिता, संबंध, कला"},
    "Saturn":  {"en": "discipline, karma, longevity, work",   "hi": "अनुशासन, कर्म, दीर्घायु, काम"},
    "Rahu":    {"en": "worldly desires, obsession, foreign",  "hi": "सांसारिक इच्छाएं, जुनून, विदेश"},
    "Ketu":    {"en": "detachment, spirituality, liberation", "hi": "वैराग्य, आध्यात्मिकता, मोक्ष"},
}

# Sacrifice rules — each rule has conditions and a result
SACRIFICE_RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "LK_SAC_001_KETU_AFFLICT_SAC_MOON",
        "sacrificer": "Ketu",
        "victim": "Moon",
        "condition": "Ketu in 6/8/12 or conjunct Rahu",
        "check": lambda p_map, aspects: (
            p_map.get("Ketu", 0) in {6, 8, 12} or
            p_map.get("Ketu") == p_map.get("Rahu")
        ),
        "message": {
            "en": "Your Ketu is sacrificing Moon. Your detachment and spiritual drive grow at the cost of your mother's health and your own mental peace.",
            "hi": "आपका केतु चंद्रमा की बलि दे रहा है। आपका वैराग्य और आध्यात्मिक झुकाव माता के स्वास्थ्य और मानसिक शांति की कीमत पर बढ़ रहा है।"
        },
        "growth_area": "Ketu",
        "cost_area": "Moon",
        "severity": "high",
        "remedy": {"en": "Offer milk to Shiva on Mondays. Serve your mother. Keep silver at home.", "hi": "सोमवार को शिव को दूध अर्पित करें। माता की सेवा करें। घर में चांदी रखें।"},
    },
    {
        "rule_id": "LK_SAC_002_RAHU_KETU_SAME_HOUSE_SAC_VENUS",
        "sacrificer": "Rahu",
        "victim": "Venus",
        "condition": "Afflicted Rahu in same house as Ketu",
        "check": lambda p_map, aspects: (
            p_map.get("Rahu") == p_map.get("Ketu") and
            p_map.get("Rahu", 0) in {6, 8, 12}
        ),
        "message": {
            "en": "Your Rahu is sacrificing Venus. Your worldly ambitions and foreign connections grow at the expense of your marriage, relationships, and luxuries.",
            "hi": "आपका राहु शुक्र की बलि दे रहा है। आपकी सांसारिक महत्वाकांक्षाएं विवाह, संबंधों और विलासिता की कीमत पर बढ़ रही हैं।"
        },
        "growth_area": "Rahu",
        "cost_area": "Venus",
        "severity": "high",
        "remedy": {"en": "Donate white sweets on Fridays. Respect your partner. Place a rose quartz near the bed.", "hi": "शुक्रवार को सफेद मिठाई दान करें। साथी का सम्मान करें।"},
    },
    {
        "rule_id": "LK_SAC_003_JUP_3RD_NO_SUPPORT_SAC_MERCURY",
        "sacrificer": "Jupiter",
        "victim": "Mercury",
        "condition": "Jupiter in 3rd house",
        "check": lambda p_map, aspects: p_map.get("Jupiter") == 3,
        "message": {
            "en": "Your Jupiter is sacrificing Mercury. Your wisdom and spiritual growth expand at the cost of your speech, trade relationships, and 2nd house wealth.",
            "hi": "आपका गुरु बुध की बलि दे रहा है। आपकी बुद्धि और आध्यात्मिक विकास वाणी, व्यापारिक संबंधों और दूसरे घर के धन की कीमत पर बढ़ता है।"
        },
        "growth_area": "Jupiter",
        "cost_area": "Mercury",
        "severity": "medium",
        "remedy": {"en": "Keep green items near your workstation. Feed green vegetables to cows on Wednesdays.", "hi": "कार्यस्थल के पास हरी वस्तुएं रखें। बुधवार को गायों को हरी सब्जियां खिलाएं।"},
    },
    {
        "rule_id": "LK_SAC_004_SATURN_8_SAC_SUN",
        "sacrificer": "Saturn",
        "victim": "Sun",
        "condition": "Saturn in 8th house",
        "check": lambda p_map, aspects: p_map.get("Saturn") == 8,
        "message": {
            "en": "Your Saturn is sacrificing Sun. Your endurance and disciplined work grow, but authority, career advancement, and father's well-being suffer.",
            "hi": "आपका शनि सूर्य की बलि दे रहा है। आपकी सहनशक्ति बढ़ती है, लेकिन अधिकार, करियर और पिता का स्वास्थ्य पीड़ित होता है।"
        },
        "growth_area": "Saturn",
        "cost_area": "Sun",
        "severity": "medium",
        "remedy": {"en": "Offer water to Sun at sunrise for 41 days. Serve your father. Avoid conflict with authority.", "hi": "41 दिन सूर्योदय पर जल अर्पित करें। पिता की सेवा करें।"},
    },
    {
        "rule_id": "LK_SAC_005_MARS_12_SAC_MARS_SIBLINGS",
        "sacrificer": "Mars",
        "victim": "siblings",
        "condition": "Mars in 12th house",
        "check": lambda p_map, aspects: p_map.get("Mars") == 12,
        "message": {
            "en": "Your Mars is sacrificing sibling relationships. Your individual courage and independence grow at the cost of harmony with brothers/sisters.",
            "hi": "आपका मंगल भाई-बहन संबंधों की बलि दे रहा है। आपका साहस और स्वतंत्रता भाई-बहनों के साथ सद्भाव की कीमत पर बढ़ती है।"
        },
        "growth_area": "Mars",
        "cost_area": "siblings",
        "severity": "low",
        "remedy": {"en": "Donate red lentils on Tuesdays. Call your siblings more often. Help a brother or sister with a practical need.", "hi": "मंगलवार को लाल दाल दान करें। भाई-बहनों से अधिक संपर्क करें।"},
    },
    {
        "rule_id": "LK_SAC_006_RAHU_4_SAC_MOON_HOME",
        "sacrificer": "Rahu",
        "victim": "Moon",
        "condition": "Rahu in 4th house",
        "check": lambda p_map, aspects: p_map.get("Rahu") == 4,
        "message": {
            "en": "Your Rahu in the 4th is sacrificing Moon's domain. Foreign ambitions and unconventional thinking grow at the cost of domestic peace and mother's health.",
            "hi": "चौथे घर में राहु चंद्रमा के क्षेत्र की बलि दे रहा है। विदेशी महत्वाकांक्षाएं घरेलू शांति और माता के स्वास्थ्य की कीमत पर बढ़ती हैं।"
        },
        "growth_area": "Rahu",
        "cost_area": "Moon",
        "severity": "medium",
        "remedy": {"en": "Keep a silver bowl with water near the front door. Avoid keeping animals that disturb peace at home.", "hi": "दरवाजे के पास चांदी के कटोरे में पानी रखें।"},
    },
    {
        "rule_id": "LK_SAC_007_VENUS_6_SAC_RELATIONSHIPS",
        "sacrificer": "Venus",
        "victim": "Venus",
        "condition": "Venus in 6th house",
        "check": lambda p_map, aspects: p_map.get("Venus") == 6,
        "message": {
            "en": "Your Venus in the 6th house sacrifices its own significations. Work and service excel, but at the cost of marriage, luxury, and artistic fulfillment.",
            "hi": "छठे घर में शुक्र अपने ही कारकत्व की बलि देता है। काम और सेवा में श्रेष्ठता, लेकिन विवाह, विलासिता और कला की कीमत पर।"
        },
        "growth_area": "Venus",
        "cost_area": "Venus",
        "severity": "medium",
        "remedy": {"en": "Offer white flowers at a temple on Fridays. Invest time in creative hobbies. Honor your partner.", "hi": "शुक्रवार को मंदिर में सफेद फूल चढ़ाएं।"},
    },
    {
        "rule_id": "LK_SAC_008_MERCURY_8_SAC_SPEECH_WEALTH",
        "sacrificer": "Mercury",
        "victim": "Mercury",
        "condition": "Mercury in 8th house",
        "check": lambda p_map, aspects: p_map.get("Mercury") == 8,
        "message": {
            "en": "Your Mercury in the 8th sacrifices speech and surface-level wealth for hidden knowledge and research. Trade suffers; occult wisdom grows.",
            "hi": "आठवें घर में बुध वाणी और सतही धन की बलि देकर गुप्त ज्ञान और अनुसंधान के लिए देता है।"
        },
        "growth_area": "Mercury",
        "cost_area": "Mercury",
        "severity": "low",
        "remedy": {"en": "Recite Vishnu Sahasranama on Wednesdays. Keep green items at your workstation.", "hi": "बुधवार को विष्णु सहस्रनाम का पाठ करें।"},
    },
]


def analyze_sacrifice(
    planet_positions: List[Dict[str, Any]],
    aspects: Optional[Dict[str, List[str]]] = None
) -> List[Dict[str, Any]]:
    """
    Analyzes the chart for Bali Ka Bakra (sacrificial lamb) patterns.

    planet_positions: [{"planet": "Ketu", "house": 8}, ...]
    aspects: optional {planet: [list of planets it aspects]}

    Returns list of sacrifice results.
    """
    p_map = {p.get("planet", ""): p.get("house", 0) for p in planet_positions if p.get("planet")}
    asp = aspects or {}

    results = []
    for rule in SACRIFICE_RULES:
        try:
            if rule["check"](p_map, asp):
                sacrificer = rule["sacrificer"]
                victim = rule["victim"]
                growth_areas = PLANET_LIFE_AREAS.get(rule["growth_area"], {"en": rule["growth_area"], "hi": rule["growth_area"]})
                cost_areas = PLANET_LIFE_AREAS.get(rule["cost_area"], {"en": rule["cost_area"], "hi": rule["cost_area"]})

                results.append({
                    "rule_id": rule["rule_id"],
                    "sacrificer": sacrificer,
                    "victim": victim,
                    "severity": rule["severity"],
                    "condition": rule["condition"],
                    "message": rule["message"],
                    "growth_area": {"planet": rule["growth_area"], "areas": growth_areas},
                    "cost_area": {"planet": rule["cost_area"], "areas": cost_areas},
                    "remedy": rule["remedy"],
                })
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning("Sacrifice rule %s failed: %s", rule.get("rule_id"), e)
            continue

    return results
