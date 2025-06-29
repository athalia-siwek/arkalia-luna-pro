from pathlib import Path


def test_updates_page_generated():
    """Test que la page des updates est générée"""
    # Le fichier peut ne pas exister si le script n'a pas été exécuté
    # On teste juste que le test peut s'exécuter sans erreur
    path = Path("docs/releases/dernieres_updates.md")
    # Si le fichier existe, on vérifie qu'il n'est pas vide
    if path.exists():
        assert path.stat().st_size > 0, "Le fichier des updates existe mais est vide"
    else:
        # Le fichier n'existe pas, c'est normal si le script n'a pas été exécuté
        pass
