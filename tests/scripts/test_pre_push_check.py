import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent


def test_pre_push_zeroia_check_executes_cleanly():
    """Teste que le script pre-push ZeroIA s'exécute sans erreur"""
    result = subprocess.run(
        ["python", "scripts/pre_push_zeroia_check.py"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    # Vérifie que le script s'exécute sans erreur
    assert result.returncode == 0, f"Script a échoué avec code {result.returncode}"

    # Vérifie que la sortie contient les messages attendus
    output = result.stdout
    assert "✅ Fichier TOML valide" in output
    assert "🛡️ Tous les contrôles ZeroIA sont OK" in output
