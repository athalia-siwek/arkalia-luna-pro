import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import toml

from modules.zeroia.utils.state_writer import check_health

STATE_PATH = Path("modules/zeroia/state/zeroia_state.toml")


def test_healthcheck_active(tmp_path) -> None:
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
        [sys.executable, "modules/zeroia/healthcheck_zeroia.py"],
        env={**os.environ, "ZEROIA_STATE_PATH": str(path)},
        capture_output=True,
        text=True,
        shell=False,
    )

    assert result.returncode == 0
    assert "✅" in result.stdout


def test_healthcheck_inactive(tmp_path) -> None:
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
        [sys.executable, "modules/zeroia/healthcheck_zeroia.py"],
        env={**os.environ, "ZEROIA_STATE_PATH": str(path)},
        capture_output=True,
        text=True,
        shell=False,
    )

    assert result.returncode == 1
    assert "❌" in result.stdout


def test_healthcheck_missing(tmp_path) -> None:
    path = tmp_path / "zeroia_state.toml"  # Ne pas créer le fichier

    result = subprocess.run(
        [sys.executable, "modules/zeroia/healthcheck_zeroia.py"],
        env={**os.environ, "ZEROIA_STATE_PATH": str(path)},
        capture_output=True,
        text=True,
        shell=False,
    )

    assert result.returncode == 1
    assert "❌ Fichier zeroia_state.toml manquant." in result.stdout


@pytest.mark.parametrize(
    "state_data, expected",
    [
        ({"active": True, "decision": {"last_decision": "reduce_load"}}, True),
        ({"active": False, "decision": {"last_decision": "monitor"}}, False),
        ({}, False),
        ({"active": "banana"}, False),
        ({"decision": {}}, False),
    ],
)
def test_check_health_various_states(tmp_path, state_data, expected) -> None:
    file = tmp_path / "state.toml"
    file.write_text(toml.dumps(state_data), encoding="utf-8")
    assert check_health(str(file)) == expected


@patch.dict(os.environ, {"FORCE_ZEROIA_OK": "1"})
def test_healthcheck_passes_forced() -> None:
    assert check_health(str(STATE_PATH)) is True
