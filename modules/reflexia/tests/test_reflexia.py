# modules/reflexia/tests/test_reflexia.py

import toml

from modules.reflexia.core import monitor_status


def test_monitor_status():
    assert monitor_status({"cpu": 95}) == "🛑 surcharge CPU"
    assert monitor_status({"memory": 85}) == "⚠️ haute mémoire"
    assert monitor_status({"cpu": 30, "memory": 40}) == "✅ stable"


def test_reflexia_metrics_logging(tmp_path):
    state_path = tmp_path / "reflexia_state.toml"
    # Simuler l'initialisation de Reflexia et l'écriture dans le fichier TOML
    metrics = {"cpu": 70, "memory": 60}
    with state_path.open("w") as f:
        toml.dump(metrics, f)

    # Lire le fichier et vérifier le contenu
    with state_path.open("r") as f:
        loaded_metrics = toml.load(f)

    assert loaded_metrics == metrics
