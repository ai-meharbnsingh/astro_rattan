"""
lalkitab_rahu_ketu_axis.py — Rahu-Ketu 1-7 Axis (Shadow Axis) Canonical Rules
==============================================================================
Reference: Lal Kitab 1952, Section 2.17 (Rahu-Ketu combined-by-aspect effects)

In LK 1952, Rahu and Ketu are the shadow axis — always 180 degrees apart, so
they always occupy houses that are 7 apart (H1-H7, H2-H8, ..., H6-H12). LK
treats them as "combined by aspect" whenever they share a 1-7 axis (which they
always do), and prescribes specific combined effects that manifest on BOTH
endpoint houses (i.e. the effect is symmetric — the axis itself is the unit,
not a single house).

This module implements the 6 unique Rahu-Ketu axis configurations and wires
canonical bilingual effect/remedy/caution strings into the advanced endpoint.

Public API:
    detect_rahu_ketu_axis(planet_positions) -> dict | None

The detector normalises the (rahu_house, ketu_house) pair to a sorted
(min_house, max_house) tuple so the axis_key is found regardless of which node
is at the lower-numbered end.
"""

from typing import Any, Dict, List, Optional, Tuple

# ============================================================
# Canonical 6 Rahu-Ketu axis configurations
# Key: sorted (min_house, max_house) tuple
# ============================================================

