#!/usr/bin/env python3
# 🧠 tests/unit/sandozia/test_sandozia_core_enhanced.py
# Tests pour modules/sandozia/core.py (imports corrigés)

import asyncio
import importlib.util
import sys
from pathlib import Path

import pytest

# Ajout dynamique du module sandozia.core
core_path = Path(__file__).resolve().parents[3] / "modules" / "sandozia" / "core.py"
spec = importlib.util.spec_from_file_location("sandozia.core", str(core_path))
if spec is not None and spec.loader is not None:
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    UsandoziaConfig = core.UsandoziaConfig
    UsandoziaCore = core.UsandoziaCore
    default_config = core.default_config
    default_core = core.default_core
    main = core.main
else:
    raise ImportError(f"Impossible d'importer le module sandozia.core depuis {core_path}")


def test_usandozia_config_default_values():
    config = UsandoziaConfig()
    assert config.enabled is True
    assert config.debug_mode is False
    assert config.max_retries == 3
    assert config.timeout == 30.0


def test_usandozia_config_custom_values():
    config = UsandoziaConfig(enabled=False, debug_mode=True, max_retries=5, timeout=60.0)
    assert config.enabled is False
    assert config.debug_mode is True
    assert config.max_retries == 5
    assert config.timeout == 60.0


def test_usandozia_core_initialization():
    config = UsandoziaConfig()
    core = UsandoziaCore(config)
    assert core.config is config
    assert hasattr(core, "logger")


def test_usandozia_core_health_check():
    config = UsandoziaConfig()
    core = UsandoziaCore(config)
    health = core.health_check()
    assert health["module"] == "sandozia"
    assert health["status"] == "healthy"
    assert health["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_usandozia_core_process():
    config = UsandoziaConfig()
    core = UsandoziaCore(config)
    data = {"test": "data"}
    result = await core.process(data)
    assert result["status"] == "success"
    assert result["data"] == data
    assert result["module"] == "sandozia"


def test_default_config_and_core():
    assert isinstance(default_config, UsandoziaConfig)
    assert isinstance(default_core, UsandoziaCore)


@pytest.mark.asyncio
async def test_main_function(monkeypatch):
    # On vérifie que main() s'exécute sans erreur
    monkeypatch.setattr("builtins.print", lambda *a, **k: None)
    await main()
