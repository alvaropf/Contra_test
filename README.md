# Contrarian Cascade

Five mechanical gates applied in sequence to 122 ETFs and 181 cross-asset ratios. A candidate has to clear every gate independently — there is no score, and nothing compensates for anything else.

---

## The cascade

| # | Gate | Default | Measures |
|---|------|---------|----------|
| 1 | Depth | ≤ −35% from the 5-year high | Long-horizon reversal. Value, not momentum. |
| 2 | Duration | ≥ 12 months since that peak | Removes crashes still in progress, and freshly unwound parabolas. |
| 3 | No new lows | 126–504 days since the last 252-day low | The definitional condition. Bounded on both sides. |
| 4 | Curvature | 100d MA slope > 0 **and** price > MA100 | Has the downtrend actually stopped bending down. |
| 5 | Vol contraction | RV percentile < 30 now, > 70 within 18m | Compression *following* expansion. |

Gates are evaluated strictly in order. `stage` is the number of consecutive gates cleared, 0 to 5. A row that fails gate 2 never has gates 3–5 evaluated, and the table marks them as not reached rather than as failures.

### Why a cascade and not a weighted score

A score lets a strong reading on depth compensate for a failed exhaustion test. Those conditions are not fungible: depth without exhaustion is a falling knife, and exhaustion without depth is an asset that was never punished. Requiring each condition independently is what "the setup exists" actually means.

The cost is sample size. Five gates that each pass a third of the universe would leave under one percent if they were independent. They are not — deep drawdowns are where volatility contraction happens — but the attrition still bites, which is why the funnel is the first thing on the page.

---

## Reading the funnel

Six bars: the universe, then the survivors after each gate, with the count filtered at each step underneath.

- **One gate doing all the eliminating** means the others are decorative and the screen is that gate wearing a costume.
- **A final bar of two or three** is the screen telling you the setup is absent right now, not handing you a shortlist. Loosening thresholds until something appears is how you turn a screen into a random number generator.
- Gates you switch off show as greyed bars and pass the count straight through.

---

## Asymmetry is not a gate

The gates decide whether the setup exists. Whether you want it is separate, and continuous. Each expanded row reports:

- **Risk to base low** — distance down to the level whose violation falsifies the thesis. Gate 3 hands you this level; that is most of its practical value.
- **Upside to prior high** — distance up to the gate-1 reference.
- **Payoff ratio** — the second divided by the first.

A name that cleared depth by 60% but sits far above its invalidation level is a worse holding than one that barely cleared at 36% and sits just above it. Sort on payoff, not on stage.

---

## Presets

| Preset | What it does |
|---|---|
| **Strict** | 45% depth, 15 months, 160–420 days, slope > 2%/yr, vol below the 20th after the 80th. Expect a handful or an empty screen. |
| **Default** | The table above. |
| **Loose** | 25% depth, 9 months, 90–630 days, slope > −6%, no price-above-MA requirement, vol below the 45th. |
| **Watchlist** | Gate 4 switched off. Gates 1, 2, 3 and 5 put something on the list; you turn gate 4 on later as the trigger. |

The Watchlist preset exists because gate 4 is the slowest to confirm and will often fire months after gate 5 — the base has to build before a moving average can turn. Running the screen without it and applying it later separates "this is interesting" from "this is now."

---

## Parameters

Everything is exposed and every change recomputes locally in the browser. Re-fetching prices is only needed when the universe changes.

**Gate 1** — minimum drawdown; look-back window for the high (3–6y); reference high as **highest close** or **highest 60-day mean**.

The reference-high option is for the parabola problem. An asset that doubles and halves is mechanically 50% off its high while sitting exactly where it started, because a single print set the reference. Using the highest trailing 60-day mean leaves a sustained top almost unchanged and strips most of the height out of a short spike. It is not an extra gate, just a different reference price — the default is highest close.

**Gate 2** — minimum and maximum age of the peak. The maximum defaults to off.

**Gate 3** — minimum and maximum days since the last new low, and the new-low window (126/189/252/378 days). The maximum is what stops a quiet perennial sideways asset from qualifying: it requires that a low actually happened within the past two years.

**Gate 4** — method (MA slope, or quadratic on log price); MA length; slope window; minimum slope in %/yr; whether to require price above the MA.

MA slope alone has a base effect: the average moves by the new bar minus the dropped bar, so a large down day rolling out of the window can turn the slope positive with no new information in current price. Requiring price above the MA closes that hole, because price above an average cannot be produced by old data leaving the sample. Shortening the MA makes the artifact worse per event, not better, which is why the price condition ships on by default. The quadratic alternative fits `log(P) = at² + bt + c` over the trailing window and requires `a > 0` (bowl-shaped) and `2a + b > 0` (rising at the right edge). It measures the second derivative directly and has no base effect by construction; it typically confirms 2–4 months after the low versus 6–10 for an MA200 slope.

**Gate 5** — volatility window; current percentile ceiling; prior peak percentile floor; how far back to look for that peak; length of the percentile history.

