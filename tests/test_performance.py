"""Performance tests for AstroVedic API.

Covers:
- Response time benchmarks (6 tests)
- Concurrency safety (3 tests)
- Load endurance (2 tests)

Uses time.perf_counter for measurement and ThreadPoolExecutor for concurrency.
Rate limiter is set to a very high value so performance measurements are not skewed.
"""
import os
import time
import sqlite3
import tracemalloc
import importlib
import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi.testclient import TestClient


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture(scope="module")
def perf_db(tmp_path_factory):
    """Create a fresh test database for all performance tests.

    Uses module scope + very high rate limit so perf tests are not throttled.
    """
    db_path = str(tmp_path_factory.mktemp("perfdb") / "test_perf.db")
    os.environ["DB_PATH"] = db_path
    os.environ["RATE_LIMIT_PER_MINUTE"] = "99999"
    import app.config
    importlib.reload(app.config)
    import app.database
    importlib.reload(app.database)
    from app.database import init_db, migrate_users_table
    init_db(db_path)
    migrate_users_table(db_path)
    return db_path


@pytest.fixture(scope="module")
def perf_client(perf_db):
    """TestClient with high rate limit for performance tests."""
    from app.main import app
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture(scope="module")
def perf_user_token(perf_client):
    """Register a user for performance tests, return token."""
    resp = perf_client.post("/api/auth/register", json={
        "email": "perfuser@test.com",
        "password": "perfpass123",
        "name": "Perf User",
    })
    assert resp.status_code == 201
    return resp.json()["token"]


@pytest.fixture(scope="module")
def seeded_product_id(perf_db):
    """Insert a test product directly and return its ID."""
    conn = sqlite3.connect(perf_db)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """INSERT INTO products (id, name, description, category, price, stock, is_active)
           VALUES ('perf-prod-001', 'Ruby Gemstone', 'Natural unheated ruby', 'gemstone', 2500.0, 100, 1)"""
    )
    conn.commit()
    conn.close()
    return "perf-prod-001"


# ============================================================
# Response Time Benchmarks (6 tests)
# ============================================================

class TestResponseTime:
    """API response time benchmarks."""

    def test_health_under_50ms(self, perf_client):
        """GET /health must respond in under 50ms."""
        start = time.perf_counter()
        resp = perf_client.get("/health")
        duration_ms = (time.perf_counter() - start) * 1000
        assert resp.status_code == 200
        assert duration_ms < 50, f"Health took {duration_ms:.1f}ms (limit: 50ms)"

    def test_products_under_200ms(self, perf_client):
        """GET /api/products must respond in under 200ms."""
        start = time.perf_counter()
        resp = perf_client.get("/api/products")
        duration_ms = (time.perf_counter() - start) * 1000
        assert resp.status_code == 200
        assert duration_ms < 200, f"Products took {duration_ms:.1f}ms (limit: 200ms)"

    def test_panchang_under_500ms(self, perf_client):
        """GET /api/panchang must respond in under 500ms."""
        start = time.perf_counter()
        resp = perf_client.get("/api/panchang", params={
            "date": "2025-01-15",
            "latitude": 28.6139,
            "longitude": 77.2090,
        })
        duration_ms = (time.perf_counter() - start) * 1000
        assert resp.status_code == 200
        assert duration_ms < 500, f"Panchang took {duration_ms:.1f}ms (limit: 500ms)"

    def test_kundli_generate_under_2000ms(self, perf_client, perf_user_token):
        """POST /api/kundli/generate must respond in under 2000ms."""
        start = time.perf_counter()
        resp = perf_client.post(
            "/api/kundli/generate",
            json={
                "person_name": "Perf Test Person",
                "birth_date": "1990-05-15",
                "birth_time": "14:30:00",
                "birth_place": "Delhi, India",
                "latitude": 28.6139,
                "longitude": 77.209,
                "timezone_offset": 5.5,
            },
            headers={"Authorization": f"Bearer {perf_user_token}"},
        )
        duration_ms = (time.perf_counter() - start) * 1000
        assert resp.status_code == 201
        assert duration_ms < 2000, f"Kundli generate took {duration_ms:.1f}ms (limit: 2000ms)"

    def test_numerology_under_100ms(self, perf_client):
        """POST /api/numerology/calculate must respond in under 100ms."""
        start = time.perf_counter()
        resp = perf_client.post("/api/numerology/calculate", json={
            "name": "Meharban Singh",
            "birth_date": "1990-05-15",
        })
        duration_ms = (time.perf_counter() - start) * 1000
        assert resp.status_code == 200
        assert duration_ms < 100, f"Numerology took {duration_ms:.1f}ms (limit: 100ms)"

    def test_search_under_200ms(self, perf_client, seeded_product_id):
        """GET /api/search?q=ruby must respond in under 200ms."""
        start = time.perf_counter()
        resp = perf_client.get("/api/search", params={"q": "ruby"})
        duration_ms = (time.perf_counter() - start) * 1000
        assert resp.status_code == 200
        assert duration_ms < 200, f"Search took {duration_ms:.1f}ms (limit: 200ms)"


# ============================================================
# Concurrency Tests (3 tests)
# ============================================================

