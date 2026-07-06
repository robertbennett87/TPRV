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

**Social pulse.** Then run one additional WebSearch per commodity using the
`social` section of the config: build the query from `query_template` and
restrict it with `allowed_domains: social.domains`. You are looking for the
retail/trader read: StockTwits bullish/bearish sentiment gauges, notable
trader calls, TradingView Minds/idea chatter, X posts from market
commentators. Treat this stream as noisy — check dates carefully (social
search results are often stale), ignore undated technical-analysis spam, and
never let a single post outweigh the news flow. Its value is (a) catching
positioning/mood shifts before they show up in coverage and (b) flagging when
the crowd disagrees with the news narrative.

## 3. Score sentiment

Assign each commodity a label and score on the standardized 7-point scale:

| Score | Label            | Use when the news flow is…                                  |
|-------|------------------|-------------------------------------------------------------|
| +3    | Very bullish     | one-sided bullish with a major structural/supply-shock story |
| +2    | Bullish          | clearly bullish; catalysts strongly outweigh the bear case   |
| +1    | Leaning bullish  | net-positive tone, but the bull case is young or contested   |
|  0    | Neutral / mixed  | balanced, offsetting, or quiet news flow                     |
| -1    | Leaning bearish  | net-negative tone, but the bear case is young or contested   |
| -2    | Bearish          | clearly bearish; catalysts strongly outweigh the bull case   |
| -3    | Very bearish     | one-sided bearish with a major structural/glut/demand-shock story |

Sentiment means *market/news tone about the price outlook*, not whether the
price already moved. Judge from the balance of catalysts in the coverage,
weighted by the commodity's `drivers` list. Reserve ±3 for genuinely extreme,
one-sided narratives — most readings should live between -2 and +2. Record the
delta versus the previous report (e.g. "▲ from Neutral", "unchanged").

## 4. Write the report

Create `reports/YYYY-MM-DD-HHMM-utc.md` (UTC timestamp of the run) with:

1. **Dashboard table** at the top: Commodity | Sentiment | Score | Δ vs last
   report | One-line driver.
2. **"Biggest shifts" paragraph**: 2-4 sentences on the most significant
   sentiment changes since the last edition. If nothing shifted, say so.
3. **Per-commodity sections**, each containing:
   - **What's happening** — 2-4 sentences summarizing the news, with source
     links inline.
   - **Social pulse** — 1-2 sentences on the retail/trader mood from the
     social sweep, with links. Say explicitly when it diverges from the news
     tone, and write "No fresh social signal" if nothing dated and relevant
     turned up.
   - **What it means** — 1-3 sentences of interpretation for someone covering
     this beat: why sentiment sits where it does, what would change it, and
     anything worth watching before the next edition (data releases, meetings,
     weather windows).

Keep the whole report readable in under five minutes. Cite sources as
markdown links.

## 5. Update the score history

1. Append one row per commodity to `history/scores.csv`
   (columns: `timestamp_utc,commodity,score,label,driver`). Use the same
   run timestamp for every row (`YYYY-MM-DDTHH:MMZ`), the commodity `id`
   from the config, the numeric score, the label, and the one-line driver
   from the dashboard table. Quote the driver field if it contains commas.
2. Regenerate the history dashboard: `python3 scripts/render_history.py`
   (reads `history/scores.csv`, writes `HISTORY.md`).
3. Render the PDF edition: `python3 scripts/render_pdf.py` (defaults to the
   newest report; writes `reports/pdf/<same-name>.pdf`).

## 6. Publish

1. `git add reports/ history/ HISTORY.md && git commit` with message
   `Sentiment report YYYY-MM-DD HH:MM UTC` (this includes the PDF under
   `reports/pdf/`).
2. Pull with rebase, then `git push -u origin claude/commodities-sentiment-monitor-2qj2mb`
   (retry on network errors with backoff).
3. End your session with a **condensed version of the report as your final
   message**: the dashboard table plus one line of "what it means" per
   commodity, leading with the biggest sentiment shifts. This final message is
   what gets delivered to the user's notification — make it self-contained.
