"""Colourful illustrated banners for the portfolio cards (inline SVG, 480x300, drawn with preserveAspectRatio="slice").

Each project gets its own palette and a small scene that hints at what the product does: layered white cards, glass chips,
sparkles and soft shadows on a vivid gradient. Scenes are drawn in a 480x300 space and shifted/scaled by 0.88 so the card tag in the top-left corner never covers them; keep the key shapes inside x 70..410, y 50..250. In the black-and-white theme CSS turns the banners monochrome.
banner(slug) -> '<svg ...>...</svg>'
"""
import html, math

W, H = 480, 300
INK = "#111B3A"
INK2 = "#4B5677"
WHITE = "#FFFFFF"


def e(s): return html.escape(str(s), quote=False)


class B:
    """One banner: collects defs and shapes, ids are prefixed so many banners can live on one page."""
    def __init__(self, slug, c1, c2, c3):
        self.p, self.c1, self.c2, self.c3 = slug, c1, c2, c3
        self.parts = []

    def add(self, s): self.parts.append(s); return self

    # ---- primitives
    def blob(self, cx, cy, r, fill=WHITE, op=.12): return self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" fill-opacity="{op}"/>')

    def card(self, x, y, w, h, r=16, fill=WHITE, op=.97, rot=0, shadow=True, stroke=None):
        tr = f' transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else ""
        sh = f' filter="url(#sh{self.p})"' if shadow else ""
        st = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
        return self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" fill-opacity="{op}"{sh}{tr}{st}/>')

    def rect(self, x, y, w, h, r=4, fill=INK, op=1): return self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" fill-opacity="{op}"/>')

    def bar(self, x, y, w, h=6, fill=INK, op=.18): return self.rect(x, y, w, h, h / 2, fill, op)

    def circle(self, cx, cy, r, fill=INK, op=1, stroke=None, sw=2):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        return self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" fill-opacity="{op}"{st}/>')

    def path(self, d, fill="none", stroke=None, sw=2, op=1, cap="round", dash=None, fo=None):
        st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="round" stroke-opacity="{op}"' if stroke else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        fop = f' fill-opacity="{fo}"' if fo is not None else ""
        return self.add(f'<path d="{d}" fill="{fill}"{fop}{st}{da}/>')

    def text(self, x, y, s, size=12, weight=700, fill=INK, anchor="start", op=1):
        return self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" fill-opacity="{op}" text-anchor="{anchor}">{e(s)}</text>')

    def chip(self, x, y, label, fill=WHITE, tc=INK, size=12, op=.95, dot=None):
        w = int(len(label) * size * .6 + (30 if dot else 20))
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{size + 12}" rx="{(size + 12) / 2}" fill="{fill}" fill-opacity="{op}" filter="url(#sh{self.p})"/>')
        if dot: self.circle(x + 12, y + (size + 12) / 2, 4, dot)
        self.text(x + (22 if dot else 10), y + size + 2, label, size, 700, tc)
        return w

    def sparkle(self, cx, cy, r=8, fill=WHITE, op=.95):
        d = f"M{cx} {cy - r} Q{cx} {cy} {cx + r} {cy} Q{cx} {cy} {cx} {cy + r} Q{cx} {cy} {cx - r} {cy} Q{cx} {cy} {cx} {cy - r}Z"
        return self.path(d, fill, op=1, fo=op)

    def person(self, cx, cy, s=1.0, fill=INK, op=.9):
        self.circle(cx, cy - 10 * s, 9 * s, fill, op)
        return self.path(f"M{cx - 16 * s} {cy + 22 * s} Q{cx - 16 * s} {cy + 2 * s} {cx} {cy + 2 * s} Q{cx + 16 * s} {cy + 2 * s} {cx + 16 * s} {cy + 22 * s}Z", fill, fo=op)

    def check(self, cx, cy, r=11, fill="#16A34A"):
        self.circle(cx, cy, r, fill)
        return self.path(f"M{cx - r * .4} {cy} L{cx - r * .08} {cy + r * .34} L{cx + r * .46} {cy - r * .3}", stroke=WHITE, sw=2.4)

    # ---- output
    def svg(self):
        p = self.p
        defs = (f'<defs><linearGradient id="g{p}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{self.c1}"/><stop offset=".55" stop-color="{self.c2}"/><stop offset="1" stop-color="{self.c3}"/></linearGradient>'
                f'<radialGradient id="r{p}" cx=".25" cy=".2" r=".8"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
                f'<linearGradient id="a{p}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{self.c1}"/><stop offset="1" stop-color="{self.c3}"/></linearGradient>'
                f'<pattern id="d{p}" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="#fff" fill-opacity=".35"/></pattern>'
                f'<filter id="sh{p}" x="-25%" y="-25%" width="150%" height="170%"><feDropShadow dx="0" dy="7" stdDeviation="8" flood-color="#0B1030" flood-opacity=".28"/></filter></defs>')
        bg = (f'<rect width="{W}" height="{H}" fill="url(#g{p})"/><rect width="{W}" height="{H}" fill="url(#r{p})"/>'
              f'<circle cx="420" cy="30" r="130" fill="#fff" fill-opacity=".10"/><circle cx="30" cy="290" r="120" fill="#fff" fill-opacity=".10"/>'
              f'<rect x="300" y="190" width="180" height="110" fill="url(#d{p})"/>'
              f'<path d="M-20 230 C 90 190, 200 260, 330 215 S 470 200 520 220 L520 320 L-20 320Z" fill="#fff" fill-opacity=".07"/>')
        return (f'<svg class="pf-banner__svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">'
                + defs + bg + '<g transform="translate(34 26) scale(.88)">' + "".join(self.parts) + "</g></svg>")


# ====================================================================== scenes
def podagain(b):
    b.card(130, 84, 224, 128)
    b.rect(144, 98, 56, 56, 12, f"url(#a{b.p})")
    b.circle(163, 120, 9, WHITE, .95); b.circle(183, 120, 9, WHITE, .75); b.path("M153 138 Q173 154 193 138", stroke=WHITE, sw=3)
    b.bar(212, 104, 112, 9, INK, .85); b.bar(212, 122, 78, 7, INK, .22); b.bar(212, 138, 54, 7, INK, .14)
    for i in range(30):
        h = 8 + abs(math.sin(i * 1.3)) * 22 + abs(math.cos(i * .5)) * 8
        b.rect(144 + i * 6.4, 182 - h / 2, 3.6, h, 1.8, f"url(#a{b.p})" if i < 13 else INK, 1 if i < 13 else .15)
    b.circle(240, 226, 21, WHITE); b.path("M233 215 L250 226 L233 237Z", f"url(#a{b.p})")
    b.chip(76, 76, "2 AI hosts", dot="#A855F7"); b.chip(322, 66, "Transcript", dot="#EC4899")
    b.circle(98, 176, 17, WHITE, .95); b.rect(94, 164, 8, 15, 4, f"url(#a{b.p})"); b.path("M90 175 Q90 186 98 186 Q106 186 106 175", stroke=INK, sw=2); b.bar(94, 188, 8, 3, INK, .6)
    b.sparkle(368, 128, 9); b.sparkle(112, 120, 6); b.sparkle(372, 214, 7, WHITE, .8)


def ai_support(b):
    b.card(84, 66, 176, 62, 18)
    b.circle(106, 90, 11, f"url(#a{b.p})"); b.bar(126, 82, 108, 8, INK, .55); b.bar(126, 98, 78, 7, INK, .2)
    b.add(f'<path d="M110 128 l-14 14 l24 -8z" fill="#fff" fill-opacity=".97"/>')
    b.card(158, 146, 242, 96, 20, stroke=b.c2)
    b.chip(172, 134, "Suggested reply", fill=b.c2, tc=WHITE, size=11)
    b.bar(172, 170, 190, 8, INK, .55); b.bar(172, 186, 150, 8, INK, .3); b.bar(172, 202, 112, 8, INK, .18)
    b.chip(172, 218, "Refund policy §3", fill="#EEF2FF", tc="#3730A3", size=10, op=1)
    b.sparkle(376, 168, 12, b.c3); b.sparkle(362, 196, 6, b.c2)
    b.chip(316, 64, "Cited sources", dot="#22D3EE"); b.sparkle(96, 176, 7); b.sparkle(124, 220, 5, WHITE, .8)


def booking(b):
    b.card(138, 62, 204, 170, 20)
    b.rect(138, 62, 204, 40, 20, f"url(#a{b.p})"); b.rect(138, 82, 204, 20, 0, f"url(#a{b.p})")
    b.text(156, 88, "March", 15, 800, WHITE); b.circle(324, 82, 5, WHITE, .9); b.circle(306, 82, 5, WHITE, .5)
    for r in range(4):
        for c in range(7):
            x, y = 152 + c * 26.5, 112 + r * 27
            sel = (r, c) in ((1, 3), (2, 5))
            hot = (r, c) in ((0, 4), (1, 1), (2, 2), (3, 0), (3, 4))
            if sel: b.circle(x + 8, y + 8, 12, b.c1)
            elif hot: b.circle(x + 8, y + 8, 12, b.c3, .55)
            b.text(x + 8, y + 12, str(r * 7 + c + 1), 10.5, 700, WHITE if sel else INK, "middle", .9 if sel else .65)
    b.check(340, 72, 15)
    b.chip(84, 206, "Booked", dot="#16A34A"); b.chip(332, 214, "$79 / mo", dot="#10B981")
    b.sparkle(104, 108, 8); b.sparkle(386, 150, 7)


def logistics(b):
    b.card(106, 68, 270, 158, 20)
    for i in range(5):
        for j in range(3):
            b.rect(122 + i * 50, 82 + j * 42, 38, 30, 6, b.c3, .35 + ((i + j) % 3) * .1)
    b.path("M96 196 C 160 176, 210 214, 290 168 S 360 122 392 140", stroke=b.c2, sw=14, op=.22)
    b.path("M132 204 C 178 150, 230 190, 262 142 S 330 100, 358 96", stroke="#EA580C", sw=5, dash="2 9")
    b.circle(132, 204, 10, WHITE, 1, "#EA580C", 4); b.circle(358, 96, 12, "#EA580C"); b.circle(358, 96, 5, WHITE)
    b.add(f'<g filter="url(#sh{b.p})"><rect x="200" y="128" width="46" height="28" rx="5" fill="#fff"/><path d="M246 136 h14 l10 11 v9 h-24z" fill="#EA580C"/><rect x="204" y="133" width="22" height="6" rx="3" fill="#EA580C" fill-opacity=".35"/></g>')
    b.circle(214, 158, 7, "#111B3A"); b.circle(214, 158, 3, WHITE); b.circle(258, 158, 7, "#111B3A"); b.circle(258, 158, 3, WHITE)
    b.chip(298, 58, "ETA 12 min", dot="#EA580C"); b.chip(84, 74, "Live", dot="#16A34A")
    b.sparkle(386, 224, 8); b.sparkle(98, 236, 6)


def restaurant(b):
    for k in range(3): b.path(f"M{180 + k * 26} 118 q-10 -14 0 -28 q10 -14 0 -28", stroke=WHITE, sw=4, op=.65)
    b.add(f'<path d="M104 150 L276 150 Q276 236 190 236 Q104 236 104 150Z" fill="#fff" fill-opacity=".97" filter="url(#sh{b.p})"/>')
    b.add(f'<ellipse cx="190" cy="150" rx="86" ry="14" fill="{b.c3}" fill-opacity=".9"/>')
    for (x, y, r, c) in [(150, 146, 11, "#16A34A"), (176, 140, 12, "#F97316"), (204, 146, 10, "#FDE047"), (228, 142, 11, "#16A34A"), (190, 152, 9, "#FFFFFF")]:
        b.circle(x, y, r, c, .95)
    b.path("M120 176 Q190 204 262 176", stroke=b.c1, sw=5, op=.35)
    b.card(296, 70, 104, 148, 14)
    b.text(310, 96, "#112", 14, 800, INK); b.bar(310, 108, 76, 6, INK, .2)
    for i in range(3): b.circle(316, 130 + i * 20, 4, b.c2); b.bar(328, 127 + i * 20, 56 - i * 10, 6, INK, .35)
    b.rect(310, 190, 28, 28, 4, INK, .88)
    for i in range(3):
        for j in range(3):
            if (i + j) % 2 == 0: b.rect(314 + i * 8, 194 + j * 8, 6, 6, 1, WHITE)
    b.chip(84, 74, "Table 12", dot="#F97316"); b.chip(318, 232, "Ready", dot="#16A34A")
    b.sparkle(262, 86, 8); b.sparkle(96, 214, 6)


def property_(b):
    b.circle(366, 84, 24, "#FDE047", .95); b.circle(366, 84, 38, "#FDE047", .25)
    b.rect(70, 226, 340, 8, 4, WHITE, .5)
    b.rect(104, 150, 74, 76, 6, WHITE, .95); b.add(f'<path d="M96 152 L141 112 L186 152Z" fill="{b.c1}" filter="url(#sh{b.p})"/>')
    b.rect(200, 120, 90, 106, 6, WHITE, .97); b.add(f'<path d="M192 122 L245 78 L298 122Z" fill="{b.c2}" filter="url(#sh{b.p})"/>')
    b.rect(310, 164, 70, 62, 6, WHITE, .93); b.add(f'<path d="M302 166 L345 132 L388 166Z" fill="{b.c1}"/>')
    for (x, y) in [(116, 168), (146, 168), (216, 140), (252, 140), (216, 176), (252, 176), (322, 180), (350, 180)]: b.rect(x, y, 20, 20, 4, b.c3, .65)
    b.rect(234, 196, 22, 30, 4, b.c1, .85); b.rect(126, 200, 20, 26, 4, b.c1, .7)
    b.add(f'<path d="M245 36 q-22 0 -22 22 q0 18 22 40 q22 -22 22 -40 q0 -22 -22 -22z" fill="#fff" filter="url(#sh{b.p})"/>')
    b.circle(245, 58, 8, b.c2)
    b.chip(84, 76, "$425k", dot="#16A34A"); b.chip(322, 214, "3 bed", dot="#38BDF8")
    b.sparkle(396, 120, 8); b.sparkle(86, 128, 6)


def telehealth(b):
    b.card(108, 66, 236, 150, 22, fill="#0B3B36", op=.92)
    b.add(f'<rect x="108" y="66" width="236" height="150" rx="22" fill="url(#a{b.p})" fill-opacity=".55"/>')
    b.person(226, 134, 2.2, WHITE, .9)
    b.card(274, 150, 58, 44, 10, shadow=False, op=.95); b.person(303, 176, .9, b.c1, .9)
    for i, col in enumerate(["#FFFFFF", "#FFFFFF", "#EF4444"]): b.circle(196 + i * 34, 200, 11, col, .95)
    b.path("M360 120 L378 120 L386 100 L398 148 L408 110 L416 120 L436 120", stroke=WHITE, sw=3.5, op=.9)
    b.circle(344, 74, 20, WHITE); b.rect(340, 64, 8, 20, 2, b.c1); b.rect(334, 70, 20, 8, 2, b.c1)
    b.chip(84, 64, "Dr. Singh", dot="#16A34A"); b.chip(320, 218, "12:04", dot="#EF4444")
    b.sparkle(96, 176, 8); b.sparkle(392, 188, 7)


def invoicing(b):
    b.card(118, 56, 176, 184, 14)
    b.rect(118, 56, 176, 38, 14, f"url(#a{b.p})"); b.rect(118, 78, 176, 16, 0, f"url(#a{b.p})")
    b.text(132, 82, "INVOICE", 15, 800, WHITE)
    for i in range(4): b.bar(132, 108 + i * 22, 100 - (i % 2) * 24, 7, INK, .22); b.bar(250, 108 + i * 22, 30, 7, INK, .4)
    b.rect(132, 198, 148, 28, 8, b.c3, .55); b.text(142, 217, "Total", 12, 700, INK); b.text(270, 217, "$5,040", 13, 800, INK, "end")
    b.add(f'<g transform="rotate(-14 252 160)"><rect x="206" y="138" width="92" height="40" rx="8" fill="#fff" fill-opacity=".92" stroke="#16A34A" stroke-width="3.5"/><text x="252" y="166" font-size="20" font-weight="800" fill="#16A34A" text-anchor="middle">PAID</text></g>')
    b.card(312, 82, 96, 70, 14)
    for i, h in enumerate([20, 32, 26, 44]): b.rect(324 + i * 20, 138 - h, 12, h, 3, b.c1 if i == 3 else b.c3, 1 if i == 3 else .7)
    for i in range(3): b.add(f'<ellipse cx="360" cy="{226 - i * 10}" rx="26" ry="9" fill="#FACC15" stroke="#CA8A04" stroke-width="2"/>')
    b.chip(316, 56, "+14%", dot="#16A34A", size=11); b.sparkle(96, 120, 8); b.sparkle(392, 190, 6)


def amazon(b):
    b.add(f'<path d="M104 112 L180 90 Q196 86 204 96 L224 130 Q230 142 218 150 L134 180 Q122 184 114 174 L100 142 Q96 126 104 112Z" fill="#fff" fill-opacity=".97" filter="url(#sh{b.p})"/>')
    b.circle(124, 122, 7, b.c1, .9)
    b.text(138, 140, "$18.50", 19, 800, "#1B1F3B"); b.text(138, 160, "$19.90", 12, 700, "#8A92AA"); b.path("M138 156 L178 156", stroke="#8A92AA", sw=1.6)
    b.card(214, 134, 190, 100, 16)
    b.path("M230 160 L262 168 L290 200 L322 192 L350 214 L388 204", stroke=b.c1, sw=4)
    b.path("M230 160 L262 168 L290 200 L322 192 L350 214 L388 204 L388 224 L230 224Z", fill=b.c2, op=0, fo=.12)
    b.path("M230 200 L262 192 L290 184 L322 180 L350 176 L388 168", stroke=INK, sw=2.5, op=.3, dash="4 6")
    b.circle(350, 214, 6, WHITE, 1, b.c1, 3)
    b.chip(300, 74, "Price drop", dot="#EF4444")
    b.circle(86, 214, 22, WHITE, .95); b.circle(82, 210, 9, "none", 1, INK, 3.5); b.path("M89 217 L98 226", stroke=INK, sw=4)
    b.sparkle(396, 108, 9); b.sparkle(120, 80, 6)


def walmart(b):
    b.card(92, 72, 154, 116, 14); b.rect(92, 72, 154, 22, 14, b.c1, .9); b.rect(92, 84, 154, 10, 0, b.c1, .9)
    for i in range(3): b.circle(104 + i * 12, 83, 3, WHITE, .9)
    for i in range(4): b.bar(106, 108 + i * 17, 126 - i * 22, 7, INK, .22)
    b.card(268, 128, 134, 104, 14)
    for r in range(4):
        for c in range(4): b.rect(280 + c * 28, 142 + r * 22, 22, 15, 4, [b.c1, b.c2, b.c3, INK][(r + c) % 4], .75 if (r + c) % 4 != 3 else .16)
    pts = [(170, 214), (214, 232), (150, 244)]
    b.path("M170 188 L170 214 L214 232 L268 200", stroke=WHITE, sw=3, op=.85, dash="3 7")
    b.path("M170 214 L150 244", stroke=WHITE, sw=3, op=.85, dash="3 7")
    for (x, y) in pts: b.circle(x, y, 9, WHITE, 1, b.c2, 4)
    b.circle(170, 188, 6, b.c3)
    b.chip(300, 74, "</> Spiders", dot="#38BDF8"); b.chip(86, 214, "200 OK", dot="#16A34A")
    b.sparkle(260, 62, 8); b.sparkle(396, 246, 6)


def repricer(b):
    b.card(98, 76, 130, 76, 16); b.text(116, 108, "$41.90", 22, 800, INK, op=.45); b.path("M116 102 L184 102", stroke=INK, sw=2, op=.35)
    b.chip(116, 120, "Current", fill="#F3E8FF", tc="#6B21A8", size=11, op=1)
    b.card(172, 160, 138, 80, 16); b.text(190, 194, "$39.99", 24, 800, "#6D28D9"); b.chip(190, 206, "Beat by 1%", fill=b.c1, tc=WHITE, size=11)
    b.path("M214 154 L214 164", stroke=WHITE, sw=3)
    b.circle(250, 118, 17, WHITE); b.path("M243 123 L250 112 L257 123", stroke="#16A34A", sw=3.2);
    b.card(300, 80, 106, 118, 16)
    for i, (v, col) in enumerate([(0.7, b.c1), (0.4, b.c2), (0.85, b.c1)]):
        y = 102 + i * 32; b.bar(314, y, 78, 6, INK, .12); b.bar(314, y, 78 * v, 6, col, 1); b.circle(314 + 78 * v, y + 3, 7, WHITE, 1, col, 3)
    b.chip(326, 58, "-4.6%", dot="#16A34A"); b.sparkle(92, 190, 8); b.sparkle(392, 222, 7); b.sparkle(268, 66, 6)


def extraction(b):
    b.card(110, 60, 156, 182, 14, rot=-4)
    for i in range(6):
        hot = i in (1, 3, 4)
        b.rect(126, 88 + i * 24, 124 - (i % 3) * 20, 12, 4, [b.c1, "#FACC15", "#34D399"][i % 3] if hot else INK, .55 if hot else .14)
    b.add(f'<rect x="100" y="148" width="180" height="26" fill="#fff" fill-opacity=".38"/><rect x="100" y="158" width="180" height="4" fill="#fff" fill-opacity=".95" filter="url(#sh{b.p})"/>')
    b.path("M270 150 L296 150", stroke=WHITE, sw=3.5, op=.9); b.path("M290 142 L298 150 L290 158", stroke=WHITE, sw=3.5, op=.9)
    b.card(298, 100, 112, 120, 14, fill="#0B2233", op=.95)
    for i, (k, v) in enumerate([("vendor", 60), ("date", 48), ("total", 64), ("tax", 40)]):
        y = 124 + i * 22; b.bar(312, y, 28, 6, "#5EEAD3", 1); b.bar(346, y, v * .7, 6, WHITE, .75)
    b.text(312, 116, "{", 13, 800, "#FACC15"); b.text(396, 214, "}", 13, 800, "#FACC15", "end")
    b.chip(84, 64, "98% match", dot="#16A34A"); b.chip(318, 66, "JSON", dot="#38BDF8"); b.sparkle(396, 246, 7); b.sparkle(88, 236, 6)


def county(b):
    gold = "#FBBF24"
    b.add(f'<path d="M122 112 L240 62 L358 112Z" fill="#fff" fill-opacity=".97" filter="url(#sh{b.p})"/>')
    b.circle(240, 96, 9, gold); b.rect(122, 118, 236, 10, 2, WHITE, .95)
    for i in range(6): b.rect(136 + i * 40, 132, 18, 70, 4, WHITE, .93); b.rect(136 + i * 40, 132, 6, 70, 3, b.c3, .35)
    b.rect(112, 204, 256, 12, 3, WHITE, .95); b.rect(98, 218, 284, 12, 3, WHITE, .8)
    b.card(360, 128, 56, 76, 10, rot=6); b.bar(370, 142, 34, 5, INK, .3); b.bar(370, 154, 28, 5, INK, .2); b.circle(388, 184, 10, gold); b.circle(388, 184, 5, "#fff", .7)
    b.add(f'<path d="M88 138 L116 126 L144 138 L144 168 Q144 188 116 200 Q88 188 88 168Z" fill="#fff" fill-opacity=".97" filter="url(#sh{b.p})"/>')
    b.path("M104 160 L113 170 L130 148", stroke="#16A34A", sw=4)
    for i in range(3):
        b.rect(176 + i * 50, 242, 36, 22, 6, WHITE, .95); b.circle(194 + i * 50, 253, 4, b.c2)
        if i < 2: b.path(f"M{212 + i * 50} 253 L{226 + i * 50} 253", stroke=gold, sw=3.5)
    b.chip(84, 66, "Verified", dot="#16A34A"); b.chip(322, 70, "Audit log", dot=gold); b.sparkle(398, 110, 8, gold); b.sparkle(80, 232, 6)


def school(b):
    b.add(f'<rect x="108" y="86" width="222" height="130" rx="14" fill="#7C3F10" fill-opacity=".95" filter="url(#sh{b.p})"/><rect x="118" y="96" width="202" height="110" rx="8" fill="#12343A"/>')
    b.text(218, 168, "A+", 54, 900, "#FDE68A", "middle"); b.path("M138 120 L190 120", stroke=WHITE, sw=3, op=.7); b.path("M138 134 L170 134", stroke=WHITE, sw=3, op=.45)
    b.path("M262 126 q10 -12 20 0 t20 0", stroke=WHITE, sw=3, op=.6)
    b.rect(104, 220, 240, 8, 4, "#7C3F10", .9)
    for i, (c, w) in enumerate([(b.c1, 84), (b.c3, 70), ("#FDE047", 76)]): b.rect(336 - (w - 70) / 2, 214 - i * 20, w, 18, 4, c, .97)
    b.add(f'<path d="M345 150 L395 130 L445 150 L395 170Z" fill="#111B3A" filter="url(#sh{b.p})"/><path d="M365 160 L365 182 Q395 198 425 182 L425 160 L395 172Z" fill="#111B3A" fill-opacity=".9"/><path d="M440 150 L440 176" stroke="#FBBF24" stroke-width="3"/>')
    b.circle(440, 180, 5, "#FBBF24")
    b.chip(84, 66, "Grade 8-B", dot="#16A34A"); b.chip(322, 240, "90.4%", dot="#F43F5E"); b.sparkle(396, 90, 8); b.sparkle(90, 236, 6)


def marketplace(b):
    b.rect(110, 112, 220, 112, 8, WHITE, .97)
    for i in range(8): b.add(f'<path d="M{110 + i * 27.5} 84 h27.5 v22 q-13.75 14 -27.5 0z" fill="{WHITE if i % 2 else b.c1}" fill-opacity="{.97 if i % 2 else 1}" filter="url(#sh{b.p})"/>')
    b.rect(110, 74, 220, 14, 4, b.c1); b.rect(140, 140, 66, 52, 6, b.c3, .55); b.rect(160, 176, 26, 48, 4, b.c1, .85)
    b.rect(226, 140, 80, 84, 6, b.c3, .35); b.bar(236, 154, 60, 8, INK, .25); b.bar(236, 172, 44, 8, INK, .15)
    for (x, y, c) in [(340, 160, "#FDE047"), (374, 178, b.c3)]:
        b.add(f'<path d="M{x} {y + 16} h46 l-4 56 h-38z" fill="{c}" fill-opacity=".97" filter="url(#sh{b.p})"/>')
        b.path(f"M{x + 12} {y + 18} q0 -16 11 -16 q11 0 11 16", stroke=INK, sw=3, op=.7)
    b.chip(84, 64, "-15%", fill="#FEF3C7", tc="#92400E", dot="#F59E0B", op=1); b.chip(334, 62, "4.8 rating", dot="#F59E0B"); b.sparkle(392, 130, 8); b.sparkle(90, 200, 7)


def inventory(b):
    b.rect(100, 88, 6, 150, 3, WHITE, .9); b.rect(314, 88, 6, 150, 3, WHITE, .9)
    for y in (130, 184, 238): b.rect(100, y, 220, 7, 3, WHITE, .95)
    cols = ["#FDBA74", "#FB923C", "#FDE68A"]
    for row, y in enumerate((88, 142, 196)):
        x = 116
        for k in range(4):
            w = 40 + ((row + k) % 2) * 10; b.rect(x, y, w, 42, 5, cols[(row + k) % 3], .98); b.rect(x, y + 14, w, 8, 0, WHITE, .35); x += w + 8
    b.card(340, 96, 70, 80, 12)
    for i in range(14): b.rect(350 + i * 4, 108, 1.6 + (i % 3), 40, 0, INK, .85)
    b.text(375, 166, "SKU-4402", 8, 700, INK, "middle", .6)
    b.chip(324, 62, "Low stock: 24", fill="#FEF3C7", tc="#92400E", dot="#F59E0B", op=1, size=11); b.chip(332, 196, "Shipped", dot="#16A34A")
    b.sparkle(90, 70, 8); b.sparkle(404, 232, 7)


def hr(b):
    colors = ["#F472B6", "#FBBF24", "#34D399", "#60A5FA"]
    b.card(98, 70, 190, 78, 18)
    for i, c in enumerate(colors): b.circle(130 + i * 44, 108, 18, c, .95); b.text(130 + i * 44, 114, "ABCD"[i], 15, 800, WHITE, "middle")
    b.card(98, 164, 190, 76, 18)
    for i, (x, w, c) in enumerate([(110, 88, b.c3), (170, 60, "#FBBF24"), (130, 110, b.c3)]):
        b.rect(x + 4, 178 + i * 20, w, 12, 6, c, .8); b.circle(98 + 18, 184 + i * 20, 0, WHITE)
    b.card(306, 96, 100, 120, 16); b.circle(356, 134, 18, "#FACC15"); b.text(356, 141, "$", 20, 900, "#92400E", "middle")
    b.bar(322, 166, 68, 7, INK, .25); b.bar(322, 182, 52, 7, INK, .15); b.rect(322, 196, 68, 12, 6, b.c3, .8)
    b.chip(300, 64, "Payroll", dot="#16A34A"); b.chip(84, 238, "5 on leave", dot="#FBBF24"); b.sparkle(398, 232, 7); b.sparkle(300, 156, 6)


SCENES = {
    "podagain": (("#5B21B6", "#C026D3", "#FB7185"), podagain),
    "ai-support-copilot": (("#3730A3", "#2563EB", "#22D3EE"), ai_support),
    "booking-subscription-platform": (("#0F766E", "#10B981", "#A7F3D0"), booking),
    "logistics-dispatch-dashboard": (("#C2410C", "#F59E0B", "#FDE68A"), logistics),
    "restaurant-ordering-kds": (("#9F1239", "#EF4444", "#FDBA74"), restaurant),
    "property-listings-marketplace": (("#1D4ED8", "#3B82F6", "#7DD3FC"), property_),
    "telehealth-video-consult": (("#047857", "#14B8A6", "#67E8F9"), telehealth),
    "invoicing-expense-saas": (("#065F46", "#059669", "#BEF264"), invoicing),
    "amazon-price-seller-monitor": (("#D97706", "#F97316", "#FB7185"), amazon),
    "walmart-catalogue-scraper": (("#0369A1", "#4F46E5", "#38BDF8"), walmart),
    "cross-marketplace-repricer": (("#A21CAF", "#7C3AED", "#F0ABFC"), repricer),
    "invoice-document-extraction": (("#0E7490", "#0EA5E9", "#5EEAD3"), extraction),
    "county-surplus-list-pipeline": (("#1E3A8A", "#2563EB", "#93C5FD"), county),
    "school-management-system": (("#BE123C", "#F43F5E", "#FDBA74"), school),
    "multi-vendor-marketplace": (("#BE185D", "#F97316", "#FDE68A"), marketplace),
    "inventory-order-management": (("#0F766E", "#0891B2", "#67E8F9"), inventory),
    "hr-leave-payroll-portal": (("#6D28D9", "#4F46E5", "#93C5FD"), hr),
}


def banner(slug):
    (c1, c2, c3), scene = SCENES[slug]
    b = B(slug, c1, c2, c3)
    scene(b)
    return b.svg()
