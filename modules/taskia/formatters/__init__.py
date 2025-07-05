#!/usr/bin/env python3
"""
🌕 TaskIA Formatters Package
📝 Formateurs extensibles selon le principe OCP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

from .html_formatter import HtmlFormatter
from .json_formatter import JsonFormatter
from .markdown_formatter import MarkdownFormatter
from .summary_formatter import SummaryFormatter

__all__ = ["SummaryFormatter", "JsonFormatter", "MarkdownFormatter", "HtmlFormatter"]

__version__ = "2.0.0"
__author__ = "Athalia"
