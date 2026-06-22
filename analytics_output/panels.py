"""Day 2 study — dark-academic figures. Each panel draws onto a given Axes so
the same logic powers standalone figures and the composed multi-panel plate."""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import theme as T

DF = pd.read_parquet("/tmp/day2_enriched.parquet")
OVERALL = (DF.DIR_GAP > 0).mean() * 100


def _rate(x):
    return (x > 0).mean() * 100


def _vlabel(ax, bars, vals, dy=4, size=14):
    for b, v in zip(bars, vals):
        ax.annotate(f"{v:.0f}%", (b.get_x()+b.get_width()/2, b.get_height()),
                    ha="center", va="bottom", xytext=(0, dy),
                    textcoords="offset points", color=T.INK, fontsize=size,
                    fontweight="bold")


# ---------------------------------------------------------------- 1. PAYOFF
def panel_payoff(ax):
    d = DF
    cells = [("BULLISH", 0, T.GREEN_L), ("BULLISH", 1, T.GREEN),
             ("BEARISH", 0, T.RED_L), ("BEARISH", 1, T.RED)]
    rates, ns, cols = [], [], []
    for dirn, e, c in cells:
        s = d[(d.DIRECTION == dirn) & (d.EARNINGS_D1 == e)]
        rates.append(_rate(s.DIR_GAP)); ns.append(len(s)); cols.append(c)
    x = [0, 1, 2.55, 3.55]
    bars = ax.bar(x, rates, width=0.84, color=cols, zorder=3,
                  edgecolor=T.BG, linewidth=1.0)
    ax.axhline(50, color=T.GREY, lw=1.0, ls=(0, (5, 4)), zorder=2)
    ax.text(4.08, 50, "coin\nflip", color=T.GREY_L, fontsize=8.5,
            ha="left", va="center")
    _vlabel(ax, bars, rates)
    for b, n, c in zip(bars, ns, cols):
        dark = c in (T.GREEN_L, T.RED_L)
        ax.annotate(f"n={n}", (b.get_x()+b.get_width()/2, 3.5), ha="center",
                    color=(T.BG if dark else "white"), fontsize=9.5, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(["none", "earnings", "none", "earnings"])
    ax.set_xlim(-0.62, 4.82)
    ax.set_ylim(0, 118); ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_ylabel("Day 2 continuation rate  (%)")
    ax.text(0.5, 110, "BULLISH", ha="center", va="center", color=T.GREEN,
            fontsize=13, fontweight="bold")
    ax.text(3.05, 110, "BEARISH", ha="center", va="center", color=T.RED,
            fontsize=13, fontweight="bold")
    T.clean(ax)
    return ax


# ----------------------------------------------------------- 2. CATALYST DIST
def panel_catalyst(ax):
    d = DF
    lo, hi = -8, 22
    bins = np.linspace(lo, hi, 46)
    for e, col, lab in [(0, T.GREY, "structural"),
                        (1, T.GREEN, "earnings")]:
        v = d.loc[d.EARNINGS_D1 == e, "DIR_GAP"]          # out-of-range dropped
        ax.hist(v, bins=bins, density=True, color=col, alpha=0.66,
                edgecolor=T.BG, linewidth=0.3, zorder=3, label=lab)
        med = v.median()
        ax.axvline(med, color=col, lw=2.0, ls=(0, (2, 2)), zorder=5)
        ax.annotate(f"median {med:.1f}%", (med, ax.get_ylim()[1]*0.99),
                    color=col, fontsize=10, fontweight="bold",
                    ha="left" if e else "right", va="top",
                    xytext=(4 if e else -4, 0), textcoords="offset points")
    ax.axvline(0, color=T.INK2, lw=1.0, zorder=2)
    ax.set_xlim(lo, hi); ax.set_ylim(top=ax.get_ylim()[1]*1.12)
    ax.set_xlabel("Day 2 gap in setup direction  (%)")
    ax.set_ylabel("density"); ax.set_yticks([])
    ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.72), fontsize=10.5)
    T.clean(ax, grid_axis="x")
    return ax


