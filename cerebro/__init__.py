"""
LLM-Cerebroscope
----------------
An open-source CLI tool for forensic data analysis and automated consistency checking
using local LLMs (Ollama).
"""

import os

# Project Metadata
__app_name__ = "llm-cerebroscope"
__version__ = "0.1.0"
__author__ = "Oskar Brzycki"
__license__ = "MIT"

# --- EXPORTS (FACADE PATTERN) ---
# This allows you to import main classes directly from the package
# Example: 'from cerebro import LogicEngine' instead of 'from cerebro.validator import LogicEngine'

# Uncomment and adjust the class names below to match your actual code:

# from .validator import LogicEngine
# from .ingestor import DocumentIngestor
# from .vector_store import ChromaManager

# __all__ defines what gets imported when someone uses: from cerebro import *
__all__ = [
    "__app_name__",
    "__version__",
    # "LogicEngine",
    # "DocumentIngestor",
]