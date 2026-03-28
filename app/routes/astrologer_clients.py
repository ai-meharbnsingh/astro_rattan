"""Astrologer Client Management routes — CRUD for astrologer's client roster with auto kundli generation."""
import json
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import require_role
from app.database import get_db
from app.models import AstrologerClientCreate, AstrologerClientUpdate
from app.astro_engine import calculate_planet_positions

router = APIRouter(prefix="/api/astrologer/clients", tags=["astrologer-clients"])


def _require_astrologer(user: dict = Depends(require_role("astrologer", "admin"))):
    """Dependency: require astrologer or admin role, return user dict."""
    return user


# ── POST / — Add a new client ──────────────────────────────────
@router.post("", status_code=status.HTTP_201_CREATED)
def add_client(
    body: AstrologerClientCreate,
    user: dict = Depends(_require_astrologer),
    db: Any = Depends(get_db),
):
    """Add a new client for the logged-in astrologer. Auto-generates kundli if birth details provided."""
    astrologer_user_id = user["sub"]
    kundli_id = None

    # Auto-generate kundli if we have sufficient birth details
    if body.birth_date and body.birth_time and body.latitude is not None and body.longitude is not None:
        chart_data = calculate_planet_positions(
            birth_date=body.birth_date,
            birth_time=body.birth_time,
            latitude=body.latitude,
            longitude=body.longitude,
            tz_offset=body.timezone_offset or 5.5,
        )
        chart_json = json.dumps(chart_data, default=str)

        db.execute(
            """INSERT INTO kundlis
               (user_id, person_name, birth_date, birth_time, birth_place,
                latitude, longitude, timezone_offset, ayanamsa, chart_data)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                astrologer_user_id,
                body.client_name,
                body.birth_date,
                body.birth_time,
                body.birth_place or "",
                body.latitude,
                body.longitude,
                body.timezone_offset or 5.5,
                "lahiri",
                chart_json,
            ),
        )
        db.commit()

        kundli_row = db.execute(
            "SELECT id FROM kundlis WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
            (astrologer_user_id,),
        ).fetchone()
        if kundli_row:
            kundli_id = kundli_row["id"]

    # Insert client record
    db.execute(
        """INSERT INTO astrologer_clients
           (astrologer_user_id, client_name, client_phone, client_email,
            birth_date, birth_time, birth_place, latitude, longitude,
            timezone_offset, gender, notes, kundli_id)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            astrologer_user_id,
            body.client_name,
            body.client_phone,
            body.client_email,
            body.birth_date,
            body.birth_time,
            body.birth_place,
            body.latitude,
            body.longitude,
            body.timezone_offset or 5.5,
            body.gender or "male",
            body.notes,
            kundli_id,
        ),
    )
    db.commit()

    # Fetch the newly created client
    client = db.execute(
        "SELECT * FROM astrologer_clients WHERE astrologer_user_id = %s ORDER BY created_at DESC LIMIT 1",
        (astrologer_user_id,),
    ).fetchone()

    result = dict(client)

    # Attach kundli chart_data if generated
    if kundli_id:
        kundli = db.execute("SELECT chart_data FROM kundlis WHERE id = %s", (kundli_id,)).fetchone()
        if kundli:
            result["chart_data"] = json.loads(kundli["chart_data"])

    return result


# ── GET / — List all clients ────────────────────────────────────
@router.get("", status_code=status.HTTP_200_OK)
def list_clients(
    search: Optional[str] = Query(default=None, description="Search by client name or phone"),
    user: dict = Depends(_require_astrologer),
    db: Any = Depends(get_db),
):
    """List all clients for the logged-in astrologer with optional search."""
    astrologer_user_id = user["sub"]

    if search:
        pattern = f"%{search}%"
        rows = db.execute(
            """SELECT id, client_name, client_phone, client_email, birth_date, birth_place, created_at
               FROM astrologer_clients
               WHERE astrologer_user_id = %s
                 AND (client_name ILIKE %s OR COALESCE(client_phone, '') ILIKE %s)
               ORDER BY created_at DESC""",
            (astrologer_user_id, pattern, pattern),
        ).fetchall()
    else:
        rows = db.execute(
            """SELECT id, client_name, client_phone, client_email, birth_date, birth_place, created_at
               FROM astrologer_clients
               WHERE astrologer_user_id = %s
               ORDER BY created_at DESC""",
            (astrologer_user_id,),
        ).fetchall()

    return [dict(r) for r in rows]


# ── GET /{client_id} — Full client details ──────────────────────
@router.get("/{client_id}", status_code=status.HTTP_200_OK)
def get_client(
    client_id: str,
    user: dict = Depends(_require_astrologer),
    db: Any = Depends(get_db),
):
    """Get full client details including kundli chart data."""
    astrologer_user_id = user["sub"]

    client = db.execute(
        "SELECT * FROM astrologer_clients WHERE id = %s AND astrologer_user_id = %s",
        (client_id, astrologer_user_id),
    ).fetchone()

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    result = dict(client)

    # Attach kundli chart_data if linked
    if client["kundli_id"]:
        kundli = db.execute(
            "SELECT chart_data, ayanamsa, iogita_analysis FROM kundlis WHERE id = %s",
            (client["kundli_id"],),
        ).fetchone()
        if kundli:
            result["chart_data"] = json.loads(kundli["chart_data"])
            result["ayanamsa"] = kundli["ayanamsa"]
            if kundli["iogita_analysis"]:
                result["iogita_analysis"] = json.loads(kundli["iogita_analysis"])

    return result