_AXIS_RULES: Dict[Tuple[int, int], Dict[str, Any]] = {
    (1, 7): {
        "axis_key": "1-7",
        "axis_en": "Self–Partnership Axis",
        "axis_hi": "स्व–साझेदारी अक्ष",
        "effect_en": (
            "Identity crisis manifests through marriage and partnership. The "
            "native struggles with the question 'who am I' inside their closest "
            "relationships — self-image and the partner's reflection collide. "
            "Marriage either forges identity or shatters it."
        ),
        "effect_hi": (
            "पहचान का संकट विवाह और साझेदारी के माध्यम से प्रकट होता है। जातक "
            "अपने निकटतम संबंधों में 'मैं कौन हूँ' के प्रश्न से जूझता है — आत्म-"
            "छवि और साथी का प्रतिबिंब टकराते हैं। विवाह या तो पहचान गढ़ता है "
            "या उसे चकनाचूर कर देता है।"
        ),
        "remedy_en": (
            "Throw a small silver piece into flowing river water (Rahu remedy) "
            "and feed a black-and-white spotted dog regularly (Ketu remedy). "
            "Perform both together — the axis is one unit."
        ),
        "remedy_hi": (
            "बहते नदी के जल में छोटी चाँदी का टुकड़ा प्रवाहित करें (राहु उपाय) "
            "और काले-सफेद चित्तीदार कुत्ते को नियमित भोजन कराएँ (केतु उपाय)। "
            "दोनों एक साथ करें — अक्ष एक ही इकाई है।"
        ),
        "caution_en": "",
        "caution_hi": "",
        "life_areas": ["identity", "partnership", "marriage"],
    },
    (2, 8): {
        "axis_key": "2-8",
        "axis_en": "Wealth–Transformation Axis",
        "axis_hi": "धन–परिवर्तन अक्ष",
        "effect_en": (
            "Sudden financial upheavals and disputes around inherited assets. "
            "Hidden family wealth surfaces unexpectedly — sometimes as windfall, "
            "sometimes as legal contest. Money flows through transformation, "
            "never through steady accumulation."
        ),
        "effect_hi": (
            "अचानक वित्तीय उथल-पुथल और विरासत में मिली संपत्ति को लेकर विवाद। "
            "छिपी पारिवारिक संपत्ति अप्रत्याशित रूप से सामने आती है — कभी "
            "आकस्मिक लाभ के रूप में, कभी कानूनी विवाद के रूप में। धन परिवर्तन "
            "से बहता है, स्थिर संचय से नहीं।"
        ),
        "remedy_en": (
            "Keep a square piece of silver in the family locker and donate a "
            "portion of any inherited sum to a temple within 43 days of "
            "receiving it."
        ),
        "remedy_hi": (
            "परिवार के लॉकर में चाँदी का वर्गाकार टुकड़ा रखें और प्राप्त "
            "विरासत का कुछ अंश 43 दिनों के भीतर मंदिर में दान करें।"
        ),
        "caution_en": (
            "Do NOT handle or accept belongings of a recently deceased person "
            "for 43 days — LK 1952 warns this activates the 8th-house shadow "
            "and blocks the 2nd-house wealth channel."
        ),
        "caution_hi": (
            "43 दिनों तक किसी हाल ही में मृत व्यक्ति की वस्तुएँ न तो छुएँ न "
            "स्वीकार करें — लाल किताब 1952 चेताती है कि यह आठवें भाव की छाया "
            "को सक्रिय कर दूसरे भाव के धन-मार्ग को अवरुद्ध कर देता है।"
        ),
        "life_areas": ["wealth", "inheritance", "transformation"],
    },
    (3, 9): {
        "axis_key": "3-9",
        "axis_en": "Effort–Fortune Axis",
        "axis_hi": "पुरुषार्थ–भाग्य अक्ष",
        "effect_en": (
            "Courageous efforts are repeatedly blocked by unseen karma from "
            "the father's lineage. Fortune arrives, but through unexpected "
            "paths — never along the route the native planned. Father's "
            "blessings transmit via strangers, not directly."
        ),
        "effect_hi": (
            "साहसिक प्रयास पिता के कुल के अदृश्य कर्म से बार-बार रुकते हैं। "
            "भाग्य आता है, पर अप्रत्याशित मार्गों से — कभी उस रास्ते से नहीं "
            "जिसकी जातक ने योजना बनाई हो। पिता का आशीर्वाद सीधे नहीं, "
            "अजनबियों के माध्यम से पहुँचता है।"
        ),
        "remedy_en": (
            "Donate mustard oil to a temple or to a poor labourer every "
            "Saturday for 43 weeks. Touch the father's feet before any major "
            "undertaking — even if the father is deceased, bow in his direction."
        ),
        "remedy_hi": (
            "प्रत्येक शनिवार को 43 सप्ताह तक मंदिर में या किसी निर्धन श्रमिक "
            "को सरसों का तेल दान करें। कोई भी बड़ा कार्य आरंभ करने से पहले "
            "पिता के चरण स्पर्श करें — यदि पिता जीवित न हों तो भी उनकी दिशा "
            "में प्रणाम करें।"
        ),
        "caution_en": "",
        "caution_hi": "",
        "life_areas": ["effort", "fortune", "father"],
    },
    (4, 10): {
        "axis_key": "4-10",
        "axis_en": "Home–Career Axis",
        "axis_hi": "गृह–कर्म अक्ष",
        "effect_en": (
            "Home stability and career ambition pull in opposite directions — "
            "one rises only as the other weakens. The mother's health is "
            "karmically linked to the native's public standing: her well-being "
            "mirrors the native's professional reputation."
        ),
        "effect_hi": (
            "घरेलू स्थिरता और करियर की महत्वाकांक्षा विपरीत दिशाओं में खींचती "
            "हैं — एक तभी उठता है जब दूसरा कमज़ोर हो। माता का स्वास्थ्य जातक "
            "की सार्वजनिक प्रतिष्ठा से कर्म-सूत्र द्वारा बंधा है: उनका कुशल "
            "जातक के व्यावसायिक सम्मान का दर्पण है।"
        ),
        "remedy_en": (
            "Pour raw cow's milk at the root of a Peepal tree every Monday at "
            "dawn. Keep the kitchen hearth spotless — LK 1952 treats the "
            "kitchen as the 4th-house anchor that stabilises the 10th."
        ),
        "remedy_hi": (
            "प्रत्येक सोमवार भोर में पीपल वृक्ष की जड़ में कच्चा गाय का दूध "
            "अर्पित करें। रसोई का चूल्हा निष्कलंक रखें — लाल किताब 1952 रसोई "
            "को चौथे भाव का आधार मानती है जो दसवें भाव को स्थिर करता है।"
        ),
        "caution_en": "",
        "caution_hi": "",
        "life_areas": ["home", "career", "mother"],
    },
    (5, 11): {
        "axis_key": "5-11",
        "axis_en": "Children–Network Axis",
        "axis_hi": "संतान–संपर्क अक्ष",
        "effect_en": (
            "Children arrive through unconventional paths — adoption, delay, "
            "or through a partner's prior relationship. The social network "
            "brings either sudden gains or sudden losses; no middle ground. "
            "Friends are instruments of the native's children's destiny."
        ),
        "effect_hi": (
            "संतान अपरंपरागत मार्गों से आती है — गोद लेना, विलंब, या साथी के "
            "पूर्व संबंध के माध्यम से। सामाजिक संपर्क या तो अचानक लाभ लाता है "
            "या अचानक हानि; बीच का कोई रास्ता नहीं। मित्र जातक की संतान के "
            "भाग्य के साधन होते हैं।"
        ),
        "remedy_en": (
            "Feed crows at dawn for 43 consecutive days with moist rice or "
            "unsweetened roti. Never refuse food to an unknown child — "
            "LK 1952 reads this as a direct 5th-house fortification."
        ),
        "remedy_hi": (
            "43 लगातार दिनों तक भोर में कौवों को गीले चावल या बिना मिठास की "
            "रोटी खिलाएँ। किसी अज्ञात बालक को भोजन देने से कभी इनकार न करें — "
            "लाल किताब 1952 इसे पंचम भाव का सीधा सुदृढ़ीकरण मानती है।"
        ),
        "caution_en": "",
        "caution_hi": "",
        "life_areas": ["children", "network", "gains"],
    },
    (6, 12): {
        "axis_key": "6-12",
        "axis_en": "Struggle–Liberation Axis",
        "axis_hi": "संघर्ष–मोक्ष अक्ष",
        "effect_en": (
            "Hidden enemies operate from blind spots, foreign-land events "
            "repeatedly reshape life direction, and spiritual awakening "
            "arrives through loss rather than joy. The native's liberation "
            "passes through enemy territory — there is no bypass."
        ),
        "effect_hi": (
            "छुपे शत्रु अदृश्य बिंदुओं से कार्य करते हैं, विदेशी भूमि की "
            "घटनाएँ बार-बार जीवन की दिशा को आकार देती हैं, और आध्यात्मिक "
            "जागरण आनंद के बजाय हानि के माध्यम से आता है। जातक का मोक्ष शत्रु-"
            "क्षेत्र से होकर जाता है — कोई उपमार्ग नहीं है।"
        ),
        "remedy_en": (
            "Donate regularly to a monastery, ashram, or dharamshala. Feed "
            "homeless dogs in the evening (the 12th-house hour). Never refuse "
            "water to a stranger at the door."
        ),
        "remedy_hi": (
            "किसी मठ, आश्रम या धर्मशाला में नियमित दान करें। संध्या समय "
            "(द्वादश भाव की घड़ी) बेसहारा कुत्तों को भोजन दें। द्वार पर आए "
            "अजनबी को जल से कभी वंचित न करें।"
        ),
        "caution_en": "",
        "caution_hi": "",
        "life_areas": ["enemies", "foreign", "liberation"],
    },
}

