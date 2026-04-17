"""
lalkitab_vastu.py — Makaan (Vastu) Directional Mapping
=======================================================
Maps Lal Kitab houses to compass directions and auto-generates
home layout diagnosis based on planetary positions.

Fixed house mapping (always 1=Aries):
  H1=East, H2=SE, H3=South, H4=SW, H5=West, H6=NW, H7=West(axis), H8=SW-deep,
  H9=North, H10=North(mid), H11=NE, H12=NE-far
Classical LK compass:
  H1=East, H4=South, H7=West, H10=North
"""
from typing import List, Dict, Any, Optional

# ─── Direction Mapping ────────────────────────────────────────────────────────

HOUSE_DIRECTION: Dict[int, Dict[str, str]] = {
    1:  {"en": "East",              "hi": "पूर्व",        "zone": "main_entrance"},
    2:  {"en": "South-East",        "hi": "दक्षिण-पूर्व", "zone": "kitchen"},
    3:  {"en": "South",             "hi": "दक्षिण",       "zone": "study"},
    4:  {"en": "South-West",        "hi": "दक्षिण-पश्चिम","zone": "master_bedroom"},
    5:  {"en": "West",              "hi": "पश्चिम",       "zone": "children_room"},
    6:  {"en": "North-West",        "hi": "उत्तर-पश्चिम", "zone": "guest_room"},
    7:  {"en": "West (partnership axis)", "hi": "पश्चिम (साझेदारी अक्ष)", "zone": "living_room"},
    8:  {"en": "Deep South-West",   "hi": "गहरा दक्षिण-पश्चिम", "zone": "storage_drain"},
    9:  {"en": "North",             "hi": "उत्तर",        "zone": "prayer_room"},
    10: {"en": "North (career axis)","hi": "उत्तर (करियर अक्ष)", "zone": "office_study"},
    11: {"en": "North-East",        "hi": "उत्तर-पूर्व",  "zone": "gains_corner"},
    12: {"en": "North-East (far)",  "hi": "उत्तर-पूर्व (दूर)", "zone": "hidden_corner"},
}

ZONE_LABEL: Dict[str, Dict[str, str]] = {
    "main_entrance":  {"en": "Main Entrance / Threshold", "hi": "मुख्य द्वार"},
    "kitchen":        {"en": "Kitchen / Fire Zone",        "hi": "रसोई / अग्नि क्षेत्र"},
    "study":          {"en": "Study / Communication Room", "hi": "अध्ययन कक्ष"},
    "master_bedroom": {"en": "Master Bedroom / Ancestral Corner", "hi": "मुख्य शयन कक्ष"},
    "children_room":  {"en": "Children's Room / Creative Corner", "hi": "बच्चों का कमरा"},
    "guest_room":     {"en": "Guest Room / Service Area",  "hi": "अतिथि कक्ष"},
    "living_room":    {"en": "Living Room / Partnership Space", "hi": "बैठक कक्ष"},
    "storage_drain":  {"en": "Storage / Drain / Dark Corner", "hi": "भंडार / नाला / अंधेरा कोना"},
    "prayer_room":    {"en": "Prayer Room / Altar",        "hi": "पूजा कक्ष / वेदी"},
    "office_study":   {"en": "Office / Career Corner",     "hi": "कार्यालय / करियर कोना"},
    "gains_corner":   {"en": "Gains Corner / North-East Light", "hi": "लाभ कोना / उत्तर-पूर्व प्रकाश"},
    "hidden_corner":  {"en": "Hidden / Spiritual Corner",  "hi": "छिपा / आध्यात्मिक कोना"},
}

# ─── Planet Vastu Diagnosis Rules ─────────────────────────────────────────────

