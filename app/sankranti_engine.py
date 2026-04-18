"""Sankranti engine — compute Sun ingress times into sidereal rashis.

This module is used by the Panchang API endpoint `/api/panchang/sankranti`.

Notes:
- Calculations are performed in UTC and then converted to a local timezone
  inferred from longitude (same heuristic used in `app/panchang_engine.py`).
- Restriction window uses the classical ±16 hour rule (P0/P1).
- Amritkaal uses the classical 16-ghati (384 min) Punya Kaal window centered
  on ingress, with a 4-ghati (96 min) Maha Punya Kaal sub-period.
- Sankranti type is determined by the vara (weekday) at ingress moment.
- Makar Sankranti (Capricorn ingress) gets additional Uttarayan fields.
- Ayana (Uttarayan/Dakshinayana) is computed for every Sankranti.
- Sign effects (most/least affected rashis) are included per Sankranti.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Any


# ---------------------------------------------------------------------------
# Classical lookup tables
# ---------------------------------------------------------------------------

# 8 Sankranti types keyed by weekday name (as returned by datetime.strftime("%A"))
_SANKRANTI_TYPES: dict[str, dict[str, str]] = {
    "Sunday":    {"type": "Ghora",     "type_hi": "घोर",      "mount": "Elephant", "mount_hi": "हाथी",  "effect": "Inauspicious for grains; good for gold",   "effect_hi": "अन्न के लिए अशुभ; सोने के लिए शुभ"},
    "Monday":    {"type": "Soumya",    "type_hi": "सौम्य",    "mount": "Cow",      "mount_hi": "गाय",   "effect": "Auspicious; prosperity for farmers",        "effect_hi": "शुभ; किसानों के लिए समृद्धि"},
    "Tuesday":   {"type": "Rakshasi",  "type_hi": "राक्षसी",  "mount": "Buffalo",  "mount_hi": "भैंस",  "effect": "Disease and conflict; inauspicious",        "effect_hi": "रोग और संघर्ष; अशुभ"},
    "Wednesday": {"type": "Mandakini", "type_hi": "मन्दाकिनी","mount": "Horse",    "mount_hi": "घोड़ा", "effect": "Mixed; moderate harvests",                  "effect_hi": "मिश्रित; मध्यम फसल"},
    "Thursday":  {"type": "Mandaa",    "type_hi": "मन्दा",    "mount": "Garuda",   "mount_hi": "गरुड़", "effect": "Auspicious; good for religious work",       "effect_hi": "शुभ; धार्मिक कार्य के लिए उत्तम"},
    "Friday":    {"type": "Mahodari",  "type_hi": "महोदरी",   "mount": "Lotus",    "mount_hi": "कमल",   "effect": "Prosperity for trade and arts",             "effect_hi": "व्यापार और कला के लिए समृद्धि"},
    "Saturday":  {"type": "Dhwankshi", "type_hi": "ध्वांक्षी","mount": "Donkey",   "mount_hi": "गधा",   "effect": "Famine and hardship; inauspicious",         "effect_hi": "अकाल और कठिनाई; अशुभ"},
}

# Ayana map keyed by English rashi name (sidereal)
_AYANA_MAP: dict[str, dict[str, str]] = {
    "Makara": {
        "ayana": "Uttarayan",
        "ayana_hi": "उत्तरायण",
        "significance_en": "Sun moves north — auspicious period begins",
        "significance_hi": "सूर्य उत्तर की ओर — शुभ काल प्रारंभ",
    },
    "Karka": {
        "ayana": "Dakshinayana",
        "ayana_hi": "दक्षिणायन",
        "significance_en": "Sun moves south — religious observances favoured",
        "significance_hi": "सूर्य दक्षिण की ओर — धार्मिक अनुष्ठान शुभ",
    },
}

# Rashis in sidereal order (0-indexed, Mesha=0)
_RASHI_LIST = [
    "Mesha", "Vrishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrishchika",
    "Dhanu", "Makara", "Kumbha", "Meena",
]

_RASHI_NAMES = [
    "Mesha",
    "Vrishabha",
    "Mithuna",
    "Karka",
    "Simha",
    "Kanya",
    "Tula",
    "Vrishchika",
    "Dhanu",
    "Makara",
    "Kumbha",
    "Meena",
]

_RASHI_NAMES_HI = [
    "मेष",
    "वृषभ",
    "मिथुन",
    "कर्क",
    "सिंह",
    "कन्या",
    "तुला",
    "वृश्चिक",
    "धनु",
    "मकर",
    "कुंभ",
    "मीन",
]


def _timezone_offset_from_longitude(longitude: float) -> float:
    # Mirror logic in `calculate_panchang()` for predictable API output.
    if 68.0 <= longitude <= 97.5:
        return 5.5
    return round(longitude / 15.0 * 2) / 2


def _sun_rashi_index_sidereal(dt_utc: datetime) -> int:
    """Return sidereal Sun rashi index (0=Mesha…11=Meena) at UTC datetime."""
    try:
        import swisseph as swe  # type: ignore
        from app.astro_engine import _SWE_LOCK

        with _SWE_LOCK:
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            jd = swe.julday(
                dt_utc.year,
                dt_utc.month,
                dt_utc.day,
                dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0,
            )
            xx, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
            lon = float(xx[0]) % 360.0
            return int(lon // 30.0)
    except Exception:
        from app.astro_engine import _approx_sun_longitude, _approx_ayanamsa, _datetime_to_jd

        jd = _datetime_to_jd(dt_utc)
        lon = (_approx_sun_longitude(jd) - _approx_ayanamsa(jd)) % 360.0
        return int(lon // 30.0)


@dataclass(frozen=True)
class SankrantiEvent:
    rashi_index: int
    ingress_utc: datetime


@lru_cache(maxsize=32)
def find_sankranti_times(year: int) -> list[SankrantiEvent]:
    """Find 12 sankranti ingress instants for the given year (UTC), ordered from Mesha."""
    start = datetime(year, 1, 1, 0, 0, tzinfo=timezone.utc)
    end = datetime(year + 1, 1, 1, 0, 0, tzinfo=timezone.utc)

    events: list[SankrantiEvent] = []
    prev_sign = _sun_rashi_index_sidereal(start)

    dt = start + timedelta(days=1)
    while dt <= end and len(events) < 12:
        sign = _sun_rashi_index_sidereal(dt)
        if sign != prev_sign:
            lo = dt - timedelta(days=1)
            hi = dt
            for _ in range(18):  # ~20-30 seconds typical; good enough for API
                mid = lo + (hi - lo) / 2
                if _sun_rashi_index_sidereal(mid) == prev_sign:
                    lo = mid
                else:
                    hi = mid
            events.append(SankrantiEvent(rashi_index=sign, ingress_utc=hi))
            prev_sign = sign
        dt = dt + timedelta(days=1)

    if not events:
        return []

    # Rotate list so that Mesha ingress (rashi_index=0) is first (matches app expectations).
    idx = next((i for i, e in enumerate(events) if e.rashi_index == 0), 0)
    if idx:
        events = events[idx:] + events[:idx]
    return events


def _sankranti_type(ingress_utc: datetime, tz: timezone) -> dict[str, str]:
    """Return the classical Sankranti type based on the vara (weekday) at local ingress."""
    local_dt = ingress_utc.astimezone(tz)
    weekday_name = local_dt.strftime("%A")  # e.g. "Monday"
    return dict(_SANKRANTI_TYPES.get(weekday_name, _SANKRANTI_TYPES["Sunday"]))


def _sankranti_amritkaal(ingress_utc: datetime, tz: timezone) -> dict[str, Any]:
    """Classical 16-ghati Punya Kaal + 4-ghati Maha Punya Kaal centered on ingress.

    1 ghati = 24 minutes.
    Punya Kaal  : 16 ghatis = 384 min  → ±8 ghatis (±192 min) around ingress.
    Maha Punya Kaal: 4 ghatis = 96 min → ±2 ghatis (±48 min) around ingress.
    """
    ghati = 24  # minutes per ghati

    def _fmt(dt_utc: datetime) -> str:
        return dt_utc.astimezone(tz).strftime("%H:%M")

    punya_start = ingress_utc - timedelta(minutes=8 * ghati)
    punya_end   = ingress_utc + timedelta(minutes=8 * ghati)
    maha_start  = ingress_utc - timedelta(minutes=2 * ghati)
    maha_end    = ingress_utc + timedelta(minutes=2 * ghati)

    return {
        "punya_kaal": {
            "start_local": _fmt(punya_start),
            "end_local":   _fmt(punya_end),
            "duration_minutes": 16 * ghati,
        },
        "maha_punya_kaal": {
            "start_local": _fmt(maha_start),
            "end_local":   _fmt(maha_end),
            "duration_minutes": 4 * ghati,
        },
        "is_classical": True,
        "note_en": "Classical 16-ghati window. Maha Punya Kaal (4 ghati) is most auspicious for bath and donation.",
        "note_hi": "शास्त्रीय 16 घटी खिड़की। महा पुण्य काल (4 घटी) स्नान और दान के लिए अत्यंत शुभ।",
    }


def _ayana_info(rashi_name: str) -> dict[str, str] | None:
    """Return Ayana info for the given rashi, or None for non-ayana-change rashis."""
    return _AYANA_MAP.get(rashi_name)


def _makar_special() -> dict[str, Any]:
    """Extra fields added only for Makar Sankranti (Capricorn ingress)."""
    return {
        "is_makar": True,
        "uttarayan_start": True,
        "significance_en": (
            "Makar Sankranti marks Uttarayan — sun begins northward journey. "
            "Most auspicious Sankranti of the year."
        ),
        "significance_hi": (
            "मकर संक्रांति उत्तरायण का आरंभ है — सूर्य उत्तर दिशा में गमन करता है। "
            "वर्ष की सबसे शुभ संक्रांति।"
        ),
        "special_activities_en": [
            "Holy bath (Prayagraj, Haridwar, Pushkar)",
            "Til-gur donation",
            "Kite flying",
            "Khichdi offering",
        ],
        "special_activities_hi": [
            "पवित्र स्नान (प्रयागराज, हरिद्वार, पुष्कर)",
            "तिल-गुड़ दान",
            "पतंग उड़ाना",
            "खिचड़ी अर्पण",
        ],
    }


def _sankranti_sign_effects(rashi_index: int) -> dict[str, list[str]]:
    """Return rashis most / least affected by this Sankranti.

    Most affected  : the ingress rashi itself + its 4th, 7th, 10th (squares/opposition).
    Least affected : 5th and 9th from ingress rashi (trines).
    """
    most  = [_RASHI_LIST[(rashi_index + d) % 12] for d in [0, 3, 6, 9]]
    least = [_RASHI_LIST[(rashi_index + d) % 12] for d in [4, 8]]
    return {"most_affected": most, "least_affected": least}


def build_sankranti_payload(year: int, longitude: float) -> dict[str, Any]:
    """Build API-friendly sankranti payload with local times + windows."""
    tz_offset = _timezone_offset_from_longitude(longitude)
    tz = timezone(timedelta(hours=tz_offset))

    def _fmt_local(dt_utc: datetime) -> str:
        return dt_utc.astimezone(tz).strftime("%Y-%m-%d %H:%M")

    def _fmt_utc(dt_utc: datetime) -> str:
        return dt_utc.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    events = find_sankranti_times(year)
    out: list[dict[str, Any]] = []
    for e in events:
        ingress = e.ingress_utc
        rashi_name = _RASHI_NAMES[e.rashi_index]

        restriction_start = ingress - timedelta(hours=16)
        restriction_end = ingress + timedelta(hours=16)

        # --- 1. Sankranti type (based on vara / weekday at local ingress) ---
        stype = _sankranti_type(ingress, tz)

        # --- 2. Classical 16-ghati amritkaal (replaces heuristic 2-hour window) ---
        amritkaal = _sankranti_amritkaal(ingress, tz)

        # --- 4. Ayana (Uttarayan / Dakshinayana) ---
        ayana = _ayana_info(rashi_name)

        # --- 5. Sign effects ---
        sign_effects = _sankranti_sign_effects(e.rashi_index)

        entry: dict[str, Any] = {
            "rashi_index": e.rashi_index,
            "rashi": rashi_name,
            "rashi_hindi": _RASHI_NAMES_HI[e.rashi_index],
            "ingress_utc": _fmt_utc(ingress),
            "ingress_local": _fmt_local(ingress),
            "restriction_window": {
                "start_local": _fmt_local(restriction_start),
                "end_local": _fmt_local(restriction_end),
                "hours_before": 16,
                "hours_after": 16,
            },
            # Classical amritkaal (was heuristic 2-hour window)
            "amritkaal": amritkaal,
            # Sankranti type
            "sankranti_type": stype,
            # Sign effects
            "sign_effects": sign_effects,
        }

        # --- 4. Ayana info (only for Makara and Karka; others inherit) ---
        if ayana is not None:
            entry["ayana"] = ayana

        # --- 3. Makar Sankranti special fields ---
        if rashi_name == "Makara":
            entry["makar_special"] = _makar_special()

        out.append(entry)

    return {
        "year": year,
        "tz_offset_hours": tz_offset,
        "ordered_from_mesha": True,
        "sankrantis": out,
    }

