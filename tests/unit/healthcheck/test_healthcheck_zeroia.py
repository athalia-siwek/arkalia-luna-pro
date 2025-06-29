from unittest.mock import patch

import modules.zeroia.healthcheck_zeroia


def test_healthcheck_zeroia_missing_file(monkeypatch, capsys):
    monkeypatch.setattr("sys.exit", lambda x: x)
    with patch("pathlib.Path.exists", return_value=False):
        modules.zeroia.healthcheck_zeroia.check_zeroia_health()
        out = capsys.readouterr().out
        assert "❌ Fichier zeroia_state.toml manquant." in out


def test_healthcheck_zeroia_active(monkeypatch, capsys):
    monkeypatch.setattr("sys.exit", lambda x: x)
    mock_data = {"active": True, "decision": {"last_decision": "some_decision"}}
    with patch("pathlib.Path.exists", return_value=True):
        with patch("toml.load", return_value=mock_data):
            modules.zeroia.healthcheck_zeroia.check_zeroia_health()
            out = capsys.readouterr().out
            assert "✅ ZeroIA est active." in out


def test_healthcheck_zeroia_inactive(monkeypatch, capsys):
    monkeypatch.setattr("sys.exit", lambda x: x)
    mock_data = {"active": False, "decision": {}}
    with patch("pathlib.Path.exists", return_value=True):
        with patch("toml.load", return_value=mock_data):
            modules.zeroia.healthcheck_zeroia.check_zeroia_health()
            out = capsys.readouterr().out
            assert "❌ ZeroIA inactive ou état incomplet." in out


def healthcheck_function_with_long_parameters(
    param1, param2, param3, param4, param5, param6, param7, param8, param9
):
    # Implementation of the function
    pass
