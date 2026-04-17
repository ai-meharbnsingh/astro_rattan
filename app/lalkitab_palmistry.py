"""
lalkitab_palmistry.py — Samudrik Shastra / Palmistry Integration
=================================================================
Correlates palm mounts and lines with Lal Kitab chart placements.
Original Lal Kitab title: "Lal Kitab Ke Farmaan (Samudrik)"
"""
from typing import List, Dict, Any

# ============================================================
# PALM ZONE DEFINITIONS
# Each zone maps to a planet and primary LK house
# ============================================================
#
# Coordinates are tuned for the frontend palm SVG whose viewBox is
# `0 0 220 300`. Mount centres sit on their anatomical locations
# inside the palm outline (fingers at the top, thumb on the left).
#
PALM_ZONES: List[Dict[str, Any]] = [
    # Mounts
    {
        "id": "jupiter_mount", "zone_type": "mount",
        "name": {"en": "Jupiter Mount", "hi": "गुरु पर्वत"},
        "location": {"en": "Base of index finger", "hi": "तर्जनी के नीचे"},
        "associated_planet": "Jupiter", "lk_house": 2,
        "svg_cx": 80, "svg_cy": 88,
        "keywords": {"en": "Wisdom, authority, prosperity", "hi": "बुद्धि, अधिकार, समृद्धि"},
    },
    {
        "id": "saturn_mount", "zone_type": "mount",
        "name": {"en": "Saturn Mount", "hi": "शनि पर्वत"},
        "location": {"en": "Base of middle finger", "hi": "मध्यमा के नीचे"},
        "associated_planet": "Saturn", "lk_house": 10,
        "svg_cx": 115, "svg_cy": 82,
        "keywords": {"en": "Discipline, career, karma", "hi": "अनुशासन, करियर, कर्म"},
    },
    {
        "id": "sun_mount", "zone_type": "mount",
        "name": {"en": "Sun Mount (Apollo)", "hi": "सूर्य पर्वत"},
        "location": {"en": "Base of ring finger", "hi": "अनामिका के नीचे"},
        "associated_planet": "Sun", "lk_house": 1,
        "svg_cx": 150, "svg_cy": 85,
        "keywords": {"en": "Fame, vitality, self", "hi": "प्रसिद्धि, जीवन शक्ति, स्व"},
    },
    {
        "id": "mercury_mount", "zone_type": "mount",
        "name": {"en": "Mercury Mount", "hi": "बुध पर्वत"},
        "location": {"en": "Base of little finger", "hi": "कनिष्ठा के नीचे"},
        "associated_planet": "Mercury", "lk_house": 7,
        "svg_cx": 185, "svg_cy": 100,
        "keywords": {"en": "Communication, business, intellect", "hi": "संचार, व्यापार, बुद्धि"},
    },
    {
        "id": "venus_mount", "zone_type": "mount",
        "name": {"en": "Venus Mount", "hi": "शुक्र पर्वत"},
        "location": {"en": "Base of thumb (thumb's fleshy part)", "hi": "अंगूठे का मांसल भाग"},
        "associated_planet": "Venus", "lk_house": 7,
        "svg_cx": 62, "svg_cy": 180,
        "keywords": {"en": "Love, beauty, luxury", "hi": "प्रेम, सुंदरता, विलासिता"},
    },
    {
        "id": "mars_inner", "zone_type": "mount",
        "name": {"en": "Inner Mars (Active)", "hi": "आंतरिक मंगल (सक्रिय)"},
        "location": {"en": "Above thumb, inner palm", "hi": "अंगूठे के ऊपर, आंतरिक हथेली"},
        "associated_planet": "Mars", "lk_house": 3,
        "svg_cx": 78, "svg_cy": 135,
        "keywords": {"en": "Courage, initiative, siblings", "hi": "साहस, पहल, भाई-बहन"},
    },
    {
        "id": "mars_outer", "zone_type": "mount",
        "name": {"en": "Outer Mars (Resistant)", "hi": "बाह्य मंगल (प्रतिरोधी)"},
        "location": {"en": "Opposite thumb, upper palm edge", "hi": "अंगूठे के सामने, ऊपरी किनारा"},
        "associated_planet": "Mars", "lk_house": 6,
        "svg_cx": 188, "svg_cy": 148,
        "keywords": {"en": "Endurance, obstacles, enemies", "hi": "सहनशक्ति, बाधाएं, शत्रु"},
    },
    {
        "id": "moon_mount", "zone_type": "mount",
        "name": {"en": "Moon Mount (Luna)", "hi": "चंद्र पर्वत"},
        "location": {"en": "Base of palm, opposite thumb", "hi": "हथेली का आधार, अंगूठे के सामने"},
        "associated_planet": "Moon", "lk_house": 4,
        "svg_cx": 185, "svg_cy": 215,
        "keywords": {"en": "Emotions, mother, imagination", "hi": "भावनाएं, माता, कल्पना"},
    },
    {
        "id": "rahu_mount", "zone_type": "mount",
        "name": {"en": "Rahu / Upper Mars (Plain)", "hi": "राहु / ऊपरी मंगल (मैदान)"},
        "location": {"en": "Center of palm", "hi": "हथेली का केंद्र"},
        "associated_planet": "Rahu", "lk_house": 12,
        "svg_cx": 125, "svg_cy": 170,
        "keywords": {"en": "Desires, foreign, shadow", "hi": "इच्छाएं, विदेश, छाया"},
    },
    # Lines — rendered as small markers at characteristic points of each line
    {
        "id": "heart_line", "zone_type": "line",
        "name": {"en": "Heart Line", "hi": "हृदय रेखा"},
        "location": {"en": "Top horizontal line", "hi": "ऊपरी क्षैतिज रेखा"},
        "associated_planet": "Venus", "lk_house": 7,
        "svg_cx": 125, "svg_cy": 112,
        "keywords": {"en": "Love, emotions, relationships", "hi": "प्रेम, भावनाएं, संबंध"},
    },
    {
        "id": "head_line", "zone_type": "line",
        "name": {"en": "Head Line", "hi": "मस्तिष्क रेखा"},
        "location": {"en": "Middle horizontal line", "hi": "मध्य क्षैतिज रेखा"},
        "associated_planet": "Mercury", "lk_house": 3,
        "svg_cx": 115, "svg_cy": 155,
        "keywords": {"en": "Intellect, focus, communication", "hi": "बुद्धि, एकाग्रता, संचार"},
    },
    {
        "id": "life_line", "zone_type": "line",
        "name": {"en": "Life Line", "hi": "जीवन रेखा"},
        "location": {"en": "Curved line around thumb", "hi": "अंगूठे के चारों ओर वक्र रेखा"},
        "associated_planet": "Saturn", "lk_house": 8,
        "svg_cx": 68, "svg_cy": 200,
        "keywords": {"en": "Vitality, health, longevity", "hi": "जीवन शक्ति, स्वास्थ्य, दीर्घायु"},
    },
    {
        "id": "fate_line", "zone_type": "line",
        "name": {"en": "Fate / Saturn Line", "hi": "भाग्य रेखा"},
        "location": {"en": "Vertical line from wrist upward", "hi": "कलाई से ऊपर की ओर"},
        "associated_planet": "Jupiter", "lk_house": 10,
        "svg_cx": 125, "svg_cy": 235,
        "keywords": {"en": "Destiny, career, direction", "hi": "भाग्य, करियर, दिशा"},
    },
    {
        "id": "sun_line", "zone_type": "line",
        "name": {"en": "Sun / Apollo Line", "hi": "सूर्य रेखा"},
        "location": {"en": "Vertical below ring finger", "hi": "अनामिका के नीचे"},
        "associated_planet": "Sun", "lk_house": 1,
        "svg_cx": 150, "svg_cy": 200,
        "keywords": {"en": "Fame, success, recognition", "hi": "प्रसिद्धि, सफलता, पहचान"},
    },
]

