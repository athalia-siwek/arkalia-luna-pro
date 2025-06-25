from modules.taskia.utils.formatter import format_summary


def taskia_main(context: dict) -> str:
    """Analyse le contexte et génère une synthèse."""
    return format_summary(context)
