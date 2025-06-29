import json
import subprocess
import sys
from pathlib import Path

STATE_FILE = Path("modules/reflexia/state/reflexia_state.json")


def setup_module(module) -> None:
    # Crée un état mock de ReflexIA
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "loop_active": True,
        "last_decision": "observe",
        "timestamp": "2025-06-26T09:59:00",
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def teardown_module(module) -> None:
    # Nettoie le fichier mock après test
    if STATE_FILE.exists():
        STATE_FILE.unlink()


def test_reflexia_monitor_runs() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/reflexia_monitor.py"],
        capture_output=True,
        text=True,
        check=True,
        shell=False,
    )
    output = result.stdout
    assert "ReflexIA Status Monitor" in output
    assert "Dernière décision" in output
    assert "Boucle active" in output
    assert "mise à jour" in output
