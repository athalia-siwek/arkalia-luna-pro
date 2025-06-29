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

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from modules.reflexia.logic.main_loop_enhanced import reflexia_loop_enhanced
except ImportError as e:
    print(f"❌ Erreur import Reflexia Enhanced: {e}")
    print("💡 Vérifier que le module reflexia est installé")
    sys.exit(1)


def format_generated():
    """Formate tous les dossiers generated avec isort + black."""
    for d in pathlib.Path(".").rglob("generated"):
        try:
            # Tri des imports avec isort (compatible black)
            subprocess.run(["isort", str(d), "--profile", "black"], check=True)
            # Formatage du code avec black
            subprocess.run(["black", str(d), "--quiet"], check=True)
            print(f"✅ Formaté: {d}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Erreur formatage {d}: {e}")
            # Fallback: essayer au moins isort
            try:
                subprocess.run(["isort", str(d), "--fix"], check=False)
                print(f"⚠️ Fallback isort appliqué: {d}")
            except Exception:
                print(f"❌ Fallback échoué: {d}")


def main():
    print("🧠 === DEMO REFLEXIA ENHANCED v2.6.0 ===")
    print("   Vraies métriques système + containers Docker")
    print("   Test avec 3 cycles, pause 3s entre chaque\n")

    try:
        reflexia_loop_enhanced(max_iterations=3, sleep_seconds=3, verbose=True)
        print("\n✅ Demo Reflexia Enhanced terminé avec succès !")
        format_generated()

    except KeyboardInterrupt:
        print("\n🛑 Demo interrompu par l'utilisateur")
    except ImportError as e:
        print(f"\n❌ Erreur import: {e}")
        print("💡 Vérifier les dépendances Reflexia")
    except Exception as e:
        print(f"\n❌ Erreur demo: {e}")
        print("💡 Vérifier la configuration Reflexia")


if __name__ == "__main__":
    main()