# ============================================================
# MARK TYPES: Benefic vs Malefic
# ============================================================
MARK_TYPES: Dict[str, Dict[str, Any]] = {
    "cross":     {"nature": "malefic",  "en": "Cross",     "hi": "क्रॉस",     "icon": "✕"},
    "island":    {"nature": "malefic",  "en": "Island",    "hi": "द्वीप",     "icon": "○"},
    "chain":     {"nature": "malefic",  "en": "Chain",     "hi": "जंजीर",     "icon": "⛓"},
    "dot":       {"nature": "malefic",  "en": "Black Dot", "hi": "काला बिंदु", "icon": "●"},
    "star":      {"nature": "mixed",    "en": "Star",      "hi": "तारा",      "icon": "★"},
    "triangle":  {"nature": "benefic",  "en": "Triangle",  "hi": "त्रिकोण",   "icon": "△"},
    "square":    {"nature": "benefic",  "en": "Square",    "hi": "चौकोर",     "icon": "□"},
    "trident":   {"nature": "benefic",  "en": "Trident",   "hi": "त्रिशूल",   "icon": "⎔"},
    "circle":    {"nature": "benefic",  "en": "Circle",    "hi": "वृत्त",     "icon": "◯"},
}

# ============================================================
# LK interpretation templates per mark + planet combination
# ============================================================
_MARK_PLANET_INTERP: Dict[str, Dict[str, Dict[str, str]]] = {
    "cross": {
        "Jupiter": {"en": "Jupiter's wisdom is blocked. Financial and spiritual obstacles present.", "hi": "गुरु की बुद्धि बाधित है। आर्थिक और आध्यात्मिक बाधाएं हैं।"},
        "Saturn":  {"en": "Karmic burden is heavy. Career progress is delayed by past-life debts.", "hi": "कर्म बोझ भारी है। करियर में विलंब पूर्वजन्म के ऋणों से है।"},
        "Sun":     {"en": "Authority is challenged. Health and vitality face recurring setbacks.", "hi": "अधिकार चुनौती में है। स्वास्थ्य और जीवन शक्ति में बार-बार असफलताएं।"},
        "Mercury": {"en": "Communication is distorted. Business ventures face unexpected betrayal.", "hi": "संचार विकृत है। व्यापारिक उद्यमों में अप्रत्याशित विश्वासघात।"},
        "Venus":   {"en": "Relationships are marked by sacrifice. Love life carries hidden burdens.", "hi": "रिश्तों में बलिदान का निशान है। प्रेम जीवन में छिपे बोझ हैं।"},
        "Mars":    {"en": "Aggressive energy turns inward. Accidents and surgical risks are elevated.", "hi": "आक्रामक ऊर्जा भीतर की ओर है। दुर्घटना और शल्य जोखिम बढ़े हुए हैं।"},
        "Moon":    {"en": "Emotional peace is disturbed. Mother's health or mental stability needs attention.", "hi": "मानसिक शांति भंग है। माता के स्वास्थ्य या मानसिक स्थिरता पर ध्यान दें।"},
        "Rahu":    {"en": "Obsessive patterns and foreign troubles. Hidden enemies operate from shadows.", "hi": "जुनूनी पैटर्न और विदेशी परेशानियां। छिपे शत्रु छाया में काम करते हैं।"},
        "Ketu":    {"en": "Spiritual confusion. Detachment is forced, not chosen. Past-life vows unfulfilled.", "hi": "आध्यात्मिक भ्रम। वैराग्य चुना नहीं बल्कि थोपा गया है।"},
    },
    "triangle": {
        "Jupiter": {"en": "Exceptional wisdom and timely wealth. Jupiter acts as Kayam in its house.", "hi": "असाधारण बुद्धि और समय पर धन। गुरु अपने घर में कायम की तरह कार्य करता है।"},
        "Saturn":  {"en": "Disciplined success through patience. Career achievements come in later years.", "hi": "धैर्य से अनुशासित सफलता। करियर की उपलब्धियां बाद के वर्षों में आती हैं।"},
        "Sun":     {"en": "Exceptional leadership. Public recognition and authority positions naturally attained.", "hi": "असाधारण नेतृत्व। सार्वजनिक पहचान और अधिकार पद स्वाभाविक रूप से प्राप्त।"},
        "Moon":    {"en": "Deep emotional intelligence. Intuition works as a guide in life decisions.", "hi": "गहरी भावनात्मक बुद्धि। अंतर्ज्ञान जीवन निर्णयों में मार्गदर्शक।"},
        "Venus":   {"en": "Blessed relationships. Marriage brings genuine happiness and material comfort.", "hi": "आशीर्वादित रिश्ते। विवाह वास्तविक खुशी और भौतिक आराम लाता है।"},
        "Mercury": {"en": "Sharp intellect and business acumen. Communication skills bring wealth.", "hi": "तीव्र बुद्धि और व्यावसायिक कुशलता। संचार कौशल धन लाते हैं।"},
        "Mars":    {"en": "Fearless courage channeled positively. Victories in legal and competitive matters.", "hi": "सकारात्मक रूप से निर्भीक साहस। कानूनी और प्रतिस्पर्धी मामलों में विजय।"},
        "Rahu":    {"en": "Unusual opportunities from foreign sources. Unconventional path to success.", "hi": "विदेशी स्रोतों से असामान्य अवसर। सफलता का अपरंपरागत मार्ग।"},
        "Ketu":    {"en": "Spiritual insights lead to liberation. Detachment used constructively.", "hi": "आध्यात्मिक अंतर्दृष्टि मुक्ति की ओर। वैराग्य का रचनात्मक उपयोग।"},
    },
    "star": {
        "Jupiter": {"en": "Sudden good fortune mixed with pride. Wisdom comes through sudden events.", "hi": "अचानक सौभाग्य अहंकार के साथ। बुद्धि अचानक घटनाओं से आती है।"},
        "Saturn":  {"en": "Sudden career breaks — can be promotion or downfall. Handle authority carefully.", "hi": "अचानक करियर का मोड़ — पदोन्नति या पतन हो सकता है। अधिकार सावधानी से संभालें।"},
        "Sun":     {"en": "Sudden fame. A star in Sun mount is a strong indicator of public recognition.", "hi": "अचानक प्रसिद्धि। सूर्य पर्वत पर तारा सार्वजनिक पहचान का मजबूत संकेत है।"},
        "Moon":    {"en": "Emotional intensity. Psychic sensitivity is heightened — can be gift or curse.", "hi": "भावनात्मक तीव्रता। मानसिक संवेदनशीलता बढ़ी — वरदान या अभिशाप हो सकती है।"},
        "Venus":   {"en": "A remarkable love affair. Partnership brings both joy and complexity.", "hi": "एक उल्लेखनीय प्रेम संबंध। साझेदारी खुशी और जटिलता दोनों लाती है।"},
        "Mercury": {"en": "Sudden intellectual breakthrough. Invention or creative discovery possible.", "hi": "अचानक बौद्धिक सफलता। आविष्कार या रचनात्मक खोज संभव।"},
        "Mars":    {"en": "War-like event. Major confrontation — could be triumph or traumatic wound.", "hi": "युद्ध जैसी घटना। बड़ी टकराहट — विजय या दर्दनाक घाव हो सकता है।"},
        "Rahu":    {"en": "Explosive events from hidden forces. Foreign incidents change life suddenly.", "hi": "छिपी शक्तियों से विस्फोटक घटनाएं। विदेशी घटनाएं जीवन अचानक बदलती हैं।"},
        "Ketu":    {"en": "Sudden spiritual awakening. A moment of deep realization changes perspective.", "hi": "अचानक आध्यात्मिक जागृति। गहरी अनुभूति का एक पल दृष्टिकोण बदलता है।"},
    },
}

