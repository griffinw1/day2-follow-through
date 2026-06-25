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
  "For this idea to be in play we want <b>high relative volume (RVOL)</b>, which tells us real institutional money is pushing the stock rather than ordinary retail noise. Every setup in this dataset cleared at least three times its average daily volume, with a median near four times, so that footprint is clearly present."),
 ("charts/closeloc.png", 2, "A bimodal conviction fingerprint",
  "For these setups to be most in play we want them to <b>close right at the high or low of the Day 1 range</b>, which shows conviction holding into the close instead of a move that faded. In this dataset the closes cluster hard at the extremes with almost nothing in the middle, exactly the fingerprint we are looking for."),
 ("charts/payoff.png", 3, "A catalyst nearly doubles the edge",
  "We want <b>the move to keep going the next day</b>, and most of the time it does. Roughly three quarters of setups continued in the same direction, and that rate climbs higher still when a fresh catalyst is sitting behind the move."),
 ("charts/catalyst.png", 4, "Earnings shifts the whole distribution",
  "We want <b>a real catalyst like earnings</b> driving the move, because that is where almost all of the edge actually lives. With an earnings catalyst the follow through is far larger, but strip the catalyst out and the structural setup on its own gives back nearly all of its advantage."),
 ("charts/extension.png", 5, "The extension paradox",
  "We want a big move but <b>not the most extreme one</b>. Counterintuitively, the wildest and highest volume names follow through the least, so the cleanest continuation comes from strong but not blown out moves rather than the lottery tickets everyone is chasing."),
 ("charts/monthly.png", 6, "A persistent, year-round edge",
  "We want to know this is a real edge and not luck from one hot stretch. The continuation rate held up in every single month of the sample, so within this dataset the effect <b>does not appear to be regime dependent</b>."),
]
INTRADAY = [
 ("charts/event_study.png", 7, "From the open: longs fade, shorts follow through",
  "Here is the catch. <b>Most of the move often happens overnight</b>, so if you are just buying at the open you are giving up a large part of the edge before you are even in the trade. That is even more true for the longs, where the realized path from the open actually fades."),
 ("charts/mfe_mae.png", 8, "Trade quality: room up vs. room down",
  "When these trades work they hand us more room in our favor than against us. On average the setup returns a <b>reward to risk of about 1.4 to 1</b>, with the typical trade running near 0.75 ATR our way versus 0.54 ATR against, and price usually reaches the level we marked before it turns."),
 ("charts/entry_compare.png", 9, "The entry rule is the edge",
  "The key rule is simple. <b>If you are not playing for the overnight gap, do not buy the open.</b> Wait for the stock to test a level and turn, then enter on that turn, because that is what separates a real edge from a coin flip."),
 ("charts/trade_cards.png", 10, "Twelve trades, worst to best",
  "Trade by trade the pattern is simple. <b>Winners keep running while losers get cut fast</b> with a tight stop, which is how the strategy ends up taking small losses and letting the bigger wins pay for them."),
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
.sum{margin-top:4px;}
.sum h3{font:700 19px/1.25 Georgia,serif;color:#16202b;margin:26px 0 8px;}
.sum p{margin:10px 0;}
.sum ul{margin:8px 0 14px;padding-left:22px;} .sum li{margin:7px 0;}
.sum b{color:#16202b;}
"""

def build():
    parts = []
    parts.append('<p class="lead" style="margin-top:24px"><b>The six daily findings on one plate.</b> '
                 'Detail and the intraday test follow below.</p>')
    parts.append('<div class="op"><img alt="Day 2 setup, six panel overview" '
                 'src="data:image/png;base64,%s"></div>' % b64("charts/plate_day2.png", maxw=1600))
    parts.append('<div class="part"><span>PART 1</span> &nbsp; The Daily Pattern</div>')
    parts.append('<p class="lead">Each setup is a qualified Day 1 footprint. The daily data shows the continuation pattern exists. Whether it is <i>tradable</i> comes in Part 2.</p>')
    parts += [fig_block(*f) for f in DAILY]
    parts.append('<div class="part"><span>PART 2</span> &nbsp; Is It Actually Tradable</div>')
    parts.append('<p class="lead">Polygon 1 minute data on a 51 setup pilot.</p>')
    parts += [fig_block(*f) for f in INTRADAY]
    parts.append('<div class="part"><span>PART 3</span> &nbsp; The One Page Verdict</div>')
    # embed the live one-pager (self-contained, always in sync) rather than a flat screenshot
    with open("FINDINGS_onepager.html") as fh:
        onepager_doc = fh.read()
    parts.append(
        '<div class="op"><iframe title="One-page findings" '
        'style="width:100%;height:1040px;border:1px solid #e3e6e9;border-radius:4px;'
        'box-shadow:0 1px 6px rgba(0,0,0,.10);background:#eceff1;display:block;" '
        f'srcdoc="{html.escape(onepager_doc)}"></iframe></div>')

    parts.append('''
    <div class="part"><span>PART 4</span> &nbsp; Summary</div>
    <div class="sum">

    <h3>The question</h3>
    <p>A stock has a huge, high volume day, the Day 1. The question is whether you can make money the next
    morning trading in the same direction. We looked at 841 of these days from May 2025 to May 2026, then
    checked a smaller group minute by minute.</p>

    <h3>The daily data looked strong</h3>
    <p>Using only end of day data, five things stood out.</p>
    <ul>
      <li><b>Real institutional volume.</b> Every stock traded at least three times its normal daily volume,
      usually about four times. This is relative volume, RVOL. Volume that large means funds and trading
      desks were active, not just individuals. (Figure 1)</li>
      <li><b>A conviction close.</b> Close location is where a stock finishes inside its daily range. Bullish
      setups closed at the high and bearish setups at the low, with almost nothing in the middle. That means
      buyers or sellers held control into the close. (Figure 2)</li>
      <li><b>A high continuation rate.</b> About 73 percent of these stocks opened the next day gapped in the
      same direction. A fresh news catalyst pushed that to about 87 percent, and to 93 percent for bullish
      earnings. (Figures 3 and 4)</li>
      <li><b>Stronger is not always better.</b> The most blown out volume names followed through the least.
      The cleanest continuation came from strong but not extreme moves. (Figure 5)</li>
      <li><b>It held all year.</b> The continuation rate showed up every month and never fell below about 64
      percent. (Figure 6)</li>
    </ul>

    <h3>The intraday reality</h3>
    <p>Watched minute by minute, the picture changes.</p>
    <ul>
      <li><b>The catch.</b> The 73 percent continuation is mostly the overnight gap, the move between one
      day's close and the next day's open, which happens while you are flat. Measured from the Day 2 open, a
      price you can actually get, the long side turns negative. Buying the open of a bullish setup won only
      about 44 percent of the time. The headline number was the gap, not a trade. (Figure 7)</li>
      <li><b>The structure is real.</b> The typical trade had more room in your favor than against you, about
      0.75 ATR up versus 0.54 ATR down, roughly 1.4 to 1. ATR, average true range, measures how much a stock
      normally moves in a day, so it compares a 400 dollar stock and a 5 dollar stock fairly. And 73 percent
      of setups traded back to the marked Day 1 level, so those levels act like magnets. (Figure 8)</li>
      <li><b>The entry rule is the edge.</b> The playbook says do not buy the open. Wait for the Test, where
      price pulls back to the Day 1 level, then the Character Flip, where selling stops and buying takes over.
      Enter on that turn with a stop just beyond it. That rule turned the long side from a loser into about
      +1.66R and the short side into +1.46R, roughly +1.56R overall. R is your risk, the distance from entry
      to stop, so +1.5R is about one and a half times what you risked. (Figure 9)</li>
      <li><b>Trade by trade.</b> Winners ride the move and losers get cut fast when price breaks back below
      the turn. Small losses, bigger wins. The exit rule, out if the turn fails, is what keeps losses small.
      (Figure 10)</li>
    </ul>

    <h3>The verdict</h3>
    <p>The pattern is real, but the big continuation everyone notices is mostly an overnight gap you cannot
    trade. The part you can trade is the entry. The money is in the entry, not the setup. The pilot supports
    it at about +1.56R, so the edge is promising but not proven.</p>

    <h3>What it means for trading</h3>
    <ul>
      <li>The setup alone is not the edge. Buying or shorting the open does not work.</li>
      <li>The entry is the edge. Wait for the test and the flip.</li>
      <li>Favor strong but not blown out moves, and a real catalyst like earnings.</li>
      <li>Keep losses small. Get out when the turn fails.</li>
    </ul>

    <h3>Limits</h3>
    <ul>
      <li>The pilot is small, about 51 trades, so it points a direction rather than proving one.</li>
      <li>Costs are not included. Commission, spread, and the cost to borrow shares for a short eat into
      results, most on smaller stocks.</li>
      <li>Some winners had tight stops, which flatters the R numbers.</li>
      <li>The group may carry selection bias, with no control group of failed setups yet.</li>
    </ul>

    <h3>Next steps</h3>
    <p>Run the entry rule across more setups, add real costs, and add a control group to separate edge from
    market drift. A rebuild of the universe at the playbook's own thresholds, with a deeper look at the long
    and short sides, is already underway.</p>

    </div>''')

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Day 2 — The Follow-Through · Full Report</title><style>{CSS}</style></head>
<body><div class="wrap">
  <div class="hero">
    <div class="kick">INSTITUTIONAL FOLLOW-THROUGH STUDY</div>
    <h1>Day&nbsp;2: The Follow-Through</h1>
    <p>The Day 2 continuation setup is buying or shorting a stock the morning after a big, high volume,
       conviction close move. <b>Part 1</b> is the daily pattern across <b>841 setups</b> (May 2025 to
       May 2026). <b>Part 2</b> tests it on intraday data. <b>Part 3</b> is the one page verdict.
       <b>Part 4</b> is the written summary.</p>
  </div>
  <div class="content">
    {''.join(parts)}
  </div>
  <div class="foot">
    841 Day 2 setups across 666 tickers, May 2025 to May 2026. Intraday pilot of 51 setups, Polygon 1 minute bars.
    Continuation means the Day 2 open gapped in the setup's direction. R is the risk to the stop below the turn.
    All charts are embedded in this file, so select all and copy to keep the images.
  </div>
</div></body></html>"""

    with open("Day2_Report.html", "w") as fh:
        fh.write(doc)
    import os
    print("wrote Day2_Report.html  (%.1f MB)" % (os.path.getsize("Day2_Report.html")/1e6))

if __name__ == "__main__":
    build()
