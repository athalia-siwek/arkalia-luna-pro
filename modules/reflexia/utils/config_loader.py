import toml


def load_weights(path: str) -> dict:
    """
    Charge les poids réflexifs depuis le fichier TOML.
    """
    try:
        return toml.load(path)
    except Exception as e:
        print(f"❌ Failed to load TOML config: {e}")
        raise  # <== Important : on re-lève l'erreur
