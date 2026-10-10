"""One-off scientific figures for Part 1 (sieves, roast curve, particle sizes, extraction)."""
import math

from reportlab.lib import colors

import build_report as R
import deep_charts as DC
import illustrations as il
from illustrations import CanvasFigure, rgba, text

HX = colors.HexColor
INK, MUTED, RULE, ROAST, CARAMEL = R.INK, R.MUTED, R.RULE, R.ROAST, R.CARAMEL
TEAL, SAFFRON, LEAF, BERRY, PLUM, SKY, GOLD = R.TEAL, R.SAFFRON, R.LEAF, R.BERRY, R.PLUM, R.SKY, R.GOLD


def sieve_sizes(w, h):
    """Round-hole screen sizes drawn to scale (mm) with the grade each one defines."""
    screens = [(13, 5.00, "C floor"), (14, 5.50, "C"), (15, 6.00, "B / AB"), (17, 6.65, "A"),
               (18, 7.10, "AA"), (19, 7.50, "EB / AAA")]

    def draw(c, W, H):
        text(c, 0, H - 9, "Screen holes to scale (mm)", 8.0, "Body-Bold", ROAST)
        scale = min((W - 10) / sum(d + 3.2 for _, d, _ in screens), 7.2)
        x = 6
        base = H * 0.52
        for num, d, g in screens:
            r = d * scale / 2
            cx = x + r
            c.setFillColor(HX("#D8DDE2"))
            c.circle(cx, base, r + 2.4, stroke=0, fill=1)
            c.setFillColor(colors.white)
            c.circle(cx, base, r, stroke=0, fill=1)
            # a bean sitting on the hole
            c.setFillColor(rgba(HX("#8FA57E"), 0.85))
            c.ellipse(cx - r * 1.05, base - r * 0.72, cx + r * 1.05, base + r * 0.72, stroke=0, fill=1)
            c.setStrokeColor(HX("#5D7050"))
            c.setLineWidth(0.6)
            c.bezier(cx - r * 0.8, base, cx - r * 0.3, base + r * 0.25, cx + r * 0.3, base - r * 0.25,
                     cx + r * 0.8, base)
            text(c, cx, base - r - 14, f"{num}", 8.2, "Head", ROAST, "middle")
            text(c, cx, base - r - 23, f"{d:.2f} mm", 6.2, "Body", MUTED, "middle")
            text(c, cx, base + r + 6, g, 6.4, "Body-Bold", INK, "middle")
            x += d * scale + 3.2 * scale
        text(c, 0, 6, "Screen number = hole size in 64ths of an inch; Indian specs use millimetres.",
             6.2, "Body-Italic", MUTED)
    return CanvasFigure(w, h, draw)


def roast_curve(w, h):
    """Idealised drum-roast profile: bean temperature, rate of rise and the phases."""
    def bt(t):
        if t < 1.0:
            return 200 - 110 * t
        return 90 + 118 * (1 - math.exp(-(t - 1.0) / 3.6)) + 8 * (t - 1.0) / 9.5

    def ror(t):
        dt = 0.05
        return (bt(t + dt) - bt(t - dt)) / (2 * dt)

    def draw(c, W, H):
        text(c, 0, H - 9, "A typical 10.5-minute drum roast", 8.2, "Body-Bold", ROAST)
        text(c, 0, H - 19, "Bean temperature (brown), rate of rise (teal, °C per minute) and the stages",
             6.8, "Body-Italic", MUTED)
        x0, x1, y0, y1 = 34, W - 34, 24, H - 30
        tmax, tlo, thi = 11.0, 60, 240

        def X(t):
            return x0 + t / tmax * (x1 - x0)

        def Y(v):
            return y0 + (v - tlo) / (thi - tlo) * (y1 - y0)

        def YR(v):
            return y0 + v / 40 * (y1 - y0)
        phases = [(1.0, 4.6, "DRYING", HX("#E5EFD9")), (4.6, 8.4, "MAILLARD / BROWNING", HX("#F6E7D2")),
                  (8.4, 10.5, "DEVELOPMENT", HX("#EBD7C3"))]
        for a, b, lab, col in phases:
            c.setFillColor(col)
            c.rect(X(a), y0, X(b) - X(a), y1 - y0, stroke=0, fill=1)
            text(c, (X(a) + X(b)) / 2, y1 - 9, lab, 6.4, "Body-Bold", MUTED, "middle")
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        for v in range(60, 241, 30):
            c.line(x0, Y(v), x1, Y(v))
            text(c, x0 - 3, Y(v) - 2.2, f"{v}°", 6.2, "Body", MUTED, "end")
        for t in range(0, 12):
            text(c, X(t), y0 - 9, f"{t}", 6.2, "Body", MUTED, "middle")
        for v in range(0, 41, 10):
            text(c, x1 + 3, YR(v) - 2.2, f"{v}", 6.2, "Body", TEAL)
        text(c, (x0 + x1) / 2, 4, "minutes", 6.6, "Body-Italic", MUTED, "middle")
        # bean temperature
        c.setStrokeColor(ROAST)
        c.setLineWidth(1.8)
        p = c.beginPath()
        p.moveTo(X(0), Y(bt(0)))
        t = 0.05
        while t <= 10.5:
            p.lineTo(X(t), Y(bt(t)))
            t += 0.05
        c.drawPath(p, stroke=1, fill=0)
        # rate of rise
        c.setStrokeColor(TEAL)
        c.setLineWidth(1.3)
        p = c.beginPath()
        t = 1.5
        p.moveTo(X(t), YR(ror(t)))
        while t <= 10.5:
            p.lineTo(X(t), YR(max(0, ror(t))))
            t += 0.05
        c.drawPath(p, stroke=1, fill=0)
        marks = [(0.0, "Charge ~200°C"), (1.0, "Turning point ~90°C"), (4.6, "Yellowing ~150-160°C"),
                 (8.4, "First crack ~196°C"), (10.5, "Drop ~208°C")]
        for i, (tt, lab) in enumerate(marks):
            yy = Y(bt(tt))
            c.setFillColor(BERRY)
            c.circle(X(tt), yy, 2.2, stroke=0, fill=1)
            off = 10 if i % 2 == 0 else -14
            il.label_box(c, X(tt) + (4 if tt < 10 else -4), yy + off, lab, 6.2,
                         "start" if tt < 10 else "end", "Body")
        text(c, X(9.45), Y(120), "development time", 6.2, "Body-Italic", INK, "middle")
        text(c, X(9.45), Y(110), "= 20% of roast", 6.2, "Body-Italic", INK, "middle")
    return CanvasFigure(w, h, draw)


