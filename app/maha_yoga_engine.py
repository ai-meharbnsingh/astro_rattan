"""
maha_yoga_engine.py — Nabhasa / Maha Yogas (Phaladeepika Adhyaya 6)
=====================================================================
38 classical yogas grouped by category:
  A. Aashraya Yogas (3) — planetary sign distribution
  B. Dala Yogas (2)     — benefic/malefic in kendras
  C. Akriti Yogas (20)  — house occupancy patterns (shapes)
  D. Sankhya Yogas (7)  — count of occupied houses
"""
from __future__ import annotations
from typing import Any, Dict, List

MOVABLE = {"Aries", "Cancer", "Libra", "Capricorn"}
FIXED   = {"Taurus", "Leo", "Scorpio", "Aquarius"}
DUAL    = {"Gemini", "Virgo", "Sagittarius", "Pisces"}

BENEFICS = {"Jupiter", "Venus", "Moon", "Mercury"}
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

CHART_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

KENDRA = {1, 4, 7, 10}
TRIKONA = {1, 5, 9}
DUSTHANA = {6, 8, 12}

# Phaladeepika sloka references
_SLOKA = {
    "Rajju":        "Phaladeepika Adh. 6 sloka 4",
    "Musala":       "Phaladeepika Adh. 6 sloka 4",
    "Nala":         "Phaladeepika Adh. 6 sloka 4",
    "Mala":         "Phaladeepika Adh. 6 sloka 5",
    "Sarpa":        "Phaladeepika Adh. 6 sloka 5",
    "Gada":         "Phaladeepika Adh. 6 sloka 6",
    "Shakata":      "Phaladeepika Adh. 6 sloka 6",
    "Vihaga":       "Phaladeepika Adh. 6 sloka 7",
    "Shringataka":  "Phaladeepika Adh. 6 sloka 7",
    "Hala":         "Phaladeepika Adh. 6 sloka 8",
    "Vajra":        "Phaladeepika Adh. 6 sloka 8",
    "Yava":         "Phaladeepika Adh. 6 sloka 9",
    "Kamala":       "Phaladeepika Adh. 6 sloka 9",
    "Vapi":         "Phaladeepika Adh. 6 sloka 10",
    "Yupa":         "Phaladeepika Adh. 6 sloka 11",
    "Ishu":         "Phaladeepika Adh. 6 sloka 11",
    "Shakti":       "Phaladeepika Adh. 6 sloka 11",
    "Danda":        "Phaladeepika Adh. 6 sloka 11",
    "Nauka":        "Phaladeepika Adh. 6 sloka 12",
    "Koota":        "Phaladeepika Adh. 6 sloka 12",
    "Chatra":       "Phaladeepika Adh. 6 sloka 12",
    "Chapa":        "Phaladeepika Adh. 6 sloka 12",
    "Ardha_Chandra":"Phaladeepika Adh. 6 sloka 13",
    "Chakra":       "Phaladeepika Adh. 6 sloka 13",
    "Samudra":      "Phaladeepika Adh. 6 sloka 13",
    "Gola":         "Phaladeepika Adh. 6 sloka 14",
    "Yuga":         "Phaladeepika Adh. 6 sloka 14",
    "Shula":        "Phaladeepika Adh. 6 sloka 14",
    "Kedara":       "Phaladeepika Adh. 6 sloka 15",
    "Pasha":        "Phaladeepika Adh. 6 sloka 15",
    "Dama":         "Phaladeepika Adh. 6 sloka 15",
    "Vallaki":      "Phaladeepika Adh. 6 sloka 15",
}


def _houses(planets: dict) -> Dict[str, int]:
    """Return {planet: house_number} for the 7 main planets."""
    return {p: int((planets.get(p) or {}).get("house", 0)) for p in CHART_PLANETS}


def _signs(planets: dict) -> Dict[str, str]:
    return {p: str((planets.get(p) or {}).get("sign", "")) for p in CHART_PLANETS}


def _occupied_houses(h: Dict[str, int]) -> set:
    return {v for v in h.values() if v > 0}


