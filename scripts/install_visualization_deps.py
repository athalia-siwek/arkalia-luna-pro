#!/usr/bin/env python3
"""
📊 Installation des dépendances de visualisation Arkalia-LUNA
Installe les packages nécessaires pour les graphiques et dashboards
"""

import subprocess
import sys
from pathlib import Path


def install_package(package: str) -> bool:
    """Installe un package avec pip"""
    try:
        print(f"📦 Installation de {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installé avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur installation {package}: {e}")
        return False


def main():
    """Installe toutes les dépendances de visualisation"""
    print("🌕 Installation des dépendances de visualisation Arkalia-LUNA...")

    # Packages de visualisation
    packages = [
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.15.0",
        "kaleido>=0.2.1",  # Pour export PNG de Plotly
        "jupyter>=1.0.0",
        "ipywidgets>=8.0.0",
    ]

    success_count = 0
    total_count = len(packages)

    for package in packages:
        if install_package(package):
            success_count += 1

    print(f"\n📊 Résumé: {success_count}/{total_count} packages installés")

    if success_count == total_count:
        print("🎉 Toutes les dépendances installées avec succès !")
        print("\n🚀 Vous pouvez maintenant utiliser:")
        print("   python3 scripts/arkalia_visualizations.py")
        return True
    else:
        print("⚠️ Certains packages n'ont pas pu être installés")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
