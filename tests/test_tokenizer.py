"""Tests for the Tokenizer class."""

from stylometry_ttr import Tokenizer


class TestTokenizer:
    """Tests for the Tokenizer class."""

    def test_basic_tokenization(self):
        text = "Hello world! This is a test."
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(text)
        assert tokens == ["hello", "world", "this", "is", "a", "test"]

    def test_contractions(self):
        text = "I can't believe it's working"
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(text)
        assert "can't" in tokens
        assert "it's" in tokens

    def test_hyphenated_words(self):
        text = "The well-known mother-in-law arrived"
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(text)
        assert "well-known" in tokens
        assert "mother-in-law" in tokens

    def test_strip_numbers(self):
        text = "Chapter 1 has 42 pages"
        tokenizer = Tokenizer(strip_numbers=True)
        tokens = tokenizer.tokenize(text)
        assert "1" not in tokens
        assert "42" not in tokens
        assert "chapter" in tokens
