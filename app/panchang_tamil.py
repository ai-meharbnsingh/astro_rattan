"""
panchang_tamil.py -- Tamil Yoga, Jeevanama & Netrama Calculations
=================================================================
Pure calculation functions (no Flask/FastAPI dependencies).
All strings include English AND Hindi AND Tamil where applicable.

Calculations covered:
- Tamil Yoga (Siddha / Marana yoga based on weekday + nakshatra)
- Jeevanama (Moon's life status based on tithi)
- Netrama (Eye status based on nakshatra pada)
"""
from __future__ import annotations

from typing import Any, Dict

# ============================================================
# TAMIL YOGA (தமிழ் யோகம்) — Weekday + Nakshatra
# ============================================================
# Each weekday has specific nakshatras that create Siddha (auspicious)
# or Marana (inauspicious) yoga. All other combinations are Neutral.
#
# Weekday convention: 0=Sunday .. 6=Saturday
# Nakshatra convention: 0=Ashwini .. 26=Revati (27 nakshatras, 0-indexed)

TAMIL_SIDDHA_NAKSHATRAS: Dict[int, list[int]] = {
    0: [0, 4, 8, 12, 16, 20, 24],   # Sunday: Ashwini, Mrigashira, Pushya, Swati, Purva Ashadha, Purva Bhadrapada, Shatabhisha
    1: [1, 5, 9, 13, 17, 21, 25],   # Monday: Bharani, Ardra, Ashlesha, Vishakha, Uttara Ashadha, Uttara Bhadrapada, Purva Bhadrapada→Dhanishta
    2: [2, 6, 10, 14, 18, 22, 26],  # Tuesday: Krittika, Punarvasu, Magha, Anuradha, Jyeshtha→Shravana, Shatabhisha→Purva Bhadrapada, Revati
    3: [3, 7, 11, 15, 19, 23],      # Wednesday: Rohini, Pushya, Uttara Phalguni→Hasta, Swati→Jyeshtha, Moola, Uttara Bhadrapada→Dhanishta
    4: [0, 4, 8, 12, 16, 20, 24],   # Thursday (same pattern as Sunday)
    5: [1, 5, 9, 13, 17, 21, 25],   # Friday (same pattern as Monday)
    6: [2, 6, 10, 14, 18, 22, 26],  # Saturday (same pattern as Tuesday)
}

TAMIL_MARANA_NAKSHATRAS: Dict[int, list[int]] = {
    0: [2, 6, 10, 14, 18, 22, 26],  # Sunday
    1: [3, 7, 11, 15, 19, 23],      # Monday
    2: [0, 4, 8, 12, 16, 20, 24],   # Tuesday
    3: [1, 5, 9, 13, 17, 21, 25],   # Wednesday
    4: [2, 6, 10, 14, 18, 22, 26],  # Thursday
    5: [3, 7, 11, 15, 19, 23],      # Friday
    6: [0, 4, 8, 12, 16, 20, 24],   # Saturday
}


def calculate_tamil_yoga(weekday: int, nakshatra_index: int) -> Dict[str, Any]:
    """Calculate Tamil Yoga based on weekday + nakshatra combination.

    Args:
        weekday: 0=Sunday .. 6=Saturday
        nakshatra_index: 0=Ashwini .. 26=Revati

    Returns:
        dict with keys: name, name_hindi, name_tamil, auspicious
    """
    if not (0 <= weekday <= 6):
        raise ValueError(f"weekday must be 0-6, got {weekday}")
    if not (0 <= nakshatra_index <= 26):
        raise ValueError(f"nakshatra_index must be 0-26, got {nakshatra_index}")

    siddha_list = TAMIL_SIDDHA_NAKSHATRAS.get(weekday, [])
    marana_list = TAMIL_MARANA_NAKSHATRAS.get(weekday, [])

    if nakshatra_index in siddha_list:
        return {
            "name": "Siddha Yoga",
            "name_hindi": "सिद्ध योग",
            "name_tamil": "சித்த யோகம்",
            "auspicious": True,
        }
    elif nakshatra_index in marana_list:
        return {
            "name": "Marana Yoga",
            "name_hindi": "मरण योग",
            "name_tamil": "மரண யோகம்",
            "auspicious": False,
        }
    else:
        return {
            "name": "Neutral",
            "name_hindi": "सामान्य",
            "name_tamil": "நடுநிலை",
            "auspicious": True,
        }