# {planet: {house: {warning_en, warning_hi, fix_en, fix_hi}}}
_VASTU_PLANET_RULES: Dict[str, Dict[int, Dict[str, str]]] = {
    "Saturn": {
        8: {
            "warning_en": "Dark room, blocked drain, or heavy furniture in South-West. Saturn in 8th creates structural decay in hidden corners.",
            "warning_hi": "दक्षिण-पश्चिम में अंधेरा कमरा, बंद नाला, या भारी फर्नीचर। शनि 8वें में छिपे कोनों में क्षरण करता है।",
            "fix_en": "Clear all blocked drains in South-West. Ensure no dark, locked, or forgotten rooms. Hang a Shani yantra in South-West.",
            "fix_hi": "दक्षिण-पश्चिम के सभी नाले साफ करें। कोई अंधेरा, बंद, या भूला कमरा न हो। दक्षिण-पश्चिम में शनि यंत्र लगाएं।",
        },
        10: {
            "warning_en": "North area (career axis) has heavy or cold energy. Blocked career flow. Saturn in 10th suppresses North-facing ambitions.",
            "warning_hi": "उत्तर (करियर अक्ष) में भारी या ठंडी ऊर्जा। करियर प्रवाह बाधित। शनि 10वें में उत्तर की महत्वाकांक्षाएं दबाता है।",
            "fix_en": "Keep North direction clean and clutter-free. Add blue or black gemstones in North corner. Avoid dark paint in career zone.",
            "fix_hi": "उत्तर दिशा साफ और खुली रखें। उत्तर कोने में नीले/काले रत्न रखें।",
        },
        1: {
            "warning_en": "Main entrance may feel heavy or blocked. East energy is restricted by Saturn. Visitors may feel unwelcome.",
            "warning_hi": "मुख्य द्वार भारी या बाधित महसूस हो सकता है। शनि लग्न में पूर्वी ऊर्जा को प्रतिबंधित करता है।",
            "fix_en": "Paint main door black or dark blue. Hang iron horse-shoe above entrance. Keep threshold clean and uncluttered.",
            "fix_hi": "मुख्य द्वार को काला या गहरा नीला रंगें। ऊपर लोहे की नाल लगाएं।",
        },
    },
    "Rahu": {
        1: {
            "warning_en": "Main entrance may be broken, shadowed, or have missing threshold. Rahu in 1st creates illusion about the home's true state.",
            "warning_hi": "मुख्य द्वार टूटा, छाया में, या बिना चौखट का हो सकता है। राहु लग्न में घर की वास्तविक स्थिति के बारे में भ्रम पैदा करता है।",
            "fix_en": "Ensure main entrance is bright, undamaged, and has a clear threshold. Keep it free of shadows or obstructions.",
            "fix_hi": "मुख्य द्वार उज्ज्वल, अक्षत, और स्पष्ट चौखट सहित रखें। छाया और बाधाओं से मुक्त रखें।",
        },
        4: {
            "warning_en": "South-West (master bedroom) may have electrical issues, strange smells, or old objects. Rahu in 4th disturbs domestic peace.",
            "warning_hi": "दक्षिण-पश्चिम (मुख्य शयन कक्ष) में बिजली की समस्या, अजीब गंध, या पुरानी वस्तुएं हो सकती हैं।",
            "fix_en": "Remove old, unused, or inherited items from master bedroom. Ensure proper ventilation. Use camphor to purify.",
            "fix_hi": "शयन कक्ष से पुरानी, अनुपयोगी वस्तुएं हटाएं। उचित वेंटिलेशन सुनिश्चित करें। कपूर से शुद्धि करें।",
        },
        12: {
            "warning_en": "North-East hidden corner may have secrets, old newspapers, or electronic waste. Rahu in 12th feeds on disorder.",
            "warning_hi": "उत्तर-पूर्व के छिपे कोने में रहस्य, पुराने अखबार, या इलेक्ट्रॉनिक कचरा हो सकता है।",
            "fix_en": "Deep-clean North-East corner. Remove all clutter. Light a diya (lamp) in this corner daily.",
            "fix_hi": "उत्तर-पूर्व कोने की गहरी सफाई करें। सभी अनावश्यक वस्तुएं हटाएं। यहां रोज दीपक जलाएं।",
        },
    },
    "Mars": {
        4: {
            "warning_en": "South-West (master bedroom/kitchen zone) may have fire risk, sharp objects, or heated arguments. Mars in 4th ignites South-West.",
            "warning_hi": "दक्षिण-पश्चिम में आग का खतरा, तेज वस्तुएं, या गर्म बहस हो सकती है।",
            "fix_en": "Avoid open flames or sharp objects in South-West bedroom. Place a red cloth or coral stone. Keep kitchen fire under control.",
            "fix_hi": "दक्षिण-पश्चिम शयन कक्ष में खुली आग या तेज वस्तुएं न रखें। लाल कपड़ा या मूंगा रखें।",
        },
        7: {
            "warning_en": "West living room (partnership space) has aggressive energy. Mars in 7th creates heated disputes in shared spaces.",
            "warning_hi": "पश्चिम बैठक (साझेदारी स्थान) में आक्रामक ऊर्जा है। मंगल 7वें में साझा स्थानों में गर्म विवाद पैदा करता है।",
            "fix_en": "Hang triangular or red-themed artwork in West. Avoid sharp corners in furniture. Place coral or red coral decorations.",
            "fix_hi": "पश्चिम में त्रिकोणीय या लाल-थीम कलाकृति लगाएं। फर्नीचर में तीखे कोने न हों।",
        },
    },
    "Ketu": {
        6: {
            "warning_en": "North-West (service/guest zone) may have pest issues, old medicines, or karmic residue. Ketu in 6th creates hidden contamination.",
            "warning_hi": "उत्तर-पश्चिम (अतिथि/सेवा क्षेत्र) में कीट, पुरानी दवाइयां, या कर्मिक अवशेष हो सकते हैं।",
            "fix_en": "Pest-proof North-West. Remove all old medicines or chemicals. Burn camphor in this zone monthly.",
            "fix_hi": "उत्तर-पश्चिम को कीट-मुक्त करें। पुरानी दवाइयां और रसायन हटाएं। मासिक कपूर जलाएं।",
        },
        4: {
            "warning_en": "South-West may hold ancestral burdens — old photographs, inherited furniture carrying unresolved karma.",
            "warning_hi": "दक्षिण-पश्चिम में पैतृक बोझ — पुरानी तस्वीरें, विरासती फर्नीचर जो अनसुलझे कर्म धारण करता है।",
            "fix_en": "Conduct annual Pitru-shanti in South-West. Remove or respectfully retire very old family photos from bedroom walls.",
            "fix_hi": "दक्षिण-पश्चिम में वार्षिक पितृ-शांति करें। बहुत पुरानी पारिवारिक तस्वीरें शयन कक्ष की दीवारों से हटाएं।",
        },
    },
    "Jupiter": {
        10: {
            "warning_en": "CRITICAL: Jupiter in 10th — do NOT install a temple or shrine inside the home. It will ruin career. External prayer only.",
            "warning_hi": "महत्वपूर्ण: गुरु 10वें में — घर के अंदर मंदिर या मूर्ति स्थापित न करें। यह करियर नष्ट करेगा। बाहरी पूजा करें।",
            "fix_en": "If you have an indoor temple, move it outside or to a nearby temple. Keep North zone (career) free of religious idols.",
            "fix_hi": "यदि घर में मंदिर है, उसे बाहर या पास के मंदिर में स्थानांतरित करें। उत्तर क्षेत्र (करियर) को धार्मिक मूर्तियों से मुक्त रखें।",
        },
        4: {
            "warning_en": "South-West (ancestral zone) blessed by Jupiter. Excellent placement — maintain a clean, peaceful bedroom.",
            "warning_hi": "दक्षिण-पश्चिम (पैतृक क्षेत्र) गुरु से आशीर्वादित। शयन कक्ष स्वच्छ और शांतिपूर्ण बनाए रखें।",
            "fix_en": "Place yellow flowers or a small Vishnu image in South-West bedroom. This strengthens Jupiter's blessing.",
            "fix_hi": "दक्षिण-पश्चिम शयन कक्ष में पीले फूल या छोटी विष्णु प्रतिमा रखें।",
        },
    },
    "Moon": {
        8: {
            "warning_en": "South-West deep corner may have water leakage, damp walls, or basement water. Moon in 8th — never accept free milk or silver from strangers.",
            "warning_hi": "दक्षिण-पश्चिम में पानी का रिसाव, नम दीवारें, या तहखाने में पानी हो सकता है। चंद्र 8वें — अजनबियों से मुफ्त दूध या चांदी स्वीकार न करें।",
            "fix_en": "Fix all water leaks in South-West. Never store water in South-West corner. Keep this zone dry.",
            "fix_hi": "दक्षिण-पश्चिम के सभी पानी के रिसाव ठीक करें। इस कोने में पानी संग्रहीत न करें। इसे सूखा रखें।",
        },
        4: {
            "warning_en": "South-West master bedroom benefits from Moon — but ensure no water storage here. Moon in 4th: family emotional health depends on bedroom peace.",
            "warning_hi": "दक्षिण-पश्चिम शयन कक्ष में चंद्र लाभदायक है — लेकिन यहां पानी भंडारण नहीं। परिवार का भावनात्मक स्वास्थ्य शयन कक्ष की शांति पर निर्भर।",
            "fix_en": "Keep a small water vessel (silver bowl) in North area instead of bedroom. Moonlight should enter master bedroom.",
            "fix_hi": "चांदी का छोटा पात्र उत्तर क्षेत्र में रखें, शयन कक्ष में नहीं। चंद्र की रोशनी शयन कक्ष में आने दें।",
        },
    },
    "Sun": {
        5: {
            "warning_en": "West children's room / creative corner: excessive authority or anger blocks creative growth. Sun in 5th — avoid blunt truth-telling to preserve luck.",
            "warning_hi": "पश्चिम बच्चों का कमरा: अत्यधिक अधिकार या क्रोध रचनात्मक विकास को रोकता है। सूर्य 5वें — भाग्य बचाने के लिए कठोर सत्य बोलने से बचें।",
            "fix_en": "Place a copper sun symbol in East (H1). Avoid storing political or authority documents in West zone.",
            "fix_hi": "पूर्व में तांबे का सूर्य प्रतीक रखें। पश्चिम क्षेत्र में राजनीतिक या अधिकार दस्तावेज न रखें।",
        },
        1: {
            "warning_en": "East main entrance blessed by Sun — keep it well-lit and clean. Sun in 1st amplifies home's East vitality.",
            "warning_hi": "पूर्व मुख्य द्वार सूर्य से आशीर्वादित — इसे अच्छी तरह से रोशन और स्वच्छ रखें।",
            "fix_en": "Offer water to rising Sun from East-facing entrance. Keep copper vessel near East window.",
            "fix_hi": "पूर्व-मुखी द्वार से उगते सूर्य को जल अर्पण करें। पूर्व खिड़की के पास तांबे का पात्र रखें।",
        },
    },
    "Venus": {
        7: {
            "warning_en": "West living room (Venus Pakka Ghar in 7th): excellent for partnerships and creative décor. Keep this area beautiful.",
            "warning_hi": "पश्चिम बैठक (शुक्र पक्का घर 7वें में): साझेदारी और रचनात्मक सजावट के लिए उत्कृष्ट।",
            "fix_en": "Use light colors, flowers, and artistic décor in West living room. A mirror on West wall amplifies Venus energy.",
            "fix_hi": "पश्चिम बैठक में हल्के रंग, फूल, और कलात्मक सजावट का उपयोग करें। पश्चिम दीवार पर दर्पण शुक्र ऊर्जा बढ़ाता है।",
        },
    },
    "Mercury": {
        7: {
            "warning_en": "West living room: Mercury (Pakka Ghar) here — good for business meetings. Keep communication tools (phone, books) in West/South-East.",
            "warning_hi": "पश्चिम बैठक: बुध (पक्का घर) यहां — व्यापारिक बैठकों के लिए अच्छा। संचार उपकरण (फोन, किताबें) पश्चिम/दक्षिण-पूर्व में रखें।",
            "fix_en": "Place green plants in South-East (Mercury's fire zone). Keep study materials in East or North-East.",
            "fix_hi": "दक्षिण-पूर्व में हरे पौधे रखें। अध्ययन सामग्री पूर्व या उत्तर-पूर्व में रखें।",
        },
    },
}

