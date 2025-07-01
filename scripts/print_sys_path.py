# scripts/print_sys_path.py

from core.ark_logger import ark_logger
import sys
from pathlib import Path

ark_logger.info("📂 PYTHON sys.path (chemins d'import, extra={"module": "scripts"}):\n" + "=" * 40)
for path in sys.path:
    ark_logger.info(f"- {path}", extra={"module": "scripts"})

ark_logger.info("\n📌 Projet détecté ici :", Path(__file__, extra={"module": "scripts"}).resolve().parent.parent)
