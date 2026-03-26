"""Tests for email notification hooks."""
from app.auth import decode_token


def test_register_triggers_welcome_email(client, monkeypatch):
    calls = []

    def fake_send_registration_welcome(name, email):
        calls.append((name, email))
        return True

    monkeypatch.setattr("app.routes.auth.send_registration_welcome", fake_send_registration_welcome)

    resp = client.post("/api/auth/register", json={
        "email": "welcome_email@test.com",
        "password": "password123",
        "name": "Welcome User",
    })

    assert resp.status_code == 201
    assert calls == [("Welcome User", "welcome_email@test.com")]


def test_create_order_triggers_order_emails(client, db, monkeypatch):
    order_calls = []
    alert_calls = []

    def fake_order_confirmation(order, email):
        order_calls.append((order, email))
        return True

    def fake_order_alert(order, email):
        alert_calls.append((order, email))
        return True

    monkeypatch.setattr("app.routes.orders.send_order_confirmation", fake_order_confirmation)
    monkeypatch.setattr("app.routes.orders.send_order_alert", fake_order_alert)

    reg = client.post("/api/auth/register", json={
        "email": "order_email@test.com",
        "password": "password123",
        "name": "Order Email User",
    })
    assert reg.status_code == 201
    token = reg.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    product = db.execute("SELECT id FROM products WHERE is_active = 1 LIMIT 1").fetchone()
    assert product is not None
    add_resp = client.post("/api/cart/add", json={"product_id": product["id"], "quantity": 1}, headers=headers)
    assert add_resp.status_code == 201

    resp = client.post("/api/orders", json={
        "shipping_address": "123 Email Test Street, Mumbai 400001",
        "payment_method": "cod",
    }, headers=headers)

    assert resp.status_code == 201
    assert len(order_calls) == 1
    assert len(alert_calls) == 1
    sent_order, sent_email = order_calls[0]
    assert sent_order["id"] == resp.json()["id"]
    assert sent_email == "order_email@test.com"
    assert sent_order["items"][0]["product_id"] == product["id"]