# Freeze: do NOT mutate at runtime.
_AXIS_RULES_FROZEN = {k: dict(v) for k, v in _AXIS_RULES.items()}


def _find_node_house(planet_positions: List[Dict[str, Any]], node: str) -> Optional[int]:
    """Find the house of Rahu or Ketu in the planet_positions list.

    Matching is case-insensitive on planet name. Returns None if not present.
    """
    target = node.lower()
    for p in planet_positions or []:
        name = str(p.get("planet", "")).lower()
        if name == target:
            try:
                h = int(p.get("house"))
                if 1 <= h <= 12:
                    return h
            except (TypeError, ValueError):
                return None
    return None


def detect_rahu_ketu_axis(
    planet_positions: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Detect the 1-7 Rahu-Ketu axis configuration and emit the canonical
    combined effect for both endpoint houses.

    Reads ``planet_positions`` (list of ``{"planet": str, "house": int}``),
    finds Rahu and Ketu, normalises their houses to a sorted
    ``(min_house, max_house)`` tuple, and looks up the canonical axis rule.

    Returns:
        dict with keys:
            rahu_house, ketu_house, axis_key, axis_en, axis_hi,
            effect_en, effect_hi, remedy_en, remedy_hi,
            caution_en, caution_hi, lk_ref, source, is_symmetric, life_areas
        or ``None`` if either node is missing, houses are invalid, or the
        pair is not a clean 1-7 axis (e.g. corrupt data where they are not
        7 apart — LK canon requires 180 degree separation).
    """
    rahu_h = _find_node_house(planet_positions, "Rahu")
    ketu_h = _find_node_house(planet_positions, "Ketu")

    if rahu_h is None or ketu_h is None:
        return None

    # Normalise to sorted axis tuple so lookup works regardless of which node
    # is at the lower-numbered end.
    low, high = (rahu_h, ketu_h) if rahu_h < ketu_h else (ketu_h, rahu_h)

    # LK canon: the axis must be a 1-7 (180 degree) relationship — i.e.
    # high - low == 6. If data is corrupt and they are not 7 apart, we
    # refuse to fabricate an axis rule.
    if high - low != 6:
        return None

    rule = _AXIS_RULES_FROZEN.get((low, high))
    if rule is None:
        return None

    return {
        "rahu_house": rahu_h,
        "ketu_house": ketu_h,
        "axis_key": rule["axis_key"],
        "axis_en": rule["axis_en"],
        "axis_hi": rule["axis_hi"],
        "effect_en": rule["effect_en"],
        "effect_hi": rule["effect_hi"],
        "remedy_en": rule["remedy_en"],
        "remedy_hi": rule["remedy_hi"],
        "caution_en": rule["caution_en"],
        "caution_hi": rule["caution_hi"],
        "lk_ref": "2.17",
        "source": "LK_CANONICAL",
        "is_symmetric": True,
        "life_areas": list(rule["life_areas"]),
    }
