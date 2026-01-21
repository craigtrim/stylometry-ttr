"""Tests for TTRAggregator."""

import json

import pytest

from stylometry_ttr import TTRCalculator, TTRResult, TTRAggregator


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
