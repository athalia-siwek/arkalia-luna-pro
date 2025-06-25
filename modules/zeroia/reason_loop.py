import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import toml

from modules.zeroia.adaptive_thresholds import should_lower_cpu_threshold

# === Chemins par défaut ===
CTX_PATH = Path("state/global_context.toml")
REFLEXIA_STATE = Path("state/reflexia_state.toml")
LOG_PATH = Path("modules/zeroia/logs/zeroia.log")
STATE_PATH = Path("modules/zeroia/state/zeroia_state.toml")
DASHBOARD_PATH = Path("state/zeroia_dashboard.json")
CONTRADICTION_LOG = Path("modules/zeroia/logs/zeroia_contradictions.log")


# === Chargements TOML robustes ===
def load_toml(path: Path) -> dict:
    try:
        if not path.exists() or path.read_text().strip() == "":
            raise ValueError(f"TOML file {path} is empty or missing")
        return toml.load(path)
    except toml.TomlDecodeError as e:
        print(f"[DEBUG] TOML Decode Error: {e}")  # Log pour vérifier l'exception
        raise ValueError(f"Invalid TOML format in {path}: {e}")
    except Exception as e:
        print(f"[DEBUG] General Error: {e}")  # Log pour vérifier l'exception
        raise ValueError(f"Failed to load TOML file {path}: {e}")


def load_context(path: Path = CTX_PATH) -> dict:
    return load_toml(path)


def load_reflexia_state(path: Path = REFLEXIA_STATE) -> dict:
    return load_toml(path)


# === Décision IA ===
def decide(context: dict) -> tuple[str, float]:
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
    return "normal", 0.4


# === Création dossier si besoin ===
def ensure_parent_dir(path: Path) -> None:
    (path.parent if path.suffix else path).mkdir(parents=True, exist_ok=True)


# === Persistance TOML ===
def persist_state(
    decision: str,
    score: float,
    ctx: dict,
    state_path_override: Optional[Path] = None,
) -> None:
    reflexia_summary = ctx.get("reflexia", {})
    status = ctx.get("status", {})
    cpu = status.get("cpu", "N/A")
    severity = status.get("severity", "none")

    state_path = state_path_override or STATE_PATH
    ensure_parent_dir(state_path)
    with open(state_path, "w", encoding="utf-8", newline="\n") as f:
        toml.dump(
            {
                "last_decision": decision,
                "confidence_score": score,
                "justification": f"cpu={cpu}, severity={severity}",
                "timestamp": str(datetime.now()),
            },
            f,
        )

    ensure_parent_dir(LOG_PATH)
    with open(LOG_PATH, "a") as f:
        f.write(
            f"{datetime.now()} :: FROM REFLEXIA: {reflexia_summary} | "
            f"CPU={cpu} | SEVERITY={severity} → DECISION = {decision} "
            f"(confidence={score})\n"
        )


# === Dashboard JSON externe ===
def update_dashboard(
    decision: str,
    score: float,
    ctx: dict,
    dashboard_path_override: Optional[Path] = None,
) -> None:
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
        f.write("\n")


# === Détection contradiction IA ===
def check_for_ia_conflict(
    reflexia_state_path: Path = REFLEXIA_STATE,
    zeroia_state_path: Path = STATE_PATH,
    log_path_override: Optional[Path] = None,
) -> None:
    reflexia_state = load_toml(reflexia_state_path)
    zeroia_state = load_toml(zeroia_state_path)

    reflexia_decision = reflexia_state.get("last_decision", "unknown")
    zeroia_decision = zeroia_state.get("last_decision", "unknown")

    if reflexia_decision != zeroia_decision:
        contradiction_log = log_path_override or CONTRADICTION_LOG
        ensure_parent_dir(contradiction_log)
        with open(contradiction_log, "a") as f:
            f.write(
                f"{datetime.now()} :: CONTRADICTION DETECTED: "
                f"ReflexIA = {reflexia_decision}, ZeroIA = {zeroia_decision}\n"
            )


# === Boucle principale testable ===
def reason_loop(
    context_path: Optional[Path] = None,
    reflexia_path: Optional[Path] = None,
    state_path: Optional[Path] = None,
    dashboard_path: Optional[Path] = None,
    log_path: Optional[Path] = None,
    contradiction_log_path: Optional[Path] = None,
) -> tuple[str, float]:
    ctx = load_context(context_path or CTX_PATH)
    reflexia_data = load_reflexia_state(reflexia_path or REFLEXIA_STATE)

    if not ctx:
        raise ValueError(
            f"Context file {context_path or CTX_PATH} is empty or invalid."
        )

    ctx["reflexia"] = reflexia_data.get("reflexia", {})
    ctx.setdefault("status", {}).update(reflexia_data.get("status", {}))

    if "cpu" not in ctx["status"] or "ram" not in ctx["status"]:
        raise KeyError(
            "Missing required keys in context: 'cpu' and 'ram' must be present."
        )

    cpu = ctx.get("status", {}).get("cpu", 0)
    decision, score = decide(ctx)
    persist_state(decision, score, ctx, state_path)
    update_dashboard(decision, score, ctx, dashboard_path)
    check_for_ia_conflict(
        reflexia_path or REFLEXIA_STATE,
        state_path or STATE_PATH,
        contradiction_log_path,
    )

    print(f"CPU usage: {str(cpu)}%")
    return decision, score


# === Lancement CLI ===
def main():
    print("🟢 ZeroIA loop started successfully")
    decision, score = reason_loop()
    print(f"ZeroIA decided: {decision} (confidence={score})")


if __name__ == "__main__":
    main()
