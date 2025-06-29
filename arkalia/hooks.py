from scripts.sitemap_generator import generate_sitemap_from_site


def generate_sitemap(config=None, **kwargs) -> None:
    """
    Hook pour générer le sitemap.xml après la construction du site.
    """
    generate_sitemap_from_site()


def before_startup() -> None:
    """
    Fonction à exécuter avant le démarrage de l'application.
    Utilisée pour initialiser ou vérifier certains éléments.
    """
    print("Initialisation avant le démarrage")
    # Placeholder désactivé pour éviter erreurs F821
    # Exemple : initialiser base de données, logs, etc.
    return None
