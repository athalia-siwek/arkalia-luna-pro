# arkalia/hooks.py

from scripts.sitemap_generator import generate_sitemap


def on_post_build(config):
    print("🌐 [Hook] Génération du sitemap...")
    generate_sitemap(config["site_url"], output_dir=config["site_dir"])
    print("✅ Sitemap généré ✔")