# --------------------------------------------------------- 3. CLOSE LOCATION
def panel_closeloc(ax):
    d = DF
    bins = np.linspace(0, 1, 41)
    ax.hist(d.loc[d.DIRECTION == "BEARISH", "D1_CLOSE_LOC"], bins=bins,
            color=T.RED, alpha=0.9, edgecolor=T.BG, linewidth=0.25, zorder=3,
            label="bearish — close near low")
    ax.hist(d.loc[d.DIRECTION == "BULLISH", "D1_CLOSE_LOC"], bins=bins,
            color=T.GREEN, alpha=0.9, edgecolor=T.BG, linewidth=0.25, zorder=3,
            label="bullish — close near high")
    ax.axvspan(0.25, 0.75, color=T.GREY, alpha=0.10, zorder=1)
    for xv in (0.25, 0.75):
        ax.axvline(xv, color=T.GREY, lw=1.0, ls=(0, (5, 4)), zorder=2)
    top = ax.get_ylim()[1]
    ax.text(0.5, top*0.96, "rubric ‘dead zone’ 0.25–0.75", ha="center",
            va="top", color=T.INK2, fontsize=10.5)
    ax.text(0.5, top*0.86, "empty by construction", ha="center", va="top",
            color=T.INK3, fontsize=9.5, style="italic")
    ax.legend(loc="center", fontsize=10.5)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Day 1 close location   (Close − Low) / (High − Low)")
    ax.set_ylabel("number of setups")
    T.clean(ax)
    return ax


# ------------------------------------------------------------- 4. FOOTPRINT
def panel_footprint(ax):
    d = DF
    bins = np.logspace(np.log10(1.2), np.log10(120), 42)
    ax.hist(d.D1_ADV_MULT.clip(upper=119), bins=bins, color=T.GREY_D,
            edgecolor=T.BG, linewidth=0.3, zorder=3)
    ax.set_xscale("log")
    top = ax.get_ylim()[1]
    ax.axvline(1.5, color=T.RED, lw=2.0, ls=(0, (3, 2)), zorder=4)
    ax.text(1.42, top*0.95, "rubric minimum\n1.5× ADV", color=T.RED, fontsize=9.5,
            fontweight="bold", va="top", ha="right")
    ax.axvline(3.0, color=T.GREEN, lw=2.0, ls=(0, (3, 2)), zorder=4)
    ax.text(3.2, top*0.78, "dataset floor\n3× ADV", color=T.GREEN, fontsize=9.5,
            fontweight="bold", va="top", ha="left")
    med = d.D1_ADV_MULT.median()
    ax.text(0.97, 0.62, f"median\n{med:.1f}× ADV", transform=ax.transAxes,
            ha="right", color=T.INK, fontsize=13, fontweight="bold")
    ax.set_xlim(1.2, 120)
    ax.set_xticks([1.5, 3, 5, 10, 25, 50, 100])
    ax.set_xticklabels(["1.5×", "3×", "5×", "10×", "25×", "50×", "100×"])
    ax.set_xlabel("Day 1 volume vs 21-day average   (log scale)")
    ax.set_ylabel("number of setups")
    T.clean(ax)
    return ax


# ------------------------------------------------------- 5. EXTENSION PARADOX
def panel_extension(ax):
    d = DF.copy()
    edges = [3, 4, 5, 7, 10, 1e9]
    labs = ["3–4×", "4–5×", "5–7×", "7–10×", "10×+"]
    d["b"] = pd.cut(d.D1_ADV_MULT, edges, labels=labs)
    g = d.groupby("b", observed=True).agg(rate=("DIR_GAP", _rate),
                                          n=("DIR_GAP", "size"))
    cols = [T.GREY_D, T.GREY, T.GREEN_L, T.GREEN, T.RED]
    bars = ax.bar(range(len(g)), g.rate, width=0.72, color=cols, zorder=3,
                  edgecolor=T.BG, linewidth=1.0)
    ax.axvspan(0.5, 3.5, color=T.GREEN, alpha=0.07, zorder=1)
    ax.text(2.0, 101, "institutional core", ha="center", color=T.GREEN,
            fontsize=11, fontweight="bold")
    _vlabel(ax, bars, g.rate, size=13)
    for b, n, c in zip(bars, g.n, cols):
        ax.annotate(f"n={n}", (b.get_x()+b.get_width()/2, 4), ha="center",
                    color=T.BG if c in (T.GREEN_L, T.GREY) else "white",
                    fontsize=9, fontweight="bold")
    ax.axhline(OVERALL, color=T.GREY_L, lw=1.0, ls=(0, (5, 4)), zorder=2)
    ax.text(4.45, OVERALL+1.5, f"overall {OVERALL:.0f}%", ha="right",
            color=T.GREY_L, fontsize=9.5)
    ax.set_xticks(range(len(g))); ax.set_xticklabels(labs)
    ax.set_ylim(0, 110)
    ax.set_xlabel("Day 1 volume multiple  (× ADV)")
    ax.set_ylabel("Day 2 continuation rate  (%)")
    T.clean(ax)
    return ax


