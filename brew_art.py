"""Vector illustrations of brewing equipment, grinders and a roaster (flat style).

Each `draw_*` function paints inside a 100 x 120 unit box; `icon(fn, w, h)` wraps one
as a flowable at any size, and `strip()` lays several out with captions.
"""
from reportlab.lib import colors

import illustrations as il
from illustrations import CanvasFigure, rgba, shade, text

HX = colors.HexColor
STEEL = HX("#B9BEC4")
STEEL_D = HX("#7D848C")
STEEL_L = HX("#EEF1F4")
GLASS = HX("#DCEBF2")
GLASS_E = HX("#9FB9C6")
COFFEE = HX("#3B2416")
COFFEE_L = HX("#6B4430")
CREMA = HX("#C98B4E")
MILK = HX("#F4EBDD")
FOAM = HX("#FFFDF8")
WOOD = HX("#9A6B43")
BLACK = HX("#2B2B2B")
PAPER_F = HX("#FAF6EE")
FLAME = HX("#F29E4C")
ALU = HX("#C7CCD1")
SAFFRON = HX("#F29E4C")


def _poly(c, pts, fill=None, stroke=None, lw=0.8, close=True):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    if close:
        p.close()
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.drawPath(p, stroke=1 if stroke is not None else 0, fill=1 if fill is not None else 0)
    return p


def _steel(c, pts, x0, x1, base=STEEL):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    il.grad_fill(c, p, "linear", (x0, 0, x1, 0), [shade(base, 0.8), shade(base, 1.6), base,
                                                   shade(base, 0.7)], [0, 0.35, 0.65, 1])
    c.setStrokeColor(shade(base, 0.6))
    c.setLineWidth(0.6)
    c.drawPath(p, stroke=1, fill=0)


def _rrect(c, x, y, w, h, r, fill, stroke=None, lw=0.6):
    c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, stroke=1 if stroke is not None else 0, fill=1)


def _drip(c, x, y0, y1, col=COFFEE):
    c.setStrokeColor(col)
    c.setLineWidth(1.2)
    c.line(x, y0, x, y1)


def _cup(c, x, y, w, h, fill=HX("#FFFFFF"), liquid=COFFEE, handle=True):
    _poly(c, [(x, y + h), (x + w, y + h), (x + w * 0.88, y), (x + w * 0.12, y)], fill, STEEL_D, 0.6)
    _poly(c, [(x + 1.2, y + h - 2.2), (x + w - 1.2, y + h - 2.2), (x + w - 2, y + h - 5),
              (x + 2, y + h - 5)], liquid)
    if handle:
        c.setStrokeColor(STEEL_D)
        c.setLineWidth(1.6)
        c.arc(x + w - 4, y + h * 0.25, x + w + 6, y + h * 0.8, -90, 180)


# ------------------------------------------------------------------ pour-over family
def draw_v60(c):
    # glass server
    _poly(c, [(26, 6), (74, 6), (78, 40), (70, 50), (30, 50), (22, 40)], rgba(GLASS, 0.8), GLASS_E)
    _poly(c, [(27, 8), (73, 8), (76, 26), (24, 26)], COFFEE_L)
    c.setStrokeColor(GLASS_E)
    c.setLineWidth(1.6)
    c.arc(72, 18, 88, 42, -80, 160)
    # base plate & cone
    _rrect(c, 28, 50, 44, 5, 2, HX("#D9D4CC"), STEEL_D)
    _poly(c, [(14, 104), (86, 104), (60, 57), (40, 57)], HX("#F1EEE9"), STEEL_D, 0.8)
    _poly(c, [(19, 101), (81, 101), (58, 60), (42, 60)], PAPER_F, HX("#D9D0C0"), 0.5)
    _poly(c, [(26, 88), (74, 88), (58, 62), (42, 62)], COFFEE_L)
    c.setStrokeColor(rgba(STEEL_D, 0.6))
    c.setLineWidth(0.5)
    for k in range(4):
        c.line(22 + k * 4, 103, 44 + k * 2, 58)
        c.line(78 - k * 4, 103, 56 - k * 2, 58)
    _drip(c, 50, 57, 30)
    # kettle spout stream
    c.setStrokeColor(GLASS_E)
    c.setLineWidth(1)
    c.bezier(84, 118, 70, 117, 58, 112, 52, 92)


