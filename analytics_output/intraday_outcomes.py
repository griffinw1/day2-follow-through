"""Compute realized Day-2 intraday outcomes from Polygon minute bars.
Outputs pilot_outcomes.csv (scalar metrics) + pilot_paths.parquet (aligned
open-anchored signed return path, minute 0..389, for the event-study figure)."""
import sys, numpy as np, pandas as pd
import polygon_fetch as PF

GRID = np.arange(0, 390)          # RTH minutes from the open


def tod_bucket(m):
    if m < 30:   return "Open (0-30m)"
    if m < 120:  return "Morning"
    if m < 300:  return "Mid-day"
    return "Afternoon"


def one_setup(row, key):
    d2 = PF.rth_frame(PF.fetch_bars(row.TICKER, str(row.DATE)[:10], key))
    if len(d2) < 30:
        return None, None
    sign = 1.0 if row.DIRECTION == "BULLISH" else -1.0
    atr = float(row.ATR14) or np.nan
    entry = float(d2["open"].iloc[0])               # Day-2 open
    hi, lo = d2["high"].max(), d2["low"].min()
    last = float(d2["close"].iloc[-1])

    fav_px = (hi - entry) if sign > 0 else (entry - lo)     # favorable excursion
    adv_px = (entry - lo) if sign > 0 else (hi - entry)     # adverse excursion
    fav_px, adv_px = max(fav_px, 0.0), max(adv_px, 0.0)

    # timing of the favorable extreme
    ext_idx = d2["high"].idxmax() if sign > 0 else d2["low"].idxmin()
    t_mfe = int(d2["min_from_open"].iloc[ext_idx])

    # morning test depth (first 60 min adverse poke) and Day-1-extreme/phase
    first60 = d2[d2["min_from_open"] < 60]
    test_px = (entry - first60["low"].min()) if sign > 0 else (first60["high"].max() - entry)
    d1_ext = row.D1_HIGH if sign > 0 else row.D1_LOW
    reached = (hi >= d1_ext) if sign > 0 else (lo <= d1_ext)
    beyond_px = (hi - d1_ext) if sign > 0 else (d1_ext - lo)

    m = dict(
        TICKER=row.TICKER, DATE=str(row.DATE)[:10], DIRECTION=row.DIRECTION,
        EARNINGS_D1=int(row.EARNINGS_D1), ADV_MULT=row.D1_ADV_MULT,
        n_bars=len(d2), entry=entry,
        ret_close=sign * (last / entry - 1) * 100,
        mfe_pct=fav_px / entry * 100, mae_pct=adv_px / entry * 100,
        mfe_atr=fav_px / atr, mae_atr=adv_px / atr,
        open_gap_atr=sign * (entry - row.D1_CLOSE) / atr,
        test_atr=max(test_px, 0.0) / atr,
        reached_d1=bool(reached),
        beyond_d1_atr=(beyond_px / atr) if reached else 0.0,
        t_mfe=t_mfe, mfe_bucket=tod_bucket(t_mfe),
        win=bool(last > entry if sign > 0 else last < entry),
    )

    # aligned open-anchored signed return path (%)
    s = d2.set_index("min_from_open")["close"].reindex(GRID).ffill().bfill()
    path = sign * (s / entry - 1) * 100
    return m, path.values


def run(setups_csv="pilot_setups.csv"):
    key = PF.load_key()
    setups = pd.read_csv(setups_csv, parse_dates=["DATE", "D1_DATE"])
    rows, paths, miss = [], [], []
    for i, row in enumerate(setups.itertuples(index=False), 1):
        try:
            m, p = one_setup(row, key)
        except Exception as e:
            m, p = None, None
            print(f"  ! {row.TICKER} {str(row.DATE)[:10]}: {e}")
        if m is None:
            miss.append(row.TICKER); continue
        rows.append(m); paths.append(p)
        print(f"[{i:>2}/{len(setups)}] {row.TICKER:<6} {row.DIRECTION[:4]} "
              f"earn={int(row.EARNINGS_D1)}  close={m['ret_close']:+5.1f}%  "
              f"MFE={m['mfe_atr']:.2f} MAE={m['mae_atr']:.2f} ATR")
    out = pd.DataFrame(rows)
    out.to_csv("pilot_outcomes.csv", index=False)
    pathdf = pd.DataFrame(paths, columns=[f"m{m}" for m in GRID])
    pathdf.insert(0, "TICKER", out["TICKER"]); pathdf.insert(1, "DIRECTION", out["DIRECTION"])
    pathdf.insert(2, "EARNINGS_D1", out["EARNINGS_D1"])
    pathdf.to_parquet("pilot_paths.parquet")
    print(f"\nDone. {len(out)} setups with data, {len(miss)} missing {miss}")
    print("Saved pilot_outcomes.csv + pilot_paths.parquet")
    return out


if __name__ == "__main__":
    run(*(sys.argv[1:2] or []))
