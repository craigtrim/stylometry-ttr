"""Tests for per-chunk TTR data (return_chunk_details option)."""

from stylometry_ttr import TTRCalculator, TTRConfig


class TestChunkDetails:
    """Tests for per-chunk TTR data (return_chunk_details option)."""

    def test_chunk_details_disabled_by_default(self, hound_tokens: list[str]):
        """Chunk details should be None when not explicitly requested."""
        calc = TTRCalculator()
        result = calc.compute(hound_tokens, text_id="test")
        assert result.chunk_ttrs is None

    def test_chunk_details_enabled(self, hound_tokens: list[str]):
        """Chunk details should be populated when return_chunk_details=True."""
        config = TTRConfig(return_chunk_details=True)
        calc = TTRCalculator(config=config)
        result = calc.compute(hound_tokens, text_id="test")

        assert result.chunk_ttrs is not None
        assert len(result.chunk_ttrs) == result.chunk_count

    def test_chunk_numbers_are_1_indexed(self, hound_tokens: list[str]):
        """Chunk numbers should start at 1, not 0."""
        config = TTRConfig(return_chunk_details=True)
        calc = TTRCalculator(config=config)
        result = calc.compute(hound_tokens, text_id="test")

        assert result.chunk_ttrs[0].chunk_number == 1
        assert result.chunk_ttrs[-1].chunk_number == len(result.chunk_ttrs)

    def test_chunk_ttr_values_in_valid_range(self, hound_tokens: list[str]):
        """All chunk TTR values should be between 0 and 1."""
        config = TTRConfig(return_chunk_details=True)
        calc = TTRCalculator(config=config)
        result = calc.compute(hound_tokens, text_id="test")

        for chunk in result.chunk_ttrs:
            assert 0.0 <= chunk.ttr <= 1.0

    def test_chunk_details_with_custom_chunk_size(self, hound_tokens: list[str]):
        """Chunk details should work with custom chunk sizes."""
        config = TTRConfig(sttr_chunk_size=500, min_words_for_sttr=1000, return_chunk_details=True)
        calc = TTRCalculator(config=config)
        result = calc.compute(hound_tokens, text_id="test")

        # With smaller chunks, we should have more of them
        assert result.chunk_count > 100
        assert len(result.chunk_ttrs) == result.chunk_count

    def test_chunk_details_graphable_output(self, hound_tokens: list[str]):
        """Demonstrate that chunk details can be used for graphing."""
        config = TTRConfig(return_chunk_details=True)
        calc = TTRCalculator(config=config)
        result = calc.compute(
            hound_tokens,
            text_id="pg2852",
            title="The Hound of the Baskervilles",
        )

        # Extract data for plotting
        x = [c.chunk_number for c in result.chunk_ttrs]
        y = [c.ttr for c in result.chunk_ttrs]

        # Verify we have plottable data
        assert len(x) == len(y)
        assert all(isinstance(n, int) for n in x)
        assert all(isinstance(v, float) for v in y)

        # Print sample for visual inspection
        print("\n" + "=" * 60)
        print("Per-Chunk TTR Data (first 10 and last 5 chunks)")
        print("=" * 60)
        print(f"{'Chunk':<10} {'TTR':<10}")
        print("-" * 20)
        for chunk in result.chunk_ttrs[:10]:
            print(f"{chunk.chunk_number:<10} {chunk.ttr:<10.6f}")
        print("...")
        for chunk in result.chunk_ttrs[-5:]:
            print(f"{chunk.chunk_number:<10} {chunk.ttr:<10.6f}")
        print("=" * 60)
        print(f"Total chunks: {len(result.chunk_ttrs)}")
        print("Ready for: plt.plot(x, y)")
        print("=" * 60)
