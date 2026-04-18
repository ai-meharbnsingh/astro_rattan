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
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from app.muhurat_rules import (
    MUHURAT_RULES, MUHURAT_ACTIVITIES, DAGDHA_TITHIS,
    get_all_activities, check_day_favorable, normalize_tithi_for_rules,
    MRITYU_YOGA_TITHI, VISHA_YOGA_TITHI,
)
from app.panchang_engine import calculate_panchang

# Good tara numbers (1-indexed): Sampat=2, Kshema=4, Sadhaka=6, Mitra=8, Ati-Mitra=9
_GOOD_TARAS = {2, 4, 6, 8, 9}
# Good Chandra Balam houses (house of current Moon from birth Moon)
_CHANDRA_BALAM_GOOD = {1, 3, 6, 7, 10, 11}

_SANKRANTI_CACHE: dict[int, list[datetime]] = {}

_CHANDRA_BALAM_FRUITS: dict[int, dict[str, str]] = {
    1: {"en": "Generally supportive for starting work.", "hi": "कार्य आरम्भ हेतु सामान्यतः अनुकूल।"},
    2: {"en": "Risk of expense/instability; avoid major commitments.", "hi": "व्यय/अस्थिरता की सम्भावना; बड़े संकल्प टालें।"},
    3: {"en": "Gains through effort; good for travel and initiative.", "hi": "परिश्रम से लाभ; यात्रा/पहल हेतु शुभ।"},
    4: {"en": "Comfort-focused but mixed; proceed with caution.", "hi": "सुख केंद्रित पर मिश्रित; सावधानी से करें।"},
    5: {"en": "Obstacles and delays likely; avoid important ceremonies.", "hi": "विघ्न/विलम्ब; महत्वपूर्ण संस्कार टालें।"},
    6: {"en": "Overcomes enemies and hurdles; favorable for action.", "hi": "शत्रु/बाधा पर विजय; कार्य हेतु अनुकूल।"},
    7: {"en": "Partnership support; good for agreements and rituals.", "hi": "सहयोग/साझेदारी; अनुबंध व अनुष्ठान हेतु शुभ।"},
    8: {"en": "Loss/accident-prone; avoid travel and risky starts.", "hi": "हानि/दुर्घटना-योग; यात्रा व जोखिमपूर्ण आरम्भ टालें।"},
    9: {"en": "Luck and dharma support; good for auspicious starts.", "hi": "भाग्य/धर्म समर्थन; शुभारम्भ हेतु अच्छा।"},
    10: {"en": "Career/authority support; favorable for business openings.", "hi": "कर्म/अधिकार समर्थन; व्यवसाय हेतु शुभ।"},
    11: {"en": "Strong gains; highly favorable for most activities.", "hi": "उत्तम लाभ; अधिकांश कार्यों हेतु बहुत शुभ।"},
    12: {"en": "Fatigue/withdrawal; avoid major new beginnings.", "hi": "थकान/विरक्ति; बड़े नए कार्य टालें।"},
}

_TARA_BALAM_FRUITS: dict[int, dict[str, str]] = {
    1: {"en": "Janma — sensitive; avoid critical beginnings.", "hi": "जन्म — संवेदनशील; महत्वपूर्ण आरम्भ टालें।"},
    2: {"en": "Sampat — prosperity; favorable.", "hi": "सम्पत — समृद्धि; शुभ।"},
    3: {"en": "Vipat — obstacles; avoid.", "hi": "विपत — बाधाएँ; वर्जित।"},
    4: {"en": "Kshema — protection; favorable.", "hi": "क्षेम — संरक्षण; शुभ।"},
    5: {"en": "Pratyari — opposition; caution.", "hi": "प्रत्यरी — विरोध; सावधानी।"},
    6: {"en": "Sadhaka — success; favorable.", "hi": "साधक — सिद्धि; शुभ।"},
    7: {"en": "Vadha/Naidhana — harm; avoid.", "hi": "वध/नैधन — हानि; वर्जित।"},
    8: {"en": "Mitra — support; favorable.", "hi": "मित्र — सहयोग; शुभ।"},
    9: {"en": "Ati-Mitra/Parama Mitra — best; highly favorable.", "hi": "अति-मित्र/परम-मित्र — सर्वोत्तम; अत्यंत शुभ।"},
}


