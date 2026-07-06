# Sentiment Score History

Standardized 7-point scale: **-3** Very bearish · **-2** Bearish · **-1** Leaning bearish · **0** Neutral/mixed · **+1** Leaning bullish · **+2** Bullish · **+3** Very bullish.

Source of truth: [`history/scores.csv`](history/scores.csv). Regenerate this file with `python3 scripts/render_history.py`. Full write-ups for every run live in [`reports/`](reports/).

## Latest reading

| Commodity | Score | Label | Trend (oldest → newest, last 12 runs) |
|---|---|---|---|
| crude-oil | -2 | Bearish | -2 |
| natural-gas | -1 | Leaning bearish | -1 |
| gold | +1 | Leaning bullish | +1 |
| silver | +1 | Leaning bullish | +1 |
| copper | 0 | Neutral / mixed | 0 |
| wheat | +2 | Bullish | +2 |
| corn | +1 | Leaning bullish | +1 |
| soybeans | -1 | Leaning bearish | -1 |

## Run-by-run scores (last 42 runs, newest first)

| Run (UTC) | crude-oil | natural-gas | gold | silver | copper | wheat | corn | soybeans |
|---|---|---|---|---|---|---|---|---|
| 2026-07-05T19:11Z | -2 | -1 | +1 | +1 | 0 | +2 | +1 | -1 |
