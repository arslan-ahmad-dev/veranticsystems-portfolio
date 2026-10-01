"""Builds the project grid in index.html and one detail page per project.
Run from the repo root:  python tools/build.py
Edit project content in tools/data.py."""
import html, re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from data import PROJECTS, GROUPS
from icons import ICONS

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIVE = "https://portfolio.veranticsystems.com/"

def esc(s): return html.escape(s, quote=False)
def attr(s): return html.escape(s, quote=True)
def chips(items): return "".join(f'<span class="chip">{esc(s)}</span>' for s in items)
def li(items): return "".join(f"<li>{esc(i)}</li>" for i in items)

# ---------------------------------------------------------------- mockups
A = 'var(--accent)'
def r(x, y, w, h, rx=6, fill='var(--bg-abyss)', op=1, stroke=None):
    s = f' stroke="{stroke}" stroke-opacity=".28"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="{op}"{s}/>'
def bar(x, y, w, h=8, op=.18): return r(x, y, w, h, 4, 'var(--text-muted)', op)
def acc(x, y, w, h, rx=6, op=.9): return r(x, y, w, h, rx, A, op)
def tint(x, y, w, h, rx=8, op=.14): return r(x, y, w, h, rx, A, op)

def frame(inner, title):
    return (f'<svg class="pf-shot__svg" viewBox="0 0 640 400" role="img" aria-label="{attr(title)}" xmlns="http://www.w3.org/2000/svg">'
            + r(0, 0, 640, 400, 14, 'var(--bg-void)', 1, A)
            + r(0, 0, 640, 34, 14, 'var(--bg-abyss)', 1) + r(0, 20, 640, 14, 0, 'var(--bg-abyss)', 1)
            + '<circle cx="20" cy="17" r="5" fill="var(--accent)" fill-opacity=".9"/><circle cx="38" cy="17" r="5" fill="var(--accent)" fill-opacity=".5"/><circle cx="56" cy="17" r="5" fill="var(--accent)" fill-opacity=".25"/>'
            + bar(90, 12, 180, 10, .22) + inner + '</svg>')

def side(): return r(0, 34, 112, 366, 0, 'var(--bg-abyss)', 1) + "".join(
    (acc(14, 54 + i * 34, 84, 22, 6, .9) if i == 0 else bar(14, 60 + i * 34, 70 - (i % 3) * 10, 8, .22)) for i in range(7))

def m_dash():
    s = side()
    for i in range(3):
        x = 130 + i * 164
        s += r(x, 52, 152, 70, 10, 'var(--bg-abyss)', 1, A) + bar(x + 14, 66, 60, 7, .3) + acc(x + 14, 84, 70 + i * 12, 16, 4, .95) + bar(x + 14, 108, 100, 6, .16)
    s += r(130, 138, 330, 244, 10, 'var(--bg-abyss)', 1, A) + bar(146, 152, 90, 8, .3)
    hs = [60, 96, 76, 128, 104, 150, 132, 170, 146]
    for i, h in enumerate(hs): s += acc(150 + i * 34, 366 - h, 22, h, 4, .35 + (i % 3) * .2)
    s += r(476, 138, 150, 244, 10, 'var(--bg-abyss)', 1, A) + bar(490, 152, 70, 8, .3)
    for i in range(6): s += tint(490, 176 + i * 32, 122, 22, 6, .16 + (i % 2) * .08)
    return s

def m_table():
    s = side() + r(130, 52, 496, 330, 10, 'var(--bg-abyss)', 1, A) + tint(130, 52, 496, 34, 10, .2)
    for i, w in enumerate([80, 120, 70, 60]): s += bar(146 + sum([80, 120, 70, 60][:i]) + i * 40, 64, w, 8, .4)
    for row in range(8):
        y = 98 + row * 34
        s += r(142, y, 472, 28, 6, 'var(--bg-void)', .6)
        s += bar(154, y + 10, 70, 8) + bar(280, y + 10, 100 + (row % 3) * 16, 8) + bar(440, y + 10, 50, 8)
        s += acc(540, y + 5, 54, 18, 9, .25 + (row % 3) * .2)
    return s

