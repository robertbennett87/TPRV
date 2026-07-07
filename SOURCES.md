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

## Reddit — access via trackers only

Direct Reddit access fails at every layer (network policy blocks the request;
Reddit blocks Anthropic's crawler; `allowed_domains: reddit.com` errors out).
Scour it indirectly:

| Route | How | Good for | Added | Status |
|---|---|---|---|---|
| ApeWisdom | WebSearch "apewisdom {tickers} reddit mentions sentiment" (direct fetch 403s — search snippets only) | Quantified Reddit crowd data: mentions/24h, unique users, % positive per ticker (SLV/GLD verified live; UNG returned 0 mentions — thin-coverage caveat) | 2026-07-07 | keep |
| AltIndex | WebSearch only (direct fetch 403s) | WSB most-mentioned tracker, 5-min refresh claims | 2026-07-07 | probation |
| Articles quoting Reddit | unrestricted WebSearch, e.g. "reddit silver squeeze discussion" | Narrative color when a retail story is in play (Yahoo Finance covered WSB silver split) | 2026-07-07 | probation |

## Independent source map (Fable consultation, 2026-07-07)

Produced by an independently-prompted Fable instance with no context from this
monitor's runs, as a from-scratch answer to "what sources should a commodities
sentiment monitor use." **Treat every entry as probation until a run proves
it**; promote winners into the working tables above, record failures under
dead ends. Entries marked (verify) were flagged by the consultation itself as
possibly stale.

### News wires & market data
Reuters Commodities (backbone wire, all legs) · Investing.com news/analysis ·
CNBC Commodities · MarketWatch Commodities (retail framing = crowdedness tell)
· Barchart daily market commentary + per-contract COT/"Opinion %" pages
(trend-crowdedness score) · TradingView per-symbol Ideas volume · OilPrice.com
· John Kemp — jkempenergy.com (verify home; the best free oil/gas
positioning notes) · NGI (Henry Hub cash color) · Kitco News · Mining.com
(copper/gold supply disruptions) · AgWeb · Successful Farming markets · DTN
Progressive Farmer (partial free).

### Trade / specialist press
Argus Media free news (physical crude differentials) · S&P Global/Platts free
headlines · RBN Energy daily blog (US gas/oil infrastructure — the natgas pro
read) · Celsius Energy (natgas weather models, verify) · Fastmarkets (physical
premia) · BullionVault/Adrian Ash · Silver Institute + World Gold Council
newsrooms · SMM metal.com English (China copper physical, Yangshan premium —
purest China demand signal) · World Grain / Grain Central · Pro Farmer
headlines (August crop tour = major ag sentiment event) · AgriCensus (verify
free layer).

### Official / agency (with schedules)
CFTC COT (Fri 3:30pm ET) · EIA petroleum (Wed) + gas storage (Thu) + STEO ·
USDA WASDE (~monthly noon ET), Export Sales (Thu), **FAS daily flash sales
≥100kt (intraday China-demand signal)**, Crop Progress (Mon) · OPEC MOMR + IEA
OMR (mid-month) · NOAA CPC 6-10/8-14 day outlooks (drives gas + ag weather
sentiment) · LME/SHFE/COMEX visible inventories · China customs data (via wire
pickups ~day 7-13) · CME FedWatch (gold/silver macro input) · Baker Hughes
(Fri).

### Social accounts (X unless noted)
@Ole_S_Hansen (Saxo — weekly COT breakdowns, all legs; highest-value single
follow) · @WarrenPies · @mikezaccardi · @Barchart (virality = crowdedness) ·
@JKempEnergy · @JavierBlas (physical oil color, tweets free) · @Amena__Bakr
(OPEC+ sourcing) · @CelsiusEnergyLLC (verify) · @RyanMaue + @BAMWXTeam
(weather) · @TaviCosta (PM narrative temperature) · @KitcoNewsNOW ·
@ColinLHamilton (verify) · #silversqueeze volume as froth gauge · @kannbwx
(Karen Braun — grain positioning, essential; verify affiliation) ·
@Eric_Snodgrass (ag weather, verify) · @ArlanFF101 (StoneX grains) ·
@SusanNOBULL (cash grain) · @AndreySizov (SovEcon — Black Sea wheat) ·
StockTwits streams $GLD $SLV $USO $UNG $CORN $WEAT $SOYB $CPER (native
bull/bear ratios).

### Sentiment / positioning trackers
Tradingster.com (cleanest free COT tables) · cotpricecharts.com (verify) ·
Saxo weekly COT note · Kitco Weekly Gold Survey (Wall St vs Main St split,
Fridays) · ApeWisdom (already in use) · SwaggyStocks / HypeEquity (verify) ·
CME QuikStrike free vol tools (options skew as positioning, verify free tier)
· GoldPrice.org fear/greed-style gauges.

### Underrated / contrarian
Hellenic Shipping News (republishes paywalled freight/tanker content free) ·
Kpler/Vortexa chart posts (floating storage = contrarian bearish tell) · SMM
Yangshan copper premium (falling premium vs rising COMEX = crowded long) ·
Reuters "Asia Gold" weekly column (Indian premia/discounts — physical buyers
strike at extremes) · Shanghai Gold Exchange premium vs London (verify
tracker) · CONAB Brazil + Rosario BCR + Buenos Aires Grain Exchange reports ·
SovEcon/IKAR Russian wheat estimates · soybeansandcorn.com (Cordonnier South
America crop scouting, free) · NASA Harvest / EU JRC MARS satellite crop
bulletins · US Drought Monitor (Thursdays, droughtmonitor.unl.edu) ·
GasBuddy/AAA pump prices (crude demand-side mood) · **Google Trends for "buy
gold" / "silver squeeze" / "gas prices" (honest retail-attention index)** ·
Kallanish / Mysteel English snippets (verify free layer).

## Known dead ends (do not retry)

- **Reddit directly** (any subreddit, any layer): network 403, crawler blocked, domain filter rejected. Use the trackers above instead.
- **apewisdom.io / altindex.com direct fetch**: 403 bot protection — their data is reachable only through search snippets.
- Generic "indicators and strategies" TradingView script pages: undated TA spam, no sentiment value.
