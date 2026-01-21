# Per-Chunk TTR Analysis

The `return_chunk_details` option provides access to individual chunk TTR values, enabling visualization of vocabulary richness across a text.

## Why Chunk-Level Data?

STTR (Standardized TTR) summarizes vocabulary richness as a single mean value. But texts aren't uniform—vocabulary density shifts between dialogue and narration, action and exposition, different speakers or topics.

Per-chunk data lets you:
- **Visualize TTR progression** across a text
- **Identify vocabulary shifts** (e.g., a chapter with unusually rich/sparse vocabulary)
- **Compare patterns** between texts or authors
- **Detect anomalies** that might indicate interpolation or ghostwriting

## Usage

```python
from stylometry_ttr import compute_ttr, TTRConfig

config = TTRConfig(return_chunk_details=True)
result = compute_ttr(text, text_id="doc1", config=config)

# Access chunk data
for chunk in result.chunk_ttrs:
    print(f"Chunk {chunk.chunk_number}: TTR = {chunk.ttr:.4f}")
```

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `sttr_chunk_size` | 1000 | Words per chunk |
| `min_words_for_sttr` | 2000 | Minimum words required |
| `return_chunk_details` | False | Enable per-chunk output |

### Chunk Size Trade-offs

| Size | Granularity | Stability | Use Case |
|------|-------------|-----------|----------|
| 500 | Fine | More volatile | Detecting local shifts, short texts |
| 1000 | Balanced | Moderate | General analysis (default) |
| 2000+ | Coarse | Very stable | Long texts, broad patterns |

## Data Structure

```python
class ChunkTTR(BaseModel):
    chunk_number: int  # 1-indexed
    ttr: float         # TTR for this chunk (0.0 to 1.0)
```

The `chunk_ttrs` field on `TTRResult` is `None` by default. It's only populated when `return_chunk_details=True`.

## Visualization Example

The package intentionally excludes visualization dependencies. Here's how to plot with your preferred library:

### Plotly

```python
import plotly.graph_objects as go
from stylometry_ttr import compute_ttr, TTRConfig

# Compute with chunk details
config = TTRConfig(return_chunk_details=True)
result = compute_ttr(text, text_id="hound", title="The Hound of the Baskervilles", config=config)

# Extract data
x = [c.chunk_number for c in result.chunk_ttrs]
y = [c.ttr for c in result.chunk_ttrs]

# Create figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='TTR per chunk'))
fig.add_hline(y=result.sttr, line_dash="dash", line_color="red",
              annotation_text=f"STTR Mean: {result.sttr:.3f}")
fig.update_layout(
    title=f"Vocabulary Richness: {result.title}",
    xaxis_title="Chunk Number (1000 words each)",
    yaxis_title="Type-Token Ratio",
    yaxis_range=[0.3, 0.5]
)
fig.show()
```

### Matplotlib

```python
import matplotlib.pyplot as plt
from stylometry_ttr import compute_ttr, TTRConfig

config = TTRConfig(return_chunk_details=True)
result = compute_ttr(text, text_id="hound", config=config)

x = [c.chunk_number for c in result.chunk_ttrs]
y = [c.ttr for c in result.chunk_ttrs]

plt.figure(figsize=(12, 5))
plt.plot(x, y, linewidth=1)
plt.axhline(y=result.sttr, color='r', linestyle='--', label=f'STTR Mean: {result.sttr:.3f}')
plt.xlabel('Chunk Number')
plt.ylabel('TTR')
plt.title(f'TTR Progression: {result.title}')
plt.legend()
plt.tight_layout()
plt.show()
```

## Interpreting the Graph

- **Flat line**: Consistent vocabulary throughout (typical of single-author, single-genre text)
- **Downward trend**: Vocabulary becoming more repetitive (common in technical writing, some genres)
- **High variance**: Shifting styles, multiple voices, or mixed content types
- **Sudden spikes/dips**: May indicate chapter boundaries, scene changes, or interpolated sections

## Backward Compatibility

This feature is fully backward compatible:
- `TTRConfig` defaults `return_chunk_details=False`
- `TTRResult.chunk_ttrs` is `None` unless explicitly requested
- Existing code continues to work unchanged
