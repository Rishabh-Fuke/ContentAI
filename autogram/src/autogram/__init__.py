"""autogram package initializer.

Provides a small helper to access important environment variables (like
OPENAI_API_KEY) and ensures .env is loaded when the package is imported.
"""
from dotenv import load_dotenv
import os
from pathlib import Path


root = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=root / '.env')


def get_openai_key():
	"""Return the OPENAI_API_KEY from environment or None if missing."""
	return os.environ.get('OPENAI_API_KEY')


__all__ = ["get_openai_key"]