# ============================================================
# JEEVANAMA (जीवनाम / ஜீவநாமா) — Moon's Life Status
# ============================================================
# Based on which tithi falls in the lunar fortnight:
#   Tithis 1-5:   Full Life   (पूर्ण जीवन / முழு வாழ்வு)
#   Tithis 6-10:  Half Life   (अर्ध जीवन / அரை வாழ்வு)
#   Tithis 11-14: Weak Life   (क्षीण जीवन / பலவீன வாழ்வு)
#   Purnima (15):  Full Life
#   Amavasya (30): Lifeless   (निर्जीव / உயிரற்ற)
#
# For Krishna paksha tithis 16-29, normalise to 1-14 range first.


def calculate_jeevanama(tithi_index: int) -> Dict[str, Any]:
    """Calculate Jeevanama (Moon's life status) based on tithi.

    Args:
        tithi_index: 1-30 (Shukla 1-15, Krishna 16-30)

    Returns:
        dict with keys: status, status_hindi, status_tamil, favorable
    """
    if not (1 <= tithi_index <= 30):
        raise ValueError(f"tithi_index must be 1-30, got {tithi_index}")

    # Special cases: Purnima and Amavasya
    if tithi_index == 15:
        return {
            "status": "Full Life",
            "status_hindi": "पूर्ण जीवन",
            "status_tamil": "முழு வாழ்வு",
            "favorable": True,
        }
    if tithi_index == 30:
        return {
            "status": "Lifeless",
            "status_hindi": "निर्जीव",
            "status_tamil": "உயிரற்ற",
            "favorable": False,
        }

    # Normalise Krishna paksha (16-29) to Shukla range (1-14)
    norm = tithi_index if tithi_index <= 14 else tithi_index - 15

    if 1 <= norm <= 5:
        return {
            "status": "Full Life",
            "status_hindi": "पूर्ण जीवन",
            "status_tamil": "முழு வாழ்வு",
            "favorable": True,
        }
    elif 6 <= norm <= 10:
        return {
            "status": "Half Life",
            "status_hindi": "अर्ध जीवन",
            "status_tamil": "அரை வாழ்வு",
            "favorable": True,
        }
    else:  # 11-14
        return {
            "status": "Weak Life",
            "status_hindi": "क्षीण जीवन",
            "status_tamil": "பலவீன வாழ்வு",
            "favorable": False,
        }


# ============================================================
# NETRAMA (नेत्रम / நேத்ரம்) — Eye Status based on Pada
# ============================================================
# Each nakshatra has 4 padas. The pada determines the eye status:
#   Pada 1, 2: "Seeing"     (दृष्टिवान / பார்வை)      — favorable
#   Pada 3:    "Half Blind" (अर्ध दृष्टि / அரைக் குருடு) — partial
#   Pada 4:    "Blind"      (अन्ध / குருடு)            — unfavorable


def calculate_netrama(nakshatra_index: int, pada: int) -> Dict[str, Any]:
    """Calculate Netrama (eye status) based on nakshatra pada.

    Args:
        nakshatra_index: 0=Ashwini .. 26=Revati (used for validation)
        pada: 1-4 (quarter of the nakshatra)

    Returns:
        dict with keys: status, status_hindi, status_tamil, favorable
    """
    if not (0 <= nakshatra_index <= 26):
        raise ValueError(f"nakshatra_index must be 0-26, got {nakshatra_index}")
    if not (1 <= pada <= 4):
        raise ValueError(f"pada must be 1-4, got {pada}")

    if pada in (1, 2):
        return {
            "status": "Seeing",
            "status_hindi": "दृष्टिवान",
            "status_tamil": "பார்வை",
            "favorable": True,
        }
    elif pada == 3:
        return {
            "status": "Half Blind",
            "status_hindi": "अर्ध दृष्टि",
            "status_tamil": "அரைக் குருடு",
            "favorable": True,
        }
    else:  # pada == 4
        return {
            "status": "Blind",
            "status_hindi": "अन्ध",
            "status_tamil": "குருடு",
            "favorable": False,
        }


# ============================================================
# MASTER FUNCTION
# ============================================================

def calculate_all_tamil(
    weekday: int,
    tithi_index: int,
    nakshatra_index: int,
    pada: int = 1,
) -> Dict[str, Dict[str, Any]]:
    """Calculate all Tamil panchang elements at once.

    Args:
        weekday: 0=Sunday .. 6=Saturday
        tithi_index: 1-30 (Shukla 1-15, Krishna 16-30)
        nakshatra_index: 0=Ashwini .. 26=Revati
        pada: 1-4 (nakshatra pada, defaults to 1)

    Returns:
        dict with keys: tamil_yoga, jeevanama, netrama
    """
    return {
        "tamil_yoga": calculate_tamil_yoga(weekday, nakshatra_index),
        "jeevanama": calculate_jeevanama(tithi_index),
        "netrama": calculate_netrama(nakshatra_index, pada),
    }
