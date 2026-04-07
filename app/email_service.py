"""AstroVedic — Email service with graceful degradation.

If SMTP is not configured, emails are logged and skipped (no crash).
"""
import logging
import smtplib
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


def _smtp_configured() -> bool:
    """Return True if all required SMTP settings are present."""
    if TESTING:
        return False
    return bool(SMTP_HOST and SMTP_PORT and SMTP_USER and SMTP_PASSWORD and FROM_EMAIL)


def send_email(to: str, subject: str, body_html: str) -> bool:
    """Send an HTML email via SMTP.

    Returns True on success, False on failure or if SMTP is not configured.
    """
    if not _smtp_configured():
        logger.info("SMTP not configured — skipping email to %s: %s", to, subject)
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{APP_NAME} <{FROM_EMAIL}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body_html, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.ehlo()
            if SMTP_PORT != 25:
                server.starttls()
                server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to, msg.as_string())
        logger.info("Email sent to %s: %s", to, subject)
        return True
    except Exception:
        logger.exception("Failed to send email to %s: %s", to, subject)
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
