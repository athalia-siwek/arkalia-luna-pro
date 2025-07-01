"""
ZeroIA Orchestrator Enhanced - Version Modernisée (Test-Safe)
Utilise la boucle Enhanced avec Error Recovery et optimisations performance
"""

from core.ark_logger import ark_logger
import time

from modules.zeroia.reason_loop_enhanced import reason_loop_enhanced_with_recovery


# Alias pour compatibilité tests - doit pointer vers la vraie fonction mockée
def reason_loop():
    """Alias pour les tests qui mockent reason_loop"""
    return reason_loop_enhanced_with_recovery()


# Alias de compatibilité pour les tests
reason_loop_enhanced = reason_loop_enhanced_with_recovery


def orchestrate_zeroia_loop(max_loops: int | None = 3) -> None:
    """
    Orchestre la boucle ZeroIA Enhanced avec Error Recovery.

    Args:
        max_loops: Nombre maximum de boucles (défaut: 3 pour tests, None = infini pour prod)
    """
    count = 0
    while True:
        try:
            # Les tests attendent ce format exact
            decision, score = reason_loop_enhanced_with_recovery()
            ark_logger.debug(f"[DEBUG] Decision: {decision} / Score: {score}", extra={"module": "zeroia"})

            if max_loops and count >= max_loops:
                ark_logger.debug(f"[DEBUG] Max loop reached ({max_loops}, extra={"module": "zeroia"}). Exiting.")
                break
            count += 1

        except Exception as e:
            ark_logger.error(f"[ERROR] An error occurred in the reason loop: {e}", extra={"module": "zeroia"})
            break  # Sortir en cas d'erreur pour éviter boucle infinie
        time.sleep(0.1)  # Réduire le sleep pour les tests


def orchestrate_zeroia_production(max_loops: int | None = None) -> None:
    """Version production avec boucle infinie pour containers"""
    orchestrate_zeroia_loop(max_loops=max_loops)


if __name__ == "__main__":
    # En mode script, utiliser la version production
    orchestrate_zeroia_production()
