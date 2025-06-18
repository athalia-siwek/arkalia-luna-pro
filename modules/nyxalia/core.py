# modules/nyxalia/core.py


def interpret_signal(signal: str) -> str:
    """
    Interprète un signal d'entrée simple.
    """
    signal = signal.strip().lower()
    if signal == "ping":
        return "pong"
    elif signal == "start":
        return "module nyxalia activé"
    return "signal inconnu"
