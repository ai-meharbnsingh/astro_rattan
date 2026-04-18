"""
app/lalkitab_tithi_timing.py

P2.10 — Tithi-based remedy timing.

Lal Kitab 1952 is explicit about planet/day pairing (Sun-Sunday, Moon-Monday,
etc.) but is SILENT on the specific tithi (lunar day) that optimises each
remedy. The tithi layer is sourced from parallel puranic tradition that the
LK field school has always used alongside the 1952 text. We therefore tag
every output with source = "LK_DERIVED" — this is tradition-aligned
inference, NOT a literal LK 1952 quote.

Canon rules encoded (see module-level docstring for each planet):
  - Shukla Paksha  (waxing)  → growth / wealth / progeny / new beginnings
  - Krishna Paksha (waning)  → removal / release / burial / disposal
  - Amavasya       (new moon)    → Pitru remedies peak
  - Purnima        (full moon)   → Moon/Satya-Narayan peak
  - Chaturdashi Krishna (K-14)   → Rahu/Ketu peak ("Shivratri equivalent")
  - Ashtami (8th of either paksha) → AVOID Moon & Venus remedies (backfire)
  - Tritiya Shukla (S-3)         → Mars remedies strongest

Tithi numbering convention:
  Shukla pratipada = S1 … Purnima = S15 (represented as 15)
  Krishna pratipada = K1 … Amavasya = K15 (represented as 15 in krishna)
  We store tithi numbers 1..15 per paksha plus the two pivots (15-S = Purnima,
  15-K = Amavasya). Forbidden lists include only the number (paksha implied
  by context or explicit in "forbidden_tithis_detail").
"""
from __future__ import annotations

from typing import Any, Dict, List


