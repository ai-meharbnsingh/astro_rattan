"""
raja_yoga_engine.py — Additional Raja Yogas (Phaladeepika Adhyaya 7)
=====================================================================
12 classical Raja Yogas from Adhyaya 7 not covered by the base dosha_engine.

Integrated into analyze_yogas_and_doshas() via the public entry point:
    detect_adh7_raja_yogas(planets, asc_sign) -> List[dict]
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

ZODIAC = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
SIGN_LORD: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}
EXALTATION: Dict[str, str] = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn", "Mercury": "Virgo",
    "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra",
}
OWN_SIGNS: Dict[str, set] = {
    "Sun": {"Leo"}, "Moon": {"Cancer"}, "Mars": {"Aries", "Scorpio"},
    "Mercury": {"Gemini", "Virgo"}, "Jupiter": {"Sagittarius", "Pisces"},
    "Venus": {"Taurus", "Libra"}, "Saturn": {"Capricorn", "Aquarius"},
}
KENDRA = {1, 4, 7, 10}
TRIKONA = {1, 5, 9}
BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

_SLOKA_BASE = "Phaladeepika Adh. 7"


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def _h(p: str, planets: dict) -> int:
    return int((planets.get(p) or {}).get("house", 0))

def _sign(p: str, planets: dict) -> str:
    return str((planets.get(p) or {}).get("sign", ""))

def _house_lord(house: int, asc_sign: str) -> str:
    if asc_sign not in ZODIAC:
        return ""
    idx = (ZODIAC.index(asc_sign) + house - 1) % 12
    return SIGN_LORD.get(ZODIAC[idx], "")

def _is_strong(planet: str, planets: dict) -> bool:
    sign = _sign(planet, planets)
    return sign in OWN_SIGNS.get(planet, set()) or sign == EXALTATION.get(planet, "")

def _in_kendra(planet: str, planets: dict) -> bool:
    return _h(planet, planets) in KENDRA

def _in_trikona(planet: str, planets: dict) -> bool:
    return _h(planet, planets) in TRIKONA

def _in_good_house(planet: str, planets: dict) -> bool:
    return _h(planet, planets) in (KENDRA | TRIKONA)

def _mutual_kendra(p1: str, p2: str, planets: dict) -> bool:
    h1, h2 = _h(p1, planets), _h(p2, planets)
    if h1 == 0 or h2 == 0:
        return False
    return ((h1 - h2) % 12) in {0, 3, 6, 9}

def _aspects_lagna(planet: str, planets: dict) -> bool:
    """Classical aspect to house 1 (lagna): 7th aspect for all + special for Mars/Jupiter/Saturn."""
    ph = _h(planet, planets)
    if ph == 0:
        return False
    dist = (1 - ph) % 12
    if dist == 6:  # 7th aspect
        return True
    if planet == "Mars" and dist in {3, 7}:
        return True
    if planet == "Jupiter" and dist in {4, 8}:
        return True
    if planet == "Saturn" and dist in {2, 9}:
        return True
    return False

def _yoga(name: str, present: bool, desc_en: str, desc_hi: str, planets: list, sloka: str = _SLOKA_BASE) -> dict:
    return {
        "name": name,
        "present": present,
        "description": desc_en,
        "description_hi": desc_hi,
        "planets_involved": planets,
        "sloka_ref": sloka,
        "category": "Raja Yoga (Adh. 7)",
    }


# ══════════════════════════════════════════════════════════════
# 1. CHAMARA YOGA
# Phaladeepika 7 sloka 3
# Jupiter in lagna OR aspecting lagna; AND lagna lord in own/exalt or kendra.
# ══════════════════════════════════════════════════════════════
def check_chamara_yoga(planets: dict, asc_sign: str) -> dict:
    lagna_lord = _house_lord(1, asc_sign)
    jup_in_lagna = _h("Jupiter", planets) == 1
    jup_aspects = _aspects_lagna("Jupiter", planets)
    ll_strong = _is_strong(lagna_lord, planets) or _in_kendra(lagna_lord, planets)

    if (jup_in_lagna or jup_aspects) and ll_strong and lagna_lord:
        desc = (
            f"Jupiter {'in lagna' if jup_in_lagna else 'aspecting lagna'} and "
            f"lagna lord {lagna_lord} is strong (H{_h(lagna_lord, planets)}). "
            "Grants exceptional eloquence, royal honour, and scholarship."
        )
        desc_hi = (
            f"बृहस्पति {'लग्न में' if jup_in_lagna else 'लग्न पर दृष्टि'} और "
            f"लग्नेश {lagna_lord} बलवान (भाव {_h(lagna_lord, planets)})। "
            "असाधारण वाक्पटुता, राजकीय सम्मान एवं विद्वत्ता प्रदान करता है।"
        )
        return _yoga("Chamara Yoga", True, desc, desc_hi, ["Jupiter", lagna_lord])
    return _yoga("Chamara Yoga", False,
                 "Jupiter must be in lagna or aspect it, and lagna lord must be strong.",
                 "बृहस्पति लग्न में या दृष्टि डाले और लग्नेश बलवान होना चाहिए।", [])


# ══════════════════════════════════════════════════════════════
# 2. SHANKHA YOGA
# Phaladeepika 7 sloka 6
# Lords of 5th and 6th in mutual kendra; lagna lord strong in kendra/own sign.
# ══════════════════════════════════════════════════════════════
def check_shankha_yoga(planets: dict, asc_sign: str) -> dict:
    l5 = _house_lord(5, asc_sign)
    l6 = _house_lord(6, asc_sign)
    ll = _house_lord(1, asc_sign)
    if not (l5 and l6 and ll):
        return _yoga("Shankha Yoga", False, "Ascendant data required.", "लग्न डेटा आवश्यक।", [])

    condition = (
        _mutual_kendra(l5, l6, planets)
        and (_in_kendra(ll, planets) or _is_strong(ll, planets))
    )
    if condition:
        desc = (
            f"5th lord {l5} and 6th lord {l6} in mutual kendra; "
            f"lagna lord {ll} is strong (H{_h(ll, planets)}). "
            "Grants authority, fame, longevity, and service to the masses."
        )
        desc_hi = (
            f"पंचमेश {l5} एवं षष्ठेश {l6} परस्पर केन्द्र में; "
            f"लग्नेश {ll} बलवान (भाव {_h(ll, planets)})। "
            "अधिकार, यश, दीर्घायु एवं जन-सेवा का योग।"
        )
        return _yoga("Shankha Yoga", True, desc, desc_hi, [l5, l6, ll])
    return _yoga("Shankha Yoga", False,
                 "5th and 6th lords not in mutual kendra with strong lagna lord.",
                 "पंचमेश-षष्ठेश परस्पर केन्द्र में नहीं या लग्नेश दुर्बल।", [])


# ══════════════════════════════════════════════════════════════
# 3. BHERI YOGA
# Phaladeepika 7 sloka 7
# Jupiter, Venus, and lagna lord all in kendra from lagna; 9th lord in own/exalt sign.
# ══════════════════════════════════════════════════════════════
def check_bheri_yoga(planets: dict, asc_sign: str) -> dict:
    ll = _house_lord(1, asc_sign)
    l9 = _house_lord(9, asc_sign)
    if not (ll and l9):
        return _yoga("Bheri Yoga", False, "Ascendant data required.", "लग्न डेटा आवश्यक।", [])

    condition = (
        _in_kendra("Jupiter", planets)
        and _in_kendra("Venus", planets)
        and _in_kendra(ll, planets)
        and _is_strong(l9, planets)
    )
    if condition:
        desc = (
            f"Jupiter (H{_h('Jupiter', planets)}), Venus (H{_h('Venus', planets)}), "
            f"and lagna lord {ll} (H{_h(ll, planets)}) all in kendra; "
            f"9th lord {l9} is strong. "
            "Royal trumpets at birth — grants immense wealth, fame, and kinglike authority."
        )
        desc_hi = (
            f"बृहस्पति (भाव {_h('Jupiter', planets)}), शुक्र (भाव {_h('Venus', planets)}), "
            f"और लग्नेश {ll} (भाव {_h(ll, planets)}) सभी केन्द्र में; "
            f"नवमेश {l9} बलवान। "
            "अपार धन, यश एवं राजकीय अधिकार का योग।"
        )
        return _yoga("Bheri Yoga", True, desc, desc_hi, ["Jupiter", "Venus", ll, l9])
    return _yoga("Bheri Yoga", False,
                 "Jupiter, Venus, lagna lord all in kendra and 9th lord strong — not met.",
                 "बृहस्पति, शुक्र, लग्नेश केन्द्र में और नवमेश बलवान — शर्त पूरी नहीं।", [])


# ══════════════════════════════════════════════════════════════
# 4. MRIDANGA YOGA
# Phaladeepika 7 sloka 8
# A planet in exaltation placed in kendra; lagna lord strong (own/exalt or kendra).
# ══════════════════════════════════════════════════════════════
def check_mridanga_yoga(planets: dict, asc_sign: str) -> dict:
    ll = _house_lord(1, asc_sign)
    ll_strong = ll and (_is_strong(ll, planets) or _in_kendra(ll, planets))
    exalted_in_kendra = []
    for p, exalt_sign in EXALTATION.items():
        if _sign(p, planets) == exalt_sign and _in_kendra(p, planets):
            exalted_in_kendra.append(p)

    if exalted_in_kendra and ll_strong:
        names_str = ", ".join(f"{p} (H{_h(p, planets)})" for p in exalted_in_kendra)
        desc = (
            f"{names_str} {'are' if len(exalted_in_kendra) > 1 else 'is'} exalted in kendra; "
            f"lagna lord {ll} is strong. "
            "The beating of royal drums — native attains sovereignty, fame, and command over armies."
        )
        desc_hi = (
            f"{', '.join(exalted_in_kendra)} केन्द्र में उच्च स्थित; लग्नेश {ll} बलवान। "
            "राजकीय नगाड़ों का योग — जातक शासन, यश एवं सेना पर नियंत्रण पाता है।"
        )
        return _yoga("Mridanga Yoga", True, desc, desc_hi, exalted_in_kendra + ([ll] if ll else []))
    return _yoga("Mridanga Yoga", False,
                 "No planet exalted in kendra with strong lagna lord.",
                 "केन्द्र में उच्च ग्रह एवं बलवान लग्नेश — शर्त पूरी नहीं।", [])


# ══════════════════════════════════════════════════════════════
# 5. PARIJATA YOGA
# Phaladeepika 7 sloka 9
# The dispositor of the lagna lord is in kendra, trikona, or own sign.
# ══════════════════════════════════════════════════════════════
def check_parijata_yoga(planets: dict, asc_sign: str) -> dict:
    ll = _house_lord(1, asc_sign)
    if not ll:
        return _yoga("Parijata Yoga", False, "Ascendant data required.", "लग्न डेटा आवश्यक।", [])

    ll_sign = _sign(ll, planets)
    dispositor = SIGN_LORD.get(ll_sign, "")
    if not dispositor:
        return _yoga("Parijata Yoga", False, "Cannot determine dispositor.", "डिस्पोसिटर निर्धारित नहीं हो सका।", [])

    condition = (
        _in_kendra(dispositor, planets)
        or _in_trikona(dispositor, planets)
        or _is_strong(dispositor, planets)
    )
    if condition:
        desc = (
            f"Lagna lord {ll} is in {ll_sign}; its dispositor {dispositor} "
            f"is in house {_h(dispositor, planets)} (kendra/trikona/own sign). "
            "Grants fame, wealth, and royal pleasures like the divine Parijata flower."
        )
        desc_hi = (
            f"लग्नेश {ll} {ll_sign} में; इसका डिस्पोसिटर {dispositor} "
            f"भाव {_h(dispositor, planets)} में (केन्द्र/त्रिकोण/स्वगृह)। "
            "पारिजात पुष्प की भाँति यश, धन एवं राजसुख का योग।"
        )
        return _yoga("Parijata Yoga", True, desc, desc_hi, [ll, dispositor])
    return _yoga("Parijata Yoga", False,
                 "Dispositor of lagna lord not in kendra, trikona, or own sign.",
                 "लग्नेश के डिस्पोसिटर की अनुकूल स्थिति नहीं।", [])


# ══════════════════════════════════════════════════════════════
# 6. KALANIDHI YOGA
# Phaladeepika 7 sloka 10
# Jupiter in 2nd or 5th, conjunct or aspected by Venus and/or Mercury.
# ══════════════════════════════════════════════════════════════
def check_kalanidhi_yoga(planets: dict, asc_sign: str) -> dict:
    jup_h = _h("Jupiter", planets)
    if jup_h not in {2, 5}:
        return _yoga("Kalanidhi Yoga", False,
                     "Jupiter must be in 2nd or 5th house.",
                     "बृहस्पति द्वितीय या पंचम भाव में होना चाहिए।", [])

    venus_h = _h("Venus", planets)
    merc_h = _h("Mercury", planets)

    def _aspects_jupiter(p_name: str, ph: int) -> bool:
        if ph == 0:
            return False
        dist = (jup_h - ph) % 12
        if dist == 6:
            return True
        if p_name == "Jupiter" and dist in {4, 8}:
            return True
        return False

    venus_linked = (venus_h == jup_h) or _aspects_jupiter("Venus", venus_h)
    merc_linked = (merc_h == jup_h) or _aspects_jupiter("Mercury", merc_h)

    if venus_linked or merc_linked:
        assoc = []
        if venus_linked:
            assoc.append("Venus")
        if merc_linked:
            assoc.append("Mercury")
        desc = (
            f"Jupiter in house {jup_h} associated with {', '.join(assoc)}. "
            "Grants mastery of arts, music, poetry, scripture, and all fine branches of learning."
        )
        desc_hi = (
            f"बृहस्पति भाव {jup_h} में {', '.join(assoc)} से युत/दृष्ट। "
            "कला, संगीत, काव्य, शास्त्र एवं विद्या में महारत का योग।"
        )
        return _yoga("Kalanidhi Yoga", True, desc, desc_hi, ["Jupiter"] + assoc)
    return _yoga("Kalanidhi Yoga", False,
                 "Jupiter in 2nd/5th but not associated with Venus or Mercury.",
                 "बृहस्पति 2/5 में पर शुक्र-बुध से संबंध नहीं।", [])


# ══════════════════════════════════════════════════════════════
# 7. DHARMA-KARMAADHIPATI YOGA
# Phaladeepika 7 sloka 12
# Lords of 9th (dharma) and 10th (karma) conjunct, exchange, or in mutual kendra.
# Most powerful Raja Yoga for career and fortune.
# ══════════════════════════════════════════════════════════════
def check_dharma_karmaadhipati_yoga(planets: dict, asc_sign: str) -> dict:
    l9 = _house_lord(9, asc_sign)
    l10 = _house_lord(10, asc_sign)
    if not (l9 and l10):
        return _yoga("Dharma-Karmaadhipati Yoga", False, "Ascendant data required.", "लग्न डेटा आवश्यक।", [])

    if l9 == l10:
        # Same planet rules both — automatic yoga
        if _h(l9, planets) > 0:
            desc = (
                f"{l9} is lord of both 9th and 10th houses (house {_h(l9, planets)}). "
                "Natural Dharma-Karmaadhipati — exceptional career, dharma, and fortune."
            )
            desc_hi = (
                f"{l9} नवम और दशम दोनों का स्वामी (भाव {_h(l9, planets)})। "
                "प्राकृतिक धर्म-कर्माधिपति — उत्कृष्ट कैरियर, धर्म एवं भाग्य।"
            )
            return _yoga("Dharma-Karmaadhipati Yoga", True, desc, desc_hi, [l9])

    conjunct = _h(l9, planets) > 0 and _h(l9, planets) == _h(l10, planets)
    exchange = _sign(l9, planets) in OWN_SIGNS.get(l10, set()) and _sign(l10, planets) in OWN_SIGNS.get(l9, set())
    mutual_k = _mutual_kendra(l9, l10, planets)

    if conjunct or exchange or mutual_k:
        mode = "conjunct" if conjunct else ("exchange signs" if exchange else "in mutual kendra")
        mode_hi = "युत" if conjunct else ("राशि परिवर्तन" if exchange else "परस्पर केन्द्र")
        desc = (
            f"9th lord {l9} and 10th lord {l10} are {mode}. "
            "Grants supreme career success, political power, and fulfilment of dharma."
        )
        desc_hi = (
            f"नवमेश {l9} एवं दशमेश {l10} {mode_hi} में। "
            "उच्च कैरियर-सफलता, राजनीतिक शक्ति एवं धर्म-सिद्धि का महायोग।"
        )
        return _yoga("Dharma-Karmaadhipati Yoga", True, desc, desc_hi, [l9, l10])
    return _yoga("Dharma-Karmaadhipati Yoga", False,
                 "9th and 10th lords not conjunct, exchanging, or in mutual kendra.",
                 "नवमेश-दशमेश युत, परिवर्तन या परस्पर केन्द्र में नहीं।", [])


# ══════════════════════════════════════════════════════════════
# 8. PARVATA YOGA
# Phaladeepika 7 sloka 14
# Benefics in kendra; 6th and 8th empty (or malefic-free).
# ══════════════════════════════════════════════════════════════
def check_parvata_yoga(planets: dict, asc_sign: str) -> dict:
    benefics_in_kendra = [p for p in BENEFICS if _h(p, planets) in KENDRA and _h(p, planets) > 0]
    h6_planets = [p for p in MALEFICS if _h(p, planets) == 6]
    h8_planets = [p for p in MALEFICS if _h(p, planets) == 8]

    if benefics_in_kendra and not h6_planets and not h8_planets:
        names = ", ".join(f"{p} (H{_h(p, planets)})" for p in benefics_in_kendra)
        desc = (
            f"Benefics in kendra: {names}; 6th and 8th free of malefics. "
            "Grants fame, mountain-high elevation in society, and long-lasting prosperity."
        )
        desc_hi = (
            f"केन्द्र में शुभ ग्रह: {', '.join(benefics_in_kendra)}; 6/8 में पाप-ग्रह नहीं। "
            "समाज में पर्वत-सी ऊँचाई, यश एवं दीर्घकालीन समृद्धि।"
        )
        return _yoga("Parvata Yoga", True, desc, desc_hi, benefics_in_kendra)
    return _yoga("Parvata Yoga", False,
                 "Benefics must be in kendra with 6th and 8th free of malefics.",
                 "शुभ ग्रह केन्द्र में और 6/8 पाप-रहित होने चाहिए।", [])


# ══════════════════════════════════════════════════════════════
# 9. KAHALA YOGA
# Phaladeepika 7 sloka 16
# Lords of 4th and 9th in mutual kendra; lagna lord strong.
# ══════════════════════════════════════════════════════════════
def check_kahala_yoga(planets: dict, asc_sign: str) -> dict:
    l4 = _house_lord(4, asc_sign)
    l9 = _house_lord(9, asc_sign)
    ll = _house_lord(1, asc_sign)
    if not (l4 and l9 and ll):
        return _yoga("Kahala Yoga", False, "Ascendant data required.", "लग्न डेटा आवश्यक।", [])

    condition = _mutual_kendra(l4, l9, planets) and (_is_strong(ll, planets) or _in_kendra(ll, planets))
    if condition:
        desc = (
            f"4th lord {l4} (H{_h(l4, planets)}) and 9th lord {l9} (H{_h(l9, planets)}) in mutual kendra; "
            f"lagna lord {ll} is strong. "
            "Grants bold temperament, leadership of armies, and authority over land and people."
        )
        desc_hi = (
            f"चतुर्थेश {l4} (भाव {_h(l4, planets)}) एवं नवमेश {l9} (भाव {_h(l9, planets)}) परस्पर केन्द्र में; "
            f"लग्नेश {ll} बलवान। "
            "साहसी स्वभाव, सैन्य-नेतृत्व एवं भूमि-शासन का योग।"
        )
        return _yoga("Kahala Yoga", True, desc, desc_hi, [l4, l9, ll])
    return _yoga("Kahala Yoga", False,
                 "4th and 9th lords not in mutual kendra, or lagna lord weak.",
                 "चतुर्थेश-नवमेश परस्पर केन्द्र में नहीं या लग्नेश दुर्बल।", [])


# ══════════════════════════════════════════════════════════════
# 10. KOORMA YOGA
# Phaladeepika 7 sloka 18
# Benefics in 1st, 3rd, and 5th; malefics only in 6th, 8th, and 12th.
# ══════════════════════════════════════════════════════════════
def check_koorma_yoga(planets: dict, asc_sign: str) -> dict:
    benefic_houses = {_h(p, planets) for p in BENEFICS if _h(p, planets) > 0}
    malefic_houses = {_h(p, planets) for p in MALEFICS if _h(p, planets) > 0}

    benefics_in_good = benefic_houses & {1, 3, 5}
    malefics_outside_dusthana = malefic_houses - {6, 8, 12}

    if benefics_in_good and not malefics_outside_dusthana:
        desc = (
            f"Benefics in houses {sorted(benefics_in_good)} (1st/3rd/5th); "
            "malefics confined to 6th/8th/12th only. "
            "The tortoise formation — grants patience, longevity, hidden depths, and ultimate success."
        )
        desc_hi = (
            f"शुभ ग्रह भाव {sorted(benefics_in_good)} में; पाप ग्रह केवल 6/8/12 में। "
            "कूर्म-कवच — धैर्य, दीर्घायु, गहन बुद्धि एवं अंतिम विजय का योग।"
        )
        return _yoga("Koorma Yoga", True, desc, desc_hi,
                     [p for p in BENEFICS if _h(p, planets) in {1, 3, 5}])
    return _yoga("Koorma Yoga", False,
                 "Benefics not all in 1st/3rd/5th, or malefics outside 6th/8th/12th.",
                 "शुभ ग्रह 1/3/5 में नहीं या पाप ग्रह अन्य भावों में भी।", [])


# ══════════════════════════════════════════════════════════════
# 11. MATSYA YOGA
# Phaladeepika 7 sloka 19
# Malefics in 1st and 9th; benefics in 4th and 8th; planets of any type in 5th.
# ══════════════════════════════════════════════════════════════
def check_matsya_yoga(planets: dict, asc_sign: str) -> dict:
    malefics_in_1_9 = [p for p in MALEFICS if _h(p, planets) in {1, 9}]
    benefics_in_4_8 = [p for p in BENEFICS if _h(p, planets) in {4, 8}]
    planets_in_5 = [p for p in list(MALEFICS | BENEFICS) if _h(p, planets) == 5]

    if malefics_in_1_9 and benefics_in_4_8 and planets_in_5:
        involved = list(set(malefics_in_1_9 + benefics_in_4_8 + planets_in_5))
        desc = (
            f"Malefics in 1st/9th ({', '.join(malefics_in_1_9)}); "
            f"benefics in 4th/8th ({', '.join(benefics_in_4_8)}); "
            f"planets in 5th ({', '.join(planets_in_5)}). "
            "The fish formation — grants fame, philanthropy, and leadership despite obstacles."
        )
        desc_hi = (
            f"पाप ग्रह 1/9 में ({', '.join(malefics_in_1_9)}); "
            f"शुभ ग्रह 4/8 में ({', '.join(benefics_in_4_8)}); "
            f"पंचम में ग्रह ({', '.join(planets_in_5)})। "
            "मत्स्य-संरचना — बाधाओं के बावजूद यश, परोपकार एवं नेतृत्व का योग।"
        )
        return _yoga("Matsya Yoga", True, desc, desc_hi, involved)
    return _yoga("Matsya Yoga", False,
                 "Matsya formation not present (malefics in 1/9, benefics in 4/8, planets in 5).",
                 "मत्स्य-संरचना नहीं (पाप 1/9, शुभ 4/8, पंचम में ग्रह)।", [])


# ══════════════════════════════════════════════════════════════
# 12. VASUMATI YOGA
# BPHS / Phaladeepika — Benefics in 3rd, 6th, 10th, or 11th from Moon.
# Native becomes independently wealthy.
# ══════════════════════════════════════════════════════════════
def check_vasumati_yoga(planets: dict, asc_sign: str) -> dict:
    moon_h = _h("Moon", planets)
    if moon_h == 0:
        return _yoga("Vasumati Yoga", False, "Moon data missing.", "चन्द्र डेटा अनुपलब्ध।", [])

    target_houses = {((moon_h + offset - 1) % 12) + 1 for offset in (2, 5, 9, 10)}
    benefics_in_target = [p for p in ["Jupiter", "Venus", "Mercury"] if _h(p, planets) in target_houses]

    if benefics_in_target:
        desc = (
            f"Benefics {', '.join(benefics_in_target)} in 3rd/6th/10th/11th from Moon (house {moon_h}). "
            "Grants self-earned independent wealth, comfort, and material abundance."
        )
        desc_hi = (
            f"शुभ ग्रह {', '.join(benefics_in_target)} चन्द्र (भाव {moon_h}) से 3/6/10/11 में। "
            "स्वोपार्जित स्वतन्त्र धन, सुख एवं भौतिक समृद्धि का योग।"
        )
        return _yoga("Vasumati Yoga", True, desc, desc_hi, ["Moon"] + benefics_in_target)
    return _yoga("Vasumati Yoga", False,
                 "No benefics in 3rd/6th/10th/11th from Moon.",
                 "चन्द्र से 3/6/10/11 में कोई शुभ ग्रह नहीं।", [])


# ══════════════════════════════════════════════════════════════
# PUBLIC ENTRY POINT
# ══════════════════════════════════════════════════════════════

def detect_adh7_raja_yogas(planets: dict, asc_sign: str) -> List[dict]:
    """
    Run all 12 Adhyaya 7 Raja Yoga checks.
    Returns list of yoga dicts (present=True or False).
    """
    checkers = [
        check_chamara_yoga,
        check_shankha_yoga,
        check_bheri_yoga,
        check_mridanga_yoga,
        check_parijata_yoga,
        check_kalanidhi_yoga,
        check_dharma_karmaadhipati_yoga,
        check_parvata_yoga,
        check_kahala_yoga,
        check_koorma_yoga,
        check_matsya_yoga,
        check_vasumati_yoga,
    ]
    results = []
    for fn in checkers:
        try:
            results.append(fn(planets, asc_sign))
        except Exception:
            pass
    return results
