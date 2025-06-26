# tests/unit/test_healthcheck.py

import os
import subprocess
from pathlib import Path

import pytest
import toml

from modules.zeroia.utils.state_writer import check_health

STATE_PATH = Path("modules/zeroia/state/zeroia_state.toml")


def test_healthcheck_active(tmp_path):
    path = tmp_path / "zeroia_state.toml"
    path.write_text(
        """
active = true

[decision]
last_decision = "reduce_load"
""",
        encoding="utf-8",
    )

    result = subprocess.run(
        ["python", "modules/zeroia/healthcheck_zeroia.py"],
        env={**dict(**os.environ, ZEROIA_STATE_PATH=str(path))},
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "✅" in result.stdout


def test_healthcheck_inactive(tmp_path):
    path = tmp_path / "zeroia_state.toml"
    path.write_text(
        """
active = false

[decision]
last_decision = "monitor"
""",
        encoding="utf-8",
    )

    result = subprocess.run(
        ["python", "modules/zeroia/healthcheck_zeroia.py"],
        env={**dict(**os.environ, ZEROIA_STATE_PATH=str(path))},
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "❌" in result.stdout


def test_healthcheck_missing(tmp_path):
    # Chemin inexistant
    path = tmp_path / "zeroia_state.toml"

    result = subprocess.run(
        ["python", "modules/zeroia/healthcheck_zeroia.py"],
        env={**dict(**os.environ, ZEROIA_STATE_PATH=str(path))},
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "❌ Fichier zeroia_state.toml manquant." in result.stdout


@pytest.mark.parametrize(
    "state_data, expected",
    [
        (
            {"active": True, "decision": {"last_decision": "reduce_load"}},
            True,
        ),  # ✅ Actif
        (
            {"active": False, "decision": {"last_decision": "monitor"}},
            False,
        ),  # ❌ Inactif
        ({}, False),  # 💥 Clé manquante
        ({"active": "banana"}, False),  # 🔥 Corruption logique
        ({"decision": {}}, False),  # 🔧 Clé présente mais pas de 'active'
    ],
)
def test_check_health_various_states(tmp_path, state_data, expected):
    file = tmp_path / "state.toml"
    file.write_text(toml.dumps(state_data), encoding="utf-8")
    assert check_health(str(file)) == expected
