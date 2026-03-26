"""Tests for consultation booking, listing, accept/complete, and WebSocket."""
import pytest
from tests.conftest import (
    _register_user, _auth_header, _make_astrologer, _make_admin,
)


# ---- Fixtures ---- #

@pytest.fixture(scope="module")
def setup_consultation(client, db):
    """Register a regular user and an astrologer, return useful ids + tokens."""
    # Regular user
    user, user_token = _register_user(client, "consult_user@test.com", name="Consult User")
    user_id = user["id"]

    # Astrologer user
    astro_user, _ = _register_user(client, "consult_astro@test.com", name="Astro Consult")
    astrologer_id, astro_token = _make_astrologer(db, astro_user["id"], "Astro Consult")

    return {
        "user_id": user_id,
        "user_token": user_token,
        "astrologer_id": astrologer_id,
        "astro_user_id": astro_user["id"],
        "astro_token": astro_token,
    }


# ---- Tests ---- #

def test_list_astrologers_200(client, setup_consultation):
    """GET /api/astrologers returns 200."""
    resp = client.get("/api/astrologers")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_book_consultation_201(client, setup_consultation):
    """POST /api/consultations/book returns 201 with valid astrologer."""
    s = setup_consultation
    resp = client.post(
        "/api/consultations/book",
        json={"astrologer_id": s["astrologer_id"], "type": "chat"},
        headers=_auth_header(s["user_token"]),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["astrologer_id"] == s["astrologer_id"]
    assert data["status"] == "requested"
    assert data["type"] == "chat"


def test_book_consultation_no_auth_401(client, setup_consultation):
    """POST /api/consultations/book without auth returns 401."""
    s = setup_consultation
    resp = client.post(
        "/api/consultations/book",
        json={"astrologer_id": s["astrologer_id"], "type": "chat"},
    )
    assert resp.status_code == 401


def test_list_consultations_200(client, setup_consultation):
    """GET /api/consultations returns 200 with a list."""
    s = setup_consultation
    resp = client.get("/api/consultations", headers=_auth_header(s["user_token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_accept_consultation_200(client, db, setup_consultation):
    """PATCH /api/consultations/{id}/accept as astrologer returns 200."""
    s = setup_consultation
    # Book a new consultation first
    book_resp = client.post(
        "/api/consultations/book",
        json={"astrologer_id": s["astrologer_id"], "type": "call"},
        headers=_auth_header(s["user_token"]),
    )
    assert book_resp.status_code == 201
    cid = book_resp.json()["id"]

    # Accept as astrologer
    resp = client.patch(
        f"/api/consultations/{cid}/accept",
        headers=_auth_header(s["astro_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "accepted"


def test_complete_consultation_200(client, db, setup_consultation):
    """PATCH /api/consultations/{id}/complete after accepting returns 200."""
    s = setup_consultation
    # Book
    book_resp = client.post(
        "/api/consultations/book",
        json={"astrologer_id": s["astrologer_id"], "type": "video"},
        headers=_auth_header(s["user_token"]),
    )
    cid = book_resp.json()["id"]

    # Accept
    client.patch(f"/api/consultations/{cid}/accept", headers=_auth_header(s["astro_token"]))

    # Complete
    resp = client.patch(
        f"/api/consultations/{cid}/complete",
        headers=_auth_header(s["astro_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"


def test_book_nonexistent_astrologer_404(client, setup_consultation):
    """Booking with a fake astrologer id returns 404."""
    s = setup_consultation
    resp = client.post(
        "/api/consultations/book",
        json={"astrologer_id": "nonexistent_id_000", "type": "chat"},
        headers=_auth_header(s["user_token"]),
    )
    assert resp.status_code == 404


def test_complete_already_completed_400(client, db, setup_consultation):
    """Cannot complete a consultation that is already completed — returns 400."""
    s = setup_consultation
    # Book + accept + complete
    book_resp = client.post(
        "/api/consultations/book",
        json={"astrologer_id": s["astrologer_id"], "type": "chat"},
        headers=_auth_header(s["user_token"]),
    )
    cid = book_resp.json()["id"]
    client.patch(f"/api/consultations/{cid}/accept", headers=_auth_header(s["astro_token"]))
    client.patch(f"/api/consultations/{cid}/complete", headers=_auth_header(s["astro_token"]))

    # Try completing again
    resp = client.patch(
        f"/api/consultations/{cid}/complete",
        headers=_auth_header(s["astro_token"]),
    )
    assert resp.status_code == 400


def test_generate_video_link_activates_video_consultation(client, db, setup_consultation):
    """Participants can generate and reuse a Jitsi link for accepted video consultations."""
    s = setup_consultation
    book_resp = client.post(
        "/api/consultations/book",
        json={"astrologer_id": s["astrologer_id"], "type": "video"},
        headers=_auth_header(s["user_token"]),
    )
    cid = book_resp.json()["id"]
    client.patch(f"/api/consultations/{cid}/accept", headers=_auth_header(s["astro_token"]))

    resp = client.post(
        f"/api/consultations/{cid}/video-link",
        headers=_auth_header(s["user_token"]),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["video_link"].startswith("https://meet.jit.si/AstroVedic-")
    assert data["room_name"].startswith("AstroVedic-")
    assert data["status"] == "active"

    row = db.execute("SELECT status, notes FROM consultations WHERE id = ?", (cid,)).fetchone()
    assert row["status"] == "active"
    assert row["notes"] == data["video_link"]

    second_resp = client.post(
        f"/api/consultations/{cid}/video-link",
        headers=_auth_header(s["astro_token"]),
    )
    assert second_resp.status_code == 200
    assert second_resp.json()["video_link"] == data["video_link"]


def test_generate_video_link_rejects_non_video_consultation(client, setup_consultation):
    """Chat and call consultations cannot open the Jitsi video room endpoint."""
    s = setup_consultation
    book_resp = client.post(
        "/api/consultations/book",
        json={"astrologer_id": s["astrologer_id"], "type": "chat"},
        headers=_auth_header(s["user_token"]),
    )
    cid = book_resp.json()["id"]
    client.patch(f"/api/consultations/{cid}/accept", headers=_auth_header(s["astro_token"]))

    resp = client.post(
        f"/api/consultations/{cid}/video-link",
        headers=_auth_header(s["user_token"]),
    )
    assert resp.status_code == 400


def test_generate_video_link_rejects_non_participant(client, setup_consultation):
    """Only the client or assigned astrologer can access the consultation video room."""
    s = setup_consultation
    outsider, outsider_token = _register_user(client, "consult_outsider@test.com", name="Outsider")
    assert outsider["email"] == "consult_outsider@test.com"

    book_resp = client.post(
        "/api/consultations/book",
        json={"astrologer_id": s["astrologer_id"], "type": "video"},
        headers=_auth_header(s["user_token"]),
    )
    cid = book_resp.json()["id"]
    client.patch(f"/api/consultations/{cid}/accept", headers=_auth_header(s["astro_token"]))

    resp = client.post(
        f"/api/consultations/{cid}/video-link",
        headers=_auth_header(outsider_token),
    )
    assert resp.status_code == 403


def test_websocket_connect_basic(client, db, setup_consultation):
    """WebSocket /ws/consultation/{id} connects with valid token for accepted consultation."""
    s = setup_consultation
    # Book + accept (to get to 'accepted' state)
    book_resp = client.post(
        "/api/consultations/book",
        json={"astrologer_id": s["astrologer_id"], "type": "chat"},
        headers=_auth_header(s["user_token"]),
    )
    cid = book_resp.json()["id"]
    client.patch(f"/api/consultations/{cid}/accept", headers=_auth_header(s["astro_token"]))

    # Connect via WebSocket as the user
    with client.websocket_connect(f"/ws/consultation/{cid}?token={s['user_token']}") as ws:
        # If we get here, the connection was accepted
        ws.send_json({"content": "Hello astrologer", "type": "text"})
        data = ws.receive_json()
        assert data["content"] == "Hello astrologer"
        assert data["sender_id"] == s["user_id"]


def test_websocket_disconnect_invalid_token(client, setup_consultation):
    """WebSocket with invalid token is closed — CHAOS #10 disconnect handling."""
    s = setup_consultation
    # Book + accept
    book_resp = client.post(
        "/api/consultations/book",
        json={"astrologer_id": s["astrologer_id"], "type": "chat"},
        headers=_auth_header(s["user_token"]),
    )
    cid = book_resp.json()["id"]
    client.patch(f"/api/consultations/{cid}/accept", headers=_auth_header(s["astro_token"]))

    # Try connecting with bad token — should raise or close
    try:
        with client.websocket_connect(f"/ws/consultation/{cid}?token=bad.token.here") as ws:
            # Should not reach here — the server closes immediately
            ws.receive_json()
            pytest.fail("Expected WebSocket to be closed due to invalid token")
    except Exception:
        # Connection rejected or closed — this is the expected path
        pass
