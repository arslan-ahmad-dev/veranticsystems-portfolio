"""Realistic product-screen mockups drawn as inline SVG (crisp at any size, follows the site's light and dark themes).

Every screen shows SAMPLE data written for the portfolio. Nothing here is a client screenshot or real data; the frame says so.
render(kind, spec, url) returns a complete <svg>. Specs live in tools/screens.py.
"""
import html, math

A = "var(--accent)"
TXT, MUT, SUB = "var(--text-primary)", "var(--text-muted)", "var(--text-subtle)"
PAN, BG, VOID = "var(--bg-abyss)", "var(--bg-void)", "var(--bg-void)"
OK, WARN, BAD = "#1f9d57", "#c98a0a", "#d64545"
TONES = {"ok": OK, "warn": WARN, "bad": BAD, "info": A, "muted": MUT}


def e(s): return html.escape(str(s), quote=False)


def fit(s, size, maxw):
    s = str(s); lim = max(1, int(maxw / (size * 0.56)))
    return s if len(s) <= lim else s[: max(1, lim - 1)].rstrip() + "…"


def R(x, y, w, h, rx=8, fill=VOID, op=1, stroke=None, so=.2, sw=1):
    st = f' stroke="{stroke}" stroke-opacity="{so}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="{op}"{st}/>'


def card(x, y, w, h, rx=10): return R(x, y, w, h, rx, VOID, 1, A, .18)


def T(x, y, s, size=12, weight=400, fill=TXT, anchor="start", op=1, maxw=None):
    s = fit(s, size, maxw) if maxw else s
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" fill-opacity="{op}" text-anchor="{anchor}">{e(s)}</text>'


