def format_summary(context: dict) -> str:
    """Formate proprement le résumé d’un contexte donné."""
    return "\n".join(f"- {key}: {value}" for key, value in context.items())