def particle_dist(w, h):
    """Illustrative particle-size distributions for flat, conical and blade grinders."""
    def gauss(x, m, s):
        return math.exp(-0.5 * ((x - m) / s) ** 2)

    curves = [("Flat burrs", TEAL, lambda x: gauss(x, 700, 140) + 0.10 * gauss(x, 60, 30)),
              ("Conical burrs", SAFFRON, lambda x: 0.85 * gauss(x, 720, 190) + 0.30 * gauss(x, 70, 40)),
              ("Blade grinder", BERRY, lambda x: 0.45 * gauss(x, 650, 420) + 0.28 * gauss(x, 90, 70)
               + 0.18 * gauss(x, 1500, 300))]

    def draw(c, W, H):
        text(c, 0, H - 9, "Particle-size distribution, same average grind (illustrative)", 8.2,
             "Body-Bold", ROAST)
        x0, x1, y0, y1 = 20, W - 8, 24, H - 18
        xmax = 2000

        def X(v):
            return x0 + v / xmax * (x1 - x0)

        def Y(v):
            return y0 + v * (y1 - y0)
        c.setFillColor(rgba(GOLD, 0.16))
        c.rect(X(0), y0, X(100) - X(0), y1 - y0, stroke=0, fill=1)
        text(c, X(50), y1 - 8, "fines", 6.2, "Body-Italic", MUTED, "middle")
        c.setFillColor(rgba(SKY, 0.10))
        c.rect(X(1200), y0, X(2000) - X(1200), y1 - y0, stroke=0, fill=1)
        text(c, X(1600), y1 - 8, "boulders", 6.2, "Body-Italic", MUTED, "middle")
        c.setStrokeColor(MUTED)
        c.setLineWidth(0.6)
        c.line(x0, y0, x1, y0)
        for v in range(0, 2001, 250):
            text(c, X(v), y0 - 9, f"{v}", 6.0, "Body", MUTED, "middle")
        text(c, (x0 + x1) / 2, 4, "particle size, microns (µm)", 6.6, "Body-Italic", MUTED, "middle")
        for name, col, f in curves:
            c.setStrokeColor(col)
            c.setLineWidth(1.6)
            p = c.beginPath()
            p.moveTo(X(0), Y(f(0)))
            for v in range(10, 2001, 10):
                p.lineTo(X(v), Y(min(1.05, f(v))))
            c.drawPath(p, stroke=1, fill=0)
        DC._legend(c, [(n, col, "line") for n, col, _ in curves], X(1150), y1 - 26)
    return CanvasFigure(w, h, draw)


