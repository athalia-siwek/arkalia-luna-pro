"""Tests pour core/core.py"""

from core.core import TestCore


def test_core_initialization() -> None:
    """Test de l'initialisation de TestCore"""
    core = TestCore()
    assert isinstance(core, TestCore)


def test_basic_functionality() -> None:
    """Test de la fonctionnalité de base"""
    core = TestCore()
    assert core.basic_functionality() is True
