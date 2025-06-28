# 📄 tests/unit/test_zeroia_fail_input.py

from pathlib import Path

import pytest

from modules.zeroia.reason_loop import reason_loop
from tests.unit.test_helpers import ensure_test_toml, ensure_zeroia_state_file

ensure_test_toml()


def test_fail_on_missing_keys(tmp_path: Path):
    """💥 Depuis la correction ZeroIA, les clés manquantes utilisent des defaults au lieu de lever KeyError."""
    ctx_path = tmp_path / "ctx.toml"
    reflexia_path = tmp_path / "reflexia.toml"

    ctx_path.write_text("[status]\ncpu = 95\n")  # 🧪 Pas de ram
    reflexia_path.write_text("[status]\n")  # 🧪 Structure minimale

    ensure_zeroia_state_file()

    # ZeroIA ne lève plus KeyError, il utilise des defaults et fonctionne
    result = reason_loop(context_path=ctx_path, reflexia_path=reflexia_path)
    assert result is not None  # Le processus fonctionne avec des defaults


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
        match=(
            r"\[TOML\] Format invalide dans .*: "
            r"Found invalid character in key name: ':'"
        ),
    ):
        reason_loop(context_path=ctx_path, reflexia_path=reflexia_path)