# ── PUT /{client_id} — Update client ────────────────────────────
@router.put("/{client_id}", status_code=status.HTTP_200_OK)
def update_client(
    client_id: str,
    body: AstrologerClientUpdate,
    user: dict = Depends(_require_astrologer),
    db: Any = Depends(get_db),
):
    """Update client details. Regenerates kundli if birth details change."""
    astrologer_user_id = user["sub"]

    existing = db.execute(
        "SELECT * FROM astrologer_clients WHERE id = %s AND astrologer_user_id = %s",
        (client_id, astrologer_user_id),
    ).fetchone()

    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    updates = []
    params = []

    field_map = {
        "client_name": body.client_name,
        "client_phone": body.client_phone,
        "client_email": body.client_email,
        "birth_date": body.birth_date,
        "birth_time": body.birth_time,
        "birth_place": body.birth_place,
        "latitude": body.latitude,
        "longitude": body.longitude,
        "timezone_offset": body.timezone_offset,
        "gender": body.gender,
        "notes": body.notes,
    }

    for col, val in field_map.items():
        if val is not None:
            updates.append(f"{col} = %s")
            params.append(val)

    # Check if birth details changed — if so, regenerate kundli
    birth_changed = any(
        getattr(body, f) is not None
        for f in ("birth_date", "birth_time", "latitude", "longitude")
    )

    if birth_changed:
        new_date = body.birth_date or existing["birth_date"]
        new_time = body.birth_time or existing["birth_time"]
        new_lat = body.latitude if body.latitude is not None else existing["latitude"]
        new_lon = body.longitude if body.longitude is not None else existing["longitude"]
        new_tz = body.timezone_offset if body.timezone_offset is not None else (existing["timezone_offset"] or 5.5)
        new_place = body.birth_place or existing["birth_place"] or ""
        new_name = body.client_name or existing["client_name"]

        if new_date and new_time and new_lat is not None and new_lon is not None:
            chart_data = calculate_planet_positions(
                birth_date=new_date,
                birth_time=new_time,
                latitude=new_lat,
                longitude=new_lon,
                tz_offset=new_tz,
            )
            chart_json = json.dumps(chart_data, default=str)

            db.execute(
                """INSERT INTO kundlis
                   (user_id, person_name, birth_date, birth_time, birth_place,
                    latitude, longitude, timezone_offset, ayanamsa, chart_data)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (astrologer_user_id, new_name, new_date, new_time, new_place,
                 new_lat, new_lon, new_tz, "lahiri", chart_json),
            )
            db.commit()

            kundli_row = db.execute(
                "SELECT id FROM kundlis WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                (astrologer_user_id,),
            ).fetchone()
            if kundli_row:
                updates.append("kundli_id = %s")
                params.append(kundli_row["id"])

    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    updates.append("updated_at = to_char(NOW(), 'YYYY-MM-DD\"T\"HH24:MI:SS')")
    params.extend([client_id, astrologer_user_id])

    db.execute(
        f"UPDATE astrologer_clients SET {', '.join(updates)} WHERE id = %s AND astrologer_user_id = %s",
        params,
    )
    db.commit()

    updated = db.execute(
        "SELECT * FROM astrologer_clients WHERE id = %s AND astrologer_user_id = %s",
        (client_id, astrologer_user_id),
    ).fetchone()

    return dict(updated)


# ── DELETE /{client_id} — Remove client ─────────────────────────
@router.delete("/{client_id}", status_code=status.HTTP_200_OK)
def delete_client(
    client_id: str,
    user: dict = Depends(_require_astrologer),
    db: Any = Depends(get_db),
):
    """Remove client from astrologer's roster (kundli data is kept)."""
    astrologer_user_id = user["sub"]

    existing = db.execute(
        "SELECT id FROM astrologer_clients WHERE id = %s AND astrologer_user_id = %s",
        (client_id, astrologer_user_id),
    ).fetchone()

    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    db.execute(
        "DELETE FROM astrologer_clients WHERE id = %s AND astrologer_user_id = %s",
        (client_id, astrologer_user_id),
    )
    db.commit()

    return {"message": "Client removed", "id": client_id}


# ── GET /{client_id}/kundli — Full kundli data ─────────────────
@router.get("/{client_id}/kundli", status_code=status.HTTP_200_OK)
def get_client_kundli(
    client_id: str,
    user: dict = Depends(_require_astrologer),
    db: Any = Depends(get_db),
):
    """Get the full kundli data for a client."""
    astrologer_user_id = user["sub"]

    client = db.execute(
        "SELECT * FROM astrologer_clients WHERE id = %s AND astrologer_user_id = %s",
        (client_id, astrologer_user_id),
    ).fetchone()

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    if not client["kundli_id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No kundli generated for this client. Update their birth details to generate one.",
        )

    kundli = db.execute(
        "SELECT * FROM kundlis WHERE id = %s",
        (client["kundli_id"],),
    ).fetchone()

    if not kundli:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kundli not found")

    return {
        "id": kundli["id"],
        "person_name": kundli["person_name"],
        "birth_date": kundli["birth_date"],
        "birth_time": kundli["birth_time"],
        "birth_place": kundli["birth_place"],
        "latitude": kundli["latitude"],
        "longitude": kundli["longitude"],
        "timezone_offset": kundli["timezone_offset"],
        "ayanamsa": kundli["ayanamsa"],
        "chart_data": json.loads(kundli["chart_data"]),
        "iogita_analysis": json.loads(kundli["iogita_analysis"]) if kundli["iogita_analysis"] else None,
        "created_at": kundli["created_at"],
    }
