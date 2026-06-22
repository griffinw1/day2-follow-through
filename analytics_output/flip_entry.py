"""The *real* playbook entry: morning Test -> Character Flip -> enter, stop below
the turn, one invalidation. Rule-based so it's backtestable. Compares the
realized flip-entry trade to the naive open-entry baseline.

BULLISH: turn = lowest low in first 90m; flip = first GREEN higher-high bar after
the turn; entry = flip close; stop = turn low; exit = stop-hit or session close.
BEARISH: mirror (turn = highest high; flip = first RED lower-low bar; stop = turn high)."""
import numpy as np, pandas as pd
import polygon_fetch as PF

TEST_WIN = 90          # minutes the morning test may form in
R_FLOOR = 0.05         # min risk as fraction of ATR (avoid degenerate tiny-R)


def _flip_long(df, atr):
    tw = df[df.min_from_open < TEST_WIN]
    if len(tw) < 5:
        return None
    ti = tw["low"].idxmin()
    turn_lo, turn_t = df.loc[ti, "low"], df.loc[ti, "min_from_open"]
    after = df[df.min_from_open > turn_t].reset_index(drop=True)
    flip = None
    for j in range(1, len(after)):
        b, p = after.iloc[j], after.iloc[j - 1]
        if b.close > b.open and b.high > p.high:
            flip = b; break
    if flip is None:
        return None
    entry, stop = float(flip.close), float(turn_lo)
    R = max(entry - stop, R_FLOOR * atr)
    post = df[df.min_from_open >= flip.min_from_open]
    stopped, exit_px = False, float(post["close"].iloc[-1])
    for b in post.itertuples():
        if b.low <= stop:
            stopped, exit_px = True, stop; break
    mfe = (post["high"].max() - entry); mae = (entry - post["low"].min())
    return dict(turn_t=turn_t, entry_t=int(flip.min_from_open), entry=entry,
                stop=stop, R=R, exit=exit_px, stopped=stopped,
                ret_R=(exit_px - entry) / R, ret_pct=(exit_px / entry - 1) * 100,
                mfe_R=mfe / R, mae_R=mae / R, risk_atr=(entry - stop) / atr)


def _flip_short(df, atr):
    tw = df[df.min_from_open < TEST_WIN]
    if len(tw) < 5:
        return None
    ti = tw["high"].idxmax()
    turn_hi, turn_t = df.loc[ti, "high"], df.loc[ti, "min_from_open"]
    after = df[df.min_from_open > turn_t].reset_index(drop=True)
    flip = None
    for j in range(1, len(after)):
        b, p = after.iloc[j], after.iloc[j - 1]
        if b.close < b.open and b.low < p.low:
            flip = b; break
    if flip is None:
        return None
    entry, stop = float(flip.close), float(turn_hi)
    R = max(stop - entry, R_FLOOR * atr)
    post = df[df.min_from_open >= flip.min_from_open]
    stopped, exit_px = False, float(post["close"].iloc[-1])
    for b in post.itertuples():
        if b.high >= stop:
            stopped, exit_px = True, stop; break
    mfe = (entry - post["low"].min()); mae = (post["high"].max() - entry)
    return dict(turn_t=turn_t, entry_t=int(flip.min_from_open), entry=entry,
                stop=stop, R=R, exit=exit_px, stopped=stopped,
                ret_R=(entry - exit_px) / R, ret_pct=(1 - exit_px / entry) * 100,
                mfe_R=mfe / R, mae_R=mae / R, risk_atr=(stop - entry) / atr)


def run(setups_csv="pilot_setups.csv"):
    key = PF.load_key()
    sx = pd.read_csv(setups_csv, parse_dates=["DATE"])
    rows = []
    for row in sx.itertuples(index=False):
        df = PF.rth_frame(PF.fetch_bars(row.TICKER, str(row.DATE)[:10], key))
        if len(df) < 30:
            continue
        atr = float(row.ATR14)
        r = (_flip_long if row.DIRECTION == "BULLISH" else _flip_short)(df, atr)
        rec = dict(TICKER=row.TICKER, DATE=str(row.DATE)[:10], DIRECTION=row.DIRECTION,
                   EARNINGS_D1=int(row.EARNINGS_D1), has_trade=r is not None)
        if r:
            rec.update(r)
            rec["clean_hold"] = bool(r["turn_t"] < 10)
        rows.append(rec)
    out = pd.DataFrame(rows)
    out.to_csv("pilot_flip.csv", index=False)
    t = out[out.has_trade].copy()
    print(f"\n===== TEST-AND-FLIP ENTRY (realized, n={len(t)} valid trades / {len(out)}) =====")

    def blk(name, s):
        if not len(s):
            return f"{name:<24} (none)"
        exp = s.ret_R.mean()
        return (f"{name:<24} n={len(s):>2}  win={ (s.ret_R>0).mean()*100:4.0f}%  "
                f"expectancy={exp:+.2f}R  median={s.ret_R.median():+.2f}R  "
                f"stopped={s.stopped.mean()*100:3.0f}%  entry@{s.entry_t.median():.0f}m")
    print(blk("ALL", t))
    print(blk("  BULLISH", t[t.DIRECTION == "BULLISH"]))
    print(blk("  BEARISH", t[t.DIRECTION == "BEARISH"]))
    print(blk("  bullish+earnings", t[(t.DIRECTION=='BULLISH')&(t.EARNINGS_D1==1)]))
    print(blk("  bearish+earnings", t[(t.DIRECTION=='BEARISH')&(t.EARNINGS_D1==1)]))
    print(blk("  test (pullback)", t[~t.clean_hold]))
    print(blk("  clean hold", t[t.clean_hold]))
    print("\nSaved pilot_flip.csv")
    return out


if __name__ == "__main__":
    run()
