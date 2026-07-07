# Learned Source Registry

A curated, self-improving list of sources for the sentiment monitor. Every run
**reads this file before gathering** and uses it to target searches; every run
**updates it afterward**: add a source/account that provided dated,
decision-relevant information (say what it was good for), and demote or remove
one that has gone stale or repeatedly added nothing. Keep entries honest —
this list is only useful if it reflects what actually worked.

Status: **keep** = proven over multiple runs · **probation** = added recently,
watch whether it keeps earning its place.

## News & data sites

| Source | Where | Good for | Added | Status |
|---|---|---|---|---|
| Trading Economics | tradingeconomics.com/commodity/* | Consistent per-commodity price + driver summaries, every run | 2026-07-05 | keep |
| OilPrice.com | oilprice.com | Crude geopolitics & supply-flow detail (Hormuz, OSPs, tanker incidents) | 2026-07-05 | keep |
| Natural Gas Intelligence | naturalgasintel.com | Gas-specific flows, storage color, Waha/Mexico angles | 2026-07-05 | keep |
| EIA STEO & weekly data | eia.gov | Official storage prints and price outlooks (gas, crude) | 2026-07-05 | keep |
| Kitco | kitco.com | Precious metals price action + analyst commentary | 2026-07-05 | keep |
| Fastmarkets | fastmarkets.com | Copper concentrate/mine-supply detail | 2026-07-06 | keep |
| Barchart | barchart.com | Futures settlements and grain/energy market recaps | 2026-07-05 | keep |
| Farm Progress / Farm Futures | farmprogress.com | Grain session recaps, cash markets, export sales color | 2026-07-05 | keep |
| AgWeb | agweb.com | Grain futures commentary | 2026-07-05 | keep |
| USDA ERS market outlooks | ers.usda.gov | Balance-sheet context (HRW crop, acreage records) | 2026-07-05 | keep |
| CNBC oil page | cnbc.com/oil | Aggregated crude headlines incl. Barchart wire | 2026-07-06 | keep |
| Investing.com | investing.com/commodities/* | Futures quotes + short driver notes | 2026-07-05 | keep |
| Mitrade / FXStreet feed | mitrade.com | Intraday precious-metals moves with timestamps | 2026-07-06 | probation |
| Fortune commodities | fortune.com | Daily oil price recaps | 2026-07-07 | probation |

## Social accounts & feeds

| Account / Feed | Platform | Good for | Added | Status |
|---|---|---|---|---|
| StockTwits SLV/GLD sentiment gauges | stocktwits.com/symbol/SLV/sentiment (and GLD) | Quantified retail bullish/bearish flips — the crowd-score anchor for precious metals | 2026-07-06 | keep |
| StockTwits news desk | stocktwits.com/news-articles | Retail-sentiment framing of metals moves; surfaces analyst calls (Brandt, Schiff, Hansen) | 2026-07-06 | keep |
| TradingView Minds — USOIL | tradingview.com/symbols/USOIL/minds | Crude trader positioning chatter (support zones, stop clusters) | 2026-07-06 | keep |
| TradingView Minds — XAUUSD | tradingview.com/symbols/XAUUSD/minds | Gold trader mood, overbought/oversold chatter | 2026-07-06 | keep |
| TradingView Minds — WHEATF | tradingview.com/symbols/WHEATF/minds | Wheat mood/positioning split (managed money vs commercials) | 2026-07-06 | keep |
| TradingView news wire (Zacks/Reuters syndication) | tradingview.com/news | Trader-poll style sentiment splits (retail vs institutional %) | 2026-07-06 | keep |
| @sentimentrader | X (x.com/sentimentrader) | Cross-asset sentiment extremes; surfaced twice in metals sweeps — not yet directly quoted | 2026-07-06 | probation |
| Gary Wagner (@GoldForecast) | StockTwits | Gold technical commentary | 2026-07-07 | probation |
| StockTwits COPX/CPER symbols | stocktwits.com/symbol/COPX, /CPER | Copper retail sentiment proxies (miners ETF chatter) | 2026-07-07 | probation |

## Named analysts worth flagging when they appear

Peter Brandt (metals technicals), Ole Hansen / Saxo (metals macro), Citi &
Goldman metals desks (copper targets), Pickering Energy (crude flows),
Commodity Weather Group (ag/gas forecasts — moved natgas score 2026-07-06).

## Known dead ends (do not retry)

- **Reddit** (all subreddits): blocks Anthropic's crawler — API rejects the domain filter outright.
- Generic "indicators and strategies" TradingView script pages: undated TA spam, no sentiment value.
