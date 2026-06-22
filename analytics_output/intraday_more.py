"""Fig 9 — entry rule comparison (open vs test-and-flip).
Fig 10 — trade-card small multiples (representative setups)."""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import theme as T, polygon_fetch as PF

OUT = pd.read_csv("pilot_outcomes.csv")
FLIP = pd.read_csv("pilot_flip.csv")
SET = pd.read_csv("pilot_setups.csv", parse_dates=["DATE"])
KEY = PF.load_key()


# ---------------------------------------------------- Fig 9: entry comparison
def fig_entry_compare():
    T.apply()
    fig = plt.figure(figsize=(12, 7.6))
    ax = fig.add_axes([0.085, 0.16, 0.86, 0.58])
    f = FLIP[FLIP.has_trade]
    cells = ["BULLISH", "BEARISH"]
    open_med = [OUT[OUT.DIRECTION == d].ret_close.median() for d in cells]
    flip_med = [f[f.DIRECTION == d].ret_pct.median() for d in cells]
    flip_exp = [f[f.DIRECTION == d].ret_R.mean() for d in cells]
    flip_win = [(f[f.DIRECTION == d].ret_R > 0).mean()*100 for d in cells]
    x = np.arange(2)
    w = 0.36
    b1 = ax.bar(x - w/2, open_med, w, color=T.GREY, zorder=3, label="buy/short the OPEN")
    b2 = ax.bar(x + w/2, flip_med, w, color=[T.GREEN, T.RED], zorder=3,
                label="TEST-AND-FLIP entry")
    ax.axhline(0, color=T.INK2, lw=1.1, zorder=2)
    for xi, v in zip(x - w/2, open_med):
        ax.annotate(f"{v:+.1f}%", (xi, v), ha="center",
                    va="top" if v < 0 else "bottom",
                    xytext=(0, -4 if v < 0 else 4), textcoords="offset points",
                    color=T.GREY_L, fontsize=12, fontweight="bold")
    for xi, v, e, wn in zip(x + w/2, flip_med, flip_exp, flip_win):
        ax.annotate(f"{v:+.1f}%", (xi, v), ha="center", va="bottom",
                    xytext=(0, 4), textcoords="offset points", color=T.INK,
                    fontsize=12, fontweight="bold")
        ax.annotate(f"{e:+.2f}R  ·  {wn:.0f}% win", (xi, v),
                    ha="center", va="bottom", xytext=(0, 22),
                    textcoords="offset points", color=T.GREEN_L if v>0 else T.RED_L,
                    fontsize=10.5, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(["BULLISH  (long)", "BEARISH  (short)"],
                                         fontsize=12, fontweight="bold")
    ax.set_ylabel("median Day-2 return  (%)")
    ax.set_ylim(min(open_med)-0.8, max(flip_med)+1.6)
    ax.legend(loc="upper left", fontsize=11)
    T.clean(ax)
    T.fig_header(fig, 9, "The entry rule is the edge",
                 "Buying the open loses on the long side; waiting for the flip turns it positive")
    T.source_note(fig, "Pilot n=51. Open = open-to-close; flip = test-to-flip entry, stop below the turn. R = risk to that stop")
    fig.savefig("charts/entry_compare.png", dpi=200)
    plt.close(fig)
    print("saved charts/entry_compare.png")


# ------------------------------------------------------- Fig 10: trade cards
def _sim_exit(df, dirn, entry_t, entry, stop):
    post = df[df.min_from_open >= entry_t]
    for b in post.itertuples():
        if (dirn == "BULLISH" and b.low <= stop) or (dirn == "BEARISH" and b.high >= stop):
            return int(b.min_from_open), stop
    return int(post["min_from_open"].iloc[-1]), float(post["close"].iloc[-1])


def fig_trade_cards():
    T.apply()
    f = FLIP[FLIP.has_trade].reset_index(drop=True)
    order = f.sort_values("ret_R").reset_index(drop=True)          # worst -> best
    pick = order.iloc[np.linspace(0, len(order)-1, 12).astype(int)]  # representative spread
    fig = plt.figure(figsize=(14, 9))
    fig.text(0.5, 0.965, "FIGURE 10", color=T.GREEN, fontsize=12, fontweight="bold",
             ha="center", family=T.SANS)
    fig.text(0.5, 0.93, "Twelve trades, worst to best", color=T.INK, fontsize=24,
             fontweight="bold", ha="center", family=T.SERIF)
    fig.text(0.5, 0.902, "minute close from the open  ·  dashed grey = VWAP  ·  faint = Day-1 levels  ·  triangle = flip entry  ·  X = exit  ·  dashed red = stop",
             color=T.INK2, fontsize=11, ha="center", family=T.SANS)
    rows, cols = 3, 4
    L, Rr, Tt, Bb, hg, vg = 0.045, 0.985, 0.875, 0.05, 0.035, 0.075
    cw = (Rr - L - (cols-1)*hg) / cols
    ch = (Tt - Bb - (rows-1)*vg) / rows
    for i, (_, r) in enumerate(pick.iterrows()):
        rr, cc = divmod(i, cols)
        ax = fig.add_axes([L + cc*(cw+hg), Tt - ch - rr*(ch+vg), cw, ch])
        df = PF.rth_frame(PF.fetch_bars(r.TICKER, r.DATE, KEY))
        s = SET[(SET.TICKER == r.TICKER) & (SET.DATE == r.DATE)].iloc[0]
        m = df.min_from_open.values
        vwap = (df.vwap*df.vol).cumsum()/df.vol.cumsum()
        win = r.ret_R > 0
        ax.plot(m, df.close, color=T.INK, lw=1.0, zorder=4)
        ax.plot(m, vwap, color=T.GREY, lw=1.0, ls=(0, (3, 2)), zorder=3)
        for lv, lc in [(s.D1_HIGH, T.GREY_D), (s.D1_LOW, T.GREY_D), (s.D1_CLOSE, T.STEEL if hasattr(T,'STEEL') else T.GREY)]:
            if df.low.min() <= lv <= df.high.max():
                ax.axhline(lv, color=T.GREY_D, lw=0.7, zorder=2)
        ax.axhline(r.stop, color=T.RED, lw=0.9, ls=(0, (2, 2)), zorder=3)
        mk = "^" if r.DIRECTION == "BULLISH" else "v"
        ec = T.GREEN if win else T.RED
        ax.scatter([r.entry_t], [r.entry], marker=mk, s=70, color=ec,
                   edgecolor=T.BG, linewidth=0.7, zorder=6)
        ext, exp = _sim_exit(df, r.DIRECTION, r.entry_t, r.entry, r.stop)
        ax.scatter([ext], [exp], marker="x", s=46, color=T.INK, linewidth=1.6, zorder=6)
        ax.set_xlim(0, 390); ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color(ec); sp.set_linewidth(1.4)
        tag = "WIN" if win else "LOSS"
        ax.set_title(f"{r.TICKER}  ·  {r.DIRECTION[:4]}  ·  {r.ret_R:+.1f}R",
                     color=ec, fontsize=11, fontweight="bold", pad=3)
    fig.savefig("charts/trade_cards.png", dpi=200)
    plt.close(fig)
    print("saved charts/trade_cards.png")


if __name__ == "__main__":
    fig_entry_compare()
    fig_trade_cards()
