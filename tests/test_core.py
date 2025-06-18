# tests/test_core.py

from core import app  # core/__init__.py ou core.py doit exposer `app`


def test_app_exists():
    assert app is not None
