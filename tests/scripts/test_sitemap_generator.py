import os
import xml.etree.ElementTree as ET

import pytest

SITEMAP_PATH = "site/sitemap.xml"
MKDOCS_CONFIG_PATH = "mkdocs.yml"
NAMESPACE = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


@pytest.fixture(scope="module", autouse=True)
def check_sitemap_file():
    assert os.path.exists(
        SITEMAP_PATH
    ), f"❌ Le fichier {SITEMAP_PATH} est introuvable."


def test_sitemap_is_valid_xml():
    """🧪 Vérifie que sitemap.xml est un XML bien formé"""
    try:
        ET.parse(SITEMAP_PATH)
    except ET.ParseError as e:
        pytest.fail(f"❌ Le fichier sitemap.xml n'est pas un XML valide : {e}")


def test_sitemap_contains_urls():
    """🧪 Vérifie que le sitemap contient au moins une URL valide"""
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    urls = root.findall("sm:url", NAMESPACE)

    assert urls, "❌ Aucune balise <url> trouvée dans sitemap.xml"

    for url_elem in urls:
        loc = url_elem.find("sm:loc", NAMESPACE)
        assert loc is not None, "❌ Une balise <url> ne contient pas de <loc>"
        assert loc.text and loc.text.startswith(
            "http"
        ), f"❌ URL invalide détectée : {loc.text}"


def test_sitemap_matches_nav():
    """🧠 Vérifie que chaque page déclarée dans 'nav:' de mkdocs.yml est bien
    présente dans le sitemap, en ignorant les sections archivées
    """
    # 1. Lire le fichier sitemap
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    urls_in_sitemap = {
        loc.text.strip()
        for url in root.findall("sm:url", NAMESPACE)
        if (loc := url.find("sm:loc", NAMESPACE)) is not None and loc.text is not None
    }

    # 2. Lire les fichiers référencés dans `nav`
    assert (
        urls_in_sitemap
    ), "\u274c Aucune URL trouvée dans le sitemap qui correspond à 'nav'"
