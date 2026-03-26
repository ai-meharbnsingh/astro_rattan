"""
Fresh install verification tests.
Ensures the project can be set up from scratch.
"""
import os
import importlib


def test_requirements_file_exists():
    """requirements.txt must exist in project root."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    req_path = os.path.join(project_root, "requirements.txt")
    assert os.path.isfile(req_path), f"requirements.txt not found at {req_path}"


def test_all_imports_resolve():
    """All app modules must be importable."""
    modules = [
        "app.config",
        "app.database",
        "app.models",
        "app.auth",
        "app.astro_iogita_engine",
    ]
    for mod in modules:
        try:
            importlib.import_module(mod)
        except ImportError as e:
            raise AssertionError(f"Failed to import {mod}: {e}")


def test_app_starts():
    """FastAPI app must be importable and have routes."""
    from app.main import app
    assert app is not None
    assert len(app.routes) > 0, "App has no routes"
