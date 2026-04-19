"""
Lal Kitab Rules Engine (backend)

Purpose:
- Provide rule-driven structures used by the UI without relying on
  frontend hardcoded/mock datasets.

Currently served:
- Mirror house axis occupancy (1↔7, 2↔8, ...) with LK canonical interpretations.
- Cross-house rule triggers with bilingual planet-level interpretation text.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


MIRROR_HOUSES: Tuple[Tuple[int, int], ...] = (
    (1, 7),
    (2, 8),
    (3, 9),
    (4, 10),
    (5, 11),
    (6, 12),
)

# Cross-house rules: planet in from_house directly influences to_house affairs.
CROSS_RULES: Tuple[Tuple[int, int], ...] = (
    (1, 7),
    (4, 10),
    (5, 9),
    (2, 8),
    (3, 9),
    (6, 12),
    (7, 1),
    (10, 4),
)

# LK 1952 mirror-axis canonical texts
_MIRROR_TEXTS: Dict[Tuple[int, int], Dict[str, str]] = {
    (1, 7): {
        "en": "Self vs. Partner axis. What you project (H1) directly mirrors what your partnerships receive (H7). Balance of ego and relationship is the life theme.",
        "hi": "स्वयं बनाम साझेदार धुरी। जो आप प्रकट करते हैं (भाव 1) वही आपके संबंधों को प्रभावित करता है (भाव 7)।",
    },
    (2, 8): {
        "en": "Family wealth vs. Ancestral legacy axis. Your personal resources (H2) and inherited/in-law wealth (H8) are karmically linked.",
        "hi": "पारिवारिक धन बनाम पैतृक संपदा धुरी। व्यक्तिगत संपत्ति (भाव 2) और विरासती/ससुराल धन (भाव 8) कर्म से जुड़े हैं।",
    },
    (3, 9): {
        "en": "Effort vs. Fate axis. Your courage and sibling bonds (H3) are the engine of your luck and dharma (H9). Destiny is earned through action.",
        "hi": "पुरुषार्थ बनाम भाग्य धुरी। साहस और भाई-बहन (भाव 3) आपके भाग्य और धर्म (भाव 9) को प्रेरित करते हैं।",
    },
    (4, 10): {
        "en": "Home vs. Career axis. The foundation at home (H4) determines the height of public achievement (H10). Mother's blessings shape career destiny.",
        "hi": "घर बनाम करियर धुरी। घर की नींव (भाव 4) सार्वजनिक सफलता (भाव 10) की ऊँचाई तय करती है।",
    },
    (5, 11): {
        "en": "Intelligence vs. Gains axis. Past karma and children (H5) link directly to financial gains and elder siblings (H11). Wisdom yields wealth.",
        "hi": "बुद्धि बनाम लाभ धुरी। पूर्व कर्म और संतान (भाव 5) आर्थिक लाभ और बड़े भाई-बहनों (भाव 11) से जुड़े हैं।",
    },
    (6, 12): {
        "en": "Service vs. Loss axis. Debts, diseases, and enemies (H6) flow into hidden expenditures and liberation (H12). What we owe defines what we lose.",
        "hi": "सेवा बनाम व्यय धुरी। ऋण, रोग और शत्रु (भाव 6) छुपे खर्चों और मोक्ष (भाव 12) में परिवर्तित होते हैं।",
    },
}

_MUTUAL_NOTES: Dict[Tuple[int, int], Dict[str, str]] = {
    (1, 7): {
        "en": "Planets in both H1 and H7 create a tug-of-war between self and partner. Either the native sacrifices for relationships or the partner dominates. LK recommends resolving ego before expecting marital harmony.",
        "hi": "भाव 1 और 7 दोनों में ग्रह होने से स्वयं और साझेदार के बीच खिंचाव रहता है। लाल किताब के अनुसार वैवाहिक सुख के लिए अहंकार का त्याग आवश्यक है।",
    },
    (2, 8): {
        "en": "Both H2 and H8 occupied signals wealth coming from two directions — earned and inherited — but also risk of sudden losses. Family karma and in-law tensions require resolution.",
        "hi": "भाव 2 और 8 दोनों में ग्रह — अर्जित और विरासती दोनों ओर से धन आता है, पर अचानक हानि का भी जोखिम है। पारिवारिक कर्म का समाधान जरूरी है।",
    },
    (3, 9): {
        "en": "Planets in both H3 and H9 amplify the effort-luck link. Tremendous energy available — if courage matches dharma, fate rewards handsomely. Sibling relationships shape spiritual progress.",
        "hi": "भाव 3 और 9 दोनों में ग्रह — पुरुषार्थ और भाग्य का सीधा संबंध। साहस और धर्म का समन्वय होने पर भाग्य प्रबल होता है।",
    },
    (4, 10): {
        "en": "Planets in both H4 and H10 indicate a life pulled between domestic duties and career ambitions. Mother's karma and public success are intertwined. One must balance both to avoid exhaustion.",
        "hi": "भाव 4 और 10 दोनों में ग्रह — गृहस्थी और करियर के बीच खिंचाव। माता का कर्म और सार्वजनिक सफलता आपस में जुड़े हैं।",
    },
    (5, 11): {
        "en": "Both H5 and H11 occupied creates powerful wealth-building potential through intelligence and networking. Children and gains become parallel blessings, but speculative tendencies must be controlled.",
        "hi": "भाव 5 और 11 दोनों में ग्रह — बुद्धि और संपर्क के माध्यम से धन-निर्माण की प्रबल संभावना। सट्टे की प्रवृत्ति पर नियंत्रण आवश्यक है।",
    },
    (6, 12): {
        "en": "Both H6 and H12 occupied intensifies the debt-loss cycle. Enemies and expenditures feed each other. LK 1952 advises clearing karmic debts (rin) first before seeking foreign settlement or spiritual retreat.",
        "hi": "भाव 6 और 12 दोनों में ग्रह — ऋण और हानि का चक्र तीव्र होता है। लाल किताब के अनुसार पहले ऋण-मुक्ति और फिर विदेश/मोक्ष की तलाश करें।",
    },
}

# Cross-rule house-level interpretation texts
_CROSS_TEXTS: Dict[Tuple[int, int], Dict[str, str]] = {
    (1, 7): {
        "en": "Planets in H1 directly shape marriage and open partnerships. The native's personality and appearance become the primary factor in relationship outcomes.",
        "hi": "भाव 1 के ग्रह सीधे विवाह और साझेदारी को प्रभावित करते हैं। व्यक्तित्व और स्वरूप ही संबंधों का निर्धारक बनता है।",
    },
    (4, 10): {
        "en": "Planets in H4 shape career trajectory and public reputation. A strong home foundation elevates career; domestic turmoil suppresses professional rise.",
        "hi": "भाव 4 के ग्रह करियर और सामाजिक प्रतिष्ठा को आकार देते हैं। मजबूत घर की नींव करियर को ऊँचाई देती है।",
    },
    (5, 9): {
        "en": "Planets in H5 determine fortune, dharma, and spiritual merit. Intelligence and children become the bridge to higher luck.",
        "hi": "भाव 5 के ग्रह भाग्य, धर्म और आध्यात्मिक पुण्य तय करते हैं। बुद्धि और संतान भाग्य का सेतु बनते हैं।",
    },
    (2, 8): {
        "en": "Planets in H2 affect longevity and in-law relationships. Family speech and wealth directly impact inheritance and occult matters.",
        "hi": "भाव 2 के ग्रह आयु और ससुराल संबंधों को प्रभावित करते हैं। पारिवारिक वाणी और धन विरासत को सीधे प्रभावित करते हैं।",
    },
    (3, 9): {
        "en": "Planets in H3 (courage, siblings) determine fate, religious inclinations, and long journeys. Efforts made today become tomorrow's fortune.",
        "hi": "भाव 3 के ग्रह (साहस, भाई-बहन) भाग्य, धर्म और तीर्थयात्राओं को निर्धारित करते हैं। आज का पुरुषार्थ कल का भाग्य है।",
    },
    (6, 12): {
        "en": "Planets in H6 create hidden expenses and losses (H12). Debts and enemies drain resources in ways not immediately visible — resolve them early.",
        "hi": "भाव 6 के ग्रह छुपे खर्च और हानि (भाव 12) उत्पन्न करते हैं। ऋण और शत्रु अदृश्य रूप से संसाधन खींचते हैं — जल्दी समाधान करें।",
    },
    (7, 1): {
        "en": "Planets in H7 influence the native's health, physical appearance, and overall vitality. Partners and alliances leave a direct imprint on self.",
        "hi": "भाव 7 के ग्रह जातक के स्वास्थ्य, स्वरूप और शक्ति को प्रभावित करते हैं। साझेदार और गठबंधन स्वयं पर सीधा असर डालते हैं।",
    },
    (10, 4): {
        "en": "Planets in H10 impact home life and mother's wellbeing. Career ambitions and public duties can either elevate or disturb domestic peace.",
        "hi": "भाव 10 के ग्रह घर और माता के जीवन को प्रभावित करते हैं। करियर की महत्वाकांक्षा घरेलू शांति को बढ़ा या बिगाड़ सकती है।",
    },
}

# Planet-specific cross-effect notes (planet → which house it's in → interpretation)
_PLANET_CROSS_NOTES: Dict[str, Dict[int, Dict[str, str]]] = {
    "Sun": {
        1: {"en": "Sun in H1 magnifies ego in partnerships (H7). Spouse may feel overshadowed. Leadership in relationships is a strength when balanced.", "hi": "भाव 1 में सूर्य — साझेदारी में अहंकार बढ़ता है। संतुलित नेतृत्व से संबंध मजबूत होते हैं।"},
        7: {"en": "Sun in H7 illuminates self (H1). The native's vitality and identity are shaped by partnerships. Strong, authoritative spouse.", "hi": "भाव 7 में सूर्य — जातक का व्यक्तित्व साझेदारी से प्रकाशित होता है। प्रभावशाली जीवनसाथी।"},
        4: {"en": "Sun in H4 gives career boost (H10) through father's or government's support. Property and prestige linked.", "hi": "भाव 4 में सूर्य — पिता या सरकार के समर्थन से करियर को बल मिलता है।"},
        10: {"en": "Sun in H10 may disturb home peace (H4) due to career demands. Government job or leadership role likely.", "hi": "भाव 10 में सूर्य — करियर की माँगों से घरेलू शांति प्रभावित हो सकती है। सरकारी पद की संभावना।"},
    },
    "Moon": {
        1: {"en": "Moon in H1 makes emotions the core of partnerships (H7). Sensitive, nurturing approach to relationships. Spouse may be emotionally dependent.", "hi": "भाव 1 में चंद्र — भावनाएँ साझेदारी की नींव हैं। संवेदनशील और पोषण देने वाला जीवनसाथी।"},
        4: {"en": "Moon in H4 gives strong maternal support for career (H10). Real estate and emotional stability advance public life.", "hi": "भाव 4 में चंद्र — मातृ सहयोग से करियर को बल। अचल संपत्ति और भावनात्मक स्थिरता सार्वजनिक जीवन को आगे बढ़ाती है।"},
    },
    "Mars": {
        1: {"en": "Mars in H1 brings aggression into partnerships (H7). Delayed or turbulent marriage possible. Physical energy and courage attract strong partners.", "hi": "भाव 1 में मंगल — साझेदारी में आक्रामकता। विवाह में देरी या उथल-पुथल संभव। साहस से प्रभावशाली साझेदार मिलते हैं।"},
        3: {"en": "Mars in H3 turns courage and boldness into fate (H9). Action-oriented dharma — fortune favors the brave.", "hi": "भाव 3 में मंगल — साहस और पुरुषार्थ भाग्य बनाते हैं। सक्रिय धर्म — भाग्य वीरों का साथ देता है।"},
    },
    "Mercury": {
        1: {"en": "Mercury in H1 makes communication the pillar of partnerships (H7). Business marriages or intellectually matched spouse. Trade partnerships flourish.", "hi": "भाव 1 में बुध — संवाद साझेदारी की नींव। व्यापारिक विवाह या बौद्धिक जीवनसाथी। व्यापार साझेदारी फलती है।"},
        6: {"en": "Mercury in H6 creates analytical approach to debts (H12). Skillful management of expenses and hidden enemies through intelligence.", "hi": "भाव 6 में बुध — ऋण और व्यय का बुद्धिमान प्रबंधन। छुपे शत्रुओं पर विश्लेषणात्मक नियंत्रण।"},
    },
    "Jupiter": {
        1: {"en": "Jupiter in H1 blesses partnerships (H7) with wisdom and fortune. Spouse is learned, generous, or brings great luck.", "hi": "भाव 1 में गुरु — साझेदारी को ज्ञान और सौभाग्य का आशीर्वाद। जीवनसाथी विद्वान या सौभाग्यशाली।"},
        5: {"en": "Jupiter in H5 powerfully elevates luck and dharma (H9). Children, wisdom, and past karma combine to create outstanding fortune.", "hi": "भाव 5 में गुरु — भाग्य और धर्म को प्रबल शक्ति मिलती है। संतान, ज्ञान और पूर्व कर्म मिलकर उत्तम भाग्य बनाते हैं।"},
    },
    "Venus": {
        1: {"en": "Venus in H1 creates magnetic attraction in partnerships (H7). Beautiful or artistic spouse. Harmony in marriage when Venus is well-placed.", "hi": "भाव 1 में शुक्र — साझेदारी में चुंबकीय आकर्षण। सुंदर या कलाप्रिय जीवनसाथी। शुक्र की स्थिति अच्छी हो तो वैवाहिक सुख।"},
        7: {"en": "Venus in H7 directly elevates self-beauty and charm (H1). The native radiates attractiveness. Marriage brings abundance and pleasure.", "hi": "भाव 7 में शुक्र — जातक के सौंदर्य और आकर्षण में वृद्धि। विवाह सुख-समृद्धि लाता है।"},
    },
    "Saturn": {
        1: {"en": "Saturn in H1 causes delays and seriousness in partnerships (H7). Marriage may be delayed or to an older/mature person. Discipline in relationships yields long-term rewards.", "hi": "भाव 1 में शनि — साझेदारी में विलंब और गंभीरता। विवाह देर से या परिपक्व व्यक्ति से। अनुशासन से दीर्घकालिक लाभ।"},
        7: {"en": "Saturn in H7 can delay partnerships but ensures lasting bonds. Older, serious, or Capricorn/Aquarius-influenced spouse. Self (H1) gains discipline through relationships.", "hi": "भाव 7 में शनि — साझेदारी में देरी पर स्थायी बंधन। गंभीर या उम्रदराज जीवनसाथी। संबंधों से जातक में अनुशासन।"},
        10: {"en": "Saturn in H10 brings career through hard work. Home (H4) becomes a refuge from professional pressures. Success comes late but durably.", "hi": "भाव 10 में शनि — कठिन परिश्रम से करियर। घर (भाव 4) पेशेवर दबाव से राहत देता है। सफलता देर से पर टिकाऊ।"},
    },
    "Rahu": {
        1: {"en": "Rahu in H1 creates unconventional or foreign partnerships (H7). Unusual, non-traditional, or inter-community marriage. Obsession with relationships.", "hi": "भाव 1 में राहु — अपरंपरागत या विदेशी साझेदारी। असामान्य या अंतर-समुदाय विवाह। संबंधों में जुनून।"},
        6: {"en": "Rahu in H6 amplifies hidden losses (H12). Enemies may operate in shadow. Foreign settlement possible but accompanied by unseen expenses.", "hi": "भाव 6 में राहु — छुपी हानि बढ़ती है। शत्रु परदे के पीछे काम करते हैं। विदेश बस्ती संभव पर अदृश्य खर्च के साथ।"},
    },
    "Ketu": {
        1: {"en": "Ketu in H1 brings spiritual approach to partnerships (H7). Detachment in marriage possible. Past-life connection with spouse. Native seeks liberation through relationships.", "hi": "भाव 1 में केतु — साझेदारी में आध्यात्मिक दृष्टिकोण। विवाह में वैराग्य संभव। पूर्वजन्म का जीवनसाथी से संबंध।"},
        6: {"en": "Ketu in H6 dissolves debts through spiritual means (H12). Hidden enemies lose power. Moksha-oriented lifestyle reduces losses.", "hi": "भाव 6 में केतु — आध्यात्मिक माध्यम से ऋण का विघटन। छुपे शत्रु कमजोर पड़ते हैं। मोक्षपरक जीवनशैली हानि को कम करती है।"},
    },
}


def build_rules(planet_positions: Dict[str, int]) -> Dict[str, Any]:
    house_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    for p, h in planet_positions.items():
        if not h:
            continue
        hn = int(h)
        if 1 <= hn <= 12:
            house_planets[hn].append(p)

    mirror_axis = []
    for h1, h2 in MIRROR_HOUSES:
        p1 = house_planets.get(h1, [])
        p2 = house_planets.get(h2, [])
        axis_text = _MIRROR_TEXTS.get((h1, h2), {})
        entry = {
            "h1": h1,
            "h2": h2,
            "planets_h1": p1,
            "planets_h2": p2,
            "has_mutual": bool(p1 and p2),
            "axis_text_en": axis_text.get("en", ""),
            "axis_text_hi": axis_text.get("hi", ""),
        }
        if p1 and p2:
            mutual = _MUTUAL_NOTES.get((h1, h2), {})
            entry["mutual_note_en"] = mutual.get("en", "")
            entry["mutual_note_hi"] = mutual.get("hi", "")
        mirror_axis.append(entry)

    cross_effects = []
    for idx, (from_h, to_h) in enumerate(CROSS_RULES, start=1):
        pf = house_planets.get(from_h, [])
        rule_text = _CROSS_TEXTS.get((from_h, to_h), {})
        planet_notes = []
        for planet in pf:
            pnotes = _PLANET_CROSS_NOTES.get(planet, {}).get(from_h)
            if pnotes:
                planet_notes.append({"planet": planet, "note_en": pnotes["en"], "note_hi": pnotes["hi"]})
        cross_effects.append(
            {
                "idx": idx,
                "from_house": from_h,
                "to_house": to_h,
                "trigger_planets": pf,
                "has_trigger": bool(pf),
                "rule_text_en": rule_text.get("en", ""),
                "rule_text_hi": rule_text.get("hi", ""),
                "planet_notes": planet_notes,
            }
        )

    return {"mirror_axis": mirror_axis, "cross_effects": cross_effects}

