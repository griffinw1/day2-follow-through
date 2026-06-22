# Day 2 — The Follow-Through

An institutional follow-through study of the "Day 2" continuation setup: buying or
shorting a stock the morning after a big, high-volume, conviction-close move.

- **Part 1** — the daily pattern across **841 setups** (666 tickers, May 2025–May 2026)
- **Part 2** — an intraday reality check on a **51-setup pilot** (Polygon 1-minute bars)
- **Part 3** — the one-page verdict

## Live report

Published via GitHub Pages:

- **Full report:** `index.html` (all charts embedded, copy-paste friendly)
- **One-page findings:** `onepager.html`

## Repo layout

| Path | What |
|------|------|
| `index.html` | Full report (served as the GitHub Pages landing page) |
| `onepager.html` | Standalone one-page findings summary |
| `analytics_output/` | Source HTML, charts, data (CSV/parquet), and the build scripts |
| `analytics_output/build_report.py` | Assembles the self-contained `Day2_Report.html` |

`index.html` / `onepager.html` are generated copies of the files in `analytics_output/`.
Regenerate the report with `python analytics_output/build_report.py`, then copy the
output up to the repo root.