# ─── General Vastu Tips per House ────────────────────────────────────────────

_HOUSE_VASTU_TIPS: Dict[int, Dict[str, str]] = {
    1:  {"en": "East: Main entrance must be bright, open, unobstructed. Use wood, avoid metal doors.", "hi": "पूर्व: मुख्य द्वार उज्ज्वल, खुला और अबाधित होना चाहिए। लकड़ी का प्रयोग करें।"},
    2:  {"en": "South-East: Kitchen fire element. Stove should face East. Avoid water storage here.", "hi": "दक्षिण-पूर्व: रसोई अग्नि तत्व। चूल्हा पूर्व मुख। यहां पानी भंडार न करें।"},
    3:  {"en": "South: Study/communication room. Use white or light yellow walls. Good for library.", "hi": "दक्षिण: अध्ययन/संचार कक्ष। सफेद या हल्के पीले रंग की दीवारें।"},
    4:  {"en": "South-West: Master bedroom — the heaviest, most stable corner. Avoid clutter here.", "hi": "दक्षिण-पश्चिम: मुख्य शयन कक्ष — सबसे भारी, स्थिर कोना। यहां अव्यवस्था न हो।"},
    5:  {"en": "West: Children's room or creative corner. Use orange/yellow. Natural light essential.", "hi": "पश्चिम: बच्चों का कमरा या रचनात्मक कोना। नारंगी/पीला रंग। प्राकृतिक प्रकाश जरूरी।"},
    6:  {"en": "North-West: Guest room or service area. Keep it airy. Avoid storing valuables here.", "hi": "उत्तर-पश्चिम: अतिथि कक्ष या सेवा क्षेत्र। हवादार रखें।"},
    7:  {"en": "West axis: Living room — the partnership space. Keep welcoming, uncluttered.", "hi": "पश्चिम अक्ष: बैठक कक्ष — साझेदारी स्थान। स्वागत-योग्य और व्यवस्थित रखें।"},
    8:  {"en": "Deep S-W: Storage or utility. Ensure no blocked drains, no rot, no dark locked spaces.", "hi": "गहरा दक्षिण-पश्चिम: भंडार या उपयोगिता। बंद नाले, सड़न, अंधे कमरे न हों।"},
    9:  {"en": "North: Prayer room / altar. This is the most auspicious direction. Keep it clean and lit.", "hi": "उत्तर: पूजा कक्ष / वेदी। यह सबसे शुभ दिशा है। स्वच्छ और रोशन रखें।"},
    10: {"en": "North (career axis): Office/study. Sit facing North or East. Keep it organized.", "hi": "उत्तर (करियर अक्ष): कार्यालय/अध्ययन। उत्तर या पूर्व मुख बैठें। व्यवस्थित रखें।"},
    11: {"en": "North-East: Gains corner. Must be the cleanest, lightest corner. Open to sunlight.", "hi": "उत्तर-पूर्व: लाभ कोना। सबसे साफ, हल्का कोना। सूर्य की रोशनी आने दें।"},
    12: {"en": "N-E far: Hidden/spiritual corner. Avoid storing heavy objects. Good for meditation.", "hi": "उत्तर-पूर्व दूर: छिपा/आध्यात्मिक कोना। भारी वस्तुएं न रखें। ध्यान के लिए अच्छा।"},
}

