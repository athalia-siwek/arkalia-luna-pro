from pathlib import Path


def test_no_macos_hidden_files():
    hidden = list(Path("docs").rglob("._*"))
    assert not hidden, f"🚨 Fichiers ._* détectés : {[str(f) for f in hidden]}"
