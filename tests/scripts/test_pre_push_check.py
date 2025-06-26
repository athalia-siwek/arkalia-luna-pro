import subprocess
import sys


def test_pre_push_zeroia_check_executes_cleanly():
    """
    Vérifie que le script pre_push_zeroia_check.py s'exécute sans crash
    et affiche un message de fin cohérent.
    """
    result = subprocess.run(
        [sys.executable, "scripts/pre_push_zeroia_check.py"],
        capture_output=True,
        text=True,
        check=True,
        shell=False,
    )

    # 🧪 Vérifie que le script a bien terminé (code 0 ou géré)
    assert result.returncode in [
        0,
        1,
    ], f"Code retour inattendu : {result.returncode}\nSTDERR:\n{result.stderr}"

    # ✅ Vérifie que la sortie contient un indicateur de succès ou d'erreur contrôlée
    assert (
        "ZeroIA Pre-Push Check Complete" in result.stdout or "Erreur" in result.stdout
    ), f"Sortie inattendue :\n{result.stdout}"
