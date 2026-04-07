"""AstroVedic — Email service with graceful degradation.

Supports two transports:
1. Resend HTTP API (works on Vercel serverless — SMTP is blocked there)
2. SMTP (works on Render, Railway, local dev)

If neither is configured, emails are logged and skipped (no crash).
"""
import json
import logging
import smtplib
import urllib.request
import urllib.error
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    FROM_EMAIL,
    EMAIL_TO,
    APP_NAME,
    FRONTEND_URL,
    TESTING,
)

logger = logging.getLogger(__name__)

# Resend API key (HTTP email — works on Vercel)
import os
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")


def _smtp_configured() -> bool:
    """Return True if all required SMTP settings are present."""
    if TESTING:
        return False
    return bool(SMTP_HOST and SMTP_PORT and SMTP_USER and SMTP_PASSWORD and FROM_EMAIL)


def _send_via_resend(to: str, subject: str, body_html: str) -> bool:
    """Send email via Resend HTTP API (no SMTP needed)."""
    if not RESEND_API_KEY:
        return False
    from_addr = FROM_EMAIL if FROM_EMAIL else "AstroVedic <onboarding@resend.dev>"
    payload = json.dumps({
        "from": f"{APP_NAME} <{from_addr}>",
        "to": [to],
        "subject": subject,
        "html": body_html,
    }).encode()
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            logger.info("Email sent via Resend to %s: %s (id=%s)", to, subject, result.get("id"))
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        logger.error("Resend API error %d for %s: %s", e.code, to, body)
        return False
    except Exception as e:
        logger.error("Resend failed for %s: %s", to, e)
        return False


def _send_via_smtp(to: str, subject: str, body_html: str) -> bool:
    """Send email via SMTP (works on non-Vercel platforms)."""
    if not _smtp_configured():
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{APP_NAME} <{FROM_EMAIL}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body_html, "html"))

    methods = [
        ("STARTTLS", SMTP_PORT, False),
        ("SSL", 465, True),
    ]
    for method_name, port, use_ssl in methods:
        try:
            if use_ssl:
                server = smtplib.SMTP_SSL(SMTP_HOST, port, timeout=15)
            else:
                server = smtplib.SMTP(SMTP_HOST, port, timeout=15)
                server.ehlo()
                server.starttls()
                server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to, msg.as_string())
            server.quit()
            logger.info("Email sent via SMTP %s to %s: %s", method_name, to, subject)
            return True
        except Exception as e:
            logger.warning("SMTP %s (port %d) failed for %s: %s", method_name, port, to, e)
            continue
    return False


def send_email(to: str, subject: str, body_html: str) -> bool:
    """Send an HTML email. Tries Resend (HTTP) first, then SMTP fallback."""
    if TESTING:
        logger.info("TESTING mode — skipping email to %s: %s", to, subject)
        return False

    # Try Resend first (works on Vercel)
    if RESEND_API_KEY:
        if _send_via_resend(to, subject, body_html):
            return True

    # Fall back to SMTP (works on Render, Railway, local)
    if _smtp_configured():
        if _send_via_smtp(to, subject, body_html):
            return True

    logger.error("No email transport available for %s: %s", to, subject)
    return False


def send_order_confirmation(order: dict, user_email: str) -> bool:
    """Send an order confirmation email."""
    order_id = order.get("id", "N/A")
    total = order.get("total", "0.00")
    items_html = ""
    for item in order.get("items", []):
        items_html += f"<li>{item.get('name', 'Item')} — Rs. {item.get('price', '0')}</li>"
    if not items_html:
        items_html = "<li>See your account for order details</li>"

    body = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #6366F1;">Order Confirmed</h1>
        <p>Thank you for your order with {APP_NAME}!</p>
        <p><strong>Order ID:</strong> {order_id}</p>
        <h3>Items:</h3>
        <ul>{items_html}</ul>
        <p><strong>Total:</strong> Rs. {total}</p>
        <hr style="border: 1px solid #E2E8F0; margin: 20px 0;">
        <p style="color: #64748B; font-size: 12px;">
            This is an automated message from {APP_NAME}. Please do not reply.
        </p>
    </div>
    """
    return send_email(user_email, f"{APP_NAME} — Order #{order_id} Confirmed", body)


def send_order_alert(order: dict, user_email: str) -> bool:
    """Send an internal order alert to the configured operations inbox."""
    if not EMAIL_TO:
        logger.info("EMAIL_TO not configured — skipping order alert for order %s", order.get("id", "N/A"))
        return False

    body = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #6366F1;">New Order Received</h1>
        <p><strong>Order ID:</strong> {order.get("id", "N/A")}</p>
        <p><strong>Customer Email:</strong> {user_email}</p>
        <p><strong>Total:</strong> Rs. {order.get("total", "0.00")}</p>
        <p><strong>Payment Method:</strong> {order.get("payment_method", "N/A")}</p>
        <p><strong>Shipping Address:</strong> {order.get("shipping_address", "N/A")}</p>
    </div>
    """
    return send_email(EMAIL_TO, f"{APP_NAME} — New Order {order.get('id', 'N/A')}", body)


