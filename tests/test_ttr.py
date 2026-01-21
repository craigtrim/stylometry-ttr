"""Tests for TTR computation."""

import json
from pathlib import Path

import pytest

from stylometry_ttr import TTRCalculator, TTRConfig, Tokenizer, TTRResult, TTRAggregator


DATA_DIR = Path(__file__).parent / "data"
HOUND_FILE = DATA_DIR / "doyle-the-hound-of-the-baskervilles.txt"


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


class TestOutputFormats:
    """Tests for output formatting methods."""

    @pytest.fixture
    def sample_result(self) -> TTRResult:
        calc = TTRCalculator()
        tokens = ["the", "quick", "brown", "fox", "jumps"]
        return calc.compute(tokens, text_id="test-001", title="Test Doc")

    def test_to_json_returns_valid_json(self, sample_result: TTRResult):
        json_str = sample_result.to_json()
        parsed = json.loads(json_str)
        assert parsed["text_id"] == "test-001"
        assert parsed["total_words"] == 5
        assert parsed["ttr"] == 1.0

    def test_to_json_excludes_none_by_default(self, sample_result: TTRResult):
        json_str = sample_result.to_json()
        parsed = json.loads(json_str)
        assert "sttr" not in parsed
        assert "delta_mean" not in parsed

    def test_to_json_includes_none_when_requested(self, sample_result: TTRResult):
        json_str = sample_result.to_json(exclude_none=False)
        parsed = json.loads(json_str)
        assert "sttr" in parsed
        assert parsed["sttr"] is None

    def test_to_table_returns_string(self, sample_result: TTRResult):
        table = sample_result.to_table()
        assert isinstance(table, str)
        assert "TTR Report:" in table
        assert "Test Doc" in table

    def test_to_table_contains_metrics(self, sample_result: TTRResult):
        table = sample_result.to_table()
        assert "Total Words" in table
        assert "Unique Words" in table
        assert "TTR" in table

    def test_str_returns_table(self, sample_result: TTRResult):
        assert str(sample_result) == sample_result.to_table()


class TestTTRAggregator:
    """Tests for TTRAggregator."""

    @pytest.fixture
    def sample_results(self) -> list[TTRResult]:
        calc = TTRCalculator()
        results = []
        for i, tokens in enumerate([
            ["a", "b", "c", "d", "e"],
            ["a", "a", "b", "b", "c"],
            ["x", "y", "z", "x", "y"],
        ]):
            results.append(calc.compute(tokens, text_id=f"doc-{i}"))
        return results

    def test_aggregate_computes_stats(self, sample_results: list[TTRResult]):
        aggregator = TTRAggregator()
        agg = aggregator.aggregate(sample_results, group_id="test-group")
        assert agg.group_id == "test-group"
        assert agg.text_count == 3
        assert agg.total_words == 15

    def test_aggregate_ttr_stats(self, sample_results: list[TTRResult]):
        aggregator = TTRAggregator()
        agg = aggregator.aggregate(sample_results, group_id="test")
        assert 0.0 < agg.ttr_mean < 1.0
        assert agg.ttr_min <= agg.ttr_mean <= agg.ttr_max

    def test_aggregate_empty_raises(self):
        aggregator = TTRAggregator()
        with pytest.raises(ValueError):
            aggregator.aggregate([], group_id="empty")

    def test_aggregate_to_table(self, sample_results: list[TTRResult]):
        aggregator = TTRAggregator()
        agg = aggregator.aggregate(sample_results, group_id="test-group")
        table = agg.to_table()
        assert "TTR Aggregate:" in table
        assert "test-group" in table

    def test_aggregate_to_json(self, sample_results: list[TTRResult]):
        aggregator = TTRAggregator()
        agg = aggregator.aggregate(sample_results, group_id="test-group")
        json_str = agg.to_json()
        parsed = json.loads(json_str)
        assert parsed["group_id"] == "test-group"
        assert parsed["text_count"] == 3


class TestHoundOfTheBaskervilles:
    """Integration test using The Hound of the Baskervilles."""

    @pytest.fixture
    def hound_text(self) -> str:
        return HOUND_FILE.read_text(encoding="utf-8")

    @pytest.fixture
    def hound_tokens(self, hound_text: str) -> list[str]:
        tokenizer = Tokenizer()
        return tokenizer.tokenize(hound_text)

    @pytest.fixture
    def hound_result(self, hound_tokens: list[str]) -> TTRResult:
        calc = TTRCalculator()
        return calc.compute(
            hound_tokens,
            text_id="pg2852",
            title="The Hound of the Baskervilles",
            author="Arthur Conan Doyle",
        )

    def test_tokenization_word_count(self, hound_tokens: list[str]):
        # The Hound of the Baskervilles should have substantial word count
        assert len(hound_tokens) > 50000
        assert len(hound_tokens) < 100000

    def test_ttr_in_expected_range(self, hound_result: TTRResult):
        # TTR for a novel is typically 0.05-0.15
        assert 0.05 < hound_result.ttr < 0.20

    def test_root_ttr_computed(self, hound_result: TTRResult):
        assert hound_result.root_ttr > 0

    def test_log_ttr_computed(self, hound_result: TTRResult):
        assert 0.7 < hound_result.log_ttr < 1.0

    def test_sttr_computed(self, hound_result: TTRResult):
        # STTR should be computed for a full novel
        assert hound_result.sttr is not None
        assert hound_result.sttr_std is not None
        assert hound_result.chunk_count is not None
        assert hound_result.chunk_count > 50

    def test_delta_metrics_computed(self, hound_result: TTRResult):
        assert hound_result.delta_mean is not None
        assert hound_result.delta_std is not None
        assert hound_result.delta_min is not None
        assert hound_result.delta_max is not None

    def test_print_results(self, hound_result: TTRResult):
        """Print results for README documentation."""
        print("\n" + "=" * 60)
        print("TTR Results: The Hound of the Baskervilles")
        print("=" * 60)
        print(f"Total Words:    {hound_result.total_words:,}")
        print(f"Unique Words:   {hound_result.unique_words:,}")
        print(f"TTR:            {hound_result.ttr:.6f}")
        print(f"Root TTR:       {hound_result.root_ttr:.4f}")
        print(f"Log TTR:        {hound_result.log_ttr:.6f}")
        print(f"STTR:           {hound_result.sttr:.6f}")
        print(f"STTR Std:       {hound_result.sttr_std:.6f}")
        print(f"Chunks:         {hound_result.chunk_count}")
        print(f"Delta Mean:     {hound_result.delta_mean:.6f}")
        print(f"Delta Std:      {hound_result.delta_std:.6f}")
        print(f"Delta Min:      {hound_result.delta_min:.6f}")
        print(f"Delta Max:      {hound_result.delta_max:.6f}")
        print("=" * 60)