def m_chat():
    s = r(0, 34, 200, 366, 0, 'var(--bg-abyss)', 1)
    for i in range(6): s += (tint(10, 48 + i * 52, 180, 44, 8, .22) if i == 1 else r(10, 48 + i * 52, 180, 44, 8, 'var(--bg-void)', .6)) + bar(22, 62 + i * 52, 90, 8, .35) + bar(22, 78 + i * 52, 140, 6, .18)
    s += bar(220, 52, 120, 9, .35)
    s += r(220, 76, 250, 56, 12, 'var(--bg-abyss)', 1, A) + bar(236, 92, 200, 7) + bar(236, 108, 150, 7)
    s += r(300, 146, 320, 112, 12, A, .14, A) + acc(316, 160, 90, 10, 4, .85) + bar(316, 182, 280, 7, .3) + bar(316, 198, 260, 7, .3) + bar(316, 214, 200, 7, .3)
    s += r(316, 232, 120, 18, 9, A, .25, A) + r(444, 232, 80, 18, 9, 'var(--bg-void)', 1, A)
    s += r(220, 276, 400, 22, 8, 'var(--bg-abyss)', 1, A) + bar(232, 283, 120, 7, .3)
    s += r(220, 312, 400, 72, 10, 'var(--bg-abyss)', 1, A) + bar(234, 326, 130, 7, .4) + bar(234, 344, 330, 6, .2) + bar(234, 358, 280, 6, .2)
    return s

def m_map():
    s = r(0, 34, 640, 366, 0, 'var(--bg-abyss)', 1)
    for i in range(1, 10): s += f'<path d="M{i*64} 34 V400" stroke="var(--accent)" stroke-opacity=".08"/>'
    for i in range(1, 8): s += f'<path d="M0 {34+i*46} H640" stroke="var(--accent)" stroke-opacity=".08"/>'
    s += '<path d="M60 340 C140 260 200 300 260 220 S400 170 470 110 580 90 600 70" fill="none" stroke="var(--accent)" stroke-width="5" stroke-linecap="round" stroke-opacity=".7"/>'
    for x, y in [(60, 340), (260, 220), (470, 110), (600, 70), (340, 300), (180, 150)]:
        s += f'<circle cx="{x}" cy="{y}" r="11" fill="var(--accent)" fill-opacity=".25"/><circle cx="{x}" cy="{y}" r="6" fill="var(--accent)"/>'
    s += r(16, 50, 190, 180, 12, 'var(--bg-void)', .96, A)
    s += bar(30, 64, 80, 8, .4)
    for i in range(4): s += tint(28, 88 + i * 34, 166, 26, 7, .16) + bar(38, 97 + i * 34, 90, 7, .35)
    return s

def m_cal():
    s = side() + bar(130, 50, 120, 9, .4)
    for d in range(7): s += bar(150 + d * 68, 76, 40, 7, .35)
    for w in range(5):
        for d in range(7): s += r(134 + d * 68, 92 + w * 58, 62, 52, 6, 'var(--bg-abyss)', 1, A)
    for (d, w, h, o) in [(1, 0, 30, .9), (3, 0, 20, .45), (0, 1, 36, .6), (4, 1, 24, .9), (2, 2, 34, .45), (5, 2, 22, .9), (1, 3, 30, .6), (6, 3, 26, .45), (3, 4, 32, .9)]:
        s += acc(138 + d * 68, 98 + w * 58, 54, h, 5, o)
    return s

