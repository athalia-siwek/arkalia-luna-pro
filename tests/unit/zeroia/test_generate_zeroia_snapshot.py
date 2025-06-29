# 📄 tests/unit/test_generate_zeroia_snapshot.py

from pathlib import Path

import toml

from modules.zeroia.snapshot_generator import generate_snapshot


def test_snapshot_generation(tmp_path: Path) -> None:
    # 🧪 Création d’un état minimal de ZeroIA
    state_data = {
        "inputs": {
            "reflexia_last_decision": "monitor",
            "zeroia_last_decision": "reduce_load",
        },
        "decision": {
            "last_decision": "reduce_load",
            "confidence_score": 0.75,
            "justification": "cpu=72.1, severity=warning",
            "timestamp": "2025-06-26 01:17:43.861556",
        },
        "timestamp": "2025-06-26 01:17:43",
    }

    # 📂 Fichier source simulé
    input_file = tmp_path / "zeroia_state.toml"
    toml.dump(state_data, input_file.open("w"))

    # 📂 Fichier snapshot cible
    output_file = tmp_path / "snapshot.toml"

    # ⚙️ Génération snapshot
    result = generate_snapshot(input_path=input_file, output_path=output_file)

    # ✅ Assertions robustes
    assert result is True
    assert output_file.exists()

    snapshot_data = toml.load(output_file)
    assert "inputs" in snapshot_data
    assert "decision" in snapshot_data
    assert "timestamp" in snapshot_data
    assert "snapshot_time" in snapshot_data
