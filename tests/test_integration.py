"""Integration tests using The Hound of the Baskervilles."""

import pytest

from stylometry_ttr import TTRCalculator, TTRResult


class TestHoundOfTheBaskervilles:
    """Integration test using The Hound of the Baskervilles."""

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
