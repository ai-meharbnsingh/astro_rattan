"""Tests for public and admin blog routes plus sitemap generation."""
from tests.conftest import _register_user, _auth_header, _make_admin


def test_public_blog_list_returns_seed_posts(client):
    """Published blog list should expose starter editorial posts."""
    resp = client.get("/api/blog/posts")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 3
    assert any(item["slug"] == "how-to-read-your-daily-panchang" for item in data["items"])


def test_public_blog_detail_returns_post(client):
    """Published blog detail should return full content."""
    resp = client.get("/api/blog/posts/how-to-read-your-daily-panchang")
    assert resp.status_code == 200
    data = resp.json()
    assert data["slug"] == "how-to-read-your-daily-panchang"
    assert "content" in data
    assert "Panchang" in data["title"]


def test_dynamic_sitemap_includes_blog_routes(client):
    """Runtime sitemap should include blog index and post URLs."""
    resp = client.get("/sitemap.xml")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/xml")
    body = resp.text
    assert "/blog</loc>" in body
    assert "/blog/how-to-read-your-daily-panchang</loc>" in body


def test_admin_blog_crud_flow(client, db):
    """Admin should be able to create, update, and delete a blog post."""
    admin_user, _ = _register_user(client, "blog_admin@test.com", name="Blog Admin")
    admin_token = _make_admin(db, admin_user["id"])

    create_resp = client.post(
        "/api/admin/blog",
        json={
            "title": "Palmistry Testing Deep Dive",
            "excerpt": "A long-form editorial note about testing palmistry image flows and making sure the system is reliable in production.",
            "content": "This article explains how palmistry image analysis should be validated in production environments with clear fixtures, realistic input sizes, and stable response contracts. It also covers regression checks for uploads and reading quality.",
            "tags": ["testing", "palmistry"],
        },
        headers=_auth_header(admin_token),
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["slug"] == "palmistry-testing-deep-dive"

    update_resp = client.patch(
        f"/api/admin/blog/{created['id']}",
        json={"title": "Palmistry Testing Deep Dive Updated", "is_published": False},
        headers=_auth_header(admin_token),
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["slug"] == "palmistry-testing-deep-dive-updated"
    assert updated["is_published"] is False

    public_resp = client.get(f"/api/blog/posts/{updated['slug']}")
    assert public_resp.status_code == 404

    delete_resp = client.delete(
        f"/api/admin/blog/{created['id']}",
        headers=_auth_header(admin_token),
    )
    assert delete_resp.status_code == 204


def test_non_admin_cannot_create_blog_post(client):
    """Non-admin users must be blocked from editorial admin routes."""
    _, token = _register_user(client, "blog_user@test.com", name="Blog User")
    resp = client.post(
        "/api/admin/blog",
        json={
            "title": "Unauthorized Post Attempt",
            "excerpt": "This excerpt is long enough to satisfy validation but should never be accepted by the admin endpoint.",
            "content": "This content is long enough to satisfy validation but should not be accepted because the user is not an admin and the route must reject it.",
        },
        headers=_auth_header(token),
    )
    assert resp.status_code == 403
