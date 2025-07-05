from pathlib import Path

import pytest
import toml

from core.ark_logger import ark_logger
from modules.zeroia.reason_loop import check_for_ia_conflict


def write_toml(path: Path, content: dict) -> None:
    with open(path, "w") as f:
        toml.dump(content, f)


def test_contradiction_detection(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Simule une divergence de décision entre ReflexIA et ZeroIA,
    et vérifie la détection + création du log de contradiction.
    """
    reflexia_path = tmp_path / "reflexia_state.toml"
    zeroia_path = tmp_path / "zeroia_state.toml"
    contradiction_log = tmp_path / "zeroia_contradictions.log"

    # 💡 Génère contenu TOML valide AVEC bloc [decision]
    toml.dump({"decision": {"last_decision": "observe"}}, reflexia_path.open("w"))
    toml.dump({"decision": {"last_decision": "shutdown"}}, zeroia_path.open("w"))

    # 🔁 Et ajoute (si manquant) :
    assert reflexia_path.read_text()
    assert zeroia_path.read_text()

    # Test simple de la fonction sans patcher les constantes
    ark_logger.debug(
        f"[DEBUG] Checking for IA conflict with log path: {contradiction_log}",
        extra={"module": "zeroia"},
    )
    check_for_ia_conflict(
        reflexia_decision="decision1",
        zeroia_decision="decision2",
        log_path=contradiction_log,
    )

    # Et ajuste ce bout final :
    assert contradiction_log.exists(), "The contradiction log file was not created."
    assert "CONTRADICTION DETECTÉE" in contradiction_log.read_text().upper()