def draw_chemex(c):
    _poly(c, [(20, 112), (80, 112), (58, 66), (62, 58), (84, 30), (78, 8), (22, 8), (16, 30),
              (38, 58), (42, 66)], rgba(GLASS, 0.85), GLASS_E, 0.9)
    _poly(c, [(19, 26), (81, 26), (77, 10), (23, 10)], COFFEE_L)
    _poly(c, [(24, 110), (76, 110), (54, 70), (46, 70)], PAPER_F, HX("#D9D0C0"), 0.5)
    _poly(c, [(32, 96), (68, 96), (54, 72), (46, 72)], COFFEE_L)
    _poly(c, [(36, 70), (64, 70), (62, 56), (38, 56)], WOOD, shade(WOOD, 0.7))
    c.setStrokeColor(HX("#5A3A22"))
    c.setLineWidth(1.4)
    c.line(50, 63, 50, 44)
    c.setFillColor(HX("#5A3A22"))
    c.circle(50, 42, 2.4, stroke=0, fill=1)


def draw_kalita(c):
    _cup(c, 24, 6, 52, 40, liquid=COFFEE_L)
    _rrect(c, 22, 46, 56, 5, 2, STEEL, STEEL_D)
    _steel(c, [(16, 100), (84, 100), (66, 52), (34, 52)], 16, 84)
    pts = []
    for k in range(13):
        x = 20 + k * 5
        pts.append((x, 104 if k % 2 == 0 else 99))
    _poly(c, pts + [(64, 58), (36, 58)], PAPER_F, HX("#D9D0C0"), 0.5)
    _poly(c, [(26, 82), (74, 82), (64, 60), (36, 60)], COFFEE_L)
    for x in (44, 50, 56):
        _drip(c, x, 51, 40)


def draw_clever(c):
    _cup(c, 26, 6, 48, 36, liquid=COFFEE_L)
    _poly(c, [(14, 104), (86, 104), (62, 50), (38, 50)], rgba(HX("#CFE3EA"), 0.9), GLASS_E)
    _poly(c, [(19, 98), (81, 98), (60, 54), (40, 54)], COFFEE)
    _rrect(c, 36, 42, 28, 8, 2, BLACK)
    text(c, 50, 30, "", 6)


# ------------------------------------------------------------------ immersion
def draw_french_press(c):
    _poly(c, [(26, 10), (70, 10), (70, 92), (26, 92)], rgba(GLASS, 0.75), GLASS_E)
    _poly(c, [(27, 11), (69, 11), (69, 70), (27, 70)], COFFEE)
    _poly(c, [(27, 70), (69, 70), (69, 76), (27, 76)], HX("#8A5A3A"))
    _steel(c, [(23, 4), (73, 4), (73, 12), (23, 12)], 23, 73)
    _steel(c, [(24, 90), (72, 90), (72, 98), (24, 98)], 24, 72)
    _poly(c, [(28, 60), (68, 60), (68, 63), (28, 63)], STEEL_D)
    c.setStrokeColor(STEEL_D)
    c.setLineWidth(2)
    c.line(48, 63, 48, 112)
    c.setFillColor(BLACK)
    c.circle(48, 114, 4, stroke=0, fill=1)
    c.setStrokeColor(BLACK)
    c.setLineWidth(4)
    c.bezier(71, 84, 88, 84, 88, 30, 71, 30)


def draw_aeropress(c):
    _cup(c, 24, 6, 52, 32, liquid=COFFEE_L)
    _rrect(c, 31, 38, 38, 4, 1.5, BLACK)
    _poly(c, [(34, 42), (66, 42), (66, 92), (34, 92)], rgba(HX("#C9CDD2"), 0.8), STEEL_D)
    _poly(c, [(35, 43), (65, 43), (65, 66), (35, 66)], COFFEE)
    _rrect(c, 28, 90, 44, 4, 1.5, rgba(STEEL_D, 0.9))
    _poly(c, [(36, 70), (64, 70), (64, 112), (36, 112)], rgba(HX("#9DA3AA"), 0.8), STEEL_D)
    _rrect(c, 30, 112, 40, 5, 2, BLACK)
    _rrect(c, 36, 67, 28, 4, 1, BLACK)


