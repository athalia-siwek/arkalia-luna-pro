# scripts/sitemap_generator.py

import datetime
import os

import yaml


def parse_nav_from_mkdocs(mkdocs_yml_path="mkdocs.yml"):
    """Charge la config MkDocs et extrait les chemins de navigation."""
    with open(mkdocs_yml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)  # 🔒 Remplace UnsafeLoader → plus sécurisé
    return extract_paths(config.get("nav", []))


def extract_paths(nav, prefix=""):
    """Parcours récursivement la nav pour extraire tous les chemins .md"""
    paths = []

    for item in nav:
        if isinstance(item, dict):
            for _, value in item.items():
                if isinstance(value, list):
                    paths += extract_paths(value, prefix)
                elif isinstance(value, str):
                    path = value.replace(".md", "/").replace("index/", "")
                    paths.append(f"{prefix}{path}")
        elif isinstance(item, str):
            path = item.replace(".md", "/")
            paths.append(f"{prefix}{path}")

    return sorted(set(paths))  # 💡 Supprime les doublons et trie


def generate_sitemap(site_url=None, output_dir="site", mkdocs_yml_path="mkdocs.yml"):
    """Génère un fichier sitemap.xml basé sur la config mkdocs.yml"""
    site_url = site_url or os.getenv(
        "ARKALIA_SITE_URL", "https://arkalia-luna-system.github.io/arkalia-luna-pro"
    )
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    urls = parse_nav_from_mkdocs(mkdocs_yml_path)

    os.makedirs(output_dir, exist_ok=True)
    sitemap_path = os.path.join(output_dir, "sitemap.xml")

    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for path in urls:
            path = path.strip("/")
            full_url = f"{site_url.rstrip('/')}/{path}/"
            f.write("  <url>\n")
            f.write(f"    <loc>{full_url}</loc>\n")
            f.write(f"    <lastmod>{now}</lastmod>\n")
            f.write("  </url>\n")
        f.write("</urlset>\n")

    print(f"✅ Sitemap généré : {sitemap_path}")


def generate_sitemap_from_site():
    """Exécution par appel externe"""
    site_url = "https://arkalia-luna-system.github.io/arkalia-luna-pro"
    generate_sitemap(site_url)


# 💡 Exécution directe
if __name__ == "__main__":
    generate_sitemap(
        site_url="https://arkalia-luna-system.github.io/arkalia-luna-pro",
        output_dir="site",
    )
