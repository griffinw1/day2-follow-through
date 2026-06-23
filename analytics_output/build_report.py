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
  "We want <b>high relative volume (RVOL)</b> for this idea to be in play — and we have it in this dataset."),
 ("charts/closeloc.png", 2, "A bimodal conviction fingerprint",
  "For these setups to be most in play we want them to <b>close at the low or high of the Day-1 range</b> — and we see that in the dataset."),
 ("charts/payoff.png", 3, "A catalyst nearly doubles the edge",
  "We want <b>the move to keep going the next day</b> — and most of the time it does, especially when a catalyst is behind it."),
 ("charts/catalyst.png", 4, "Earnings shifts the whole distribution",
  "We want <b>a real catalyst like earnings</b> driving the move — and when there is one, the follow-through is far bigger."),
 ("charts/extension.png", 5, "The extension paradox",
  "We want a big move — but <b>not the most extreme one</b>. The wildest, highest-volume names actually follow through the least, so don't chase them."),
 ("charts/monthly.png", 6, "A persistent, year-round edge",
  "We want to know this isn't luck — and it isn't: <b>the edge showed up in every single month</b> of the year."),
]
INTRADAY = [
 ("charts/event_study.png", 7, "From the open: longs fade, shorts follow through",
  "The catch: the next-day jump happens <b>overnight, before you can trade it</b>. If you just buy at the open, the long trades actually lose."),
 ("charts/mfe_mae.png", 8, "Trade quality: room up vs. room down",
  "When these trades work they <b>give you more reward than risk</b> — price usually runs to the level we marked before it turns."),
 ("charts/entry_compare.png", 9, "The entry rule is the edge",
  "The key rule: <b>don't buy the open — wait for the stock to test a level and turn</b>. Entering on that turn is what makes it profitable."),
 ("charts/trade_cards.png", 10, "Twelve trades, worst to best",
  "Trade by trade it's simple: <b>winners keep running, losers get cut fast</b> with a tight stop — small losses, bigger wins."),
]

def fig_block(path, n, title, expl):
    # the chart image already carries its own "FIGURE N" + title, so the block
    # is just the image + a short explanatory caption (no duplicate heading).
    return f"""
    <figure class="fig">
      <img alt="Figure {n}: {html.escape(title)}" src="data:image/png;base64,{b64(path)}">
      <figcaption><b>Figure {n}.</b> {expl}</figcaption>
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
    parts.append('<p class="lead" style="margin-top:24px"><b>The whole study on one plate.</b> '
                 'The six daily findings at a glance — full detail and the intraday reality check follow below.</p>')
    parts.append('<div class="op"><img alt="The Day 2 setup at a glance — six-panel overview" '
                 'src="data:image/png;base64,%s"></div>' % b64("charts/plate_day2.png", maxw=1600))
    parts.append('<div class="part"><span>PART 1</span> &nbsp; The Daily Setup — A Strong-Looking Pattern</div>')
    parts.append('<p class="lead">Each setup is a fully-qualified Day-1 footprint. The daily evidence below shows the continuation pattern exists; whether it is <i>tradable</i> comes in Part 2.</p>')
    parts += [fig_block(*f) for f in DAILY]
    parts.append('<div class="part"><span>PART 2</span> &nbsp; The Intraday Reality Check — Is It Tradable?</div>')
    parts.append('<p class="lead">Realized Polygon 1-minute data on a 51-setup pilot. This is where the headline number meets reality.</p>')
    parts += [fig_block(*f) for f in INTRADAY]
    parts.append('<div class="part"><span>PART 3</span> &nbsp; Findings — One Page</div>')
    # embed the live one-pager (self-contained, always in sync) rather than a flat screenshot
    with open("FINDINGS_onepager.html") as fh:
        onepager_doc = fh.read()
    parts.append(
        '<div class="op"><iframe title="One-page findings" '
        'style="width:100%;height:1040px;border:1px solid #e3e6e9;border-radius:4px;'
        'box-shadow:0 1px 6px rgba(0,0,0,.10);background:#eceff1;display:block;" '
        f'srcdoc="{html.escape(onepager_doc)}"></iframe></div>')

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
