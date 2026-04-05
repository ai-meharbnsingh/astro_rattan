"""WebSocket and REST routes for consultation chat messages."""
import json
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query, status
from app.auth import decode_token, get_current_user
from app.database import get_db

router = APIRouter()

# In-memory map: consultation_id -> set of connected WebSockets
_active_connections: dict[str, set[WebSocket]] = {}


# ---------------------------------------------------------------------------
# REST endpoint — GET /api/messages/{consultation_id}
# ---------------------------------------------------------------------------

@router.get("/api/messages/{consultation_id}", status_code=status.HTTP_200_OK)
def get_messages(
    consultation_id: str,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Return message history for a consultation (REST alternative to WebSocket).

    The caller must be either the consultation client or the astrologer.
    """
    user_id = current_user["sub"]

    # Verify the consultation exists and the user is a participant
    consultation = db.execute(
        """
        SELECT c.id, c.user_id, a.user_id as astrologer_user_id
        FROM consultations c
        JOIN astrologers a ON a.id = c.astrologer_id
        WHERE c.id = %s
        """,
        (consultation_id,),
    ).fetchone()

    if consultation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Consultation not found"
        )

    if user_id not in (consultation["user_id"], consultation["astrologer_user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not a participant in this consultation"
        )

    offset = (page - 1) * limit

    total = db.execute(
        "SELECT COUNT(*) as cnt FROM messages WHERE consultation_id = %s",
        (consultation_id,),
    ).fetchone()["cnt"]

    rows = db.execute(
        """SELECT m.id, m.consultation_id, m.sender_id, m.content, m.message_type, m.created_at,
                  u.name as sender_name
           FROM messages m
           JOIN users u ON u.id = m.sender_id
           WHERE m.consultation_id = %s
           ORDER BY m.created_at ASC
           LIMIT %s OFFSET %s""",
        (consultation_id, limit, offset),
    ).fetchall()

    return {
        "consultation_id": consultation_id,
        "messages": [
            {
                "id": r["id"],
                "sender_id": r["sender_id"],
                "sender_name": r["sender_name"],
                "content": r["content"],
                "type": r["message_type"],
                "created_at": r["created_at"],
            }
            for r in rows
        ],
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.websocket("/ws/consultation/{consultation_id}")
async def consultation_ws(
    websocket: WebSocket,
    consultation_id: str,
    token: str = Query(None),
):
    """
    WebSocket endpoint for real-time consultation messages.
    Auth via JWT token in query param: /ws/consultation/{id}%stoken=<jwt>
    """
    # Authenticate via query param
    if not token:
        await websocket.close(code=4001, reason="Missing token")
        return

    payload = decode_token(token)
    if payload is None:
        await websocket.close(code=4001, reason="Invalid token")
        return

    user_id = payload.get("sub")
    user_name = payload.get("name", "User")

    # Verify the consultation exists and user is a participant
    db_gen = get_db()
    db = next(db_gen)
    try:
        consultation = db.execute(
            """
            SELECT c.id, c.user_id, c.astrologer_id, c.status,
                   a.user_id as astrologer_user_id
            FROM consultations c
            JOIN astrologers a ON a.id = c.astrologer_id
            WHERE c.id = %s
            """,
            (consultation_id,),
        ).fetchone()

        if consultation is None:
            await websocket.close(code=4004, reason="Consultation not found")
            return

        # Check user is either the client or the astrologer
        if user_id not in (consultation["user_id"], consultation["astrologer_user_id"]):
            await websocket.close(code=4003, reason="Not a participant")
            return

        if consultation["status"] not in ("accepted", "active"):
            await websocket.close(
                code=4002,
                reason=f"Consultation is in '{consultation['status']}' state",
            )
            return

        # Mark as active if currently accepted
        if consultation["status"] == "accepted":
            db.execute(
                "UPDATE consultations SET status = 'active', started_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id = %s",
                (consultation_id,),
            )
            db.commit()

    finally:
        try:
            next(db_gen, None)
        except StopIteration:
            pass

    # Accept connection
    await websocket.accept()

    # Register connection
    if consultation_id not in _active_connections:
        _active_connections[consultation_id] = set()
    _active_connections[consultation_id].add(websocket)

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON"})
                continue

            content = data.get("content", "").strip()
            message_type = data.get("type", "text")

            if not content:
                await websocket.send_json({"error": "Empty message"})
                continue

            # Persist message
            db_gen2 = get_db()
            db2 = next(db_gen2)
            try:
                cursor = db2.execute(
                    """
                    INSERT INTO messages (consultation_id, sender_id, content, message_type)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, created_at
                    """,
                    (consultation_id, user_id, content, message_type),
                )
                msg_row = cursor.fetchone()
                db2.commit()

                outgoing = {
                    "id": msg_row["id"],
                    "consultation_id": consultation_id,
                    "sender_id": user_id,
                    "sender_name": user_name,
                    "content": content,
                    "type": message_type,
                    "created_at": msg_row["created_at"],
                }
            finally:
                try:
                    next(db_gen2, None)
                except StopIteration:
                    pass

            # Broadcast to all connected clients for this consultation
            dead = set()
            for conn in _active_connections.get(consultation_id, set()):
                try:
                    await conn.send_json(outgoing)
                except Exception:
                    dead.add(conn)

            # Clean up dead connections
            if dead and consultation_id in _active_connections:
                _active_connections[consultation_id] -= dead

    except WebSocketDisconnect:
        pass
    finally:
        if consultation_id in _active_connections:
            _active_connections[consultation_id].discard(websocket)
            if not _active_connections[consultation_id]:
                del _active_connections[consultation_id]
