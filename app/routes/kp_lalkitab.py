"""KP Astrology and Lal Kitab Remedies routes."""
import json
import logging

logger = logging.getLogger(__name__)
from datetime import date as _date
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.astro_engine import calculate_planet_positions
from app.database import get_db
from app.kp_engine import calculate_kp_cuspal, calculate_kp_horary, get_horary_prediction
from app.lalkitab_engine import get_remedies, REMEDIES_BY_HOUSE
from app.models import KPHoraryRequest, KPHoraryPredictRequest
from app.lalkitab_advanced import (
    calculate_masnui_planets,
    calculate_karmic_debts,
    calculate_karmic_debts_with_hora,
    identify_teva_type,
    get_prohibitions,
    calculate_lk_aspects,
    calculate_sleeping_status,
    calculate_kayam_grah,
    calculate_bunyaad,
    calculate_takkar,
    calculate_enemy_presence,
    calculate_dhoka,
    calculate_achanak_chot,
    enrich_debts_active_passive,
)
from app.lalkitab_interpretations import (
    get_all_interpretations_for_chart,
    get_lk_validated_remedies,
)
from app.lalkitab_translations import PLANET_NAMES_HI

router = APIRouter()

# ─────────────────────────────────────────────────────────────
# Sign → LK house mapping (sidereal: Aries=1 … Pisces=12)
# ─────────────────────────────────────────────────────────────
_SIGN_TO_LK_HOUSE = {
    'Aries': 1, 'Taurus': 2, 'Gemini': 3, 'Cancer': 4,
    'Leo': 5, 'Virgo': 6, 'Libra': 7, 'Scorpio': 8,
    'Sagittarius': 9, 'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12,
}

_PLANET_SPEED = {
    'Sun': 'fast', 'Moon': 'fast', 'Mercury': 'fast', 'Venus': 'fast',
    'Mars': 'medium', 'Jupiter': 'slow', 'Saturn': 'slow',
    'Rahu': 'slow', 'Ketu': 'slow',
}

_KNOWN_PLANETS = set(_PLANET_SPEED.keys())


@router.post("/api/kp/cuspal")
def kp_cuspal(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """
    Calculate KP cuspal chart with star lords, sub lords, and significators.

    Contract input: {kundli_id}
    Looks up the kundli, extracts planet_longitudes and house_cusps from chart_data.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT * FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kundli not found",
        )

    # Recalculate chart with KP (Krishnamurti) ayanamsa for accurate KP positions
    chart_data = calculate_planet_positions(
        birth_date=row["birth_date"],
        birth_time=row["birth_time"],
        latitude=row.get("latitude", 0.0),
        longitude=row.get("longitude", 0.0),
        tz_offset=row.get("timezone_offset", 0.0),
        ayanamsa="kp",
    )

    # Extract planet longitudes from chart_data
    planet_longitudes = {}
    for planet_name, info in chart_data.get("planets", {}).items():
        planet_longitudes[planet_name] = info.get("longitude", 0.0)

    # Extract house cusps from chart_data
    house_cusps = chart_data.get("placidus_cusps", chart_data.get("house_cusps", []))
    if not house_cusps or len(house_cusps) != 12:
        # Generate default cusps from ascendant if house_cusps not stored
        asc_lon = chart_data.get("ascendant", {}).get("longitude", 0.0)
        house_cusps = [(asc_lon + i * 30.0) % 360.0 for i in range(12)]

    if not planet_longitudes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet longitudes",
        )

    try:
        result = calculate_kp_cuspal(planet_longitudes, house_cusps)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    # Contract response: {cuspal_chart, significators}
    return {
        "cuspal_chart": {
            "cusps": result.get("cusps", []),
            "planets": result.get("planets", {}),
        },
        "significators": result.get("significators", {}),
    }


@router.post("/api/lalkitab/remedies")
def lalkitab_remedies(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """
    Get Lal Kitab remedies for weak or afflicted planets.

    Contract input: {kundli_id}
    Looks up the kundli, extracts planet_positions from chart_data.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT * FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kundli not found",
        )

    chart_data = json.loads(row["chart_data"])

    # Extract planet positions as {planet: sign}
    planet_positions = {}
    for planet_name, info in chart_data.get("planets", {}).items():
        planet_positions[planet_name] = info.get("sign", "Aries")

    if not planet_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet positions",
        )

    try:
        res = get_remedies(planet_positions)
        # Transform into flat list for frontend with translations.
        # Look up the authentic Hindi (Devanagari) version from REMEDIES_BY_HOUSE
        # using the planet + lk_house. If no match is found we emit remedy_hi=None
        # rather than duplicating English — duplication would be a fraud pattern.
        remedies_list = []
        for planet, info in res.items():
            if not info.get("remedies"):
                continue
            lk_house = info.get("lk_house", 0)
            house_remedy = REMEDIES_BY_HOUSE.get(planet, {}).get(lk_house, {})
            en_from_house = house_remedy.get("en")
            hi_from_house = house_remedy.get("hi")
            for r_text in info["remedies"]:
                # Match the backward-compat English string against the house remedy.
                # get_remedies() builds compat_remedies from house_remedy["en"],
                # so these should be equal — but fall back safely.
                if en_from_house and r_text == en_from_house and hi_from_house:
                    remedy_hi_val = hi_from_house
                elif hi_from_house:
                    remedy_hi_val = hi_from_house
                else:
                    # No authentic Hindi available — do NOT duplicate English.
                    remedy_hi_val = None
                remedies_list.append({
                    "planet_en": planet,
                    "planet_hi": PLANET_NAMES_HI.get(planet, planet),
                    "remedy_en": r_text,
                    "remedy_hi": remedy_hi_val,
                })
        return {"remedies": remedies_list}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )


