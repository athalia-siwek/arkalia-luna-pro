# modules/assistantia/utils/processing.py


def process_input(message: str) -> str:
    """Prétraite le message utilisateur."""
    message = message.strip()
    if not message:
        return "Tu as dit : "
    return f"Tu as dit : {message}"
