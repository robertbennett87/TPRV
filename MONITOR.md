# Commodities Sentiment Monitor — Run Instructions

You are producing one edition of a recurring commodities sentiment report for a
**commodities relative-value trading pod**. The readers trade spreads between
these markets, not just outrights: the differentials between legs, crowdedness,
and dated catalysts matter as much as direction. Follow these steps exactly.

## 1. Load context

1. Make sure you are on branch `claude/commodities-sentiment-monitor-2qj2mb`
   (fetch and check it out if not), and pull the latest changes.
2. Read `config/commodities.yaml` — this is the watchlist. Cover every entry.
3. Find the most recent file in `reports/` (sorted by path; paths embed the
   timestamp). Read it — it is your baseline for "what changed". If no report
   exists, this edition is the baseline and every delta is "new".

## 2. Gather news (per commodity)

**First read `SOURCES.md`** — the learned source registry. It tells you which
sites, feeds, and accounts have proven useful and which are dead ends.

For each commodity, run the `search_terms` from the config with WebSearch.
Focus on developments from roughly the last 24 hours, and especially anything
newer than the previous report's timestamp. Prefer primary market sources
(Reuters, Bloomberg, CNBC, Trading Economics, Investing.com, agency reports
like EIA/USDA/OPEC/USGS). Note price direction if reported.

**Scour far and wide, not just the defaults:**
- When a thread matters (a tanker incident, a cargo booking, a crop-damage
  estimate), run a follow-up search on that specific story rather than
  settling for the one mention.
- Use the registry: target `keep`-status sources with `allowed_domains` or
  source-specific queries when their beat is in play (e.g. StockTwits
  sentiment gauges for metals crowd scores, TradingView Minds for
  positioning chatter, NGI for gas flows).
- Each run, spend one or two searches probing beyond the usual set —
  trade press (Platts/S&P Global, Argus, World Grain, Mining.com), regional
  outlets near the story (European press for EU crops, Gulf press for OPEC),
  or a named analyst from the registry. New finds feed the registry.

**Social pulse.** Then run one additional WebSearch per commodity using the
`social` section of the config: build the query from `query_template` and
restrict it with `allowed_domains: social.domains`. Also target the specific
accounts and feeds listed under "Social accounts & feeds" in `SOURCES.md`
when their beat is in play. You are looking for the retail/trader read:
StockTwits bullish/bearish sentiment gauges, notable trader calls,
TradingView Minds/idea chatter, X posts from market commentators. Treat this
stream as noisy — check dates carefully (social search results are often
stale), ignore undated technical-analysis spam, and never let a single post
outweigh the news flow. Its value is (a) catching positioning/mood shifts
before they show up in coverage and (b) flagging when the crowd disagrees
with the news narrative.

**Curate the registry (every run).** After gathering, update `SOURCES.md`:
- **Add** any source, feed, or account that provided dated, decision-relevant
  information this run — with one line on what it's good for, today's date,
  and `probation` status.
- **Promote** a probation entry to `keep` once it has earned its place across
  several runs; **demote or remove** entries that keep coming back stale.
- Record new dead ends so future runs don't waste searches.
This file is the monitor's memory — the goal is a slowly improving, curated
source list that sharpens the measurement over time.

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

**Crowdedness (0-3).** Separately from direction, score how one-sided and
crowded the view is, using the social sweep's uniformity plus any positioning
evidence in coverage (COT/managed-money data, trader polls, retail gauges):

| Crowd | Meaning |
|-------|---------|
| 0 | genuinely two-sided; bulls and bears both vocal |
| 1 | mild lean; dissent easy to find |
| 2 | one-sided narrative; dissent is the minority take |
| 3 | crowded AND uniform — positioning stretched the same way (contrarian risk) |

Direction and crowd are independent: a +2/crowd-3 reading is a bullish but
fade-vulnerable market; a -2/crowd-0 reading is a bearish story the market is
still arguing about. When positioning visibly disagrees with the news tone
(e.g. bullish flow, large traders net short), say so — that tension is the
signal.

## 4. Write the report

Create `reports/YYYY-MM-DD-HHMM-utc.md` (UTC timestamp of the run) with:

1. **Dashboard table** at the top: Commodity | Sentiment | Score | Crowd |
   Δ vs last report | One-line driver.
2. **"Biggest shifts" paragraph**: 2-4 sentences on the most significant
   sentiment changes since the last edition. If nothing shifted, say so.
3. **"## RV pair matrix"** — one row per pair in the config:
   Pair | Spread (leg1−leg2) | Δ vs last | Read. "Spread" is the sentiment
   differential; "Read" is one line on which leg is doing the work and
   whether the differential is widening or narrowing. Flag any pair where
   the differential moved this run.
4. **"## Catalyst calendar (next 7 days)"** — build from the `calendar`
   config plus any dated events found in this run's coverage (Fed
   meetings/minutes, OPEC+ dates, USDA reports, expiries). One row per
   event: Date | Event | Legs | Why it matters now. Actual dates, not
   day-of-week names alone.
5. **Per-commodity sections**, each containing:
   - **What's happening** — 2-4 sentences summarizing the news, with source
     links inline. Note any term-structure/curve or spread mentions in
     coverage (contango/backwardation, storage economics, freight), not just
     outright direction.
   - **Social pulse** — 1-2 sentences on the retail/trader mood from the
     social sweep, with links. Say explicitly when it diverges from the news
     tone, and write "No fresh social signal" if nothing dated and relevant
     turned up.
   - **Positioning read** — 1-3 sentences for someone long/short this leg or
     its spreads: what changed for the position, where the asymmetry sits
     (what's priced vs what isn't), what invalidates the read, and the next
     dated catalyst that can reprice it.

Keep the whole report readable in under five minutes. Cite sources as
markdown links.

## 5. Update the score history

1. Append one row per commodity to `history/scores.csv`
   (columns: `timestamp_utc,commodity,score,label,crowd,driver`). Use the
   same run timestamp for every row (`YYYY-MM-DDTHH:MMZ`), the commodity
   `id` from the config, the numeric score, the label, the crowd score, and
   the one-line driver from the dashboard table. Quote the driver field if
   it contains commas.
2. Append one row per pair to `history/pairs.csv`
   (columns: `timestamp_utc,pair,leg1,leg2,diff` where
   `diff = score(leg1) - score(leg2)`).
3. Regenerate the history dashboard: `python3 scripts/render_history.py`
   (reads both CSVs, writes `HISTORY.md`).
4. Render the PDF edition: `python3 scripts/render_pdf.py` (defaults to the
   newest report; writes `reports/pdf/<same-name>.pdf`).
5. **Email the PDF, if possible.** Check whether an email-capable tool or
   connector (e.g. Gmail) is available in the session. If yes, send the PDF to
   every address under `distribution.email` in `config/commodities.yaml`,
   using `distribution.subject_template` for the subject and the condensed
   dashboard summary as the body. If no email capability exists, skip this
   step silently — do not fail the run — and note "email not sent (no
   connector)" in your final message.

## 6. Publish

1. `git add reports/ history/ HISTORY.md SOURCES.md && git commit` with
   message `Sentiment report YYYY-MM-DD HH:MM UTC` (this includes the PDF
   under `reports/pdf/` and any registry updates).
2. Pull with rebase, then `git push -u origin claude/commodities-sentiment-monitor-2qj2mb`
   (retry on network errors with backoff).
3. End your session with a **condensed version of the report as your final
   message**: the dashboard table plus one line of "what it means" per
   commodity, leading with the biggest sentiment shifts. This final message is
   what gets delivered to the user's notification — make it self-contained.