def draw_cold_brew(c):
    _poly(c, [(22, 6), (78, 6), (80, 92), (20, 92)], rgba(GLASS, 0.8), GLASS_E)
    _poly(c, [(23, 7), (77, 7), (79, 80), (21, 80)], HX("#4A2E1D"))
    c.setFillColor(rgba(HX("#E9DCC4"), 0.9))
    c.roundRect(34, 30, 32, 52, 6, stroke=0, fill=1)
    c.setFillColor(rgba(COFFEE_L, 0.8))
    for k in range(40):
        x = 37 + (k * 7) % 26
        y = 34 + (k * 11) % 44
        c.circle(x, y, 1.1, stroke=0, fill=1)
    _rrect(c, 18, 92, 64, 9, 3, STEEL_D)
    for i, y in enumerate((60, 45, 20)):
        c.setFillColor(rgba(colors.white, 0.75))
        c.rect(26 + i * 15, y, 7, 7, stroke=0, fill=1)


def draw_siphon(c):
    c.setFillColor(rgba(GLASS, 0.85))
    c.setStrokeColor(GLASS_E)
    c.setLineWidth(0.9)
    c.circle(50, 30, 20, stroke=1, fill=1)
    c.setFillColor(COFFEE_L)
    p = c.beginPath()
    p.moveTo(31, 26)
    p.arcTo(30, 10, 70, 50, 190, 160)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    _poly(c, [(36, 112), (64, 112), (60, 62), (54, 54), (46, 54), (40, 62)], rgba(GLASS, 0.85), GLASS_E)
    _poly(c, [(39, 96), (61, 96), (59, 66), (41, 66)], COFFEE)
    c.setStrokeColor(GLASS_E)
    c.setLineWidth(2)
    c.line(50, 54, 50, 32)
    c.setStrokeColor(STEEL_D)
    c.setLineWidth(2.2)
    c.line(78, 4, 78, 84)
    c.line(78, 84, 62, 84)
    c.line(78, 50, 68, 50)
    _rrect(c, 40, 2, 20, 6, 2, STEEL_D)
    c.setFillColor(FLAME)
    _poly(c, [(46, 8), (50, 14), (54, 8)], FLAME)


def draw_cezve(c):
    _poly(c, [(30, 18), (64, 18), (60, 56), (66, 64), (28, 64), (34, 56)], HX("#C77B3B"),
          shade(HX("#C77B3B"), 0.6))
    _poly(c, [(29, 60), (65, 60), (66, 66), (28, 66)], HX("#C9A46A"))
    c.setStrokeColor(WOOD)
    c.setLineWidth(4)
    c.line(64, 56, 96, 74)
    _rrect(c, 18, 6, 64, 12, 3, HX("#E3C99A"))
    c.setFillColor(rgba(FLAME, 0.9))
    for x in (34, 46, 58):
        _poly(c, [(x - 4, 6), (x, 13), (x + 4, 6)], FLAME)


def draw_phin(c):
    _poly(c, [(28, 6), (72, 6), (74, 60), (26, 60)], rgba(GLASS, 0.85), GLASS_E)
    _poly(c, [(29, 7), (71, 7), (72, 22), (28, 22)], HX("#F2E3C2"))
    _poly(c, [(28, 22), (72, 22), (73, 40), (27, 40)], COFFEE_L)
    _rrect(c, 22, 60, 56, 4, 1.5, STEEL, STEEL_D)
    _steel(c, [(32, 64), (68, 64), (68, 92), (32, 92)], 32, 68)
    _steel(c, [(30, 92), (70, 92), (70, 98), (30, 98)], 30, 70)
    _drip(c, 50, 60, 42)


def draw_batch(c):
    _steel(c, [(14, 30), (86, 30), (86, 112), (14, 112)], 14, 86, base=HX("#5E6268"))
    _rrect(c, 22, 82, 56, 22, 3, BLACK)
    _rrect(c, 26, 90, 48, 8, 2, HX("#3D3D3D"))
    _steel(c, [(30, 8), (70, 8), (72, 62), (28, 62)], 28, 72)
    _rrect(c, 34, 62, 32, 6, 2, BLACK)
    c.setFillColor(HX("#3CC46A"))
    c.circle(78, 40, 2, stroke=0, fill=1)
    _rrect(c, 10, 2, 80, 6, 2, BLACK)


