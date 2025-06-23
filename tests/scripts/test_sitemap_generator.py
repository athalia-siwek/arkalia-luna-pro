# tests/scripts/test_sitemap_generator.py

import os
import sys
import xml.etree.ElementTree as ET

import pytest
import yaml

# 📌 Injection du path du script
sys.path.insert(
    0, os.path.abspath("/Volumes/T7/devstation/cursor/arkalia-luna-pro/scripts")
)
import sitemap_generator  # noqa: E402

SITEMAP_PATH = "site/sitemap.xml"
MKDOCS_CONFIG_PATH = "mkdocs.yml"
SITE_URL = "https://arkalia-luna-system.github.io/arkalia-luna-pro"
NAMESPACE = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


@pytest.fixture(scope="module", autouse=True)
def check_sitemap_file():
    assert os.path.exists(
        SITEMAP_PATH
    ), f"❌ Le fichier {SITEMAP_PATH} est introuvable."


def test_sitemap_is_valid_xml():
    try:
        ET.parse(SITEMAP_PATH)
    except ET.ParseError as e:
        pytest.fail(f"❌ Le fichier sitemap.xml n'est pas un XML valide : {e}")


def test_sitemap_contains_urls():
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    urls = root.findall("sm:url", NAMESPACE)
    assert urls, "❌ Aucune balise <url> trouvée dans sitemap.xml"

    for url_elem in urls:
        loc = url_elem.find("sm:loc", NAMESPACE)
        assert loc is not None, "❌ Une balise <url> ne contient pas de <loc>"
        assert loc.text and loc.text.startswith("http"), f"❌ URL invalide : {loc.text}"


def test_sitemap_matches_nav():
    # 🔍 Extraction des chemins attendus
    with open(MKDOCS_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    expected_paths = sitemap_generator.extract_paths(config.get("nav", []))

    # 📄 Extraction des URLs actuelles du sitemap
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    urls_in_sitemap = {
        loc.text.strip()
        for url in root.findall("sm:url", NAMESPACE)
        if (loc := url.find("sm:loc", NAMESPACE)) is not None and loc.text
    }

    # 🧠 Génère les URLs attendues (gestion du cas 'index.md' → "")
    expected_urls = {
        (
            f"{SITE_URL.rstrip('/')}/"
            if not p.strip("/")
            else f"{SITE_URL.rstrip('/')}/{p.strip('/')}/"
        )
        for p in expected_paths
    }

    missing_urls = expected_urls - urls_in_sitemap
    assert not missing_urls, f"❌ Pages manquantes dans sitemap.xml : {missing_urls}"


def test_extract_paths_basic():
    mock_nav = [
        "index.md",
        {"Démarrage": ["installation.md", "configuration.md"]},
        {"Modules": [{"AssistantIA": "assistantia.md"}, "api.md"]},
    ]
    result = sitemap_generator.extract_paths(mock_nav)
    assert all(path in result for path in ("index/", "installation/", "assistantia/"))
