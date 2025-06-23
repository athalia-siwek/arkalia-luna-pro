#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎛️ Lancement direct de la boucle ReflexIA

Ce script exécute la boucle réflexive complète (collecte des métriques,
décision adaptative, sauvegarde du snapshot) via le cœur du module `reflexia`.

💡 Usage :
    python run_reflexia.py
"""

from modules.reflexia.core import launch_reflexia_loop

if __name__ == "__main__":
    launch_reflexia_loop()