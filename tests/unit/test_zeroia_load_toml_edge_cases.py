# 🧪 Tests pour les cas limites de chargement TOML dans ZeroIA

import pytest
import toml

from modules.zeroia.reason_loop import load_context, load_reflexia_state, load_toml
from tests.unit.test_helpers import ensure_test_toml

ensure_test_toml()


def test_load_toml_empty_file(tmp_path):
    """🧠 Test avec un fichier TOML complètement vide"""
    empty_file = tmp_path / "empty.toml"
    empty_file.write_text("")

    with pytest.raises(ValueError, match="empty or missing"):
        load_toml(empty_file)


def test_load_toml_whitespace_only_file(tmp_path):
    """🧠 Test avec un fichier contenant seulement des espaces"""
    whitespace_file = tmp_path / "whitespace.toml"
    whitespace_file.write_text("   \n  \t  \n  ")

    with pytest.raises(ValueError, match="empty or missing"):
        load_toml(whitespace_file)


def test_load_toml_missing_file(tmp_path):
    """🧠 Test avec un fichier qui n'existe pas"""
    missing_file = tmp_path / "nonexistent.toml"

    with pytest.raises(ValueError, match="empty or missing"):
        load_toml(missing_file)


def test_load_toml_invalid_syntax(tmp_path):
    """🧠 Test avec une syntaxe TOML invalide"""
    invalid_file = tmp_path / "invalid.toml"
    invalid_file.write_text("[invalid syntax\nno closing bracket")

    with pytest.raises(ValueError, match="Format invalide"):
        load_toml(invalid_file)


def test_load_toml_permission_error(tmp_path):
    """🧠 Test avec un fichier sans permissions de lecture"""
    restricted_file = tmp_path / "restricted.toml"
    restricted_file.write_text("[status]\ncpu = 50")
    restricted_file.chmod(0o000)  # Supprime toutes les permissions

    try:
        with pytest.raises(ValueError, match="Erreur lors du chargement"):
            load_toml(restricted_file)
    finally:
        # Remet les permissions pour le nettoyage
        restricted_file.chmod(0o644)


def test_load_toml_valid_file(tmp_path):
    """🧠 Test avec un fichier TOML valide"""
    valid_file = tmp_path / "valid.toml"
    test_data = {"status": {"cpu": 50, "ram": 40}, "active": True}
    toml.dump(test_data, valid_file.open("w"))

    result = load_toml(valid_file)
    assert result == test_data


def test_load_context_with_custom_path(tmp_path):
    """🧠 Test de load_context avec un chemin personnalisé"""
    custom_context = tmp_path / "custom_context.toml"
    test_data = {"status": {"cpu": 60, "ram": 45}}
    toml.dump(test_data, custom_context.open("w"))

    result = load_context(custom_context)
    assert result == test_data


def test_load_reflexia_state_with_custom_path(tmp_path):
    """🧠 Test de load_reflexia_state avec un chemin personnalisé"""
    custom_reflexia = tmp_path / "custom_reflexia.toml"
    test_data = {"decision": {"last_decision": "monitor"}, "active": True}
    toml.dump(test_data, custom_reflexia.open("w"))

    result = load_reflexia_state(custom_reflexia)
    assert result == test_data


def test_load_toml_unicode_content(tmp_path):
    """🧠 Test avec du contenu Unicode dans le TOML"""
    unicode_file = tmp_path / "unicode.toml"
    unicode_file.write_text(
        '[status]\ndescription = "Système en français avec accents éàü"',
        encoding="utf-8",
    )

    result = load_toml(unicode_file)
    assert result["status"]["description"] == "Système en français avec accents éàü"


def test_load_toml_large_file(tmp_path):
    """🧠 Test avec un fichier TOML de grande taille"""
    large_file = tmp_path / "large.toml"

    # Génère un gros fichier TOML avec beaucoup de données
    large_data = {
        "status": {"cpu": 50, "ram": 40},
        "metrics": {f"metric_{i}": i for i in range(1000)},
        "logs": [f"log_entry_{i}" for i in range(500)],
    }

    toml.dump(large_data, large_file.open("w"))

    result = load_toml(large_file)
    assert len(result["metrics"]) == 1000
    assert len(result["logs"]) == 500
    assert result["status"]["cpu"] == 50


def test_load_toml_special_characters(tmp_path):
    """🧠 Test avec des caractères spéciaux dans le TOML"""
    special_file = tmp_path / "special.toml"
    special_data = {
        "path": "/home/user/folder with spaces/file-name_123.txt",
        "regex": r"^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}$",
        "command": "echo 'Hello, $USER!'",
    }

    toml.dump(special_data, special_file.open("w"))

    result = load_toml(special_file)
    assert result == special_data


def test_load_toml_nested_structures(tmp_path):
    """🧠 Test avec des structures TOML très imbriquées"""
    nested_file = tmp_path / "nested.toml"
    nested_data = {
        "level1": {
            "level2": {"level3": {"level4": {"cpu": 75, "data": ["a", "b", "c"]}}}
        }
    }

    toml.dump(nested_data, nested_file.open("w"))

    result = load_toml(nested_file)
    assert result["level1"]["level2"]["level3"]["level4"]["cpu"] == 75