def send_verification_otp(user_email: str, otp: str) -> bool:
    """Send email verification OTP."""
    body = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #6366F1;">Verify Your Email</h1>
        <p>Use the following code to verify your email address for {APP_NAME}:</p>
        <div style="background: #F1F5F9; padding: 20px; border-radius: 8px;
                    font-family: monospace; font-size: 32px; text-align: center;
                    letter-spacing: 8px; margin: 20px 0; font-weight: bold; color: #1E293B;">
            {otp}
        </div>
        <p>This code expires in <strong>10 minutes</strong>.</p>
        <p style="color: #64748B;">If you did not request this, please ignore this email.</p>
        <hr style="border: 1px solid #E2E8F0; margin: 20px 0;">
        <p style="color: #64748B; font-size: 12px;">
            This is an automated message from {APP_NAME}. Please do not reply.
        </p>
    </div>
    """
    return send_email(user_email, f"{APP_NAME} — Email Verification Code", body)


def send_registration_welcome(user_name: str, user_email: str) -> bool:
    """Send a welcome email after registration."""
    body = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #6366F1;">Welcome to {APP_NAME}!</h1>
        <p>Namaste {user_name},</p>
        <p>Your account has been created successfully. Explore the ancient wisdom of
        Vedic astrology with our comprehensive tools:</p>
        <ul>
            <li>Birth Chart (Kundli) generation</li>
            <li>Daily horoscope and Panchang</li>
            <li>AI-powered astrological guidance</li>
            <li>Numerology, Tarot, and more</li>
        </ul>
        <p>Begin your cosmic journey today!</p>
        <hr style="border: 1px solid #E2E8F0; margin: 20px 0;">
        <p style="color: #64748B; font-size: 12px;">
            This is an automated message from {APP_NAME}. Please do not reply.
        </p>
    </div>
    """
    return send_email(user_email, f"Welcome to {APP_NAME}", body)


def send_password_reset(user_email: str, reset_token: str) -> bool:
    """Send a password reset email with a token link."""
    body = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #6366F1;">Password Reset</h1>
        <p>We received a request to reset your {APP_NAME} password.</p>
        <p>Use the following token to reset your password:</p>
        <div style="background: #F1F5F9; padding: 15px; border-radius: 8px;
                    font-family: monospace; font-size: 18px; text-align: center;
                    letter-spacing: 2px; margin: 20px 0;">
            {reset_token}
        </div>
        <p>This token expires in 1 hour. If you did not request a password reset,
        please ignore this email.</p>
        <hr style="border: 1px solid #E2E8F0; margin: 20px 0;">
        <p style="color: #64748B; font-size: 12px;">
            This is an automated message from {APP_NAME}. Please do not reply.
        </p>
    </div>
    """
    return send_email(user_email, f"{APP_NAME} — Password Reset", body)


def send_report_ready(report: dict, user_email: str) -> bool:
    """Send a report-ready email with the PDF link."""
    report_id = report.get("id", "N/A")
    report_type = str(report.get("report_type", "report")).replace("_", " ").title()
    pdf_url = report.get("pdf_url", "")
    report_link = f"{FRONTEND_URL}{pdf_url}" if pdf_url else FRONTEND_URL

    body = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #6366F1;">Your Report Is Ready</h1>
        <p>Your {report_type} report has been generated successfully.</p>
        <p><strong>Report ID:</strong> {report_id}</p>
        <p><a href="{report_link}" style="color: #6366F1;">Open your report</a></p>
        <hr style="border: 1px solid #E2E8F0; margin: 20px 0;">
        <p style="color: #64748B; font-size: 12px;">
            This is an automated message from {APP_NAME}. Please do not reply.
        </p>
    </div>
    """
    return send_email(user_email, f"{APP_NAME} — {report_type} Ready", body)
