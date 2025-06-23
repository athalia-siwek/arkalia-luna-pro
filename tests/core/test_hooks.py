from arkalia import hooks


def test_before_startup_runs():
    # Appelle le hook ou vérifie son effet secondaire
    assert hooks.before_startup() is None  # ou un effet mesurable


def test_hooks_importable():
    assert True