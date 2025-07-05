"""
Module core.

Ce module fait partie du système Arkalia Luna Pro.
"""

from modules.taskia.utils.formatter import format_summary


def taskia_main(context: dict) -> str:
    return format_summary(context)
