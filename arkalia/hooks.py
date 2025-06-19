def generate_sitemap(config=None):
    import subprocess

    print("🌐 [Sitemap] Génération du sitemap.xml…")
    subprocess.run(["python3", "scripts/sitemap_generator.py"], check=True)
    print("✅ Sitemap généré : site/sitemap.xml")
