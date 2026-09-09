"""
/api/snapshot?tickers=SPY,QQQ,...  —  adjusted daily closes for the cascade scanner.

Returns a columnar payload so the whole universe fits inside Vercel's response
limit: one shared date index, then one array of closes per ticker with nulls
where a series has no bar.

    { "dates": ["2019-01-02", ...],
      "series": { "SPY": [123.4567, null, ...], ... },
      "meta":   { "bars": 1764, "count": 40, "missing": ["XYZ"] } }

auto_adjust=True gives dividend- and split-adjusted closes. That matters here:
on price returns alone a ratio like HYG/IEF drifts down about four points a year
from the yield differential, which is enough to clear a 35% depth gate over
fifteen years with no economic content behind it.

Tickers yfinance cannot deliver are listed in meta.missing and are absent from
series. Nothing is ever mocked or padded.
"""

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
import json
import math

import pandas as pd
import yfinance as yf

YEARS_HISTORY = 7          # gates need a 5y window plus buffer for the vol history
MAX_BARS = 1850
CHUNK = 20                 # one bad ticker cannot sink the rest of the batch
MAX_TICKERS = 60           # the client fetches in chunks of 40
MIN_BARS = 300
FFILL_LIMIT = 5            # bridges real holidays, cannot fabricate a flat tail

_cache = {}                # key -> {"data": dict, "ts": datetime}
CACHE_SECONDS = 21600      # 6 hours; daily closes change once a day


def _download(batch, start):
    return yf.download(
        batch,
        start=start,
        interval="1d",
        auto_adjust=True,
        group_by="ticker",
        threads=True,
        progress=False,
    )


def build_snapshot(tickers):
    start = (datetime.utcnow() - timedelta(days=int(YEARS_HISTORY * 365.25))).strftime("%Y-%m-%d")
    cols = {}

    for i in range(0, len(tickers), CHUNK):
        batch = tickers[i:i + CHUNK]
        try:
            raw = _download(batch, start)
        except Exception as exc:                      # noqa: BLE001
            print(f"chunk starting {batch[0]} failed: {exc}")
            continue
        if raw is None or raw.empty:
            continue

        if isinstance(raw.columns, pd.MultiIndex):
            present = set(raw.columns.get_level_values(0))
            for sym in batch:
                if sym not in present:
                    continue
                sub = raw[sym]
                if "Close" not in sub.columns:
                    continue
                s = sub["Close"].ffill(limit=FFILL_LIMIT).dropna()
                if len(s) >= MIN_BARS:
                    cols[sym] = s
        else:
            if "Close" in raw.columns and batch:
                s = raw["Close"].ffill(limit=FFILL_LIMIT).dropna()
                if len(s) >= MIN_BARS:
                    cols[batch[0]] = s

    if not cols:
        return {"dates": [], "series": {}, "meta": {"bars": 0, "count": 0, "missing": tickers}}

    frame = pd.concat(cols, axis=1).sort_index().tail(MAX_BARS)
    dates = [ts.strftime("%Y-%m-%d") for ts in frame.index]

    series = {}
    for sym in frame.columns:
        vals = []
        for v in frame[sym].tolist():
            vals.append(None if v is None or (isinstance(v, float) and math.isnan(v)) else round(float(v), 4))
        series[sym] = vals

    missing = [t for t in tickers if t not in series]
    return {
        "dates": dates,
        "series": series,
        "meta": {"bars": len(dates), "count": len(series), "missing": missing},
    }


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            qs = parse_qs(urlparse(self.path).query)
            raw = (qs.get("tickers", [""])[0] or "").upper()

            tickers, seen = [], set()
            for tok in raw.split(","):
                tok = tok.strip()
                if tok and tok not in seen:
                    seen.add(tok)
                    tickers.append(tok)
            tickers = tickers[:MAX_TICKERS]
            if not tickers:
                raise ValueError("No tickers requested. Call /api/snapshot?tickers=SPY,QQQ")

            key = ",".join(sorted(tickers))
            entry = _cache.get(key)
            if entry is None or (datetime.utcnow() - entry["ts"]).total_seconds() > CACHE_SECONDS:
                entry = {"data": build_snapshot(tickers), "ts": datetime.utcnow()}
                _cache[key] = entry

            body = json.dumps(entry["data"], separators=(",", ":"))
            status = 200
        except Exception as exc:                       # noqa: BLE001
            import traceback
            body = json.dumps({"error": str(exc), "traceback": traceback.format_exc()})
            status = 500

        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "public, s-maxage=21600, stale-while-revalidate=86400")
        self.end_headers()
        self.wfile.write(body.encode())

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()

    def log_message(self, *args):
        pass