def _get_default_interp(mark_nature: str, planet: str, house: int, lang: str = "en") -> str:
    if mark_nature == "malefic":
        msg = f"{planet} in house {house} is under pressure. Focus on {planet.lower()}-related remedies."
        msg_hi = f"{planet} घर {house} में दबाव में है। {planet} से संबंधित उपाय करें।"
    else:
        msg = f"{planet} in house {house} shows positive potential. Build on {planet.lower()}-related activities."
        msg_hi = f"{planet} घर {house} में सकारात्मक क्षमता दिखाता है।"
    return msg if lang == "en" else msg_hi


def get_palm_zones() -> List[Dict[str, Any]]:
    """Return all palm zones normalized to frontend-expected shape."""
    # Tuned for the frontend palm SVG viewBox 0 0 220 300 — mounts sized so
    # the four finger mounts (Jupiter/Saturn/Sun/Mercury) don't overlap.
    _SVG_R = {"mount": 15, "line": 9}
    return [
        {
            # canonical frontend fields
            "zone_id": z["id"],
            "planet": z["associated_planet"],
            "name": z["name"]["en"] if isinstance(z.get("name"), dict) else z.get("name", z["id"]),
            "name_hi": z["name"]["hi"] if isinstance(z.get("name"), dict) else "",
            "zone_type": z["zone_type"],
            "svg_cx": z["svg_cx"],
            "svg_cy": z["svg_cy"],
            "svg_r": _SVG_R.get(z["zone_type"], 15),
            # extras
            "lk_house": z["lk_house"],
            "location_en": z["location"]["en"] if isinstance(z.get("location"), dict) else "",
            "keywords_en": z["keywords"]["en"] if isinstance(z.get("keywords"), dict) else "",
        }
        for z in PALM_ZONES
    ]


