"""WhatsApp Business API webhook routes."""
import logging
from fastapi import APIRouter, Request, Query, Depends
from fastapi.responses import PlainTextResponse
from app.whatsapp_engine import (
    WHATSAPP_VERIFY_TOKEN,
    send_text_message,
    process_incoming_message,
)
from app.auth import require_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """Meta webhook verification endpoint."""
    if hub_mode == "subscribe" and hub_verify_token == WHATSAPP_VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge or "")
    return PlainTextResponse(content="Forbidden", status_code=403)


@router.post("/webhook")
async def receive_message(request: Request):
    """Receive incoming WhatsApp messages."""
    try:
        body = await request.json()
        entries = body.get("entry", [])
        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    if msg.get("type") == "text":
                        sender = msg["from"]
                        text = msg["text"]["body"]
                        logger.info("WhatsApp message from %s: %s", sender, text[:100])
                        response = await process_incoming_message(text, sender)
                        await send_text_message(sender, response)
    except Exception as e:
        logger.error("WhatsApp webhook error: %s", e)
    return {"status": "ok"}


@router.post("/send")
async def admin_send_message(
    request: Request,
    _user=Depends(require_role("admin")),
):
    """Admin endpoint to send a WhatsApp message."""
    body = await request.json()
    phone = body.get("phone", "")
    message = body.get("message", "")
    if not phone or not message:
        return {"error": "phone and message required"}, 400
    success = await send_text_message(phone, message)
    return {"success": success}
