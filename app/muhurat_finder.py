"""Muhurat Finder Engine — finds auspicious dates for specific activities.

Classical rules applied (Muhurta Chintamani + standard Jyotish):
  - Tithi / Nakshatra / Weekday / Month filtering
  - Bhadra realm check (Earth vs Swarga/Patala)
  - Dagdha Tithi (burned day) elimination
  - Sankranti (Sun sign ingress) avoidance
  - Guru/Shukra Asta (combustion) block for marriage
  - Kula Kanthaka Dosha for marriage
  - Retrograde Jupiter block for samskaras
  - Retrograde Saturn block for griha/property
  - Simha Surya (Sun in Leo) block for marriage
  - Chandra Balam (optional — requires birth Moon rashi index)
  - Tara Balam   (optional — requires birth nakshatra index)
"""
import calendar
from datetime import date
from typing import Any, Dict, List, Optional

from app.muhurat_rules import (
    MUHURAT_RULES, MUHURAT_ACTIVITIES, DAGDHA_TITHIS,
    get_all_activities, check_day_favorable, normalize_tithi_for_rules,
)
from app.panchang_engine import calculate_panchang

# Good tara numbers (1-indexed): Sampat=2, Kshema=4, Sadhaka=6, Mitra=8, Ati-Mitra=9
_GOOD_TARAS = {2, 4, 6, 8, 9}
# Good Chandra Balam houses (house of current Moon from birth Moon)
_CHANDRA_BALAM_GOOD = {1, 3, 6, 7, 10, 11}


