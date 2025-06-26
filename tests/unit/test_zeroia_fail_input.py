# 📄 tests/unit/test_zeroia_fail_input.py

from pathlib import Path

import pytest

from modules.zeroia.reason_loop import reason_loop
from tests.unit.test_helpers import ensure_test_toml, ensure_zeroia_state_file

ensure_test_toml()


def test_fail_on_missing_keys(tmp_path: Path):
    """💥 Manque la clé 'ram' dans le contexte (pas d'injection ReflexIA)."""
    ctx_path = tmp_path / "ctx.toml"
    reflexia_path = tmp_path / "reflexia.toml"

    ctx_path.write_text("[status]\ncpu = 95\n")  # 🧪 Pas de ram
    reflexia_path.write_text("[status]\n")  # 🧪 Structure minimale

    ensure_zeroia_state_file()

    with pytest.raises(KeyError, match=r"ram"):
        reason_loop(context_path=ctx_path, reflexia_path=reflexia_path)


def test_fail_on_empty_file(tmp_path: Path):
    """💥 Fichier TOML vide → erreur attendue."""
    ctx_path = tmp_path / "ctx_empty.toml"
    reflexia_path = tmp_path / "reflexia.toml"

    ctx_path.write_text("")  # 🧪 Vide
    reflexia_path.write_text("")

    with pytest.raises(ValueError, match=r"TOML file .* is empty or missing"):
        reason_loop(context_path=ctx_path, reflexia_path=reflexia_path)


def test_fail_on_invalid_toml(tmp_path: Path):
    """💥 Fichier TOML invalide → erreur de parsing."""
    ctx_path = tmp_path / "ctx_invalid.toml"
    reflexia_path = tmp_path / "reflexia.toml"

    ctx_path.write_text("::: invalid")  # 🧪 Format incorrect
    reflexia_path.write_text("")

    with pytest.raises(
        ValueError,
        match=r"Invalid TOML format in .*: Found invalid character in key name: ':'",
    ):
        reason_loop(context_path=ctx_path, reflexia_path=reflexia_path)
