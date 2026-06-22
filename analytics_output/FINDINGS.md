# Day 2 — Anatomy of an Institutional Follow-Through Edge
### An empirical study of 841 continuation setups, May 2025 – May 2026

**Abstract.** We examine 841 "Day 2" setups — stocks that printed a qualified
institutional footprint on Day 1 (volume ≥ 3× the 21-day average, range ≥ 2 ATR,
and a close in the extreme quartile of the day's range) — and measure how often
the move continued into the next session. Continuation is proxied by the Day 2
opening gap in the setup's direction. Across the full year the setups continued
**73% of the time**, far above a coin flip, and the edge was present in **every
month**. The single largest driver of follow-through is the presence of a fresh
catalyst: an earnings-driven Day 1 lifts the continuation rate from 59% to 87%,
and to **93% for bullish setups**. Counter-intuitively, the most violent Day 1
moves are *not* the most reliable — follow-through peaks at 7–10× volume and
fades beyond it.

---

## Data & method
- **Universe:** 841 setups across 666 tickers, Day 2 dates 2025-05-01 → 2026-05-01.
- **Pre-filtering:** every row already clears all three non-negotiable Day 1
  criteria (volume, range, close location), so results describe *conditional*
  follow-through given a qualified setup — not unconditional base rates.
- **Outcome measure:** `DIR_GAP` = the Day 2 open-to-prior-close gap signed in the
  setup direction (positive = continuation). Sign-based **continuation rate** is
  immune to the heavy-tailed magnitude outliers; magnitudes are reported as
  medians, and volume is shown on a log scale.

## Findings (each maps to a figure)

| # | Finding | Key number |
|---|---------|-----------|
| **A** | The universe is genuinely institutional — all setups sit at ≥ 3× ADV, twice the rubric minimum. | median **4.2× ADV** |
| **B** | Day 1 close location is sharply bimodal; no qualified setup lands in the 0.25–0.75 "dead zone." | bull ≈ 0.95 / bear ≈ 0.05 |
| **C** | A catalyst nearly doubles the edge. Bullish + earnings continues 93% of the time. | 59% → **93%** |
| **D** | Earnings shifts the *entire* outcome distribution right. | median +7.3% vs +0.3% |
| **E** | The extension paradox — follow-through peaks at 7–10× volume, then fades. | **87%** peak, 68% at 10×+ |
| **F** | The edge is persistent — present every month, never below ~64%. | mean **73%** |

### Directional asymmetry
Bullish setups continue more often (77%) and gap larger (median +2.8%) than
bearish setups (68%, +1.2%) — consistent with short-covering fuel above Day 1
highs and the broader market's upward drift over the window.

## Limitations (stated plainly)
- **No realized P&L.** The four trade-result columns in the source file are
  empty; "continuation" is the Day 2 *opening gap*, an entry-quality proxy, not
  an executed-trade return. Intraday MFE/MAE and the Character-Flip entry are not
  observable here.
- **Catalyst flag = earnings only.** FDA approvals, upgrades, and technical
  breakouts are not separately coded, so they sit in the "structural / no
  catalyst" bucket — making that group's 59% edge a *conservative lower bound*.
- **Low-float outliers** (e.g. a 7,700× ADV micro-cap) are real but unrepresentative;
  handled via medians, log scaling, and sign-based rates rather than removal.
- The hand-scored probability labels exist on only 155 of 841 rows and are **not**
  used for any headline result.

## Figures
`charts/plate_day2.png` — composite plate (panels A–F).
Standalone: `payoff`, `catalyst`, `closeloc`, `footprint`, `extension`, `monthly` (`.png`).
