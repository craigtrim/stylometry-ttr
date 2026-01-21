"""Tests for the TTRCalculator class."""

from stylometry_ttr import TTRCalculator, TTRConfig


class TestTTRCalculator:
    """Tests for the TTRCalculator class."""

    def test_empty_tokens(self):
        calc = TTRCalculator()
        result = calc.compute([], text_id="empty")
        assert result.total_words == 0
        assert result.unique_words == 0
        assert result.ttr == 0.0

    def test_all_unique(self):
        calc = TTRCalculator()
        tokens = ["a", "b", "c", "d", "e"]
        result = calc.compute(tokens, text_id="unique")
        assert result.ttr == 1.0
        assert result.unique_words == 5
        assert result.total_words == 5

    def test_all_same(self):
        calc = TTRCalculator()
        tokens = ["the", "the", "the", "the", "the"]
        result = calc.compute(tokens, text_id="same")
        assert result.ttr == 0.2
        assert result.unique_words == 1
        assert result.total_words == 5

    def test_sttr_requires_minimum_words(self):
        calc = TTRCalculator(config=TTRConfig(min_words_for_sttr=100))
        tokens = ["word"] * 50
        result = calc.compute(tokens, text_id="short")
        assert result.sttr is None
        assert result.chunk_count is None