def _sun_sign_index(dt_utc: datetime) -> int:
    """Return sidereal Sun sign index (0=Aries…11=Pisces) at a UTC datetime."""
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


def _find_sankranti_times(year: int) -> list[datetime]:
    """Find approximate Sankranti ingress times for a year (UTC datetimes)."""
    cached = _SANKRANTI_CACHE.get(year)
    if cached is not None:
        return cached

    start = datetime(year, 1, 1, 0, 0, tzinfo=timezone.utc)
    end = datetime(year + 1, 1, 1, 0, 0, tzinfo=timezone.utc)

    sankrantis: list[datetime] = []
    prev_sign = _sun_sign_index(start)

    dt = start + timedelta(days=1)
    while dt <= end and len(sankrantis) < 12:
        sign = _sun_sign_index(dt)
        if sign != prev_sign:
            lo = dt - timedelta(days=1)
            hi = dt
            for _ in range(16):  # ~1 minute resolution
                mid = lo + (hi - lo) / 2
                if _sun_sign_index(mid) == prev_sign:
                    lo = mid
                else:
                    hi = mid
            sankrantis.append(hi)
            prev_sign = sign
        dt = dt + timedelta(days=1)

    # Tests and UI expect index 0 = Mesha (Aries) Sankranti, not Makara.
    # Rotate list so that the ingress *into Aries* is first when available.
    if sankrantis:
        signs_after = [_sun_sign_index(t + timedelta(minutes=5)) for t in sankrantis]
        if 0 in signs_after:
            idx = signs_after.index(0)
            sankrantis = sankrantis[idx:] + sankrantis[:idx]

    _SANKRANTI_CACHE[year] = sankrantis
    return sankrantis


def _is_sankranti_restricted(d: date, sankranti_times: list[datetime]) -> bool:
    """True if the date overlaps the Sankranti restriction window (±16 hours)."""
    day_start = datetime(d.year, d.month, d.day, 0, 0, tzinfo=timezone.utc)
    day_end = day_start + timedelta(days=1)
    for st in sankranti_times:
        window_start = st - timedelta(hours=16)
        window_end = st + timedelta(hours=16)
        if window_start < day_end and window_end > day_start:
            return True
    return False


