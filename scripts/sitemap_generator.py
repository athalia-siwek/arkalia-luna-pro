import os
import time
from pathlib import Path
from urllib.parse import urljoin

BASE_URL = "https://arkalia-luna-system.github.io/arkalia-luna-pro/"
SITE_DIR = Path(__file__).resolve().parent.parent / "site"
SITEMAP_PATH = SITE_DIR / "sitemap.xml"


def collect_html_files(site_dir):
    return sorted([f for f in site_dir.rglob("*.html") if "404.html" not in str(f)])


def build_url(path):
    rel_path = path.relative_to(SITE_DIR)
    url = urljoin(BASE_URL, str(rel_path).replace(os.sep, "/"))
    return url


def generate_sitemap():
    print("🌐 [Sitemap] Génération du sitemap.xml…")
    pages = collect_html_files(SITE_DIR)

    now = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for page in pages:
        url = build_url(page)
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{now}</lastmod>")
        lines.append("  </url>")

    lines.append("</urlset>")

    SITEMAP_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Sitemap généré : {SITEMAP_PATH}")


if __name__ == "__main__":
    generate_sitemap()
