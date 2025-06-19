# scripts/sitemap_generator.py

import datetime
import os

import yaml


def parse_nav_from_mkdocs(mkdocs_yml_path="mkdocs.yml"):
    with open(mkdocs_yml_path, "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.UnsafeLoader)
    return extract_paths(config.get("nav", []))


def extract_paths(nav, prefix=""):
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

    return paths


def generate_sitemap(site_url, output_dir="site", mkdocs_yml_path="mkdocs.yml"):
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    urls = parse_nav_from_mkdocs(mkdocs_yml_path)

    # Crée le dossier output_dir si inexistant
    os.makedirs(output_dir, exist_ok=True)

    sitemap_path = os.path.join(output_dir, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for path in urls:
            full_url = f"{site_url.rstrip('/')}/{path}"
            f.write("  <url>\n")
            f.write(f"    <loc>{full_url}</loc>\n")
            f.write(f"    <lastmod>{now}</lastmod>\n")
            f.write("  </url>\n")
        f.write("</urlset>\n")

    print(f"✅ Sitemap généré : {sitemap_path}")


# 💡 Exécution directe
if __name__ == "__main__":
    generate_sitemap(
        site_url="https://arkalia-luna-system.github.io/arkalia-luna-pro",
        output_dir="site",
    )
