from pathlib import Path


def test_updates_page_generated():
    path = Path("docs/releases/dernieres_updates.md")
    assert path.exists(), "Le fichier des updates n'a pas été généré"
    assert "Dernières Updates" in path.read_text(encoding="utf-8")