def _add_lagna_warnings(windows: list[dict[str, Any]]) -> None:
    """Annotate lagna windows with warnings and safe sub-window."""
    SAFE_LAGNA_TRIM_MINS = 14  # rounded ~3°20' on a ~2h lagna

    def to_minutes(t: str) -> int:
        hh, mm = str(t or "0:0").split(":")[:2]
        return int(hh) * 60 + int(mm)

    def from_minutes(m: int) -> str:
        m = m % 1440
        return f"{m // 60:02d}:{m % 60:02d}"

    for w in windows:
        warnings: list[str] = []
        start_m = to_minutes(w.get("start", ""))
        end_m = to_minutes(w.get("end", ""))
        if start_m == end_m:
            warnings.append("Window has zero duration")
            w["warnings"] = warnings
            continue

        duration = end_m - start_m if end_m > start_m else (end_m + 1440 - start_m)
        gs = w.get("ganda_sandhi")
        if gs == "ganda":
            warnings.append("Ganda Lagna — avoid first 3°20'")
        if gs == "sandhi":
            warnings.append("Sandhi Lagna — avoid last 3°20'")

        if duration <= SAFE_LAGNA_TRIM_MINS * 2:
            warnings.append("Window too short for safe lagna after trimming")
            w["warnings"] = warnings
            continue

        w["safe_window"] = {
            "start": from_minutes(start_m + SAFE_LAGNA_TRIM_MINS),
            "end": from_minutes(end_m - SAFE_LAGNA_TRIM_MINS),
        }
        w["warnings"] = warnings


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
    sankranti_times = _find_sankranti_times(year)

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
        yoga_number  = (panchang.get("yoga") or {}).get("number", 0)

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
        chandra_balam_detail: dict[str, Any] | None = None
        tara_balam_detail: dict[str, Any] | None = None

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

        # ── P0-5: Sankranti restriction window (±16h) ────────────────
        if _is_sankranti_restricted(d, sankranti_times):
            result["reasons_bad"].append("Sankranti restriction window (±16 hours)")
            skip = True

        # ── FIX A: Sankranti — Sun within 1.5° of sign boundary ──────
        if "sankranti" in avoid:
            sun_deg = _planet("Sun").get("degree", 15)  # degree within sign (0-30)
            if sun_deg < 1.5 or sun_deg > 28.5:
                result["reasons_bad"].append("Sankranti — Sun at sign boundary, inauspicious")
                skip = True

        # ── P0-1 / P0-2: Vyatipata (#17) and Vaidhriti (#27) blocks ─
        if yoga_number in (17, 27):
            result["reasons_bad"].append("Vyatipata/Vaidhriti Yoga — hard block")
            skip = True

        # ── P0-4: Visha Yoga (tithi+weekday) hard block ─────────────
        if norm_t == VISHA_YOGA_TITHI[weekday]:
            result["reasons_bad"].append("Visha Yoga (tithi+weekday) — hard block")
            skip = True

        # ── P0-3: Mrityu Yoga (tithi+weekday) warning (soft) ────────
        if norm_t == MRITYU_YOGA_TITHI[weekday]:
            result["reasons_bad"].append("Mrityu Yoga (tithi+weekday) — warning")
            result["score"] = max(0, result["score"] - 40)

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

            # WS-F: Guru/Shukra rashi filters (hard filters)
            guru_rashi = _planet("Jupiter").get("rashi_index")
            shukra_rashi = _planet("Venus").get("rashi_index")
            # Allowed Guru rashi: Taurus, Cancer, Virgo, Sagittarius, Pisces
            if guru_rashi is None or guru_rashi not in {1, 3, 5, 8, 11}:
                result["reasons_bad"].append("Guru rashi not favorable for marriage (filter)")
                skip = True
            # Disallowed Shukra rashi: Aries, Cancer, Virgo, Scorpio
            if shukra_rashi is not None and shukra_rashi in {0, 3, 5, 7}:
                result["reasons_bad"].append("Shukra rashi unfavorable for marriage (filter)")
                skip = True

        # ════════════════════════════════════════════════════════════
        # Vastu / Griha Pravesh (WS-G) — preferences (soft scoring)
        # ════════════════════════════════════════════════════════════
        if activity_key in {"griha_pravesh", "bhoomi_puja", "shilanyas", "vastu_shanti"}:
            sun_rashi = _planet("Sun").get("rashi_index")
            # Uttarayan ~ Sun in Capricorn→Gemini (sidereal): 9..11,0..2
            if sun_rashi in {9, 10, 11, 0, 1, 2}:
                result["reasons_good"].append("Uttarayan preference (Sun in Capricorn→Gemini)")
                result["score"] = min(100, result["score"] + 5)
            else:
                result["reasons_bad"].append("Dakshinayan (Uttarayan preferred for construction)")
                result["score"] = max(0, result["score"] - 5)

            if nak_name in {"Pushya", "Rohini", "Hasta"}:
                result["reasons_good"].append("Preferred nakshatra for Vastu/Griha Pravesh")
                result["score"] = min(100, result["score"] + 5)
            else:
                result["reasons_bad"].append("Non-preferred nakshatra (Pushya/Rohini/Hasta preferred)")
                result["score"] = max(0, result["score"] - 5)

        if skip:
            continue

        # ════════════════════════════════════════════════════════════
        # FIX E: Chandra Balam (optional — soft scoring, not a block)
        # ════════════════════════════════════════════════════════════
        if birth_moon_rashi is not None:
            current_moon_ridx = _planet("Moon").get("rashi_index")
            if current_moon_ridx is not None:
                house = ((current_moon_ridx - birth_moon_rashi) % 12) + 1
                fruit = _CHANDRA_BALAM_FRUITS.get(house, {"en": "", "hi": ""})
                chandra_balam_detail = {
                    "house": house,
                    "favorable": house in _CHANDRA_BALAM_GOOD,
                    "interpretation_en": fruit["en"],
                    "interpretation_hi": fruit["hi"],
                }
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
            fruit = _TARA_BALAM_FRUITS.get(tara, {"en": "", "hi": ""})
            tara_balam_detail = {
                "tara": tara,
                "tara_name": tara_name,
                "favorable": tara in _GOOD_TARAS,
                "interpretation_en": fruit["en"],
                "interpretation_hi": fruit["hi"],
            }
            if tara in _GOOD_TARAS:
                result["reasons_good"].append(f"Tara Balam — {tara_name} tara (favorable)")
                result["score"] = min(100, result["score"] + 25)
            else:
                result["reasons_bad"].append(f"Tara Balam — {tara_name} tara (unfavorable)")
                result["score"] = max(0, result["score"] - 25)

        # ── Favorable lagna windows ───────────────────────────────────
        lagna_windows = [
            {
                "lagna": lg.get("lagna", ""),
                "start": lg.get("start", ""),
                "end": lg.get("end", ""),
                "degree": lg.get("degree", 0.0),
                "ganda_sandhi": lg.get("ganda_sandhi"),
            }
            for lg in (panchang.get("lagna_table") or [])
            if lg.get("lagna") in rules.get("favorable_lagnas", [])
        ]
        _add_lagna_warnings(lagna_windows)

        recommended_hora_windows: list[dict[str, Any]] = []
        if activity_key in {"business_start", "shop_opening"}:
            for h in (panchang.get("hora_table") or []):
                lord = h.get("lord")
                if lord in {"Mercury", "Jupiter", "Venus"}:
                    recommended_hora_windows.append(
                        {"lord": lord, "start": h.get("start", ""), "end": h.get("end", ""), "type": h.get("type", "")}
                    )
            recommended_hora_windows = recommended_hora_windows[:6]

        marriage_extras: dict[str, Any] = {}
        if activity_key == "marriage":
            _RASHI_IDX = {
                "Mesha": 0, "Vrishabha": 1, "Mithuna": 2, "Karka": 3,
                "Simha": 4, "Kanya": 5, "Tula": 6, "Vrishchika": 7,
                "Dhanu": 8, "Makara": 9, "Kumbha": 10, "Meena": 11,
            }
            _LAGNA_LORD = {
                "Mesha": "Mars",
                "Vrishabha": "Venus",
                "Mithuna": "Mercury",
                "Karka": "Moon",
                "Simha": "Sun",
                "Kanya": "Mercury",
                "Tula": "Venus",
                "Vrishchika": "Mars",
                "Dhanu": "Jupiter",
                "Makara": "Saturn",
                "Kumbha": "Saturn",
                "Meena": "Jupiter",
            }
            _OWN_SIGNS = {
                "Sun": {4},
                "Moon": {3},
                "Mars": {0, 7},
                "Mercury": {2, 5},
                "Jupiter": {8, 11},
                "Venus": {1, 6},
                "Saturn": {9, 10},
            }
            _EXALT = {
                "Sun": 0,
                "Moon": 1,
                "Mars": 9,
                "Mercury": 5,
                "Jupiter": 3,
                "Venus": 11,
                "Saturn": 6,
            }
            _DEBIL = {
                "Sun": 6,
                "Moon": 7,
                "Mars": 3,
                "Mercury": 11,
                "Jupiter": 9,
                "Venus": 5,
                "Saturn": 0,
            }

            lagna_scores: list[dict[str, Any]] = []
            for w in lagna_windows:
                lagna = w.get("lagna", "")
                lord = _LAGNA_LORD.get(lagna)
                if not lord:
                    continue
                p = _planet(lord)
                s = 50
                if p.get("combusted"):
                    s -= 20
                else:
                    s += 5
                if p.get("retrograde") and lord not in {"Sun", "Moon"}:
                    s -= 10
                else:
                    s += 5
                pr = p.get("rashi_index")
                if isinstance(pr, int):
                    if pr in _OWN_SIGNS.get(lord, set()):
                        s += 15
                    if _EXALT.get(lord) == pr:
                        s += 20
                    if _DEBIL.get(lord) == pr:
                        s -= 20
                s = max(0, min(100, s))
                lagna_scores.append({"lagna": lagna, "lord": lord, "score": s, "start": w.get("start", ""), "end": w.get("end", "")})

            best = max(lagna_scores, key=lambda x: x["score"], default=None)
            if best:
                marriage_extras["lagnasuddhi"] = best
                vivaha_quality = round(result["score"] * 0.7 + best["score"] * 0.3)
            else:
                marriage_extras["lagnasuddhi"] = None
                vivaha_quality = result["score"]

            marriage_extras["vivaha_quality"] = vivaha_quality
            marriage_extras["vivaha_paryapta"] = vivaha_quality >= 70
            if not marriage_extras["vivaha_paryapta"]:
                result["reasons_bad"].append("Vivaha Paryapta gate not met (low composite quality)")

            # Summary card
            good_bits = [nak_name, d.strftime("%A"), f"{paksha} {tithi_name}".strip()]
            risks = [r for r in result.get("reasons_bad", []) if r][:2]
            risk_txt = f" · Risk: {', '.join(risks)}" if risks else ""
            marriage_extras["summary"] = f"Good: {', '.join([b for b in good_bits if b])}{risk_txt}"

        entry = {
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
            "recommended_hora_windows": recommended_hora_windows,
            "chandra_balam": chandra_balam_detail,
            "tara_balam": tara_balam_detail,
        }
        entry.update(marriage_extras)
        favorable_dates.append(entry)

    favorable_dates.sort(key=lambda x: x["score"], reverse=True)

    response = {
        "activity":        activity_info,
        "month":           month,
        "year":            year,
        "latitude":        latitude,
        "longitude":       longitude,
        "dates":           favorable_dates[:limit],
        "total_favorable": len(favorable_dates),
    }
    if activity_key == "marriage":
        all_months = [
            "Chaitra", "Vaishakha", "Jyeshtha", "Ashadha",
            "Shravana", "Bhadrapada", "Ashwin", "Kartik",
            "Margashirsha", "Pausha", "Magha", "Phalguna",
        ]
        allowed = MUHURAT_RULES.get("marriage", {}).get("favorable_months", []) or []
        response["marriage_season_calendar"] = {
            "allowed_months": allowed,
            "forbidden_months": [m for m in all_months if m not in allowed],
        }
    return response