def extraction_sequence(w, h):
    def draw(c, W, H):
        text(c, 0, H - 9, "What dissolves first: the order of extraction", 8.2, "Body-Bold", ROAST)
        x0, x1, y0, y1 = 6, W - 6, 26, H - 20
        bands = [("ACIDS & SALTS", "sour, bright, salty", HX("#F2C14E"), 0.0, 0.36),
                 ("SUGARS & BROWNING PRODUCTS", "sweet, caramel, body", HX("#C68B59"), 0.30, 0.74),
                 ("BITTER COMPOUNDS & TANNINS", "bitter, dry, astringent", HX("#5A3A26"), 0.66, 1.0)]
        bh = (y1 - y0) / 3
        for i, (lab, sub, col, a, b) in enumerate(bands):
            y = y1 - (i + 1) * bh
            c.setFillColor(col)
            c.roundRect(x0 + a * (x1 - x0), y + 2, (b - a) * (x1 - x0), bh - 4, 4, stroke=0, fill=1)
            tc = colors.white if i == 2 else INK
            text(c, x0 + a * (x1 - x0) + 6, y + bh / 2 + 0.5, lab, 6.8, "Body-Bold", tc)
            text(c, x0 + a * (x1 - x0) + 6, y + bh / 2 - 7.5, sub, 6.2, "Body", tc)
        il.arrow(c, x0, 14, x1, 14, MUTED, 0.9, 4)
        text(c, x0, 3, "early in the brew / coarse grind / short time", 6.2, "Body-Italic", MUTED)
        text(c, x1, 3, "late in the brew / fine grind / long time", 6.2, "Body-Italic", MUTED, "end")
        mid = x0 + 0.52 * (x1 - x0)
        c.setStrokeColor(LEAF)
        c.setLineWidth(1.2)
        c.setDash(3, 2)
        c.line(mid, y0 - 2, mid, y1 + 2)
        c.setDash()
        il.label_box(c, mid, y1 + 4, "sweet spot: 18-22% extracted", 6.4, "middle", "Body-Bold", LEAF)
    return CanvasFigure(w, h, draw)


def method_map(w, h):
    pts = [("Espresso", 9.2, 9.0), ("Moka pot", 6.0, 8.2), ("Turkish", 2.4, 9.4), ("French press", 3.6, 7.0),
           ("AeroPress", 6.8, 6.0), ("Filter kaapi", 4.2, 7.9), ("Clever", 6.6, 5.2),
           ("V60", 8.6, 3.8), ("Kalita", 7.7, 4.6), ("Chemex", 9.5, 2.9), ("Batch brew", 7.2, 3.6),
           ("Siphon", 8.2, 5.0), ("Cold brew", 5.0, 4.6), ("Phin", 4.7, 8.6)]
    cols = {"Espresso": BERRY, "Moka pot": BERRY, "AeroPress": BERRY, "Turkish": PLUM, "French press": SKY,
            "Clever": SKY, "Cold brew": SKY, "Siphon": SKY, "V60": TEAL, "Kalita": TEAL, "Chemex": TEAL,
            "Batch brew": TEAL, "Filter kaapi": SAFFRON, "Phin": SAFFRON}
    points = [(n, x, y, 30, cols[n]) for n, x, y in pts]
    fig = DC.bubble(points, w, h, title="Why there are so many methods: each trades clarity against body",
                    sub="Red = pressure, blue = immersion, teal = paper percolation, orange = metal-filter "
                        "percolation, purple = boiled",
                    xlab="clarity: clean, transparent, tea-like  →",
                    ylab="body & strength  →", xfmt="{:.0f}", yfmt="{:.0f}", xr=(1, 10), yr=(2, 10),
                    size_scale=0.9, label_size=6.6)
    return fig


def grind_microns(w, h):
    items = [("Turkish", 40, 220, PLUM, "40-220 µm  powder"),
             ("Espresso", 180, 380, BERRY, "180-380  fine sand"),
             ("Filter kaapi", 250, 450, SAFFRON, "250-450  fine"),
             ("Moka pot", 360, 660, BERRY, "360-660  fine-medium"),
             ("AeroPress", 320, 960, BERRY, "320-960  depends on recipe"),
             ("V60 / Kalita", 400, 900, TEAL, "400-900  table salt"),
             ("Chemex / batch", 600, 1000, TEAL, "600-1,000  medium-coarse"),
             ("French press", 690, 1300, SKY, "690-1,300  coarse"),
             ("Cold brew", 800, 1500, SKY, "800-1,500  very coarse")]
    return R.hbar_ranges(items, "Grind size by method (microns, approximate)", w, h,
                         lambda v: f"{v:,}", 1500, label_w=78, note="burr grinder, 1 mm = 1,000 µm")


def cup_anatomy(parts, w, h, title):
    """parts: [(label, rupees, colour)] stacked into one horizontal bar = price of a drink."""
    def draw(c, W, H):
        text(c, 0, H - 9, title, 8.2, "Body-Bold", ROAST)
        tot = sum(v for _, v, _ in parts)
        x0, x1 = 0, W
        y = H - 46
        bh = 22
        x = x0
        for i, (lab, v, col) in enumerate(parts):
            ww = v / tot * (x1 - x0)
            c.setFillColor(col)
            c.rect(x, y, ww, bh, stroke=0, fill=1)
            c.setStrokeColor(colors.white)
            c.setLineWidth(0.8)
            c.line(x, y, x, y + bh)
            if ww > 22:
                text(c, x + ww / 2, y + bh / 2 - 2.6, f"₹{v:.0f}", 7.0, "Body-Bold",
                     colors.white if i not in (1, 2) else INK, "middle")
            ly = y - 12 - (i % 2) * 10
            text(c, x + ww / 2, ly, lab, 6.2, "Body", INK, "middle")
            x += ww
        text(c, 0, y + bh + 4, f"Total ₹{tot:.0f} (ex-GST)", 6.8, "Body-Italic", MUTED)
    return CanvasFigure(w, h, draw)