# ------------------------------------------------------------------ stove-top & pressure
def draw_moka(c):
    _steel(c, [(24, 8), (76, 8), (68, 54), (32, 54)], 24, 76, base=ALU)
    _steel(c, [(34, 54), (66, 54), (66, 60), (34, 60)], 34, 66, base=ALU)
    _steel(c, [(30, 60), (70, 60), (76, 100), (24, 100)], 24, 76, base=ALU)
    _poly(c, [(24, 100), (76, 100), (70, 106), (30, 106)], shade(ALU, 0.9), STEEL_D)
    c.setFillColor(BLACK)
    c.circle(50, 109, 3.5, stroke=0, fill=1)
    _poly(c, [(24, 98), (14, 104), (16, 106), (27, 101)], shade(ALU, 0.85), STEEL_D)
    c.setStrokeColor(BLACK)
    c.setLineWidth(5)
    c.bezier(76, 96, 94, 94, 94, 70, 80, 66)
    c.setStrokeColor(rgba(STEEL_D, 0.55))
    c.setLineWidth(0.5)
    for x in (38, 50, 62):
        c.line(x, 10, x - (x - 50) * 0.2, 52)
        c.line(x - (x - 50) * 0.15, 62, x + (x - 50) * 0.2, 98)
    c.setFillColor(rgba(FLAME, 0.9))
    for x in (36, 50, 64):
        _poly(c, [(x - 5, 0), (x, 7), (x + 5, 0)], FLAME)


def draw_espresso(c):
    _steel(c, [(4, 46), (96, 46), (96, 104), (4, 104)], 4, 96)
    _rrect(c, 4, 104, 92, 6, 2, shade(STEEL, 0.8))
    for k in range(3):
        _rrect(c, 12 + k * 26, 110, 20, 7, 2, HX("#FFFFFF"), STEEL_D)
    _rrect(c, 12, 78, 76, 16, 3, HX("#2E2E2E"))
    c.setFillColor(HX("#7FD1E0"))
    c.rect(18, 84, 14, 5, stroke=0, fill=1)
    c.setFillColor(SAFFRON)
    for k in range(3):
        c.circle(46 + k * 8, 86, 2, stroke=0, fill=1)
    _steel(c, [(38, 40), (62, 40), (62, 50), (38, 50)], 38, 62, base=shade(STEEL, 0.9))
    _rrect(c, 36, 34, 28, 6, 2, STEEL_D)
    c.setStrokeColor(BLACK)
    c.setLineWidth(4)
    c.line(62, 37, 90, 33)
    _cup(c, 40, 14, 20, 15, liquid=CREMA)
    c.setStrokeColor(COFFEE)
    c.setLineWidth(1)
    c.line(47, 33, 47, 27)
    c.line(53, 33, 53, 27)
    _steel(c, [(2, 6), (98, 6), (98, 14), (2, 14)], 2, 98, base=shade(STEEL, 0.85))
    c.setStrokeColor(STEEL_D)
    c.setLineWidth(1.8)
    c.line(12, 60, 10, 26)
    c.line(10, 26, 14, 22)


def draw_kaapi(c):
    _steel(c, [(30, 58), (70, 58), (70, 98), (30, 98)], 30, 70)
    _poly(c, [(28, 98), (72, 98), (68, 104), (32, 104)], shade(STEEL, 0.9), STEEL_D)
    c.setFillColor(STEEL_D)
    c.circle(50, 107, 3, stroke=0, fill=1)
    _steel(c, [(26, 8), (74, 8), (74, 62), (26, 62)], 26, 74)
    c.setFillColor(rgba(COFFEE, 0.9))
    c.rect(28, 10, 44, 20, stroke=0, fill=1)
    c.setFillColor(rgba(colors.white, 0.6))
    for k in range(7):
        c.circle(34 + k * 5, 60, 0.9, stroke=0, fill=1)
    for x in (38, 50, 62):
        _drip(c, x, 56, 34)
    _rrect(c, 24, 58, 52, 3, 1, STEEL_D)


def draw_davara(c):
    _steel(c, [(10, 6), (90, 6), (84, 30), (16, 30)], 10, 90)
    _poly(c, [(12, 28), (88, 28), (86, 32), (14, 32)], shade(STEEL, 0.8))
    _steel(c, [(30, 30), (70, 30), (74, 96), (26, 96)], 26, 74)
    _poly(c, [(27, 92), (73, 92), (74, 100), (26, 100)], HX("#C9965F"))
    c.setFillColor(HX("#E9D2AE"))
    for k in range(9):
        c.circle(30 + k * 5, 100.5, 2.2, stroke=0, fill=1)


