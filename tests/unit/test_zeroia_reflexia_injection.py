from pathlib import Path

from modules.zeroia.reason_loop import reason_loop
from tests.unit.test_helpers import ensure_test_toml, ensure_zeroia_state_file

ensure_test_toml()


def test_reflexia_injection_merges_into_context(tmp_path: Path):
    """🧪 Vérifie que ReflexIA injecte ses données dans un contexte vide."""
    ctx_path = tmp_path / "ctx.toml"
    reflexia_path = tmp_path / "reflexia.toml"

    # 🧪 Contexte minimal
    ctx_path.write_text("[status]\n")

    # 🧠 ReflexIA injecte CPU + RAM + insight
    reflexia_path.write_text(
        """
        [status]
        cpu = 84
        ram = 72

        [reflexia]
        insight = "reflexia active"
    """
    )

    # 🔁 Lancement simulé avec injection
    decision, score = reason_loop(context_path=ctx_path, reflexia_path=reflexia_path)

    # ✅ Le résultat doit être logique
    assert decision == "reduce_load"
    assert 0.7 <= score <= 0.8  # 🧪 Acceptable selon should_lower_cpu_threshold()

    ensure_zeroia_state_file()
