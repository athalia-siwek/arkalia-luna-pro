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


def save_toml_if_changed(data: dict, target_path: str):
    tmp_path = target_path + ".tmp"
    # Exclure l'horodatage pour le calcul du hachage
    data_to_hash = data.copy()
    data_to_hash.pop("timestamp", None)

    with open(tmp_path, "w", encoding="utf-8", newline="\n") as f:
        toml.dump(data_to_hash, f)

    if file_hash(tmp_path) != file_hash(target_path):
        os.replace(tmp_path, target_path)
    else:
        os.remove(tmp_path)

    # Ajouter l'horodatage après la comparaison
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(target_path, "w", encoding="utf-8", newline="\n") as f:
        toml.dump(data, f)


def save_json_if_changed(data: dict, target_path: str):
    tmp_path = target_path + ".tmp"
    # Exclure l'horodatage pour le calcul du hachage
    data_to_hash = data.copy()
    data_to_hash.pop("timestamp", None)

    with open(tmp_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data_to_hash, f, indent=2, sort_keys=True)

    if file_hash(tmp_path) != file_hash(target_path):
        os.replace(tmp_path, target_path)
    else:
        os.remove(tmp_path)

    # Ajouter l'horodatage après la comparaison
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(target_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def check_health(file_path):
    try:
        data = toml.load(file_path)
        return data.get("zeroia", {}).get("active", False) is True
    except Exception as e:
        print(f"Erreur lors de la vérification de l'état: {e}")
        return False


def write_state_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_zeroia_state(path: str) -> dict:
    with open(path, "r") as f:
        return toml.load(f)


__all__ = [
    "file_hash",
    "save_toml_if_changed",
    "save_json_if_changed",
    "check_health",
    "write_state_json",
    "load_zeroia_state",
]