# ------------------------------------------------------------------ grinders & roaster
def draw_burrs(c, w, h):
    """Flat vs conical burrs, schematic cross-sections, plus a blade grinder."""
    col = STEEL_D
    bw = w / 3
    # flat burrs
    fw = min(96, bw - 40)
    cxf = bw / 2
    x = cxf - fw / 2
    _steel(c, [(x, h * 0.52), (x + fw, h * 0.52), (x + fw, h * 0.60), (x, h * 0.60)], x, x + fw)
    _steel(c, [(x, h * 0.42), (x + fw, h * 0.42), (x + fw, h * 0.50), (x, h * 0.50)], x, x + fw)
    c.setFillColor(HX("#FFFFFF"))
    c.rect(cxf - 6, h * 0.52, 12, h * 0.08, stroke=0, fill=1)
    c.setFillColor(COFFEE_L)
    for k in range(9):
        c.circle(x + 6 + k * (fw - 12) / 8, h * 0.51, 1.3, stroke=0, fill=1)
    il.arrow(c, cxf, h * 0.86, cxf, h * 0.62, CREMA, 1.2, 4)
    text(c, cxf, h * 0.88, "beans in", 6.4, "Body", il.MUTED, "middle")
    il.arrow(c, x + 2, h * 0.51, x - 12, h * 0.51, CREMA, 1.0, 3)
    il.arrow(c, x + fw - 2, h * 0.51, x + fw + 12, h * 0.51, CREMA, 1.0, 3)
    text(c, cxf, h * 0.24, "FLAT BURRS", 7.2, "Body-Bold", il.ROAST, "middle")
    text(c, cxf, h * 0.14, "two parallel rings; grounds exit", 6.2, "Body", il.MUTED, "middle")
    text(c, cxf, h * 0.06, "sideways; very even particle size", 6.2, "Body", il.MUTED, "middle")
    # conical burrs
    cx = bw * 1.5
    _steel(c, [(cx - 30, h * 0.36), (cx + 30, h * 0.36), (cx + 22, h * 0.74), (cx - 22, h * 0.74)],
           cx - 30, cx + 30, base=shade(STEEL, 0.9))
    _steel(c, [(cx - 22, h * 0.40), (cx + 22, h * 0.40), (cx + 8, h * 0.72), (cx - 8, h * 0.72)],
           cx - 22, cx + 22)
    c.setStrokeColor(rgba(col, 0.7))
    c.setLineWidth(0.5)
    for k in range(-3, 4):
        c.line(cx + k * 5, h * 0.42, cx + k * 2, h * 0.70)
    il.arrow(c, cx, h * 0.92, cx, h * 0.76, CREMA, 1.2, 4)
    il.arrow(c, cx, h * 0.38, cx, h * 0.27, CREMA, 1.0, 3)
    text(c, cx, h * 0.18, "CONICAL BURRS", 7.2, "Body-Bold", il.ROAST, "middle")
    text(c, cx, h * 0.09, "cone inside a ring; grounds fall down;", 6.2, "Body", il.MUTED, "middle")
    text(c, cx, h * 0.01, "two particle peaks (more fines)", 6.2, "Body", il.MUTED, "middle")
    # blade
    cx = bw * 2.5
    _poly(c, [(cx - 24, h * 0.80), (cx + 24, h * 0.80), (cx + 20, h * 0.36), (cx - 20, h * 0.36)],
          rgba(GLASS, 0.8), GLASS_E)
    c.setStrokeColor(BLACK)
    c.setLineWidth(2.2)
    c.line(cx - 16, h * 0.48, cx + 16, h * 0.42)
    c.setFillColor(COFFEE_L)
    for k in range(18):
        c.circle(cx - 16 + (k * 7) % 32, h * 0.44 + (k * 5) % 20, 1.0 + (k % 3) * 0.7, stroke=0, fill=1)
    text(c, cx, h * 0.24, "BLADE GRINDER", 7.2, "Body-Bold", il.BERRY, "middle")
    text(c, cx, h * 0.14, "a spinning blade smashes beans:", 6.2, "Body", il.MUTED, "middle")
    text(c, cx, h * 0.06, "dust + chunks, uneven extraction", 6.2, "Body", il.MUTED, "middle")


