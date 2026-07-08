# Sentiment Score History

Standardized 7-point scale: **-3** Very bearish · **-2** Bearish · **-1** Leaning bearish · **0** Neutral/mixed · **+1** Leaning bullish · **+2** Bullish · **+3** Very bullish.

Source of truth: [`history/scores.csv`](history/scores.csv). Regenerate this file with `python3 scripts/render_history.py`. Full write-ups for every run live in [`reports/`](reports/).

## Latest reading

| Commodity | Score | Label | Trend (oldest → newest, last 12 runs) |
|---|---|---|---|
| crude-oil | 0 | Neutral / mixed | -2 → -1 → -1 → -1 → -1 → -1 → -1 → 0 → 0 |
| natural-gas | -1 | Leaning bearish | -1 → -1 → -1 → -2 → -2 → -2 → -2 → -2 → -1 |
| gold | +1 | Leaning bullish | +1 → +1 → +1 → +1 → +1 → +1 → +1 → +1 → +1 |
| silver | +1 | Leaning bullish | +1 → +2 → +2 → +2 → +2 → +2 → +1 → +1 → +1 |
| copper | +2 | Bullish | 0 → +1 → +1 → +1 → +1 → +2 → +2 → +2 → +2 |
| wheat | +2 | Bullish | +2 → +2 → +2 → +2 → +2 → +2 → +2 → +2 → +2 |
| corn | +2 | Bullish | +1 → +2 → +2 → +2 → +2 → +2 → +2 → +2 → +2 |
| soybeans | +1 | Leaning bullish | -1 → 0 → 0 → 0 → +1 → +1 → +1 → +1 → +1 |

## Run-by-run scores (last 42 runs, newest first)

| Run (UTC) | crude-oil | natural-gas | gold | silver | copper | wheat | corn | soybeans |
|---|---|---|---|---|---|---|---|---|
| 2026-07-08T09:35Z | 0 | -1 | +1 | +1 | +2 | +2 | +2 | +1 |
| 2026-07-07T20:05Z | 0 | -2 | +1 | +1 | +2 | +2 | +2 | +1 |
| 2026-07-07T16:30Z | -1 | -2 | +1 | +1 | +2 | +2 | +2 | +1 |
| 2026-07-07T12:26Z | -1 | -2 | +1 | +2 | +2 | +2 | +2 | +1 |
| 2026-07-07T11:10Z | -1 | -2 | +1 | +2 | +1 | +2 | +2 | +1 |
| 2026-07-06T23:00Z | -1 | -2 | +1 | +2 | +1 | +2 | +2 | 0 |
| 2026-07-06T22:15Z | -1 | -1 | +1 | +2 | +1 | +2 | +2 | 0 |
| 2026-07-06T22:00Z | -1 | -1 | +1 | +2 | +1 | +2 | +2 | 0 |
| 2026-07-05T19:11Z | -2 | -1 | +1 | +1 | 0 | +2 | +1 | -1 |

## RV pair sentiment differentials (leg1 − leg2, last 42 runs, newest first)

Positive = news flow favors leg1 outperformance. Pairs defined in `config/commodities.yaml`; raw data in [`history/pairs.csv`](history/pairs.csv).

| Run (UTC) | gold-silver | corn-soybeans | corn-wheat | crude-natgas | gold-copper |
|---|---|---|---|---|---|
| 2026-07-08T09:35Z | 0 | +1 | 0 | +1 | -1 |
| 2026-07-07T20:05Z | 0 | +1 | 0 | +2 | -1 |
| 2026-07-07T16:30Z | 0 | +1 | 0 | +1 | -1 |
| 2026-07-07T12:26Z | -1 | +1 | 0 | +1 | -1 |
| 2026-07-07T11:10Z | -1 | +1 | 0 | +1 | 0 |
| 2026-07-06T23:00Z | -1 | +2 | 0 | +1 | 0 |
| 2026-07-06T22:15Z | -1 | +2 | 0 | 0 | 0 |
| 2026-07-06T22:00Z | -1 | +2 | 0 | 0 | 0 |
| 2026-07-05T19:11Z | 0 | +2 | -1 | -1 | +1 |
