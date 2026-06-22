"""Polygon.io minute-bar fetcher with on-disk caching.
Key is read from $POLYGON_API_KEY or a local .env (never hard-coded)."""
import os, ssl, json, time, pathlib, urllib.request, urllib.error
import pandas as pd
try:
    import certifi
    SSLCTX = ssl.create_default_context(cafile=certifi.where())
except Exception:                       # fall back to system trust store
    SSLCTX = ssl.create_default_context()

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "intraday_cache"
CACHE.mkdir(exist_ok=True)


def load_key():
    k = os.environ.get("POLYGON_API_KEY")
    if k:
        return k.strip()
    envf = HERE / ".env"
    if envf.exists():
        for line in envf.read_text().splitlines():
            line = line.strip()
            if line.startswith("POLYGON_API_KEY"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError(
        "No Polygon key. Put POLYGON_API_KEY in env or analytics_output/.env")


def fetch_bars(ticker, date, key=None, multiplier=1, timespan="minute",
               max_retry=5):
    """Return raw Polygon results list for one ticker/day (cached)."""
    cf = CACHE / f"{ticker}_{date}_{timespan}.json"
    if cf.exists():
        return json.loads(cf.read_text())
    key = key or load_key()
    url = (f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/"
           f"{multiplier}/{timespan}/{date}/{date}"
           f"?adjusted=true&sort=asc&limit=50000&apiKey={key}")
    for attempt in range(max_retry):
        try:
            with urllib.request.urlopen(url, timeout=30, context=SSLCTX) as r:
                j = json.loads(r.read().decode())
            res = j.get("results", []) or []
            cf.write_text(json.dumps(res))
            return res
        except urllib.error.HTTPError as e:
            if e.code == 429:                      # rate limited -> back off
                time.sleep(2 ** attempt * 3)
                continue
            if e.code in (403, 401):
                raise RuntimeError(f"Polygon auth/plan error {e.code}: "
                                   f"{e.read().decode()[:200]}")
            time.sleep(1.5)
        except (urllib.error.URLError, TimeoutError):
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to fetch {ticker} {date} after {max_retry} tries")


def rth_frame(results):
    """Raw results -> regular-session (09:30-16:00 ET) minute DataFrame."""
    if not results:
        return pd.DataFrame()
    df = pd.DataFrame(results)
    df["ts"] = pd.to_datetime(df["t"], unit="ms", utc=True).dt.tz_convert(
        "America/New_York")
    df = df.rename(columns={"o": "open", "h": "high", "l": "low",
                            "c": "close", "v": "vol", "vw": "vwap"})
    mins = df["ts"].dt.hour * 60 + df["ts"].dt.minute
    df = df[(mins >= 570) & (mins < 960)].copy()        # 9:30 .. 16:00
    df["min_from_open"] = (mins - 570).reset_index(drop=True) if len(df) else []
    return df.reset_index(drop=True)


if __name__ == "__main__":   # connectivity smoke test
    key = load_key()
    print("Key loaded (…%s). Testing AAPL on 2025-05-01…" % key[-4:])
    r = fetch_bars("AAPL", "2025-05-01", key)
    d = rth_frame(r)
    print(f"  {len(d)} RTH minute bars; first {d.ts.iloc[0]}  last {d.ts.iloc[-1]}")
    print(d[["ts", "open", "high", "low", "close", "vol", "vwap"]].head(3).to_string(index=False))
