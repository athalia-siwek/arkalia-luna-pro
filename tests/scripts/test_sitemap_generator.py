# tests/scripts/test_sitemap_generator.py

import os
import sys
import xml.etree.ElementTree as ET
from unittest.mock import patch

import pytest
import yaml

# 📌 CI skip automatique si sitemap non généré
CI = os.getenv("CI", "false").lower() == "true"

# 📌 Injection du path du script pour l'import
sys.path.insert(
    0, os.path.abspath("/Volumes/T7/devstation/cursor/arkalia-luna-pro/scripts")
)
from scripts.sitemap_generator import extract_paths, ping_google_sitemap  # noqa: E402

SITEMAP_PATH = "site/sitemap.xml"
MKDOCS_CONFIG_PATH = "mkdocs.yml"
SITE_URL = "https://arkalia-luna-system.github.io/arkalia-luna-pro"
NAMESPACE = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# 🚫 Skip tout le fichier si en CI et sitemap absent
skip_if_no_sitemap = pytest.mark.skipif(
    CI and not os.path.exists(SITEMAP_PATH), reason="⏭️ Sitemap non encore généré en CI"
)


def ensure_sitemap_exists():
    if not os.path.exists(SITEMAP_PATH):
        pytest.fail(
            f"❌ Le fichier {SITEMAP_PATH} est introuvable. Exécute 'mkdocs build'."
        )


@skip_if_no_sitemap
def test_sitemap_is_valid_xml():
    ensure_sitemap_exists()
    try:
        ET.parse(SITEMAP_PATH)
    except ET.ParseError as e:
        pytest.fail(f"❌ Le fichier sitemap.xml n'est pas un XML valide : {e}")


@skip_if_no_sitemap
def test_sitemap_contains_urls():
    ensure_sitemap_exists()
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    urls = root.findall("sm:url", NAMESPACE)
    assert urls, "❌ Aucune balise <url> trouvée dans sitemap.xml"

    for url_elem in urls:
        loc = url_elem.find("sm:loc", NAMESPACE)
        assert loc is not None, "❌ Une balise <url> ne contient pas de <loc>"
        assert loc.text and loc.text.startswith("http"), f"❌ URL invalide : {loc.text}"


@skip_if_no_sitemap
def test_sitemap_matches_nav():
    ensure_sitemap_exists()
    # 🔍 Extraction des chemins attendus
    with open(MKDOCS_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    expected_paths = extract_paths(config.get("nav", []))

    # 📄 Extraction des URLs actuelles du sitemap
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    urls_in_sitemap = {
        loc.text.strip()
        for url in root.findall("sm:url", NAMESPACE)
        if (loc := url.find("sm:loc", NAMESPACE)) is not None and loc.text
    }

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
    result = extract_paths(mock_nav)
    assert all(path in result for path in ("index/", "installation/", "assistantia/"))


@patch("requests.get")
def test_ping_google_sitemap_success(mock_get):
    mock_get.return_value.status_code = 200

    try:
        ping_google_sitemap()
    except Exception as e:
        pytest.fail(f"Ping Google a levé une exception : {e}")

    mock_get.assert_called_once()
    assert mock_get.call_args[0][0].startswith("https://www.google.com/ping?sitemap=")
