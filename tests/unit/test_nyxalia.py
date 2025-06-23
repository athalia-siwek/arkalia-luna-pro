# modules/nyxalia/tests/test_nyxalia.py

from modules.nyxalia.core import interpret_signal


def test_interpret_signal():
    assert interpret_signal("ping") == "pong"
    assert interpret_signal("start") == "module nyxalia activé"
    assert interpret_signal("hello") == "signal inconnu"
