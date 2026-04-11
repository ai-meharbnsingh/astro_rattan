"""KP Astrology and Lal Kitab Remedies routes."""
import json
from datetime import date as _date
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.astro_engine import calculate_planet_positions
from app.database import get_db
from app.kp_engine import calculate_kp_cuspal
from app.lalkitab_engine import get_remedies

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
        result = get_remedies(planet_positions)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Calculation error — please try again",
        )

    return {"remedies_by_planet": result}


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
