"""Payment initiation and webhook routes.

Supports 3 payment methods:
- COD: No payment gateway. Order marked as placed, payment collected on delivery.
- Razorpay: Creates Razorpay order via API. Frontend uses razorpay.js checkout.
- Stripe: Creates Stripe checkout session. Frontend redirects to Stripe hosted page.
"""
import hashlib
import hmac
import json
import os
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.auth import get_current_user
from app.config import (
    DB_PATH as _DEFAULT_DB_PATH,
    RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET,
    STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET,
    FRONTEND_URL,
)
from app.database import get_db
from app.models import PaymentInitiateRequest, ReportPaymentInitiateRequest
from app.config import DB_PATH as _DEFAULT_DB_PATH


def _get_webhook_db():
    """Create a psycopg2 connection for async webhook handlers.

    Webhook endpoints are async (need await request.body()), so they run
    in the event loop thread. This helper creates a direct psycopg2 connection
    wrapped in PgConnection for sqlite3-like API compatibility.
    """
    from app.database import DATABASE_URL, PgConnection
    import psycopg2
    raw = psycopg2.connect(DATABASE_URL)
    raw.autocommit = False
    return PgConnection(raw)

router = APIRouter()


@router.post("/api/payments/initiate")
def initiate_payment(
    req: PaymentInitiateRequest,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Initiate a payment for an order. Creates a pending payment record.
    Returns payment details for the client to complete with the provider.
    """
    user_id = user.get("sub")

    # Verify order exists and belongs to user
    order = db.execute(
        "SELECT id, total, payment_status FROM orders WHERE id = %s AND user_id = %s",
        (req.order_id, user_id),
    ).fetchone()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    if order["payment_status"] == "paid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Order is already paid"
        )

    # Check for existing pending payment (idempotent)
    existing = db.execute(
        "SELECT id FROM payments WHERE order_id = %s AND provider = %s AND status = 'pending'",
        (req.order_id, req.provider.value),
    ).fetchone()

    if existing:
        return {
            "payment_id": existing["id"],
            "order_id": req.order_id,
            "amount": order["total"],
            "provider": req.provider.value,
        }

    amount = order["total"]
    provider = req.provider.value
    provider_payment_id = None
    payment_url = None
    razorpay_key_id = None

    # --- COD: no gateway needed ---
    if provider == "cod":
        pass  # Just create record, no external call

    # --- RAZORPAY: Create Razorpay Order ---
    elif provider == "razorpay":
        if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
            try:
                import razorpay
                client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
                rz_order = client.order.create({
                    "amount": int(amount * 100),  # Razorpay uses paise
                    "currency": "INR",
                    "receipt": req.order_id,
                })
                provider_payment_id = rz_order["id"]
                razorpay_key_id = RAZORPAY_KEY_ID
            except Exception as e:
                # Razorpay API unavailable — create record anyway for manual processing
                provider_payment_id = f"rz_pending_{req.order_id}"
        else:
            provider_payment_id = f"rz_test_{req.order_id}"  # Test mode

    # --- STRIPE: Create Checkout Session ---
    elif provider == "stripe":
        if STRIPE_SECRET_KEY:
            try:
                import stripe
                stripe.api_key = STRIPE_SECRET_KEY
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[{
                        "price_data": {
                            "currency": "inr",
                            "product_data": {"name": f"AstroVedic Order {req.order_id}"},
                            "unit_amount": int(amount * 100),
                        },
                        "quantity": 1,
                    }],
                    mode="payment",
                    success_url=f"{FRONTEND_URL}/orders/{req.order_id}%spayment=success",
                    cancel_url=f"{FRONTEND_URL}/orders/{req.order_id}%spayment=cancelled",
                    metadata={"order_id": req.order_id},
                )
                provider_payment_id = session.id
                payment_url = session.url
            except Exception as e:
                provider_payment_id = f"stripe_pending_{req.order_id}"
        else:
            provider_payment_id = f"stripe_test_{req.order_id}"  # Test mode

    # Create payment record
    cursor = db.execute(
        """INSERT INTO payments (order_id, provider, provider_payment_id, amount, currency, status)
           VALUES (%s, %s, %s, %s, 'INR', 'pending')
           RETURNING id""",
        (req.order_id, provider, provider_payment_id, amount),
    )
    payment_id = cursor.fetchone()["id"]
    db.commit()

    result = {
        "payment_id": payment_id,
        "order_id": req.order_id,
        "amount": amount,
        "currency": "INR",
        "provider": provider,
        "provider_payment_id": provider_payment_id,
    }
    if payment_url:
        result["payment_url"] = payment_url  # Stripe checkout URL
    if razorpay_key_id:
        result["razorpay_key_id"] = razorpay_key_id  # Frontend needs this for razorpay.js

    return result


@router.post("/api/payments/report/initiate")
def initiate_report_payment(
    req: ReportPaymentInitiateRequest,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """
    Initiate a payment for a report. Creates a pending payment record.
    Returns payment details for the client to complete with the provider.
    """
    user_id = user.get("sub")

    # Verify report exists and belongs to user
    report = db.execute(
        "SELECT id, price, status FROM reports WHERE id = %s AND user_id = %s",
        (req.report_id, user_id),
    ).fetchone()

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    if report["status"] in ("ready", "paid"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Report is already paid and ready"
        )

    # Check for existing pending payment (idempotent)
    existing = db.execute(
        "SELECT id FROM payments WHERE report_id = %s AND provider = %s AND status = 'pending'",
        (req.report_id, req.provider.value),
    ).fetchone()

    if existing:
        return {
            "payment_id": existing["id"],
            "report_id": req.report_id,
            "amount": report["price"],
            "provider": req.provider.value,
        }

    amount = report["price"]
    provider = req.provider.value
    provider_payment_id = None
    payment_url = None
    razorpay_key_id = None

    # --- COD: no gateway needed ---
    if provider == "cod":
        pass  # Just create record, no external call

    # --- RAZORPAY: Create Razorpay Order ---
    elif provider == "razorpay":
        if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
            try:
                import razorpay
                client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
                rz_order = client.order.create({
                    "amount": int(amount * 100),  # Razorpay uses paise
                    "currency": "INR",
                    "receipt": f"report_{req.report_id}",
                })
                provider_payment_id = rz_order["id"]
                razorpay_key_id = RAZORPAY_KEY_ID
            except Exception:
                provider_payment_id = f"rz_pending_report_{req.report_id}"
        else:
            provider_payment_id = f"rz_test_report_{req.report_id}"

    # --- STRIPE: Create Checkout Session ---
    elif provider == "stripe":
        if STRIPE_SECRET_KEY:
            try:
                import stripe
                stripe.api_key = STRIPE_SECRET_KEY
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[{
                        "price_data": {
                            "currency": "inr",
                            "product_data": {"name": f"AstroVedic Report"},
                            "unit_amount": int(amount * 100),
                        },
                        "quantity": 1,
                    }],
                    mode="payment",
                    success_url=f"{FRONTEND_URL}/profile%sreport_payment=success&report_id={req.report_id}",
                    cancel_url=f"{FRONTEND_URL}/profile%sreport_payment=cancelled",
                    metadata={"report_id": req.report_id, "user_id": user_id},
                )
                provider_payment_id = session.id
                payment_url = session.url
            except Exception:
                provider_payment_id = f"stripe_pending_report_{req.report_id}"
        else:
            provider_payment_id = f"stripe_test_report_{req.report_id}"

    # Create payment record
    cursor = db.execute(
        """INSERT INTO payments (report_id, provider, provider_payment_id, amount, currency, status)
           VALUES (%s, %s, %s, %s, 'INR', 'pending')
           RETURNING id""",
        (req.report_id, provider, provider_payment_id, amount),
    )
    payment_id = cursor.fetchone()["id"]
    db.commit()

    result = {
        "payment_id": payment_id,
        "report_id": req.report_id,
        "amount": amount,
        "currency": "INR",
        "provider": provider,
        "provider_payment_id": provider_payment_id,
    }
    if payment_url:
        result["payment_url"] = payment_url
    if razorpay_key_id:
        result["razorpay_key_id"] = razorpay_key_id

    return result


@router.post("/api/payments/webhook/razorpay")
async def razorpay_webhook(request: Request):
    """
    Razorpay payment webhook. Verifies signature and updates payment/order status.
    Idempotent: re-processing an already-completed payment is a no-op.
    """
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")

    # Verify signature
    if RAZORPAY_KEY_SECRET:
        expected = hmac.new(
            RAZORPAY_KEY_SECRET.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected, signature):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Razorpay signature",
            )

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON body"
        )

    event = payload.get("event", "")
    payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
    razorpay_payment_id = payment_entity.get("id", "")
    order_id = payment_entity.get("notes", {}).get("order_id", "")
    report_id = payment_entity.get("notes", {}).get("report_id", "")

    if not order_id and not report_id:
        return {"status": "ok", "message": "No order_id or report_id in notes, skipped"}

    # Create DB connection in async context (same thread as event loop)
    db = _get_webhook_db()
    try:
        # Idempotent: check if already processed
        existing = db.execute(
            "SELECT id, status FROM payments WHERE order_id = %s AND provider = 'razorpay' AND provider_payment_id = %s",
            (order_id, razorpay_payment_id),
        ).fetchone()

        if existing and existing["status"] == "completed":
            return {"status": "ok", "message": "Already processed"}

        # Handle report payments
        if report_id:
            if event == "payment.captured":
                # Update payment record
                db.execute(
                    """
                    UPDATE payments SET status = 'completed', provider_payment_id = %s,
                           metadata = %s WHERE report_id = %s AND provider = 'razorpay' AND status = 'pending'
                    """,
                    (razorpay_payment_id, json.dumps(payment_entity), report_id),
                )
                # Update report status and trigger PDF generation
                db.execute(
                    "UPDATE reports SET status = 'paid', updated_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id = %s",
                    (report_id,),
                )
                db.commit()
                
                # Trigger PDF generation in background
                report_row = db.execute(
                    "SELECT kundli_id, report_type FROM reports WHERE id = %s", (report_id,)
                ).fetchone()
                if report_row:
                    from app.routes.reports import _background_generate_pdf
                    import threading
                    db_path = os.getenv("DB_PATH", _DEFAULT_DB_PATH)
                    threading.Thread(
                        target=_background_generate_pdf,
                        args=(report_id, report_row["kundli_id"], report_row["report_type"], db_path)
                    ).start()
                
                return {"status": "ok", "message": "Report payment captured"}
            elif event == "payment.failed":
                db.execute(
                    """
                    UPDATE payments SET status = 'failed', provider_payment_id = %s,
                           metadata = %s WHERE report_id = %s AND provider = 'razorpay' AND status = 'pending'
                    """,
                    (razorpay_payment_id, json.dumps(payment_entity), report_id),
                )
                db.commit()
                return {"status": "ok", "message": "Report payment failure recorded"}
            return {"status": "ok", "message": f"Event '{event}' acknowledged for report"}

        # Handle order payments
        if event == "payment.captured":
            # Update payment record
            db.execute(
                """
                UPDATE payments SET status = 'completed', provider_payment_id = %s,
                       metadata = %s WHERE order_id = %s AND provider = 'razorpay' AND status = 'pending'
                """,
                (razorpay_payment_id, json.dumps(payment_entity), order_id),
            )
            # Update order payment status
            db.execute(
                "UPDATE orders SET payment_status = 'paid', status = 'confirmed', "
                "updated_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id = %s",
                (order_id,),
            )
            db.commit()
            return {"status": "ok", "message": "Payment captured"}

        elif event == "payment.failed":
            db.execute(
                """
                UPDATE payments SET status = 'failed', provider_payment_id = %s,
                       metadata = %s WHERE order_id = %s AND provider = 'razorpay' AND status = 'pending'
                """,
                (razorpay_payment_id, json.dumps(payment_entity), order_id),
            )
            db.execute(
                "UPDATE orders SET payment_status = 'failed', updated_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id = %s",
                (order_id,),
            )
            db.commit()
            return {"status": "ok", "message": "Payment failure recorded"}

        return {"status": "ok", "message": f"Event '{event}' acknowledged"}
    finally:
        db.close()


@router.post("/api/payments/webhook/stripe")
async def stripe_webhook(request: Request):
    """
    Stripe payment webhook. Verifies signature and updates payment/order status.
    Idempotent: re-processing an already-completed payment is a no-op.
    C-02: Uses stripe.Webhook.construct_event as PRIMARY verification method.
    """
    body = await request.body()
    signature = request.headers.get("Stripe-Signature", "")

    # Verify Stripe signature — prefer stripe library, fallback to manual HMAC
    if STRIPE_WEBHOOK_SECRET and signature:
        try:
            import stripe as _stripe_lib
            # Use official Stripe SDK verification (preferred — C-02)
            event_obj = _stripe_lib.Webhook.construct_event(
                body, signature, STRIPE_WEBHOOK_SECRET
            )
            payload = event_obj  # construct_event returns the parsed event
        except ImportError:
            # stripe library not installed — fallback to manual HMAC
            parts = dict(item.split("=", 1) for item in signature.split(",") if "=" in item)
            timestamp = parts.get("t", "")
            sig_v1 = parts.get("v1", "")

            if timestamp and sig_v1:
                signed_payload = f"{timestamp}.{body.decode()}"
                expected = hmac.new(
                    STRIPE_WEBHOOK_SECRET.encode(),
                    signed_payload.encode(),
                    hashlib.sha256,
                ).hexdigest()
                if not hmac.compare_digest(expected, sig_v1):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid Stripe signature",
                    )
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON body"
                )
        except Exception as e:
            # Catches stripe.error.SignatureVerificationError and any other
            # verification failure from the Stripe SDK
            err_type = type(e).__name__
            if err_type == "SignatureVerificationError" or "signature" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid Stripe signature",
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Webhook verification failed: {str(e)}",
            )
    else:
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON body"
            )

    event_type = payload.get("type", "")
    data_object = payload.get("data", {}).get("object", {})
    stripe_payment_id = data_object.get("id", "")
    order_id = data_object.get("metadata", {}).get("order_id", "")
    report_id = data_object.get("metadata", {}).get("report_id", "")

    if not order_id and not report_id:
        return {"status": "ok", "message": "No order_id or report_id in metadata, skipped"}

    # Create DB connection in async context (same thread as event loop)
    db = _get_webhook_db()
    try:
        # Idempotent: check if already processed
        existing = db.execute(
            "SELECT id, status FROM payments WHERE order_id = %s AND provider = 'stripe' AND provider_payment_id = %s",
            (order_id, stripe_payment_id),
        ).fetchone()

        if existing and existing["status"] == "completed":
            return {"status": "ok", "message": "Already processed"}

        # Handle report payments
        if report_id:
            if event_type in ("checkout.session.completed", "payment_intent.succeeded"):
                db.execute(
                    """
                    UPDATE payments SET status = 'completed', provider_payment_id = %s,
                           metadata = %s WHERE report_id = %s AND provider = 'stripe' AND status = 'pending'
                    """,
                    (stripe_payment_id, json.dumps(data_object), report_id),
                )
                db.execute(
                    "UPDATE reports SET status = 'paid', updated_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id = %s",
                    (report_id,),
                )
                db.commit()
                
                # Trigger PDF generation in background
                report_row = db.execute(
                    "SELECT kundli_id, report_type FROM reports WHERE id = %s", (report_id,)
                ).fetchone()
                if report_row:
                    from app.routes.reports import _background_generate_pdf
                    import threading
                    db_path = os.getenv("DB_PATH", _DEFAULT_DB_PATH)
                    threading.Thread(
                        target=_background_generate_pdf,
                        args=(report_id, report_row["kundli_id"], report_row["report_type"], db_path)
                    ).start()
                
                return {"status": "ok", "message": "Report payment succeeded"}
            elif event_type == "payment_intent.payment_failed":
                db.execute(
                    """
                    UPDATE payments SET status = 'failed', provider_payment_id = %s,
                           metadata = %s WHERE report_id = %s AND provider = 'stripe' AND status = 'pending'
                    """,
                    (stripe_payment_id, json.dumps(data_object), report_id),
                )
                db.commit()
                return {"status": "ok", "message": "Report payment failure recorded"}
            return {"status": "ok", "message": f"Event '{event_type}' acknowledged for report"}

        # Handle order payments
        if event_type in ("checkout.session.completed", "payment_intent.succeeded"):
            db.execute(
                """
                UPDATE payments SET status = 'completed', provider_payment_id = %s,
                       metadata = %s WHERE order_id = %s AND provider = 'stripe' AND status = 'pending'
                """,
                (stripe_payment_id, json.dumps(data_object), order_id),
            )
            db.execute(
                "UPDATE orders SET payment_status = 'paid', status = 'confirmed', "
                "updated_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id = %s",
                (order_id,),
            )
            db.commit()
            return {"status": "ok", "message": "Payment succeeded"}

        elif event_type == "payment_intent.payment_failed":
            db.execute(
                """
                UPDATE payments SET status = 'failed', provider_payment_id = %s,
                       metadata = %s WHERE order_id = %s AND provider = 'stripe' AND status = 'pending'
                """,
                (stripe_payment_id, json.dumps(data_object), order_id),
            )
            db.execute(
                "UPDATE orders SET payment_status = 'failed', updated_at = to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS') WHERE id = %s",
                (order_id,),
            )
            db.commit()
            return {"status": "ok", "message": "Payment failure recorded"}

        return {"status": "ok", "message": f"Event '{event_type}' acknowledged"}
    finally:
        db.close()
