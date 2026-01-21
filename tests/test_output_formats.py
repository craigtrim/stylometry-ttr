"""Tests for output formatting methods."""

import json

import pytest

from stylometry_ttr import TTRCalculator, TTRResult


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
