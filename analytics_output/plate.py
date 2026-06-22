"""Composite academic plate: the whole Day 2 story as one Figure (panels A-F)."""
import matplotlib.pyplot as plt
import theme as T
import panels as P


def build():
    T.apply()
    fig = plt.figure(figsize=(14, 16.4))

    # ---- master title block ----
    fig.text(0.055, 0.972, "THE DAY 2 CONTINUATION SETUP", color=T.GREEN,
             fontsize=14, fontweight="bold", family=T.SANS)
    fig.text(0.055, 0.945, "Anatomy of an institutional follow-through edge",
             color=T.INK, fontsize=30, fontweight="bold", family=T.SERIF)
    fig.text(0.055, 0.922,
             "841 fully-qualified Day 1 footprints — volume ≥ 3× ADV, move ≥ 2 ATR, "
             "extreme-quartile close — tracked into Day 2.",
             color=T.INK2, fontsize=13, family=T.SANS)
    fig.add_artist(plt.Line2D([0.055, 0.945], [0.908, 0.908], color=T.AXIS,
                              lw=1.0, transform=fig.transFigure))

    # ---- 3x2 grid ----
    L, R = 0.075, 0.975
    colgap = 0.085
    cw = (R - L - colgap) / 2
    cols = [L, L + cw + colgap]
    top, bot = 0.845, 0.118
    rowgap = 0.072
    rh = (top - bot - 2 * rowgap) / 3
    rows = [top - rh, top - rh - rowgap - rh, bot]   # row1,2,3 bottoms

    grid = [
        ("A", "Institutional-grade volume", P.panel_footprint, 0, 0),
        ("B", "A bimodal conviction fingerprint", P.panel_closeloc, 0, 1),
        ("C", "A catalyst nearly doubles the edge", P.panel_payoff, 1, 0),
        ("D", "Earnings shifts the distribution", P.panel_catalyst, 1, 1),
        ("E", "The extension paradox", P.panel_extension, 2, 0),
        ("F", "A persistent, year-round edge", P.panel_monthly, 2, 1),
    ]
    for letter, title, fn, r, c in grid:
        x, y = cols[c], rows[r]
        ax = fig.add_axes([x, y, cw, rh])
        fn(ax)
        fig.text(x - 0.012, y + rh + 0.018, letter, color=T.GREEN, fontsize=17,
                 fontweight="bold", family=T.SERIF, va="bottom")
        fig.text(x + 0.022, y + rh + 0.019, title, color=T.INK, fontsize=14,
                 fontweight="bold", family=T.SANS, va="bottom")

    # ---- caption / source ----
    fig.add_artist(plt.Line2D([0.055, 0.945], [0.052, 0.052], color=T.AXIS,
                              lw=1.0, transform=fig.transFigure))
    fig.text(0.055, 0.032,
             "Continuation = the Day 2 session opened gapped in the setup’s direction.  "
             "Bullish n = 495, bearish n = 346; earnings catalyst on 51% of setups.",
             color=T.INK3, fontsize=10.5, family=T.SANS)
    fig.text(0.055, 0.014,
             "Data: 841 Day 2 setups across 666 tickers, May 2025 – May 2026.",
             color=T.INK3, fontsize=10.5, family=T.SANS)

    fig.savefig("charts/plate_day2.png", dpi=200)
    plt.close(fig)
    print("saved charts/plate_day2.png")


if __name__ == "__main__":
    build()