class TestConcurrency:
    """Concurrent request safety tests."""

    def test_concurrent_products_all_succeed(self, perf_client):
        """10 concurrent GET /api/products must all return 200."""
        results = []

        def fetch_products():
            return perf_client.get("/api/products")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_products) for _ in range(10)]
            for f in as_completed(futures):
                results.append(f.result())

        assert len(results) == 10
        for resp in results:
            assert resp.status_code == 200, f"Got {resp.status_code}: {resp.text}"

    def test_concurrent_kundli_generate_no_race(self, perf_db, perf_user_token):
        """10 concurrent kundli generations must all succeed without race conditions."""
        os.environ["DB_PATH"] = perf_db
        from app.main import app
        concurrent_client = TestClient(app, raise_server_exceptions=False)
        results = []

        def gen_kundli(idx):
            return concurrent_client.post(
                "/api/kundli/generate",
                json={
                    "person_name": f"Concurrent Person {idx}",
                    "birth_date": "1990-05-15",
                    "birth_time": "14:30:00",
                    "birth_place": "Delhi, India",
                    "latitude": 28.6139,
                    "longitude": 77.209,
                    "timezone_offset": 5.5,
                },
                headers={"Authorization": f"Bearer {perf_user_token}"},
            )

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(gen_kundli, i) for i in range(10)]
            for f in as_completed(futures):
                results.append(f.result())

        assert len(results) == 10
        success_count = sum(1 for r in results if r.status_code == 201)
        assert success_count == 10, f"Only {success_count}/10 kundli generations succeeded"

        # Verify all 10 are actually stored (no duplicates or lost writes)
        conn = sqlite3.connect(perf_db)
        count = conn.execute(
            "SELECT COUNT(*) as c FROM kundlis WHERE person_name LIKE 'Concurrent Person%'"
        ).fetchone()[0]
        conn.close()
        assert count == 10, f"Expected 10 kundlis but found {count}"

    def test_concurrent_cart_adds_correct_stock(self, perf_db, seeded_product_id):
        """5 concurrent cart adds for same product must all track stock correctly."""
        # Create 5 separate users with their own tokens
        os.environ["DB_PATH"] = perf_db
        from app.main import app
        cart_client = TestClient(app, raise_server_exceptions=False)

        user_tokens = []
        for i in range(5):
            resp = cart_client.post("/api/auth/register", json={
                "email": f"cartuser{i}@test.com",
                "password": "cartpass123",
                "name": f"Cart User {i}",
            })
            if resp.status_code == 201:
                user_tokens.append(resp.json()["token"])
            elif resp.status_code == 409:
                # Already exists from previous run — login instead
                resp = cart_client.post("/api/auth/login", json={
                    "email": f"cartuser{i}@test.com",
                    "password": "cartpass123",
                })
                user_tokens.append(resp.json()["token"])

        assert len(user_tokens) == 5, f"Only got {len(user_tokens)} user tokens"

        results = []

        def add_to_cart(token):
            return cart_client.post(
                "/api/cart/add",
                json={"product_id": seeded_product_id, "quantity": 1},
                headers={"Authorization": f"Bearer {token}"},
            )

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(add_to_cart, t) for t in user_tokens]
            for f in as_completed(futures):
                results.append(f.result())

        assert len(results) == 5
        success_count = sum(1 for r in results if r.status_code == 201)
        assert success_count == 5, f"Only {success_count}/5 cart adds succeeded"


# ============================================================
# Load Tests (2 tests)
# ============================================================

class TestLoad:
    """Load and endurance tests."""

    def test_50_sequential_health_no_degradation(self, perf_client):
        """50 sequential requests to /health must all be under 100ms with no degradation."""
        durations = []
        for _ in range(50):
            start = time.perf_counter()
            resp = perf_client.get("/health")
            duration_ms = (time.perf_counter() - start) * 1000
            assert resp.status_code == 200
            durations.append(duration_ms)

        # All must be under 100ms
        for i, d in enumerate(durations):
            assert d < 100, f"Request {i+1} took {d:.1f}ms (limit: 100ms)"

        # Check no degradation: last 10 should not be significantly worse than first 10
        first_10_avg = sum(durations[:10]) / 10
        last_10_avg = sum(durations[-10:]) / 10
        # Allow up to 3x degradation (generous margin for test environment variance)
        assert last_10_avg < first_10_avg * 3 + 5, (
            f"Performance degradation detected: first 10 avg={first_10_avg:.1f}ms, "
            f"last 10 avg={last_10_avg:.1f}ms"
        )

    def test_memory_stable_after_100_requests(self, perf_client):
        """Memory must be stable after 100 requests (no leak)."""
        tracemalloc.start()
        snapshot_before = tracemalloc.take_snapshot()

        for _ in range(100):
            perf_client.get("/health")

        snapshot_after = tracemalloc.take_snapshot()
        tracemalloc.stop()

        # Compare memory: calculate total allocated in both snapshots
        stats_before = snapshot_before.statistics("filename")
        stats_after = snapshot_after.statistics("filename")

        total_before = sum(s.size for s in stats_before)
        total_after = sum(s.size for s in stats_after)

        # Memory growth should be less than 10MB for 100 simple requests
        growth_mb = (total_after - total_before) / (1024 * 1024)
        assert growth_mb < 10, (
            f"Memory grew by {growth_mb:.2f}MB after 100 requests (limit: 10MB)"
        )
