"""
lalkitab_chandra_kundali.py — Chandra Kundali as an INDEPENDENT LK framework
=============================================================================
Lal Kitab 1952 treats the Chandra Kundali (Moon chart) as a STANDALONE
predictive framework — not a Vedic shortcut of the Lagna chart.

What this module does
---------------------
1. Re-anchors every planet relative to Moon's natal house so Moon becomes H1
   in the Chandra Kundali.
2. Looks up each re-anchored planet against an LK-specific Chandra reading
   table (`lalkitab_chandra_readings.CHANDRA_READINGS`).
3. Provides a conflict detector that flags planets whose Lagna reading and
   Chandra reading diverge meaningfully (one favourable, one not).

The Chandra Kundali's readings are DELIBERATELY different from the Lagna
table — this is the LK 1952 canonical position: the Moon-chart speaks to
emotion / memory / mother / public / mental states, the Lagna-chart speaks
to body / dharma / karma / identity. They are read side-by-side, and
conflicts are flagged to the native rather than silently overridden.

Shift formula
-------------
    chandra_house = ((natal_house - moon_house) % 12) + 1

With moon_house = N the Moon ends up at chandra_house = 1 (by definition).

Public API
----------
    compute_chandra_kundali(planet_positions, moon_house, *, lagna_interpretations=None)
    detect_chandra_lagna_conflicts(chandra_readings, lagna_interpretations)
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.lalkitab_chandra_readings import get_chandra_reading
from app.lalkitab_translations import PLANET_NAMES_HI


_VALID_PLANETS = {
    "Sun", "Moon", "Mars", "Mercury",
    "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
}

# Lagna-nature classification → is_favourable boolean.
# The Lagna table in `lalkitab_interpretations.py` tags each placement as one
# of: "raja", "raja_or_fakir", "mixed", "manda".
#
#   raja           → clearly favourable in Lagna context
#   raja_or_fakir  → conditional — default to favourable (best-case LK canon)
#   mixed          → neither clearly favourable nor clearly negative → excluded
#                    from conflict detection (we only flag CLEAR disagreements)
#   manda          → clearly unfavourable in Lagna context
_LAGNA_NATURE_TO_FAVOURABLE: Dict[str, Optional[bool]] = {
    "raja": True,
    "raja_or_fakir": True,
    "mixed": None,      # neutral — skip in conflict detection
    "manda": False,
}


# ═══════════════════════════════════════════════════════════════════
# Core transformation
# ═══════════════════════════════════════════════════════════════════

def _shift_to_chandra_house(natal_house: int, moon_house: int) -> int:
    """Re-anchor a natal house so Moon's natal house becomes H1."""
    return ((int(natal_house) - int(moon_house)) % 12) + 1


