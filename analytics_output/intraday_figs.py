"""Intraday pilot figures: (7) Day-2 event-study path with bootstrap bands,
(8) MFE/MAE trade-quality scatter. Dark-academic theme."""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import theme as T

GRID = np.arange(0, 390)
XT = [0, 60, 120, 180, 240, 300, 360, 389]
XTL = ["9:30", "10:30", "11:30", "12:30", "13:30", "14:30", "15:30", "16:00"]


def _boot_band(mat, B=2000, seed=1):
    rng = np.random.default_rng(seed)
    n = mat.shape[0]
    idx = rng.integers(0, n, size=(B, n))
    means = mat[idx].mean(axis=1)              # (B, 390)
    lo, hi = np.percentile(means, [2.5, 97.5], axis=0)
    return mat.mean(axis=0), lo, hi


# ------------------------------------------------------- Fig 7: event study
def fig_event_study(paths):
    T.apply()
    fig = plt.figure(figsize=(12, 7.6))
    ax = fig.add_axes([0.095, 0.135, 0.85, 0.585])
    groups = [(paths.DIRECTION == "BULLISH", T.GREEN, "bullish — long from open"),
              (paths.DIRECTION == "BEARISH", T.RED, "bearish — short from open")]
    pcols = [c for c in paths.columns if c.startswith("m")]
    ymin, ymax = 0.0, 0.0
    for mask, col, lab in groups:
        mat = paths.loc[mask, pcols].to_numpy(float)
        for r in mat:                                   # faint spaghetti
            ax.plot(GRID, r, color=col, lw=0.5, alpha=0.07, zorder=2)
        mean, lo, hi = _boot_band(mat)
        ax.fill_between(GRID, lo, hi, color=col, alpha=0.18, zorder=3, lw=0)
        ax.plot(GRID, mean, color=col, lw=3.0, zorder=4,
                label=f"{lab}  (n={int(mask.sum())})")
        ax.annotate(f"{mean[-1]:+.1f}%", (GRID[-1], mean[-1]), color=col,
                    fontsize=13, fontweight="bold", va="center",
                    xytext=(7, 0), textcoords="offset points")
        ymin, ymax = min(ymin, lo.min()), max(ymax, hi.max())
    ax.axhline(0, color=T.INK2, lw=1.0, zorder=1)
    ax.set_ylim(ymin - 0.5, ymax + 0.5)
    ax.set_xticks(XT); ax.set_xticklabels(XTL)
    ax.set_xlim(0, 410)
    ax.set_xlabel("time of day (Day 2)")
    ax.set_ylabel("mean cumulative return from open,\nsigned to setup direction  (%)")
    ax.legend(loc="upper left", fontsize=11)
    T.clean(ax)
    T.fig_header(fig, 7, "From the open: longs fade, shorts follow through",
                 "Average Day-2 intraday path from the open, signed to the setup direction")
    T.source_note(fig, "Pilot n=51, realized Polygon 1-min bars. Shaded = 95% bootstrap CI; faint lines = individual setups")
    fig.savefig("charts/event_study.png", dpi=200)
    plt.close(fig)
    print("saved charts/event_study.png")


# -------------------------------------------------------- Fig 8: MFE/MAE
def fig_mfe_mae(out):
    T.apply()
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_axes([0.095, 0.115, 0.84, 0.63])
    win, loss = out[out.win], out[~out.win]
    for s, col, lab in [(win, T.GREEN, "closed in direction"),
                        (loss, T.RED, "closed against")]:
        ax.scatter(s.mae_atr, s.mfe_atr, s=60, color=col, alpha=0.8,
                   edgecolor=T.BG, linewidth=0.6, zorder=3, label=lab)
    hi = float(np.nanpercentile(out[["mfe_atr", "mae_atr"]].to_numpy(), 98)) * 1.1
    ax.plot([0, hi], [0, hi], color=T.GREY, lw=1.2, ls=(0, (5, 4)), zorder=2)
    ax.annotate("MFE = MAE", (hi*0.82, hi*0.82), color=T.GREY, fontsize=9.5,
                rotation=45, va="bottom")
    mfe_m, mae_m = out.mfe_atr.median(), out.mae_atr.median()
    ax.axhline(mfe_m, color=T.GREEN, lw=1.0, ls=(0, (2, 2)), zorder=2)
    ax.axvline(mae_m, color=T.RED, lw=1.0, ls=(0, (2, 2)), zorder=2)
    ax.annotate(f"median MFE {mfe_m:.2f} ATR", (hi*0.99, mfe_m), color=T.GREEN,
                fontsize=9.5, ha="right", va="bottom")
    ax.annotate(f"median MAE\n{mae_m:.2f} ATR", (mae_m, hi*0.99), color=T.RED,
                fontsize=9.5, ha="left", va="top")
    ax.set_xlim(0, hi); ax.set_ylim(0, hi)
    ax.set_xlabel("maximum adverse excursion  (ATR units)")
    ax.set_ylabel("maximum favorable excursion  (ATR units)")
    ax.legend(loc="upper right", fontsize=11)
    T.clean(ax)
    ax.set_axisbelow(True); ax.grid(True, color=T.GRID, lw=0.8)
    T.fig_header(fig, 8, "Trade quality: room up vs. room down",
                 "Per-setup favorable vs. adverse excursion, in ATR units")
    T.source_note(fig, "Pilot: realized Polygon 1-minute bars. Points above the diagonal had more upside than downside")
    fig.savefig("charts/mfe_mae.png", dpi=200)
    plt.close(fig)
    print("saved charts/mfe_mae.png")


def summary(out):
    print("\n===== PILOT INTRADAY SUMMARY (realized) =====")
    print(f"n setups with data: {len(out)}")
    print(f"closed in direction: {out.win.mean()*100:.0f}%")
    print(f"median close return: {out.ret_close.median():+.2f}%")
    print(f"median MFE: {out.mfe_atr.median():.2f} ATR | median MAE: {out.mae_atr.median():.2f} ATR")
    print(f"edge ratio (MFE/MAE medians): {out.mfe_atr.median()/out.mae_atr.median():.2f}")
    print(f"reached Day-1 extreme: {out.reached_d1.mean()*100:.0f}%")
    g = out.groupby("EARNINGS_D1").agg(win=("win","mean"), ret=("ret_close","median"),
        mfe=("mfe_atr","median"), mae=("mae_atr","median"), reach=("reached_d1","mean"))
    print("\nBy catalyst:\n", g.round(2).to_string())


if __name__ == "__main__":
    out = pd.read_csv("pilot_outcomes.csv")
    paths = pd.read_parquet("pilot_paths.parquet")
    summary(out)
    fig_event_study(paths)
    fig_mfe_mae(out)
