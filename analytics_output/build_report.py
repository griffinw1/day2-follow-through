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
  "For this idea to be in play we want <b>high relative volume (RVOL)</b>, which means real institutional money is involved, not retail. Every setup in this dataset cleared at least three times its average daily volume, with a median near four times."),
 ("charts/closeloc.png", 2, "A bimodal conviction fingerprint",
  "For these setups to be most in play we want them to <b>close right at the high or low of the Day 1 range</b>, which shows conviction holding into the close instead of a move that faded. In this dataset the closes cluster hard at the extremes with almost nothing in the middle."),
 ("charts/payoff.png", 3, "A catalyst nearly doubles the edge",
  "We want <b>the move to keep going the next day</b>, and most of the time it does. Roughly three quarters of setups continued in the same direction, and that rate climbs higher still when a fresh catalyst is sitting behind the move."),
 ("charts/catalyst.png", 4, "Earnings shifts the whole distribution",
  "We want <b>a real catalyst like earnings</b> driving the move, because that is where almost all of the edge lives. With an earnings catalyst the follow through is far larger, but strip the catalyst out and the structural setup on its own gives back nearly all of its advantage."),
 ("charts/extension.png", 5, "The extension paradox",
  "We want a big move but <b>not the most extreme one</b>. The wildest and highest volume names follow through the least, so the cleanest continuation comes from strong but not blown out moves rather than the lottery tickets everyone is chasing."),
 ("charts/monthly.png", 6, "A persistent, year-round edge",
  "We want to know this is a real edge and not luck from one hot stretch. The continuation rate held up in every single month of the sample, so within this dataset the effect <b>does not appear to be regime dependent</b>."),
]
INTRADAY = [
 ("charts/event_study.png", 7, "From the open: longs fade, shorts follow through",
  "Here is the catch. <b>Most of the move often happens overnight</b>, so if you are just buying at the open you are giving up a large part of the edge before you are even in the trade. That is even more true for the longs, where the realized path from the open actually fades."),
 ("charts/mfe_mae.png", 8, "Trade quality: room up vs. room down",
  "When these trades work they hand us more room in our favor than against us. On average the setup returns a <b>reward to risk of about 1.4 to 1</b>, with the typical trade running near 0.75 ATR our way versus 0.54 ATR against, and price usually reaches the level we marked before it turns."),
 ("charts/entry_compare.png", 9, "The entry rule is the edge",
  "<b>If you are not playing for the overnight gap, do not buy the open.</b> Wait for the stock to test a level and turn, then enter on that turn, because that is what separates a real edge from a coin flip."),
 ("charts/trade_cards.png", 10, "Twelve trades, worst to best",
  "Trade by trade, <b>winners keep running while losers get cut fast</b> with a tight stop, which is how the strategy ends up taking small losses and letting the bigger wins pay for them."),
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
    takeaways = ('''
    <div class="part"><span>KEY TAKEAWAYS</span> &nbsp; What the Data Told Us</div>
    <div class="sum">
      <h3>1. Longs carried more forgiving edge than shorts</h3>
      <p>In our testing the long side gave us more room for error. We are not saying shorts have no edge, we
      think there is real discretionary edge there, but longs were more forgiving. Taken on the disciplined
      entry, waiting for the test and the flip instead of buying the open, the long side returned about
      <b>+1.66R</b> for us and stayed positive across a much broader and looser set of setups. The short side
      only worked in a narrow window, a controlled two to three day run that did not end in a vertical climax,
      at about <b>+1.16R with a 55 percent win rate</b>, and the names most people would call the strongest
      shorts, the vertical parabolas, actually lost and stopped out on nearly every attempt. We will also say
      it plainly, <b>the short Day 2s we think have the most edge are not even in this dataset</b>, they get
      screened out before we ever see them. Longs forgive imprecision, shorts punish it.</p>

      <h3>2. The thresholds here are stricter than they need to be</h3>
      <p>This dataset requires a Day 1 range of at least 2 ATR, and nothing smaller is included, <b>0 of the
      841 setups</b> sit below it. The playbook itself only calls for more than 1 ATR, so the data is about
      twice as strict as the method it is testing. That cutoff quietly removes the setups we like most. Think about a short setup where the stock
      only ran up about 2 ATR, or less. If the Day 1 move down is the same size or bigger, it has already
      covered the entire run up, so there may be no meat on the bone left for another leg down. When we rebuilt the universe at the real threshold, about <b>32,800 setups qualified versus the 841
      here</b>, so this dataset captured only around <b>2.5 percent</b> of the actual opportunity set. As noted in the
      first point, this 2 ATR floor is exactly what screens out the short setups we like best.</p>

      <h3>3. Without a catalyst there is no real edge, and the earnings edge does not generalize</h3>
      <p>The dataset shows an edge when an earnings catalyst is present, you can see it in the catalyst charts
      above, but that edge does not hold up once you test it broadly and pay real costs. Trading the drift
      after earnings does not work in practice. In large stocks the news is priced in almost instantly, and in
      small stocks the drift is real but lives in names you cannot trade cheaply, wide spreads, thin volume,
      and hard or expensive borrow, so the costs eat whatever is there. A catalyst is necessary but not
      sufficient, and it does not have to be earnings. The real edge comes from judging each setup on its own,
      the catalyst, the structure, the trend, and the tape together, not from one fixed screen.</p>
    </div>''')
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
    parts.append(takeaways)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Day 2 — The Follow-Through · Full Report</title><style>{CSS}</style></head>
<body><div class="wrap">
  <div class="hero">
    <div class="kick">INSTITUTIONAL FOLLOW-THROUGH STUDY</div>
    <h1>Day&nbsp;2: The Follow-Through</h1>
    <p>The Day 2 continuation setup is buying or shorting a stock the morning after a big, high volume,
       conviction close move. <b>Part 1</b> is the daily pattern across <b>841 setups</b> (May 2025 to
       May 2026) and <b>Part 2</b> tests it on intraday data. Our key takeaways are at the bottom.</p>
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