def compute_chandra_kundali(
    planet_positions: List[Dict[str, Any]],
    moon_house: int,
    *,
    lagna_interpretations: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Build the Chandra Kundali as an independent LK predictive framework.

    Args:
        planet_positions: list of {"planet": str, "house": int} — natal positions.
        moon_house:       Moon's natal house (1-12). Becomes H1 of Chandra chart.
        lagna_interpretations: optional list from
            `lalkitab_interpretations.get_all_interpretations_for_chart(...)` —
            when supplied, conflicts_with_lagna is filled in.

    Returns:
        {
          "moon_lagna_house": int,
          "chandra_positions": [{planet, planet_hi, natal_house, chandra_house}, ...],
          "readings":          [{planet, planet_hi, chandra_house, en, hi,
                                  is_favourable}, ...],
          "conflicts_with_lagna": [{planet, lagna_house, chandra_house,
                                    lagna_is_favourable, chandra_is_favourable,
                                    lagna_nature, note_en, note_hi}, ...],
          "framework_note_en":   str,
          "framework_note_hi":   str,
          "source":              "LK_CANONICAL_CHANDRA_1952",
        }
    """
    if not isinstance(moon_house, int) or not (1 <= moon_house <= 12):
        raise ValueError(f"moon_house must be int 1-12, got {moon_house!r}")

    # ── 1. Re-anchor every planet ────────────────────────────────
    chandra_positions: List[Dict[str, Any]] = []
    for pos in planet_positions or []:
        planet = pos.get("planet")
        natal_house = pos.get("house")
        if planet not in _VALID_PLANETS:
            continue
        if not isinstance(natal_house, int) or not (1 <= natal_house <= 12):
            continue
        chandra_house = _shift_to_chandra_house(natal_house, moon_house)
        chandra_positions.append({
            "planet": planet,
            "planet_hi": PLANET_NAMES_HI.get(planet, planet),
            "natal_house": natal_house,
            "chandra_house": chandra_house,
        })

    # ── 2. Build per-planet Chandra readings ─────────────────────
    readings: List[Dict[str, Any]] = []
    for cp in chandra_positions:
        reading = get_chandra_reading(cp["planet"], cp["chandra_house"])
        if not reading:
            continue
        readings.append({
            "planet": cp["planet"],
            "planet_hi": cp["planet_hi"],
            "chandra_house": cp["chandra_house"],
            "natal_house": cp["natal_house"],
            "en": reading["en"],
            "hi": reading["hi"],
            "is_favourable": reading["is_favourable"],
        })

    # ── 3. Detect conflicts with Lagna readings (optional) ───────
    conflicts: List[Dict[str, Any]] = []
    if lagna_interpretations:
        conflicts = detect_chandra_lagna_conflicts(readings, lagna_interpretations)

    return {
        "moon_lagna_house": moon_house,
        "chandra_positions": chandra_positions,
        "readings": readings,
        "conflicts_with_lagna": conflicts,
        "framework_note_en": (
            "The Chandra Kundali is an INDEPENDENT Lal Kitab predictive "
            "framework (per LK 1952). Moon becomes H1; every other planet "
            "is re-anchored. Readings here speak to emotion, memory, mother, "
            "public mood, and inner states — NOT a duplicate of the Lagna "
            "chart. Where Lagna and Chandra disagree, both voices matter: "
            "Lagna shows the outer body of life, Chandra shows its inner heart."
        ),
        "framework_note_hi": (
            "चंद्र कुंडली लाल किताब (1952) का एक स्वतंत्र भविष्यसूचक ढांचा है। "
            "चंद्रमा H1 बन जाता है और बाकी सभी ग्रह पुनः-स्थापित हो जाते हैं। "
            "यहाँ पढ़ाई गई बातें भावना, स्मृति, माँ, जन-मानस व आंतरिक स्थिति से "
            "जुड़ी हैं — लग्न कुंडली की नकल नहीं। जब लग्न व चंद्र एक-दूसरे से "
            "असहमत हों, तो दोनों आवाज़ें ज़रूरी हैं: लग्न जीवन का बाहरी शरीर "
            "दिखाता है, चंद्र उसका भीतरी हृदय।"
        ),
        "source": "LK_CANONICAL_CHANDRA_1952",
    }


# ═══════════════════════════════════════════════════════════════════
# Conflict detector
# ═══════════════════════════════════════════════════════════════════

def detect_chandra_lagna_conflicts(
    chandra_readings: List[Dict[str, Any]],
    lagna_interpretations: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Compare each planet's Chandra reading against its Lagna interpretation and
    return a list of planets where the two frameworks DISAGREE.

    A "conflict" is recorded only when BOTH sides have a clear sentiment and
    they differ:
        Lagna "raja" / "raja_or_fakir"  vs  Chandra is_favourable == False
        Lagna "manda"                   vs  Chandra is_favourable == True

    Lagna nature "mixed" is treated as neutral and NEVER flagged — LK 1952
    explicitly avoids forcing interpretation on conditional placements.

    Args:
        chandra_readings:       output of compute_chandra_kundali(...)['readings']
        lagna_interpretations:  output of get_all_interpretations_for_chart(...)

    Returns:
        list of conflict dicts — may be empty.
    """
    # Index Lagna by planet for O(1) lookup.
    lagna_by_planet: Dict[str, Dict[str, Any]] = {
        item["planet"]: item
        for item in lagna_interpretations
        if isinstance(item, dict) and item.get("planet")
    }

    conflicts: List[Dict[str, Any]] = []
    for reading in chandra_readings:
        planet = reading["planet"]
        lagna = lagna_by_planet.get(planet)
        if not lagna:
            continue

        lagna_nature = (lagna.get("nature") or "mixed").lower()
        lagna_fav = _LAGNA_NATURE_TO_FAVOURABLE.get(lagna_nature)
        chandra_fav = bool(reading.get("is_favourable"))

        # Skip neutral/mixed Lagna — we only flag clear disagreements.
        if lagna_fav is None:
            continue
        if lagna_fav == chandra_fav:
            continue

        if lagna_fav and not chandra_fav:
            note_en = (
                f"Lagna chart calls {planet} auspicious (nature: "
                f"{lagna_nature}), but Chandra chart reads it as emotionally "
                f"strained. Outer success may coexist with inner unease."
            )
            note_hi = (
                f"लग्न कुंडली {planet} को शुभ बताती है ({lagna_nature}), "
                f"परन्तु चंद्र कुंडली इसे भावनात्मक रूप से पीड़ित पढ़ती है। "
                f"बाहरी सफलता के साथ भीतरी अशांति संभव।"
            )
        else:
            note_en = (
                f"Lagna chart calls {planet} unfavourable (nature: "
                f"{lagna_nature}), but Chandra chart reads it as emotionally "
                f"blessed. Outer struggle may mask genuine inner peace."
            )
            note_hi = (
                f"लग्न कुंडली {planet} को प्रतिकूल बताती है ({lagna_nature}), "
                f"परन्तु चंद्र कुंडली इसे भावनात्मक रूप से शुभ पढ़ती है। "
                f"बाहरी संघर्ष के पीछे सच्ची आंतरिक शांति छिपी हो सकती है।"
            )

        conflicts.append({
            "planet": planet,
            "planet_hi": PLANET_NAMES_HI.get(planet, planet),
            "lagna_house": lagna.get("house"),
            "chandra_house": reading.get("chandra_house"),
            "lagna_nature": lagna_nature,
            "lagna_is_favourable": lagna_fav,
            "chandra_is_favourable": chandra_fav,
            "note_en": note_en,
            "note_hi": note_hi,
        })

    return conflicts


__all__ = [
    "compute_chandra_kundali",
    "detect_chandra_lagna_conflicts",
]
