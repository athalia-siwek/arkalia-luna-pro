import pytest
import toml

from modules.zeroia import reason_loop


def test_decide_high_cpu():
    context = {"status": {"cpu": 91}}
    assert reason_loop.decide(context)[0] == "reduce_load"


def test_decide_medium_cpu():
    context = {"status": {"cpu": 72}}
    assert reason_loop.decide(context)[0] == "reduce_load"


def test_decide_low_cpu():
    context = {"status": {"cpu": 45}}
    assert reason_loop.decide(context)[0] == "normal"


def test_decide_critical():
    context = {"status": {"severity": "critical"}}
    assert reason_loop.decide(context)[0] == "emergency_shutdown"


def test_decide_no_status():
    context = {}
    assert reason_loop.decide(context)[0] == "normal"


def test_toml_parsing_error(tmp_path, monkeypatch):
    # Crée un fichier TOML avec une erreur de syntaxe
    broken_toml_path = tmp_path / "broken_context.toml"
    with open(broken_toml_path, "w") as f:
        f.write("[status\nseverity = 'critical'")  # Manque une fermeture de crochet

    # Monkeypatch pour utiliser le fichier TOML cassé
    monkeypatch.setattr("modules.zeroia.reason_loop.CTX_PATH", broken_toml_path)

    # Vérifie que la fonction load_context lève une erreur
    with pytest.raises(toml.TomlDecodeError):
        reason_loop.load_context()