def draw_roaster(c, w, h):
    """Schematic drum roaster with labelled parts."""
    s = min(w / 300, h / 170)
    c.translate(max(0, (w - 380 * s) / 2), 0)
    c.saveState()
    c.scale(s, s)
    # body
    _steel(c, [(90, 50), (190, 50), (190, 120), (90, 120)], 90, 190, base=HX("#4A4F55"))
    # hopper
    _steel(c, [(115, 150), (165, 150), (148, 122), (132, 122)], 115, 165)
    # drum (cutaway)
    c.setFillColor(HX("#2A2A2A"))
    c.circle(140, 85, 28, stroke=0, fill=1)
    c.setFillColor(HX("#A86A38"))
    for k in range(26):
        x = 120 + (k * 9) % 40
        y = 62 + (k * 7) % 14
        c.ellipse(x, y, x + 5, y + 3.2, stroke=0, fill=1)
    c.setStrokeColor(STEEL)
    c.setLineWidth(1)
    c.circle(140, 85, 28, stroke=1, fill=0)
    c.line(140, 85, 158, 104)
    c.line(140, 85, 120, 100)
    # burner
    for x in (118, 132, 146, 160):
        _poly(c, [(x - 6, 52), (x, 64), (x + 6, 52)], FLAME)
    # chimney / cyclone
    _steel(c, [(196, 108), (212, 108), (212, 160), (196, 160)], 196, 212)
    _steel(c, [(230, 60), (262, 60), (262, 120), (230, 120)], 230, 262)
    _poly(c, [(230, 60), (262, 60), (246, 40)], STEEL, STEEL_D)
    c.setStrokeColor(STEEL_D)
    c.setLineWidth(5)
    c.line(190, 112, 230, 112)
    # cooling tray
    c.setFillColor(HX("#5E6268"))
    c.ellipse(20, 30, 92, 52, stroke=0, fill=1)
    c.setFillColor(HX("#7A4A2A"))
    for k in range(30):
        x = 28 + (k * 11) % 56
        y = 36 + (k * 5) % 12
        c.ellipse(x, y, x + 4.5, y + 3, stroke=0, fill=1)
    _steel(c, [(48, 6), (64, 6), (64, 30), (48, 30)], 48, 64)
    _steel(c, [(92, 72), (100, 72), (96, 54), (88, 54)], 88, 100)
    # legs
    _rrect(c, 96, 30, 8, 20, 1, STEEL_D)
    _rrect(c, 176, 30, 8, 20, 1, STEEL_D)
    c.restoreState()
    labs = [(140, 156, 175, 165, "Hopper: green beans in"),
            (160, 98, 268, 140, "Rotating drum: beans tumble"),
            (150, 58, 268, 30, "Gas burner: heat by conduction + convection"),
            (204, 150, 268, 160, "Exhaust: smoke & chaff out"),
            (246, 92, 268, 92, "Cyclone collects chaff"),
            (40, 50, 0, 64, "Cooling tray: stir + air"),
            (96, 64, 4, 100, "Probe: bean temperature")]
    for x0, y0, x1, y1, t in labs:
        il.leader(c, x1 * s + (0 if x1 < x0 else 0), y1 * s + 2, x0 * s, y0 * s)
        il.label_box(c, x1 * s, y1 * s, t, 6.4, "start" if x1 > x0 else "start", "Body")


# ------------------------------------------------------------------ milk drinks
MILK_DRINKS = [  # name, cup shape (w, h), layers bottom->top [(fraction, colour)], note
    ("Espresso", (34, 26), [(0.8, COFFEE), (0.2, CREMA)], "30-40 ml"),
    ("Macchiato", (34, 30), [(0.6, COFFEE), (0.15, CREMA), (0.25, FOAM)], "+ dab of foam"),
    ("Cortado", (40, 40), [(0.5, COFFEE), (0.5, MILK)], "1:1, ~120 ml"),
    ("Flat white", (52, 40), [(0.3, COFFEE), (0.62, HX("#D9B48A")), (0.08, FOAM)], "~160 ml, thin foam"),
    ("Cappuccino", (54, 42), [(0.25, COFFEE), (0.4, HX("#D9B48A")), (0.35, FOAM)], "~180 ml, 1-2 cm foam"),
    ("Latte", (46, 62), [(0.18, COFFEE), (0.72, HX("#E2C29C")), (0.1, FOAM)], "240-300 ml"),
    ("Mocha", (46, 60), [(0.12, HX("#2A160C")), (0.18, COFFEE), (0.6, HX("#C79A72")), (0.1, FOAM)],
     "+ chocolate"),
    ("Filter kaapi", (34, 56), [(0.35, COFFEE_L), (0.5, HX("#D7AE7E")), (0.15, HX("#F1E3CC"))],
     "decoction + hot milk"),
]


