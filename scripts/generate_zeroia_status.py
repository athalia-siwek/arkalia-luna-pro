# scripts/generate_zeroia_status.py

import datetime
import os
import subprocess  # nosec
import sys
from pathlib import Path

OUTPUT_FILE = "docs/logs/zeroia_status.md"


def get_container_logs(container_name: str, tail: int = 50) -> str:
    try:
        logs = subprocess.check_output(
            ["docker", "logs", container_name, "--tail", str(tail)],
            stderr=subprocess.DEVNULL,
        )  # nosec
        return logs.decode("utf-8", errors="ignore")
    except subprocess.CalledProcessError:
        return ""


def get_container_status(container_name: str) -> str:
    try:
        status = subprocess.check_output(
            ["docker", "inspect", "-f", "{{.State.Status}}", container_name]
        )  # nosec
        return status.decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return "unknown"


def parse_decisions(logs: str) -> list[str]:
    lines = logs.splitlines()
    return [line.strip() for line in lines if "ZeroIA decided" in line]


def write_markdown(status: str, decisions: list[str]) -> None:
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# 🤖 ZeroIA — Statut automatique\n\n")
        f.write(f"- 🕰️ Dernière mise à jour : `{timestamp}`\n")
        f.write("- 📦 Conteneur : `zeroia`\n")
        f.write(f"- 🔄 Statut Docker : `{status}`\n\n")

        if decisions:
            f.write("## 🧠 Dernières décisions IA\n\n")
            for d in decisions[-10:]:
                f.write(f"- {d}\n")
        else:
            f.write("Aucune décision récente détectée.\n")

    print(f"✅ Statut écrit dans {OUTPUT_FILE}")


def get_file_info(filepath):
    p = Path(filepath)
    if not p.exists():
        return f"- ❌ {filepath} (not found)"
    size = p.stat().st_size
    mtime = datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime(
        "%Y-%m-%d %H:%M"
    )
    return f"- ✅ `{filepath}` — **{size} bytes**, modifié le *{mtime}*"


def main():
    container = "zeroia"
    if not os.path.exists("docs/logs"):
        os.makedirs("docs/logs")

    status = get_container_status(container)
    logs = get_container_logs(container, tail=100)
    decisions = parse_decisions(logs)

    if not logs:
        print("❌ Impossible de récupérer les logs de ZeroIA.")
        sys.exit(1)

    write_markdown(status, decisions)


if __name__ == "__main__":
    main()
