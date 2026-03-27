"""WebSocket route for consultation chat messages."""
import json
from typing import Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.auth import decode_token
from app.database import get_db

router = APIRouter()

# In-memory map: consultation_id -> set of connected WebSockets
_active_connections: dict[str, set[WebSocket]] = {}


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