def m_cards():
    s = ""
    for i in range(6):
        x = 24 + (i % 3) * 200; y = 52 + (i // 3) * 170
        s += r(x, y, 188, 158, 12, 'var(--bg-abyss)', 1, A) + tint(x + 10, y + 10, 168, 84, 8, .18 + (i % 3) * .06)
        s += bar(x + 12, y + 106, 110, 8, .38) + bar(x + 12, y + 124, 70, 7, .2) + acc(x + 128, y + 120, 48, 20, 10, .85)
    return s

def m_player():
    s = r(40, 56, 560, 150, 14, 'var(--bg-abyss)', 1, A) + acc(60, 76, 56, 56, 12, .85) + bar(132, 84, 180, 10, .45) + bar(132, 106, 120, 7, .25)
    for i in range(46):
        h = 14 + ((i * 37) % 46)
        s += r(60 + i * 11.6, 176 - h / 2 - 10, 7, h, 3, A, .35 + (i % 4) * .15)
    s += r(60, 196, 520, 5, 3, 'var(--text-muted)', .2) + r(60, 196, 270, 5, 3, A, .95)
    s += r(40, 224, 560, 160, 14, 'var(--bg-abyss)', 1, A) + acc(60, 244, 24, 24, 12, .9) + bar(94, 250, 70, 8, .4) + bar(94, 268, 420, 7, .22)
    s += r(60, 290, 24, 24, 12, 'var(--text-muted)', .5) + bar(94, 296, 70, 8, .4) + bar(94, 314, 380, 7, .22)
    s += acc(60, 336, 24, 24, 12, .9) + bar(94, 342, 70, 8, .4) + bar(94, 360, 330, 7, .22)
    return s

def m_kanban():
    s = ""
    for c, name in enumerate(range(3)):
        x = 24 + c * 204
        s += r(x, 52, 192, 332, 12, 'var(--bg-abyss)', 1, A) + acc(x + 14, 66, 70, 10, 5, .8)
        for i in range(4 - c % 2):
            y = 92 + i * 72
            s += r(x + 10, y, 172, 62, 8, 'var(--bg-void)', .9, A) + bar(x + 20, y + 12, 110, 8, .4) + bar(x + 20, y + 30, 140, 6, .2) + acc(x + 20, y + 44, 40, 10, 5, .3 + (i % 3) * .25)
    return s

def m_doc():
    s = r(40, 50, 330, 336, 10, 'var(--bg-abyss)', 1, A) + acc(60, 70, 80, 14, 4, .9) + bar(260, 70, 90, 8, .3)
    for i in range(9): s += bar(60, 108 + i * 22, 250 - (i % 3) * 40, 7, .2)
    for y in (126, 192, 280): s += r(56, y - 6, 270, 20, 5, A, .2, A)
    s += r(390, 50, 220, 336, 10, 'var(--bg-abyss)', 1, A) + bar(406, 66, 90, 8, .4)
    for i in range(6):
        y = 92 + i * 48
        s += bar(406, y, 60, 6, .3) + r(406, y + 12, 188, 22, 6, 'var(--bg-void)', .9, A) + bar(414, y + 20, 90 + (i % 3) * 20, 6, .35) + acc(566, y + 16, 22, 14, 7, .35 + (i % 3) * .25)
    return s

def m_video():
    s = r(24, 50, 400, 300, 12, 'var(--bg-abyss)', 1, A) + '<circle cx="224" cy="180" r="50" fill="var(--accent)" fill-opacity=".2"/><circle cx="224" cy="168" r="20" fill="var(--accent)" fill-opacity=".6"/><path d="M180 232 a44 34 0 0 1 88 0" fill="var(--accent)" fill-opacity=".6"/>'
    s += r(316, 62, 96, 70, 8, 'var(--bg-void)', 1, A) + '<circle cx="364" cy="88" r="12" fill="var(--accent)" fill-opacity=".5"/>'
    for i, o in enumerate((.9, .35, .35, .35)): s += r(150 + i * 44, 318, 32, 22, 11, A if i == 0 else 'var(--text-muted)', o)
    s += r(440, 50, 176, 300, 12, 'var(--bg-abyss)', 1, A) + bar(454, 66, 80, 8, .4)
    for i in range(7): s += bar(454, 96 + i * 30, 150 - (i % 3) * 24, 7, .22)
    s += r(24, 364, 592, 22, 8, 'var(--bg-abyss)', 1, A)
    return s

def m_flow():
    s = ""
    pos = [(40, 70), (250, 70), (460, 70), (40, 250), (250, 250), (460, 250)]
    for i, (x, y) in enumerate(pos):
        s += r(x, y, 140, 80, 12, 'var(--bg-abyss)', 1, A) + (acc(x + 14, y + 16, 60, 10, 5, .9) if i % 2 == 0 else tint(x + 14, y + 14, 60, 12, 6, .5)) + bar(x + 14, y + 40, 100, 7, .3) + bar(x + 14, y + 56, 70, 6, .18)
    for (x1, y1, x2, y2) in [(180, 110, 250, 110), (390, 110, 460, 110), (530, 150, 530, 250), (460, 290, 390, 290), (250, 290, 180, 290)]:
        s += f'<path d="M{x1} {y1} L{x2} {y2}" stroke="var(--accent)" stroke-width="3" stroke-linecap="round" stroke-opacity=".7"/>'
    s += '<circle cx="250" cy="110" r="5" fill="var(--accent)"/><circle cx="460" cy="110" r="5" fill="var(--accent)"/><circle cx="530" cy="250" r="5" fill="var(--accent)"/><circle cx="390" cy="290" r="5" fill="var(--accent)"/><circle cx="180" cy="290" r="5" fill="var(--accent)"/>'
    return s

MOCK = dict(dash=m_dash, table=m_table, chat=m_chat, map=m_map, cal=m_cal, cards=m_cards, player=m_player, kanban=m_kanban, doc=m_doc, video=m_video, flow=m_flow)

# ---------------------------------------------------------------- index pieces
def card(p, base="", feat=False):
    ic = ICONS[p["icon"]]
    href = f'{base}projects/{p["slug"]}/'
    cls = "work-card pf-card card" + (" pf-card--pod" if feat else "")
    return f'''            <div class="{cls}" data-group="{p['group']}" data-tilt>
              <div class="work-card__media">
                <div class="work-card__bg work-card__bg--{p['bg']}">
                  <svg class="work-card__art" viewBox="0 0 120 120" aria-hidden="true">{ic}</svg>
                </div>
                <span class="work-card__tag">{esc(p['tag'])}</span>
              </div>
              <div class="work-card__body">
                <p class="work-card__cat">{esc(p['cat'])}</p>
                <h3><a class="pf-card__title" href="{href}">{esc(p['name'])}</a></h3>
                <p class="pf-card__sum">{esc(p['short'])}</p>
                <ul class="pf-list">{li(p['bullets'])}</ul>
                <div class="chips pf-stack">{chips(p['stack'][:6])}</div>
                <span class="work-card__link pf-card__more">View details &amp; roadmap<span class="arrow">→</span></span>
              </div>
            </div>
'''

def build_index():
    p = ROOT / "index.html"
    t = p.read_text(encoding="utf-8")
    ordered = [x for x in PROJECTS if x.get("featured")] + [x for x in PROJECTS if not x.get("featured")]
    cards = "".join(card(x, feat=x.get("featured", False)) for x in ordered)
    block = f'''      <!-- projects:start -->
      <section class="sec sec--void" id="projects">
        <div class="container">
          <div class="work__grid pf-grid">
{cards}          </div>
        </div>
      </section>
      <!-- projects:end -->
'''
    t = re.sub(r"      <!-- projects:start -->.*?<!-- projects:end -->\n", lambda m: block, t, flags=re.S)
    p.write_text(t, encoding="utf-8")
    return t

# ---------------------------------------------------------------- detail pages
def shell_parts(index_html):
    head_end = index_html.index("</head>")
    head = index_html[:head_end]
    body_start = index_html.index("<body>")
    header = re.search(r"    <header>.*?</header>\n", index_html, re.S).group(0)
    footer = re.search(r"    <footer class=\"footer\">.*?</footer>\n", index_html, re.S).group(0)
    modal = re.search(r"  <!-- =+ BOOKING MODAL =+ -->.*?(?=  <script)", index_html, re.S).group(0)
    return head, header, footer, modal

def to_sub(s):  # rewrite root-relative paths for pages at projects/<slug>/
    for d in ("css", "js", "fonts", "images"):
        s = s.replace(f'"{d}/', f'"../../{d}/')
    return s

def build_detail(p, index_html, i):
    head, header, footer, modal = shell_parts(index_html)
    n = len(PROJECTS)
    prev_p, next_p = PROJECTS[(i - 1) % n], PROJECTS[(i + 1) % n]
    title = f'{p["name"]} | VeranticSystems Portfolio'
    desc = p["short"]
    url = f'{LIVE}projects/{p["slug"]}/'
    h = head
    h = re.sub(r"<title>.*?</title>", lambda m: f"<title>{esc(title)}</title>", h, count=1)
    h = re.sub(r'(<meta name="description" content=").*?(">)', lambda m: m.group(1) + attr(desc) + m.group(2), h, count=1)
    h = re.sub(r'(<link rel="canonical" href=").*?(">)', lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = re.sub(r'(og:title" content=").*?(">)', lambda m: m.group(1) + attr(title) + m.group(2), h)
    h = re.sub(r'(twitter:title" content=").*?(">)', lambda m: m.group(1) + attr(title) + m.group(2), h)
    h = re.sub(r'(og:description" content=").*?(">)', lambda m: m.group(1) + attr(desc) + m.group(2), h)
    h = re.sub(r'(twitter:description" content=").*?(">)', lambda m: m.group(1) + attr(desc) + m.group(2), h)
    h = re.sub(r'(og:url" content=").*?(">)', lambda m: m.group(1) + url + m.group(2), h)
    ld = '<script type="application/ld+json" data-seo>{"@context":"https://schema.org","@type":"CreativeWork","name":%s,"description":%s,"url":"%s","publisher":{"@type":"Organization","name":"VeranticSystems","url":"https://veranticsystems.com/"}}</script>' % (
        __import__("json").dumps(p["name"]), __import__("json").dumps(desc), url)
    h = re.sub(r'<script type="application/ld\+json" data-seo>.*?</script>', lambda m: ld, h, count=1, flags=re.S)
    h = to_sub(h)
    hdr = to_sub(header).replace('href="#top"', 'href="../../"').replace('<a href="#top" class="brand"', '<a href="../../" class="brand"')

    shots = "".join(
        f'<figure class="pf-shot card{" pf-shot--wide" if k == 0 else ""}">{frame(MOCK[kind](), cap)}<figcaption>{esc(cap)}</figcaption></figure>'
        for k, (kind, cap) in enumerate(p["screens"]))
    outcomes = "".join(f'<div class="mini"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in p["outcomes"])
    feats = "".join(f'<div class="rule card"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in p["features"])
    flow = "".join(f"<li><b>{esc(a)}</b><span>{esc(b)}</span></li>" for a, b in p["flow"])
    road = "".join(
        f'<li class="pf-road__item"><span class="pf-road__num">{k + 1}</span><div class="pf-road__body card"><div class="pf-road__top"><h3>{esc(ph)}</h3><span class="pf-road__time">{esc(du)}</span></div><ul class="pf-list">{li(tasks)}</ul></div></li>'
        for k, (ph, du, tasks) in enumerate(p["roadmap"]))
    note = ("A typical delivery roadmap for a project of this kind." if not p.get("featured")
            else "How the PodAgain work was sequenced, from audit to launch.")
    illus = ("Screens are illustrative layouts of the product, not client screenshots." if not p.get("featured")
             else "Screens are illustrative layouts of the product.")

    body = f'''<body>
<a class="skip-link" href="#main">Skip to content</a>

  <div class="bg-grid" aria-hidden="true"></div>
  <div class="bg-glow" aria-hidden="true"></div>

  <div class="page">

{hdr}
    <main id="main">

      <section class="page-hero pf-detail-hero">
        <div class="page-hero__blob" aria-hidden="true"></div>
        <div class="page-hero__blob page-hero__blob--2" aria-hidden="true"></div>
        <div class="container">
          <div class="page-hero__inner page-hero__inner--center">
            <a class="pf-back" href="../../#projects">← All projects</a>
            <p class="eyebrow">{esc(p['cat'])}</p>
            <h1 class="page-hero__title">{esc(p['name'])}</h1>
            <p class="page-hero__lead">{esc(p['short'])}</p>
            <div class="chips pf-stack pf-stack--center">{chips(p['stack'])}</div>
          </div>
        </div>
      </section>

      <section class="sec sec--void">
        <div class="container">
          <div class="pf-shots">{shots}</div>
          <p class="pf-note pf-note--center">{esc(illus)}</p>
        </div>
      </section>

      <section class="sec sec--abyss">
        <div class="section-line" aria-hidden="true"></div>
        <div class="container">
          <div class="pf-two">
            <div>
              <p class="eyebrow">Overview</p>
              <h2 class="h2 pf-h2">What it is</h2>
              <p class="pf-text">{esc(p['overview'])}</p>
            </div>
            <div>
              <p class="eyebrow">The problem</p>
              <h2 class="h2 pf-h2">Why it was needed</h2>
              <p class="pf-text">{esc(p['problem'])}</p>
            </div>
          </div>
          <div class="work-item__metrics pf-outcomes">{outcomes}</div>
        </div>
      </section>

      <section class="sec sec--void">
        <div class="section-line" aria-hidden="true"></div>
        <div class="container">
          <div class="section-head">
            <p class="eyebrow">Features</p>
            <h2 class="h2">What We Built</h2>
          </div>
          <div class="pf-features">{feats}</div>
        </div>
      </section>

      <section class="sec sec--abyss">
        <div class="section-line" aria-hidden="true"></div>
        <div class="container">
          <div class="section-head">
            <p class="eyebrow">Architecture</p>
            <h2 class="h2">How It Fits Together</h2>
          </div>
          <div class="pf-arch card">
            <ol class="pf-flow">{flow}</ol>
            <p class="pf-note">{esc(p['flownote'])}</p>
          </div>
        </div>
      </section>

      <section class="sec sec--void">
        <div class="section-line" aria-hidden="true"></div>
        <div class="container">
          <div class="section-head">
            <p class="eyebrow">Roadmap</p>
            <h2 class="h2">From Idea to Launch</h2>
            <p>{esc(note)}</p>
          </div>
          <ol class="pf-road">{road}</ol>
        </div>
      </section>

      <section class="sec sec--abyss">
        <div class="section-line" aria-hidden="true"></div>
        <div class="container">
          <div class="pf-cta card">
            <div><h2 class="h2 pf-h2">Want something like this?</h2><p class="pf-text">Tell us what it should do and we'll come back with a stack, a scope and a timeline.</p></div>
            <button type="button" class="btn-primary btn-shimmer" data-book>Discuss Your Project</button>
          </div>
          <nav class="pf-pager" aria-label="More projects">
            <a href="../{prev_p['slug']}/"><span>← Previous</span><b>{esc(prev_p['name'])}</b></a>
            <a href="../{next_p['slug']}/" class="pf-pager__next"><span>Next →</span><b>{esc(next_p['name'])}</b></a>
          </nav>
        </div>
      </section>
    </main>

{to_sub(footer)}
  </div>

{modal}  <script src="../../js/config.js"></script>
  <script src="../../js/main.js"></script>
</body>
</html>
'''
    out = ROOT / "projects" / p["slug"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(h + "</head>\n" + body, encoding="utf-8")

def build_sitemap():
    urls = [LIVE] + [f'{LIVE}projects/{p["slug"]}/' for p in PROJECTS]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    x += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(x, encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {LIVE}sitemap.xml\n", encoding="utf-8")

if __name__ == "__main__":
    idx = build_index()
    for i, p in enumerate(PROJECTS):
        build_detail(p, idx, i)
    build_sitemap()
    print("built", len(PROJECTS), "detail pages")
