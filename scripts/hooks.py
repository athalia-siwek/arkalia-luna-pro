# scripts/hooks.py


def run_sitemap_generator(config=None):
    import os
    import subprocess
    import sys

    script_path = os.path.join("scripts", "sitemap_generator.py")
    if not os.path.exists(script_path):
        print(f"[hooks] ❌ Script non trouvé : {script_path}", file=sys.stderr)
        return

    try:
        subprocess.run(["python", script_path], check=True)
        print("[hooks] ✅ Sitemap généré avec succès")
    except subprocess.CalledProcessError as e:
        print(
            f"[hooks] ❌ Erreur lors de l'exécution du sitemap : {e}", file=sys.stderr
        )
