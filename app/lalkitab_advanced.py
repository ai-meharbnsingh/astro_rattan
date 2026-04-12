"""
lalkitab_advanced.py -- Advanced Lal Kitab Logic Engine
========================================================
Implements "Pundit-level" logic including:
1. Masnui Grah (Artificial Planets)
2. Lal Kitab Rin (Karmic Debts)
3. Teva Typology (Andha/Dharmi Teva)
4. Prohibited Remedies (Precautions)
"""

from typing import Dict, List, Optional, Any

# ============================================================
# 1. MASNUI GRAH (ARTIFICIAL PLANETS)
# Reference: PDF 2.2.1
# ============================================================

MASNUI_MAPPING = [
    {
        "planets": {"Saturn", "Venus"}, 
        "result": "Jupiter", 
        "domain": {"en": "Children, wisdom, prosperity", "hi": "संतान, बुद्धि, समृद्धि"}
    },
    {
        "planets": {"Jupiter", "Venus"}, 
        "result": "Saturn", 
        "domain": {"en": "Delays, structure, maturity", "hi": "विलंब, संरचना, परिपक्वता"}
    },
    {
        "planets": {"Sun", "Mercury"}, 
        "result": "Mars", 
        "domain": {"en": "Courage, siblings, property", "hi": "साहस, भाई-बहन, संपत्ति"}
    },
    {
        "planets": {"Sun", "Mars"}, 
        "result": "Mercury", 
        "domain": {"en": "Intellect, commerce, health", "hi": "बुद्धि, वाणिज्य, स्वास्थ्य"}
    },
    {
        "planets": {"Saturn", "Mercury"}, 
        "result": "Venus", 
        "domain": {"en": "Partnerships, arts, wealth", "hi": "साझेदारी, कला, धन"}
    },
    {
        "planets": {"Moon", "Jupiter"}, 
        "result": "Sun", 
        "domain": {"en": "Vitality, career, father", "hi": "जीवन शक्ति, करियर, पिता"}
    },
    {
        "planets": {"Sun", "Jupiter"}, 
        "result": "Moon", 
        "domain": {"en": "Emotions, mother, public", "hi": "भावनाएं, माता, जनता"}
    },
    {
        "planets": {"Rahu", "Ketu"}, 
        "result": "Venus", 
        "domain": {"en": "Relationships, pleasures, addictions", "hi": "संबंध, सुख, व्यसन"}
    },
    {
        "planets": {"Mars", "Saturn"}, 
        "result": "Rahu", 
        "domain": {"en": "Foreign, accidents, upheaval", "hi": "विदेश, दुर्घटनाएं, उथल-पुथल"}
    },
    {
        "planets": {"Moon", "Saturn"}, 
        "result": "Ketu", 
        "domain": {"en": "Liberation, loss, meditation", "hi": "मुक्ति, हानि, ध्यान"}
    },
]

