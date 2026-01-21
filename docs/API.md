# API Reference

Full API documentation for stylometry-ttr.

## Import Styles

```python
# Simple import
from stylometry_ttr import compute_ttr

# Namespace style
import stylometry_ttr as ttr
result = ttr.compute(text, text_id="doc1")
tokens = ttr.tokenize(text)
```

## Functions

### `compute_ttr()`

Main entry point for TTR computation.

```python
from stylometry_ttr import compute_ttr

result = compute_ttr(
    text,                    # Raw text string
    text_id,                 # Unique identifier (required)
    title="",                # Optional title
    author="",               # Optional author
    config=None,             # Optional TTRConfig
)
```

### `tokenize()`

Tokenize text into words.

```python
from stylometry_ttr import tokenize

tokens = tokenize(text, lowercase=True)
```

## Classes

### `TTRConfig`

Configuration for TTR computation.

```python
from stylometry_ttr import TTRConfig

config = TTRConfig(
    sttr_chunk_size=1000,     # Words per chunk for STTR (default: 1000)
    min_words_for_sttr=2000,  # Minimum words to compute STTR (default: 2000)
)
```

### `Tokenizer`

Text tokenizer with full configuration options.

```python
from stylometry_ttr import Tokenizer

tokenizer = Tokenizer(
    lowercase=True,       # Normalize to lowercase (default: True)
    min_length=1,         # Minimum token length (default: 1)
    strip_numbers=False,  # Exclude numeric tokens (default: False)
)

tokens = tokenizer.tokenize(text)
```

### `TTRCalculator`

Low-level TTR calculator for custom pipelines.

```python
from stylometry_ttr import TTRCalculator, TTRConfig

calculator = TTRCalculator(config=TTRConfig())
result = calculator.compute(
    tokens,              # List of tokens
    text_id,             # Unique identifier
    title="",            # Optional title
    author="",           # Optional author
)
```

### `TTRAggregator`

Aggregate multiple TTR results into group statistics.

```python
from stylometry_ttr import TTRAggregator

aggregator = TTRAggregator()
aggregate = aggregator.aggregate(
    results,             # List of TTRResult objects
    group_id,            # Group identifier (e.g., author name)
)
```

## Models

### `TTRResult`

Result object returned by `compute_ttr()`.

| Field | Type | Description |
|-------|------|-------------|
| `text_id` | str | Unique identifier |
| `title` | str | Text title |
| `author` | str | Author identifier |
| `total_words` | int | Total token count |
| `unique_words` | int | Unique token count (types) |
| `ttr` | float | Raw TTR: unique/total |
| `root_ttr` | float | Root TTR (Guiraud's index) |
| `log_ttr` | float | Log TTR (Herdan's C) |
| `sttr` | float | Standardized TTR (None if text too short) |
| `sttr_std` | float | STTR standard deviation |
| `chunk_count` | int | Number of chunks for STTR |
| `delta_mean` | float | Mean chunk-to-chunk TTR change |
| `delta_std` | float | Std dev of TTR deltas (volatility) |
| `delta_min` | float | Largest negative swing |
| `delta_max` | float | Largest positive swing |

### `TTRAggregate`

Result object returned by `TTRAggregator.aggregate()`.

| Field | Type | Description |
|-------|------|-------------|
| `group_id` | str | Group identifier |
| `text_count` | int | Number of texts |
| `total_words` | int | Sum of words across all texts |
| `ttr_mean` | float | Mean TTR |
| `ttr_std` | float | TTR standard deviation |
| `ttr_min` | float | Minimum TTR |
| `ttr_max` | float | Maximum TTR |
| `ttr_median` | float | Median TTR |
| `root_ttr_mean` | float | Mean Root TTR |
| `root_ttr_std` | float | Root TTR standard deviation |
| `log_ttr_mean` | float | Mean Log TTR |
| `log_ttr_std` | float | Log TTR standard deviation |
| `sttr_mean` | float | Mean STTR |
| `sttr_std` | float | STTR standard deviation |
| `delta_std_mean` | float | Mean delta std across texts |
| `generated_at` | datetime | Timestamp |

## Output Formats

### ASCII Table

```python
result = compute_ttr(text, text_id="doc1")
print(result)  # Uses __str__
# or
print(result.to_table())
```

Output:
```
+----------------------------------------------------------+
| TTR Report: doc1                                         |
+----------------------------+-----------------------------+
| Metric                     |                       Value |
+----------------------------+-----------------------------+
| Total Words                |                      59,261 |
| Unique Words               |                       5,747 |
| TTR                        |                    0.096978 |
| Root TTR                   |                     23.6079 |
| Log TTR                    |                    0.787686 |
| STTR                       |                    0.414712 |
| STTR Std                   |                    0.025063 |
| Chunk Count                |                          59 |
| Delta Mean                 |                    0.000224 |
| Delta Std                  |                    0.030489 |
| Delta Min                  |                   -0.059000 |
| Delta Max                  |                    0.072000 |
+----------------------------+-----------------------------+
```

### JSON

```python
result = compute_ttr(text, text_id="doc1")
print(result.to_json())
# or with options
print(result.to_json(indent=4, exclude_none=False))
```

Output:
```json
{
  "text_id": "doc1",
  "title": "",
  "author": "",
  "total_words": 59261,
  "unique_words": 5747,
  "ttr": 0.096978,
  "root_ttr": 23.6079,
  "log_ttr": 0.787686,
  "sttr": 0.414712,
  "sttr_std": 0.025063,
  "chunk_count": 59,
  "delta_mean": 0.000224,
  "delta_std": 0.030489,
  "delta_min": -0.059,
  "delta_max": 0.072
}
```

### Dictionary

```python
result = compute_ttr(text, text_id="doc1")
data = result.model_dump()              # Full dict
data = result.model_dump(exclude_none=True)  # Skip None values
```

## All Exports

```python
from stylometry_ttr import (
    # Primary API
    compute_ttr,
    compute,      # Alias for compute_ttr
    tokenize,

    # Models
    TTRResult,
    TTRAggregate,

    # Classes
    TTRCalculator,
    TTRConfig,
    TTRAggregator,
    Tokenizer,
    tokenize_iter,
)
```
