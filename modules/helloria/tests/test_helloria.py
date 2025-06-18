# modules/helloria/tests/test_helloria.py

from modules.helloria.core import greet_user


def test_greet_user():
    assert greet_user("Athalia") == "Bienvenue dans Helloria, Athalia !"
    assert greet_user("Visiteur") == "Bienvenue dans Helloria, Visiteur !"
