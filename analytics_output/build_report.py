"""Assemble a single self-contained HTML report: every chart base64-embedded
(copy-paste friendly), in narrative order with a short explanation, and the
one-page findings summary at the bottom."""
import base64, io, html
from PIL import Image

def b64(path, maxw=1500):
    im = Image.open(path).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, int(im.height*maxw/im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()

# (file, fig#, title, explanation)
DAILY = [
 ("charts/footprint.png", 1, "An institutional-grade universe",
  "All 841 setups cleared at least 3× their 21-day average volume — twice the rulebook minimum, with a median of 4.2×. That volume is the institutional fingerprint: funds and desks moving with urgency, not retail momentum."),
 ("charts/closeloc.png", 2, "A bimodal conviction fingerprint",
  "Day-1 close location is sharply bimodal — bullish setups close near the high (~0.95), bearish near the low (~0.05), and nothing lands in the 0.25–0.75 “dead zone.” It’s the signature of participants who held into the close with conviction."),
 ("charts/payoff.png", 3, "A catalyst nearly doubles the edge",
  "On Day 2, 73% of setups gapped in the continuation direction. A fresh catalyst nearly doubles the edge: bullish setups with earnings continued 93% of the time, versus 59% with no catalyst."),
 ("charts/catalyst.png", 4, "Earnings shifts the whole distribution",
  "Earnings doesn’t just lift the hit rate — it shifts the entire outcome distribution to the right, from a median +0.3% for structural moves to +7.3% for earnings-driven ones."),
 ("charts/extension.png", 5, "The extension paradox",
  "More is not always better. Follow-through peaks at 7–10× volume and then fades — the most blown-out, lottery-ticket names (10×+) are the least reliable, exactly the caution the methodology raises about chasing extended moves."),
 ("charts/monthly.png", 6, "A persistent, year-round edge",
  "This wasn’t a single-month fluke. The continuation rate held every month of the year, never dropping below ~64%."),
]
INTRADAY = [
 ("charts/event_study.png", 7, "From the open: longs fade, shorts follow through",
  "Here’s the catch: that 73% “continuation” is the overnight gap, which happens while you’re flat. Tracking the realized intraday path from the open tells a different story — longs fade (−0.7%) while shorts follow through (+1.5%). Measured from a tradable entry, the long edge at the open disappears."),
 ("charts/mfe_mae.png", 8, "Trade quality: room up vs. room down",
  "Still, the structure is real. Across the 51-setup pilot the median trade had more room up (0.75 ATR) than down (0.54 ATR) — a 1.38:1 ratio — and 73% of setups reached the marked Day-1 level. Those levels are genuine intraday magnets."),
 ("charts/entry_compare.png", 9, "The entry rule is the edge",
  "The resolution: the methodology says don’t buy the open — wait for the morning Test and the Character Flip. Backtesting that exact entry (enter on the flip, stop below the turn) flips the long side from −0.8% to +1.66R expectancy. The entry rule, not the setup alone, is where the money is."),
 ("charts/trade_cards.png", 10, "Twelve trades, worst to best",
  "Twelve representative trades, worst to best — each showing the minute path from the open, session VWAP, Day-1 levels, the flip entry (triangle) and the exit (×). Winners ride the favorable excursion; losers stop out quickly below the turn — the single invalidation rule in action."),
]

def fig_block(path, n, title, expl):
    # the chart image already carries its own "FIGURE N" + title, so the block
    # is just the image + a short explanatory caption (no duplicate heading).
    return f"""
    <figure class="fig">
      <img alt="Figure {n}: {html.escape(title)}" src="data:image/png;base64,{b64(path)}">
      <figcaption><b>Figure {n}.</b> {html.escape(expl)}</figcaption>
    </figure>"""

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#eceff1;color:#15202b;
  font:15px/1.62 "Helvetica Neue",Helvetica,Arial,sans-serif;}
.wrap{max-width:880px;margin:22px auto;background:#fff;
  box-shadow:0 1px 8px rgba(0,0,0,.12);}
