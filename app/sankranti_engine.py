"""Sankranti engine — compute Sun ingress times into sidereal rashis.

This module is used by the Panchang API endpoint `/api/panchang/sankranti`.

Notes:
- Calculations are performed in UTC and then converted to a local timezone
  inferred from longitude (same heuristic used in `app/panchang_engine.py`).
- Restriction window uses the classical ±16 hour rule (P0/P1).
- Punyakaal is returned as a conservative heuristic window and explicitly
  marked as such (classical prahar-specific punyakaal varies by sankranti type).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Any


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
        restriction_start = ingress - timedelta(hours=16)
        restriction_end = ingress + timedelta(hours=16)

        # Heuristic punyakaal (explicitly marked). Classical punyakaal depends on
        # sankranti type (day/night, direction, weekday), which is P2.
        punya_start = ingress - timedelta(hours=1)
        punya_end = ingress + timedelta(hours=1)

        out.append(
            {
                "rashi_index": e.rashi_index,
                "rashi": _RASHI_NAMES[e.rashi_index],
                "rashi_hindi": _RASHI_NAMES_HI[e.rashi_index],
                "ingress_utc": _fmt_utc(ingress),
                "ingress_local": _fmt_local(ingress),
                "restriction_window": {
                    "start_local": _fmt_local(restriction_start),
                    "end_local": _fmt_local(restriction_end),
                    "hours_before": 16,
                    "hours_after": 16,
                },
                "punyakaal": {
                    "start_local": _fmt_local(punya_start),
                    "end_local": _fmt_local(punya_end),
                    "heuristic": True,
                    "note_en": "Heuristic 2-hour window around ingress; classical punyakaal varies by sankranti type.",
                    "note_hi": "यह 2-घंटे का अनुमानित विंडो है; शास्त्रीय पुण्यकाल संक्रांति-प्रकार पर निर्भर करता है।",
                },
            }
        )

    return {
        "year": year,
        "tz_offset_hours": tz_offset,
        "ordered_from_mesha": True,
        "sankrantis": out,
    }

