#!/usr/bin/env python3
# 🧠 scripts/demo_reflexia_enhanced.py
"""
Demo Reflexia Enhanced v2.6.0

Test de la nouvelle version avec vraies métriques système
"""

import pathlib
import subprocess
import sys
from pathlib import Path

from core.ark_logger import ark_logger

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from modules.reflexia.logic.main_loop_enhanced import reflexia_loop_enhanced
except ImportError as e:
    ark_logger.info(f"❌ Erreur import Reflexia Enhanced: {e}", extra={"module": "scripts"})
    ark_logger.info("💡 Vérifier que le module reflexia est installé", extra={"module": "scripts"})
    sys.exit(1)


def format_generated():
    """Formate tous les dossiers generated avec isort + black."""
    for d in pathlib.Path(".").rglob("generated"):
        try:
            # Tri des imports avec isort (compatible black)
            subprocess.run(["isort", str(d), "--profile", "black"], check=True)
            # Formatage du code avec black
            subprocess.run(["black", str(d), "--quiet"], check=True)
            ark_logger.info(f"✅ Formaté: {d}", extra={"module": "scripts"})
        except subprocess.CalledProcessError as e:
            ark_logger.info(f"⚠️ Erreur formatage {d}: {e}", extra={"module": "scripts"})
            # Fallback: essayer au moins isort
            try:
                subprocess.run(["isort", str(d), "--fix"], check=False)
                ark_logger.info(f"⚠️ Fallback isort appliqué: {d}", extra={"module": "scripts"})
            except Exception:
                ark_logger.info(f"❌ Fallback échoué: {d}", extra={"module": "scripts"})


def main() -> None:
    ark_logger.info("🧠 === DEMO REFLEXIA ENHANCED v2.6.0 ===", extra={"module": "scripts"})
    ark_logger.info("   Vraies métriques système + containers Docker", extra={"module": "scripts"})
    ark_logger.info("   Test avec 3 cycles, pause 3s entre chaque\n", extra={"module": "scripts"})

    try:
        reflexia_loop_enhanced(max_iterations=3, sleep_seconds=3, verbose=True)
        ark_logger.info(
            "\n✅ Demo Reflexia Enhanced terminé avec succès !", extra={"module": "scripts"}
        )
        format_generated()

    except KeyboardInterrupt:
        ark_logger.info("\n🛑 Demo interrompu par l'utilisateur", extra={"module": "scripts"})
    except ImportError as e:
        ark_logger.info(f"\n❌ Erreur import: {e}", extra={"module": "scripts"})
        ark_logger.info("💡 Vérifier les dépendances Reflexia", extra={"module": "scripts"})
    except Exception as e:
        raise RuntimeError(f"Erreur demo reflexia enhanced: {e}") from e


if __name__ == "__main__":
    main()
