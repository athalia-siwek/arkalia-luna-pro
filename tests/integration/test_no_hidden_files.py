from pathlib import Path


def test_no_mac_hidden_files():
    docs = Path("docs")
    hidden = list(docs.rglob("._*"))
    assert not hidden, f"Fichiers invisibles trouvés : {[str(f) for f in hidden]}"
