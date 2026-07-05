# Commodities Sentiment Monitor — Run Instructions

You are producing one edition of a recurring commodities sentiment report for a
journalist who covers these markets. Follow these steps exactly.

## 1. Load context

1. Make sure you are on branch `claude/commodities-sentiment-monitor-2qj2mb`
   (fetch and check it out if not), and pull the latest changes.
2. Read `config/commodities.yaml` — this is the watchlist. Cover every entry.
3. Find the most recent file in `reports/` (sorted by path; paths embed the
   timestamp). Read it — it is your baseline for "what changed". If no report
   exists, this edition is the baseline and every delta is "new".

## 2. Gather news (per commodity)

For each commodity, run the `search_terms` from the config with WebSearch.
Focus on developments from roughly the last 24 hours, and especially anything
newer than the previous report's timestamp. Prefer primary market sources
(Reuters, Bloomberg, CNBC, Trading Economics, Investing.com, agency reports
like EIA/USDA/OPEC/USGS). Note price direction if reported.

## 3. Score sentiment

Assign each commodity a sentiment label and score:

| Score | Label            |
|-------|------------------|
| +2    | Bullish          |
| +1    | Leaning bullish  |
|  0    | Neutral / mixed  |
| -1    | Leaning bearish  |
| -2    | Bearish          |

Sentiment means *market/news tone about the price outlook*, not whether the
price already moved. Judge from the balance of catalysts in the coverage,
weighted by the commodity's `drivers` list. Record the delta versus the
previous report (e.g. "▲ from Neutral", "unchanged").

## 4. Write the report

Create `reports/YYYY-MM-DD-HHMM-utc.md` (UTC timestamp of the run) with:

1. **Dashboard table** at the top: Commodity | Sentiment | Score | Δ vs last
   report | One-line driver.
2. **"Biggest shifts" paragraph**: 2-4 sentences on the most significant
   sentiment changes since the last edition. If nothing shifted, say so.
3. **Per-commodity sections**, each containing:
   - **What's happening** — 2-4 sentences summarizing the news, with source
     links inline.
   - **What it means** — 1-3 sentences of interpretation for someone covering
     this beat: why sentiment sits where it does, what would change it, and
     anything worth watching before the next edition (data releases, meetings,
     weather windows).

Keep the whole report readable in under five minutes. Cite sources as
markdown links.

## 5. Publish

1. `git add reports/ && git commit` with message
   `Sentiment report YYYY-MM-DD HH:MM UTC`.
2. Pull with rebase, then `git push -u origin claude/commodities-sentiment-monitor-2qj2mb`
   (retry on network errors with backoff).
3. End your session with a **condensed version of the report as your final
   message**: the dashboard table plus one line of "what it means" per
   commodity, leading with the biggest sentiment shifts. This final message is
   what gets delivered to the user's notification — make it self-contained.