def _yoga(name: str, category: str, effect_en: str, effect_hi: str, planets_involved: list) -> dict:
    return {
        "name": name,
        "category": category,
        "effect_en": effect_en,
        "effect_hi": effect_hi,
        "planets_involved": planets_involved,
        "sloka_ref": _SLOKA.get(name, "Phaladeepika Adh. 6"),
    }


# --- A. AASHRAYA YOGAS -------------------------------------------------------

def _check_rajju(planets: dict) -> dict | None:
    s = _signs(planets)
    # Require ALL 7 planets to have a populated sign AND all in MOVABLE.
    # If any planet has an empty sign the condition is indeterminate — do not fire.
    if all(s[p] for p in CHART_PLANETS) and all(s[p] in MOVABLE for p in CHART_PLANETS):
        return _yoga("Rajju", "Aashraya",
            "All seven planets in movable signs — the native is a wanderer, restless, fond of travel and change. Earns through movement and enterprise. Leadership in dynamic fields.",
            "सातों ग्रह चर राशियों में — जातक घुमक्कड़, चंचल, यात्रा-प्रिय। गति एवं उद्यम से कमाई। गतिशील क्षेत्रों में नेतृत्व।",
            CHART_PLANETS)
    return None


def _check_musala(planets: dict) -> dict | None:
    s = _signs(planets)
    # Require ALL 7 planets to have a populated sign AND all in FIXED.
    if all(s[p] for p in CHART_PLANETS) and all(s[p] in FIXED for p in CHART_PLANETS):
        return _yoga("Musala", "Aashraya",
            "All seven planets in fixed signs — the native is steadfast, obstinate, fond of stability and authority. Earns through persistence. Accumulates property and wealth.",
            "सातों ग्रह स्थिर राशियों में — जातक दृढ़, हठी, स्थिरता-प्रिय। दृढ़ता से कमाई। संपत्ति एवं धन का संचय।",
            CHART_PLANETS)
    return None


def _check_nala(planets: dict) -> dict | None:
    s = _signs(planets)
    # Require ALL 7 planets to have a populated sign AND all in DUAL.
    if all(s[p] for p in CHART_PLANETS) and all(s[p] in DUAL for p in CHART_PLANETS):
        return _yoga("Nala", "Aashraya",
            "All seven planets in dual signs — the native is versatile, skilled in crafts and arts, manages multiple affairs simultaneously. Success through adaptability and skill.",
            "सातों ग्रह द्विस्वभाव राशियों में — जातक बहुमुखी, शिल्प-कलाओं में निपुण, एक साथ अनेक कार्य। अनुकूलता एवं कौशल से सफलता।",
            CHART_PLANETS)
    return None


# --- B. DALA YOGAS -----------------------------------------------------------

def _check_mala(planets: dict) -> dict | None:
    h = _houses(planets)
    bens = [p for p in ("Jupiter", "Venus", "Moon", "Mercury") if h.get(p) in KENDRA]
    if len(bens) >= 3:
        return _yoga("Mala", "Dala",
            "Three or more benefic planets (Jupiter, Venus, Moon, Mercury) in kendras — the native is wealthy, respected, learned, and enjoys the comforts of life. Long life with prosperity.",
            "तीन या अधिक शुभ ग्रह (बृहस्पति, शुक्र, चंद्र, बुध) केंद्रों में — जातक धनी, सम्मानित, विद्वान, जीवन-सुख भोगने वाला। दीर्घायु एवं समृद्धि।",
            bens)
    return None


def _check_sarpa(planets: dict) -> dict | None:
    h = _houses(planets)
    mals = [p for p in ("Sun", "Mars", "Saturn", "Rahu", "Ketu") if h.get(p) in KENDRA]
    if len(mals) >= 3:
        return _yoga("Sarpa", "Dala",
            "Three or more malefic planets in kendras — the native faces hardship, servitude, and obstacles. Life is difficult but can develop exceptional endurance and rise through adversity.",
            "तीन या अधिक पापी ग्रह केंद्रों में — जातक को कठिनाई, सेवा-भाव एवं बाधाएं। जीवन कठिन परन्तु असाधारण सहनशीलता विकसित; विपरीतता से उठना संभव।",
            mals)
    return None