.hero{background:#16202b;color:#fff;padding:30px 40px 26px;}
.hero .kick{color:#5fd0a3;font-size:12px;font-weight:700;letter-spacing:3px;}
.hero h1{font:700 32px/1.15 Georgia,"Times New Roman",serif;margin:8px 0 10px;}
.hero p{color:#b6c0c9;font-size:14px;margin:0;max-width:680px;}
.hero p b{color:#e9eef2;}
.content{padding:8px 40px 30px;}
.part{font:700 13px/1 "Helvetica Neue",Arial,sans-serif;letter-spacing:2px;
  text-transform:uppercase;color:#16202b;margin:34px 0 6px;
  padding:10px 0 8px;border-top:3px solid #16202b;border-bottom:1px solid #dfe3e7;}
.part span{color:#1d8a64;}
.lead{color:#5c6772;font-size:14px;margin:8px 0 4px;}
.fig{margin:26px 0 30px;}
.figlabel{color:#1d8a64;font-size:11.5px;font-weight:700;letter-spacing:2px;}
.fig h3{font:700 20px/1.2 Georgia,serif;margin:3px 0 12px;}
.fig img{width:100%;height:auto;display:block;border:1px solid #e3e6e9;border-radius:4px;}
.fig figcaption{color:#3a4550;font-size:14px;margin-top:11px;
  padding-left:14px;border-left:3px solid #1d8a64;}
.op{margin:18px 0 6px;}
.op img{width:100%;height:auto;display:block;border:1px solid #e3e6e9;
  border-radius:4px;box-shadow:0 1px 6px rgba(0,0,0,.10);}
.foot{padding:16px 40px 26px;border-top:1px solid #dfe3e7;
  color:#5c6772;font-size:11.5px;}
"""

def build():
    parts = []
    parts.append('<div class="part"><span>PART 1</span> &nbsp; The Daily Setup — A Strong-Looking Pattern</div>')
    parts.append('<p class="lead">Each setup is a fully-qualified Day-1 footprint. The daily evidence below shows the continuation pattern exists; whether it is <i>tradable</i> comes in Part 2.</p>')
    parts += [fig_block(*f) for f in DAILY]
    parts.append('<div class="part"><span>PART 2</span> &nbsp; The Intraday Reality Check — Is It Tradable?</div>')
    parts.append('<p class="lead">Realized Polygon 1-minute data on a 51-setup pilot. This is where the headline number meets reality.</p>')
    parts += [fig_block(*f) for f in INTRADAY]
    parts.append('<div class="part"><span>PART 3</span> &nbsp; Findings — One Page</div>')
    parts.append(f'<div class="op"><img alt="One-page findings" src="data:image/png;base64,{b64("/tmp/onepager.png", maxw=1600)}"></div>')

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Day 2 — The Follow-Through · Full Report</title><style>{CSS}</style></head>
<body><div class="wrap">
  <div class="hero">
    <div class="kick">INSTITUTIONAL FOLLOW-THROUGH STUDY</div>
    <h1>Day&nbsp;2: The Follow-Through</h1>
    <p>A study of the “Day 2” continuation setup — buying or shorting a stock the morning after a big,
       high-volume, conviction-close move. <b>Part 1</b> shows the daily pattern across
       <b>841 setups</b> (May 2025–May 2026); <b>Part 2</b> stress-tests it on realized intraday data;
       <b>Part 3</b> is the one-page verdict. Read top to bottom.</p>
  </div>
  <div class="content">
    {''.join(parts)}
  </div>
  <div class="foot">
    Data: 841 Day 2 setups across 666 tickers, May 2025 – May 2026 · intraday pilot n = 51, Polygon 1-minute bars.
    Continuation = the Day-2 open gapped in the setup’s direction. R = risk to the stop below the turn.
    All figures are embedded in this file — select all, copy, and paste into a document to keep the images.
  </div>
</div></body></html>"""

    with open("Day2_Report.html", "w") as fh:
        fh.write(doc)
    import os
    print("wrote Day2_Report.html  (%.1f MB)" % (os.path.getsize("Day2_Report.html")/1e6))

if __name__ == "__main__":
    build()