# ─────────────────────────────────────────────────────────────
# Planet → tithi preference table.
# paksha: "shukla" | "krishna" | "either"
# preferred_tithis: numbers 1..15 that are optimum in the preferred paksha
# forbidden_tithis: numbers 1..15 that backfire (any paksha unless noted)
# peak_tithi: the SINGLE strongest tithi (paksha+number), with EN/HI names
# ─────────────────────────────────────────────────────────────
PLANET_TITHI_RULES: Dict[str, Dict[str, Any]] = {
    "Sun": {
        "preferred_paksha": "shukla",
        "preferred_tithis": [1, 7, 12],  # Pratipada, Saptami (Sun's tithi), Dwadashi
        "forbidden_tithis": [8],          # Ashtami dilutes solar fire
        "peak_tithi": 7,
        "peak_tithi_paksha": "shukla",
        "peak_tithi_en": "Shukla Saptami (7th of bright half)",
        "peak_tithi_hi": "शुक्ल सप्तमी (उज्ज्वल पक्ष की सातवीं)",
        "reason_en": (
            "Saptami is the Sun's own tithi (Ratha-Saptami tradition). "
            "Shukla paksha strengthens vitality and father-karma remedies."
        ),
        "reason_hi": (
            "सप्तमी सूर्य की अपनी तिथि है (रथ-सप्तमी परंपरा)। "
            "शुक्ल पक्ष जीवनी-शक्ति और पितृ-कर्म उपायों को बल देता है।"
        ),
    },
    "Moon": {
        "preferred_paksha": "shukla",
        "preferred_tithis": [2, 5, 15],  # Dwitiya (Moon's birth), Panchami, Purnima
        "forbidden_tithis": [8],          # Ashtami — explicit LK canon: Moon backfires
        "peak_tithi": 15,
        "peak_tithi_paksha": "shukla",
        "peak_tithi_en": "Purnima (Full Moon)",
        "peak_tithi_hi": "पूर्णिमा (पूर्ण चंद्र)",
        "reason_en": (
            "Moon remedies peak at Purnima — full luminance amplifies all "
            "Chandra upayas (Satya-Narayan katha tradition). Avoid Ashtami: "
            "Moon's light is halved and the remedy inverts."
        ),
        "reason_hi": (
            "चंद्र उपाय पूर्णिमा पर चरम पर होते हैं — पूर्ण प्रकाश सभी "
            "चंद्र-उपायों को बढ़ाता है (सत्य-नारायण कथा परंपरा)। अष्टमी "
            "वर्जित — चंद्र प्रकाश आधा होता है, उपाय उल्टा पड़ता है।"
        ),
    },
    "Mars": {
        "preferred_paksha": "shukla",
        "preferred_tithis": [3, 6, 11],  # Tritiya (Mangal's strongest), Shashthi, Ekadashi
        "forbidden_tithis": [4, 14],      # Chaturthi (Ganesh-dominant), K-14 (Rahu)
        "peak_tithi": 3,
        "peak_tithi_paksha": "shukla",
        "peak_tithi_en": "Shukla Tritiya (3rd of bright half)",
        "peak_tithi_hi": "शुक्ल तृतीया (उज्ज्वल पक्ष की तीसरी)",
        "reason_en": (
            "Shukla Tritiya is Mars's peak tithi (Akshaya-Tritiya tradition). "
            "Waxing phase channels courage and energy without the aggression "
            "inversion seen in Krishna paksha Mars remedies."
        ),
        "reason_hi": (
            "शुक्ल तृतीया मंगल की चरम तिथि है (अक्षय-तृतीया परंपरा)। "
            "बढ़ता पक्ष साहस और ऊर्जा देता है — कृष्ण पक्ष में मंगल उपाय "
            "क्रोध-उल्टा प्रभाव दे सकते हैं।"
        ),
    },
    "Mercury": {
        "preferred_paksha": "shukla",
        "preferred_tithis": [2, 5, 11],  # Dwitiya, Panchami (Naag), Ekadashi
        "forbidden_tithis": [4],          # Chaturthi
        "peak_tithi": 5,
        "peak_tithi_paksha": "shukla",
        "peak_tithi_en": "Shukla Panchami (5th of bright half)",
        "peak_tithi_hi": "शुक्ल पंचमी (उज्ज्वल पक्ष की पांचवीं)",
        "reason_en": (
            "Panchami is Budh's communication tithi (Naag-Panchami). "
            "Shukla paksha favours learning, commerce, and speech remedies."
        ),
        "reason_hi": (
            "पंचमी बुध की संचार-तिथि है (नाग-पंचमी)। शुक्ल पक्ष विद्या, "
            "व्यापार और वाणी के उपायों को बल देता है।"
        ),
    },
    "Jupiter": {
        "preferred_paksha": "shukla",
        "preferred_tithis": [5, 11, 15],  # Panchami, Ekadashi, Purnima
        "forbidden_tithis": [30, 15],     # Amavasya (Jupiter's light masked) — see paksha note
        # NOTE: for Jupiter we encode Amavasya as forbidden by returning
        # forbidden_tithis_detail with paksha = krishna for 15.
        "peak_tithi": 11,
        "peak_tithi_paksha": "shukla",
        "peak_tithi_en": "Shukla Ekadashi (11th of bright half)",
        "peak_tithi_hi": "शुक्ल एकादशी (उज्ज्वल पक्ष की ग्यारहवीं)",
        "reason_en": (
            "Ekadashi is Vishnu/Guru's fast tithi — wisdom, wealth, and "
            "progeny remedies peak here. Avoid Amavasya: Jupiter's light is "
            "fully masked and the remedy produces no effect (LK 4.09-adjacent)."
        ),
        "reason_hi": (
            "एकादशी विष्णु/गुरु का व्रत है — विद्या, धन, संतान के उपाय यहाँ "
            "चरम पर। अमावस्या पर नहीं — गुरु की रोशनी पूरी ढकी रहती है, "
            "उपाय निष्फल (लाल किताब 4.09 के अनुरूप)।"
        ),
    },
    "Venus": {
        "preferred_paksha": "shukla",
        "preferred_tithis": [1, 6, 13],  # Pratipada, Shashthi, Trayodashi
        "forbidden_tithis": [8],          # Ashtami — Venus backfires (explicit LK canon)
        "peak_tithi": 13,
        "peak_tithi_paksha": "shukla",
        "peak_tithi_en": "Shukla Trayodashi (13th of bright half)",
        "peak_tithi_hi": "शुक्ल त्रयोदशी (उज्ज्वल पक्ष की तेरहवीं)",
        "reason_en": (
            "Trayodashi (Pradosh) is the tithi of beauty and conjugal harmony. "
            "Shukla paksha amplifies marriage, wealth, and luxury remedies. "
            "Avoid Ashtami: Venus silently backfires."
        ),
        "reason_hi": (
            "त्रयोदशी (प्रदोष) सौंदर्य और दांपत्य की तिथि है। शुक्ल पक्ष "
            "विवाह, धन, विलास उपायों को बढ़ाता है। अष्टमी वर्जित — शुक्र "
            "चुपचाप उल्टा पड़ता है।"
        ),
    },
    "Saturn": {
        "preferred_paksha": "krishna",
        "preferred_tithis": [8, 14, 15],  # Ashtami, Chaturdashi, Amavasya (all krishna)
        "forbidden_tithis": [],           # Saturn is the night-planet — few tithi conflicts
        "peak_tithi": 14,
        "peak_tithi_paksha": "krishna",
        "peak_tithi_en": "Krishna Chaturdashi (14th of dark half)",
        "peak_tithi_hi": "कृष्ण चतुर्दशी (अंधेरे पक्ष की चौदहवीं)",
        "reason_en": (
            "Krishna Chaturdashi is the 'Shivratri-equivalent' — Saturn and "
            "Shiva remedies reach peak potency. Krishna paksha aligns with "
            "Saturn's release/dissolution karma: burying iron, donating oil, "
            "dissolving debts."
        ),
        "reason_hi": (
            "कृष्ण चतुर्दशी 'शिवरात्रि-तुल्य' है — शनि और शिव उपाय चरम "
            "शक्ति पर। कृष्ण पक्ष शनि के निर्मोचन-कर्म से मेल खाता है: "
            "लोहा दबाना, तेल दान, ऋण-मुक्ति।"
        ),
    },
    "Rahu": {
        "preferred_paksha": "krishna",
        "preferred_tithis": [14, 15],  # Krishna Chaturdashi, Amavasya
        "forbidden_tithis": [],
        "peak_tithi": 14,
        "peak_tithi_paksha": "krishna",
        "peak_tithi_en": "Krishna Chaturdashi (14th of dark half)",
        "peak_tithi_hi": "कृष्ण चतुर्दशी (अंधेरे पक्ष की चौदहवीं)",
        "reason_en": (
            "Krishna Chaturdashi ('Shivratri equivalent') is the most potent "
            "tithi for Rahu dissolution remedies. Amavasya midnight is the "
            "explicit LK 4.09 exception for Rahu upayas — burying, secret "
            "donations, river-drift rituals."
        ),
        "reason_hi": (
            "कृष्ण चतुर्दशी ('शिवरात्रि-तुल्य') राहु-निर्मोचन उपायों के लिए "
            "सर्वाधिक प्रभावी। अमावस्या आधी रात लाल किताब 4.09 का स्पष्ट "
            "राहु अपवाद है — दबाना, गुप्त दान, नदी-प्रवाह।"
        ),
    },
    "Ketu": {
        "preferred_paksha": "krishna",
        "preferred_tithis": [14, 15],  # Krishna Chaturdashi, Amavasya
        "forbidden_tithis": [],
        "peak_tithi": 15,
        "peak_tithi_paksha": "krishna",
        "peak_tithi_en": "Amavasya (New Moon)",
        "peak_tithi_hi": "अमावस्या (नव चंद्र)",
        "reason_en": (
            "Amavasya is Pitru Paksha peak — Ketu remedies that touch "
            "ancestor karma (Pitru Rin) reach full potency here. Krishna "
            "paksha aligns with Ketu's detachment/moksha signal."
        ),
        "reason_hi": (
            "अमावस्या पितृ पक्ष का चरम है — केतु के पितृ-ऋण सम्बंधी उपाय "
            "पूर्ण शक्ति पर। कृष्ण पक्ष केतु के वैराग्य/मोक्ष संकेत से मेल "
            "खाता है।"
        ),
    },
}