def draw_milk_drinks(c, w, h):
    n = len(MILK_DRINKS)
    cw = w / n
    base = 22
    for i, (name, (cwid, chgt), layers, note) in enumerate(MILK_DRINKS):
        cx = i * cw + cw / 2
        x = cx - cwid / 2
        y = base
        # cup outline
        _poly(c, [(x, y + chgt), (x + cwid, y + chgt), (x + cwid * 0.9, y), (x + cwid * 0.1, y)],
              HX("#FFFFFF"), STEEL_D, 0.7)
        yy = y
        for frac, col in layers:
            hh = (chgt - 2) * frac
            t0 = (yy - y) / chgt
            t1 = (yy + hh - y) / chgt
            xa0 = x + cwid * 0.1 * (1 - t0) + 1
            xb0 = x + cwid - cwid * 0.1 * (1 - t0) - 1
            xa1 = x + cwid * 0.1 * (1 - t1) + 1
            xb1 = x + cwid - cwid * 0.1 * (1 - t1) - 1
            _poly(c, [(xa0, yy + 0.8), (xb0, yy + 0.8), (xb1, yy + hh), (xa1, yy + hh)], col)
            yy += hh
        text(c, cx, 12, name, 7.0, "Body-Bold", il.INK, "middle")
        text(c, cx, 4, note, 5.9, "Body", il.MUTED, "middle")
    lx = w - 190
    for lab, col in (("espresso", COFFEE), ("steamed milk", HX("#D9B48A")), ("microfoam", FOAM)):
        c.setFillColor(col)
        c.setStrokeColor(STEEL_D)
        c.setLineWidth(0.4)
        c.rect(lx, h - 9, 7, 6, stroke=1, fill=1)
        text(c, lx + 10, h - 8, lab, 6.2)
        lx += 22 + il.pdfmetrics.stringWidth(lab, "Body", 6.2)


# ------------------------------------------------------------------ wrappers
DRAW = {"v60": draw_v60, "chemex": draw_chemex, "kalita": draw_kalita, "clever": draw_clever,
        "french": draw_french_press, "aeropress": draw_aeropress, "cold": draw_cold_brew,
        "siphon": draw_siphon, "cezve": draw_cezve, "phin": draw_phin, "batch": draw_batch,
        "moka": draw_moka, "espresso": draw_espresso, "kaapi": draw_kaapi, "davara": draw_davara}


def paint(c, key, x, y, w, h):
    s = min(w / 100, h / 120)
    c.saveState()
    c.translate(x + (w - 100 * s) / 2, y + (h - 120 * s) / 2)
    c.scale(s, s)
    DRAW[key](c)
    c.restoreState()


def icon(key, w, h, bg=True):
    def draw(c, W, H):
        if bg:
            c.setFillColor(HX("#F7F1E8"))
            c.roundRect(0, 0, W, H, 6, stroke=0, fill=1)
        paint(c, key, 4, 4, W - 8, H - 8)
    return CanvasFigure(w, h, draw)


def strip(items, w, h):
    """items: [(key, caption)] -> row of icons with captions underneath."""
    def draw(c, W, H):
        n = len(items)
        cw = W / n
        for i, (key, cap) in enumerate(items):
            x = i * cw
            c.setFillColor(HX("#F7F1E8"))
            c.roundRect(x + 3, 14, cw - 6, H - 14, 6, stroke=0, fill=1)
            paint(c, key, x + 6, 17, cw - 12, H - 20)
            text(c, x + cw / 2, 3, cap, 7.0, "Body-Bold", il.ROAST, "middle")
    return CanvasFigure(w, h, draw)


def figure(fn, w, h):
    return CanvasFigure(w, h, fn)