def calculate_palm_correlations(
    planet_positions: List[Dict[str, Any]],
    palm_marks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Correlates palm marks with LK chart placements.

    planet_positions: [{"planet": "Jupiter", "house": 2}, ...]
    palm_marks: [{"zone_id": "jupiter_mount", "mark_type": "cross"}, ...]

    Returns: {correlations, overall_samudrik_score, summary}
    """
    p_map = {p.get("planet", ""): p.get("house", 0) for p in planet_positions if p.get("planet")}

    from app.lalkitab_advanced import PAKKA_GHAR

    correlations = []
    benefic_count = 0
    malefic_count = 0

    zone_map = {z["id"]: z for z in PALM_ZONES}

    for mark in palm_marks:
        zone_id = mark.get("zone_id", "")
        mark_type = mark.get("mark_type", "")
        zone = zone_map.get(zone_id)
        if not zone or mark_type not in MARK_TYPES:
            continue

        planet = zone["associated_planet"]
        mark_info = MARK_TYPES[mark_type]
        mark_nature = mark_info["nature"]
        planet_house = p_map.get(planet, zone["lk_house"])
        pakka = PAKKA_GHAR.get(planet, 0)
        is_in_pakka = (planet_house == pakka)
        is_in_enemy_zone = planet_house in {6, 8, 12}

        # Interpretation lookup
        interp_pool = _MARK_PLANET_INTERP.get(mark_type, {})
        if planet in interp_pool:
            interp_en = interp_pool[planet]["en"]
            interp_hi = interp_pool[planet]["hi"]
        else:
            interp_en = _get_default_interp(mark_nature, planet, planet_house, "en")
            interp_hi = _get_default_interp(mark_nature, planet, planet_house, "hi")

        # Kayam amplification
        kayam_note = None
        if is_in_pakka and mark_nature == "benefic":
            kayam_note = {"en": f"{planet} is in its Pakka Ghar (house {pakka}). This mark's positive energy is amplified — {planet} acts as Kayam.", "hi": f"{planet} अपने पक्के घर ({pakka}) में है। इस चिह्न की सकारात्मक ऊर्जा प्रवर्धित है — {planet} कायम की तरह कार्य करता है।"}
        elif is_in_pakka and mark_nature == "malefic":
            kayam_note = {"en": f"Warning: {planet} is in its Pakka Ghar but shows a {mark_type} on palm. Internal conflict between destiny and current path.", "hi": f"चेतावनी: {planet} अपने पक्के घर में है लेकिन हथेली पर {mark_type} दिखाता है।"}

        # Remedy needed?
        remedy_needed = (mark_nature == "malefic" and is_in_enemy_zone) or (mark_nature == "malefic" and not is_in_pakka)
        remedy = None
        if remedy_needed:
            remedy_map = {
                "Jupiter": {"en": "Feed yellow food (dal, banana) to poor on Thursdays.", "hi": "गुरुवार को गरीबों को पीला भोजन (दाल, केला) खिलाएं।"},
                "Saturn":  {"en": "Serve black sesame seeds (til) and oil to poor on Saturdays.", "hi": "शनिवार को गरीबों को काले तिल और तेल दें।"},
                "Sun":     {"en": "Offer water to Sun at sunrise with red flowers for 43 days.", "hi": "43 दिन सूर्योदय पर लाल फूलों से सूर्य को जल अर्पित करें।"},
                "Mercury": {"en": "Feed green vegetables to cows on Wednesdays.", "hi": "बुधवार को गायों को हरी सब्जियां खिलाएं।"},
                "Venus":   {"en": "Offer white flowers at a temple on Fridays.", "hi": "शुक्रवार को मंदिर में सफेद फूल चढ़ाएं।"},
                "Mars":    {"en": "Donate red lentils (masoor dal) on Tuesdays.", "hi": "मंगलवार को लाल मसूर दाल दान करें।"},
                "Moon":    {"en": "Offer milk to Shiva on Mondays. Keep silver with you.", "hi": "सोमवार को शिव को दूध अर्पित करें। चांदी साथ रखें।"},
                "Rahu":    {"en": "Donate blue/black items on Saturdays. Avoid non-veg food on Sundays.", "hi": "शनिवार को नीली/काली वस्तुएं दान करें।"},
                "Ketu":    {"en": "Feed dogs brown/yellow bread. Keep a dog if possible.", "hi": "कुत्तों को भूरी/पीली रोटी खिलाएं।"},
            }
            remedy = remedy_map.get(planet, {"en": "Consult a Lal Kitab expert for personalized remedy.", "hi": "व्यक्तिगत उपाय के लिए लाल किताब विशेषज्ञ से परामर्श लें।"})

        if mark_nature == "benefic":
            benefic_count += 1
        elif mark_nature == "malefic":
            malefic_count += 1
        # "mixed" nature counts as neither — no impact on score

        correlations.append({
            "zone_id": zone_id,
            "zone_name": zone["name"]["en"] if isinstance(zone.get("name"), dict) else zone.get("name", zone_id),
            "planet": planet,
            "mark_type": mark_type,
            "nature": mark_nature,
            "planet_house": planet_house,
            "is_in_pakka_ghar": is_in_pakka,
            "interpretation": {"en": interp_en, "hi": interp_hi},
            "kayam_note": kayam_note,
            "remedy_needed": remedy_needed,
            "remedy": remedy,
        })

    # Samudrik score: 50 + benefic*10 - malefic*10 clamped 0-100
    score = max(0, min(100, 50 + (benefic_count * 10) - (malefic_count * 10)))

    if score >= 70:
        summary_en = "Your palm shows predominantly positive signs. Your Lal Kitab chart is well-aligned with your physical destiny marks."
        summary_hi = "आपकी हथेली अधिकतर सकारात्मक चिह्न दिखाती है। आपकी लाल किताब कुंडली आपके भौतिक भाग्य चिह्नों से अच्छी तरह संरेखित है।"
    elif score >= 40:
        summary_en = "Your palm shows a mix of challenges and opportunities. Focus on the remedies listed below."
        summary_hi = "आपकी हथेली चुनौतियों और अवसरों का मिश्रण दिखाती है। नीचे सूचीबद्ध उपायों पर ध्यान दें।"
    else:
        summary_en = "Your palm shows significant karmic patterns. Consistent remedies are recommended."
        summary_hi = "आपकी हथेली महत्वपूर्ण कर्मिक पैटर्न दिखाती है। लगातार उपाय अनुशंसित हैं।"

    return {
        "correlations": correlations,
        "overall_samudrik_score": score,
        "benefic_count": benefic_count,
        "malefic_count": malefic_count,
        "summary": {"en": summary_en, "hi": summary_hi},
        "mark_types": MARK_TYPES,
    }
