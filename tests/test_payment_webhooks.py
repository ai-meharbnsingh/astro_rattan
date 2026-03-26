"""H-13: Payment webhook idempotency and signature tests.

Tests:
- Razorpay webhook valid/invalid signature
- Razorpay webhook replay idempotency
- Stripe webhook valid/invalid signature
- Stripe webhook replay idempotency
- Payment status transition guards
"""
import hashlib
import hmac
import json
import os
import sqlite3
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def test_db(tmp_path):
    """Create a fresh test database."""
    db_path = str(tmp_path / "test_webhooks.db")
    os.environ["DB_PATH"] = db_path

    from app.database import init_db, migrate_users_table
    init_db(db_path)
    migrate_users_table(db_path)
    return db_path


@pytest.fixture
def client(test_db):
    """TestClient with fresh DB — created once, no module reloading."""
    os.environ["DB_PATH"] = test_db
    from app.main import app
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def user_token(client):
    """Register a regular user and return JWT token."""
    resp = client.post("/api/auth/register", json={
        "email": "webhook_user@test.com",
        "password": "password123",
        "name": "Webhook User",
    })
    return resp.json()["token"]


def _get_user_id(db_path, email):
    """Helper: get user ID from email."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row["id"] if row else None


def _setup_order_and_payment(db_path, user_id, provider, provider_payment_id=None,
                             order_id=None, payment_id=None, payment_status="pending",
                             order_payment_status="pending"):
    """Helper: insert an order + pending payment directly into DB."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")

    oid = order_id or f"ord_{provider}_test"
    ppid = provider_payment_id or f"{provider}_pay_test"
    pid = payment_id or f"pay_{provider}_test"

    conn.execute(
        """INSERT OR IGNORE INTO orders (id, user_id, status, total, shipping_address,
           payment_method, payment_status)
           VALUES (?, ?, 'placed', 500.0, '123 Test Street', ?, ?)""",
        (oid, user_id, provider, order_payment_status),
    )

    conn.execute(
        """INSERT OR IGNORE INTO payments (id, order_id, provider, provider_payment_id,
           amount, currency, status)
           VALUES (?, ?, ?, ?, 500.0, 'INR', ?)""",
        (pid, oid, provider, ppid, payment_status),
    )
    conn.commit()
    conn.close()
    return oid


def _make_razorpay_body_and_sig(order_id, payment_id, secret, event="payment.captured"):
    """Build Razorpay webhook body and HMAC signature."""
    payload = {
        "event": event,
        "payload": {
            "payment": {
                "entity": {
                    "id": payment_id,
                    "notes": {"order_id": order_id},
                }
            }
        }
    }
    body = json.dumps(payload).encode()
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return body, sig


def _make_stripe_body(order_id, payment_id, event_type="payment_intent.succeeded"):
    """Build Stripe webhook body (no signature needed for no-secret mode)."""
    payload = {
        "type": event_type,
        "data": {
            "object": {
                "id": payment_id,
                "metadata": {"order_id": order_id},
            }
        }
    }
    return json.dumps(payload).encode()


# ============================================================
# Razorpay Webhook Tests
# ============================================================

