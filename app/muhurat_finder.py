"""Muhurat Finder Engine — finds auspicious dates for specific activities."""
import calendar
from datetime import date
from typing import Any, Dict, List

from app.muhurat_rules import (
    MUHURAT_RULES, MUHURAT_ACTIVITIES, DAGDHA_TITHIS,
    get_all_activities, check_day_favorable, normalize_tithi_for_rules,
)
from app.panchang_engine import calculate_panchang


def find_muhurat_dates(
    activity_key: str,
    month: int,
    year: int,
    latitude: float = 28.6139,
    longitude: float = 77.2090,
    limit: int = 10,
) -> Dict[str, Any]:
    """
    Find auspicious dates for an activity in a given month.

    Returns dict with:
    - activity: activity metadata
    - month, year
    - dates: list of favorable date dicts sorted by score
    """
    activity_info = MUHURAT_ACTIVITIES.get(activity_key)
    if not activity_info:
        return {"error": f"Unknown activity: {activity_key}", "dates": []}

    rules = MUHURAT_RULES.get(activity_key)
    if not rules:
        return {"error": "No rules for activity", "dates": []}

    days_in_month = calendar.monthrange(year, month)[1]
    favorable_dates: List[Dict[str, Any]] = []

    for day in range(1, days_in_month + 1):
        d = date(year, month, day)
        d_str = d.isoformat()
        weekday = d.weekday()  # 0=Mon..6=Sun

        try:
            panchang = calculate_panchang(d_str, latitude, longitude)
        except Exception:
            continue

        tithi = panchang.get("tithi", {})
        tithi_index = tithi.get("number", 0)
        tithi_name = tithi.get("name", "")
        paksha = tithi.get("paksha", "")
        nakshatra = panchang.get("nakshatra", {})
        nakshatra_name = nakshatra.get("name", "")
        hindu_month = panchang.get("hindu_calendar", {}).get("maas", "")

        # Check basic favorability
        result = check_day_favorable(
            activity_key, tithi_index, paksha, nakshatra_name, weekday, hindu_month,
        )

        if not result["favorable"]:
            continue

        # Check avoid conditions from panchang data
        skip = False
        avoid = rules.get("avoid_conditions", [])
        planets = panchang.get("planetary_positions", [])

        # Helper: get a planet dict by name
        def _planet(name: str):
            for p in planets:
                if p.get("name") == name:
                    return p
            return {}

        # --- Rahu Kaal: note only, never skip the whole day ---
        # (Rahu Kaal is shown in results so user can pick a window outside it)

        # --- FIX 1: Bhadra realm — only Earth-realm Vishti is dangerous ---
        # Moon in Simha(4)/Kanya(5) or Kumbha(10)/Meena(11) = Bhadra on Earth = forbidden
        # Moon in all other signs = Bhadra in Swarga/Patala = harmless
        if "bhadra" in avoid:
            karana_name = panchang.get("karana", {}).get("name", "").lower()
            if "vishti" in karana_name or "bhadra" in karana_name:
                moon_rashi_idx = _planet("Moon").get("rashi_index")
                BHADRA_EARTH_SIGNS = {4, 5, 10, 11}  # Leo, Virgo, Aquarius, Pisces
                if moon_rashi_idx is None or moon_rashi_idx in BHADRA_EARTH_SIGNS:
                    result["reasons_bad"].append("Bhadra/Vishti on Earth (Leo/Virgo/Aquarius/Pisces Moon)")
                    result["reasons_bad_hindi"] = result.get("reasons_bad_hindi", [])
                    result["reasons_bad_hindi"].append("भद्रा काल — भू-लोक (सिंह/कन्या/कुम्भ/मीन राशि चंद्र)")
                    skip = True
                # else: Bhadra in Swarga/Patala — harmless, do not skip

        # --- Panchaka ---
        if "panchaka" in avoid:
            panchaka = panchang.get("panchaka")
            if isinstance(panchaka, dict) and panchaka.get("active"):
                result["reasons_bad"].append("Panchaka active")
                skip = True

        # --- Ganda Moola ---
        if "ganda_moola" in avoid:
            special = panchang.get("special_yogas", {})
            gm = special.get("ganda_moola", {})
            if isinstance(gm, dict) and gm.get("active"):
                result["reasons_bad"].append("Ganda Moola active")
                skip = True

        # --- FIX 2: Dagdha Tithi — burned day for ALL activities ---
        norm_t = normalize_tithi_for_rules(tithi_index)
        if DAGDHA_TITHIS.get(weekday) == norm_t:
            result["reasons_bad"].append("Dagdha Tithi (burned day — avoid all new work)")
            skip = True

        # ============================================================
        # Marriage-specific classical checks (Muhurta Chintamani)
        # ============================================================
        if activity_key == "marriage":
            # --- FIX 3: Guru/Shukra Asta — Jupiter or Venus combust ---
            # Per classical rule: when Guru or Shukra is asta (combust),
            # all marriages are absolutely forbidden.
            guru = _planet("Jupiter")
            shukra = _planet("Venus")
            if guru.get("combusted"):
                result["reasons_bad"].append("Guru Asta (Jupiter combust) — marriages forbidden")
                skip = True
            if shukra.get("combusted"):
                result["reasons_bad"].append("Shukra Asta (Venus combust) — marriages forbidden")
                skip = True

            # --- FIX 4: Kula Kanthaka Dosha ---
            # Mars in 1st, 8th, or 12th house from Moon = destruction of marriage
            moon_ridx = _planet("Moon").get("rashi_index")
            mars_ridx = _planet("Mars").get("rashi_index")
            if moon_ridx is not None and mars_ridx is not None:
                mars_house = ((mars_ridx - moon_ridx) % 12) + 1
                if mars_house in (1, 8, 12):
                    result["reasons_bad"].append(
                        f"Kula Kanthaka Dosha — Mars in H{mars_house} from Moon"
                    )
                    skip = True

        if skip:
            continue

        # Find favorable lagna windows
        lagna_windows = []
        lagna_table = panchang.get("lagna_table") or []
        for lagna in lagna_table:
            lagna_name = lagna.get("lagna", "")
            if lagna_name in rules.get("favorable_lagnas", []):
                lagna_windows.append({
                    "lagna": lagna_name,
                    "start": lagna.get("start", ""),
                    "end": lagna.get("end", ""),
                })

        favorable_dates.append({
            "date": d_str,
            "weekday": d.strftime("%A"),
            "weekday_hindi": _HINDI_DAYS.get(d.strftime("%A"), ""),
            "tithi": tithi_name,
            "nakshatra": nakshatra_name,
            "paksha": paksha,
            "score": result["score"],
            "reasons_good": result["reasons_good"],
            "sunrise": panchang.get("sunrise", ""),
            "sunset": panchang.get("sunset", ""),
            "rahu_kaal": panchang.get("rahu_kaal", {}),
            "lagna_windows": lagna_windows,
        })

    # Sort by score descending
    favorable_dates.sort(key=lambda x: x["score"], reverse=True)

    return {
        "activity": activity_info,
        "month": month,
        "year": year,
        "latitude": latitude,
        "longitude": longitude,
        "dates": favorable_dates[:limit],
        "total_favorable": len(favorable_dates),
    }


_HINDI_DAYS = {
    "Monday": "सोमवार", "Tuesday": "मंगलवार", "Wednesday": "बुधवार",
    "Thursday": "गुरुवार", "Friday": "शुक्रवार", "Saturday": "शनिवार",
    "Sunday": "रविवार",
}