# ---------------------------------------------------------------- 6. MONTHLY
def panel_monthly(ax):
    d = DF.copy()
    d["ym"] = pd.PeriodIndex(d.DATE, freq="M")
    g = d.groupby("ym").agg(rate=("DIR_GAP", _rate), n=("DIR_GAP", "size"))
    g = g[g.n >= 15]
    x = np.arange(len(g))
    ax2 = ax.twinx()
    ax2.bar(x, g.n, width=0.6, color=T.GREY_D, zorder=1)
    ax2.set_ylim(0, g.n.max()*3.1); ax2.set_yticks([])
    for s in ax2.spines.values():
        s.set_visible(False)
    ax.plot(x, g.rate, color=T.GREEN, lw=2.6, zorder=4)
    ax.scatter(x, g.rate, s=46, color=T.INK, edgecolor=T.GREEN, linewidth=1.8,
               zorder=5)
    ax.axhline(50, color=T.GREY, lw=1.0, ls=(0, (5, 4)), zorder=2)
    ax.text(len(g)-0.5, 46.5, "coin flip 50%", ha="right", color=T.GREY, fontsize=9.5)
    avg = g.rate.mean()
    ax.axhline(avg, color=T.GREEN, lw=1.2, ls=(0, (5, 3)), zorder=2)
    ax.text(len(g)-0.5, avg+1.6, f"mean {avg:.0f}%", ha="right", color=T.GREEN,
            fontsize=10, fontweight="bold")
    ax.set_ylim(40, 100)
    ax.set_xticks(x)
    ax.set_xticklabels([p.strftime("%b\n%y") for p in g.index], fontsize=9.5)
    ax.set_ylabel("Day 2 continuation rate  (%)")
    ax.set_zorder(ax2.get_zorder()+1); ax.patch.set_visible(False)
    T.clean(ax)
    ax.text(0.012, 0.055, "grey bars = monthly setup count", transform=ax.transAxes,
            color=T.INK3, fontsize=9)
    return ax


# ---------------------------------------------------------- standalone driver
SPECS = [
    ("footprint", 1, panel_footprint, "An institutional-grade universe",
     "Day 1 volume relative to each stock’s 21-day average", 0.135),
    ("closeloc", 2, panel_closeloc, "A bimodal conviction fingerprint",
     "Distribution of Day 1 close location across all 841 setups", 0.135),
    ("payoff", 3, panel_payoff, "A catalyst nearly doubles the edge",
     "Day 2 continuation rate by setup direction and Day 1 catalyst", 0.175),
    ("catalyst", 4, panel_catalyst, "Earnings shifts the whole outcome distribution",
     "Day 2 directional gap, earnings-driven vs. structural Day 1 moves", 0.135),
    ("extension", 5, panel_extension, "The extension paradox",
     "Continuation rate by Day 1 volume — more is not always better", 0.135),
    ("monthly", 6, panel_monthly, "A persistent, year-round edge",
     "Monthly Day 2 continuation rate, May 2025 – May 2026", 0.135),
]
SRC = "Data: 841 Day 2 setups across 666 tickers · May 2025 – May 2026"


def save_standalone():
    T.apply()
    for name, n, fn, title, cap, bot in SPECS:
        fig = plt.figure(figsize=(12, 7.6))
        ax = fig.add_axes([0.082, bot, 0.86, 0.95 - 0.20 - bot])
        fn(ax)
        T.fig_header(fig, n, title, cap)
        T.source_note(fig, SRC)
        fig.savefig(f"charts/{name}.png")
        plt.close(fig)
        print("saved charts/%s.png" % name)


if __name__ == "__main__":
    save_standalone()
