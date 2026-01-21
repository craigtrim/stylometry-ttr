"""Shared fixtures for TTR tests."""

from pathlib import Path

import pytest

from stylometry_ttr import Tokenizer


DATA_DIR = Path(__file__).parent / "data"
HOUND_FILE = DATA_DIR / "doyle-the-hound-of-the-baskervilles.txt"


@pytest.fixture
def hound_text() -> str:
    """Load The Hound of the Baskervilles text."""
    return HOUND_FILE.read_text(encoding="utf-8")


@pytest.fixture
def hound_tokens(hound_text: str) -> list[str]:
    """Tokenize The Hound of the Baskervilles."""
    tokenizer = Tokenizer()
    return tokenizer.tokenize(hound_text)
