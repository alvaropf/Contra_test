# Contrarian Cascade

Five gates, evaluated in order, on 122 ETFs and 181 cross-asset ratios. A candidate clears each gate independently — there is no score, and nothing compensates for anything else.

| # | Gate | Tunable | Fixed |
|---|------|---------|-------|
| 1 | Depth | minimum drawdown (35%) | measured from the highest close of the last 5 years |
| 2 | Duration | minimum age of that peak (12m) | — |
| 3 | No new lows | minimum days since the last 252-day low (126) | capped at 504 days so the damage stays recent |
| 4 | Curvature | on / off | 100-day average rising over 60 sessions, and price above it |
| 5 | Vol contraction | current percentile ceiling (30th) | ranked over 5 years; must have exceeded the 70th within 18 months |

Four sliders, one checkbox, three presets. Everything else is held constant and documented in the Method section at the bottom of the page.

---

## Using it

**Run scan** pulls seven years of adjusted closes in chunks of 40, with a progress readout. Every knob after that recomputes locally — a re-fetch is only needed if you change the asset list.

The default view shows anything clearing **4 or 5 gates**, assets and ratios together in one table. Use the segmented control to isolate one or the other, and the dropdown to widen to 3+ or narrow to 5 only.

**Click any row** for the full chart: log-scale price or ratio over five years with the 100- and 200-day averages, the gate-1 reference high and the base low as dashed lines, a marker on the last 252-day low, and the stretch without a new low shaded. Underneath it, the volatility percentile path with the two thresholds gate 5 tests against, so you can see whether the compression actually followed an expansion. Escape or a click outside closes it.

**The funnel strip** in the header is the count surviving each gate, one line for assets and one for ratios. If a single gate eliminates almost everything and the rest eliminate nothing, the screen is that gate wearing a costume. If the last number reads two, the setup is absent right now — that is a result, not a prompt to loosen thresholds.

**Presets.** Strict is 45% / 15 months / 160 days / 20th percentile. Balanced is the default. Loose is 25% / 9 months / 90 days / 45th.

**The curvature checkbox** is the watchlist switch. Gate 4 is the slowest to confirm — the base has to build before an average can turn — so it will often fire months after gate 5. Turn it off, let gates 1, 2, 3 and 5 build the list, and use the turn as your entry trigger.

---

## Asymmetry

The gates decide whether the setup exists. Whether you want it is separate and continuous. Every row and every chart panel reports the distance down to the base low, the distance up to the prior high, and the ratio between them. Gate 3 is what hands you that invalidation level, which is most of its practical value. Sort on payoff, not on stage.

---

## Universe

122 ETFs across fixed income, commodities, resource equities, developed and emerging markets, technology and themes, US broad and style, US sectors and US industries. 181 ratios across eleven classes, including a large intra-sector block (XBI/IBB, KRE/KBE, IGV/SMH and so on) which carries more information than the sector-vs-market ratios.

Fifteen tickers were cut from the source list. **UNG, USO and UGA** are structurally broken for this purpose — roll decay means UNG clears any depth gate every day of its existence and never reverts. The other twelve are duplicates that would produce two events for one observation: GLTR, VTI, IEFA, ACWI, AIA, EPI, OEF, IGM, VTV, MGK, IAT, XLRE. All fifteen are listed with reasons at the bottom of the Method section, and any can be pasted back through the list editor in the Tune panel.

---

## Data

`api/snapshot.py` pulls adjusted daily closes with yfinance and returns a columnar payload — one shared date index plus one array per ticker — which keeps a 40-ticker chunk near 1 MB rather than 3 MB.

`auto_adjust=True` is not optional. On price returns alone, HYG/IEF drifts down about four points a year from the yield differential, which would clear a 35% depth gate over fifteen years with nothing economic behind it. The same applies to XLU/SPY, RWR/SPY and IWD/IWF.

Volatility is computed from closes rather than true range, because ratios have no meaningful high and low and consistency across the two screens is worth more than the small gain from intraday data.

A ticker yfinance cannot deliver is dropped, not filled. Nothing is mocked.

---

## Deploying

Repo root must look like this — `api/` and `index.html` at the top level, `requirements.txt` **inside** `api/` so Vercel treats the file as a serverless function rather than autodetecting a Python application:

```
index.html
vercel.json
package.json
api/
  snapshot.py
  requirements.txt
```

```bash
vercel dev      # local, runs the Python function too
vercel --prod   # deploy
```

---

## Limits

A live screen, not a backtest, and not investment advice. It cannot tell you the base rate — of everything clearing a deep drawdown plus six months without a new low, some meaningful fraction makes a new low anyway, and only an event study over decades will say what fraction. It has no non-price anchor, so an asset in genuine terminal decline can clear every gate. And events cluster: one bad October fires forty of these at once, which is one observation and not forty.
