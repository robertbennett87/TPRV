# TPRV — Commodities Sentiment Monitor

A recurring sentiment monitor for commodities news. Every few hours a
scheduled Claude Code session gathers the latest coverage for each commodity
on the watchlist, scores the sentiment, explains what's driving it and what it
means for someone covering the beat, and:

- commits the full report to [`reports/`](reports/),
- appends every score to the running history in
  [`history/scores.csv`](history/scores.csv) and refreshes the
  [`HISTORY.md`](HISTORY.md) dashboard, and
- delivers a condensed summary by push/email notification.

## How it works

- **`config/commodities.yaml`** — the watchlist. Edit this to add/remove
  commodities or tune search terms and drivers. Changes take effect on the
  next scheduled run; no other step needed.
- **`MONITOR.md`** — the methodology each run follows: gather news via web
  search, score sentiment on a -2…+2 scale, compare against the previous
  report, write the new edition.
- **`reports/`** — the archive, one markdown file per run, timestamped in
  UTC. The newest report is each run's baseline for "what changed".
- **`history/scores.csv`** — the running score history: one row per
  commodity per run (`timestamp_utc,commodity,score,label,driver`). This is
  the machine-readable source of truth for charting sentiment over time.
- **`HISTORY.md`** — human-readable view of the history: latest reading and
  recent trend per commodity, plus a run-by-run score grid at the monitor's
  4-hour intervals. Regenerated each run by `scripts/render_history.py`.

## Schedule

Runs are driven by a Claude Code routine (scheduled trigger) that fires every
4 hours and spawns a fresh session which follows `MONITOR.md`. Adjust the
cadence or pause it from the Claude Code routines/triggers settings, or ask
Claude to update the trigger.

## Standardized sentiment scale

| Score | Label            |
|-------|------------------|
| +3    | Very bullish     |
| +2    | Bullish          |
| +1    | Leaning bullish  |
|  0    | Neutral / mixed  |
| -1    | Leaning bearish  |
| -2    | Bearish          |
| -3    | Very bearish     |

Sentiment reflects the tone of news about the price outlook — the balance of
bullish vs bearish catalysts in current coverage — not just the last price
move. The extremes (±3) are reserved for one-sided narratives around a major
structural story (a supply shock, a demand collapse); most readings should
live between -2 and +2 so that moves across gradations stay meaningful.
