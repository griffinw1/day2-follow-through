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

    parts.append('''
    <div class="part"><span>PART 4</span> &nbsp; The Full Picture, Explained Simply</div>
    <p class="lead">A plain language walkthrough of everything above, written so a newer trader can follow it
    start to finish. Every point ties back to a chart in this report.</p>
    <div class="sum">

    <h3>What this study set out to answer</h3>
    <p>The Day 2 trade is simple to describe. A stock has a huge, high volume day, which we call Day 1. The
    question we tested is whether the next morning, Day 2, you can make money trading in the same direction
    as that big move. We looked at 841 of these big days between May 2025 and May 2026, and then zoomed in
    on a smaller group minute by minute to see what actually happened once the market opened.</p>

    <h3>Part 1, the daily picture looked very strong</h3>
    <p>Seen from a distance, using only end of day data, the setup looks like a clean edge. Five things stood out.</p>
    <ul>
      <li><b>Real institutional volume.</b> Every stock we kept traded on enormous volume, at least three
      times its own normal daily volume and usually about four times. Traders call this relative volume, or
      RVOL. Volume that large means big players such as funds and trading desks were active, not just
      individuals. That is the fingerprint we want before calling something a Day 1. (Figure 1)</li>
      <li><b>A conviction close.</b> We also looked at where each stock finished inside its daily range,
      which is called the close location. Bullish setups closed right at the high of the day and bearish
      setups right at the low, with almost nothing finishing in the middle. Closing at the extreme is a sign
      that buyers, or sellers, stayed in control all the way into the end of the day. (Figure 2)</li>
      <li><b>A high continuation rate.</b> On Day 2, about 73 percent of these stocks opened gapped in the
      same direction as the Day 1 move. When a fresh news catalyst was behind the move that rose to about 87
      percent, and to about 93 percent for bullish earnings. (Figures 3 and 4)</li>
      <li><b>Stronger is not always better.</b> The most extreme, most blown out volume names actually
      followed through the least. The cleanest and most reliable continuation came from strong but not crazy
      moves, not from the lottery ticket names everyone chases. (Figure 5)</li>
      <li><b>It held all year.</b> This was not one lucky month. The continuation rate showed up in every
      single month of the year and never fell below about 64 percent. (Figure 6)</li>
    </ul>
    <p>On paper, that is a clear and repeatable pattern.</p>

    <h3>Part 2, the honest intraday check</h3>
    <p>The daily view is encouraging, but it hides a problem that only shows up when you watch the trade
    minute by minute.</p>
    <ul>
      <li><b>The catch.</b> That 73 percent continuation is mostly the overnight gap, the jump that happens
      between one day's close and the next day's open, while you are flat and cannot do anything about it. If
      you instead measure from a price you could actually get, the Day 2 open, the long side flips from a
      winner to a loser. Buying the open of a bullish setup won only about 44 percent of the time. So the
      headline number was the gap, not a trade you could take. (Figure 7)</li>
      <li><b>The structure is still real.</b> Even so, the move has good shape. In the minute by minute
      pilot, the typical trade offered more room in your favor than against you, about 0.75 ATR up versus
      0.54 ATR down, which is roughly 1.4 to 1. ATR, or average true range, is just a measure of how much a
      stock normally moves in a day, so we can compare a 400 dollar stock and a 5 dollar stock fairly. On top
      of that, 73 percent of setups traded back to the Day 1 level we had marked, so those levels act like
      magnets. (Figure 8)</li>
      <li><b>The entry rule is the real edge.</b> The playbook is explicit that you should not buy the open.
      You wait for two things. First the Test, where price pulls back to the Day 1 level. Then the Character
      Flip, the moment the selling stops and buying clearly takes over. You enter on that turn and place your
      stop just beyond it. When we backtested that exact rule, the long side went from a loser to about
      +1.66R and the short side to about +1.46R, for roughly +1.56R overall. R simply means your risk, the
      distance from your entry to your stop, so +1.5R means you earned about one and a half times what you
      were risking. (Figure 9)</li>
      <li><b>Trade by trade.</b> Looking at individual trades from worst to best, the winners ride the
      favorable move while the losers are cut quickly when price breaks back below the turn. The result is
      small losses and bigger wins. That single exit rule, get out if the turn fails, is what keeps the
      losers small. (Figure 10)</li>
    </ul>

    <h3>Part 3, the verdict in one breath</h3>
    <p>Putting it together, the pattern is real, but the part that grabs attention, the big continuation, is
    mostly an overnight gap you cannot trade. The part you can trade is the entry. The money comes from
    discipline at the entry, not from the setup by itself. The pilot supports this at about +1.56R, which
    makes the edge promising rather than proven.</p>

    <h3>What to take away, in plain terms</h3>
    <ul>
      <li>The setup alone is not the edge. Buying or shorting the open does not work.</li>
      <li>The entry rule is the edge. Wait for the test and the flip before you commit.</li>
      <li>Favor strong but not blown out moves, and favor setups with a real catalyst such as earnings.</li>
      <li>Keep every loss small by honoring the one exit rule when the turn fails.</li>
    </ul>

    <h3>What we still do not know</h3>
    <p>This is a first look, not a finished product, and a few honest limits matter.</p>
    <ul>
      <li>The minute by minute pilot is small, about 51 trades, so it points in a direction rather than
      proving one.</li>
      <li>Trading costs are not included yet. Commission, the spread between the bid and the ask, and the
      cost to borrow shares for a short all eat into results, and they hit hardest on smaller stocks.</li>
      <li>Some winners had very tight stops, which can make the R numbers look better than they would in
      real trading.</li>
      <li>The group we studied may carry selection bias, and we do not yet have a control group of failed
      setups to compare against.</li>
    </ul>

    <h3>Where this is heading</h3>
    <p>The next steps are to run the same entry rule across many more setups, to add realistic trading costs,
    and to add a control group so we can tell a true edge apart from the market simply drifting upward. Work
    has also begun on rebuilding the universe at the playbook's own thresholds and studying the long and
    short sides in more depth, which will feed a future version of this report.</p>

    </div>''')

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
