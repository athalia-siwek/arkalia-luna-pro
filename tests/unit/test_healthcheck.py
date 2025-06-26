# tests/unit/test_healthcheck.py

import subprocess
from pathlib import Path

import pytest
import toml

from modules.zeroia.utils.state_writer import check_health

STATE_PATH = Path("modules/zeroia/state/zeroia_state.toml")


def test_healthcheck_active(monkeypatch):
    # Simule un état actif
    STATE_PATH.write_text("active = true\n")

    result = subprocess.run(
        ["python", "modules/zeroia/healthcheck_zeroia.py"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "✅" in result.stdout


def test_healthcheck_inactive(monkeypatch):
    # Simule un état inactif
    STATE_PATH.write_text("active = false\n")

    result = subprocess.run(
        ["python", "modules/zeroia/healthcheck_zeroia.py"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "❌" in result.stdout


def test_healthcheck_missing(monkeypatch):
    # Supprime le fichier
    if STATE_PATH.exists():
        STATE_PATH.unlink()

    result = subprocess.run(
        ["python", "modules/zeroia/healthcheck_zeroia.py"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "💥" in result.stdout


@pytest.mark.parametrize(
    "state_data, expected",
    [
        ({"zeroia": {"active": True}}, True),  # ✅ Actif
        ({"zeroia": {"active": False}}, False),  # ❌ Inactif
        ({}, False),  # 💥 Clé manquante
        ({"zeroia": {"active": "banana"}}, False),  # 🔥 Corruption logique
        ({"zeroia": {}}, False),  # 🔧 Clé présente mais vide
    ],
)
def test_check_health_various_states(tmp_path, state_data, expected):
    file = tmp_path / "state.toml"
    file.write_text(toml.dumps(state_data), encoding="utf-8")
    assert check_health(str(file)) == expected