def line(x1, y1, x2, y2, op=.14, w=1, col=A, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round"{d}/>'


def pill(x, y, label, tone="info", size=10, align="start"):
    w = int(len(label) * size * 0.58 + 14); c = TONES.get(tone, A)
    x0 = x - w if align == "end" else x
    return R(x0, y, w, size + 9, (size + 9) / 2, c, .14) + T(x0 + w / 2, y + size + 1.5, label, size, 600, c, "middle"), w


def pill_s(x, y, label, tone="info", size=10, align="start"): return pill(x, y, label, tone, size, align)[0]


def avatar(cx, cy, r, label, op=.9):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{A}" fill-opacity=".18"/>' + T(cx, cy + r * .36, label, r * .95, 700, A, "middle", op)


def frame(inner, title, url="app.example.com"):
    return (f'<svg class="pf-shot__svg" viewBox="0 0 640 400" role="img" aria-label="{e(title)}" xmlns="http://www.w3.org/2000/svg">'
            + R(0, 0, 640, 400, 14, BG, 1, A, .3)
            + R(0, 0, 640, 34, 14, PAN, 1) + R(0, 20, 640, 14, 0, PAN, 1)
            + f'<circle cx="20" cy="17" r="5" fill="{A}" fill-opacity=".9"/><circle cx="38" cy="17" r="5" fill="{A}" fill-opacity=".5"/><circle cx="56" cy="17" r="5" fill="{A}" fill-opacity=".25"/>'
            + R(80, 8, 250, 19, 9.5, VOID, 1, A, .16) + T(92, 21, fit(url, 10, 226), 10, 500, MUT)
            + R(520, 8, 104, 19, 9.5, A, .1) + T(572, 21, "Sample data", 10, 600, A, "middle")
            + inner + "</svg>")


def sidebar(items, active=0, w=112):
    s = R(0, 34, w, 366, 0, PAN, 1) + line(w, 34, w, 400, .12)
    for i, it in enumerate(items):
        y = 52 + i * 32
        if i == active: s += R(10, y - 4, w - 20, 26, 7, A, .16) + f'<circle cx="23" cy="{y + 9}" r="3.5" fill="{A}"/>' + T(34, y + 13, it, 11, 700, TXT, maxw=w - 44)
        else: s += f'<circle cx="23" cy="{y + 9}" r="3" fill="{SUB}" fill-opacity=".6"/>' + T(34, y + 13, it, 11, 500, MUT, maxw=w - 44)
    return s


def header(x, y, title, sub=None, right=None):
    s = T(x, y, title, 16, 700, TXT)
    if sub: s += T(x, y + 16, sub, 10.5, 400, MUT)
    if right:
        w = int(len(right) * 6.2 + 20)
        s += R(626 - w, y - 15, w, 22, 11, VOID, 1, A, .2) + T(626 - w / 2, y, right, 10, 600, MUT, "middle")
    return s


def kpi(x, y, w, label, value, delta=None, tone="ok"):
    s = card(x, y, w, 62) + T(x + 12, y + 20, label, 10.5, 500, MUT, maxw=w - 20) + T(x + 12, y + 46, value, 20, 700, TXT, maxw=w - 20)
    if delta: s += T(x + w - 12, y + 46, delta, 10.5, 700, TONES[tone], "end")
    return s


def chart(x, y, w, h, title, vals, xlabels, unit="", fmt=None, tone_line=A, second=None):
    """Area/line chart with horizontal grid, y labels, x labels, end-point value."""
    fmt = fmt or (lambda v: f"{v:,.0f}")
    s = card(x, y, w, h) + T(x + 14, y + 22, title, 12, 700)
    px0, px1, py0, py1 = x + 44, x + w - 16, y + 38, y + h - 30
    allv = vals + (second or [])
    lo, hi = min(allv), max(allv)
    span = (hi - lo) or 1; lo2, hi2 = lo - span * .1, hi + span * .12
    for i in range(5):
        gy = py1 - (py1 - py0) * i / 4; gv = lo2 + (hi2 - lo2) * i / 4
        s += line(px0, gy, px1, gy, .1) + T(px0 - 6, gy + 3.5, fmt(gv) + unit, 9, 400, SUB, "end")
    def pts(series):
        return [(px0 + (px1 - px0) * i / (len(series) - 1), py1 - (py1 - py0) * (v - lo2) / (hi2 - lo2)) for i, v in enumerate(series)]
    def path(p): return "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in p)
    pp = pts(vals)
    s += f'<path d="{path(pp)} L{pp[-1][0]:.1f} {py1} L{pp[0][0]:.1f} {py1} Z" fill="{tone_line}" fill-opacity=".1"/>'
    if second:
        p2 = pts(second); s += f'<path d="{path(p2)}" fill="none" stroke="{MUT}" stroke-opacity=".55" stroke-width="2" stroke-dasharray="4 4" stroke-linecap="round"/>'
    s += f'<path d="{path(pp)}" fill="none" stroke="{tone_line}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>'
    ex, ey = pp[-1]
    s += f'<circle cx="{ex}" cy="{ey}" r="4.5" fill="{tone_line}"/><circle cx="{ex}" cy="{ey}" r="9" fill="{tone_line}" fill-opacity=".18"/>'
    lbl = fmt(vals[-1]) + unit
    s += R(ex - 54, ey - 30, 48, 18, 6, TXT, .92) + T(ex - 30, ey - 17.5, lbl, 10, 700, BG, "middle")
    step = max(1, len(xlabels) // 6)
    for i, lb in enumerate(xlabels):
        if i % step == 0: s += T(px0 + (px1 - px0) * i / (len(xlabels) - 1), py1 + 16, lb, 9, 400, SUB, "middle")
    return s


def bars(x, y, w, h, title, vals, labels, tone=A, fmt=None):
    fmt = fmt or (lambda v: f"{v:,.0f}")
    s = card(x, y, w, h) + T(x + 14, y + 22, title, 12, 700)
    px0, px1, py0, py1 = x + 14, x + w - 14, y + 40, y + h - 26
    mx = max(vals) * 1.15; n = len(vals); gap = 8; bw = (px1 - px0 - gap * (n - 1)) / n
    for i in range(4): s += line(px0, py1 - (py1 - py0) * i / 3, px1, py1 - (py1 - py0) * i / 3, .08)
    for i, v in enumerate(vals):
        bh = (py1 - py0) * v / mx; bx = px0 + i * (bw + gap)
        s += R(bx, py1 - bh, bw, bh, 4, tone, .35 + .5 * (i == n - 1))
        s += T(bx + bw / 2, py1 - bh - 5, fmt(v), 9, 700, TXT, "middle") + T(bx + bw / 2, py1 + 14, labels[i], 9, 400, SUB, "middle")
    return s


def toplist(x, y, w, h, title, items, tone=A):
    s = card(x, y, w, h) + T(x + 14, y + 22, title, 12, 700)
    mx = max(v for _, v in items) or 1
    for i, (nm, v) in enumerate(items):
        yy = y + 42 + i * ((h - 52) / max(1, len(items)))
        s += T(x + 14, yy + 9, nm, 10.5, 500, TXT, maxw=w - 58) + T(x + w - 14, yy + 9, f"{v:,}" if isinstance(v, int) else v, 10.5, 700, MUT, "end")
        s += R(x + 14, yy + 15, w - 28, 5, 2.5, A, .1) + R(x + 14, yy + 15, (w - 28) * (v if isinstance(v, (int, float)) else 50) / mx, 5, 2.5, tone, .75)
    return s


# ------------------------------------------------------------------ screens
def dash(sp):
    s = sidebar(sp["nav"], sp.get("active", 0)) + header(130, 62, sp["title"], sp.get("sub"), sp.get("range", "Last 30 days"))
    ks = sp["kpis"]; kw = (496 - 12 * (len(ks) - 1)) / len(ks)
    for i, (lb, v, d, *t) in enumerate(ks): s += kpi(130 + i * (kw + 12), 80, kw, lb, v, d, t[0] if t else "ok")
    ch = sp["chart"]
    if ch.get("kind") == "bars":
        s += bars(130, 154, 304, 230, ch["title"], ch["vals"], ch["labels"], fmt=ch.get("fmt"))
    else:
        s += chart(130, 154, 304, 230, ch["title"], ch["vals"], ch["labels"], ch.get("unit", ""), ch.get("fmt"), second=ch.get("second"))
    s += toplist(446, 154, 180, 230, sp["list"]["title"], sp["list"]["items"])
    return s


def table(sp):
    s = sidebar(sp["nav"], sp.get("active", 0)) + header(130, 62, sp["title"], sp.get("sub"))
    # filter chips + search
    cx = 130
    for i, f in enumerate(sp.get("filters", [])):
        ps, w = pill(cx, 82, f, "info" if i == 0 else "muted", 10); s += ps; cx += w + 6
    s += R(480, 80, 146, 22, 11, VOID, 1, A, .2) + T(494, 95, sp.get("search", "Search"), 10, 400, SUB)
    cols = sp["cols"]; tot = sum(c[1] for c in cols); x0, wtot = 130, 496
    s += card(x0, 112, wtot, 272) + R(x0, 112, wtot, 28, 10, A, .12) + R(x0, 128, wtot, 12, 0, A, .12)
    cxs, acc = [], x0 + 12
    for nm, wt, *al in cols: cxs.append(acc); acc += (wtot - 24) * wt / tot
    for i, (nm, wt, *al) in enumerate(cols):
        right = bool(al and al[0] == "r")
        s += T((cxs[i] + (wtot - 24) * wt / tot - 8) if right else cxs[i], 130, nm, 9.5, 700, MUT, "end" if right else "start")
    rows = sp["rows"]; rh = min(30, 240 / len(rows))
    for r, row in enumerate(rows):
        y = 140 + r * rh
        if r % 2: s += R(x0 + 4, y + 1, wtot - 8, rh - 2, 5, A, .05)
        for i, (nm, wt, *al) in enumerate(cols):
            v = row[i]; cw = (wtot - 24) * wt / tot
            if isinstance(v, tuple):  # (label, tone) status pill
                s += pill_s(cxs[i], y + rh / 2 - 8, v[0], v[1], 9.5)
            else:
                right = bool(al and al[0] == "r"); strong = i == 0
                s += T((cxs[i] + cw - 8) if right else cxs[i], y + rh / 2 + 3.5, v, 10.5, 600 if strong else 400, TXT if strong else MUT, "end" if right else "start", maxw=cw - 10)
    return s


def chat(sp):
    s = R(0, 34, 190, 366, 0, PAN, 1) + line(190, 34, 190, 400, .12) + T(14, 60, sp["inbox"], 12, 700)
    for i, (nm, pv, tm) in enumerate(sp["threads"]):
        y = 72 + i * 56
        s += (R(8, y, 174, 50, 8, A, .14) if i == sp.get("active", 1) else "") + avatar(28, y + 25, 12, nm[0]) + T(48, y + 20, nm, 11, 700, maxw=100) + T(176, y + 20, tm, 9, 400, SUB, "end") + T(48, y + 35, pv, 9.5, 400, MUT, maxw=124)
    s += T(210, 60, sp["subject"], 14, 700, maxw=300) + pill_s(626, 46, sp.get("badge", "Open"), "info", 10, "end") + line(200, 72, 626, 72, .12)
    y = 86
    for who, lines in sp["messages"]:
        h = 18 + 15 * len(lines)
        s += avatar(222, y + 12, 11, who[0]) + R(240, y, 330, h, 10, PAN, 1, A, .14)
        for k, ln in enumerate(lines): s += T(252, y + 20 + k * 15, ln, 10.5, 400, TXT, maxw=308)
        y += h + 12
    ch_h = 52 + len(sp["reply"]) * 15 + 4 + 22 + 40
    s += R(210, y, 416, ch_h, 12, A, .08, A, .45, 1.5)
    s += pill_s(224, y + 12, "Suggested reply", "info", 9.5) + T(618, y + 24, "2 sources used", 9.5, 600, MUT, "end")
    for k, ln in enumerate(sp["reply"]): s += T(224, y + 52 + k * 15, ln, 10.5, 400, TXT, maxw=392)
    cy = y + 52 + len(sp["reply"]) * 15 + 4
    for k, c in enumerate(sp["cites"]):
        ps, w = pill(224 + sum(int(len(sp["cites"][j]) * 5.6 + 22) for j in range(k)), cy, c, "muted", 9); s += ps
    by = y + ch_h - 10
    s += R(448, by - 22, 80, 24, 12, VOID, 1, A, .3) + T(488, by - 6, "Edit", 10.5, 700, A, "middle") + R(536, by - 22, 80, 24, 12, A, .95) + T(576, by - 6, "Send", 10.5, 700, BG, "middle")
    return s


def map_(sp):
    s = R(0, 34, 640, 366, 0, PAN, 1)
    # city blocks, river, roads
    for bx in range(0, 640, 64):
        for by in range(40, 400, 58):
            if (bx // 64 + by // 58) % 3: s += R(bx + 6, by + 6, 52, 46, 6, A, .05 + ((bx + by) % 5) * .01)
    s += f'<path d="M-10 330 C 120 290, 220 360, 330 320 S 560 300, 650 340" fill="none" stroke="{A}" stroke-opacity=".18" stroke-width="22" stroke-linecap="round"/>'
    for y in (96, 212, 300): s += line(0, y, 640, y + 8, .18, 3, col=MUT)
    for x in (150, 330, 520): s += line(x, 34, x + 12, 400, .18, 3, col=MUT)
    pts = sp.get("route") or []
    if pts: s += f'<path d="M{" L".join(f"{a} {b}" for a, b in pts)}" fill="none" stroke="{A}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" stroke-opacity=".85"/>'
    for i, (a, b, lb, tone) in enumerate(sp["pins"]):
        c = TONES[tone]
        s += f'<circle cx="{a}" cy="{b}" r="11" fill="{c}"/><circle cx="{a}" cy="{b}" r="17" fill="{c}" fill-opacity=".2"/>' + T(a, b + 4, lb, 10.5, 700, BG, "middle")
    for a, b, nm in sp.get("vehicles", []):
        s += R(a - 4, b - 15, 62, 20, 10, TXT, .92) + f'<circle cx="{a + 8}" cy="{b - 5}" r="4" fill="{OK}"/>' + T(a + 17, b - 2, nm, 9.5, 700, BG)
    px, py, pw = 16, 48, 190
    s += card(px, py, pw, 38 + len(sp["jobs"]) * 38 + 10) + T(px + 12, py + 22, sp["panel"], 12, 700)
    for i, (jid, st, eta, tone) in enumerate(sp["jobs"]):
        y = py + 36 + i * 38
        s += f'<circle cx="{px + 16}" cy="{y + 12}" r="4.5" fill="{TONES[tone]}"/>' + T(px + 28, y + 12, jid, 10.5, 700, maxw=90) + (T(px + pw - 12, y + 12, eta, 10, 700, MUT, "end") if eta else "") + T(px + 28, y + 26, st, 9.5, 400, MUT, maxw=150)
    return s


def cal_rows(sp):
    """Leave calendar: one row per person, events span several day columns. events = (row, first_day, span, (label, sub), tone)."""
    s = sidebar(sp["nav"], sp.get("active", 0)) + header(130, 62, sp["title"], sp.get("sub"), sp.get("range", "Week view"))
    days = sp["days"]; x0 = 224; gw = (626 - x0) / len(days); rows = sp["hours"]; rh = 258 / len(rows)
    for i, (d, n) in enumerate(days):
        s += T(x0 + i * gw + gw / 2, 96, d, 10.5, 700, MUT, "middle") + T(x0 + i * gw + gw / 2, 112, n, 12, 700, A if i == sp.get("today", 0) else TXT, "middle")
    for j, nm in enumerate(rows):
        y = 124 + j * rh
        s += line(138, y, 626, y, .1) + avatar(152, y + rh / 2, 10, nm[0]) + T(168, y + rh / 2 + 4, nm, 10.5, 600, TXT, maxw=54)
    for i in range(len(days) + 1): s += line(x0 + i * gw, 118, x0 + i * gw, 382, .08)
    for r, d0, span, label, tone in sp["events"]:
        x, y, w, h = x0 + d0 * gw + 3, 124 + r * rh + 4, span * gw - 6, rh - 8
        c = TONES[tone]
        s += R(x, y, w, h, 7, c, .18) + R(x, y, 3, h, 1.5, c, 1) + T(x + 10, y + h / 2 + 4, label[0], 10, 700, TXT, maxw=w - 14)
    return s


def cal(sp):
    if sp.get("mode") == "rows": return cal_rows(sp)
    s = sidebar(sp["nav"], sp.get("active", 0)) + header(130, 62, sp["title"], sp.get("sub"), sp.get("range", "Week view"))
    days = sp["days"]; x0, gw = 168, (626 - 168) / len(days)
    for i, (d, n) in enumerate(days):
        s += T(x0 + i * gw + gw / 2, 96, d, 10.5, 700, MUT, "middle") + T(x0 + i * gw + gw / 2, 112, n, 12, 700, A if i == sp.get("today", 0) else TXT, "middle")
    hours = sp["hours"]; hh = 258 / len(hours)
    for j, hr in enumerate(hours):
        y = 124 + j * hh
        s += line(x0 - 6, y, 626, y, .1) + T(160, y + 4, hr, 9, 400, SUB, "end")
    for i in range(len(days) + 1): s += line(x0 + i * gw, 118, x0 + i * gw, 384, .08)
    for d, start, ln, label, tone in sp["events"]:
        x, y, w, h = x0 + d * gw + 3, 124 + start * hh + 2, gw - 6, ln * hh - 4
        c = TONES[tone]
        s += R(x, y, w, h, 6, c, .16) + R(x, y, 3, h, 1.5, c, 1) + T(x + 9, y + 14, label[0], 9.5, 700, TXT, maxw=w - 14)
        if h > 30: s += T(x + 9, y + 27, label[1], 9, 400, MUT, maxw=w - 14)
    return s


def cards(sp):
    v = sp.get("variant", "plans")
    s = sidebar(sp["nav"], sp.get("active", 0)) + header(130, 62, sp["title"], sp.get("sub"), sp.get("right")) if sp.get("nav") else header(24, 64, sp["title"], sp.get("sub"), sp.get("right"))
    x0 = 130 if sp.get("nav") else 24; wtot = 496 if sp.get("nav") else 592
    if v == "phone":
        s = R(0, 34, 640, 366, 0, PAN, 1) + T(30, 66, sp["title"], 16, 700) + T(30, 84, sp.get("sub", ""), 10.5, 400, MUT)
        px, py, pw, ph = 40, 100, 220, 290
        s += R(px, py, pw, ph, 26, VOID, 1, A, .35, 2) + R(px + 80, py + 8, 60, 6, 3, A, .25)
        s += T(px + 16, py + 38, sp["phone_title"], 13, 700) + T(px + 16, py + 54, sp["phone_sub"], 9.5, 400, MUT)
        for i, (nm, ds, pr) in enumerate(sp["items"]):
            y = py + 66 + i * 54
            s += R(px + 12, y, pw - 24, 48, 10, PAN, 1, A, .12) + R(px + 20, y + 8, 32, 32, 8, A, .2 + .05 * i) + T(px + 60, y + 20, nm, 10.5, 700, maxw=100) + T(px + 60, y + 34, ds, 9, 400, MUT, maxw=100)
            s += T(px + pw - 20, y + 20, pr, 10.5, 700, TXT, "end") + R(px + pw - 54, y + 26, 34, 16, 8, A, .95) + T(px + pw - 37, y + 37.5, "Add", 9, 700, BG, "middle")
        # modifiers panel
        mx = 290
        s += card(mx, 100, 336, 290) + T(mx + 16, 126, sp["mod_title"], 13, 700) + T(mx + 16, 142, sp["mod_sub"], 10, 400, MUT)
        for g, (gt, opts) in enumerate(sp["mods"]):
            y = 160 + g * 64
            s += T(mx + 16, y, gt, 10.5, 700, MUT)
            cx = mx + 16
            for k, (o, sel) in enumerate(opts):
                ps, w = pill(cx, y + 8, o, "info" if sel else "muted", 10); s += ps; cx += w + 6
        s += R(mx + 16, 346, 304, 32, 16, A, .95) + T(mx + 168, 366, sp["cta"], 11.5, 700, BG, "middle")
        return s
    cs = sp["cards"]; n = len(cs); gw = (wtot - 14 * (n - 1)) / n
    for i, c in enumerate(cs):
        x = x0 + i * (gw + 14); hot = c.get("hot")
        s += R(x, 96, gw, 288, 12, VOID, 1, A, .55 if hot else .18, 1.8 if hot else 1)
        if hot: s += pill_s(x + gw - 10, 106, "Most popular", "info", 9, "end")
        if v == "plans":
            s += T(x + 14, 128, c["name"], 12.5, 700, maxw=gw - 28) + T(x + 14, 160, c["price"], 22, 700) + T(x + 14, 176, c.get("per", ""), 9.5, 400, MUT)
            for k, b in enumerate(c["bullets"]):
                s += f'<circle cx="{x + 20}" cy="{200 + k * 24}" r="6" fill="{OK}" fill-opacity=".18"/><path d="M{x + 17} {200 + k * 24} l2.2 2.4 l4 -4.6" fill="none" stroke="{OK}" stroke-width="1.6" stroke-linecap="round"/>' + T(x + 32, 204 + k * 24, b, 10.5, 400, TXT, maxw=gw - 44)
            s += R(x + 14, 346, gw - 28, 28, 14, A if hot else VOID, .95 if hot else 1, A, .4) + T(x + gw / 2, 364, c.get("cta", "Choose plan"), 11, 700, BG if hot else A, "middle")
        else:  # product / listing grid
            s += R(x + 8, 104, gw - 16, 120, 8, A, .12 + .05 * i) + T(x + 14, 122, c.get("tag", ""), 9, 700, A) if c.get("tag") else R(x + 8, 104, gw - 16, 120, 8, A, .12 + .05 * i)
            s += f'<path d="M{x + 8} 224 L{x + 8 + (gw - 16) * .35} 170 L{x + 8 + (gw - 16) * .6} 205 L{x + 8 + (gw - 16) * .8} 160 L{x + gw - 8} 224 Z" fill="{A}" fill-opacity=".14"/>'
            s += T(x + 14, 246, c["name"], 11.5, 700, maxw=gw - 28) + T(x + 14, 262, c["meta"], 9.5, 400, MUT, maxw=gw - 28) + T(x + 14, 292, c["price"], 14, 700) + T(x + gw - 14, 292, c.get("badge", ""), 9.5, 700, OK, "end")
            for k, b in enumerate(c.get("bullets", [])[:3]): s += T(x + 14, 312 + k * 16, b, 9.5, 400, MUT, maxw=gw - 28)
    return s


def player(sp):
    s = R(0, 34, 640, 366, 0, PAN, 1)
    s += R(24, 52, 150, 150, 16, A, .18) + f'<circle cx="99" cy="127" r="44" fill="{A}" fill-opacity=".25"/><circle cx="82" cy="118" r="14" fill="{A}" fill-opacity=".55"/><circle cx="116" cy="118" r="14" fill="{A}" fill-opacity=".4"/>'
    s += T(24, 226, sp["title"], 14, 700, maxw=250) + T(24, 244, sp["sub"], 10.5, 400, MUT, maxw=250)
    s += pill_s(24, 254, sp["hosts"][0], "info", 9.5) + pill_s(24 + int(len(sp["hosts"][0]) * 5.6 + 20), 254, sp["hosts"][1], "muted", 9.5)
    # waveform
    for i in range(46):
        h = 10 + (abs(math.sin(i * 1.7) * 26) + abs(math.cos(i * .6) * 14))
        s += R(24 + i * 5.4, 306 - h / 2, 3.2, h, 1.6, A, .85 if i < 19 else .28)
    s += R(24, 330, 250, 5, 2.5, A, .15) + R(24, 330, 104, 5, 2.5, A, .9) + T(24, 352, sp["time"][0], 9, 400, SUB) + T(274, 352, sp["time"][1], 9, 400, SUB, "end")
    s += f'<circle cx="149" cy="372" r="14" fill="{A}"/><path d="M144.5 366 L156 372 L144.5 378Z" fill="{BG}"/>'
    # transcript
    s += card(300, 52, 326, 332) + T(316, 78, "Transcript", 12.5, 700) + pill_s(626 - 16, 62, sp["status"], "ok", 9.5, "end")
    y = 94
    for i, (who, txt, cur) in enumerate(sp["lines"]):
        h = 18 + 14 * len(txt)
        if cur: s += R(308, y - 4, 310, h + 2, 8, A, .13)
        s += T(316, y + 10, who, 9.5, 700, A if who == sp["hosts"][0] else MUT)
        for k, ln in enumerate(txt): s += T(316, y + 25 + k * 14, ln, 10.5, 500 if cur else 400, TXT, maxw=296)
        y += h + 10
    return s


def kanban(sp):
    s = R(0, 34, 640, 366, 0, PAN, 1) + T(24, 62, sp["title"], 16, 700) + T(24, 80, sp.get("sub", ""), 10.5, 400, MUT)
    cols = sp["cols"]; n = len(cols); gw = (592 - 12 * (n - 1)) / n
    for i, (nm, cnt, items) in enumerate(cols):
        x = 24 + i * (gw + 12)
        ch = min(292, 46 + max(len(c[2]) for c in cols) * 62 + 8)
        s += R(x, 94, gw, ch, 12, VOID, 1, A, .16) + T(x + 12, 116, nm, 11.5, 700) + pill_s(x + gw - 10, 102, str(cnt), "muted", 9.5, "end")
        for k, it in enumerate(items):
            y = 128 + k * 62
            s += R(x + 8, y, gw - 16, 56, 8, PAN, 1, A, .14) + T(x + 16, y + 18, it[0], 10.5, 700, maxw=gw - 34) + T(x + 16, y + 33, it[1], 9.5, 400, MUT, maxw=gw - 34)
            if len(it) > 2: s += pill_s(x + 16, y + 38, it[2][0], it[2][1], 8.5)
    return s


def doc(sp):
    d = sp["doc"]; has_side = bool(sp.get("fields")); dw = 330 if has_side else 592
    s = R(0, 34, 640, 366, 0, PAN, 1)
    dx = 24
    s += R(dx + 3, 51, dw, 336, 10, A, .06) + R(dx, 48, dw, 336, 10, VOID, 1, A, .2)
    s += R(dx + 16, 64, 26, 26, 7, A, .9) + T(dx + 52, 76, d["from"], 12, 700, maxw=150) + T(dx + 52, 90, d.get("from_sub", ""), 9, 400, MUT, maxw=150)
    s += T(dx + dw - 16, 78, d["title"], 15, 700, A, "end") + T(dx + dw - 16, 94, d["number"], 10.5, 600, MUT, "end")
    s += T(dx + 16, 122, "Billed to", 9, 700, SUB) + T(dx + 16, 137, d["to"], 11, 600, maxw=150) + T(dx + 16, 151, d.get("to_sub", ""), 9.5, 400, MUT, maxw=150)
    s += T(dx + dw - 16, 122, "Date", 9, 700, SUB, "end") + T(dx + dw - 16, 137, d["date"], 11, 600, TXT, "end") + T(dx + dw - 16, 151, d.get("due", ""), 9.5, 400, MUT, "end")
    ty = 170
    s += R(dx + 12, ty, dw - 24, 22, 6, A, .12)
    cols = d["cols"]; cw = [0.52, 0.14, 0.17, 0.17] if len(cols) == 4 else [0.6, 0.2, 0.2]
    xs = [dx + 22 + (dw - 44) * sum(cw[:i]) for i in range(len(cols))]
    for i, c in enumerate(cols): s += T(xs[i] if i == 0 else xs[i] + (dw - 44) * cw[i], ty + 15, c, 9.5, 700, MUT, "start" if i == 0 else "end")
    rh = min(24, (372 - (ty + 36) - len(d["totals"]) * 20) / len(d["rows"]))
    for r, row in enumerate(d["rows"]):
        y = ty + 28 + r * rh
        s += line(dx + 14, y + rh - 3, dx + dw - 14, y + rh - 3, .08)
        for i, v in enumerate(row): s += T(xs[i] if i == 0 else xs[i] + (dw - 44) * cw[i], y + 12, v, 10.5, 500 if i == 0 else 400, TXT if i == 0 else MUT, "start" if i == 0 else "end", maxw=(dw - 44) * cw[i] - 6)
    ty2 = ty + 36 + len(d["rows"]) * rh
    for k, (lb, v, strong) in enumerate(d["totals"]):
        y = ty2 + k * 20
        s += T(dx + dw - 120, y + 12, lb, 10.5, 700 if strong else 400, TXT if strong else MUT, "end") + T(dx + dw - 16, y + 12, v, 11 if strong else 10.5, 700 if strong else 500, TXT, "end")
    # highlight boxes (extraction view)
    marks = sp.get("marks", [])
    boxes = {"vendor": (dx + 48, 63, 160, 32), "number": (dx + dw - 140, 82, 128, 17), "date": (dx + dw - 120, 125, 106, 17), "total": (dx + dw - 190, ty2 + (len(d['totals']) - 1) * 20 - 1, 178, 20)}
    for m in marks:
        bx, by, bw, bh = boxes[m]
        s += R(bx, by, bw, bh, 5, A, .12, A, .8, 1.5)
    if has_side:
        sx = 372; sw = 254
        s += card(sx, 48, sw, 336) + T(sx + 14, 72, "Extracted fields", 12.5, 700) + pill_s(sx + sw - 12, 56, sp.get("side_badge", "JSON"), "muted", 9.5, "end")
        for i, (nm, val, conf) in enumerate(sp["fields"]):
            y = 88 + i * 36
            low = conf < 85
            s += T(sx + 14, y + 10, nm, 9.5, 600, SUB) + T(sx + 14, y + 25, val, 11, 700, TXT, maxw=140)
            s += R(sx + sw - 92, y + 8, 78, 5, 2.5, A, .12) + R(sx + sw - 92, y + 8, 78 * conf / 100, 5, 2.5, WARN if low else OK, .9) + T(sx + sw - 14, y + 27, f"{conf}%", 9.5, 700, WARN if low else MUT, "end")
            if low: s += pill_s(sx + sw - 14, y - 4, "Review", "warn", 8.5, "end")
    return s


def video(sp):
    s = R(0, 34, 640, 366, 0, PAN, 1)
    s += R(20, 48, 400, 290, 14, A, .16) + f'<circle cx="220" cy="170" r="52" fill="{A}" fill-opacity=".22"/><circle cx="220" cy="152" r="22" fill="{A}" fill-opacity=".45"/><path d="M178 214 Q220 170 262 214 L262 230 L178 230Z" fill="{A}" fill-opacity=".4"/>'
    s += R(32, 60, 132, 22, 11, TXT, .85) + T(98, 75, sp["who"], 10, 700, BG, "middle") + pill_s(408, 58, sp["timer"], "ok", 9.5, "end")
    s += R(306, 252, 104, 78, 10, VOID, 1, A, .3) + f'<circle cx="358" cy="282" r="14" fill="{A}" fill-opacity=".4"/><path d="M336 316 Q358 290 380 316Z" fill="{A}" fill-opacity=".3"/>' + T(358, 324, "You", 9, 600, MUT, "middle")
    for i, (lb, bad) in enumerate([("Mic", 0), ("Cam", 0), ("Share", 0), ("Chat", 0)]):
        s += f'<circle cx="{100 + i * 46}" cy="318" r="15" fill="{VOID}" stroke="{A}" stroke-opacity=".3"/>' + T(100 + i * 46, 321, lb[0], 10, 700, MUT, "middle")
    s += f'<rect x="20" y="346" width="400" height="38" rx="12" fill="{VOID}" stroke="{A}" stroke-opacity=".18"/>' + T(34, 369, sp["strip"], 10.5, 500, MUT, maxw=370)
    s += R(430, 48, 196, 336, 14, VOID, 1, A, .18) + T(446, 72, "Visit details", 12.5, 700)
    for i, (k, v) in enumerate(sp["details"]):
        y = 90 + i * 30; s += T(446, y + 9, k, 9, 600, SUB) + T(446, y + 23, v, 10.5, 600, TXT, maxw=164)
    ny = 90 + len(sp["details"]) * 30 + 6
    s += T(446, ny + 10, "Notes", 10.5, 700) + R(442, ny + 18, 172, 384 - ny - 52, 8, PAN, 1, A, .12)
    for k, ln in enumerate(sp["notes"]): s += T(452, ny + 36 + k * 15, ln, 9.5, 400, MUT, maxw=156)
    s += R(442, 352, 172, 24, 12, A, .95) + T(528, 368, "Save note", 10.5, 700, BG, "middle")
    return s


def flow(sp):
    s = R(0, 34, 640, 366, 0, PAN, 1) + T(24, 62, sp["title"], 16, 700) + T(24, 80, sp.get("sub", ""), 10.5, 400, MUT)
    nodes = sp["nodes"]; pos = [(24, 100), (228, 100), (432, 100), (432, 250), (228, 250), (24, 250)]
    w, h = 184, 112
    arrows = [(208, 156, 228, 156), (412, 156, 432, 156), (524, 212, 524, 250), (432, 306, 412, 306), (228, 306, 208, 306)]
    for (x1, y1, x2, y2) in arrows:
        s += line(x1, y1, x2, y2, .75, 2.5) + f'<circle cx="{x2}" cy="{y2}" r="4" fill="{A}"/>'
    for i, ((x, y), n) in enumerate(zip(pos, nodes)):
        s += card(x, y, w, h, 12) + f'<circle cx="{x + 18}" cy="{y + 20}" r="9" fill="{A}" fill-opacity=".9"/>' + T(x + 18, y + 24, str(i + 1), 10, 700, BG, "middle")
        s += T(x + 34, y + 24, n[0], 11.5, 700, maxw=w - 44) + T(x + 14, y + 46, n[1], 9.5, 400, MUT, maxw=w - 28)
        if len(n) > 2: s += pill_s(x + 14, y + h - 28, n[2][0], n[2][1], 9)
        if len(n) > 3: s += T(x + w - 14, y + h - 12, n[3], 9.5, 700, MUT, "end")
    return s


KINDS = dict(dash=dash, table=table, chat=chat, map=map_, cal=cal, cards=cards, player=player, kanban=kanban, doc=doc, video=video, flow=flow)


def render(kind, spec, caption, url):
    return frame(KINDS[kind](spec), caption, url)
