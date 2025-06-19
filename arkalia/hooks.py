# arkalia/hooks.py

from scripts.sitemap_generator import generate_sitemap_from_site


def generate_sitemap(config=None, **kwargs):
    """
    Hook pour générer le sitemap.xml après la construction du site.
    """
    generate_sitemap_from_site()