# --- C. AKRITI YOGAS (shape yogas) ------------------------------------------

def _check_gada(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    pairs = [{1, 2}, {4, 5}, {7, 8}, {10, 11}]
    for pair in pairs:
        if occ and occ.issubset(pair):
            return _yoga("Gada", "Akriti",
                "All planets concentrated in two adjacent houses (mace shape) — native gains wealth through persistent effort in a specific domain. Strong accumulation, focused energy.",
                "सभी ग्रह दो सन्निकट भावों में केंद्रित (गदा आकार) — जातक एक विशिष्ट क्षेत्र में निरंतर प्रयास से धन अर्जित। प्रबल संचय, केंद्रित ऊर्जा।",
                CHART_PLANETS)
    return None


def _check_shakata(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if occ and occ.issubset({1, 7}):
        return _yoga("Shakata", "Akriti",
            "All planets in houses 1 and 7 (cart shape) — native's fortune rises and falls repeatedly like a wheel. Fluctuating wealth and relationships, but eventual stability.",
            "सभी ग्रह भाव 1 और 7 में (शकट आकार) — जातक का भाग्य पहिए की तरह चढ़ता-उतरता है। धन एवं संबंधों में उतार-चढ़ाव, परन्तु अंततः स्थिरता।",
            CHART_PLANETS)
    return None


def _check_vihaga(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if occ and occ.issubset({4, 10}):
        return _yoga("Vihaga", "Akriti",
            "All planets in houses 4 and 10 (bird shape) — native is a skilled messenger, traveler, or networker. Success through communication, mediation, and mobility.",
            "सभी ग्रह भाव 4 और 10 में (विहग/पक्षी आकार) — जातक कुशल दूत, यात्री या नेटवर्कर। संवाद, मध्यस्थता एवं गति से सफलता।",
            CHART_PLANETS)
    return None


def _check_shringataka(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if occ and occ.issubset({1, 5, 9}):
        return _yoga("Shringataka", "Akriti",
            "All planets in the trikona houses 1, 5, 9 (triangle shape) — native is extremely fortunate, virtuous, and dharmic. Blessed by divine grace, respected and prosperous.",
            "सभी ग्रह त्रिकोण भाव 1, 5, 9 में (श्रृंगाटक आकार) — जातक अत्यंत भाग्यशाली, पुण्यात्मा एवं धार्मिक। दिव्य कृपा, सम्मान एवं समृद्धि।",
            CHART_PLANETS)
    return None


def _check_hala(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    trines = [{2, 6, 10}, {3, 7, 11}, {4, 8, 12}]
    for t in trines:
        if occ and occ.issubset(t):
            return _yoga("Hala", "Akriti",
                "All planets in a trine of dusthana or upachaya houses (plow shape) — native earns through service, hard work, and labor. Success in agriculture, engineering, or systematic toil.",
                "सभी ग्रह दुःस्थान या उपचय भावों के त्रिकोण में (हल आकार) — जातक सेवा, कठिन परिश्रम से कमाता है। कृषि, इंजीनियरिंग या व्यवस्थित श्रम में सफलता।",
                CHART_PLANETS)
    return None


def _check_vajra(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    bens_in_1_7 = all(h.get(p) in {1, 7} for p in ("Jupiter", "Venus", "Moon", "Mercury") if h.get(p, 0) > 0)
    mals_in_4_10 = all(h.get(p) in {4, 10} for p in ("Sun", "Mars", "Saturn") if h.get(p, 0) > 0)
    if bens_in_1_7 and mals_in_4_10 and occ.issubset({1, 4, 7, 10}):
        return _yoga("Vajra", "Akriti",
            "Benefics in 1st and 7th, malefics in 4th and 10th (thunderbolt shape) — native is bold and fortunate in youth and old age, but faces adversity in the middle period. Resilient and powerful.",
            "शुभ ग्रह प्रथम और सप्तम में, पापी चतुर्थ और दशम में (वज्र आकार) — जातक युवावस्था एवं वृद्धावस्था में भाग्यशाली, मध्य में कठिनाई। लचीला एवं शक्तिशाली।",
            CHART_PLANETS)
    return None


def _check_yava(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    mals_in_1_7 = all(h.get(p) in {1, 7} for p in ("Sun", "Mars", "Saturn") if h.get(p, 0) > 0)
    bens_in_4_10 = all(h.get(p) in {4, 10} for p in ("Jupiter", "Venus", "Moon", "Mercury") if h.get(p, 0) > 0)
    if mals_in_1_7 and bens_in_4_10 and occ.issubset({1, 4, 7, 10}):
        return _yoga("Yava", "Akriti",
            "Malefics in 1st and 7th, benefics in 4th and 10th (barleycorn shape) — native faces hardship in youth and old age but prospers in the middle period. Learned, charitable, and self-controlled.",
            "पापी प्रथम और सप्तम में, शुभ चतुर्थ और दशम में (यव आकार) — जातक युवावस्था एवं वृद्धावस्था में कठिनाई, मध्य में समृद्धि। विद्वान, दानशील एवं संयमी।",
            CHART_PLANETS)
    return None


def _check_kamala(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if {1, 4, 7, 10}.issubset(occ):
        return _yoga("Kamala", "Akriti",
            "All four kendra houses occupied (lotus shape) — native is endowed with fame, virtue, wealth, and a long life. Rises to eminence like a lotus blooming from mud. Royal honor and recognition.",
            "चारों केंद्र भाव ग्रह-युक्त (कमल आकार) — जातक यश, पुण्य, धन एवं दीर्घायु से संपन्न। कमल की तरह उत्थान। राजकीय सम्मान एवं मान्यता।",
            CHART_PLANETS)
    return None


def _check_vapi(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if {3, 6, 10, 11}.issubset(occ):
        return _yoga("Vapi", "Akriti",
            "Houses 3, 6, 10, 11 all occupied (reservoir shape) — native accumulates wealth steadily through sustained effort. Long life, persistent work, and systematic gains.",
            "भाव 3, 6, 10, 11 सभी ग्रह-युक्त (वापी आकार) — जातक निरंतर प्रयास से धन का संचय करता है। दीर्घायु, दृढ़ कार्य एवं व्यवस्थित लाभ।",
            CHART_PLANETS)
    return None


def _check_yupa(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if occ and occ.issubset({1, 2, 3, 4}):
        return _yoga("Yupa", "Akriti",
            "All planets in houses 1–4 (sacrificial post shape) — native is virtuous, generous, skilled in rituals and ceremonies. Often connected to religious or traditional institutions.",
            "सभी ग्रह भाव 1–4 में (यूप आकार) — जातक पुण्यात्मा, दानशील, अनुष्ठानों में कुशल। धार्मिक या परंपरागत संस्थाओं से जुड़ाव।",
            CHART_PLANETS)
    return None


def _check_ishu(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if occ and occ.issubset({4, 5, 6, 7}):
        return _yoga("Ishu", "Akriti",
            "All planets in houses 4–7 (arrow/dart shape) — native is focused, purposeful, and aims directly at goals. Success through single-minded determination and targeted effort.",
            "सभी ग्रह भाव 4–7 में (इषु/बाण आकार) — जातक केंद्रित, उद्देश्यपूर्ण, लक्ष्य पर सीधा निशाना। एकनिष्ठ संकल्प एवं लक्षित प्रयास से सफलता।",
            CHART_PLANETS)
    return None


def _check_shakti(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if occ and occ.issubset({7, 8, 9, 10}):
        return _yoga("Shakti", "Akriti",
            "All planets in houses 7–10 (spear shape) — native is powerful, assertive, and rises to authority through partnerships and social standing. Strong in the latter half of life.",
            "सभी ग्रह भाव 7–10 में (शक्ति/भाला आकार) — जातक शक्तिशाली, दृढ़, साझेदारी एवं सामाजिक प्रतिष्ठा से अधिकार तक उठता है। जीवन के उत्तरार्ध में बली।",
            CHART_PLANETS)
    return None


def _check_danda(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if occ and occ.issubset({10, 11, 12}):
        return _yoga("Danda", "Akriti",
            "All planets in houses 10–12 (rod/staff shape) — native has authority but may become isolated or rigid. Service-oriented, may occupy high administrative positions but at personal cost.",
            "सभी ग्रह भाव 10–12 में (दंड आकार) — जातक के पास अधिकार परन्तु एकाकीपन या कठोरता संभव। सेवा-परायण, उच्च प्रशासनिक पद, परन्तु व्यक्तिगत मूल्य पर।",
            CHART_PLANETS)
    return None


def _check_nauka(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if occ and occ.issubset({1, 2, 3, 4, 5, 6, 7}):
        count_in_range = sum(1 for v in occ if 1 <= v <= 7)
        if count_in_range >= 6:
            result = _yoga("Nauka", "Akriti",
                "Majority of planets in houses 1–7 (boat shape) — native earns through sea trade, foreign commerce, or travel across waters. Benefits from hospitality, transport, or navigation industries.",
                "अधिकांश ग्रह भाव 1–7 में (नाव आकार) — जातक समुद्री व्यापार, विदेशी वाणिज्य या जल-यात्रा से कमाई। आतिथ्य, परिवहन या नौचालन उद्योग से लाभ।",
                CHART_PLANETS)
            result["count"] = count_in_range
            return result
    return None


def _check_koota(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if occ and occ.issubset({2, 3, 4, 5, 6, 7, 8}):
        count_in_range = sum(1 for v in occ if 2 <= v <= 8)
        if count_in_range >= 6:
            result = _yoga("Koota", "Akriti",
                "Majority of planets in houses 2–8 (fortress/peak shape) — native is skilled in strategy, defense, and management. May rise to positions of protective authority.",
                "अधिकांश ग्रह भाव 2–8 में (कूट/किला आकार) — जातक रणनीति, रक्षा एवं प्रबंधन में कुशल। रक्षात्मक सत्ता के पदों पर उठ सकता है।",
                CHART_PLANETS)
            result["count"] = count_in_range
            return result
    return None


def _check_chatra(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if occ and occ.issubset({4, 5, 6, 7, 8, 9, 10}):
        count_in_range = sum(1 for v in occ if 4 <= v <= 10)
        if count_in_range >= 6:
            result = _yoga("Chatra", "Akriti",
                "Majority of planets in houses 4–10 (umbrella/parasol shape) — native provides shelter and protection to others. Leadership, patronage, and a life of comfort and honor.",
                "अधिकांश ग्रह भाव 4–10 में (छत्र आकार) — जातक दूसरों को आश्रय एवं सुरक्षा देता है। नेतृत्व, संरक्षण एवं आराम एवं सम्मान का जीवन।",
                CHART_PLANETS)
            result["count"] = count_in_range
            return result
    return None


def _check_chapa(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if occ and occ.issubset({7, 8, 9, 10, 11, 12, 1}):
        count_in_range = sum(1 for v in occ if v in {7, 8, 9, 10, 11, 12, 1})
        if count_in_range >= 6:
            result = _yoga("Chapa", "Akriti",
                "Majority of planets in houses 7–1 (bow shape) — native is skilled in commerce, diplomacy, and subtle strategy. Successful in partnerships and indirect influence.",
                "अधिकांश ग्रह भाव 7–1 में (चाप/धनुष आकार) — जातक वाणिज्य, कूटनीति एवं सूक्ष्म रणनीति में कुशल। साझेदारी एवं अप्रत्यक्ष प्रभाव में सफल।",
                CHART_PLANETS)
            result["count"] = count_in_range
            return result
    return None


def _check_ardha_chandra(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    if len(occ) >= 6:
        for start in range(1, 13):
            span = {((start - 1 + i) % 12) + 1 for i in range(7)}
            if occ.issubset(span):
                result = _yoga("Ardha_Chandra", "Akriti",
                    "Planets span exactly seven consecutive houses (half-moon shape) — native is skilled in warfare, weaponry, or competitive arts. Bold, decisive, and often finds fame through dramatic achievement.",
                    "ग्रह सात लगातार भावों में फैले हैं (अर्धचंद्र आकार) — जातक युद्ध, शस्त्र-विद्या या प्रतिस्पर्धी कलाओं में कुशल। साहसी, निर्णायक, नाटकीय उपलब्धि से यश।",
                    CHART_PLANETS)
                result["count"] = len(occ)
                return result
    return None


def _check_chakra(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    alt1 = {1, 3, 5, 7, 9, 11}
    alt2 = {2, 4, 6, 8, 10, 12}
    if occ and (occ.issubset(alt1) and len(occ.intersection(alt1)) >= 5):
        return _yoga("Chakra", "Akriti",
            "Five or more alternate odd houses occupied (wheel shape) — native rises to kingship or equivalent authority. Fame spreads in all directions. A yoga of exceptional eminence.",
            "पांच या अधिक विषम भाव ग्रह-युक्त (चक्र आकार) — जातक राजत्व या समकक्ष सत्ता तक उठता है। यश सभी दिशाओं में फैलता है। असाधारण श्रेष्ठता का योग।",
            CHART_PLANETS)
    if occ and (occ.issubset(alt2) and len(occ.intersection(alt2)) >= 5):
        return _yoga("Chakra", "Akriti",
            "Five or more alternate even houses occupied (wheel shape) — native rises to exceptional authority and wealth. Fame and influence spread widely. A yoga of high achievement.",
            "पांच या अधिक सम भाव ग्रह-युक्त (चक्र आकार) — जातक असाधारण सत्ता एवं धन तक उठता है। यश एवं प्रभाव दूर-दूर तक फैलता है।",
            CHART_PLANETS)
    return None


def _check_samudra(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    even = {2, 4, 6, 8, 10, 12}
    if len(occ.intersection(even)) >= 6:
        return _yoga("Samudra", "Akriti",
            "All six even houses occupied (ocean shape) — native enjoys immense wealth, high status, and a life full of pleasures and comforts. Generous, attractive, and beloved by all.",
            "छहों सम भाव ग्रह-युक्त (समुद्र आकार) — जातक अपार धन, उच्च पद, सुख-भोग से परिपूर्ण जीवन। उदार, आकर्षक एवं सबका प्रिय।",
            CHART_PLANETS)
    return None


# --- D. SANKHYA YOGAS (count of occupied houses) ----------------------------

_SANKHYA = {
    1: ("Gola",    "benefic",
        "All planets in a single house — native is extremely focused, obsessive, and single-minded. May attain mastery in one domain but lacks balance. Fame or infamy through intense specialization.",
        "सभी ग्रह एक ही भाव में — जातक अत्यंत केंद्रित, एकनिष्ठ। एक क्षेत्र में महारत परन्तु संतुलन का अभाव। तीव्र विशेषज्ञता से यश या बदनामी।"),
    2: ("Yuga",    "malefic",
        "Planets distributed across only two houses — native's life revolves around two dominant themes only. Limited flexibility, but intense mastery in those areas.",
        "ग्रह केवल दो भावों में — जातक का जीवन केवल दो प्रमुख विषयों पर केंद्रित। सीमित लचीलापन, परन्तु उन क्षेत्रों में गहन महारत।"),
    3: ("Shula",   "malefic",
        "Planets in three houses only (trident shape) — native has power but faces recurring obstacles and conflicts. Strong in adversity, can rise through competition and challenge.",
        "ग्रह केवल तीन भावों में (शूल आकार) — जातक के पास शक्ति परन्तु बारंबार बाधाएं एवं संघर्ष। विपरीतता में बलशाली, प्रतिस्पर्धा से उठ सकता है।"),
    4: ("Kedara",  "benefic",
        "Planets in four houses — native is a farmer-like accumulator, systematic and patient. Acquires land, property, and sustenance through methodical effort.",
        "ग्रह चार भावों में — जातक किसान की तरह संचयकर्ता, व्यवस्थित एवं धैर्यशाली। क्रमबद्ध प्रयास से भूमि, संपत्ति एवं आजीविका।"),
    5: ("Pasha",   "malefic",
        "Planets in five houses — native is caught in entanglements, obligations, and bonds. Skilled in networking but prone to entrapment and complex interpersonal situations.",
        "ग्रह पांच भावों में — जातक उलझनों, दायित्वों एवं बंधनों में। नेटवर्किंग में कुशल परन्तु जाल एवं जटिल पारस्परिक स्थितियों की प्रवृत्ति।"),
    6: ("Dama",    "benefic",
        "Planets in six houses — native is prosperous, well-rounded, and socially successful. The wide distribution grants adaptability and diverse sources of wealth and happiness.",
        "ग्रह छह भावों में — जातक समृद्ध, सर्वांगीण एवं सामाजिक रूप से सफल। विस्तृत वितरण अनुकूलनशीलता एवं विविध धन-सुख के स्रोत देता है।"),
    7: ("Vallaki", "benefic",
        "Planets in seven or more houses — native is highly accomplished, learned, and long-lived. Versatile, widely respected, and gifted with multiple talents like a well-tuned instrument.",
        "ग्रह सात या अधिक भावों में — जातक अत्यंत कुशल, विद्वान एवं दीर्घायु। बहुमुखी, व्यापक सम्मान एवं सुव्यवस्थित वाद्ययंत्र की तरह अनेक प्रतिभाएं।"),
}


def _check_sankhya(planets: dict) -> dict | None:
    h = _houses(planets)
    occ = _occupied_houses(h)
    count = len(occ)
    key = min(count, 7)
    if key in _SANKHYA:
        name, nature, effect_en, effect_hi = _SANKHYA[key]
        return {
            "name": name,
            "category": "Sankhya",
            "effect_en": effect_en,
            "effect_hi": effect_hi,
            "planets_involved": CHART_PLANETS,
            "sloka_ref": _SLOKA.get(name, "Phaladeepika Adh. 6 sloka 14"),
            "houses_occupied": sorted(occ),
            "count": count,
        }
    return None


# --- MAIN ENTRY --------------------------------------------------------------

def analyze_maha_yogas(planets: dict) -> Dict[str, Any]:
    """
    Detect all applicable Nabhasa/Maha Yogas.

    `planets` is the standard chart planets dict:
      {planet_name: {"house": int, "sign": str, ...}}

    Returns:
      {
        "detected": [list of yoga dicts],
        "count": int,
        "summary_en": str,
        "summary_hi": str,
        "sloka_ref": "Phaladeepika Adh. 6",
      }
    """
    checkers = [
        _check_rajju, _check_musala, _check_nala,
        _check_mala, _check_sarpa,
        _check_gada, _check_shakata, _check_vihaga, _check_shringataka, _check_hala,
        _check_vajra, _check_yava, _check_kamala, _check_vapi,
        _check_yupa, _check_ishu, _check_shakti, _check_danda,
        _check_nauka, _check_koota, _check_chatra, _check_chapa,
        _check_ardha_chandra, _check_chakra, _check_samudra,
    ]
    detected = []
    for fn in checkers:
        result = fn(planets)
        if result:
            detected.append(result)

    # Sankhya yoga is always exactly one (based on count of occupied houses)
    sankhya = _check_sankhya(planets)
    if sankhya:
        detected.append(sankhya)

    count = len(detected)
    if count == 0:
        summary_en = "No classical Nabhasa yoga detected in this chart."
        summary_hi = "इस कुंडली में कोई नभस योग नहीं पाया गया।"
    elif count == 1:
        summary_en = f"1 Nabhasa yoga detected: {detected[0]['name']}."
        summary_hi = f"1 नभस योग पाया गया: {detected[0]['name']}।"
    else:
        names = ", ".join(d["name"] for d in detected)
        summary_en = f"{count} Nabhasa yogas detected: {names}."
        summary_hi = f"{count} नभस योग पाए गए: {names}।"

    return {
        "detected": detected,
        "count": count,
        "summary_en": summary_en,
        "summary_hi": summary_hi,
        "sloka_ref": "Phaladeepika Adh. 6",
    }
