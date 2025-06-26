import hashlib
import json
import os
from datetime import datetime

import toml


def file_hash(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def save_toml_if_changed(data: dict, target_path: str) -> None:
    tmp_path = f"{target_path}.tmp"
    data_to_hash = data.copy()
    data_to_hash.pop("timestamp", None)

    with open(tmp_path, "w", encoding="utf-8", newline="\n") as f:
        toml.dump(data_to_hash, f)

    if file_hash(tmp_path) != file_hash(target_path):
        os.replace(tmp_path, target_path)
    else:
        os.remove(tmp_path)

    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(target_path, "w", encoding="utf-8", newline="\n") as f:
        toml.dump(data, f)
    with open(target_path, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n")


def save_json_if_changed(data: dict, target_path: str) -> None:
    tmp_path = f"{target_path}.tmp"
    data_to_hash = data.copy()
    data_to_hash.pop("timestamp", None)

    with open(tmp_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data_to_hash, f, indent=2, sort_keys=True)

    if file_hash(tmp_path) != file_hash(target_path):
        os.replace(tmp_path, target_path)
    else:
        os.remove(tmp_path)

    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(target_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    with open(target_path, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n")


def check_health(path: str) -> bool:
    try:
        data = toml.load(path)
        if os.getenv("FORCE_ZEROIA_OK") == "1":
            return True
        return bool(
            data.get("active") is True or data.get("zeroia", {}).get("active") is True
        )
    except (toml.TomlDecodeError, OSError, TypeError):
        return False


def write_state_json(file_path: str, data: dict) -> None:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def load_zeroia_state(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return toml.load(f)


__all__ = [
    "check_health",
    "file_hash",
    "load_zeroia_state",
    "save_json_if_changed",
    "save_toml_if_changed",
    "write_state_json",
]