class TestRazorpayWebhookValidSignature:
    """test_razorpay_webhook_valid_signature: 200, order status updated."""

    def test_razorpay_webhook_valid_signature(self, test_db, client):
        """Webhook with correct HMAC signature should succeed and update order."""
        secret = "rzp_test_secret_valid"

        # Register user
        resp = client.post("/api/auth/register", json={
            "email": "rz_valid@test.com", "password": "pass123456", "name": "RZ User",
        })
        user_id = _get_user_id(test_db, "rz_valid@test.com")

        order_id = _setup_order_and_payment(
            test_db, user_id, "razorpay", "pay_rz_valid_123",
            order_id="ord_rz_valid", payment_id="pay_rz_valid",
        )

        body, sig = _make_razorpay_body_and_sig(order_id, "pay_rz_valid_123", secret)

        with patch("app.routes.payments.RAZORPAY_KEY_SECRET", secret):
            resp = client.post(
                "/api/payments/webhook/razorpay",
                content=body,
                headers={"X-Razorpay-Signature": sig, "Content-Type": "application/json"},
            )
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
        assert resp.json()["status"] == "ok"

        # Verify order updated to paid
        conn = sqlite3.connect(test_db)
        conn.row_factory = sqlite3.Row
        order = conn.execute(
            "SELECT payment_status FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        conn.close()
        assert order["payment_status"] == "paid"


class TestRazorpayWebhookInvalidSignature:
    """test_razorpay_webhook_invalid_signature: 400."""

    def test_razorpay_webhook_invalid_signature(self, test_db, client):
        """Webhook with incorrect signature must return 400."""
        secret = "rzp_test_secret_invalid"

        payload = {
            "event": "payment.captured",
            "payload": {
                "payment": {
                    "entity": {"id": "pay_rz_bad", "notes": {"order_id": "ord_x"}}
                }
            }
        }
        body = json.dumps(payload).encode()

        with patch("app.routes.payments.RAZORPAY_KEY_SECRET", secret):
            resp = client.post(
                "/api/payments/webhook/razorpay",
                content=body,
                headers={"X-Razorpay-Signature": "wrong_sig", "Content-Type": "application/json"},
            )
        assert resp.status_code == 400


class TestRazorpayWebhookReplayIdempotent:
    """test_razorpay_webhook_replay_idempotent: 200, order not double-charged."""

    def test_razorpay_webhook_replay_idempotent(self, test_db, client):
        """Replaying the same webhook should return 200 but NOT double-process."""
        secret = "rzp_test_secret_replay"

        # Register user
        resp = client.post("/api/auth/register", json={
            "email": "rz_replay@test.com", "password": "pass123456", "name": "RZ Replay",
        })
        user_id = _get_user_id(test_db, "rz_replay@test.com")

        order_id = _setup_order_and_payment(
            test_db, user_id, "razorpay", "pay_rz_replay_123",
            order_id="ord_rz_replay", payment_id="pay_rz_replay",
        )

        body, sig = _make_razorpay_body_and_sig(order_id, "pay_rz_replay_123", secret)

        with patch("app.routes.payments.RAZORPAY_KEY_SECRET", secret):
            # First call -- should process
            resp1 = client.post(
                "/api/payments/webhook/razorpay",
                content=body,
                headers={"X-Razorpay-Signature": sig, "Content-Type": "application/json"},
            )
            assert resp1.status_code == 200

            # Second call (replay) -- should return 200 "already processed"
            resp2 = client.post(
                "/api/payments/webhook/razorpay",
                content=body,
                headers={"X-Razorpay-Signature": sig, "Content-Type": "application/json"},
            )
            assert resp2.status_code == 200
            assert "already" in resp2.json().get("message", "").lower()


# ============================================================
# Stripe Webhook Tests
# ============================================================

class TestStripeWebhookValid:
    """test_stripe_webhook_valid: 200 with no secret set (passthrough mode)."""

    def test_stripe_webhook_valid_no_secret(self, test_db, client):
        """When STRIPE_WEBHOOK_SECRET is empty, webhook accepts valid JSON."""
        # Register user
        resp = client.post("/api/auth/register", json={
            "email": "stripe_valid@test.com", "password": "pass123456", "name": "Stripe User",
        })
        user_id = _get_user_id(test_db, "stripe_valid@test.com")

        order_id = _setup_order_and_payment(
            test_db, user_id, "stripe", "pi_stripe_valid",
            order_id="ord_stripe_valid", payment_id="pay_stripe_valid",
        )

        body = _make_stripe_body(order_id, "pi_stripe_valid")

        with patch("app.routes.payments.STRIPE_WEBHOOK_SECRET", ""):
            resp = client.post(
                "/api/payments/webhook/stripe",
                content=body,
                headers={"Content-Type": "application/json"},
            )
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
        assert resp.json()["status"] == "ok"

        # Verify order updated
        conn = sqlite3.connect(test_db)
        conn.row_factory = sqlite3.Row
        order = conn.execute(
            "SELECT payment_status FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        conn.close()
        assert order["payment_status"] == "paid"


class TestStripeWebhookInvalidSig:
    """test_stripe_webhook_invalid_sig: 400."""

    def test_stripe_webhook_invalid_sig(self, test_db, client):
        """Webhook with bad Stripe-Signature when secret is set must return 400."""
        secret = "whsec_test_secret_invalid"

        body = _make_stripe_body("ord_x", "pi_bad")

        with patch("app.routes.payments.STRIPE_WEBHOOK_SECRET", secret):
            resp = client.post(
                "/api/payments/webhook/stripe",
                content=body,
                headers={
                    "Stripe-Signature": "t=12345,v1=completely_invalid_signature",
                    "Content-Type": "application/json",
                },
            )
        assert resp.status_code == 400


class TestStripeWebhookReplayIdempotent:
    """test_stripe_webhook_replay_idempotent: 200."""

    def test_stripe_webhook_replay_idempotent(self, test_db, client):
        """Replaying the same Stripe webhook should return 200 but not double-process."""
        # Register user
        resp = client.post("/api/auth/register", json={
            "email": "stripe_replay@test.com", "password": "pass123456", "name": "Stripe Replay",
        })
        user_id = _get_user_id(test_db, "stripe_replay@test.com")

        order_id = _setup_order_and_payment(
            test_db, user_id, "stripe", "pi_stripe_replay",
            order_id="ord_stripe_replay", payment_id="pay_stripe_replay",
        )

        body = _make_stripe_body(order_id, "pi_stripe_replay")

        with patch("app.routes.payments.STRIPE_WEBHOOK_SECRET", ""):
            # First call
            resp1 = client.post(
                "/api/payments/webhook/stripe",
                content=body,
                headers={"Content-Type": "application/json"},
            )
            assert resp1.status_code == 200

            # Replay -- should return 200 "already processed"
            resp2 = client.post(
                "/api/payments/webhook/stripe",
                content=body,
                headers={"Content-Type": "application/json"},
            )
            assert resp2.status_code == 200
            assert "already" in resp2.json().get("message", "").lower()


# ============================================================
# Payment Status Transition Tests
# ============================================================

class TestPaymentStatusTransitions:
    """test_payment_status_transitions: pending->completed, not completed->pending."""

    def test_pending_to_completed_via_webhook(self, test_db, client):
        """A pending payment should transition to completed on successful webhook."""
        # Register user
        resp = client.post("/api/auth/register", json={
            "email": "transition@test.com", "password": "pass123456", "name": "Trans User",
        })
        user_id = _get_user_id(test_db, "transition@test.com")

        order_id = _setup_order_and_payment(
            test_db, user_id, "stripe", "pi_transition",
            order_id="ord_transition", payment_id="pay_transition",
        )

        # Verify initial state is pending
        conn = sqlite3.connect(test_db)
        conn.row_factory = sqlite3.Row
        payment = conn.execute(
            "SELECT status FROM payments WHERE order_id = ?", (order_id,)
        ).fetchone()
        conn.close()
        assert payment["status"] == "pending"

        # Send successful webhook
        body = _make_stripe_body(order_id, "pi_transition")

        with patch("app.routes.payments.STRIPE_WEBHOOK_SECRET", ""):
            resp = client.post(
                "/api/payments/webhook/stripe",
                content=body,
                headers={"Content-Type": "application/json"},
            )
        assert resp.status_code == 200

        # Verify payment is now completed
        conn = sqlite3.connect(test_db)
        conn.row_factory = sqlite3.Row
        payment = conn.execute(
            "SELECT status FROM payments WHERE order_id = ?", (order_id,)
        ).fetchone()
        conn.close()
        assert payment["status"] == "completed"

    def test_completed_cannot_revert_to_pending(self, test_db, client):
        """A completed payment should NOT revert to pending on a second webhook."""
        # Register user
        resp = client.post("/api/auth/register", json={
            "email": "norevert@test.com", "password": "pass123456", "name": "No Revert",
        })
        user_id = _get_user_id(test_db, "norevert@test.com")

        # Create order + payment and mark payment as completed directly
        conn = sqlite3.connect(test_db)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        order_id = "ord_no_revert"
        conn.execute(
            """INSERT OR IGNORE INTO orders (id, user_id, status, total, shipping_address,
               payment_method, payment_status)
               VALUES (?, ?, 'confirmed', 500.0, '123 Test St', 'stripe', 'paid')""",
            (order_id, user_id),
        )
        conn.execute(
            """INSERT OR IGNORE INTO payments (id, order_id, provider, provider_payment_id,
               amount, currency, status)
               VALUES ('pay_no_revert', ?, 'stripe', 'pi_no_revert', 500.0, 'INR', 'completed')""",
            (order_id,),
        )
        conn.commit()
        conn.close()

        # Send a "payment_intent.succeeded" webhook for the already-completed payment
        body = _make_stripe_body(order_id, "pi_no_revert")

        with patch("app.routes.payments.STRIPE_WEBHOOK_SECRET", ""):
            resp = client.post(
                "/api/payments/webhook/stripe",
                content=body,
                headers={"Content-Type": "application/json"},
            )
        assert resp.status_code == 200
        assert "already" in resp.json().get("message", "").lower()

        # Verify payment is STILL completed (not reverted)
        conn = sqlite3.connect(test_db)
        conn.row_factory = sqlite3.Row
        payment = conn.execute(
            "SELECT status FROM payments WHERE order_id = ? AND provider = 'stripe'",
            (order_id,),
        ).fetchone()
        conn.close()
        assert payment["status"] == "completed"
