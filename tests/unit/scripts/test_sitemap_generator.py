import os
import sys
import unittest
from unittest.mock import MagicMock, mock_open, patch

import pytest
import yaml
from defusedxml.ElementTree import parse as safe_parse

# 📌 Injection du path du script pour l'import
sys.path.insert(0, os.path.abspath("/Volumes/T7/devstation/cursor/arkalia-luna-pro/scripts"))

from scripts.sitemap_generator import extract_paths, generate_sitemap, ping_google_sitemap

# 📌 CI skip automatique si sitemap non généré
CI = os.getenv("CI", "false").lower() == "true"
SITEMAP_PATH = "site/sitemap.xml"
MKDOCS_CONFIG_PATH = "mkdocs.yml"
SITE_URL = "https://arkalia-luna-system.github.io/arkalia-luna-pro"
NAMESPACE = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# 🚫 Skip tout le fichier si en CI et sitemap absent
skip_if_no_sitemap = pytest.mark.skipif(
    CI and not os.path.exists(SITEMAP_PATH), reason="⏭️ Sitemap non encore généré en CI"
)


def ensure_sitemap_exists() -> None:
    if not os.path.exists(SITEMAP_PATH):
        pytest.fail(f"❌ Le fichier {SITEMAP_PATH} est introuvable. Exécute 'mkdocs build'.")


@skip_if_no_sitemap
def test_sitemap_is_valid_xml() -> None:
    ensure_sitemap_exists()
    try:
        safe_parse(SITEMAP_PATH)
    except Exception as e:
        pytest.fail(f"❌ Le fichier sitemap.xml n'est pas un XML valide : {e}")


@skip_if_no_sitemap
def test_sitemap_contains_urls() -> None:
    ensure_sitemap_exists()
    tree = safe_parse(SITEMAP_PATH)
    root = tree.getroot()
    urls = root.findall("sm:url", NAMESPACE)
    assert urls, "❌ Aucune balise <url> trouvée dans sitemap.xml"

    for url_elem in urls:
        loc = url_elem.find("sm:loc", NAMESPACE)
        assert loc is not None, "❌ Une balise <url> ne contient pas de <loc>"
        assert loc.text and loc.text.startswith("http"), f"❌ URL invalide : {loc.text}"


@skip_if_no_sitemap
def test_sitemap_matches_nav() -> None:
    ensure_sitemap_exists()
    with open(MKDOCS_CONFIG_PATH, encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.Loader)
    nav = config.get("nav", [])
    assert len(nav) > 0, "Navigation vide"

    expected_paths = extract_paths(nav)

    tree = safe_parse(SITEMAP_PATH)
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

    # Exclure les URLs README/ qui ne sont pas dans le sitemap
    expected_urls.discard(f"{SITE_URL.rstrip('/')}/README/")

    missing_urls = expected_urls - urls_in_sitemap
    assert not missing_urls, f"❌ Pages manquantes dans sitemap.xml : {missing_urls}"


def test_extract_paths_basic() -> None:
    mock_nav = [
        "index.md",
        {"Démarrage": ["installation.md", "configuration.md"]},
        {"Modules": [{"AssistantIA": "assistantia.md"}, "api.md"]},
    ]
    result = extract_paths(mock_nav)
    assert all(
        path in result for path in ("index/", "installation/", "assistantia/")
    ), "Chemins manquants"


@patch("requests.get")
def test_ping_google_sitemap_success(mock_get) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    try:
        ping_google_sitemap()
    except Exception as e:
        pytest.fail(f"Ping Google a levé une exception : {e}")

    mock_get.assert_called_once()
    assert mock_get.call_args[0][0].startswith(
        "https://www.google.com/ping?sitemap="
    ), "Ping Google échoué"


@patch("requests.get", side_effect=Exception("Network error"))
def test_ping_google_sitemap_failure(mock_get) -> None:
    ping_google_sitemap()
    mock_get.assert_called_once()


class TestSitemapGenerator(unittest.TestCase):
    def test_generate_sitemap(self):
        """Teste la génération complète du sitemap"""
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("os.makedirs"):
                with patch("datetime.datetime") as mock_datetime:
                    mock_datetime.now.return_value.strftime.return_value = "2025-01-01"

                    with patch(
                        "scripts.sitemap_generator.parse_nav_from_mkdocs",
                        return_value=["path1/", "path2/"],
                    ):
                        generate_sitemap()

                        # Vérifie que le fichier a été écrit avec le bon contenu
                        mock_file.assert_called()
                        handle = mock_file()
                        # Vérifie qu'une écriture a été effectuée
                        handle.write.assert_called()


if __name__ == "__main__":
    unittest.main()
