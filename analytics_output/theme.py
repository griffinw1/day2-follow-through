"""Dark-academic visual system for the Day 2 study.
Palette restricted to GREEN / RED / GREY on a charcoal ground, per journal-
figure conventions: high data-ink ratio, soft off-white text, desaturated
hues, Figure-N captions. Import as T and call T.apply()."""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# ---- Ground & ink (dark, never pure black / pure white) ------------------
BG      = "#101216"   # charcoal figure ground
PANEL   = "#14171C"   # very slightly elevated panel
INK     = "#ECECEC"   # high-emphasis soft white
INK2    = "#A7ADB5"   # secondary grey text
INK3    = "#6B7178"   # captions / faint
GRID    = "#23272E"   # near-invisible grid
AXIS    = "#3A3F47"   # axis / spine

# ---- Restricted palette: green, red, grey (desaturated for dark) ---------
GREEN   = "#3FB783"   # bullish / positive
GREEN_L = "#7FCBA6"   # light green
GREEN_D = "#2C7E5C"   # deep green
RED     = "#DB5B4D"   # bearish / negative
RED_L   = "#E79286"   # light red
RED_D   = "#9E3F35"   # deep red
GREY    = "#7E848D"   # neutral mid grey
GREY_L  = "#B7BCC3"   # light grey
GREY_D  = "#474C55"   # dark grey fill


def _font(cands):
    avail = {f.name for f in fm.fontManager.ttflist}
    for c in cands:
        if c in avail:
            return c
    return "DejaVu Sans"


SERIF = None
SANS = None


def apply():
    global SERIF, SANS
    SERIF = _font(["Charter", "Palatino", "Georgia", "DejaVu Serif"])
    SANS = _font(["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"])
    mpl.rcParams.update({
        "font.family": SANS,
        "font.size": 11,
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "axes.edgecolor": AXIS,
        "axes.linewidth": 0.9,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlecolor": INK,
        "axes.labelcolor": INK2,
        "axes.labelsize": 11.5,
        "text.color": INK,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "xtick.labelsize": 10.5,
        "ytick.labelsize": 10.5,
        "legend.frameon": False,
        "legend.labelcolor": INK,
        "figure.dpi": 130,
        "savefig.dpi": 200,
    })
    return SERIF, SANS


def fig_header(fig, n, title, caption=None, x=0.062, y=0.955):
    """Prominent academic title block: 'FIGURE N' label, big serif title."""
    fig.text(x, y, f"FIGURE {n}", color=GREEN, fontsize=12, fontweight="bold",
             family=SANS)
    fig.text(x, y - 0.066, title, color=INK, fontsize=27, fontweight="bold",
             family=SERIF)
    if caption:
        fig.text(x, y - 0.112, caption, color=INK2, fontsize=13, family=SANS)


def source_note(fig, text, x=0.062, y=0.028):
    fig.text(x, y, text, color=INK3, fontsize=9.5, family=SANS)
    fig.text(0.94, y, "Continuation = Day 2 open gapped in the setup direction",
             color=INK3, fontsize=9.5, ha="right", family=SANS)


def clean(ax, grid_axis="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    ax.tick_params(length=0)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    return ax
