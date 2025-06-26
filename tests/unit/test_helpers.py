# 📄 tests/unit/test_helpers.py

from pathlib import Path


def ensure_test_toml():
    """
    Crée un fichier TOML de test minimal pour éviter les erreurs liées
    aux fichiers manquants ou vides dans les tests ZeroIA.
    """
    path = Path("modules/zeroia/state/zeroia_state.toml")
    if not path.exists() or path.read_text().strip() == "":
        path.write_text(
            """
[status]
active = true
confidence = 0.9

[decision]
goal = "observe"
context = "reflexia"
            """.strip()
        )


def ensure_zeroia_state_file():
    path = Path("modules/zeroia/state/zeroia_state.toml")
    if not path.exists() or path.read_text().strip() == "":
        path.write_text(
            """
[status]
active = true
confidence = 0.93

[decision]
goal = "observe"
context = "reflexia"
""".strip()
        )