_HINDI_DAYS = {
    "Monday": "सोमवार", "Tuesday": "मंगलवार", "Wednesday": "बुधवार",
    "Thursday": "गुरुवार", "Friday": "शुक्रवार", "Saturday": "शनिवार",
    "Sunday": "रविवार",
}


# ============================================================
# WS-H: Travel Muhurta (Prakarana 10) — direction × nakshatra
# ============================================================

_TRAVEL_MATRIX: dict[str, list[str]] = {
    # NOTE: This is a pragmatic matrix (directional matching + Pushya universal).
    # Directions are normalized in _normalize_direction().
    "E":  ["Ashwini", "Mrigashira", "Punarvasu", "Hasta", "Swati", "Shravana", "Dhanishta"],
    "S":  ["Bharani", "Magha", "Purva Phalguni", "Chitra", "Vishakha", "Purva Ashadha", "Purva Bhadrapada"],
    "W":  ["Rohini", "Ardra", "Ashlesha", "Anuradha", "Moola", "Uttara Ashadha", "Shatabhisha"],
    "N":  ["Krittika", "Pushya", "Uttara Phalguni", "Hasta", "Uttara Ashadha", "Uttara Bhadrapada", "Revati"],
    "NE": ["Ashwini", "Punarvasu", "Pushya", "Hasta", "Uttara Phalguni", "Uttara Ashadha", "Revati"],
    "SE": ["Bharani", "Purva Phalguni", "Chitra", "Vishakha", "Purva Ashadha", "Dhanishta"],
    "SW": ["Rohini", "Ashlesha", "Anuradha", "Moola", "Shatabhisha", "Purva Bhadrapada"],
    "NW": ["Krittika", "Pushya", "Uttara Phalguni", "Hasta", "Shravana", "Uttara Bhadrapada"],
}


