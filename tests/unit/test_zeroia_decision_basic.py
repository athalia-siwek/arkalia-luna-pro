# 📄 tests/unit/test_zeroia_decision_basic.py

from pathlib import Path

import pytest

from modules.zeroia.reason_loop import decide, load_toml


def test_decide_high_cpu():
    """⚠️ CPU > 80 → reduce_load"""
    context = {"status": {"cpu": 91}}
    decision, _ = decide(context)
    assert decision == "reduce_load"


def test_decide_medium_cpu():
    """🟠 CPU entre 60 et 80 → reduce_load"""
    context = {"status": {"cpu": 72}}
    decision, _ = decide(context)
    assert decision == "reduce_load"


def test_decide_low_cpu():
    """🟢 CPU < 60 → normal"""
    context = {"status": {"cpu": 45}}
    decision, _ = decide(context)
    assert decision == "normal"


def test_decide_critical():
    """🔴 Cas critique explicite → emergency_shutdown"""
    context = {"status": {"severity": "critical"}}
    decision, _ = decide(context)
    assert decision == "emergency_shutdown"


def test_decide_no_status():
    """🟢 Pas d'infos → fallback safe"""
    context = {}
    decision, _ = decide(context)
    assert decision == "normal"


def test_toml_parsing_error(tmp_path: Path):
    """💥 Charge un fichier TOML invalide → erreur captée"""
    broken_file = tmp_path / "broken.toml"
    broken_file.write_text("[status\nseverity = 'critical'")  # TOML invalide

    with pytest.raises(ValueError, match=r"Invalid TOML format"):
        load_toml(broken_file)
