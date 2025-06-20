# arkalia/hooks.py

from scripts.sitemap_generator import generate_sitemap_from_site


def generate_sitemap(config=None, **kwargs):
    """
    Hook pour générer le sitemap.xml après la construction du site.
    """
    generate_sitemap_from_site()


def before_startup() -> None:
    """
    Fonction à exécuter avant le démarrage de l'application.
    Peut être utilisée pour initialiser des variables ou vérifier des conditions.
    """
    # Exemple d'initialisation ou de vérification
    print("Initialisation avant le démarrage")
    return None
