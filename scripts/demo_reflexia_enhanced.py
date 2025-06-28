#!/usr/bin/env python3
# 🧠 scripts/demo_reflexia_enhanced.py
"""
Demo Reflexia Enhanced v2.6.0

Test de la nouvelle version avec vraies métriques système
"""

import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.reflexia.logic.main_loop_enhanced import reflexia_loop_enhanced


def main():
    print("🧠 === DEMO REFLEXIA ENHANCED v2.6.0 ===")
    print("   Vraies métriques système + containers Docker")
    print("   Test avec 3 cycles, pause 3s entre chaque\n")

    try:
        reflexia_loop_enhanced(max_iterations=3, sleep_seconds=3, verbose=True)
        print("\n✅ Demo Reflexia Enhanced terminé avec succès !")

    except KeyboardInterrupt:
        print("\n🛑 Demo interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur demo: {e}")


if __name__ == "__main__":
    main()
