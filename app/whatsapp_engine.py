"""WhatsApp Business Cloud API integration for AstroVedic chatbot."""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "astrovedic_verify_2026")
WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"


async def send_text_message(to_phone: str, text: str) -> bool:
    """Send a text message via WhatsApp Business API."""
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        logger.warning("WhatsApp not configured - WHATSAPP_TOKEN or WHATSAPP_PHONE_ID missing")
        return False
    try:
        import httpx
        url = f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": text},
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers, timeout=15)
            resp.raise_for_status()
        return True
    except Exception as e:
        logger.error("WhatsApp send failed: %s", e)
        return False


async def send_template_message(to_phone: str, template_name: str, parameters: list) -> bool:
    """Send a template message via WhatsApp Business API."""
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        return False
    try:
        import httpx
        url = f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        components = []
        if parameters:
            components.append({
                "type": "body",
                "parameters": [{"type": "text", "text": p} for p in parameters],
            })
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "template",
            "template": {"name": template_name, "language": {"code": "en"}, "components": components},
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers, timeout=15)
            resp.raise_for_status()
        return True
    except Exception as e:
        logger.error("WhatsApp template send failed: %s", e)
        return False


async def process_incoming_message(message_text: str, sender_phone: str) -> str:
    """Process incoming WhatsApp message and generate AI response."""
    text_lower = message_text.strip().lower()

    # Keyword routing
    if text_lower in ("kundli", "birth chart"):
        return (
            "To generate your Kundli, please share:\n"
            "1. Date of Birth (DD-MM-YYYY)\n"
            "2. Time of Birth (HH:MM AM/PM)\n"
            "3. Place of Birth\n\n"
            "Or visit our website for instant results!"
        )

    if text_lower in ("horoscope", "rashifal"):
        return (
            "Which zodiac sign?\n\n"
            "1. Aries  2. Taurus  3. Gemini\n"
            "4. Cancer  5. Leo  6. Virgo\n"
            "7. Libra  8. Scorpio  9. Sagittarius\n"
            "10. Capricorn  11. Aquarius  12. Pisces\n\n"
            "Reply with the sign name or number."
        )

    if text_lower in ("panchang", "today"):
        try:
            from app.panchang_engine import calculate_panchang
            from datetime import date
            p = calculate_panchang(date.today().isoformat(), 28.6139, 77.2090)
            return (
                f"Today's Panchang:\n"
                f"Tithi: {p.get('tithi', {}).get('name', 'N/A')}\n"
                f"Nakshatra: {p.get('nakshatra', {}).get('name', 'N/A')}\n"
                f"Yoga: {p.get('yoga', {}).get('name', 'N/A')}\n"
                f"Sunrise: {p.get('sunrise', 'N/A')}\n"
                f"Sunset: {p.get('sunset', 'N/A')}"
            )
        except Exception:
            return "Today's Panchang is available on our website. Visit astrovedic.com/panchang"

    if text_lower in ("hi", "hello", "namaste"):
        return (
            "Namaste! 🙏 Welcome to AstroVedic.\n\n"
            "I can help you with:\n"
            "• Type 'kundli' for birth chart\n"
            "• Type 'horoscope' for daily predictions\n"
            "• Type 'panchang' for today's panchang\n"
            "• Or ask any astrology question!\n\n"
            "How can I help you today?"
        )

    # Forward to AI engine for general questions
    try:
        from app.ai_engine import _call_ai
        response = await _call_ai(
            system="You are AstroVedic AI Astrologer on WhatsApp. Give concise, helpful Vedic astrology answers. Keep responses under 300 words.",
            user=message_text,
        )
        return response or "I appreciate your question. Please visit astrovedic.com for detailed insights."
    except Exception:
        return "Thank you for your question! For detailed astrology insights, visit astrovedic.com"