def calculate_masnui_planets(planet_positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Identifies artificial planets formed by conjunctions in the same house.
    """
    # Group planets by house
    house_map: Dict[int, set] = {}
    for p in planet_positions:
        h = p.get("house")
        if h:
            if h not in house_map:
                house_map[h] = set()
            house_map[h].add(p["planet"])

    results = []
    for house, planets in house_map.items():
        if len(planets) < 2:
            continue
            
        for rule in MASNUI_MAPPING:
            # Check if all required planets for the rule are in this house
            if rule["planets"].issubset(planets):
                results.append({
                    "house": house,
                    "formed_by": list(rule["planets"]),
                    "masnui_planet": rule["result"],
                    "affected_domain": rule["domain"]
                })
    
    return results

def calculate_karmic_debts(planet_positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Identifies the 9 types of Karmic Debts based on planetary triggers.
    Reference: PDF 2.3.1
    """
    # Helper to get planet's house
    p_map = {p["planet"]: p["house"] for p in planet_positions}
    
    # Helper to check if any of the planets are in a set of houses
    def in_houses(planets: List[str], houses: set) -> bool:
        return any(p_map.get(p) in houses for p in planets)

    debts = []

    # 1. Pitru Rin (Father's Debt)
    if in_houses(["Venus", "Mercury", "Rahu", "Ketu"], {2, 5, 9, 12}):
        debts.append({
            "name": {"hi": "पितृ ऋण", "en": "Pitru Rin"},
            "type": {"hi": "पिता / पूर्वज का ऋण", "en": "Father's / Forefather's Debt"},
            "reason": {"hi": "२, ५, ९, या १२वें भाव में शुक्र, बुध, राहु, या केतु", "en": "Venus, Mercury, Rahu, or Ketu in 2, 5, 9, or 12th house"},
            "manifestation": {"hi": "पारिवारिक इतिहास में मंदिर का विनाश, पीपल के पेड़ को नुकसान, पैतृक वंश में बाधाएं।", "en": "Temple destruction in family history, peepal tree damage, paternal lineage disruptions."},
            "remedy": {"hi": "पूरे परिवार से बराबर धन इकट्ठा करें और उसे एक ही दिन में किसी मंदिर में दान करें।", "en": "Collect equal money from all family members and donate it to a temple on the same day."}
        })

    # 2. Matru Rin (Mother's Debt)
    if p_map.get("Ketu") == 4:
        debts.append({
            "name": {"hi": "मातृ ऋण", "en": "Matru Rin"},
            "type": {"hi": "माता / मातृ ऋण", "en": "Mother's / Maternal Debt"},
            "reason": {"hi": "चौथे भाव में केतु", "en": "Ketu in 4th house"},
            "manifestation": {"hi": "मातृ उपेक्षा पैटर्न, माँ-बच्चे के संबंधों में कठिनाइयाँ, भावनात्मक सुरक्षा की कमी।", "en": "Maternal neglect patterns, mother-child relationship difficulties, emotional security deficits."},
            "remedy": {"hi": "पूरे परिवार से बराबर मात्रा में चांदी (या सिक्के) इकट्ठा करें और उसे बहते पानी में प्रवाहित करें।", "en": "Collect equal amounts of silver (or coins) from all family members and immerse it in flowing water."}
        })

    # 3. Sva Rin (Self Debt)
    if in_houses(["Venus", "Saturn", "Rahu"], {5}):
        debts.append({
            "name": {"hi": "स्व ऋण", "en": "Sva Rin"},
            "type": {"hi": "स्वयं का ऋण", "en": "Self Debt"},
            "reason": {"hi": "५वें भाव में शुक्र, शनि, या राहु", "en": "Venus, Saturn, or Rahu in 5th house"},
            "manifestation": {"hi": "नास्तिक प्रवृत्तियाँ, हृदय रोग, निर्दोष होने के बावजूद कानूनी दंड।", "en": "Atheistic tendencies, heart disease, legal penalties despite innocence."},
            "remedy": {"hi": "परिजनों से समान धन राशि एकत्र कर यज्ञ या सामूहिक पूजन कराएं।", "en": "Collect equal money from family members and perform a Yajna or community prayer."}
        })

    # 4. Bhratri Rin (Brother's Debt)
    if p_map.get("Mars") in {3, 6, 8, 12} and p_map.get("Saturn") in {3, 6, 8, 12}:
        debts.append({
            "name": {"hi": "भ्रातृ ऋण", "en": "Bhratri Rin"},
            "type": {"hi": "भाई / मित्र का ऋण", "en": "Brother's / Friend's Debt"},
            "reason": {"hi": "३, ६, ८, या १२वें भाव में मंगल और शनि", "en": "Mars and Saturn in 3, 6, 8, or 12th house"},
            "manifestation": {"hi": "बड़े भाई की अकाल मृत्यु, दोस्तों द्वारा विश्वासघात, भाई-बहनों द्वारा संपत्ति पर कब्जा।", "en": "Elder brother's early death, betrayal by friends, property seizure by siblings."},
            "remedy": {"hi": "परिजनों से समान मात्रा में तांबा या गुड़ एकत्र कर किसी धार्मिक स्थान पर दान करें।", "en": "Collect equal amounts of copper or jaggery from family members and donate to a religious place."}
        })

    # 5. Bhagini Rin (Sister's Debt)
    if p_map.get("Moon") in {3, 6} or (p_map.get("Rahu") in {3, 4, 6} and p_map.get("Mercury") in {3, 4, 6}):
        debts.append({
            "name": {"hi": "भगिनी ऋण", "en": "Bhagini Rin"},
            "type": {"hi": "बहन / पुत्री का ऋण", "en": "Sister's / Daughter's Debt"},
            "reason": {"hi": "३/६ में चंद्रमा या ३, ४, ६ में राहु-बुध की युति", "en": "Moon in 3/6 or Rahu-Mercury conjunction in 3, 4, 6"},
            "manifestation": {"hi": "बालिकाओं का शोषण, बहन के जन्म पर अशुभ घटनाएँ।", "en": "Exploitation of female children, inauspicious events at sister's birth."},
            "remedy": {"hi": "परिजनों से बराबर मात्रा में पीले रंग की कौड़ियाँ इकट्ठा करें, उन्हें जलाकर राख करें और उसी दिन बहते पानी में बहा दें।", "en": "Collect equal yellow sea shells (Kaudis) from family, burn them to ash, and immerse in flowing water on the same day."}
        })

    # 6. Deva Rin (Divine Debt)
    if p_map.get("Jupiter") in {6, 8, 12}:
        debts.append({
            "name": {"hi": "देव ऋण", "en": "Deva Rin"},
            "type": {"hi": "दिव्य / शिक्षक का ऋण", "en": "Divine / Teacher's Debt"},
            "reason": {"hi": "६, ८, या १२वें भाव में गुरु", "en": "Jupiter in 6, 8, or 12th house"},
            "manifestation": {"hi": "गुरु का विश्वासघात, पुजारी का अनादर, पवित्र वृक्ष का विनाश, गौ हत्या।", "en": "Guru betrayal, priest disrespect, sacred tree destruction, cow killing."},
            "remedy": {"hi": "परिजनों से बराबर मात्रा में हल्दी की गांठें या चने की दाल एकत्र कर किसी पुराने मंदिर में दान करें।", "en": "Collect equal pieces of turmeric or chana dal from family and donate to an old temple."}
        })

    # 7. Stree Rin (Women's Debt)
    if in_houses(["Sun", "Moon", "Rahu"], {2, 7}):
        debts.append({
            "name": {"hi": "स्त्री ऋण", "en": "Stree Rin"},
            "type": {"hi": "स्त्री ऋण", "en": "Women's Debt"},
            "reason": {"hi": "दूसरे या ७वें भाव में सूर्य, चंद्रमा, या राहु", "en": "Sun, Moon, or Rahu in 2nd or 7th house"},
            "manifestation": {"hi": "संबंधों में संघर्ष, विवाह में बाधाएं, महिलाओं के शोषण के पैटर्न।", "en": "Relationship conflicts, marriage obstacles, female exploitation patterns."},
            "remedy": {"hi": "परिजनों से बराबर धन एकत्र कर १०० सफेद गायों को एक समय का भोजन खिलाएं।", "en": "Collect equal money from family and feed 100 white cows once."}
        })

    # 8. Nara Rin (Humanity Debt)
    if p_map.get("Saturn") in {1, 2, 4, 7, 8, 12}:
        debts.append({
            "name": {"hi": "नरा ऋण", "en": "Nara Rin"},
            "type": {"hi": "मानवता का ऋण", "en": "Humanity Debt"},
            "reason": {"hi": "केंद्र या दुस्थान भावों में शनि", "en": "Saturn in angular or dusthana houses"},
            "manifestation": {"hi": "सामान्यीकृत जीवन बाधाएं, पुराना कष्ट, शापित होने की भावना।", "en": "Generalized life obstacles, chronic suffering, feeling of being cursed."},
            "remedy": {"hi": "परिजनों से बराबर राशि एकत्र कर अनाथालय या कोढ़ी आश्रम में दान करें।", "en": "Collect equal money from family and donate to an orphanage or leprosy center."}
        })

    # 9. Prakriti Rin (Nature Debt)
    if (p_map.get("Mercury") in {3, 6, 10, 12}) and (p_map.get("Rahu") in {3, 6, 10, 12} or p_map.get("Ketu") in {3, 6, 10, 12}):
        debts.append({
            "name": {"hi": "प्रकृति ऋण", "en": "Prakriti Rin"},
            "type": {"hi": "प्रकृति का ऋण", "en": "Nature Debt"},
            "reason": {"hi": "३, ६, १०, १२ में राहु/केतु के साथ पीड़ित बुध", "en": "Afflicted Mercury with Rahu/Ketu in 3, 6, 10, 12"},
            "manifestation": {"hi": "पिछले जन्मों में पर्यावरण का विनाश, पशु क्रूरता, प्राकृतिक आपदा की संवेदनशीलता।", "en": "Environmental destruction in past lives, animal cruelty, natural disaster vulnerability."},
            "remedy": {"hi": "परिजनों से बराबर धन एकत्र कर ४३ दिनों तक १०० कुत्तों को दूध और ब्रेड खिलाएं।", "en": "Collect equal money from family and feed 100 dogs milk and bread for 43 days."}
        })

    return debts

# ============================================================
# 3. TEVA TYPOLOGY (ANDHA / DHARMI) - Placeholder for next step
# ============================================================

def identify_teva_type(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detects if the chart is an Andha Teva (Blind) or Dharmi Teva (Religious).
    Reference: PDF 2.1.1, 2.1.2
    """
    p_map = {p["planet"]: p["house"] for p in planet_positions}
    
    # 1. Andha Teva Detection (Two or more enemies in 10th)
    planets_in_10 = [p["planet"] for p in planet_positions if p["house"] == 10]
    is_andha = len(planets_in_10) >= 2
    
    # 2. Dharmi Teva Detection
    is_dharmi = False
    # Path A: Jupiter + Saturn together
    if p_map.get("Jupiter") == p_map.get("Saturn") and p_map.get("Jupiter") is not None:
        is_dharmi = True
    # Path B: Specific auspicious placements
    elif p_map.get("Jupiter") in {6, 9, 11} or p_map.get("Saturn") in {9, 11}:
        is_dharmi = True

    return {
        "is_andha": is_andha,
        "is_dharmi": is_dharmi,
        "description": {
            "andha": {
                "hi": "करियर और सार्वजनिक छवि में मौलिक बाधा। सफलता के लिए गहन शनिवार के उपायों की आवश्यकता है।" if is_andha else "सामान्य कुंडली दृष्टि।",
                "en": "Fundamental obstruction in career and public image. Success requires intensive Saturday remedies." if is_andha else "Normal chart vision."
            },
            "dharmi": {
                "hi": "पूर्व जन्म के पुण्यों से जन्मजात सुरक्षा। यहाँ तक कि पापी ग्रह भी 'धर्मी ग्रह' (सुरक्षात्मक) के रूप में कार्य करते हैं।" if is_dharmi else "मानक कर्मिक प्रतिक्रिया।",
                "en": "Innate protection from past merit. Even malefic planets act as 'Dharmi Grah' (protective)." if is_dharmi else "Standard karmic responsiveness."
            }
        }
    }

# ============================================================
# 4. PROHIBITED REMEDIES (PRECAUTIONS) - Placeholder for next step
# ============================================================

def get_prohibitions(planet_positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Returns a list of forbidden actions/remedies based on house placements.
    Reference: PDF 2.4.1
    """
    p_map = {p["planet"]: p["house"] for p in planet_positions}
    prohibitions = []

    rules = [
        {
            "planet": "Moon", "house": {12}, "category": {"en": "Religious charity", "hi": "धार्मिक दान"}, 
            "item": {"en": "Donations to saints, temple construction", "hi": "साधु-संतों को दान, मंदिर निर्माण"}, 
            "risk": {"en": "Mental health crisis, poverty", "hi": "मानसिक स्वास्थ्य संकट, गरीबी"}
        },
        {
            "planet": "Jupiter", "house": {7}, "category": {"en": "Clothing charity", "hi": "वस्त्र दान"}, 
            "item": {"en": "Any clothing donation", "hi": "किसी भी प्रकार का वस्त्र दान"}, 
            "risk": {"en": "Financial loss, partnership destruction", "hi": "आर्थिक हानि, साझेदारी का विनाश"}
        },
        {
            "planet": "Sun", "house": {7, 8}, "category": {"en": "Timed donations", "hi": "समयबद्ध दान"}, 
            "item": {"en": "Morning/Evening donations specifically", "hi": "विशेष रूप से सुबह/शाम का दान"}, 
            "risk": {"en": "Authority loss, health crisis", "hi": "अधिकार की हानि, स्वास्थ्य संकट"}
        },
        {
            "planet": "Venus", "house": {9}, "category": {"en": "Female-targeted charity", "hi": "स्त्री-केंद्रित दान"}, 
            "item": {"en": "Financial aid to widows/poor girls", "hi": "विधवाओं/गरीब लड़कियों को वित्तीय सहायता"}, 
            "risk": {"en": "Progeny obstruction, marital conflict", "hi": "संतान प्राप्ति में बाधा, वैवाहिक कलह"}
        },
        {
            "planet": "Saturn", "house": {4}, "category": {"en": "Oil/Alcohol", "hi": "तेल/शराब"}, 
            "item": {"en": "Oil donations, serving liquor", "hi": "तेल का दान, शराब परोसना"}, 
            "risk": {"en": "Mother's health, property loss", "hi": "माता का स्वास्थ्य, संपत्ति की हानि"}
        },
        {
            "planet": "Mars", "house": {8}, "category": {"en": "Red/Copper", "hi": "लाल वस्तुएं/तांबा"}, 
            "item": {"en": "Red cloth, copper vessels", "hi": "लाल कपड़ा, तांबे के बर्तन"}, 
            "risk": {"en": "Accident proneness, blood diseases", "hi": "दुर्घटना की संभावना, रक्त रोग"}
        },
        {
            "planet": "Rahu", "house": {6}, "category": {"en": "Dark items", "hi": "काली वस्तुएं"}, 
            "item": {"en": "Blue/Black cloth, gemstone gifts", "hi": "नीला/काला कपड़ा, रत्न उपहार में देना"}, 
            "risk": {"en": "Legal entanglement, chronic disease", "hi": "कानूनी उलझन, पुरानी बीमारी"}
        },
        {
            "planet": "Ketu", "house": {12}, "category": {"en": "Warmth charity", "hi": "गर्मी/ऊनी दान"}, 
            "item": {"en": "Blankets, heating equipment", "hi": "कंबल, हीटिंग उपकरण"}, 
            "risk": {"en": "Sleep disorders, spiritual confusion", "hi": "नींद में खलल, आध्यात्मिक भ्रम"}
        },
        {
            "planet": "Mercury", "house": {3, 8, 9, 12}, "category": {"en": "Green items", "hi": "हरी वस्तुएं"}, 
            "item": {"en": "Money plant, green cloth, emerald", "hi": "मनी प्लांट, हरा कपड़ा, पन्ना"}, 
            "risk": {"en": "Sibling conflict, travel accidents", "hi": "भाई-बहनों से विवाद, यात्रा दुर्घटनाएं"}
        },
        {
            "planet": "Saturn", "house": {10}, "category": {"en": "Construction", "hi": "निर्माण"}, 
            "item": {"en": "House construction before age 48", "hi": "४८ वर्ष की आयु से पहले घर का निर्माण"}, 
            "risk": {"en": "Complete wealth destruction", "hi": "धन का पूर्ण विनाश"}
        },
        {
            "planet": "Jupiter", "house": {10}, "category": {"en": "Sympathetic feeding", "hi": "सह सहानुभूति भोजन"}, 
            "item": {"en": "Feeding others with emotional display", "hi": "भावनात्मक प्रदर्शन के साथ दूसरों को खिलाना"}, 
            "risk": {"en": "Severe suffering (Acts like poison)", "hi": "गंभीर कष्ट (जहर की तरह काम करता है)"}
        },
    ]

    for rule in rules:
        h = p_map.get(rule["planet"])
        if h in rule["house"]:
            prohibitions.append({
                "planet": rule["planet"],
                "house": h,
                "forbidden": rule["item"],
                "category": rule["category"],
                "backlash_risk": rule["risk"]
            })

    return prohibitions