@router.get("/api/lalkitab/remedies/enriched/{kundli_id}")
def get_enriched_remedies(kundli_id: str, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """
    Return enriched remedies for ALL 9 planets: problem / reason / remedy / how_it_works.
    Always returns all planets (not just weak ones) so the UI can show education for every house.
    """
    row = db.execute(
        "SELECT chart_data, birth_date FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])
    planet_positions = {p: info.get("sign", "Aries") for p, info in chart_data.get("planets", {}).items()}
    if not planet_positions:
        raise HTTPException(status_code=400, detail="No planet positions in chart")

    res = get_remedies(planet_positions)
    enriched = []
    for planet, info in res.items():
        r = info["remedy"]
        enriched.append({
            "planet": planet,
            "planet_hi": PLANET_NAMES_HI.get(planet, planet),
            "sign": info["sign"],
            "lk_house": info["lk_house"],
            "dignity": info["dignity"],
            "strength": info["strength"],
            "has_remedy": info["has_remedy"],
            "urgency": r.get("urgency", "low"),
            "material": r.get("material", ""),
            "day": r.get("day", ""),
            # Remedy action
            "remedy_en": r.get("en", ""),
            "remedy_hi": r.get("hi", ""),
            # Education fields
            "problem_en": r.get("problem_en", ""),
            "problem_hi": r.get("problem_hi", ""),
            "reason_en": r.get("reason_en", ""),
            "reason_hi": r.get("reason_hi", ""),
            "how_en": r.get("how_en", ""),
            "how_hi": r.get("how_hi", ""),
        })
    # Sort: weak/high urgency first, then by house number
    urgency_order = {"high": 0, "medium": 1, "low": 2}
    enriched.sort(key=lambda x: (0 if x["has_remedy"] else 1, urgency_order.get(x["urgency"], 2), x["lk_house"]))
    return {"remedies": enriched}


# ─────────────────────────────────────────────────────────────
# Lal Kitab Remedy Tracker
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/tracker/{kundli_id}")
def get_tracker_state(kundli_id: str, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """Return all tracker logs for a kundli: {logs: [{date, completed_ids}], journal: [...]}"""
    user_id = user["sub"]
    logs = db.execute(
        "SELECT date, completed_ids FROM lk_tracker_logs WHERE user_id = %s AND kundli_id = %s ORDER BY date",
        (user_id, kundli_id),
    ).fetchall()
    journal = db.execute(
        "SELECT date, note, created_at FROM lk_journal_entries WHERE user_id = %s AND source = 'tracker' AND kundli_id = %s ORDER BY created_at DESC LIMIT 30",
        (user_id, kundli_id),
    ).fetchall()
    done_map = {row["date"]: json.loads(row["completed_ids"] or "[]") for row in logs}
    journal_list = [{"date": r["date"], "note": r["note"]} for r in journal]
    return {"done_map": done_map, "journal": journal_list}


@router.post("/api/lalkitab/tracker/{kundli_id}/toggle")
def toggle_tracker_remedy(kundli_id: str, payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """Toggle a remedy done/undone for today. payload: {date, remedy_id}"""
    user_id = user["sub"]
    date = payload.get("date")
    remedy_id = payload.get("remedy_id")
    if not date or not remedy_id:
        raise HTTPException(status_code=400, detail="date and remedy_id required")

    row = db.execute(
        "SELECT completed_ids FROM lk_tracker_logs WHERE user_id = %s AND kundli_id = %s AND date = %s",
        (user_id, kundli_id, date),
    ).fetchone()

    if row:
        ids = json.loads(row["completed_ids"] or "[]")
        if remedy_id in ids:
            ids.remove(remedy_id)
        else:
            ids.append(remedy_id)
        db.execute(
            "UPDATE lk_tracker_logs SET completed_ids = %s, updated_at = NOW() WHERE user_id = %s AND kundli_id = %s AND date = %s",
            (json.dumps(ids), user_id, kundli_id, date),
        )
    else:
        ids = [remedy_id]
        db.execute(
            "INSERT INTO lk_tracker_logs (user_id, kundli_id, date, completed_ids) VALUES (%s, %s, %s, %s)",
            (user_id, kundli_id, date, json.dumps(ids)),
        )
    db.commit()
    return {"date": date, "completed_ids": ids}


@router.post("/api/lalkitab/tracker/{kundli_id}/journal")
def add_tracker_journal(kundli_id: str, payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """Add a journal entry for the tracker. payload: {date, note}"""
    user_id = user["sub"]
    date = payload.get("date")
    note = (payload.get("note") or "").strip()
    if not date or not note:
        raise HTTPException(status_code=400, detail="date and note required")
    db.execute(
        "INSERT INTO lk_journal_entries (user_id, source, kundli_id, date, note) VALUES (%s, 'tracker', %s, %s, %s)",
        (user_id, kundli_id, date, note),
    )
    db.commit()
    return {"ok": True}


# ─────────────────────────────────────────────────────────────
# Lal Kitab Chandra Chalana Protocol
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/chandra")
def get_chandra_state(user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """Return the user's Chandra protocol state."""
    user_id = user["sub"]
    row = db.execute(
        "SELECT start_date, completed_days FROM lk_chandra_protocol WHERE user_id = %s",
        (user_id,),
    ).fetchone()
    journal = db.execute(
        "SELECT date, note FROM lk_journal_entries WHERE user_id = %s AND source = 'chandra' ORDER BY created_at DESC LIMIT 60",
        (user_id,),
    ).fetchall()
    if row:
        return {
            "start_date": row["start_date"],
            "completed_days": json.loads(row["completed_days"] or "[]"),
            "journal": [{"date": r["date"], "note": r["note"]} for r in journal],
        }
    return {"start_date": None, "completed_days": [], "journal": [{"date": r["date"], "note": r["note"]} for r in journal]}


@router.post("/api/lalkitab/chandra/start")
def start_chandra_protocol(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """Start or restart the 43-day Chandra protocol. payload: {start_date}"""
    user_id = user["sub"]
    start_date = payload.get("start_date")
    if not start_date:
        raise HTTPException(status_code=400, detail="start_date required")
    row = db.execute("SELECT id FROM lk_chandra_protocol WHERE user_id = %s", (user_id,)).fetchone()
    if row:
        db.execute(
            "UPDATE lk_chandra_protocol SET start_date = %s, completed_days = '[]', updated_at = NOW() WHERE user_id = %s",
            (start_date, user_id),
        )
    else:
        db.execute(
            "INSERT INTO lk_chandra_protocol (user_id, start_date, completed_days) VALUES (%s, %s, '[]')",
            (user_id, start_date),
        )
    db.commit()
    return {"start_date": start_date, "completed_days": []}


@router.post("/api/lalkitab/chandra/mark-done")
def mark_chandra_day_done(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """Mark today as done in the protocol. payload: {date}"""
    user_id = user["sub"]
    date = payload.get("date")
    if not date:
        raise HTTPException(status_code=400, detail="date required")
    row = db.execute("SELECT completed_days FROM lk_chandra_protocol WHERE user_id = %s", (user_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Protocol not started")
    days = json.loads(row["completed_days"] or "[]")
    if date not in days:
        days.append(date)
        db.execute(
            "UPDATE lk_chandra_protocol SET completed_days = %s, updated_at = NOW() WHERE user_id = %s",
            (json.dumps(days), user_id),
        )
        db.commit()
    return {"completed_days": days}


@router.post("/api/lalkitab/chandra/journal")
def add_chandra_journal(payload: dict, user: dict = Depends(get_current_user), db: Any = Depends(get_db)):
    """Add a Chandra protocol journal entry. payload: {date, note}"""
    user_id = user["sub"]
    date = payload.get("date")
    note = (payload.get("note") or "").strip()
    if not date or not note:
        raise HTTPException(status_code=400, detail="date and note required")
    db.execute(
        "INSERT INTO lk_journal_entries (user_id, source, date, note) VALUES (%s, 'chandra', %s, %s)",
        (user_id, date, note),
    )
    db.commit()
    return {"ok": True}


# ─────────────────────────────────────────────────────────────
# Lal Kitab Gochar (Live Transit Positions)
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/gochar")
def get_gochar_transits(user: dict = Depends(get_current_user)):
    """Return today's live planetary positions mapped to LK houses (sidereal/Lahiri)."""
    import logging
    from app.mundane_engine import _get_current_planet_positions

    logger = logging.getLogger(__name__)
    try:
        planets = _get_current_planet_positions()
    except Exception as exc:
        logger.error("gochar: failed to compute planet positions: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Could not compute planetary positions")

    transits = []
    for pname, pdata in planets.items():
        if pname not in _KNOWN_PLANETS:
            continue
        sign = pdata.get("sign", "Aries")
        transits.append({
            "planet": pname,
            "sign": sign,
            "sign_degree": round(pdata.get("sign_degree") or 0.0, 2),
            "nakshatra": pdata.get("nakshatra"),
            "retrograde": bool(pdata.get("retrograde", False)),
            "lk_house": _SIGN_TO_LK_HOUSE.get(sign, 0),
            "speed_note": _PLANET_SPEED.get(pname, "medium"),
        })

    return {"transits": transits, "as_of": _date.today().isoformat()}


# ─────────────────────────────────────────────────────────────
# Lal Kitab Nishaniyan (Signs/Omens from DB)
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/nishaniyan/{kundli_id}")
def get_nishaniyan(
    kundli_id: str,
    category: str = None,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return nishaniyan (omens/signs) from DB matched to chart planet positions."""
    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])
    # Build list of (planet_lower, lk_house) tuples
    planet_house_pairs = []
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        sign = info.get("sign", "Aries")
        house = _SIGN_TO_LK_HOUSE.get(sign, 0)
        if house:
            planet_house_pairs.append((planet_name.lower(), house))

    if not planet_house_pairs:
        return {"nishaniyan": []}

    # Build parameterised WHERE clause
    placeholders = " OR ".join(
        "(planet = %s AND house = %s)" for _ in planet_house_pairs
    )
    params = [val for pair in planet_house_pairs for val in pair]

    if category:
        query = (
            f"SELECT * FROM nishaniyan_master WHERE ({placeholders}) AND category = %s"
            " ORDER BY planet, house"
        )
        params.append(category)
    else:
        query = (
            f"SELECT * FROM nishaniyan_master WHERE ({placeholders})"
            " ORDER BY planet, house"
        )

    rows = db.execute(query, params).fetchall()
    nishaniyan = [
        {
            "id": r["id"],
            "planet": r["planet"],
            "house": r["house"],
            "nishani_text": r["nishani_text"],
            "nishani_text_en": r["nishani_text_en"],
            "category": r["category"],
            "severity": r["severity"],
        }
        for r in rows
    ]
    return {"nishaniyan": nishaniyan}


# ─────────────────────────────────────────────────────────────
# Lal Kitab Rin (Karmic Debts)
# ─────────────────────────────────────────────────────────────

# Which houses indicate affliction/weakness → activates related rin
_AFFLICTION_HOUSES = {6, 8, 12}

# Planet → rin debt_type mapping (primary planet for each debt)
_PLANET_TO_RIN = {
    "sun": "पितृ ऋण",
    "moon": "मातृ ऋण",
    "mercury": "भ्रातृ ऋण",
    "jupiter": "देव ऋण",
    "venus": "स्त्री ऋण",
    "mars": "शत्रु ऋण",
    "saturn": "पितामह ऋण",
    "rahu": "प्रपितामह ऋण",
    "ketu": "प्रपितामह ऋण",
}


@router.get("/api/lalkitab/rin/{kundli_id}")
def get_rin(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return Lal Kitab rin (karmic debts) with active flag based on chart."""
    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])

    # Find which planets are in affliction houses
    afflicted_planets: set[str] = set()
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        sign = info.get("sign", "Aries")
        house = _SIGN_TO_LK_HOUSE.get(sign, 0)
        # NOTE: Simplified affliction model — checks only houses 6/8/12 (Dusthana).
        # Does not include lordship afflictions or Pakka Ghar deviations. Full
        # affliction model lives in lalkitab_advanced.analyze_full_affliction().
        if house in _AFFLICTION_HOUSES:
            afflicted_planets.add(planet_name.lower())

    # Fetch all 8 debts from DB
    debt_rows = db.execute(
        "SELECT * FROM lal_kitab_debts ORDER BY debt_type"
    ).fetchall()

    debts = []
    for r in debt_rows:
        # Mark active if the associated planet is afflicted
        associated_planet = r["planet"]  # lowercase e.g. "sun"
        active = associated_planet in afflicted_planets
        debts.append({
            "id": r["id"],
            "debt_type": r["debt_type"],
            "planet": r["planet"],
            "description": r["description"],
            "indication": r["indication"],
            "remedy": r["remedy"],
            "active": active,
        })

    return {"debts": debts, "afflicted_planets": sorted(afflicted_planets)}


# ─────────────────────────────────────────────────────────────
# Lal Kitab Predictions (Marriage / Career / Health / Wealth)
# ─────────────────────────────────────────────────────────────

_MANGLIK_HOUSES = {1, 2, 4, 7, 8, 12}

# 10th house planet → career mapping
_CAREER_MAP = {
    "sun": {
        "careers": ["सरकारी नौकरी", "प्रशासन", "राजनीति", "डॉक्टर"],
        "en_careers": ["Government Service", "Administration", "Politics", "Doctor"],
        "nature": "job",
    },
    "moon": {
        "careers": ["व्यापार", "जल व्यवसाय", "कृषि", "दूध-डेयरी"],
        "en_careers": ["Trade", "Water-related business", "Agriculture", "Dairy"],
        "nature": "business",
    },
    "mars": {
        "careers": ["सेना", "पुलिस", "इंजीनियरिंग", "ठेकेदारी"],
        "en_careers": ["Military", "Police", "Engineering", "Contracting"],
        "nature": "job",
    },
    "mercury": {
        "careers": ["लेखन", "व्यापार", "एकाउंटेंट", "मीडिया"],
        "en_careers": ["Writing", "Trade", "Accounting", "Media"],
        "nature": "business",
    },
    "jupiter": {
        "careers": ["शिक्षा", "धर्म", "न्याय", "बैंकिंग"],
        "en_careers": ["Education", "Religion", "Law", "Banking"],
        "nature": "job",
    },
    "venus": {
        "careers": ["कला", "फैशन", "मनोरंजन", "होटल"],
        "en_careers": ["Arts", "Fashion", "Entertainment", "Hospitality"],
        "nature": "business",
    },
    "saturn": {
        "careers": ["मजदूरी", "निर्माण", "खनिज", "तेल-गैस"],
        "en_careers": ["Labour", "Construction", "Mining", "Oil & Gas"],
        "nature": "job",
    },
    "rahu": {
        "careers": ["तकनीक", "विदेश व्यापार", "अनुसंधान", "राजनीति"],
        "en_careers": ["Technology", "Foreign Trade", "Research", "Politics"],
        "nature": "business",
    },
    "ketu": {
        "careers": ["अध्यात्म", "चिकित्सा", "गुप्त विज्ञान", "खोज"],
        "en_careers": ["Spirituality", "Medicine", "Occult", "Research"],
        "nature": "business",
    },
}

# 6/8/12 house planets → health areas
_HEALTH_MAP = {
    "sun": {"area": "हृदय, आंखें, रीढ़", "en_area": "Heart, Eyes, Spine"},
    "moon": {"area": "मन, फेफड़े, तरल", "en_area": "Mind, Lungs, Fluids"},
    "mars": {"area": "रक्त, मांसपेशी, सर्जरी", "en_area": "Blood, Muscles, Surgery risk"},
    "mercury": {"area": "नसें, त्वचा, पाचन", "en_area": "Nerves, Skin, Digestion"},
    "jupiter": {"area": "यकृत, मोटापा, मधुमेह", "en_area": "Liver, Obesity, Diabetes"},
    "venus": {"area": "गुर्दे, त्वचा, प्रजनन", "en_area": "Kidneys, Skin, Reproductive"},
    "saturn": {"area": "हड्डियां, जोड़, दांत", "en_area": "Bones, Joints, Teeth"},
    "rahu": {"area": "मानसिक विकार, अज्ञात रोग", "en_area": "Mental disorders, Unknown ailments"},
    "ketu": {"area": "संक्रमण, रहस्यमय रोग", "en_area": "Infections, Mysterious illness"},
}

# Jupiter/Venus house → wealth potential
_WEALTH_MAP = {
    1: {"potential": "उत्तम", "en": "Excellent", "score": 90},
    2: {"potential": "श्रेष्ठ", "en": "Superior", "score": 95},
    4: {"potential": "अच्छा", "en": "Good", "score": 75},
    5: {"potential": "उत्तम", "en": "Excellent", "score": 88},
    7: {"potential": "व्यापार से", "en": "Through business", "score": 80},
    9: {"potential": "भाग्यशाली", "en": "Lucky", "score": 92},
    10: {"potential": "कर्म से", "en": "Through hard work", "score": 78},
    11: {"potential": "श्रेष्ठ", "en": "Superior", "score": 93},
    3: {"potential": "मध्यम", "en": "Moderate", "score": 60},
    6: {"potential": "संघर्ष", "en": "Struggle", "score": 45},
    8: {"potential": "उतार-चढ़ाव", "en": "Fluctuating", "score": 55},
    12: {"potential": "व्यय", "en": "Expenditure", "score": 40},
}


def _get_planet_positions(kundli_id: str, user_id: str, db: Any) -> dict:
    """Fetch chart_data and return {planet_lower: lk_house} mapping."""
    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user_id),
    ).fetchone()
    if not row:
        return None
    chart_data = json.loads(row["chart_data"])
    positions = {}
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        sign = info.get("sign", "Aries")
        house = _SIGN_TO_LK_HOUSE.get(sign, 0)
        positions[planet_name.lower()] = house
    return positions


@router.get("/api/lalkitab/predictions/marriage/{kundli_id}")
def predict_marriage(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Marriage predictions: Manglik check, 7th house lord, Venus placement."""
    positions = _get_planet_positions(kundli_id, user["sub"], db)
    if positions is None:
        raise HTTPException(status_code=404, detail="Kundli not found")

    mars_house = positions.get("mars", 0)
    is_manglik = mars_house in _MANGLIK_HOUSES
    manglik_severity = (
        "strong" if mars_house in {1, 7, 8} else
        "moderate" if mars_house in {2, 4, 12} else
        "none"
    )

    venus_house = positions.get("venus", 0)
    seventh_planets = [p for p, h in positions.items() if h == 7]

    # Spouse quality based on Venus house
    venus_descriptions = {
        1: {"hi": "आकर्षक और प्रभावशाली जीवनसाथी", "en": "Attractive, dominant spouse"},
        2: {"hi": "धनी और सुखी परिवार", "en": "Wealthy, happy family life"},
        3: {"hi": "साहसी, यात्रा-प्रिय साथी", "en": "Adventurous, travel-loving partner"},
        4: {"hi": "घरेलू और सुखी जीवन", "en": "Domestic, happy life"},
        5: {"hi": "प्रेम-विवाह, रचनात्मक साथी", "en": "Love marriage, creative partner"},
        6: {"hi": "स्वास्थ्य-सावधानी, सेवा-प्रिय साथी", "en": "Health-conscious, service-oriented partner"},
        7: {"hi": "उत्तम वैवाहिक जीवन", "en": "Excellent marital life"},
        8: {"hi": "गहरा बंधन, पारिवारिक सम्पत्ति", "en": "Deep bond, inherited property"},
        9: {"hi": "भाग्यशाली, धार्मिक साथी", "en": "Lucky, religious partner"},
        10: {"hi": "कार्यक्षेत्र से मिलन, उच्च पद", "en": "Career-driven partner, high status"},
        11: {"hi": "मित्र से विवाह, लाभदायक", "en": "Friendship leads to marriage, profitable"},
        12: {"hi": "विदेश-निवास संभव, अध्यात्मिक साथी", "en": "Foreign settlement possible, spiritual partner"},
    }

    spouse_desc = venus_descriptions.get(venus_house, {"hi": "सामान्य वैवाहिक जीवन", "en": "Average marital life"})

    # Manglik remedies
    manglik_remedies = []
    if is_manglik:
        manglik_remedies = [
            "मंगलवार को हनुमान चालीसा पाठ करें",
            "लाल मसूर या गुड़ मंगलवार को दान करें",
            "मंगल यंत्र स्थापित करें",
        ]

    return {
        "is_manglik": is_manglik,
        "manglik_severity": manglik_severity,
        "mars_house": mars_house,
        "venus_house": venus_house,
        "spouse_description": spouse_desc,
        "seventh_house_planets": seventh_planets,
        "manglik_remedies": manglik_remedies,
        "compatibility_note": {
            "hi": "मांगलिक दोष होने पर मांगलिक से विवाह शुभ होता है" if is_manglik else "मंगल दोष नहीं — सामान्य विवाह योग",
            "en": "Manglik should marry a Manglik for harmony" if is_manglik else "No Manglik dosha — normal marriage prospects",
        },
    }


@router.get("/api/lalkitab/predictions/career/{kundli_id}")
def predict_career(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Career predictions: 10th house planet, Saturn, Sun placements."""
    positions = _get_planet_positions(kundli_id, user["sub"], db)
    if positions is None:
        raise HTTPException(status_code=404, detail="Kundli not found")

    tenth_planets = [p for p, h in positions.items() if h == 10]
    primary = tenth_planets[0] if tenth_planets else None

    career_info = _CAREER_MAP.get(primary, {
        "careers": ["विविध क्षेत्र", "स्वतंत्र कार्य"],
        "en_careers": ["Diverse fields", "Self-employment"],
        "nature": "business",
    }) if primary else {
        "careers": ["विविध क्षेत्र", "स्वतंत्र कार्य"],
        "en_careers": ["Diverse fields", "Self-employment"],
        "nature": "business",
    }

    sun_house = positions.get("sun", 0)
    saturn_house = positions.get("saturn", 0)
    mercury_house = positions.get("mercury", 0)

    # Business vs job suitability
    business_indicators = sum([
        positions.get("mercury", 0) in {2, 3, 7, 10, 11},
        positions.get("venus", 0) in {2, 7, 11},
        positions.get("jupiter", 0) in {2, 5, 9, 11},
        positions.get("moon", 0) in {2, 7, 11},
    ])
    job_indicators = sum([
        positions.get("sun", 0) in {1, 9, 10},
        positions.get("saturn", 0) in {3, 6, 10, 11},
        positions.get("mars", 0) in {1, 3, 6, 10},
    ])
    suitability = "business" if business_indicators > job_indicators else "job"

    # Favourable age periods by 10th house planet
    favourable_ages = {
        "sun": [22, 32, 42],
        "moon": [24, 32, 40],
        "mars": [28, 36, 44],
        "mercury": [25, 34, 45],
        "jupiter": [30, 39, 48],
        "venus": [25, 33, 41],
        "saturn": [32, 42, 52],
        "rahu": [27, 35, 42],
        "ketu": [30, 40, 50],
    }

    return {
        "tenth_house_planets": tenth_planets,
        "primary_planet": primary,
        "career_options": career_info["careers"],
        "career_options_en": career_info["en_careers"],
        "nature": career_info["nature"],
        "suitability": suitability,
        "favourable_ages": favourable_ages.get(primary, [28, 36, 44]),
        "sun_house": sun_house,
        "saturn_house": saturn_house,
        "mercury_house": mercury_house,
        "advice": {
            "hi": f"{'व्यापार में अधिक लाभ' if suitability == 'business' else 'नौकरी में स्थिरता'} — दसवें भाव में {'कोई ग्रह नहीं' if not primary else primary.capitalize()} है",
            "en": f"{'Business favoured for higher gains' if suitability == 'business' else 'Job brings stability'} — {primary.capitalize() if primary else 'No planet'} in 10th house",
        },
    }


@router.get("/api/lalkitab/predictions/health/{kundli_id}")
def predict_health(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Health predictions: planets in 6/8/12 houses, Sun/Moon/Mars/Saturn placements."""
    positions = _get_planet_positions(kundli_id, user["sub"], db)
    if positions is None:
        raise HTTPException(status_code=404, detail="Kundli not found")

    # Planets in health-sensitive houses
    health_house_planets = {
        6: [p for p, h in positions.items() if h == 6],
        8: [p for p, h in positions.items() if h == 8],
        12: [p for p, h in positions.items() if h == 12],
    }

    vulnerable_areas = []
    precautions = []
    chronic_risk = []

    for house, planets in health_house_planets.items():
        for planet in planets:
            info = _HEALTH_MAP.get(planet, {})
            if info:
                vulnerable_areas.append({
                    "planet": planet,
                    "house": house,
                    "area_hi": info["area"],
                    "area_en": info["en_area"],
                })
            if house == 8:
                chronic_risk.append(planet)

    # Additional key planet checks
    sun_house = positions.get("sun", 0)
    moon_house = positions.get("moon", 0)
    mars_house = positions.get("mars", 0)
    saturn_house = positions.get("saturn", 0)

    if sun_house in {6, 8, 12}:
        precautions.append({"hi": "हृदय रोग से सावधानी, नियमित जांच करें", "en": "Beware of heart issues, regular checkups"})
    if moon_house in {6, 8, 12}:
        precautions.append({"hi": "मानसिक स्वास्थ्य पर ध्यान दें, ध्यान करें", "en": "Focus on mental health, meditate regularly"})
    if mars_house in {6, 8, 12}:
        precautions.append({"hi": "रक्त-विकार व चोट से बचें", "en": "Avoid blood disorders, be cautious of injuries"})
    if saturn_house in {6, 8, 12}:
        precautions.append({"hi": "जोड़ों व हड्डियों की देखभाल करें", "en": "Take care of joints and bones"})

    overall = "caution" if len(vulnerable_areas) >= 3 else "moderate" if vulnerable_areas else "good"

    return {
        "overall_health": overall,
        "vulnerable_areas": vulnerable_areas,
        "precautions": precautions,
        "chronic_risk_planets": chronic_risk,
        "health_house_planets": {str(k): v for k, v in health_house_planets.items()},
        "sun_house": sun_house,
        "moon_house": moon_house,
        "mars_house": mars_house,
        "saturn_house": saturn_house,
    }


@router.get("/api/lalkitab/predictions/wealth/{kundli_id}")
def predict_wealth(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Wealth predictions: Jupiter/Venus placement, 2nd/11th house analysis."""
    positions = _get_planet_positions(kundli_id, user["sub"], db)
    if positions is None:
        raise HTTPException(status_code=404, detail="Kundli not found")

    jupiter_house = positions.get("jupiter", 0)
    venus_house = positions.get("venus", 0)
    second_planets = [p for p, h in positions.items() if h == 2]
    eleventh_planets = [p for p, h in positions.items() if h == 11]

    jup_wealth = _WEALTH_MAP.get(jupiter_house, {"potential": "मध्यम", "en": "Moderate", "score": 60})
    ven_wealth = _WEALTH_MAP.get(venus_house, {"potential": "मध्यम", "en": "Moderate", "score": 60})
    wealth_score = round((jup_wealth["score"] + ven_wealth["score"]) / 2)

    # Income sources based on 2nd/11th house planets
    income_source_map = {
        "sun": {"hi": "सरकार/पिता से आय", "en": "Income from government/father"},
        "moon": {"hi": "व्यापार/माता से आय", "en": "Income from trade/mother"},
        "mars": {"hi": "भूमि/साहस से आय", "en": "Income from land/courage"},
        "mercury": {"hi": "बुद्धि/व्यापार से आय", "en": "Income from intellect/business"},
        "jupiter": {"hi": "शिक्षा/धर्म से आय", "en": "Income from education/spirituality"},
        "venus": {"hi": "कला/विलासिता से आय", "en": "Income from arts/luxury"},
        "saturn": {"hi": "मेहनत/सेवा से आय", "en": "Income from hard work/service"},
        "rahu": {"hi": "तकनीक/विदेश से आय", "en": "Income from technology/foreign"},
        "ketu": {"hi": "गुप्त/अध्यात्म से आय", "en": "Income from occult/spirituality"},
    }

    income_sources = []
    for p in second_planets + eleventh_planets:
        src = income_source_map.get(p)
        if src and src not in income_sources:
            income_sources.append(src)

    # Investment advice based on Jupiter house
    investment_map = {
        1: {"hi": "स्वयं के व्यवसाय में निवेश करें", "en": "Invest in own business"},
        2: {"hi": "सोना, चांदी, नकद बचत", "en": "Gold, silver, cash savings"},
        4: {"hi": "भूमि, मकान में निवेश", "en": "Real estate investment"},
        5: {"hi": "शेयर, लॉटरी, सट्टे में सावधानी", "en": "Stocks with caution, avoid speculation"},
        7: {"hi": "साझेदारी में निवेश लाभदायक", "en": "Partnership investments beneficial"},
        9: {"hi": "धर्म-स्थान, विदेश में निवेश", "en": "Religious places, foreign investment"},
        10: {"hi": "व्यवसाय विस्तार में निवेश", "en": "Business expansion investment"},
        11: {"hi": "सभी प्रकार का निवेश शुभ", "en": "All types of investment favourable"},
    }
    investment_advice = investment_map.get(
        jupiter_house,
        {"hi": "सावधानी से निवेश करें", "en": "Invest cautiously"},
    )

    return {
        "wealth_score": wealth_score,
        "wealth_potential_hi": jup_wealth["potential"],
        "wealth_potential_en": jup_wealth["en"],
        "jupiter_house": jupiter_house,
        "venus_house": venus_house,
        "second_house_planets": second_planets,
        "eleventh_house_planets": eleventh_planets,
        "income_sources": income_sources,
        "investment_advice": investment_advice,
        "savings_tip": {
            "hi": "गुरु ११वें भाव में हो तो बचत अवश्य करें" if jupiter_house == 11 else "नियमित बचत और दान दोनों आवश्यक हैं",
            "en": "Jupiter in 11th — always save regularly" if jupiter_house == 11 else "Regular savings and charity both essential",
        },
    }


# ─────────────────────────────────────────────────────────────
# Lal Kitab Remedies Master (position-based from DB)
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/remedies/master/{kundli_id}")
def get_remedies_master(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return position-based remedies from remedies_master for each planet in its LK house."""
    positions = _get_planet_positions(kundli_id, user["sub"], db)
    if positions is None:
        raise HTTPException(status_code=404, detail="Kundli not found")

    # Build list of active planet-house pairs (skip house=0)
    active_planets = [p for p, h in positions.items() if h != 0]
    active_houses = [h for p, h in positions.items() if h != 0]

    remedies = []
    if active_planets:
        # Single query instead of N separate queries (one per planet)
        rows = db.execute(
            "SELECT * FROM remedies_master WHERE planet = ANY(%s) AND house = ANY(%s)",
            (active_planets, active_houses),
        ).fetchall()
        # Filter to only matching (planet, house) pairs since ANY is OR-based
        valid_pairs = {(p, h) for p, h in positions.items() if h != 0}
        for r in rows:
            if (r["planet"], r["house"]) in valid_pairs:
                remedies.append({
                    "planet": r["planet"],
                    "house": r["house"],
                    "remedy_text": r["remedy_text"],
                    "remedy_type": r["remedy_type"],
                    "duration_days": r["duration_days"],
                    "instructions": r["instructions"],
                    "caution": r["caution"],
                })

    return {"remedies": remedies}


@router.get("/api/lalkitab/advanced/{kundli_id}")
def get_lalkitab_advanced(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return advanced Lal Kitab analysis: Masnui Grah, Karmic Debts (with Hora), Teva type, and Prohibitions."""
    # Use the shared helper so we get the authoritative house derivation
    # (prefers explicit chart_data.planets[p]["house"], falls back to sign).
    # This eliminates the earlier sign-only bug that contradicted _get_lk_positions.
    positions, row = _get_lk_positions(kundli_id, user["sub"], db)

    # formatted_positions: list of {"planet": "Sun", "house": N} — already correct shape.
    formatted_positions = [
        {"planet": p["planet"].capitalize(), "house": p["house"]}
        for p in positions
    ]

    # Calculate Hora-based karmic debts if birth datetime available
    hora_debt_analysis = None
    try:
        from datetime import datetime
        birth_datetime = datetime.combine(
            datetime.strptime(row["birth_date"], "%Y-%m-%d").date(),
            datetime.strptime(row["birth_time"], "%H:%M:%S").time()
        )
        hora_debt_analysis = calculate_karmic_debts_with_hora(
            formatted_positions, 
            birth_datetime=birth_datetime
        )
    except Exception as e:
        logger.warning("Hora calculation failed: %s", e)

    # Calculate new logic
    lk_aspects = calculate_lk_aspects(formatted_positions)
    sleeping_info = calculate_sleeping_status(formatted_positions)
    kayam_planets = calculate_kayam_grah(formatted_positions, lk_aspects)

    return {
        "masnui_planets": calculate_masnui_planets(formatted_positions),
        "karmic_debts": hora_debt_analysis["final_debts"] if hora_debt_analysis else calculate_karmic_debts(formatted_positions),
        "karmic_debts_hora_analysis": hora_debt_analysis,
        "teva_type": identify_teva_type(formatted_positions),
        "prohibitions": get_prohibitions(formatted_positions),
        "aspects": lk_aspects,
        "sleeping": sleeping_info,
        "kayam": kayam_planets
    }


# ─────────────────────────────────────────────────────────────
# Lal Kitab Bunyaad / Takkar / Enemy Presence Analysis
# ─────────────────────────────────────────────────────────────

@router.post("/api/kp-lalkitab/lk-analysis")
def lk_analysis(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Combined Lal Kitab analysis: Bunyaad (Foundation), Takkar (Collision), Enemy Presence.

    Contract input: {kundli_id}
    Returns bunyaad, takkar, and enemy_presence results.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])

    # Build formatted_positions matching the pattern used by advanced endpoint
    formatted_positions = []
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        sign = info.get("sign", "Aries")
        house = _SIGN_TO_LK_HOUSE.get(sign, 0)
        if house:
            formatted_positions.append({
                "planet": planet_name,
                "house": house,
            })

    if not formatted_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet positions",
        )

    try:
        bunyaad = calculate_bunyaad(formatted_positions)
        takkar = calculate_takkar(formatted_positions)
        enemy_presence = calculate_enemy_presence(formatted_positions)
    except Exception as exc:
        logger.error("LK analysis error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return {
        "bunyaad": bunyaad,
        "takkar": takkar,
        "enemy_presence": enemy_presence,
    }


# ─────────────────────────────────────────────────────────────
# Lal Kitab House-by-House Planet Interpretations
# ─────────────────────────────────────────────────────────────

@router.post("/api/kp-lalkitab/lk-interpretations")
def lk_interpretations(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Return per-house Lal Kitab interpretations for every planet in the kundli.

    Contract input: {kundli_id}
    Returns list of interpretation dicts with nature, effect_en/hi, conditions, keywords.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])

    formatted_positions = []
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        sign = info.get("sign", "Aries")
        house = _SIGN_TO_LK_HOUSE.get(sign, 0)
        if house:
            formatted_positions.append({
                "planet": planet_name,
                "house": house,
            })

    if not formatted_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet positions",
        )

    try:
        interpretations = get_all_interpretations_for_chart(formatted_positions)
    except Exception as exc:
        logger.error("LK interpretations error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return {"interpretations": interpretations}


@router.post("/api/kp-lalkitab/lk-validated-remedies")
def lk_validated_remedies(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Return applicable validated Lal Kitab remedies based on planet positions.

    Contract input: {kundli_id}
    Returns list of remedy dicts with name, procedure, validation status.
    """
    kundli_id = payload.get("kundli_id")
    if not kundli_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="kundli_id is required",
        )

    row = db.execute(
        "SELECT chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    chart_data = json.loads(row["chart_data"])

    formatted_positions = []
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        sign = info.get("sign", "Aries")
        house = _SIGN_TO_LK_HOUSE.get(sign, 0)
        if house:
            formatted_positions.append({
                "planet": planet_name,
                "house": house,
            })

    if not formatted_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart data has no planet positions",
        )

    try:
        remedies = get_lk_validated_remedies(formatted_positions)
    except Exception as exc:
        logger.error("LK validated remedies error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return {"remedies": remedies}


# ─────────────────────────────────────────────────────────────
# Saved Predictions (Bookmark)
# ─────────────────────────────────────────────────────────────

@router.post("/api/lalkitab/predictions/save")
def save_prediction(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Save a prediction bookmark. payload: {kundli_id, prediction_type, prediction_data, note}"""
    kundli_id = payload.get("kundli_id")
    prediction_type = payload.get("prediction_type", "").strip()
    prediction_data = payload.get("prediction_data", {})
    note = (payload.get("note") or "").strip()

    if not kundli_id or not prediction_type:
        raise HTTPException(status_code=400, detail="kundli_id and prediction_type required")

    db.execute(
        "INSERT INTO saved_predictions (user_id, kundli_id, prediction_type, prediction_data, note) "
        "VALUES (%s, %s, %s, %s, %s)",
        (user["sub"], kundli_id, prediction_type, json.dumps(prediction_data), note),
    )
    db.commit()
    return {"ok": True}


@router.get("/api/lalkitab/predictions/saved/{kundli_id}")
def get_saved_predictions(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return all saved predictions for a kundli."""
    rows = db.execute(
        "SELECT id, prediction_type, prediction_data, note, created_at "
        "FROM saved_predictions WHERE user_id = %s AND kundli_id = %s ORDER BY created_at DESC",
        (user["sub"], kundli_id),
    ).fetchall()

    predictions = []
    for r in rows:
        predictions.append({
            "id": r["id"],
            "prediction_type": r["prediction_type"],
            "prediction_data": json.loads(r["prediction_data"]) if r["prediction_data"] else {},
            "note": r["note"],
            "created_at": r["created_at"].isoformat() if r["created_at"] else None,
        })

    return {"predictions": predictions}


@router.delete("/api/lalkitab/predictions/saved/{prediction_id}")
def delete_saved_prediction(
    prediction_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Delete a saved prediction by ID (owner-only)."""
    result = db.execute(
        "DELETE FROM saved_predictions WHERE id = %s AND user_id = %s",
        (prediction_id, user["sub"]),
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"ok": True}


# ─────────────────────────────────────────────────────────────
# KP Horary (Prashna) — 1-249 Number System
# ─────────────────────────────────────────────────────────────

@router.post("/api/kp/horary")
def kp_horary(
    body: KPHoraryRequest,
    user: dict = Depends(get_current_user),
):
    """
    Calculate a full KP Horary chart from querent's number (1-249).

    Returns horary number details, house cusps, planets with star/sub lords,
    significators, and ruling planets for the query moment.
    """
    try:
        result = calculate_kp_horary(
            number=body.number,
            query_datetime=body.query_datetime,
            query_place=body.query_place,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error("KP Horary calculation error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return result


@router.post("/api/kp/horary/predict")
def kp_horary_predict(
    body: KPHoraryPredictRequest,
    user: dict = Depends(get_current_user),
):
    """
    Get a KP Horary prediction for a specific question type.

    Supported question types: marriage, job, travel, health, finance,
    legal, education, property.

    Returns full horary chart plus prediction analysis with verdict
    (favorable / unfavorable / mixed) and timing estimate.
    """
    try:
        result = get_horary_prediction(
            number=body.number,
            question_type=body.question_type,
            query_datetime=body.query_datetime,
            query_place=body.query_place,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error("KP Horary prediction error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return result


# ═══════════════════════════════════════════════════════════════════
# HELPER — extract LK planet positions from kundli_id
# ═══════════════════════════════════════════════════════════════════

def _get_lk_positions(kundli_id: str, user_sub: str, db: Any):
    """Load kundli from DB, convert to LK planet-position list."""
    row = db.execute(
        "SELECT * FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user_sub),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")
    try:
        raw = row["chart_data"]
        chart_data = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except (json.JSONDecodeError, TypeError):
        raise HTTPException(status_code=500, detail="Corrupt chart data")
    positions = []
    for planet_name, info in chart_data.get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS:
            continue
        if not isinstance(info, dict):
            continue
        # Prefer explicit house number if present, else derive from sign
        if "house" in info and isinstance(info["house"], int):
            house = info["house"]
        else:
            sign = info.get("sign", "")
            house = _SIGN_TO_LK_HOUSE.get(sign, 0)
        if house > 0:
            positions.append({"planet": planet_name, "house": house})
    return positions, row


# ═══════════════════════════════════════════════════════════════════
# PALMISTRY (Samudrik Shastra)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/palm/zones")
def get_palm_zones():
    """Return all palm zones (mounts + lines) with planet/house mappings. No auth required."""
    from app.lalkitab_palmistry import get_palm_zones as _zones, MARK_TYPES
    return {"zones": _zones(), "mark_types": MARK_TYPES}


@router.post("/api/lalkitab/palm/correlate")
def correlate_palm_marks(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    payload: {kundli_id, palm_marks: [{zone_id, mark_type}]}
    Returns palm-to-chart correlations with interpretations and remedies.
    """
    from app.lalkitab_palmistry import calculate_palm_correlations
    kundli_id = payload.get("kundli_id")
    marks = payload.get("palm_marks", payload.get("marks", []))  # accept both keys
    if not kundli_id:
        raise HTTPException(status_code=400, detail="kundli_id required")
    if not isinstance(marks, list):
        raise HTTPException(status_code=400, detail="palm_marks must be a list")
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    return calculate_palm_correlations(positions, marks)


# ═══════════════════════════════════════════════════════════════════
# AGE MILESTONE TRIGGERS (Safar-e-Zindagi)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/milestones/{kundli_id}")
def get_age_milestones(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return Safar-e-Zindagi age milestone analysis with countdown to next trigger."""
    from app.lalkitab_milestones import calculate_age_milestones
    positions, row = _get_lk_positions(kundli_id, user["sub"], db)
    birth_date = str(row.get("birth_date") or row.get("dob") or "").strip()
    if not birth_date:
        try:
            raw = row["chart_data"]
            cd = json.loads(raw) if isinstance(raw, str) else (raw or {})
            birth_date = cd.get("birth_date", "")
        except Exception:
            birth_date = ""
    if not birth_date:
        raise HTTPException(status_code=422, detail="birth_date not found in kundli")
    return calculate_age_milestones(birth_date, positions)


# ═══════════════════════════════════════════════════════════════════
# TECHNICAL LOGIC (Chalti Gaadi, Dhur-Dhur-Aage, Soya Ghar)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/technical/{kundli_id}")
def get_technical_analysis(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return Chalti Gaadi, Dhur-Dhur-Aage, Soya Ghar, Planet Statuses, Muththi and Kayam Grah analysis."""
    from app.lalkitab_technical import (
        calculate_chalti_gaadi,
        calculate_dhur_dhur_aage,
        calculate_soya_ghar,
        classify_all_planet_statuses,
        calculate_muththi,
    )
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    lk_aspects = calculate_lk_aspects(positions)
    return {
        "chalti_gaadi": calculate_chalti_gaadi(positions),
        "dhur_dhur_aage": calculate_dhur_dhur_aage(positions),
        "soya_ghar": calculate_soya_ghar(positions),
        "planet_statuses": classify_all_planet_statuses(positions),
        "muththi": calculate_muththi(positions),
        "kayam": calculate_kayam_grah(positions, lk_aspects),
    }


# ═══════════════════════════════════════════════════════════════════
# BALI KA BAKRA (Sacrifice Analysis)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/sacrifice/{kundli_id}")
def get_sacrifice_analysis(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return Bali Ka Bakra sacrifice chain analysis for this chart."""
    from app.lalkitab_sacrifice import analyze_sacrifice
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    results = analyze_sacrifice(positions)
    return {
        "kundli_id": kundli_id,
        "sacrifice_count": len(results),
        "has_sacrifices": len(results) > 0,
        "results": results,
    }


# ═══════════════════════════════════════════════════════════════════
# FORBIDDEN REMEDIES
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/forbidden/{kundli_id}")
def get_forbidden_list(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return dynamic forbidden actions list based on this chart's planet placements."""
    from app.lalkitab_forbidden import get_forbidden_remedies
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    results = get_forbidden_remedies(positions)
    return {
        "kundli_id": kundli_id,
        "forbidden_count": len(results),
        "rules": results,
    }


# ═══════════════════════════════════════════════════════════════════
# FAMILY CHART LINKING (Grah-Gasti)
# ═══════════════════════════════════════════════════════════════════

def _positions_from_chart(chart_data: dict) -> list:
    """Parse planet positions from a chart_data dict (no DB lookup)."""
    positions = []
    for planet_name, info in (chart_data or {}).get("planets", {}).items():
        if planet_name not in _KNOWN_PLANETS or not isinstance(info, dict):
            continue
        if "house" in info and isinstance(info["house"], int):
            house = info["house"]
        else:
            house = _SIGN_TO_LK_HOUSE.get(info.get("sign", ""), 0)
        if house > 0:
            positions.append({"planet": planet_name, "house": house})
    return positions


@router.get("/api/lalkitab/family/{kundli_id}")
def get_family_links(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return family chart links with per-member harmony analysis."""
    from app.lalkitab_family import calculate_family_harmony, get_family_dominant_planet, get_family_theme

    owner_row = db.execute(
        "SELECT id, chart_data FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not owner_row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    try:
        raw = owner_row["chart_data"]
        owner_chart = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except Exception:
        owner_chart = {}
    owner_positions = _positions_from_chart(owner_chart)

    links = db.execute(
        """SELECT lf.id AS link_id, lf.member_kundli_id, lf.relation,
                  k.person_name, k.birth_date, k.chart_data
           FROM lal_kitab_family_links lf
           JOIN kundlis k ON k.id = lf.member_kundli_id
           WHERE lf.owner_kundli_id = %s AND lf.user_id = %s
           ORDER BY lf.created_at""",
        (kundli_id, user["sub"]),
    ).fetchall()

    linked_members = []
    all_scores = []
    all_positions = list(owner_positions)

    for link in links:
        try:
            raw_m = link["chart_data"]
            member_chart = json.loads(raw_m) if isinstance(raw_m, str) else (raw_m or {})
        except Exception:
            member_chart = {}
        member_positions = _positions_from_chart(member_chart)
        harmony = calculate_family_harmony(owner_positions, member_positions, member_name=link["person_name"])
        all_scores.append(harmony["harmony_score"])
        all_positions.extend(member_positions)
        linked_members.append({
            "link_id": link["link_id"],
            "kundli_id": link["member_kundli_id"],
            "name": link["person_name"],
            "relation": link["relation"],
            "birth_date": link["birth_date"],
            "harmony_score": harmony["harmony_score"],
            "shared_planets": harmony["shared_planets"],
            "support_planets": harmony["support_planets"],
            "tension_planets": harmony["tension_planets"],
            "theme": harmony["theme"],
            "cross_waking_narratives": harmony["cross_waking_narratives"],
        })

    avg_score = round(sum(all_scores) / len(all_scores)) if all_scores else 0
    dominant_planet = get_family_dominant_planet(all_positions) if all_positions else None
    family_theme = get_family_theme(avg_score) if all_scores else None

    return {
        "kundli_id": kundli_id,
        "linked_members": linked_members,
        "family_harmony": avg_score,
        "dominant_planet": dominant_planet,
        "family_theme": family_theme,
    }


@router.post("/api/lalkitab/family/{kundli_id}/link")
def add_family_link(
    kundli_id: str,
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Link a family member kundli to the owner kundli. payload: {member_kundli_id, relation}"""
    member_kundli_id = payload.get("member_kundli_id", "").strip()
    relation = payload.get("relation", "family").strip()
    if not member_kundli_id:
        raise HTTPException(status_code=400, detail="member_kundli_id required")
    if member_kundli_id == kundli_id:
        raise HTTPException(status_code=400, detail="Cannot link kundli to itself")

    owner = db.execute(
        "SELECT id FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner kundli not found")

    member = db.execute(
        "SELECT id FROM kundlis WHERE id = %s AND user_id = %s",
        (member_kundli_id, user["sub"]),
    ).fetchone()
    if not member:
        raise HTTPException(status_code=404, detail="Member kundli not found or not yours")

    try:
        row = db.execute(
            """INSERT INTO lal_kitab_family_links (owner_kundli_id, member_kundli_id, relation, user_id)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (owner_kundli_id, member_kundli_id) DO UPDATE SET relation = EXCLUDED.relation
               RETURNING id""",
            (kundli_id, member_kundli_id, relation, user["sub"]),
        ).fetchone()
        db.commit()
    except Exception as e:
        logger.warning("[family_link] insert error: %s", e)
        raise HTTPException(status_code=500, detail="Failed to create link")

    return {"link_id": row["id"], "status": "linked"}


@router.delete("/api/lalkitab/family/{kundli_id}/link/{link_id}")
def remove_family_link(
    kundli_id: str,
    link_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Remove a family member link."""
    row = db.execute(
        """DELETE FROM lal_kitab_family_links
           WHERE id = %s AND owner_kundli_id = %s AND user_id = %s
           RETURNING id""",
        (link_id, kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Link not found")
    db.commit()
    return {"status": "unlinked"}


# ═══════════════════════════════════════════════════════════════════
# VASTU DIRECTIONAL DIAGNOSIS (Makaan)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/vastu/{kundli_id}")
def get_vastu_diagnosis_route(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Vastu home-layout diagnosis from LK planet positions."""
    from app.lalkitab_vastu import get_vastu_diagnosis
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    return get_vastu_diagnosis(positions)


# ═══════════════════════════════════════════════════════════════════
# 7-YEAR SUB-CYCLE
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/seven-year-cycle/{kundli_id}")
def get_seven_year_cycle_route(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return the active 7-year sub-cycle for a kundli."""
    from app.lalkitab_milestones import get_seven_year_cycle
    positions, row = _get_lk_positions(kundli_id, user["sub"], db)
    birth_date_str = row.get("birth_date", "")
    try:
        from datetime import date
        bdate = _date.fromisoformat(birth_date_str)
        current_age = (date.today() - bdate).days // 365
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="birth_date missing or invalid — cannot compute seven-year cycle",
        )
    return get_seven_year_cycle(current_age, positions)


# ═══════════════════════════════════════════════════════════════════
# DHOKA (DECEPTION) + ACHANAK CHOT (SUDDEN STRIKE)
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/relationship-engine/{kundli_id}")
def get_relationship_engine(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Returns Takkar, Dhoka, Achanak Chot, and Bunyaad analysis."""
    from app.lalkitab_advanced import calculate_takkar, calculate_bunyaad, calculate_dhoka, calculate_achanak_chot
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    return {
        "takkar":      calculate_takkar(positions),
        "dhoka":       calculate_dhoka(positions),
        "achanak_chot": calculate_achanak_chot(positions),
        "bunyaad":     calculate_bunyaad(positions),
    }


# ═══════════════════════════════════════════════════════════════════
# ACTIVE vs PASSIVE RIN
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/rin-active/{kundli_id}")
def get_active_rin(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Returns karmic debts with active/passive activation status."""
    from app.lalkitab_advanced import calculate_karmic_debts, enrich_debts_active_passive
    positions, _ = _get_lk_positions(kundli_id, user["sub"], db)
    debts = calculate_karmic_debts(positions)
    return {"debts": enrich_debts_active_passive(debts, positions)}


# ═══════════════════════════════════════════════════════════════════
# 43-DAY REMEDY TRACKER
# ═══════════════════════════════════════════════════════════════════

@router.get("/api/lalkitab/remedy-tracker/{kundli_id}")
def list_remedy_trackers(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """List all remedy trackers for a kundli."""
    rows = db.execute(
        "SELECT * FROM remedy_trackers WHERE user_id = %s AND kundli_id = %s ORDER BY created_at DESC",
        (user["sub"], kundli_id),
    ).fetchall()
    result = []
    for r in rows:
        try:
            check_ins = json.loads(r["check_ins"]) if r["check_ins"] else []
        except Exception:
            check_ins = []
        result.append({
            "id": r["id"],
            "remedy_title": r["remedy_title"],
            "remedy_description": r["remedy_description"],
            "planet": r["planet"],
            "started_at": str(r["started_at"]),
            "target_days": r["target_days"],
            "completed_days": r["completed_days"],
            "check_ins": check_ins,
            "status": r["status"],
            "progress_pct": round(r["completed_days"] / r["target_days"] * 100) if r["target_days"] > 0 else 0,
        })
    return {"trackers": result}


@router.post("/api/lalkitab/remedy-tracker/{kundli_id}")
def create_remedy_tracker(
    kundli_id: str,
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Start a new 43-day remedy tracker."""
    title = payload.get("remedy_title", "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="remedy_title required")
    # Verify kundli ownership
    k = db.execute("SELECT id FROM kundlis WHERE id = %s AND user_id = %s", (kundli_id, user["sub"])).fetchone()
    if not k:
        raise HTTPException(status_code=404, detail="Kundli not found")
    from datetime import date as _date_cls
    started_at = payload.get("started_at") or str(_date_cls.today())
    row = db.execute(
        """INSERT INTO remedy_trackers
           (user_id, kundli_id, remedy_title, remedy_description, planet, started_at, target_days)
           VALUES (%s, %s, %s, %s, %s, %s, %s)
           RETURNING id""",
        (user["sub"], kundli_id, title,
         payload.get("remedy_description", ""),
         payload.get("planet"),
         started_at,
         int(payload.get("target_days", 43))),
    ).fetchone()
    db.commit()
    return {"tracker_id": row["id"], "status": "created"}


@router.post("/api/lalkitab/remedy-tracker/{tracker_id}/checkin")
def checkin_remedy_tracker(
    tracker_id: str,
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Mark today as completed for a tracker.
    If 'missed' is True in payload, status becomes 'broken' and completed_days resets.
    """
    from datetime import date as _date_cls
    today = str(_date_cls.today())
    row = db.execute(
        "SELECT * FROM remedy_trackers WHERE id = %s AND user_id = %s",
        (tracker_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Tracker not found")
    if row["status"] not in ("active", "paused"):
        raise HTTPException(status_code=400, detail=f"Tracker is {row['status']} — cannot check in")
    try:
        check_ins = json.loads(row["check_ins"]) if row["check_ins"] else []
    except Exception:
        check_ins = []
    missed = payload.get("missed", False)
    if missed:
        # Missed day = reset to broken
        db.execute(
            "UPDATE remedy_trackers SET status='broken', completed_days=0, check_ins='[]', updated_at=NOW() WHERE id=%s",
            (tracker_id,),
        )
        db.commit()
        return {"status": "broken", "message": "Remedy chain broken — reset to day 0. Start again with fresh resolve."}
    if today not in check_ins:
        check_ins.append(today)
    completed = len(check_ins)
    new_status = "completed" if completed >= row["target_days"] else "active"
    db.execute(
        "UPDATE remedy_trackers SET completed_days=%s, check_ins=%s, status=%s, updated_at=NOW() WHERE id=%s",
        (completed, json.dumps(check_ins), new_status, tracker_id),
    )
    db.commit()
    return {
        "status": new_status,
        "completed_days": completed,
        "target_days": row["target_days"],
        "progress_pct": round(completed / row["target_days"] * 100),
        "days_remaining": max(0, row["target_days"] - completed),
    }


@router.delete("/api/lalkitab/remedy-tracker/{tracker_id}")
def delete_remedy_tracker(
    tracker_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Delete a remedy tracker."""
    row = db.execute(
        "DELETE FROM remedy_trackers WHERE id=%s AND user_id=%s RETURNING id",
        (tracker_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Tracker not found")
    db.commit()
    return {"status": "deleted"}


# ─────────────────────────────────────────────────────────────
# Lal Kitab Saala Grah — 35-Year Dasha Timeline
# ─────────────────────────────────────────────────────────────
from app.lalkitab_dasha import get_dasha_timeline as _get_dasha_timeline
from datetime import date as _date_today


@router.get("/api/lalkitab/dasha/{kundli_id}")
def get_lk_dasha(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """LK Saala Grah (Year Ruler) Dasha timeline — which planet rules each year of life."""
    row = db.execute(
        "SELECT birth_date FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    result = _get_dasha_timeline(
        birth_date=str(row["birth_date"]),
        current_date=_date_today.today().isoformat(),
    )
    return result


# ─────────────────────────────────────────────────────────────
# Lal Kitab Prediction Feedback (per-kundli, per-area ratings)
# ─────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/predictions/feedback/{kundli_id}")
def get_prediction_feedback(
    kundli_id: str,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return saved prediction feedback ratings for a kundli."""
    row = db.execute(
        "SELECT feedback FROM lk_prediction_feedback WHERE user_id = %s AND kundli_id = %s",
        (user["sub"], kundli_id),
    ).fetchone()
    return {"feedback": json.loads(row["feedback"]) if row else {}}


@router.post("/api/lalkitab/predictions/feedback")
def save_prediction_feedback(
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Upsert prediction feedback ratings. payload: {kundli_id, feedback: {areaKey: rating}}"""
    kundli_id = payload.get("kundli_id")
    feedback = payload.get("feedback", {})
    if not kundli_id:
        raise HTTPException(status_code=400, detail="kundli_id required")

    # Verify kundli ownership
    row = db.execute(
        "SELECT id FROM kundlis WHERE id = %s AND user_id = %s",
        (kundli_id, user["sub"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Kundli not found")

    existing = db.execute(
        "SELECT id FROM lk_prediction_feedback WHERE user_id = %s AND kundli_id = %s",
        (user["sub"], kundli_id),
    ).fetchone()
    if existing:
        db.execute(
            "UPDATE lk_prediction_feedback SET feedback = %s, updated_at = NOW() WHERE user_id = %s AND kundli_id = %s",
            (json.dumps(feedback), user["sub"], kundli_id),
        )
    else:
        db.execute(
            "INSERT INTO lk_prediction_feedback (user_id, kundli_id, feedback) VALUES (%s, %s, %s)",
            (user["sub"], kundli_id, json.dumps(feedback)),
        )
    db.commit()
    return {"ok": True}
