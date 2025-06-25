# scripts/print_sys_path.py

import sys
from pathlib import Path

print("📂 PYTHON sys.path (chemins d'import):\n" + "=" * 40)
for path in sys.path:
    print(f"- {path}")

print("\n📌 Projet détecté ici :", Path(__file__).resolve().parent.parent)
