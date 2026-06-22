# Project: Day 2 — The Follow-Through

Institutional follow-through study. The findings are published as a live site via GitHub Pages.

- **GitHub repo:** https://github.com/griffinw1/day2-follow-through
- **Live report (GitHub Pages):** https://griffinw1.github.io/day2-follow-through/
- **Pages source:** `main` branch, root (`/`). `index.html` is the landing page.

## ⚠️ ALWAYS push changes to GitHub

After making **any** change to files in this project, you MUST commit and push to the
`origin` remote (the repo above) so the change is saved and the live site stays current.
Do this automatically at the end of the change — do not wait to be asked.

```bash
git add -A
git commit -m "<concise description of the change>"
git push origin main
```

End every commit message with:

```
Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

If `git push` fails because the remote moved ahead, run `git pull --rebase origin main`
and push again.

## Keeping the published files in sync

The live site is served from the repo root, not from `analytics_output/`:

- `index.html`     — generated copy of `analytics_output/Day2_Report.html`
- `onepager.html`  — generated copy of `analytics_output/FINDINGS_onepager.html`

When you change anything that affects the report (the build script, charts, data, or the
one-pager), **regenerate and re-copy before pushing**:

```bash
python analytics_output/build_report.py          # rebuilds analytics_output/Day2_Report.html
cp analytics_output/Day2_Report.html index.html
cp analytics_output/FINDINGS_onepager.html onepager.html
```

Then commit and push (see above).

## Never commit secrets

`analytics_output/.env` holds `POLYGON_API_KEY` and is git-ignored. Never commit it, and
never commit any other API keys, tokens, or credentials. The `.gitignore` already excludes
`.env`, `__pycache__/`, and the regenerable `analytics_output/intraday_cache/`.
