import pytest

from modules.zeroia.reason_loop import decide, load_context, load_reflexia_state


def test_zeroia_self_contradiction():
    """
    Teste si ZeroIA et Reflexia divergent logiquement.
    """
    context = load_context()
    reflexia_state = load_reflexia_state()

    # Simule l'intégration des données de Reflexia dans le contexte de ZeroIA
    context["reflexia"] = reflexia_state.get("reflexia", {})
    context.setdefault("status", {}).update(reflexia_state.get("status", {}))

    decision, score = decide(context)

    # Exemple de logique de test :
    # Si Reflexia indique une sévérité critique, ZeroIA ne devrait pas être en mode
    # "normal"
    assert decision != "normal", (
        "ZeroIA ne devrait pas être en mode normal lorsque Reflexia signale "
        "une sévérité critique."
    )

    # Ajoutez d'autres assertions selon les besoins pour détecter les contradictions


if __name__ == "__main__":
    pytest.main(["-v", __file__])
