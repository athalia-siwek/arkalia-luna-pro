import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import toml

from modules.zeroia.adaptive_thresholds import should_lower_cpu_threshold

# === Chemins relatifs depuis /app ===
CTX_PATH = Path("state/global_context.toml")
REFLEXIA_STATE = Path("state/reflexia_state.toml")
LOG_PATH = Path("modules/zeroia/logs/zeroia.log")
STATE_PATH = Path("modules/zeroia/state/zeroia_state.toml")
DASHBOARD_PATH = Path("state/zeroia_dashboard.json")
CONTRADICTION_LOG = Path("modules/zeroia/logs/zeroia_contradictions.log")


# === Chargement TOML sécurisé ===
def load_toml(path: Path) -> dict:
    return toml.load(path) if path.exists() else {}


# === Chargement des contextes ===
def load_context():
    return load_toml(CTX_PATH)


def load_reflexia_state():
    return load_toml(REFLEXIA_STATE)


# === Décision logique IA ===
def decide(context):
    status = context.get("status", {})
    severity = status.get("severity", "none")
    cpu = status.get("cpu", 0)

    if should_lower_cpu_threshold() and cpu > 70:
        return "reduce_load", 0.75
    if severity == "critical":
        return "emergency_shutdown", 1.0
    elif cpu > 80:
        return "reduce_load", 0.8
    elif cpu > 60:
        return "monitor", 0.6
    else:
        return "normal", 0.4


# === Création dossier parent si besoin ===
def ensure_parent_dir(path: Path):
    if path.suffix:  # Fichier
        path.parent.mkdir(parents=True, exist_ok=True)
    else:  # Dossier
        path.mkdir(parents=True, exist_ok=True)


# === Persistance état IA ===
def persist_state(decision, score, ctx, state_path_override: Optional[Path] = None):
    reflexia_summary = ctx.get("reflexia", {})
    status = ctx.get("status", {})
    cpu = status.get("cpu", "N/A")
    severity = status.get("severity", "none")

    ensure_parent_dir(LOG_PATH)
    with open(LOG_PATH, "a") as f:
        f.write(
            f"{datetime.now()} :: FROM REFLEXIA: {reflexia_summary} | "
            f"CPU={cpu} | SEVERITY={severity} → DECISION = {decision} "
            f"(confidence={score})\n"
        )

    state_path = state_path_override or STATE_PATH
    ensure_parent_dir(state_path)
    with open(state_path, "w") as f:
        toml.dump(
            {
                "last_decision": decision,
                "confidence_score": score,
                "justification": f"cpu={cpu}, severity={severity}",
                "timestamp": str(datetime.now()),
            },
            f,
        )


# === Écriture dashboard JSON externe ===
def update_dashboard(
    decision, score, ctx, dashboard_path_override: Optional[Path] = None
):
    dashboard_path = dashboard_path_override or DASHBOARD_PATH
    ensure_parent_dir(dashboard_path)
    dashboard = {
        "last_decision": decision,
        "confidence": score,
        "reasoning_loop_active": True,
        "connected_modules": ["reflexia"],
        "previous": ["reduce_load", "monitor", "monitor"],
        "last_updated": str(datetime.now()),
    }
    with open(dashboard_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)
        f.write("\n")  # 👈 Corrige définitivement le problème de EOF manquant


# === Détection de contradiction ReflexIA vs ZeroIA ===
def check_for_ia_conflict(log_path_override: Optional[Path] = None):
    reflexia_state = load_toml(REFLEXIA_STATE)
    zeroia_state = load_toml(STATE_PATH)

    reflexia_decision = reflexia_state.get("last_decision", "unknown")
    zeroia_decision = zeroia_state.get("last_decision", "unknown")

    if reflexia_decision != zeroia_decision:
        contradiction_log_path = log_path_override or CONTRADICTION_LOG
        ensure_parent_dir(contradiction_log_path)
        with open(contradiction_log_path, "a") as f:
            f.write(
                f"{datetime.now()} :: CONTRADICTION DETECTED: "
                f"ReflexIA = {reflexia_decision}, ZeroIA = {zeroia_decision}\n"
            )


# === Boucle principale ===
def main():
    print("🟢 ZeroIA loop started successfully")
    ctx = load_context()
    reflexia_data = load_reflexia_state()

    ctx["reflexia"] = reflexia_data.get("reflexia", {})
    ctx.setdefault("status", {}).update(reflexia_data.get("status", {}))

    decision, score = decide(ctx)
    persist_state(decision, score, ctx)
    update_dashboard(decision, score, ctx)
    check_for_ia_conflict()

    print(f"ZeroIA decided: {decision} (confidence={score})")


if __name__ == "__main__":
    main()
