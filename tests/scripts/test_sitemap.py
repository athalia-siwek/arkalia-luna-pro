# tests/test_sitemap.py

import os

from defusedxml.ElementTree import parse as secure_parse


def test_sitemap_exists():
    assert os.path.exists("site/sitemap.xml"), "Le fichier sitemap.xml est introuvable"


def test_sitemap_is_valid_xml():
    try:
        secure_parse("site/sitemap.xml")
    except Exception as e:
        raise AssertionError(f"Erreur de parsing XML : {e}")


def test_sitemap_contains_urls():
    tree = secure_parse("site/sitemap.xml")
    root = tree.getroot()
    urls = root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
    assert len(urls) >= 5, f"Sitemap trop court : {len(urls)} éléments trouvés"