# Planets that are forbidden on Ashtami (either paksha). Explicit LK canon.
ASHTAMI_FORBIDDEN_PLANETS = {"Moon", "Venus"}


def get_tithi_remedy_timing(planet: str, remedy_text: str = "") -> Dict[str, Any]:
    """
    Return the tithi-timing bundle for a given planet's remedy.

    Args:
        planet: target planet ("Sun", "Moon", ...).
        remedy_text: (optional) free-text hint — currently unused, reserved
            for future keyword-triggered overrides (e.g. "burial" → always
            krishna paksha irrespective of planet default).

    Returns:
        dict with keys:
            preferred_paksha        : 'shukla' | 'krishna' | 'either'
            preferred_tithis        : list[int]     — 1..15 in preferred paksha
            forbidden_tithis        : list[int]     — 1..15 to AVOID
            forbidden_tithis_detail : list[dict]    — {tithi, paksha, reason_en/hi}
            peak_tithi              : int           — the single optimum number
            peak_tithi_paksha       : str           — 'shukla' | 'krishna'
            peak_tithi_en           : str
            peak_tithi_hi           : str
            reason_en               : str
            reason_hi               : str
            lk_ref                  : "4.16"         — canon anchor
            source                  : "LK_DERIVED"   — tradition-inferred
    """
    rules = PLANET_TITHI_RULES.get(planet)
    if not rules:
        # Unknown planet — return a safe, empty-but-valid shape so callers
        # don't need to null-guard.
        return {
            "preferred_paksha": "either",
            "preferred_tithis": [],
            "forbidden_tithis": [],
            "forbidden_tithis_detail": [],
            "peak_tithi": None,
            "peak_tithi_paksha": None,
            "peak_tithi_en": "",
            "peak_tithi_hi": "",
            "reason_en": "",
            "reason_hi": "",
            "lk_ref": "4.16",
            "source": "LK_DERIVED",
        }

    # Build the forbidden_tithis_detail list with per-tithi EN/HI reasons.
    detail: List[Dict[str, Any]] = []
    for t in rules.get("forbidden_tithis", []):
        if t == 8 and planet in ASHTAMI_FORBIDDEN_PLANETS:
            detail.append({
                "tithi": 8,
                "paksha": "either",
                "reason_en": (
                    f"Ashtami (8th, either paksha) — {planet} remedies "
                    f"backfire silently. LK canon explicitly flags Moon and "
                    f"Venus Ashtami reversals."
                ),
                "reason_hi": (
                    f"अष्टमी (दोनों पक्ष की आठवीं) — {planet} उपाय चुपचाप "
                    f"उल्टे पड़ते हैं। लाल किताब परंपरा चंद्र और शुक्र की "
                    f"अष्टमी-उल्टी स्पष्ट रूप से बताती है।"
                ),
            })
        elif t == 8:
            detail.append({
                "tithi": 8, "paksha": "either",
                "reason_en": f"Ashtami disperses {planet}'s energy — remedy weakens.",
                "reason_hi": f"अष्टमी {planet} की ऊर्जा को बिखेरती है — उपाय कमज़ोर।",
            })
        elif t == 15 and planet == "Jupiter":
            detail.append({
                "tithi": 15,
                "paksha": "krishna",
                "reason_en": (
                    "Amavasya (Krishna 15) — Jupiter's light is fully masked; "
                    "the remedy produces no effect."
                ),
                "reason_hi": (
                    "अमावस्या (कृष्ण 15) — गुरु की रोशनी पूरी ढकी रहती है, "
                    "उपाय निष्फल रहता है।"
                ),
            })
        elif t == 14 and planet == "Mars":
            detail.append({
                "tithi": 14,
                "paksha": "krishna",
                "reason_en": (
                    "Krishna Chaturdashi is Rahu's peak — Mars remedies clash "
                    "with Rahu's dominion and can trigger aggression."
                ),
                "reason_hi": (
                    "कृष्ण चतुर्दशी राहु का चरम — मंगल उपाय राहु-प्रभुत्व से "
                    "टकराते हैं, क्रोध/विवाद बढ़ सकता है।"
                ),
            })
        elif t == 4:
            detail.append({
                "tithi": 4, "paksha": "either",
                "reason_en": (
                    f"Chaturthi is Ganesh-dominant; {planet} remedies are "
                    f"overridden and their specific benefit is lost."
                ),
                "reason_hi": (
                    f"चतुर्थी गणेश-प्रधान तिथि है; {planet} उपाय का विशेष "
                    f"लाभ दब जाता है।"
                ),
            })
        else:
            detail.append({
                "tithi": t, "paksha": "either",
                "reason_en": f"Tithi {t} is unfavourable for {planet} remedies.",
                "reason_hi": f"तिथि {t} {planet} उपायों के लिए अनुकूल नहीं।",
            })

    # Strip Jupiter's sentinel "30" marker (used only internally) — we already
    # encoded Amavasya via the krishna-15 detail entry.
    forbidden_out = [t for t in rules.get("forbidden_tithis", []) if t != 30]

    return {
        "preferred_paksha": rules["preferred_paksha"],
        "preferred_tithis": list(rules.get("preferred_tithis", [])),
        "forbidden_tithis": forbidden_out,
        "forbidden_tithis_detail": detail,
        "peak_tithi": rules.get("peak_tithi"),
        "peak_tithi_paksha": rules.get("peak_tithi_paksha"),
        "peak_tithi_en": rules.get("peak_tithi_en", ""),
        "peak_tithi_hi": rules.get("peak_tithi_hi", ""),
        "reason_en": rules.get("reason_en", ""),
        "reason_hi": rules.get("reason_hi", ""),
        "lk_ref": "4.16",
        "source": "LK_DERIVED",
    }