# ─── Main Engine ──────────────────────────────────────────────────────────────

def get_vastu_diagnosis(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate Vastu home layout diagnosis from Lal Kitab planet positions.

    Returns:
    - directional_map: house→direction→zone→planets
    - planet_warnings: specific warnings per malefic placement
    - priority_fixes: top 3 most urgent fixes
    - general_layout: direction tips for all 12 houses
    """
    p_map: Dict[str, int] = {}
    for p in planet_positions:
        name = p.get("planet")
        house = p.get("house")
        if name and isinstance(house, int):
            p_map[name] = house

    house_to_planets: Dict[int, List[str]] = {}
    for planet, house in p_map.items():
        house_to_planets.setdefault(house, []).append(planet)

    # Build directional map (all 12 houses)
    directional_map = []
    for house in range(1, 13):
        direction_info = HOUSE_DIRECTION[house]
        zone_key = direction_info["zone"]
        zone_info = ZONE_LABEL[zone_key]
        planets_here = house_to_planets.get(house, [])
        directional_map.append({
            "house": house,
            "direction": {"en": direction_info["en"], "hi": direction_info["hi"]},
            "zone": {"en": zone_info["en"], "hi": zone_info["hi"]},
            "planets": planets_here,
            "is_empty": len(planets_here) == 0,
        })

    # Planet-specific warnings
    planet_warnings = []
    for planet, rules in _VASTU_PLANET_RULES.items():
        house = p_map.get(planet)
        if house is None:
            continue
        if house in rules:
            rule = rules[house]
            direction = HOUSE_DIRECTION[house]
            zone_key = direction["zone"]
            planet_warnings.append({
                "planet": planet,
                "house": house,
                "direction": {"en": direction["en"], "hi": direction["hi"]},
                "zone": {"en": ZONE_LABEL[zone_key]["en"], "hi": ZONE_LABEL[zone_key]["hi"]},
                "warning": {"en": rule["warning_en"], "hi": rule["warning_hi"]},
                "fix": {"en": rule["fix_en"], "hi": rule["fix_hi"]},
                "is_critical": "CRITICAL" in rule.get("warning_en", "") or planet in {"Rahu", "Saturn"},
            })

    # Sort by criticality
    planet_warnings.sort(key=lambda x: (0 if x["is_critical"] else 1))

    # Priority fixes (top 3 most critical)
    priority_fixes = planet_warnings[:3]

    # General layout advice
    general_layout = []
    for house in range(1, 13):
        tip = _HOUSE_VASTU_TIPS.get(house)
        if tip:
            direction = HOUSE_DIRECTION[house]
            general_layout.append({
                "house": house,
                "direction": {"en": direction["en"], "hi": direction["hi"]},
                "tip": tip,
            })

    return {
        "directional_map": directional_map,
        "planet_warnings": planet_warnings,
        "priority_fixes": priority_fixes,
        "general_layout": general_layout,
        "total_warnings": len(planet_warnings),
        "critical_count": sum(1 for w in planet_warnings if w["is_critical"]),
    }


def get_vastu_house_for_direction(direction: str) -> Optional[int]:
    """Reverse lookup: direction string → house number."""
    direction_lower = direction.lower()
    for house, info in HOUSE_DIRECTION.items():
        if direction_lower in info["en"].lower():
            return house
    return None