def find_muhurat_dates(
    activity_key: str,
    month: int,
    year: int,
    latitude: float = 28.6139,
    longitude: float = 77.2090,
    limit: int = 10,
    birth_moon_rashi: Optional[int] = None,   # 0-11, Aries=0 … Pisces=11
    birth_nakshatra: Optional[int] = None,    # 0-26
) -> Dict[str, Any]:
    """
    Find auspicious dates for an activity in a given month.

    Optional birth_moon_rashi / birth_nakshatra enable personalised
    Chandra Balam and Tara Balam scoring (±25 pts each, not hard blocks).

    Returns dict with: activity, month, year, dates (sorted by score desc).
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
        weekday = d.weekday()  # 0=Mon … 6=Sun

        try:
            panchang = calculate_panchang(d_str, latitude, longitude)
        except Exception:
            continue

        tithi        = panchang.get("tithi", {})
        tithi_index  = tithi.get("number", 0)
        tithi_name   = tithi.get("name", "")
        paksha       = tithi.get("paksha", "")
        nakshatra    = panchang.get("nakshatra", {})
        nak_name     = nakshatra.get("name", "")
        nak_index    = nakshatra.get("index", 0)
        hindu_month  = panchang.get("hindu_calendar", {}).get("maas", "")
        planets      = panchang.get("planetary_positions", [])

        # ── helper ──────────────────────────────────────────
        def _planet(name: str) -> Dict[str, Any]:
            for p in planets:
                if p.get("name") == name:
                    return p
            return {}

        # ── basic favorability (tithi / nakshatra / weekday / month) ──
        result = check_day_favorable(
            activity_key, tithi_index, paksha, nak_name, weekday, hindu_month,
        )
        if not result["favorable"]:
            continue

        skip  = False
        avoid = rules.get("avoid_conditions", [])

        # ── FIX 1 (previous session): Bhadra realm ──────────────────
        if "bhadra" in avoid:
            karana_name = panchang.get("karana", {}).get("name", "").lower()
            if "vishti" in karana_name or "bhadra" in karana_name:
                moon_ridx = _planet("Moon").get("rashi_index")
                # Earth-realm signs: Leo(4), Virgo(5), Aquarius(10), Pisces(11)
                if moon_ridx is None or moon_ridx in {4, 5, 10, 11}:
                    result["reasons_bad"].append("Bhadra/Vishti on Earth (Leo/Virgo/Aquarius/Pisces Moon)")
                    skip = True

        # ── Panchaka ─────────────────────────────────────────────────
        if "panchaka" in avoid:
            p_obj = panchang.get("panchaka")
            if isinstance(p_obj, dict) and p_obj.get("active"):
                result["reasons_bad"].append("Panchaka active")
                skip = True

        # ── Ganda Moola ──────────────────────────────────────────────
        if "ganda_moola" in avoid:
            gm = panchang.get("special_yogas", {}).get("ganda_moola", {})
            if isinstance(gm, dict) and gm.get("active"):
                result["reasons_bad"].append("Ganda Moola active")
                skip = True

        # ── FIX 2 (previous session): Dagdha Tithi ───────────────────
        norm_t = normalize_tithi_for_rules(tithi_index)
        if DAGDHA_TITHIS.get(weekday) == norm_t:
            result["reasons_bad"].append("Dagdha Tithi — burned day, avoid all new work")
            skip = True

        # ── FIX A: Sankranti — Sun within 1.5° of sign boundary ──────
        if "sankranti" in avoid:
            sun_deg = _planet("Sun").get("degree", 15)  # degree within sign (0-30)
            if sun_deg < 1.5 or sun_deg > 28.5:
                result["reasons_bad"].append("Sankranti — Sun at sign boundary, inauspicious")
                skip = True

        # ── FIX B: Retrograde Jupiter (Guru Vakri) ────────────────────
        if "retrograde_jupiter" in avoid:
            if _planet("Jupiter").get("retrograde"):
                result["reasons_bad"].append("Guru Vakri (Jupiter retrograde) — samskaras forbidden")
                skip = True

        # ── FIX C: Retrograde Saturn (Shani Vakri) ───────────────────
        if "retrograde_saturn" in avoid:
            if _planet("Saturn").get("retrograde"):
                result["reasons_bad"].append("Shani Vakri (Saturn retrograde) — inauspicious for this activity")
                skip = True

        # ════════════════════════════════════════════════════════════
        # Marriage-specific checks
        # ════════════════════════════════════════════════════════════
        if activity_key == "marriage":
            # FIX 3 (previous session): Guru/Shukra Asta
            if _planet("Jupiter").get("combusted"):
                result["reasons_bad"].append("Guru Asta (Jupiter combust) — marriages forbidden")
                skip = True
            if _planet("Venus").get("combusted"):
                result["reasons_bad"].append("Shukra Asta (Venus combust) — marriages forbidden")
                skip = True

            # FIX 4 (previous session): Kula Kanthaka Dosha
            moon_ridx = _planet("Moon").get("rashi_index")
            mars_ridx = _planet("Mars").get("rashi_index")
            if moon_ridx is not None and mars_ridx is not None:
                mars_house = ((mars_ridx - moon_ridx) % 12) + 1
                if mars_house in (1, 8, 12):
                    result["reasons_bad"].append(
                        f"Kula Kanthaka Dosha — Mars in H{mars_house} from Moon"
                    )
                    skip = True

            # FIX D: Simha Surya — Sun in Leo (rashi_index=4) forbidden for marriage
            sun_rashi = _planet("Sun").get("rashi_index")
            if sun_rashi == 4:
                result["reasons_bad"].append("Simha Surya — Sun in Leo, marriage inauspicious")
                skip = True

        if skip:
            continue

        # ════════════════════════════════════════════════════════════
        # FIX E: Chandra Balam (optional — soft scoring, not a block)
        # ════════════════════════════════════════════════════════════
        if birth_moon_rashi is not None:
            current_moon_ridx = _planet("Moon").get("rashi_index")
            if current_moon_ridx is not None:
                house = ((current_moon_ridx - birth_moon_rashi) % 12) + 1
                if house in _CHANDRA_BALAM_GOOD:
                    result["reasons_good"].append(f"Chandra Balam strong (H{house} from birth Moon)")
                    result["score"] = min(100, result["score"] + 25)
                else:
                    result["reasons_bad"].append(f"Chandra Balam weak (H{house} from birth Moon)")
                    result["score"] = max(0, result["score"] - 25)

        # ════════════════════════════════════════════════════════════
        # FIX F: Tara Balam (optional — soft scoring, not a block)
        # ════════════════════════════════════════════════════════════
        if birth_nakshatra is not None:
            tara = ((nak_index - birth_nakshatra) % 9) + 1
            _TARA_NAMES = ["Janma","Sampat","Vipat","Kshema","Pratyari","Sadhaka","Vadha","Mitra","Ati-Mitra"]
            tara_name = _TARA_NAMES[tara - 1]
            if tara in _GOOD_TARAS:
                result["reasons_good"].append(f"Tara Balam — {tara_name} tara (favorable)")
                result["score"] = min(100, result["score"] + 25)
            else:
                result["reasons_bad"].append(f"Tara Balam — {tara_name} tara (unfavorable)")
                result["score"] = max(0, result["score"] - 25)

        # ── Favorable lagna windows ───────────────────────────────────
        lagna_windows = [
            {"lagna": lg.get("lagna", ""), "start": lg.get("start", ""), "end": lg.get("end", "")}
            for lg in (panchang.get("lagna_table") or [])
            if lg.get("lagna") in rules.get("favorable_lagnas", [])
        ]

        favorable_dates.append({
            "date":           d_str,
            "weekday":        d.strftime("%A"),
            "weekday_hindi":  _HINDI_DAYS.get(d.strftime("%A"), ""),
            "tithi":          tithi_name,
            "nakshatra":      nak_name,
            "paksha":         paksha,
            "score":          result["score"],
            "reasons_good":   result["reasons_good"],
            "reasons_bad":    result.get("reasons_bad", []),
            "sunrise":        panchang.get("sunrise", ""),
            "sunset":         panchang.get("sunset", ""),
            "rahu_kaal":      panchang.get("rahu_kaal", {}),
            "lagna_windows":  lagna_windows,
        })

    favorable_dates.sort(key=lambda x: x["score"], reverse=True)

    return {
        "activity":        activity_info,
        "month":           month,
        "year":            year,
        "latitude":        latitude,
        "longitude":       longitude,
        "dates":           favorable_dates[:limit],
        "total_favorable": len(favorable_dates),
    }


_HINDI_DAYS = {
    "Monday": "सोमवार", "Tuesday": "मंगलवार", "Wednesday": "बुधवार",
    "Thursday": "गुरुवार", "Friday": "शुक्रवार", "Saturday": "शनिवार",
    "Sunday": "रविवार",
}
