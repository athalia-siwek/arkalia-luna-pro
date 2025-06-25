#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ROOT / "modules"
ENV_FILE = ROOT / ".env"


def ensure_init_py():
    init_path = MODULES / "__init__.py"
    if not init_path.exists():
        init_path.touch()
        print(f"✅ Créé : {init_path}")
    else:
        print(f"✔️ Déjà présent : {init_path}")


def ensure_env_py_path():
    if ENV_FILE.exists():
        content = ENV_FILE.read_text()
        if "PYTHONPATH" in content:
            print("✔️ PYTHONPATH déjà présent dans .env")
            return
    with open(ENV_FILE, "a") as f:
        f.write("\nPYTHONPATH=./modules\n")
    print(f"✅ PYTHONPATH ajouté à {ENV_FILE}")


def main():
    print("🔧 Patch Pyright / Cursor en cours…")
    ensure_init_py()
    ensure_env_py_path()
    print("✅ Terminé. Recharge Cursor (⇧⌘P > Reload Window)")


if __name__ == "__main__":
    main()