def _normalize_direction(direction: str) -> str:
    d = (direction or "").strip().upper().replace(" ", "")
    aliases = {
        "EAST": "E",
        "WEST": "W",
        "NORTH": "N",
        "SOUTH": "S",
        "NORTHEAST": "NE",
        "NORTH-EAST": "NE",
        "NE": "NE",
        "NORTHWEST": "NW",
        "NORTH-WEST": "NW",
        "NW": "NW",
        "SOUTHEAST": "SE",
        "SOUTH-EAST": "SE",
        "SE": "SE",
        "SOUTHWEST": "SW",
        "SOUTH-WEST": "SW",
        "SW": "SW",
        "E": "E",
        "W": "W",
        "N": "N",
        "S": "S",
    }
    return aliases.get(d, d)


def find_travel_muhurat(
    direction: str,
    month: int,
    year: int,
    latitude: float = 28.6139,
    longitude: float = 77.2090,
    limit: int = 10,
) -> Dict[str, Any]:
    """Find auspicious travel dates for a direction using nakshatra matching + Pushya universal bonus."""
    norm_dir = _normalize_direction(direction)
    preferred = _TRAVEL_MATRIX.get(norm_dir, [])
    if not preferred:
        return {"error": f"Invalid direction: {direction}", "dates": []}

    days_in_month = calendar.monthrange(year, month)[1]
    sankranti_times = _find_sankranti_times(year)
    out: list[dict[str, Any]] = []

    for day in range(1, days_in_month + 1):
        d = date(year, month, day)
        d_str = d.isoformat()
        weekday = d.weekday()
        try:
            panchang = calculate_panchang(d_str, latitude, longitude)
        except Exception:
            continue

        tithi = panchang.get("tithi", {}) or {}
        tithi_name = tithi.get("name", "")
        paksha = tithi.get("paksha", "")
        nak = panchang.get("nakshatra", {}) or {}
        nak_name = nak.get("name", "")
        yoga_number = (panchang.get("yoga") or {}).get("number", 0)

        reasons_good: list[str] = []
        reasons_bad: list[str] = []

        # Direction × Nakshatra
        is_pushya = nak_name == "Pushya"
        if nak_name in preferred:
            reasons_good.append(f"Direction match — {norm_dir} travel")
        elif is_pushya:
            reasons_good.append("Pushya Nakshatra — best for travel in all directions")
        else:
            continue

        # Common hard blocks (reuse P0 logic where applicable)
        if _is_sankranti_restricted(d, sankranti_times):
            reasons_bad.append("Sankranti restriction window (±16 hours)")
            continue
        if yoga_number in (17, 27):
            reasons_bad.append("Vyatipata/Vaidhriti Yoga — hard block")
            continue
        # Bhadra / Vishti earth realm
        karana_name = (panchang.get("karana", {}) or {}).get("name", "").lower()
        if "vishti" in karana_name or "bhadra" in karana_name:
            moon_ridx = None
            for p in (panchang.get("planetary_positions") or []):
                if p.get("name") == "Moon":
                    moon_ridx = p.get("rashi_index")
                    break
            if moon_ridx is None or moon_ridx in {4, 5, 10, 11}:
                reasons_bad.append("Bhadra/Vishti on Earth (Leo/Virgo/Aquarius/Pisces Moon)")
                continue
        p_obj = panchang.get("panchaka")
        if isinstance(p_obj, dict) and p_obj.get("active"):
            reasons_bad.append("Panchaka active")
            continue
        gm = (panchang.get("special_yogas", {}) or {}).get("ganda_moola", {})
        if isinstance(gm, dict) and gm.get("active"):
            reasons_bad.append("Ganda Moola active")
            continue

        score = 80
        if is_pushya:
            score = min(100, score + 10)
        if paksha.lower() == "shukla":
            score = min(100, score + 5)
            reasons_good.append("Shukla Paksha preference")

        out.append(
            {
                "date": d_str,
                "weekday": d.strftime("%A"),
                "weekday_hindi": _HINDI_DAYS.get(d.strftime("%A"), ""),
                "tithi": tithi_name,
                "nakshatra": nak_name,
                "paksha": paksha,
                "score": score,
                "reasons_good": reasons_good,
                "reasons_bad": reasons_bad,
                "sunrise": panchang.get("sunrise", ""),
                "sunset": panchang.get("sunset", ""),
                "rahu_kaal": panchang.get("rahu_kaal", {}),
            }
        )

    out.sort(key=lambda x: x["score"], reverse=True)
    return {
        "direction": norm_dir,
        "month": month,
        "year": year,
        "latitude": latitude,
        "longitude": longitude,
        "pushya_guide": {
            "en": "Pushya Nakshatra is traditionally considered auspicious for travel in all directions.",
            "hi": "पुष्य नक्षत्र को परम्परागत रूप से सभी दिशाओं में यात्रा हेतु शुभ माना गया है।",
        },
        "matrix": {k: v for k, v in _TRAVEL_MATRIX.items()},
        "dates": out[:limit],
        "total_favorable": len(out),
    }
