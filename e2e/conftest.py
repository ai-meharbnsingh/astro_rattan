"""E2E test configuration — starts backend, frontend preview, and browser fixtures."""
import os
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

import pytest
from playwright.sync_api import sync_playwright

def _get_free_port() -> int:
    """Reserve a free local port for a short-lived test server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


BACKEND_PORT = _get_free_port()
FRONTEND_PORT = _get_free_port()
SERVER_URL = f"http://127.0.0.1:{BACKEND_PORT}"
FRONTEND_URL = f"http://127.0.0.1:{FRONTEND_PORT}"
BACKEND_LOG_PATH = os.path.join(tempfile.gettempdir(), "astrovedic_e2e_backend.log")
FRONTEND_LOG_PATH = os.path.join(tempfile.gettempdir(), "astrovedic_e2e_frontend.log")


def _wait_for_http(url: str, timeout_seconds: int = 30, process: subprocess.Popen | None = None):
    """Poll an HTTP endpoint until it responds."""
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if process is not None and process.poll() is not None:
            raise RuntimeError(f"Process exited while waiting for {url} with code {process.returncode}")
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status < 500:
                    return
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(0.5)
    raise RuntimeError(f"Timed out waiting for {url}")


@pytest.fixture(scope="session")
def e2e_db_path():
    """Database path used by the E2E backend server."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_e2e.db")


@pytest.fixture(scope="session", autouse=True)
def start_server(e2e_db_path):
    """Start real uvicorn server for E2E tests."""
    if os.path.exists(e2e_db_path):
        os.unlink(e2e_db_path)

    env = os.environ.copy()
    env["DB_PATH"] = e2e_db_path
    env["JWT_SECRET"] = "e2e-test-secret"
    env["TESTING"] = "1"
    env["CORS_ORIGINS"] = FRONTEND_URL
    env["FRONTEND_URL"] = FRONTEND_URL
    env["FRONTEND_PORT"] = str(FRONTEND_PORT)
    backend_log = open(BACKEND_LOG_PATH, "w")

    proc = subprocess.Popen(
        ["python3", "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(BACKEND_PORT)],
        cwd=os.path.dirname(os.path.dirname(__file__)),
        env=env,
        stdout=backend_log,
        stderr=backend_log,
        text=True,
    )

    try:
        _wait_for_http(f"{SERVER_URL}/health", process=proc)
        yield SERVER_URL
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        backend_log.close()
        if os.path.exists(e2e_db_path):
            os.unlink(e2e_db_path)


@pytest.fixture(scope="session")
def start_frontend(start_server):
    """Serve the frontend with Vite dev server for browser E2E."""
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
    env = os.environ.copy()
    env["VITE_API_URL"] = start_server
    frontend_log = open(FRONTEND_LOG_PATH, "w")
    preview = subprocess.Popen(
        ["npm", "run", "dev", "--", "--host", "127.0.0.1", "--port", str(FRONTEND_PORT)],
        cwd=frontend_dir,
        env=env,
        stdout=frontend_log,
        stderr=frontend_log,
        text=True,
    )

    try:
        _wait_for_http(FRONTEND_URL, process=preview)
        yield FRONTEND_URL
    finally:
        preview.terminate()
        try:
            preview.wait(timeout=5)
        except subprocess.TimeoutExpired:
            preview.kill()
        frontend_log.close()


@pytest.fixture(scope="session")
def base_url(start_server):
    return start_server


@pytest.fixture(scope="session")
def frontend_url(start_frontend):
    return start_frontend


@pytest.fixture(scope="session")
def api_url(start_server):
    return start_server


@pytest.fixture(scope="session")
def playwright_instance():
    """Shared Playwright instance."""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance, start_frontend):
    """Shared Chromium browser for browser smoke tests."""
    headless = os.getenv("E2E_HEADLESS", "1") not in ("0", "false", "False")
    slow_mo = int(os.getenv("E2E_SLOWMO_MS", "0"))
    browser = playwright_instance.chromium.launch(headless=headless, slow_mo=slow_mo)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser, frontend_url):
    """Fresh browser context per test."""
    context = browser.new_context(base_url=frontend_url)
    yield context
    context.close()


@pytest.fixture()
def page(context):
    """Fresh page per test."""
    page = context.new_page()
    yield page
    page.close()