The two-part structure is the point. Compression alone picks up assets that have simply always been quiet. Compression after expansion is what a base looks like, and it is the condition that makes the eventual move violent.

---

## Universe

122 ETFs, grouped into fixed income, commodities, resource equities, developed markets, emerging markets, technology and themes, US broad and style, US sectors, and US industries.

Fifteen tickers were removed from the source list. Three are structurally broken for this purpose:

| Ticker | Why |
|---|---|
| **UNG** | Roll decay — down over 99% since inception on carry alone. Clears any depth gate every day of its existence and never reverts. |
| **USO** | Same problem at smaller magnitude, plus the April 2020 forced methodology change. Not a clean oil series. |
| **UGA** | Same roll-decay structure. |

The other twelve are duplicates that would produce two events for one observation: **GLTR** (a basket of four metals held individually), **VTI** (≈SPY), **IEFA** (≈VEA, which has five more years of history), **ACWI** (≈SPY + ACWX), **AIA** (≈AAXJ), **EPI** (≈INDA), **OEF** (≈SPY), **IGM** (spanned by XLK/SMH/IGV/SKYY), **VTV** (≈IWD), **MGK** (≈IWF), **IAT** (≈KRE), **XLRE** (≈RWR, which starts in 2001 rather than 2015).

Add any of them back through the Universe editor. GSG and DBC also carry roll cost, but bounded rather than unbounded, and they stay in.

---

## Ratios

181 pairs across eleven classes: cross-asset, fixed income, commodity, miners vs metal, region, country vs EM, Europe, style and size, sector vs market, industry vs market, and intra-sector.

The same five gates run on each ratio series. Ratio drawdown is measured in log space, so a fall from 1.0 to 0.5 and one from 0.5 to 0.25 are the same event.

Nothing here assumes a ratio mean-reverts. That matters, because most macro ratios are regime-switching with very long regimes rather than stationary — a z-score against a fixed window would have had you long commodities in 1998 and short in 2008, both wrong at the extreme. The cascade is drawdown- and duration-based, so it makes no stationarity assumption. What it remains exposed to is regime persistence: a ratio can clear every gate and then resume a fifteen-year secular decline.

The intra-sector block carries the most information. XBI/IBB strips out large-cap pharma and reads pure speculative biotech appetite; KRE/KBE isolates regional bank stress from the sector; IGV/SMH separates software from hardware, two genuinely different cycles that a vs-SPY ratio blurs together. The sector-vs-market block duplicates the absolute screen more than the others do, since in a rising market a sector ratio and the sector itself hit depth and exhaustion at nearly the same time. Cut there first if you want to trim.

---

## Data

`api/snapshot.py` is a Vercel Python function that pulls adjusted daily closes with yfinance and returns a columnar payload:

```
GET /api/snapshot?tickers=SPY,QQQ,...
→ { "dates": ["2019-01-02", ...],
    "series": { "SPY": [123.4567, null, ...] },
    "meta": { "bars": 1764, "count": 40, "missing": [] } }
```

- Seven years of history, capped at 1850 bars. The gates need a five-year window for depth plus a five-year distribution for the volatility percentile.
- One shared date index instead of per-bar objects. That is what keeps a 40-ticker chunk near 1 MB instead of 3 MB, comfortably inside Vercel's response limit.
- `auto_adjust=True`, so closes are dividend- and split-adjusted. This is not optional. On price returns alone, HYG/IEF drifts down about four points a year from the yield differential — enough to clear a 35% depth gate over fifteen years with nothing economic behind it. The same applies to XLU/SPY, RWR/SPY and IWD/IWF.
- The client fetches in chunks of 40 with a progress bar, so no single function call approaches the 60-second limit.
- Six-hour in-memory cache on warm instances plus edge caching.
- A ticker yfinance cannot deliver appears in `meta.missing`, renders as **No data**, and is dropped from the funnel, the ratios and the composites. Nothing is mocked or padded.

Volatility is computed from closes rather than true range. The ratios have no meaningful high and low, and consistency across the two screens is worth more than the small gain from intraday data.

---

## Running it

```bash
npm i -g vercel
vercel dev          # runs the Python function locally too
vercel --prod       # deploy
```

`npx serve .` will render the page but has no `/api`, so the scan will fail.

---

## What this does not do

It is a live screen, not a backtest, and not investment advice.

**No base rate.** Of all the assets that clear a deep drawdown plus six months without a new low, some meaningful fraction go on to make a new low anyway. That number is the honest measure of what the screen is up against, and only an event study over several decades will produce it.

**No non-price anchor.** The cascade is fully mechanical, which makes it clean and testable, and leaves it exposed to assets in terminal decline. Gate 3 absorbs more of that than you would expect — things going to zero keep making new lows and never accumulate 126 clean days — but the slow-obsolescence case survives: no crash, just a decade of grinding lower with periodic sideways pauses that clear every gate.

**No clustering adjustment.** Events cluster in time. One bad October will fire forty of these at once across correlated series. That is one observation, not forty, and the screen has no way to tell you so.
