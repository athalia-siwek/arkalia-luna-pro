# 📄 tests/unit/test_zeroia_decision_basic.py

from pathlib import Path

import pytest

from modules.zeroia.reason_loop import decide, load_toml


def test_decide_high_cpu():
    """⚠️ CPU > 80 → reduce_load"""
    context = {"status": {"cpu": 91}}
    assert decide(context)[0] == "reduce_load"


def test_decide_medium_cpu():
    """🟠 CPU entre 60 et 80 → reduce_load"""
    context = {"status": {"cpu": 72}}
    assert decide(context)[0] == "reduce_load"


def test_decide_low_cpu():
    """🟢 CPU < 60 → normal"""
    context = {"status": {"cpu": 45}}
    assert decide(context)[0] == "normal"


def test_decide_critical():
    """🔴 Cas critique explicite → emergency_shutdown"""
    context = {"status": {"severity": "critical"}}
    assert decide(context)[0] == "emergency_shutdown"


def test_decide_no_status():
    """🟢 Pas d'infos → fallback safe"""
    context = {}
    assert decide(context)[0] == "normal"


def test_toml_parsing_error(tmp_path: Path):
    """💥 Charge un fichier TOML invalide → erreur captée"""
    broken_file = tmp_path / "broken.toml"
    broken_file.write_text("[status\nseverity = 'critical'")  # TOML invalide

    with pytest.raises(ValueError, match="Invalid TOML format"):
        load_toml(broken_file)
