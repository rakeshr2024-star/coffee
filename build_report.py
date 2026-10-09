#!/usr/bin/env python3
"""Build Final_Coff.pdf: a novice's field guide to judging coffee quality, with an
Indian sourcing lens, a raw-material cost model for an Ahmedabad cafe, and ratings
of Ahmedabad coffee places.  Pure ReportLab (platypus + graphics), no other deps.

Run:  python3 build_report.py            -> writes Final_Coff.pdf next to this file
"""
import math
import os

from reportlab.graphics.shapes import (Circle, Drawing, Group, Line, Polygon,
                                       Rect, String, Wedge)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame,
                                KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Final_Coff.pdf")

# --------------------------------------------------------------------------- fonts
FONT_DIR = "/usr/share/fonts/truetype/crosextra"
pdfmetrics.registerFont(TTFont("Body", f"{FONT_DIR}/Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", f"{FONT_DIR}/Carlito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Body-Italic", f"{FONT_DIR}/Carlito-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Body-BoldItalic", f"{FONT_DIR}/Carlito-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("Head", f"{FONT_DIR}/Caladea-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Head-Reg", f"{FONT_DIR}/Caladea-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Head-Italic", f"{FONT_DIR}/Caladea-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sym", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold",
                              italic="Body-Italic", boldItalic="Body-BoldItalic")
pdfmetrics.registerFontFamily("Head", normal="Head-Reg", bold="Head",
                              italic="Head-Italic", boldItalic="Head")

# --------------------------------------------------------------------------- palette
HX = colors.HexColor
ESPRESSO = HX("#2B1A12")
ROAST = HX("#6F4E37")
CARAMEL = HX("#C68B59")
CREMA = HX("#F3E5D0")
PAPER = HX("#FFFDF9")
TEAL = HX("#1B998B")
SAFFRON = HX("#F29E4C")
LEAF = HX("#3A7D44")
BERRY = HX("#C0392B")
PLUM = HX("#6A4C93")
SKY = HX("#2E86AB")
GOLD = HX("#E9C46A")
INK = HX("#2D2A26")
MUTED = HX("#7A6F66")
RULE = HX("#E6DCCF")
ZEBRA = HX("#FAF4EC")
SERIES = [SKY, BERRY, TEAL, SAFFRON, PLUM, LEAF, CARAMEL, GOLD]

PAGE_W, PAGE_H = A4
MARGIN = 16 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

# --------------------------------------------------------------------------- styles
BODY = ParagraphStyle("body", fontName="Body", fontSize=9.4, leading=12.6,
                      textColor=INK, spaceAfter=4)
BODY_SM = ParagraphStyle("bodysm", parent=BODY, fontSize=8.4, leading=11)
LEAD = ParagraphStyle("lead", parent=BODY, fontSize=10.6, leading=14.5,
                      textColor=ROAST, fontName="Body-Italic", spaceAfter=6)
H2 = ParagraphStyle("h2", fontName="Head", fontSize=12.5, leading=15,
                    textColor=ESPRESSO, spaceBefore=7, spaceAfter=3.5)
H3 = ParagraphStyle("h3", fontName="Body-Bold", fontSize=9.6, leading=12,
                    textColor=ROAST, spaceBefore=4, spaceAfter=2)
CAPTION = ParagraphStyle("cap", fontName="Body-Italic", fontSize=7.6, leading=9.6,
                         textColor=MUTED, alignment=TA_CENTER, spaceBefore=1,
                         spaceAfter=6)
CELL = ParagraphStyle("cell", fontName="Body", fontSize=7.7, leading=9.4,
                      textColor=INK)
CELL_B = ParagraphStyle("cellb", parent=CELL, fontName="Body-Bold")
CELL_C = ParagraphStyle("cellc", parent=CELL, alignment=TA_CENTER)
HEAD_CELL = ParagraphStyle("hcell", fontName="Body-Bold", fontSize=7.8,
                           leading=9.4, textColor=colors.white)
HEAD_CELL_C = ParagraphStyle("hcellc", parent=HEAD_CELL, alignment=TA_CENTER)
BULLET = ParagraphStyle("bullet", parent=BODY, leftIndent=10, bulletIndent=1,
                        spaceAfter=2.2)
SOURCE = ParagraphStyle("src", fontName="Body", fontSize=7.2, leading=9,
                        textColor=MUTED, spaceAfter=1.5)


def P(text, style=BODY):
    return Paragraph(text, style)


def bullets(items, style=BULLET, color="#C68B59"):
    return [Paragraph(f'<font name="Sym" size="6.5" color="{color}">\u25A0</font>&nbsp;&nbsp;{t}',
                      style) for t in items]


# --------------------------------------------------------------------------- score colours
def score_color(s):
    if s >= 9:
        return HX("#1B998B")
    if s >= 8:
        return HX("#52B788")
    if s >= 7:
        return HX("#E9C46A")
    if s >= 6:
        return HX("#F4A261")
    return HX("#E76F51")


def score_text_color(s):
    return colors.white if (s >= 9 or s < 6) else INK


# --------------------------------------------------------------------------- flowables
class SectionBand(Flowable):
    """Full-width coloured band with a numbered roundel, title and subtitle."""

    def __init__(self, num, title, subtitle, color=ROAST):
        super().__init__()
        self.num, self.title, self.subtitle, self.color = num, title, subtitle, color
        self.height = 17 * mm

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(self.color)
        c.roundRect(0, 0, self.width, self.height, 4, stroke=0, fill=1)
        c.setFillColor(colors.Color(1, 1, 1, alpha=0.12))
        c.circle(self.width - 18 * mm, self.height / 2, 14 * mm, stroke=0, fill=1)
        c.circle(self.width - 8 * mm, self.height, 9 * mm, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.circle(9.5 * mm, self.height / 2, 5.6 * mm, stroke=0, fill=1)
        c.setFillColor(self.color)
        c.setFont("Head", 13)
        c.drawCentredString(9.5 * mm, self.height / 2 - 4.4, str(self.num))
        c.setFillColor(colors.white)
        c.setFont("Head", 16)
        c.drawString(19 * mm, self.height / 2 + 0.6 * mm, self.title)
        c.setFont("Body-Italic", 9)
        c.drawString(19 * mm, self.height / 2 - 4.6 * mm, self.subtitle)
        c.restoreState()


def section(num, title, subtitle, color=ROAST):
    return [SectionBand(num, title, subtitle, color), Spacer(1, 6)]


def callout(title, body_items, color=TEAL, bg=None, width=CONTENT_W):
    bg = bg or HX("#EEF8F6")
    content = [P(f'<font name="Body-Bold" color="{color.hexval().replace("0x", "#")}">'
                 f'{title}</font>', ParagraphStyle("ct", parent=BODY, spaceAfter=2))]
    for item in body_items:
        content.append(P(item, ParagraphStyle("cb", parent=BODY_SM, spaceAfter=1.5)))
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3.2, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def data_table(header, rows, col_widths, head_color=ROAST, score_cols=(),
               center_cols=(), bold_first=True, font_size=None, zebra=True, head_size=None):
    """header: list of str; rows: list of lists (str or float for score cols)."""
    cell = CELL if font_size is None else ParagraphStyle("c2", parent=CELL, fontSize=font_size,
                                                         leading=font_size + 1.8)
    cell_b = ParagraphStyle("c2b", parent=cell, fontName="Body-Bold")
    cell_c = ParagraphStyle("c2c", parent=cell, alignment=TA_CENTER)
    hl = HEAD_CELL if head_size is None else ParagraphStyle(
        "hc2", parent=HEAD_CELL, fontSize=head_size, leading=head_size + 1.6)
    hc = ParagraphStyle("hc2c", parent=hl, alignment=TA_CENTER)
    data = [[P(h, hc if i in center_cols or i in score_cols else hl)
             for i, h in enumerate(header)]]
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), head_color),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
    ]
    for r, row in enumerate(rows, start=1):
        out = []
        if zebra and r % 2 == 0:
            style.append(("BACKGROUND", (0, r), (-1, r), ZEBRA))
        for c, v in enumerate(row):
            if c in score_cols and isinstance(v, (int, float)):
                txt = f"{v:g}" if isinstance(v, int) or v == int(v) else f"{v:.1f}"
                out.append(P(f'<font name="Body-Bold">{txt}</font>',
                             ParagraphStyle("sc", parent=cell_c,
                                            textColor=score_text_color(v))))
                style.append(("BACKGROUND", (c, r), (c, r), score_color(v)))
            elif c == 0 and bold_first:
                out.append(P(str(v), cell_b))
            elif c in center_cols or c in score_cols:
                out.append(P(str(v), cell_c))
            else:
                out.append(P(str(v), cell))
        data.append(out)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


def fig(drawing, caption):
    return KeepTogether([drawing, P(caption, CAPTION)])


# --------------------------------------------------------------------------- drawings
def txt(x, y, s, size=8, font="Body", color=INK, anchor="start"):
    return String(x, y, s, fontName=font, fontSize=size, fillColor=color,
                  textAnchor=anchor)


def seed_to_cup():
    w, h = CONTENT_W, 98
    d = Drawing(w, h)
    stages = [
        ("Genetics", "variety &\nspecies", LEAF),
        ("Terroir", "altitude, soil,\nshade, climate", HX("#4E9F3D")),
        ("Harvest", "ripe-only\nhand picking", HX("#8AB17D")),
        ("Processing", "washed, natural,\nhoney, anaerobic", GOLD),
        ("Drying &\nStorage", "10-12% moisture,\nstable aw", SAFFRON),
        ("Roasting", "time, temp,\ndevelopment", CARAMEL),
        ("Freshness", "days off roast,\npackaging", ROAST),
        ("Brewing", "grind, ratio,\nwater, temp", ESPRESSO),
    ]
    n = len(stages)
    gap = 3
    cw = (w - gap * (n - 1)) / n
    top = h - 6
    for i, (name, sub, col) in enumerate(stages):
        x = i * (cw + gap)
        tip = 8
        pts = [x, top - 44, x + cw, top - 44, x + cw + tip, top - 22, x + cw, top,
               x, top]
        if i > 0:
            pts += [x + tip, top - 22]
        d.add(Polygon(pts, fillColor=col, strokeColor=None))
        lines = name.split("\n")
        for j, ln in enumerate(lines):
            d.add(txt(x + cw / 2 + 3, top - 18 - j * 10 + (5 if len(lines) > 1 else 0),
                      ln, 8.6, "Body-Bold", colors.white, "middle"))
        for j, ln in enumerate(sub.split("\n")):
            d.add(txt(x + cw / 2 + 2, top - 57 - j * 9, ln, 7.1, "Body", INK, "middle"))
    # bracket annotations
    def bracket(x0, x1, y, label, col):
        d.add(Line(x0, y, x1, y, strokeColor=col, strokeWidth=1.4))
        d.add(Line(x0, y, x0, y + 4, strokeColor=col, strokeWidth=1.4))
        d.add(Line(x1, y, x1, y + 4, strokeColor=col, strokeWidth=1.4))
        d.add(txt((x0 + x1) / 2, y - 9, label, 7.6, "Body-Bold", col, "middle"))
    bracket(2, 5 * (cw + gap) - gap - 2, 16, "QUALITY IS CREATED  (farm & mill: sets the ceiling)", LEAF)
    bracket(5 * (cw + gap) + 2, 7 * (cw + gap) - gap - 2, 16, "PRESERVED (roaster)", CARAMEL)
    bracket(7 * (cw + gap) + 2, w - 2, 16, "KEPT / LOST (you)", ESPRESSO)
    return d


def impact_chart():
    items = [("Variety (genetics)", 9), ("Altitude & terroir", 9), ("Ripe-cherry picking", 10),
             ("Processing & drying", 9), ("Green storage", 7), ("Roast skill", 9),
             ("Freshness (days off roast)", 8), ("Grinder quality", 8), ("Brew recipe", 7),
             ("Water chemistry", 7)]
    w, h = CONTENT_W * 0.52, 132
    d = Drawing(w, h)
    lab_w = 98
    bar_w = w - lab_w - 22
    row_h = (h - 14) / len(items)
    for i, (lab, v) in enumerate(items):
        y = h - 14 - (i + 1) * row_h + 3
        d.add(txt(lab_w - 4, y + 2.5, lab, 7.4, "Body", INK, "end"))
        d.add(Rect(lab_w, y, bar_w, row_h - 5, fillColor=HX("#F1EAE0"), strokeColor=None))
        d.add(Rect(lab_w, y, bar_w * v / 10, row_h - 5, fillColor=score_color(v),
                   strokeColor=None))
        d.add(txt(lab_w + bar_w * v / 10 + 3, y + 2.5, f"{v}", 7.4, "Body-Bold", INK))
    d.add(txt(lab_w, h - 8, "Impact on the final cup (my rating, /10)", 7.8, "Body-Bold", ROAST))
    return d


def sca_ladder():
    w, h = CONTENT_W * 0.44, 150
    d = Drawing(w, h)
    bands = [
        ("90-100", "Outstanding", "Competition lots, top Geishas", HX("#1B998B")),
        ("85-89.99", "Excellent", "Top estate micro-lots", HX("#52B788")),
        ("80-84.99", "Very good", "Entry to 'specialty'", HX("#E9C46A")),
        ("70-79.99", "Commercial", "Most supermarket coffee", HX("#F4A261")),
        ("< 70", "Below grade", "Defective / exchange-reject", HX("#E76F51")),
    ]
    bh = (h - 16) / len(bands)
    for i, (rng, name, eg, col) in enumerate(bands):
        y = h - 16 - (i + 1) * bh
        inset = i * 7
        d.add(Rect(inset, y + 1.5, w - 2 * inset, bh - 3, fillColor=col, strokeColor=None,
                   rx=3, ry=3))
        tc = colors.white if i in (0, 4) else INK
        d.add(txt(inset + 6, y + bh / 2 + 1, rng, 9, "Head", tc))
        d.add(txt(inset + 58, y + bh / 2 + 1.5, name, 8.2, "Body-Bold", tc))
        d.add(txt(inset + 58, y + bh / 2 - 7.5, eg, 6.8, "Body", tc))
    d.add(txt(w / 2, h - 9, "SCA 100-point cup score", 7.8, "Body-Bold", ROAST, "middle"))
    return d


def roast_spectrum():
    w, h = CONTENT_W, 150
    d = Drawing(w, h)
    x0, x1 = 4, w - 4
    # ---- row 1: roast timeline (minutes) with phases and crack markers
    tmax = 13.0

    def xt(t):
        return x0 + t / tmax * (x1 - x0)
    y1 = h - 40
    phases = [(0, 5, "DRYING  (green → yellow, to ~150-160°C)", HX("#8DB86A")),
              (5, 9, "MAILLARD  (browning, aromas form)", CARAMEL),
              (9, 11.2, "DEVELOPMENT", ROAST),
              (11.2, 13, "TO DARK", ESPRESSO)]
    for a, b, lab, col in phases:
        d.add(Rect(xt(a) + 1, y1, xt(b) - xt(a) - 2, 16, fillColor=col, strokeColor=None,
                   rx=3, ry=3))
        d.add(txt((xt(a) + xt(b)) / 2, y1 + 5.2, lab, 7, "Body-Bold", colors.white, "middle"))
    for t, lab in [(9, "1st crack ~196-205°C"), (12, "2nd crack ~224-230°C")]:
        d.add(Line(xt(t), y1 - 3, xt(t), y1 + 22, strokeColor=BERRY, strokeWidth=1.2,
                   strokeDashArray=[2, 2]))
        d.add(txt(xt(t), y1 + 25, lab, 7.2, "Body-Bold", BERRY, "middle"))
    for m in range(0, 14):
        d.add(Line(xt(m), y1 - 5, xt(m), y1 - 2, strokeColor=MUTED, strokeWidth=0.6))
        d.add(txt(xt(m), y1 - 12, f"{m}", 6.2, "Body", MUTED, "middle"))
    d.add(txt(x0, h - 8, "A typical 9-14 minute roast (minutes)  •  development ≈ 15-25% of total time",
              7.6, "Body-Bold", ROAST))
    # ---- row 2: roast level swatches
    levels = [("Green", "raw seed", "grassy, hay", "~10-12% moisture", HX("#8DB86A"), INK),
              ("Light", "200-212°C", "Agtron 70-85", "bright, floral", HX("#C99A5B"), INK),
              ("Medium", "212-222°C", "Agtron 55-70", "caramel, balanced", HX("#9C6635"),
               colors.white),
              ("Medium-dark", "222-228°C", "Agtron 45-55", "chocolate, spice", HX("#6B4024"),
               colors.white),
              ("Dark", "228-240°C", "Agtron 25-45", "smoky, bitter-sweet", HX("#2E1A10"),
               colors.white)]
    n = len(levels)
    gap = 6
    sw = (x1 - x0 - gap * (n - 1)) / n
    y2 = 26
    for i, (nm, temp, ag, fl, col, tc) in enumerate(levels):
        x = x0 + i * (sw + gap)
        d.add(Rect(x, y2, sw, 44, fillColor=col, strokeColor=None, rx=4, ry=4))
        # bean glyph
        bx, by = x + 16, y2 + 22
        d.add(Circle(bx, by, 7, fillColor=colors.Color(1, 1, 1, alpha=0.22), strokeColor=None))
        d.add(txt(x + 30, y2 + 31, nm, 8.6, "Body-Bold", tc))
        d.add(txt(x + 30, y2 + 21, temp, 7, "Body", tc))
        d.add(txt(x + 30, y2 + 12, ag, 7, "Body", tc))
        d.add(txt(x + 30, y2 + 3, fl, 6.8, "Body-Italic", tc))
    # ---- flavour arrow
    ay = 10
    d.add(Line(x0, ay, x1 - 6, ay, strokeColor=INK, strokeWidth=0.8))
    d.add(Polygon([x1 - 6, ay + 3, x1, ay, x1 - 6, ay - 3], fillColor=INK, strokeColor=None))
    d.add(txt(x0 + (x1 - x0) * 0.28, ay + 3.5, "more ORIGIN character: acidity, florals, fruit", 7,
              "Body-Italic", TEAL, "middle"))
    d.add(txt(x0 + (x1 - x0) * 0.75, ay + 3.5, "more ROAST character: chocolate → smoke, body, bitterness",
              7, "Body-Italic", ROAST, "middle"))
    return d


def freshness_timeline():
    w, h = CONTENT_W, 104
    d = Drawing(w, h)
    x0, x1 = 78, w - 8
    maxd = 56

    def xd(day):
        return x0 + day / maxd * (x1 - x0)
    c_rest, c_open, c_peak, c_fade, c_stale = (HX("#BFC9CA"), HX("#8ED1C6"), TEAL, GOLD,
                                               HX("#E76F51"))
    rows = [
        ("Filter / pour-over", [(0, 3, "rest", c_rest), (3, 7, "opening", c_open),
                                (7, 28, "PEAK", c_peak), (28, 45, "fading", c_fade),
                                (45, 56, "stale", c_stale)]),
        ("Espresso", [(0, 7, "too gassy", c_rest), (7, 12, "settling", c_open),
                      (12, 35, "PEAK", c_peak), (35, 48, "fading", c_fade),
                      (48, 56, "stale", c_stale)]),
        ("After opening", [(0, 21, "use within ~2-3 weeks", HX("#9AD0A5")),
                           (21, 56, "aromatics oxidise quickly", HX("#F4A261"))]),
    ]
    rh = 16
    top = h - 20
    for i, (lab, segs) in enumerate(rows):
        y = top - (i + 1) * (rh + 5) + 5
        d.add(txt(x0 - 5, y + 5, lab, 7.6, "Body-Bold", INK, "end"))
        for a, b, s_, col in segs:
            wseg = xd(b) - xd(a) - 1
            d.add(Rect(xd(a) + 0.5, y, wseg, rh, fillColor=col, strokeColor=None, rx=2, ry=2))
            tw = pdfmetrics.stringWidth(s_, "Body-Bold", 6.8)
            if tw + 4 < wseg:
                tc = colors.white if col in (c_peak, c_stale) else INK
                d.add(txt((xd(a) + xd(b)) / 2, y + 5, s_, 6.8,
                          "Body-Bold" if s_ == "PEAK" else "Body", tc, "middle"))
    ya = top - 3 * (rh + 5) - 2
    for dday in range(0, 57, 7):
        d.add(Line(xd(dday), ya, xd(dday), ya + 3, strokeColor=MUTED, strokeWidth=0.6))
        d.add(txt(xd(dday), ya - 8, f"day {dday}", 6.4, "Body", MUTED, "middle"))
    d.add(txt(x0, h - 9, "Days after the roast date (whole beans, sealed valve bag)",
              7.4, "Body-Bold", ROAST))
    lx = x1
    for lab, col in [("stale", c_stale), ("fading", c_fade), ("peak", c_peak),
                      ("opening up", c_open), ("resting / degassing", c_rest)]:
        tw = pdfmetrics.stringWidth(lab, "Body", 6.6)
        lx -= tw + 16
        d.add(Rect(lx, h - 10, 8, 6, fillColor=col, strokeColor=None))
        d.add(txt(lx + 10, h - 9.5, lab, 6.6, "Body", MUTED))
    return d


def radar(profiles, title, w=CONTENT_W / 2 - 4, h=180):
    axes = ["Acidity", "Body", "Sweetness", "Fruit/Floral", "Choc/Nut", "Earthy/Spice"]
    d = Drawing(w, h)
    cx, cy, r = w / 2, h / 2 + 2, min(w, h) / 2 - 34
    n = len(axes)

    def pt(i, v):
        a = math.pi / 2 - 2 * math.pi * i / n
        return cx + r * v / 10 * math.cos(a), cy + r * v / 10 * math.sin(a)
    for ring in (2, 4, 6, 8, 10):
        pts = []
        for i in range(n):
            pts += list(pt(i, ring))
        d.add(Polygon(pts, fillColor=None, strokeColor=RULE, strokeWidth=0.6))
    for i, ax in enumerate(axes):
        x, y = pt(i, 10)
        d.add(Line(cx, cy, x, y, strokeColor=RULE, strokeWidth=0.6))
        lx, ly = pt(i, 11.7)
        anchor = "middle" if abs(lx - cx) < 5 else ("start" if lx > cx else "end")
        d.add(txt(lx, ly - 3, ax, 7, "Body-Bold", MUTED, anchor))
    for k, (name, vals, col) in enumerate(profiles):
        pts = []
        for i, v in enumerate(vals):
            pts += list(pt(i, v))
        d.add(Polygon(pts, fillColor=col, fillOpacity=0.13, strokeColor=col, strokeWidth=1.5))
        for i, v in enumerate(vals):
            x, y = pt(i, v)
            d.add(Circle(x, y, 1.7, fillColor=col, strokeColor=None))
    # legend
    lx = 6
    for k, (name, vals, col) in enumerate(profiles):
        xx = lx + (k % 2) * (w / 2)
        yy = 10 - (k // 2) * 9
        d.add(Rect(xx, yy, 8, 5, fillColor=col, strokeColor=None))
        d.add(txt(xx + 11, yy, name, 7, "Body", INK))
    d.add(txt(w / 2, h - 8, title, 8.4, "Head", ESPRESSO, "middle"))
    return d


def grind_scale():
    w, h = CONTENT_W, 128
    d = Drawing(w, h)
    x0, x1 = 78, w - 8
    maxu = 1400

    def xu(u):
        return x0 + u / maxu * (x1 - x0)
    methods = [("Turkish", 40, 100, PLUM), ("Espresso", 200, 300, ESPRESSO),
               ("Moka pot", 300, 500, ROAST), ("Filter kaapi", 350, 550, SAFFRON),
               ("AeroPress", 400, 700, SKY), ("V60 pour-over", 500, 800, TEAL),
               ("Chemex", 700, 900, LEAF), ("French press", 900, 1200, CARAMEL),
               ("Cold brew", 1000, 1400, HX("#5DADE2"))]
    rh = (h - 26) / len(methods)
    for i, (lab, a, b, col) in enumerate(methods):
        y = h - 12 - (i + 1) * rh
        d.add(txt(x0 - 5, y + rh / 2 - 2.5, lab, 7.4, "Body-Bold", INK, "end"))
        d.add(Rect(x0, y + 1.5, x1 - x0, rh - 3, fillColor=HX("#F7F1E8"), strokeColor=None))
        d.add(Rect(xu(a), y + 1.5, xu(b) - xu(a), rh - 3, fillColor=col, strokeColor=None,
                   rx=2, ry=2))
        d.add(txt(xu(b) + 3, y + rh / 2 - 2.5, f"{a}-{b} µm", 6.6, "Body", MUTED))
    for u in range(0, 1401, 200):
        d.add(Line(xu(u), 12, xu(u), 15, strokeColor=MUTED, strokeWidth=0.6))
        d.add(txt(xu(u), 4, f"{u}", 6.4, "Body", MUTED, "middle"))
    d.add(txt(x0 - 5, 4, "particle size (µm)", 6.4, "Body-Italic", MUTED, "end"))
    d.add(txt(xu(700), h - 8, "finer = more surface = faster extraction  →  coarser for longer contact",
              7.2, "Body-Italic", ROAST, "middle"))
    return d


def donut(values, labels, cols, title, w, h, centre_txt, centre_sub):
    d = Drawing(w, h)
    cx, cy, r = w * 0.30, h / 2 - 4, min(w * 0.27, h / 2 - 16)
    total = sum(values)
    start = 90
    for v, col in zip(values, cols):
        ext = 360 * v / total
        d.add(Wedge(cx, cy, r, start - ext, start, fillColor=col, strokeColor=colors.white,
                    strokeWidth=1.2))
        start -= ext
    d.add(Circle(cx, cy, r * 0.56, fillColor=PAPER, strokeColor=None))
    d.add(txt(cx, cy + 1, centre_txt, 10.5, "Head", ESPRESSO, "middle"))
    d.add(txt(cx, cy - 8, centre_sub, 5.8, "Body", MUTED, "middle"))
    lx = w * 0.62
    for i, (v, lab, col) in enumerate(zip(values, labels, cols)):
        y = h - 32 - i * 15
        d.add(Rect(lx, y, 8, 8, fillColor=col, strokeColor=None))
        d.add(txt(lx + 12, y + 1, f"{lab}", 7.6, "Body-Bold", INK))
        d.add(txt(lx + 12, y - 7, f"{v:,.0f} t  ({100 * v / total:.0f}%)", 6.8, "Body", MUTED))
    d.add(txt(w / 2, h - 10, title, 8.4, "Head", ESPRESSO, "middle"))
    return d


def hbar_ranges(items, title, w, h, unit_fmt, maxv, label_w=120, note=None):
    """items: (label, lo, hi, colour, value_label)."""
    d = Drawing(w, h)
    x0, x1 = label_w, w - 60
    top = h - 16
    rh = (top - 14) / len(items)
    for i, (lab, lo, hi, col, vl) in enumerate(items):
        y = top - (i + 1) * rh
        d.add(txt(x0 - 5, y + rh / 2 - 2.5, lab, 7.3, "Body", INK, "end"))
        d.add(Rect(x0, y + 2, x1 - x0, rh - 4, fillColor=HX("#F7F1E8"), strokeColor=None))
        xl = x0 + lo / maxv * (x1 - x0)
        xh = x0 + hi / maxv * (x1 - x0)
        d.add(Rect(x0, y + 2, xl - x0, rh - 4, fillColor=col, fillOpacity=0.35, strokeColor=None))
        d.add(Rect(xl, y + 2, max(xh - xl, 2), rh - 4, fillColor=col, strokeColor=None))
        d.add(txt(xh + 4, y + rh / 2 - 2.5, vl, 7, "Body-Bold", INK))
    for v in range(0, int(maxv) + 1, int(maxv / 5)):
        x = x0 + v / maxv * (x1 - x0)
        d.add(Line(x, 10, x, 13, strokeColor=MUTED, strokeWidth=0.6))
        d.add(txt(x, 2, unit_fmt(v), 6.3, "Body", MUTED, "middle"))
    d.add(txt(4, h - 9, title, 8.8, "Body-Bold", ESPRESSO))
    if note:
        d.add(txt(w - 4, h - 9, note, 6.6, "Body-Italic", MUTED, "end"))
    return d


def stacked_scenarios(rows, w, h):
    """rows: (label, [coffee, milk, sweet, pack, other])"""
    comp_names = ["Coffee", "Milk", "Sugar & syrups", "Cups & packaging", "Water, filters, chemicals"]
    comp_cols = [ROAST, HX("#8ECAE6"), GOLD, SAFFRON, HX("#A3B18A")]
    d = Drawing(w, h)
    x0, x1 = 150, w - 52
    top = h - 30
    maxv = math.ceil(max(sum(c) for _, c in rows) / 100000) * 100000
    rh = (top - 16) / len(rows)
    for i, (lab, comps) in enumerate(rows):
        y = top - (i + 1) * rh
        d.add(txt(x0 - 5, y + rh / 2 - 2.5, lab, 7.3, "Body-Bold", INK, "end"))
        x = x0
        for v, col in zip(comps, comp_cols):
            ww = v / maxv * (x1 - x0)
            d.add(Rect(x, y + 2.5, ww, rh - 5, fillColor=col, strokeColor=colors.white,
                       strokeWidth=0.5))
            x += ww
        d.add(txt(x + 4, y + rh / 2 - 2.5, f"₹{sum(comps) / 100000:.2f} L", 7.2, "Body-Bold", INK))
    for v in range(0, maxv + 1, 100000 if maxv > 400000 else 50000):
        x = x0 + v / maxv * (x1 - x0)
        d.add(Line(x, 12, x, 15, strokeColor=MUTED, strokeWidth=0.6))
        d.add(txt(x, 4, f"₹{v / 100000:.1f}L", 6.3, "Body", MUTED, "middle"))
    lx = 6
    for k, (nm, col) in enumerate(zip(comp_names, comp_cols)):
        xx = lx + k * (w / 5.1)
        d.add(Rect(xx, h - 12, 8, 7, fillColor=col, strokeColor=None))
        d.add(txt(xx + 11, h - 11, nm, 7, "Body", INK))
    return d


def cafe_score_chart(cafes, w, h):
    d = Drawing(w, h)
    x0, x1 = 128, w - 26
    top = h - 6
    rh = (top - 14) / len(cafes)
    for i, (name, score) in enumerate(cafes):
        y = top - (i + 1) * rh
        d.add(txt(x0 - 5, y + rh / 2 - 2.5, name, 7.2, "Body-Bold", INK, "end"))
        d.add(Rect(x0, y + 2, x1 - x0, rh - 4, fillColor=HX("#F7F1E8"), strokeColor=None))
        ww = (score - 5) / 5 * (x1 - x0)
        d.add(Rect(x0, y + 2, ww, rh - 4, fillColor=score_color(score), strokeColor=None,
                   rx=2, ry=2))
        d.add(txt(x0 + ww + 3, y + rh / 2 - 2.5, f"{score:.1f}", 7.2, "Body-Bold", INK))
    for v in range(5, 11):
        x = x0 + (v - 5) / 5 * (x1 - x0)
        d.add(Line(x, 10, x, 13, strokeColor=MUTED, strokeWidth=0.6))
        d.add(txt(x, 2, str(v), 6.3, "Body", MUTED, "middle"))
    return d


def number_tiles(items, cols=4):
    cw = CONTENT_W / cols
    big = ParagraphStyle("nt_big", fontName="Body-Bold", fontSize=13.5, leading=15, textColor=ESPRESSO)
    small = ParagraphStyle("nt_small", fontName="Body", fontSize=7.4, leading=9, textColor=MUTED)
    rows, style = [], [("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                       ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    for r in range(0, len(items), cols):
        row = []
        for c, (b, sml, col) in enumerate(items[r:r + cols]):
            row.append([P(b, big), P(sml, small)])
            rr = r // cols
            style += [("BACKGROUND", (c, rr), (c, rr), HX("#F7F1E8")),
                      ("LINEBEFORE", (c, rr), (c, rr), 3, col),
                      ("LINEBELOW", (c, rr), (c, rr), 3, PAPER),
                      ("LINEAFTER", (c, rr), (c, rr), 3, PAPER)]
        rows.append(row)
    t = Table(rows, colWidths=[cw] * cols)
    t.setStyle(TableStyle(style))
    return t


def process_map(w=CONTENT_W * 0.56, h=158):
    """Bubble map: clarity (x) vs fruit/ferment intensity (y); bubble = typical price premium."""
    d = Drawing(w, h)
    x0, y0, x1, y1 = 34, 22, w - 10, h - 16
    d.add(Rect(x0, y0, x1 - x0, y1 - y0, fillColor=HX("#FBF6EF"), strokeColor=RULE, strokeWidth=0.6))
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    d.add(Line(mx, y0, mx, y1, strokeColor=RULE, strokeWidth=0.6, strokeDashArray=[2, 2]))
    d.add(Line(x0, my, x1, my, strokeColor=RULE, strokeWidth=0.6, strokeDashArray=[2, 2]))
    for qx, qy, lab in [(x0 + 4, y1 - 9, "wild & fruity"), (x1 - 4, y1 - 9, "fruity yet clean"),
                        (x0 + 4, y0 + 4, "earthy & heavy"), (x1 - 4, y0 + 4, "clean & classic")]:
        d.add(txt(qx, qy, lab, 6.6, "Body-Italic", MUTED, "start" if qx < mx else "end"))

    def pos(cx, cy):
        return x0 + cx / 10 * (x1 - x0), y0 + cy / 10 * (y1 - y0)
    pts = [("Washed", 8.6, 3.0, 0, TEAL), ("Honey", 6.8, 5.4, 18, GOLD),
           ("Natural", 5.0, 7.4, 10, SAFFRON), ("Anaerobic / carbonic", 3.4, 9.0, 90, BERRY),
           ("Monsooned", 4.2, 1.8, 15, ROAST), ("Wet-hulled", 2.2, 2.8, 5, LEAF)]
    for name, cx, cy, prem, col in pts:
        x, y = pos(cx, cy)
        r = 5 + prem / 9
        d.add(Circle(x, y, r, fillColor=col, fillOpacity=0.85, strokeColor=colors.white, strokeWidth=1))
        anchor = "end" if cx > 7.5 else "start"
        dx = -(r + 3) if anchor == "end" else r + 3
        d.add(txt(x + dx, y - 2.5, name, 7.4, "Body-Bold", INK, anchor))
    d.add(txt((x0 + x1) / 2, 6, "clarity / cleanliness  \u2192", 7, "Body-Bold", MUTED, "middle"))
    g = Group(txt(0, 0, "fruit & ferment intensity  \u2192", 7, "Body-Bold", MUTED, "middle"))
    g.transform = (0, 1, -1, 0, 14, (y0 + y1) / 2)
    d.add(g)
    d.add(txt(x0, h - 8, "Processing flavour map (bubble size = typical price premium)", 7.8,
              "Body-Bold", ROAST))
    return d


def legend_strip():
    w, h = CONTENT_W, 22
    d = Drawing(w, h)
    items = [(9.5, "9-10  Exceptional"), (8.5, "8-8.9  Excellent"), (7.5, "7-7.9  Good"),
             (6.5, "6-6.9  Fair / niche"), (5, "< 6  Weak for this purpose")]
    d.add(txt(0, 8, "Rating scale used throughout:", 7.6, "Body-Bold", ROAST))
    x = 118
    for s, lab in items:
        d.add(Rect(x, 5, 12, 10, fillColor=score_color(s), strokeColor=None, rx=2, ry=2))
        d.add(txt(x + 16, 8, lab, 7.4, "Body", INK))
        x += (w - 118) / 5
    return d


# --------------------------------------------------------------------------- page decorations
def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(ESPRESSO)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # decorative crema rings (a coffee cup seen from above)
    cx, cy = PAGE_W * 0.70, PAGE_H * 0.445
    for r, col, a in [(140, CARAMEL, 0.18), (114, CREMA, 0.10), (94, ROAST, 0.9),
                      (80, HX("#3B2416"), 1), (56, CARAMEL, 0.25), (32, CREMA, 0.18)]:
        c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=a))
        c.circle(cx, cy, r, stroke=0, fill=1)
    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.5))
    c.setLineWidth(1)
    c.circle(cx, cy, 94, stroke=1, fill=0)
    # beans scattered
    def bean(x, y, s, ang, col):
        c.saveState()
        c.translate(x, y)
        c.rotate(ang)
        c.setFillColor(col)
        c.ellipse(-s, -s * 0.66, s, s * 0.66, stroke=0, fill=1)
        c.setStrokeColor(colors.Color(0, 0, 0, alpha=0.45))
        c.setLineWidth(s * 0.12)
        p = c.beginPath()
        p.moveTo(-s * 0.85, 0)
        p.curveTo(-s * 0.3, s * 0.25, s * 0.3, -s * 0.25, s * 0.85, 0)
        c.drawPath(p, stroke=1, fill=0)
        c.restoreState()
    for x, y, s, a, col in [(70, 108, 16, 30, ROAST), (118, 80, 12, -20, CARAMEL),
                            (480, 95, 18, 60, ROAST), (535, 120, 11, 10, HX("#8B5E3C")),
                            (430, 58, 13, -40, CARAMEL), (165, 52, 10, 75, HX("#8B5E3C")),
                            (548, 590, 12, -15, CARAMEL), (300, 88, 9, 40, HX("#8B5E3C"))]:
        bean(x, y, s, a, col)
    # "inside" list on the left
    inside = ["Judging a cup", "Reading the bag & beans", "Species, varieties & origins",
              "Processing", "Roast & freshness", "Brewing methods", "The Indian context",
              "Costs: estate vs other sources", "Ahmedabad café cost model",
              "Ahmedabad coffee places, rated"]
    c.setFont("Body-Bold", 8.5)
    c.setFillColor(SAFFRON)
    c.drawString(MARGIN, 505, "INSIDE")
    for i, t in enumerate(inside):
        y = 488 - i * 15.5
        c.setFillColor(CARAMEL)
        c.setFont("Head", 10)
        c.drawRightString(MARGIN + 14, y, str(i + 1))
        c.setFillColor(CREMA)
        c.setFont("Body", 10)
        c.drawString(MARGIN + 22, y, t)
    # colour stripe (roast spectrum)
    stripe = [HX("#8DB86A"), HX("#D9CC72"), HX("#D39A55"), HX("#A86A38"), HX("#7A4A2A"),
              HX("#4D2F1C"), HX("#24150E")]
    sw = PAGE_W / len(stripe)
    for i, col in enumerate(stripe):
        c.setFillColor(col)
        c.rect(i * sw, PAGE_H - 14, sw + 1, 14, stroke=0, fill=1)
    # title block
    c.setFillColor(SAFFRON)
    c.setFont("Body-Bold", 10)
    c.drawString(MARGIN + 4, PAGE_H - 70, "A NOVICE'S FIELD GUIDE  •  INDIA EDITION  •  OCTOBER 2026")
    c.setFillColor(colors.white)
    c.setFont("Head", 40)
    c.drawString(MARGIN, PAGE_H - 125, "What Makes")
    c.drawString(MARGIN, PAGE_H - 170, "Coffee Great?")
    c.setFont("Head-Italic", 15)
    c.setFillColor(CREMA)
    lines = ["Source, variety, processing, roast, freshness and brewing,",
             "explained and rated. Plus Indian estates, sourcing costs,",
             "an Ahmedabad cafe raw-material model, and the city's",
             "coffee places, compared."]
    for i, ln in enumerate(lines):
        c.drawString(MARGIN, PAGE_H - 200 - i * 19, ln)
    # key number tiles
    tiles = [("80+", "SCA points = specialty"), ("Day 7-30", "peak window after roasting"),
             ("₹24.1-24.8k", "arabica parchment / 50 kg (6 Oct 2026)"),
             (f"₹{RM_LO / 1e5:.1f}-{RM_HI / 1e5:.1f} L", "raw material / month, 200 cups/day")]
    tw = (PAGE_W - 2 * MARGIN - 3 * 8) / 4
    for i, (big, small) in enumerate(tiles):
        x = MARGIN + i * (tw + 8)
        y = 150
        c.setFillColor(colors.Color(1, 1, 1, alpha=0.07))
        c.roundRect(x, y, tw, 62, 6, stroke=0, fill=1)
        c.setFillColor(SERIES[i])
        c.rect(x, y + 58, tw, 4, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Body-Bold", 18)
        c.drawString(x + 8, y + 30, big)
        c.setFont("Body", 7.6)
        c.setFillColor(CREMA)
        c.drawString(x + 8, y + 14, small)
    c.setFont("Body", 8.5)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.6))
    c.drawString(MARGIN, 34, "Desk research compiled from public sources available up to 9 Oct 2026. "
                             "Prices are indicative; ratings are the author's assessments.")
    c.restoreState()


def draw_body(c, doc):
    c.saveState()
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    stripe = [HX("#8DB86A"), HX("#D9CC72"), HX("#D39A55"), HX("#A86A38"), HX("#7A4A2A"),
              HX("#4D2F1C"), HX("#24150E")]
    sw = PAGE_W / len(stripe)
    for i, col in enumerate(stripe):
        c.setFillColor(col)
        c.rect(i * sw, PAGE_H - 5, sw + 1, 5, stroke=0, fill=1)
    c.setFont("Body-Bold", 7.4)
    c.setFillColor(ROAST)
    c.drawString(MARGIN, PAGE_H - 17, "WHAT MAKES COFFEE GREAT?")
    c.setFont("Body", 7.4)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 17, "Field guide • India edition • Oct 2026")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(MARGIN, PAGE_H - 21, PAGE_W - MARGIN, PAGE_H - 21)
    c.line(MARGIN, 22, PAGE_W - MARGIN, 22)
    c.setFillColor(ROAST)
    c.circle(PAGE_W / 2, 13, 7.5, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Body-Bold", 7.5)
    c.drawCentredString(PAGE_W / 2, 10.6, str(doc.page))
    c.setFillColor(MUTED)
    c.setFont("Body", 6.8)
    c.drawString(MARGIN, 11, "Prices indicative, Oct 2026")
    c.drawRightString(PAGE_W - MARGIN, 11, "Ratings = author's assessment (1-10)")
    c.restoreState()


# --------------------------------------------------------------------------- café cost model
MENU_MIX = [  # (drink, share of cups, coffee dose g, milk bought ml incl. steaming loss)
    ("Milk espresso drinks", 0.50, 18, 230), ("Espresso / Americano", 0.12, 18, 0),
    ("Pour-over / manual brew", 0.10, 16, 0), ("Cold brew", 0.13, 22, 0),
    ("South Indian filter kaapi", 0.15, 10, 130)]
CUPS_MONTH = 200 * 30
COFFEE_WASTE = 1.06       # dial-in, purges, spoiled shots
MILK_PER_L = 68           # full-cream, trade price (Amul Gold MRP ₹70/L from May 2026)
KAAPI_BLEND_PER_KG = 750  # commodity Plantation/robusta + chicory 80:20
SWEET_PER_DRINK = 2.5
TAKEAWAY_SHARE, CUP_SET = 0.40, 9
OTHER_MONTH = 9000        # water treatment, filter papers, cleaning chemicals
SCENARIOS = [  # (name, ₹/kg roasted landed for espresso/cold brew/pour-over, pour-over override)
    ("A. Commodity blend (regional roaster)", 950, None),
    ("B. National specialty, wholesale", 1700, None),
    ("C. Estate green, toll-roasted", 1375, None),
    ("D. Estate green, own roaster*", 1225, None),
    ("E. All Indian micro-lots, toll-roasted", 2850, None),
    ("F. Imported specialty, roasted", 4500, None),
    ("Recommended hybrid: C + micro-lot pour-over", 1375, 2850),
]


def compute_model():
    kaapi_kg = CUPS_MONTH * 0.15 * 10 / 1000 * COFFEE_WASTE
    main_kg = sum(CUPS_MONTH * sh * dose / 1000 for m, sh, dose, _ in MENU_MIX
                  if "kaapi" not in m) * COFFEE_WASTE
    pour_kg = CUPS_MONTH * 0.10 * 16 / 1000 * COFFEE_WASTE
    milk_l = sum(CUPS_MONTH * sh * ml / 1000 for _, sh, _, ml in MENU_MIX)
    milk = milk_l * MILK_PER_L
    sweet = CUPS_MONTH * SWEET_PER_DRINK
    pack = CUPS_MONTH * TAKEAWAY_SHARE * CUP_SET
    kaapi = kaapi_kg * KAAPI_BLEND_PER_KG
    out = []
    for name, price, pour_price in SCENARIOS:
        if pour_price:
            coffee = (main_kg - pour_kg) * price + pour_kg * pour_price + kaapi
        else:
            coffee = main_kg * price + kaapi
        comps = [coffee, milk, sweet, pack, OTHER_MONTH]
        out.append(dict(name=name, price=price, pour_price=pour_price, coffee=coffee,
                        comps=comps, total=sum(comps), per_drink=sum(comps) / CUPS_MONTH))
    return dict(scen=out, main_kg=main_kg, kaapi_kg=kaapi_kg, pour_kg=pour_kg, milk_l=milk_l,
                milk=milk)


MODEL = compute_model()
_IND = [x for x in MODEL["scen"] if not x["name"].startswith("F.")]   # Indian-sourced options
RM_LO, RM_HI = min(x["total"] for x in _IND), max(x["total"] for x in _IND)
SHARE_LO = min(100 * x["coffee"] / x["total"] for x in _IND)
SHARE_HI = max(100 * x["coffee"] / x["total"] for x in _IND)
_BY = {x["name"][0]: x for x in MODEL["scen"]}
UPGRADE_LO = _BY["C"]["per_drink"] - _BY["A"]["per_drink"]
UPGRADE_HI = _BY["B"]["per_drink"] - _BY["A"]["per_drink"]


# =========================================================================== CONTENT
def build_story():
    s = []
    s.append(NextPageTemplate("body"))
    s.append(PageBreak())

    # ------------------------------------------------------------------ page 2: summary
    s.append(P("How to use this guide", ParagraphStyle("t", parent=H2, fontSize=17, leading=20)))
    s.append(P("You don't need a trained palate to choose better coffee. You need to know which "
               "signals actually predict a good cup, and which are just marketing. This guide follows "
               "the coffee from seed to cup. At each stage it explains what to look for, gives the "
               "numbers that matter, and rates the options. It then applies all of that to India's "
               "estates and to the cost of running a café in Ahmedabad.", LEAD))
    toc = [
        ("1", "Judging a cup", "SCA score, the 10 attributes, where quality comes from"),
        ("2", "Reading the bag & the beans", "label checklist, green & roasted bean specs"),
        ("3", "Species, varieties & origins", "what makes one great bean differ from another"),
        ("4", "Processing", "washed, natural, honey, anaerobic, monsooned"),
        ("5", "Roast & freshness", "roast levels, temperatures, days off roast"),
        ("6", "Brewing methods", "espresso, filter kaapi, pour-over and more: specs & ratings"),
        ("7", "The Indian context", "regions, GI tags, grades, varieties, estates"),
        ("8", "Costs: estate vs other sources", "market prices, price ladder, sourcing routes"),
        ("9", "Ahmedabad café raw-material model", "6 sourcing scenarios, cost per cup"),
        ("10", "Ahmedabad coffee places, rated", "sources, methods, scores"),
    ]
    rows = []
    for n, t, d_ in toc:
        rows.append([P(f'<font name="Head" size="12" color="#C68B59">{n}</font>', CELL_C),
                     P(f'<b>{t}</b><br/><font color="#7A6F66">{d_}</font>', CELL)])
    half = (len(rows) + 1) // 2
    left = Table(rows[:half], colWidths=[28, CONTENT_W / 2 - 36])
    right = Table(rows[half:], colWidths=[28, CONTENT_W / 2 - 36])
    for t in (left, right):
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
                               ("TOPPADDING", (0, 0), (-1, -1), 3),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    s.append(Table([[left, right]], colWidths=[CONTENT_W / 2, CONTENT_W / 2],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(Spacer(1, 8))
    s.append(P("Executive summary: the 12 things that matter most", H2))
    summary = [
        "<b>Quality starts at the farm.</b> Variety, altitude and ripe-only picking set the ceiling. "
        "A roaster can only reveal it, and a barista can only avoid wasting it.",
        "<b>Specialty means 80+ points</b> on the SCA 100-point cupping scale. 85+ is excellent, "
        "90+ is rare. Ask sellers for the score.",
        "<b>Buy by roast date, never by expiry date.</b> Filter coffee peaks about 7-28 days after "
        "roasting. Espresso peaks about 12-35 days. Grind just before brewing.",
        "<b>Traceability predicts quality.</b> A bag that names an estate, a variety, an altitude, a "
        "process and a harvest is almost always better than one that says \"100% premium arabica\".",
        "<b>Process shapes flavour.</b> Washed coffees taste clean and bright. Naturals are fruity "
        "and heavy. Honey is in between. Anaerobic lots are exciting but polarising.",
        "<b>Roast to suit the brew.</b> Light to medium roasts suit pour-over. Medium to medium-dark "
        "suit espresso and milk drinks. Medium-dark to dark suits South Indian filter coffee.",
        "<b>Recipe matters:</b> espresso at 1:2 in 25-32 s and 9 bar. Pour-over at 1:15-1:17, "
        "92-96°C. Water at about 150 ppm TDS. Ahmedabad's hard water <i>must</i> be treated.",
        "<b>India's strength</b> is shade-grown arabica that is low in acidity and chocolatey, plus "
        "some of the world's best washed robusta. Leading estates such as Ratnagiri and Kerehaklu "
        "now make experimental micro-lots that compete internationally.",
        "<b>Indian commodity green arabica</b> costs about ₹550-650/kg (Oct 2026). Traceable estate "
        "specialty costs about ₹850-1,100/kg, micro-lots ₹1,500-3,500/kg. Imported green pays "
        "about 100% basic customs duty.",
        f"<b>For a 200-cup/day Ahmedabad café</b>, raw materials cost about ₹{RM_LO / 1e5:.1f}-"
        f"{RM_HI / 1e5:.1f} lakh a month with Indian beans. Coffee is {SHARE_LO:.0f}-{SHARE_HI:.0f}% "
        f"of that, and milk (~₹{MODEL['milk'] / 1000:.0f}k) is the next biggest line.",
        "<b>Best value-for-quality route:</b> buy estate green directly and have it toll-roasted for "
        "espresso and cold brew. Add a rotating micro-lot for pour-overs. Use a commodity blend with "
        "chicory for filter kaapi.",
        "<b>In Ahmedabad</b>, OCD Culture (multi-roaster slow bar), Blue Tokai and Kaffa (in-house live "
        "roastery) are the best places to train your palate (see section 10).",
    ]
    half = 6
    col1 = bullets(summary[:half], ParagraphStyle("sb", parent=BULLET, fontSize=8.6, leading=11.2))
    col2 = bullets(summary[half:], ParagraphStyle("sb", parent=BULLET, fontSize=8.6, leading=11.2))
    s.append(Table([[col1, col2]], colWidths=[CONTENT_W / 2, CONTENT_W / 2],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
    s.append(Spacer(1, 6))
    s.append(legend_strip())
    s.append(Spacer(1, 4))
    s.append(callout("A note on the ratings", [
        "All scores are my assessments, synthesised from published specifications, SCA standards, "
        "producer and roaster information and public reviews. They rate suitability for the stated "
        "purpose, not moral worth. I have not tasted these coffees or visited the cafés, so treat the "
        "scores as a starting map and let your own cupping overrule them."], color=SAFFRON,
        bg=HX("#FFF5EA")))
    s.append(Spacer(1, 8))
    s.append(P("Numbers to remember", H2))
    s.append(number_tiles([
        ("80+", "SCA points = specialty", TEAL), ("< 4 wks", "since roast date when you buy", SKY),
        ("3-7 / 7-14 d", "rest before filter / espresso", CARAMEL),
        ("18 g → 36 g", "espresso, 25-32 s, 9 bar", ESPRESSO),
        ("1:16", "pour-over ratio, 92-96°C, ~3 min", LEAF),
        ("150 ppm", "ideal brew-water TDS", HX("#5DADE2")),
        ("10-12%", "green-bean moisture", HX("#8DB86A")),
        ("15-25%", "roast time after first crack", ROAST),
        ("₹550-650", "per kg, commodity Indian green arabica", SAFFRON),
        ("₹850-1,100", "per kg, estate specialty green", PLUM),
        ("100%", "basic customs duty on imported coffee", BERRY),
        ("≥ 51%", "coffee in a coffee-chicory mix (FSSAI)", GOLD),
    ]))

    # ------------------------------------------------------------------ section 1
    s.append(PageBreak())
    s += section(1, "Judging a Cup", "What 'good' actually means, and how professionals score it",
                 ROAST)
    s.append(P("Professionals judge coffee by <b>cupping</b>. Coarsely ground coffee steeps in hot "
               "water and is then slurped from a spoon, so that roast and recipe don't hide anything. "
               "The Specialty Coffee Association (SCA) form scores ten attributes and adds them up to a "
               "100-point scale. In 2024 the SCA introduced the Coffee Value Assessment (CVA), which "
               "keeps <i>describing</i> a coffee separate from <i>liking</i> it. The 80-point specialty "
               "threshold is still the industry's common language."))
    attrs = [
        ["Fragrance / Aroma", "Smell of dry grounds, then of the wet brew",
         "Intense and pleasant: fruit, flowers, caramel, cocoa. Not flat, papery or smoky."],
        ["Flavour", "The main taste and retro-nasal smell",
         "Distinct and specific notes, not just \"coffee\"."],
        ["Aftertaste", "What lingers after swallowing",
         "Long and sweet, not dry, ashy or astringent."],
        ["Acidity", "Brightness, as in biting an apple",
         "Juicy and mouth-watering. Sharp, wince-making sourness is a defect."],
        ["Body", "Weight and texture in the mouth",
         "Skim-milk vs whole-milk feel. Neither is wrong."],
        ["Balance", "How the parts fit together", "Nothing shouts over the rest."],
        ["Sweetness", "Natural sugar-like fullness", "Pleasant without added sugar."],
        ["Clean cup", "No off-flavours from first sip to finish",
         "No mustiness, ferment, rubber or medicinal notes."],
        ["Uniformity", "Every cup of the lot tastes the same",
         "Shows careful sorting at the mill."],
        ["Overall", "The taster's holistic judgement", "Would you want a second cup?"],
    ]
    left = data_table(["Attribute", "What it is", "What a novice should notice"], attrs,
                      [62, 78, CONTENT_W * 0.56 - 140], head_color=ROAST, font_size=7.4)
    s.append(Table([[left, sca_ladder()]], colWidths=[CONTENT_W * 0.56, CONTENT_W * 0.44],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("RIGHTPADDING", (0, 0), (0, 0), 8)]))
    s.append(P("Left: the ten SCA cupping attributes. Right: what the total score means.", CAPTION))
    s.append(P("Where quality comes from: seed to cup", H2))
    s.append(fig(seed_to_cup(), "Figure 1. The quality chain. Every stage can only preserve or destroy "
                 "the potential set by the stages before it."))
    impact_txt = [
        P("Why the farm matters most", H3),
        P("A roaster cannot add sweetness that unripe cherries never had, and no brewer can remove a "
          "fermented defect. So the biggest levers are <b>genetics, altitude, picking and "
          "processing</b>. Higher altitude means cooler nights, so cherries ripen more slowly and form "
          "denser beans with more sugars and acids. That is why altitude is printed on good bags.",
          BODY_SM),
        P("What you control", H3),
        P("Freshness, grinding and brewing decide whether you taste that potential. A burr grinder "
          "matters more than an expensive brewer. Blade grinders give uneven particles that "
          "over-extract (bitter) and under-extract (sour) at the same time.", BODY_SM),
    ]
    s.append(Table([[impact_chart(), impact_txt]], colWidths=[CONTENT_W * 0.52, CONTENT_W * 0.48],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(P("Figure 2. How strongly each factor moves the final cup (author's weighting).", CAPTION))

    # ------------------------------------------------------------------ section 2
    s.append(CondPageBreak(300))
    s += section(2, "Reading the Bag & the Beans",
                 "A 60-second checklist you can use in any shop or online listing", TEAL)
    label_rows = [
        ["Roast date", "Printed date, ideally within 2-4 weeks", "Only a 12-month 'best before'", 10],
        ["Origin detail", "Country > region > estate > lot", "\"Premium blend\", origin unnamed", 9],
        ["Process", "Washed / natural / honey / anaerobic named", "Not stated", 8],
        ["Variety", "e.g. S.795, Sln 9, Chandragiri, SL28", "Just \"100% arabica\"", 7],
        ["Altitude", "India 1,000 m+; Africa / LatAm 1,400 m+", "Missing for a single origin", 7],
        ["Tasting notes", "Specific: jaggery, orange, cocoa nib", "Vague: rich, smooth, bold", 6],
        ["Roast level & use", "Matches your brew (filter / espresso)", "\"Dark\" for a delicate micro-lot", 8],
        ["Packaging", "One-way valve, resealable, opaque, N₂ flush",
         "Clear bag, no valve, open bins", 8],
        ["Whole bean", "Whole bean, ground at home or café", "Pre-ground (stale in ~30 min)", 9],
        ["Harvest / crop year", "Within the last 12 months", "Not stated", 6],
        ["Score / grade", "SCA score (e.g. 84.5), or a grade such as Plantation AA",
         "No quality data", 6],
    ]
    s.append(P("The label checklist", H2))
    s.append(data_table(["Label item", "What good looks like", "Red flag", "Importance"],
                        label_rows, [80, 200, 160, CONTENT_W - 440], head_color=TEAL,
                        score_cols=(3,)))
    s.append(Spacer(1, 6))
    s.append(P("Looking at the beans", H2))
    green_rows = [
        ["Primary (Cat. 1) defects", "0 in a 350 g sample", "full black, full sour, fungus, foreign matter"],
        ["Secondary (Cat. 2) defects", "≤ 5 full defects / 350 g", "broken, insect-bitten, unripe, shells"],
        ["Moisture content", "9-13% (ideal 10-12%)", "wet = mould risk; dry = flat, papery"],
        ["Water activity", "~0.45-0.60 aw", "high aw = ageing and mould"],
        ["Screen-size uniformity", "≤ 5% outside stated size", "uneven roast"],
        ["Quakers (roasted test)", "0 in 100 g roasted", "unripe beans, peanut taste"],
        ["Colour & smell", "Even blue-green (washed) / yellow-green (natural)", "faded, musty, chemical"],
    ]
    roasted_rows = [
        ["Colour uniformity", "Even, no pale beans", "mixed lots or poor sorting"],
        ["Surface oil", "Dry or matte for light-medium roasts", "oily light roast = stale"],
        ["Shape", "Whole beans, few chips", "scorched tips, craters"],
        ["Pale 'quakers'", "None", "underripe cherries"],
        ["Aroma when opened", "Sweet, caramel, fruit, cocoa", "cardboard, rancid, smoky"],
        ["Sound / feel", "Beans crack crisply when bitten", "soft or chewy = stale/humid"],
    ]
    gt = data_table(["Green coffee spec (SCA specialty grade)", "Target", "Why it matters"],
                    green_rows, [92, 82, CONTENT_W / 2 - 180], head_color=LEAF, font_size=7.2)
    rt = data_table(["Roasted bean check", "Good sign", "Warning"], roasted_rows,
                    [70, 92, CONTENT_W / 2 - 168], head_color=ROAST, font_size=7.2)
    s.append(Table([[gt, rt]], colWidths=[CONTENT_W / 2, CONTENT_W / 2],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("RIGHTPADDING", (0, 0), (0, 0), 6)]))
    s.append(Spacer(1, 6))
    s.append(callout("Novice shortcut", [
        "If a bag shows (1) a roast date under 4 weeks old, (2) a named estate and process, and "
        "(3) a valve, you have already filtered out about 80% of the bad coffee sold in India. "
        "Smell the beans: a sweet, fruity or chocolatey smell that fills the room is a good sign. A "
        "smell like old newspaper is not."], color=TEAL))
    s.append(Spacer(1, 6))
    s.append(P("What to see in the cup", H2))
    cup_rows = [
        ["Espresso crema", "Hazelnut to reddish-brown, 2-4 mm, 'tiger' flecks, lasts 1-2 min",
         "Pale, thin, vanishes fast (stale or under-extracted). Very dark with a white hole (over-extracted, too hot)"],
        ["Espresso flow", "Starts at ~6-8 s, honey-like stream, 25-32 s total",
         "Gushing in under 15 s (grind too coarse). Dripping past 40 s (too fine)"],
        ["Milk foam", "Glossy, wet-paint microfoam with no visible bubbles; sweet taste",
         "Stiff dry froth, big bubbles, scalded smell (over 65°C)"],
        ["Pour-over / black", "Clear, translucent amber to mahogany; aroma rises as it cools",
         "Murky, oily film or sludge (fines, dirty gear); flat smell"],
        ["Filter kaapi", "Thick, dark decoction; frothy top after metering; aroma before sugar",
         "Thin and brown-grey (stale or over-diluted); woody or medicinal (too much chicory)"],
        ["As it cools", "Sweetness and fruit become clearer, which is a sign of quality",
         "Turns harsher or more bitter as it cools, a sign of defects or a dark roast hiding them"],
    ]
    s.append(data_table(["What to look at", "Good sign", "Problem sign (and likely cause)"], cup_rows,
                        [84, 190, CONTENT_W - 274], head_color=TEAL, font_size=7.4))

    # ------------------------------------------------------------------ section 3
    s.append(CondPageBreak(300))
    s += section(3, "Species, Varieties & Origins",
                 "Why two 'great' coffees can taste nothing alike", LEAF)
    spec_rows = [
        ["Chromosomes / pollination", "44, self-pollinating", "22, cross-pollinating"],
        ["Typical altitude (global)", "900-2,200 m", "0-900 m"],
        ["Typical altitude (India)", "~1,000-1,600 m", "~500-1,000 m"],
        ["Caffeine (dry bean)", "1.2-1.5%", "2.2-2.7%"],
        ["Sugars (sucrose)", "6-9%", "3-7%"],
        ["Lipids (aroma carriers)", "15-17%", "10-11.5%"],
        ["Chlorogenic acids (bitterness)", "5.5-8%", "7-10%"],
        ["Bean shape", "Oval, S-shaped crease", "Rounder, straight crease"],
        ["Cup character", "Acidity, aroma, sweetness, complexity",
         "Body, crema, cocoa, earthy, more bitter"],
        ["Share of India crop 2025-26 (est.)", "~29% (118,125 t)", "~71% (284,875 t)"],
        ["Best uses", "Pour-over, specialty espresso", "Espresso blends (crema), filter kaapi"],
    ]
    st = data_table(["Spec", "Arabica (C. arabica)", "Robusta (C. canephora)"], spec_rows,
                    [96, 92, 92], head_color=LEAF, font_size=7.2)
    rating_box = [
        P("Specialty potential (my rating)", H3),
        data_table(["Type", "Score"], [["Arabica, high grown", 9.5], ["Arabica, low grown", 7],
                                       ["Fine robusta (washed, India)", 7.5],
                                       ["Commodity robusta", 5]],
                   [CONTENT_W - 300 - 60, 50], head_color=LEAF, score_cols=(1,), font_size=7.4),
        Spacer(1, 4),
        P("Robusta isn't 'bad coffee'. A carefully washed Indian robusta (e.g. Kaapi Royale) "
          "scores in the 80s on the Fine Robusta scale. It gives filter kaapi and espresso blends "
          "their thick body and crema.", BODY_SM),
    ]
    s.append(Table([[st, rating_box]], colWidths=[290, CONTENT_W - 290],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("LEFTPADDING", (1, 0), (1, 0), 10)]))
    s.append(Spacer(1, 4))
    s.append(P("Varieties: the 'grape' of coffee", H2))
    var_rows = [
        ["Gesha / Geisha", "Ethiopian landrace, made famous in Panama", "Jasmine, bergamot, peach, tea-like", "Panama, Colombia, Ethiopia", 10],
        ["Ethiopian landraces", "Wild & heirloom diversity", "Floral, citrus, berry", "Ethiopia", 9.5],
        ["SL28 / SL34", "Kenya, Scott Labs (1930s)", "Blackcurrant, grapefruit, juicy", "Kenya", 9.5],
        ["Bourbon", "Natural mutation, Réunion", "Sweet, round, caramel", "Rwanda, Burundi, LatAm", 8.5],
        ["Typica", "Original lineage", "Clean, delicate, sweet", "Jamaica, Hawaii, Indonesia", 8],
        ["Sln 9 (India)", "Tafarikela (Ethiopian) × Hibrido de Timor", "Floral/fruit potential; Fine Cup Award 2002", "Karnataka, Tamil Nadu", 8],
        ["S.795 (Sln 3, India)", "S.288 × Kent's", "Mild, cocoa, spice; bold bean", "India's most-planted arabica", 7.5],
        ["Chandragiri (Sln 13)", "Villa Sarchi × HdT, released 2007", "Clean, bold; rust-tolerant", "Karnataka", 7.5],
        ["Caturra / Catuai", "Dwarf Bourbon / Mundo Novo cross", "Bright but simpler", "LatAm; Catuai in India", 7],
        ["Catimor / Cauvery", "Caturra × HdT", "High yield, plainer cup", "India & Asia", 6],
        ["Robusta S.274 / CxR", "Indian robusta selections", "Cocoa, nut, heavy body", "Kerala, Kodagu", 6.5],
    ]
    s.append(data_table(["Variety", "Parentage", "Signature cup", "Where", "Cup potential"], var_rows,
                        [88, 122, 140, 104, CONTENT_W - 454], head_color=LEAF, score_cols=(4,),
                        font_size=7.3))

    s.append(CondPageBreak(200))
    s.append(P("What makes one great bean different from another great bean?", H2))
    s.append(P("Two 90-point coffees can be opposites: a Kenyan that tastes like blackcurrant juice, "
               "and a Brazilian natural like a hazelnut chocolate bar. Excellence is about "
               "<b>clarity, sweetness and a distinctive, defect-free identity</b>, not one flavour. "
               "Identity comes from four layers: <b>genetics</b> (Gesha's florals, SL28's "
               "blackcurrant), <b>terroir</b> (altitude, latitude, soil, shade), <b>processing</b> "
               "(washed clarity vs natural fruit), and <b>roast</b>."))
    origin_rows = [
        ["Ethiopia (Yirgacheffe, Guji)", "1,800-2,300 m", "Jasmine, lemon, bergamot, berry",
         "Birthplace of arabica; unmatched genetic diversity", "₹₹₹", 9.5],
        ["Kenya (Nyeri, Kirinyaga)", "1,500-2,100 m", "Blackcurrant, grapefruit, juicy",
         "SL28/SL34, volcanic soils, meticulous washing", "₹₹₹", 9.5],
        ["Panama (Boquete Geisha)", "1,500-1,900 m", "Jasmine, peach, tea-like",
         "The Gesha variety; record auction prices", "₹₹₹₹₹", 10],
        ["Colombia (Huila, Nariño)", "1,500-2,100 m", "Caramel, red apple, citrus",
         "Microclimates; near year-round harvests", "₹₹", 8.5],
        ["Brazil (Cerrado, S. Minas)", "800-1,300 m", "Nut, cocoa, low acidity",
         "Consistent naturals; the world's espresso base", "₹", 7],
        ["Sumatra", "1,100-1,600 m", "Earthy, cedar, herbal, heavy",
         "Unique wet-hulling (giling basah)", "₹₹", 7],
        ["India, high-grown arabica", "1,000-1,600 m", "Cocoa, spice, jaggery, mild citrus",
         "Two-tier shade, pepper and cardamom intercropping, low acidity", "₹-₹₹", 8],
        ["India, Monsooned Malabar", "n/a (process)", "Earthy, spicy, very low acid",
         "Monsoon-wind ageing; GI-protected and unique to India", "₹", 7],
    ]
    s.append(data_table(["Origin", "Altitude", "Signature cup", "What makes it different", "Cost", "Rating"],
                        origin_rows, [96, 56, 112, 160, 38, CONTENT_W - 462], head_color=PLUM,
                        score_cols=(5,), center_cols=(4,), font_size=7.3))
    s.append(Spacer(1, 6))
    s.append(Table([[radar([("Ethiopia (washed)", [8, 4, 7, 10, 3, 1], SKY),
                            ("Kenya", [10, 6, 7, 9, 3, 2], BERRY),
                            ("Panama Geisha", [8, 4, 9, 10, 2, 1], PLUM),
                            ("Colombia", [7, 6, 8, 6, 6, 2], SAFFRON)],
                           "Bright & aromatic origins"),
                     radar([("Brazil (natural)", [3, 8, 7, 4, 9, 3], GOLD),
                            ("Sumatra (wet-hulled)", [2, 9, 5, 2, 5, 9], LEAF),
                            ("India washed arabica", [5, 7, 7, 4, 8, 5], TEAL),
                            ("Monsooned Malabar", [1, 9, 5, 1, 6, 8], ROAST)],
                           "Body-forward & comforting origins")]],
                   colWidths=[CONTENT_W / 2, CONTENT_W / 2],
                   style=[("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(P("Figure 3. Typical flavour profiles (0-10, author's synthesis of common cupping notes). "
               "Individual lots vary.", CAPTION))
    s.append(Spacer(1, 5))
    s.append(callout("Why Indian coffee tastes the way it does", [
        "India grows coffee at 10-13°N under a two-tier canopy of silver oak and native trees, "
        "often next to pepper, cardamom and oranges. Shade and a monsoon climate give slower, even "
        "ripening, which produces <b>full body, low-to-medium acidity and chocolate, spice and jaggery "
        "notes</b>. That profile is ideal for milk drinks and filter kaapi. The newer wave of "
        "experimental processing (honey, anaerobic, carbonic maceration) is adding fruit-forward lots "
        "that compete with Central American coffees."], color=LEAF, bg=HX("#EEF6EF")))

    # ------------------------------------------------------------------ section 4
    s.append(Spacer(1, 6))
    s += section(4, "Processing", "How the fruit is removed: the biggest flavour switch after variety",
                 SAFFRON)
    proc_rows = [
        ["Washed (wet)", "Skin & pulp removed, fermented 12-48 h, washed, dried",
         "Clean, bright, terroir-forward", "High consistency; needs water", "Baseline", 9, 9],
        ["Honey / pulped natural", "Pulp off, sticky mucilage left on to dry (yellow/red/black)",
         "Sweet, rounded, softer acidity", "Medium", "+10-25%", 8.5, 8.5],
        ["Natural (dry)", "Whole cherry dried 2-4 weeks on beds or patios",
         "Fruity, winey, heavy body", "Over-ferment risk", "+0-20%", 8, 8],
        ["Anaerobic / carbonic", "Fermented in sealed tanks or CO₂ before drying",
         "Intense, boozy, tropical, cinnamon", "Variable; polarising", "+30-150%", 7, 6.5],
        ["Monsooned (India)", "Naturals exposed to monsoon winds ~12-16 weeks; beans swell, turn pale gold",
         "Very low acid, earthy, spicy, heavy", "Consistent", "GI premium", 7, 7.5],
        ["Wet-hulled", "Parchment hulled at high moisture (Indonesia)", "Earthy, herbal, low acid",
         "Idiosyncratic", "None", 6.5, 6],
    ]
    s.append(data_table(["Method", "How it works", "Flavour effect", "Risk", "Price vs washed",
                         "Novice appeal", "Café fit"],
                        proc_rows, [70, 140, 100, 66, 48, 40, CONTENT_W - 464],
                        head_color=SAFFRON, score_cols=(5, 6), center_cols=(4,), font_size=7.2))
    proc_txt = [
        P("How to read the map", H3),
        P("The less fruit flesh that stays on the bean while it dries, the cleaner and more "
          "'terroir-transparent' the cup. Leaving fruit on (honey, natural) or fermenting without "
          "oxygen (anaerobic) adds sweetness, fruit and body, at the cost of clarity and with more "
          "risk of ferment defects.", BODY_SM),
        P("Picking for a beginner", H3),
        P("Start with a <b>washed</b> Indian estate coffee, which shows the 'baseline'. Then try a "
          "<b>honey</b> or <b>natural</b> lot from the same estate to taste what processing does. "
          "Try anaerobic lots last, as a dessert-like experience.", BODY_SM),
        P("In Indian trade terms, <b>'Plantation'</b> means washed arabica, <b>'Cherry'</b> means "
          "natural (dry-processed) arabica or robusta, and <b>'Parchment'</b> (for robusta) means "
          "washed robusta.", BODY_SM),
    ]
    s.append(Spacer(1, 6))
    s.append(Table([[process_map(), proc_txt]], colWidths=[CONTENT_W * 0.56, CONTENT_W * 0.44],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("LEFTPADDING", (1, 0), (1, 0), 10)]))
    s.append(P("Figure 3b. Where each process sits between clarity and fruit intensity (author's "
               "synthesis).", CAPTION))

    # ------------------------------------------------------------------ section 5
    s.append(CondPageBreak(300))
    s += section(5, "Roast & Freshness", "Turning a seed into flavour, and how fast it fades", CARAMEL)
    s.append(P("Roasting is controlled cooking. Water is driven out (drying), sugars and amino acids "
               "brown (Maillard reactions and caramelisation), and the bean cracks open as steam and "
               "CO₂ escape (<b>first crack</b>). The time after first crack, called "
               "<b>development</b>, should usually be 15-25% of total roast time. Too little tastes "
               "grassy and sour. Too much tastes flat and roasty."))
    s.append(fig(roast_spectrum(), "Figure 4. The roast spectrum: phases, crack temperatures and "
                 "approximate Agtron colour readings (higher number = lighter)."))
    roast_rows = [
        ["Light (Cinnamon-City)", "200-212°C", "70-85", "11-13%", "Dry",
         "Bright acidity, floral, tea-like", 9, 5, 4, 2],
        ["Medium (City+-Full City)", "212-222°C", "55-70", "13-16%", "Dry",
         "Balanced: caramel, fruit + cocoa", 8, 9, 8, 6],
        ["Medium-dark (Full City+)", "222-228°C", "45-55", "16-18%", "Oil spots",
         "Chocolate, spice, heavy body", 5, 8, 9, 9],
        ["Dark (Vienna-French)", "228-240°C", "25-45", "18-22%", "Oily",
         "Smoky, bitter-sweet; origin fades", 2, 5, 7, 8],
    ]
    s.append(data_table(["Roast level", "Drop temp", "Agtron", "Wt. loss", "Surface", "Flavour",
                         "Pour-over", "Espresso", "Milk drinks", "Filter kaapi"],
                        roast_rows, [80, 44, 34, 36, 38, 104, 42, 42, 42, CONTENT_W - 462],
                        head_color=CARAMEL, score_cols=(6, 7, 8, 9), center_cols=(1, 2, 3, 4),
                        font_size=7.2, head_size=7.4))
    s.append(P("Columns on the right: my suitability rating of each roast level for each use.",
               CAPTION))
    s.append(P("Freshness: the 'days off roast' rule", H2))
    s.append(fig(freshness_timeline(), "Figure 5. Freshly roasted coffee gives off CO₂ for "
                 "days. That disturbs extraction, so coffee needs to rest before it peaks, and it then "
                 "slowly loses aromatics."))
    fresh = [
        "<b>Rest:</b> 3-7 days for filter, 7-14 days for espresso. Darker roasts degas faster and "
        "peak sooner.",
        "<b>Store</b> whole beans airtight, opaque, cool and dry. <b>Not in the fridge</b>, because of "
        "condensation and odours. Freeze only sealed single-use portions.",
        "<b>Grind to order.</b> Ground coffee loses much of its aroma within 15-30 minutes.",
        "<b>Café rule:</b> order weekly, keep no more than 2-3 weeks of stock, and rotate first-in, "
        "first-out. Ahmedabad's summer heat (40°C+) speeds staling, so keep stock air-conditioned.",
    ]
    s += bullets(fresh, ParagraphStyle("fb", parent=BULLET, fontSize=8.6, leading=11.2))

    # ------------------------------------------------------------------ section 6
    s.append(CondPageBreak(300))
    s += section(6, "Brewing Methods", "Specs, how each changes the cup, and how they rate", SKY)
    s.append(P("Every brew method is a different way to control the same three things: "
               "<b>how much coffee dissolves</b> (extraction, ideally 18-22% of the grounds' mass), "
               "<b>how strong the drink is</b> (TDS, total dissolved solids) and <b>what gets "
               "filtered out</b> (oils and fines). Paper filters give clarity, metal and immersion "
               "give body, and pressure gives intensity."))
    brew_rows = [
        ["Espresso", "1:2 (18 g → 36 g)", "200-300 µm", "90-96°C", "25-32 s", "9 bar",
         "8-12% TDS; syrupy, crema"],
        ["South Indian filter", "~20-25 g : 150 ml decoction; then 1 : 2-3 with milk", "350-550 µm",
         "~95-100°C", "15-30 min drip", "Gravity", "Thick decoction; sweet, frothy milk coffee"],
        ["V60 pour-over", "1:15-1:17 (15 g : 250 g)", "500-800 µm", "92-96°C",
         "2:30-3:30", "Gravity", "1.15-1.35% TDS; clarity, florals"],
        ["Chemex", "1:15-1:17 (30 g : 500 g)", "700-900 µm", "93-96°C", "4-5 min",
         "Gravity", "Very clean, light body"],
        ["AeroPress", "1:11-1:16 (15 g : 200 g)", "400-700 µm", "80-95°C", "1-2.5 min",
         "Hand press", "Forgiving, versatile"],
        ["French press", "1:12-1:15 (30 g : 450 g)", "900-1,200 µm", "93-96°C",
         "4 min + settle", "Immersion", "Heavy body, some silt"],
        ["Moka pot", "~1:7-1:10", "300-500 µm", "Start with hot water", "3-5 min",
         "~1-1.5 bar", "Strong, heavy; 'stovetop espresso'"],
        ["Cold brew", "1:5-1:8 concentrate, then dilute", "1,000-1,400 µm", "4-22°C",
         "12-20 h", "Immersion", "Low acid, chocolatey; batchable"],
        ["Turkish / cezve", "1:10", "<100 µm", "Near boil", "2-3 min", "-",
         "Thick, unfiltered"],
    ]
    s.append(data_table(["Method", "Ratio / dose", "Grind", "Water", "Contact time", "Force",
                         "Result"], brew_rows,
                        [70, 118, 56, 54, 56, 46, CONTENT_W - 400], head_color=SKY,
                        center_cols=(2, 3, 4, 5), font_size=7.2))
    s.append(Spacer(1, 4))
    s.append(fig(grind_scale(), "Figure 6. Approximate grind-size ranges by method. Burr "
                 "grinders vary, so dial in by taste."))
    rate_rows = [
        ["Espresso machine", 6, 9, 3, 7, 10, "₹2.5-15 L (2-group commercial)", 8.5],
        ["V60 pour-over", 10, 5, 6, 7, 4, "₹1,500-4,000", 9],
        ["Chemex", 10, 3, 6, 7, 4, "₹4,000-7,000", 8],
        ["AeroPress", 8, 6, 9, 9, 5, "₹3,000-4,500", 8.5],
        ["South Indian filter", 4, 8, 8, 7, 7, "₹400-2,000", 8],
        ["Cold brew", 6, 7, 9, 9, 9, "₹1,000-5,000", 8],
        ["French press", 5, 9, 10, 8, 4, "₹800-3,000", 7.5],
        ["Moka pot", 4, 8, 7, 6, 3, "₹1,500-4,000", 6.5],
    ]
    s.append(data_table(["Method", "Flavour clarity", "Body", "Ease (novice)", "Consistency",
                         "Café throughput", "Equipment cost (indicative)", "Overall"],
                        rate_rows, [84, 52, 40, 52, 52, 52, 120, CONTENT_W - 452],
                        head_color=SKY, score_cols=(1, 2, 3, 4, 5, 7), font_size=7.3))
    s.append(P("Brew-method ratings. L = lakh. 'Overall' weighs cup quality more heavily than "
               "convenience.", CAPTION))
    s.append(callout("Taste-fault decoder: fix the cup by taste", [
        "<b>Sour, thin, salty:</b> under-extracted. Grind finer, brew hotter or longer.  "
        "<b>Bitter, dry, hollow:</b> over-extracted. Grind coarser or shorten the brew.  "
        "<b>Ashy, burnt:</b> roasted too dark.  <b>Papery, flat:</b> stale beans.  "
        "<b>Peanut or cereal:</b> unripe 'quaker' beans.  <b>Chalky, dull:</b> water too hard."],
        color=SKY, bg=HX("#EEF5FA")))

    s.append(CondPageBreak(250))
    kaapi = [
        P("Deep dive: South Indian filter coffee (kaapi)", H2),
        P("<b>Equipment:</b> a two-chamber steel or brass filter, plus a dabara and tumbler for "
          "'metering' (pouring from a height to froth).", BODY_SM),
        P("<b>Beans:</b> traditionally peaberry or Plantation A arabica, often with some robusta for "
          "body. Medium-dark to dark roast, ground fine-medium.", BODY_SM),
        P("<b>Chicory:</b> adds body, colour and a woody bitterness and makes the coffee go further. "
          "FSSAI rules require a coffee-chicory mix to contain <b>at least 51% coffee</b>, and the "
          "label must state the split. Only chicory-free coffee may be called 'pure'. Good cafés use "
          "80:20 or 70:30.", BODY_SM),
        P("<b>Method:</b> put 20-25 g of powder in the upper chamber, press lightly with the disc, add "
          "about 150 ml of just-boiled water and wait 15-20 min. Mix 1 part decoction with 2-3 parts "
          "hot full-cream milk, sweeten, and meter until frothy.", BODY_SM),
        P("<b>Quality cues:</b> the decoction should be dark, thick and aromatic, and never "
          "re-boiled. If it tastes medicinal or woody, there is too much chicory.", BODY_SM),
        P("<b>Café rating: 9/10 for Ahmedabad.</b> It is familiar, cheap to make, quick to batch, and "
          "has a very high margin.", ParagraphStyle("k", parent=BODY_SM, textColor=TEAL,
                                                    fontName="Body-Bold")),
    ]
    espresso = [
        P("Espresso machine: specs that matter", H2),
        data_table(["Spec", "Target"], [
            ["Brew pressure", "~9 bar at the group (profiling optional)"],
            ["Temperature stability", "PID control, ±0.5°C; 90-96°C"],
            ["Boiler design", "Multi-boiler or heat-exchanger with good recovery"],
            ["Groups for ~200 cups/day", "2-group commercial + volumetric dosing"],
            ["Steam", "Dry, powerful steam for consistent microfoam"],
            ["Grinder", "On-demand, 64-83 mm flat or large conical burrs; one per bean"],
            ["Water", "Softening / RO + remineralisation (scale kills machines)"],
            ["Recipe", "18 g in → 36 g out in 25-32 s; adjust grind first"],
        ], [92, CONTENT_W / 2 - 104], head_color=ESPRESSO, font_size=7.2),
    ]
    s.append(Table([[kaapi, espresso]], colWidths=[CONTENT_W / 2, CONTENT_W / 2],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("RIGHTPADDING", (0, 0), (0, 0), 10)]))
    s.append(Spacer(1, 4))
    water_rows = [
        ["Total dissolved solids", "75-250 mg/L", "150 mg/L"],
        ["Calcium hardness (as CaCO₃)", "17-85 mg/L", "~68 mg/L"],
        ["Total alkalinity", "~40 mg/L", "40 mg/L"],
        ["pH", "6.5-7.5", "7.0"],
        ["Sodium", "≤ ~10 mg/L", "10 mg/L"],
        ["Chlorine / odour", "None", "0"],
    ]
    wt = data_table(["Water parameter (SCA)", "Acceptable", "Target"], water_rows,
                    [118, 72, 60], head_color=SKY, center_cols=(1, 2), font_size=7.3)
    wtxt = [P("Water is about 98% of the cup", H3),
            P("Water that is too hard tastes chalky and flat and scales the machine. Water that is too "
              "soft (raw RO) tastes sour and hollow. Borewell water in many parts of Ahmedabad is far "
              "harder than the SCA range, and municipal (Narmada-line) supply varies. Test with a "
              "₹300-500 TDS meter, then use RO plus a remineralising cartridge or a blend tap "
              "set to about 120-150 ppm. This single fix often improves a café's coffee more than "
              "changing the beans.", BODY_SM)]
    s.append(Table([[wt, wtxt]], colWidths=[260, CONTENT_W - 260],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("LEFTPADDING", (1, 0), (1, 0), 10)]))

    # ------------------------------------------------------------------ section 7
    s.append(Spacer(1, 8))
    s += section(7, "The Indian Context", "Where Indian coffee grows, how it is graded, who makes the best",
                 HX("#138808"))
    s.append(P("India is a mid-sized producer whose coffee is almost entirely shade-grown. The Coffee "
               "Board's post-blossom estimate for 2025-26 was a record <b>~4.03 lakh tonnes</b>, about "
               "29% arabica and 71% robusta. A first projection for 2026-27 is ~4.04 lakh t. Karnataka "
               "grows roughly 70%, led by Kodagu (~1.30 lakh t) and Chikkamagaluru (~1.04 lakh t)."))
    pies = Table([[donut([280000, 85150, 20315, 17535],
                         ["Karnataka", "Kerala", "Tamil Nadu", "AP, Odisha & NE"],
                         [HX("#138808"), SAFFRON, SKY, PLUM],
                         "Production by state, 2025-26 (est.)", CONTENT_W / 2 - 4, 120,
                         "4.03 L t", "Coffee Board est."),
                   donut([118125, 284875], ["Arabica", "Robusta"], [TEAL, ROAST],
                         "Production by species, 2025-26 (est.)", CONTENT_W / 2 - 4, 120,
                         "29 : 71", "arabica : robusta")]],
                 colWidths=[CONTENT_W / 2, CONTENT_W / 2],
                 style=[("LEFTPADDING", (0, 0), (-1, -1), 0)])
    s.append(fig(pies, "Figure 7. Coffee Board post-blossom estimate for 2025-26 as reported "
                 "(the AP/Odisha/NE slice is the remainder). USDA's estimate is lower (~3.6 L t)."))

    s.append(CondPageBreak(250))
    region_rows = [
        ["Bababudangiri", "Karnataka", "1,000-1,500 m", "Arabica", "Yes", "Full body, mild acidity, chocolate; India's coffee birthplace", 9],
        ["Chikmagalur (wider)", "Karnataka", "800-1,500 m", "Both", "Yes", "Cocoa, spice, citrus hints; most specialty estates", 8.5],
        ["Biligiri Rangana (BR) Hills", "Karnataka", "1,000-1,650 m", "Arabica", "-", "Clean, sweet, brighter (e.g. Attikan)", 8.5],
        ["Pulney Hills", "Tamil Nadu", "600-2,000 m", "Arabica", "-", "Bright, citrus, medium body", 8],
        ["Araku Valley", "AP / Odisha", "900-1,100 m", "Arabica", "Yes", "Sweet, fruity, light cocoa; tribal, organic-leaning", 8],
        ["Kodagu (Coorg)", "Karnataka", "750-1,100 m", "Robusta-led", "Yes", "Robusta: cocoa, nut. Arabica: mild, sweet", 7.5],
        ["Nilgiris / Shevaroys", "Tamil Nadu", "900-1,500 m", "Arabica", "-", "Fragrant, mellow, balanced", 7.5],
        ["Manjarabad (Sakleshpur)", "Karnataka", "900-1,200 m", "Both", "-", "Balanced, chocolatey", 7],
        ["Wayanad", "Kerala", "700-1,200 m", "Robusta", "Yes", "Full body, cocoa, earthy (fine robusta)", 7],
        ["Travancore / Nelliampathy", "Kerala", "600-1,600 m", "Both", "-", "Mild, nutty, spicy", 6.5],
        ["Malabar coast (monsooning)", "Karnataka / Kerala", "Sea level", "Process", "Yes", "Monsooned Malabar: very low acid, earthy", 7],
    ]
    s.append(P("Growing regions at a glance", H2))
    s.append(data_table(["Region", "State", "Altitude (approx.)", "Species", "GI tag", "Cup profile",
                         "Specialty rating"], region_rows,
                        [96, 58, 62, 50, 30, 160, CONTENT_W - 456], head_color=HX("#138808"),
                        score_cols=(6,), center_cols=(2, 3, 4), font_size=7.2))
    s.append(P("GI tags: Coorg Arabica, Chikmagalur Arabica, Bababudangiri Arabica, Araku Valley Arabica "
               "and Wayanaad Robusta (registered as a set), plus Monsooned Malabar Arabica and Robusta "
               "(registered earlier). Altitude ranges are approximate and vary by source.", CAPTION))
    grade_rows = [
        ["Plantation PB", "Washed arabica peaberry", "Round single bean", "Prized in filter kaapi", 8],
        ["Plantation AA", "Washed arabica", "Screen 18 (~7.0-7.2 mm)", "Top export grade", 8],
        ["Plantation A", "Washed arabica", "Screen 17 (~6.65 mm)", "Core specialty / café base", 7.5],
        ["Plantation B / C", "Washed arabica", "Screen 15 / 14 (~6.0 / 5.5 mm)", "Blends, filter powder", 5],
        ["Mysore Nuggets EB", "Extra-bold washed arabica", "Screen 19 (~7.5 mm)", "Premium export (Karnataka)", 8],
        ["Arabica Cherry AB / PB", "Natural arabica", "Screen ~15-17", "Fruity, heavier", 7],
        ["Robusta Kaapi Royale", "Premium washed robusta", "Bold, screen 17+", "India's showcase robusta", 7.5],
        ["Robusta Parchment AB", "Washed robusta", "Screen ~15-17", "Clean, strong; espresso blends", 6.5],
        ["Robusta Cherry AB", "Natural robusta", "Screen ~15-17", "Filter / instant", 5],
        ["Monsooned Malabar AA", "Monsooned arabica", "Screen 18+", "Very low acidity", 7],
    ]
    gtab = data_table(["Indian grade", "Type", "Bean size", "Typical use", "Cup score"], grade_rows,
                      [90, 100, 110, 150, CONTENT_W - 450], head_color=HX("#138808"), score_cols=(4,),
                      font_size=7.2)
    s.append(P("Indian grades: size isn't flavour", H2))
    s.append(gtab)
    s.append(P("Grades sort beans by <b>size and defects</b>. They do not guarantee taste, because an "
               "AA can cup at 78 or at 86. Ask for the cup score and the estate as well. Screen sizes "
               "are approximate (trade sources differ).", CAPTION))
    s.append(P("Indian estates and producers worth knowing", H2))
    estate_rows = [
        ["Ratnagiri Estate", "Bababudangiri, Chikmagalur",
         "Patre family since 1927; ~117 ha intercropped with pepper",
         "Pioneer of honey, anaerobic and carbonic-maceration lots in steel tanks", "₹₹₹", 9],
        ["Kerehaklu Estate", "Chikmagalur", "Farmed since 1953; coffee integrated into native forest",
         "Anoxic / anaerobic peaberry lots", "₹₹₹", 8.5],
        ["Baarbara Estate", "Bababudangiri range", "Est. 1890s; ~1,170-1,630 m; shade-grown S.795",
         "Washed; reliable and clean: chocolate, mild citrus, nutty", "₹₹", 8],
        ["Attikan Estate", "BR Hills", "1,200-1,650 m; silver-oak shade; wild fig trees",
         "Washed, honey and experimental; Catuai and Sln 9", "₹₹", 8],
        ["Araku (tribal growers)", "Andhra Pradesh / Odisha", "GI Araku Valley Arabica; smallholders",
         "Organic-leaning washed and natural lots", "₹₹", 8],
        ["Badra Estates", "Chikmagalur", "Flavour of India 2025: Best Robusta Natural; 2nd Robusta Washed",
         "Top fine-robusta producer", "₹-₹₹", 8],
    ]
    s.append(data_table(["Estate", "Region", "Profile", "Known for", "Price", "Rating"],
                        estate_rows, [78, 80, 132, 140, 32, CONTENT_W - 462],
                        head_color=HX("#138808"), score_cols=(5,), center_cols=(4,),
                        font_size=7.2))
    s.append(P("Estate ratings reflect reputation and published lot information. Quality varies by "
               "harvest and lot, so always cup the current crop. The Coffee Board's annual "
               "<i>Flavour of India: Fine Cup Award</i> and its e-auctions of winning lots are a good "
               "way to find top producers.", CAPTION))

    # ------------------------------------------------------------------ section 8
    s.append(CondPageBreak(300))
    s += section(8, "Costs: Estate vs Other Sources",
                 "From farm-gate prices to a landed kilo of roasted coffee in Ahmedabad", BERRY)
    s.append(P("Indian coffee is priced off two references. One is the <b>ICE arabica 'C' and London "
               "robusta futures</b>: December arabica closed at ~304 US¢/lb on 6 Oct 2026, after a "
               "52-week range of $2.44-4.23/lb. The other is <b>local trade quotes</b> per 50 kg bag in "
               "the producing districts. Specialty lots trade at a negotiated premium on top of these."))
    mk = hbar_ranges([
        ("Arabica parchment (washed)", 24100, 24750, TEAL, "₹24,100-24,750"),
        ("Robusta parchment (washed)", 18100, 18600, SKY, "₹18,100-18,600"),
        ("Arabica cherry (natural)", 13000, 14500, SAFFRON, "₹13,000-14,500"),
        ("Robusta cherry (natural)", 10000, 11000, ROAST, "₹10,000-11,000"),
    ], "Karnataka trade prices per 50 kg bag, 6 Oct 2026", CONTENT_W, 92,
        lambda v: f"₹{v / 1000:.0f}k", 30000, label_w=124, note="source: daily market reports")
    s.append(fig(mk, "Figure 8. Raw parchment and dried cherry, before hulling. Parchment yields "
                 "~80% clean green coffee and dried cherry ~50%, so the green-coffee cost works out to "
                 "about ₹600-620/kg (arabica parchment), ₹520-580 (arabica cherry), "
                 "₹450-465 (robusta parchment) and ₹400-440 (robusta cherry), before "
                 "curing, grading and freight."))
    ladder = hbar_ranges([
        ("Robusta, commodity", 400, 470, ROAST, "₹400-470"),
        ("Arabica cherry, commodity", 520, 600, SAFFRON, "₹520-600"),
        ("Arabica Plantation A/AA", 580, 680, GOLD, "₹580-680"),
        ("Estate specialty (83-85 pts)", 850, 1100, TEAL, "₹850-1,100"),
        ("Indian micro-lot (86+, experimental)", 1500, 3500, PLUM, "₹1,500-3,500"),
        ("Imported specialty, duty-paid", 2400, 3500, BERRY, "₹2,400-3,500"),
    ], "Green coffee price ladder (₹/kg, Oct 2026 estimates)", CONTENT_W / 2 - 4, 150,
        lambda v: f"{v / 1000:.1f}k", 4000, label_w=118)
    ladder_r = hbar_ranges([
        ("Regional commodity blend", 800, 1100, ROAST, "₹800-1,100"),
        ("Own roast, estate green", 1150, 1300, LEAF, "₹1,150-1,300"),
        ("Toll-roasted estate green", 1300, 1450, TEAL, "₹1,300-1,450"),
        ("National roaster, wholesale", 1500, 1900, SKY, "₹1,500-1,900"),
        ("National roaster, retail (250 g)", 2600, 3000, SAFFRON, "₹2,600-3,000"),
        ("Boutique retail (250 g)", 3600, 5500, PLUM, "₹3,600-5,500"),
    ], "Roasted coffee landed in Ahmedabad (₹/kg)", CONTENT_W / 2 - 4, 150,
        lambda v: f"{v / 1000:.0f}k", 6000, label_w=112)
    s.append(Table([[ladder, ladder_r]], colWidths=[CONTENT_W / 2, CONTENT_W / 2],
                   style=[("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(P("Figure 9. Price ladders. Market listings in May-Sept 2026 showed bulk "
               "Chikmagalur green arabica at ~₹450-600/kg. Retail examples: Blue Tokai single "
               "estates ₹700-750 per 250 g, Subko ₹895-1,369 per 250 g. Roasting loses "
               "13-18% of the weight, which is built into the roasted figures. Estate-specialty and "
               "micro-lot figures are my estimates of negotiated prices.", CAPTION))
    duty = data_table(["Imported green (illustrative)", "₹/kg"], [
        ["CIF value (specialty at ~$5.5/lb, ₹88/$, + freight)", "1,125"],
        ["Basic customs duty @ 100%", "1,125"],
        ["Social welfare surcharge @ 10% of duty", "113"],
        ["IGST @ 5% on the total", "118"],
        ["Landed (before clearing and agent fees)", "~2,480"],
    ], [CONTENT_W / 2 - 64, 52], head_color=BERRY, center_cols=(1,), font_size=7.3)
    duty_txt = [P("Why imported beans cost so much more", H3),
                P("Unroasted coffee (HS 0901.11) attracts a <b>100% basic customs duty</b> plus "
                  "surcharges. That roughly <b>doubles</b> the landed cost of an Ethiopian or "
                  "Colombian lot. It is why Indian cafés serving imported single origins charge "
                  "₹400+ for a pour-over, and why <b>Indian estate coffee is the "
                  "value-for-quality sweet spot</b>. Tariff lines are from secondary aggregators, "
                  "so confirm current rates with CBIC or a customs broker before importing.",
                  BODY_SM)]
    s.append(Table([[duty, duty_txt]], colWidths=[CONTENT_W / 2, CONTENT_W / 2],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("LEFTPADDING", (1, 0), (1, 0), 10)]))

    s.append(CondPageBreak(220))
    s.append(P("Sourcing routes compared", H2))
    route_rows = [
        ["A. Regional roaster, commodity blend", "Buy roasted Plantation/robusta blends locally",
         "800-1,100", 4, 9, 3, 9, 5.5],
        ["B. National specialty roaster (wholesale)", "B2B supply from a national specialty brand",
         "1,500-1,900", 8, 9, 9, 9, 8],
        ["C. Estate green + toll roasting", "Buy green direct from an estate; a contract roaster roasts to your profile",
         "1,300-1,450", 8, 7, 10, 6, 8.5],
        ["D. Estate green + own roaster", "In-house 2-5 kg roaster (capex & skill needed)",
         "1,150-1,300 + capex", 9, 6, 10, 3, 8],
        ["E. Curing works / trader green", "Plantation A / Cherry AB from curers, roasted by you or a toll roaster",
         "850-1,000", 5, 7, 4, 7, 6.5],
        ["F. Imported specialty", "Importer or roaster offering Ethiopia / Colombia etc.",
         "3,500-5,000", 9, 8, 8, 7, 6],
    ]
    s.append(data_table(["Route", "How it works", "₹/kg roasted, landed", "Quality control",
                         "Consistency", "Traceability", "Ease / low MOQ", "Overall"],
                        route_rows, [92, 124, 58, 44, 46, 48, 44, CONTENT_W - 456],
                        head_color=BERRY, score_cols=(3, 4, 5, 6, 7), center_cols=(2,),
                        font_size=7.2, head_size=7.0))
    s.append(P("Estate-to-estate differences: Ratnagiri-style experimental micro-lots cost 2-4× a "
               "reliable washed S.795 estate lot like Baarbara. Pay that premium only for pour-over "
               "menus, where customers can taste it. In milk drinks a clean washed estate lot or a "
               "fine robusta blend gives better value.", BODY_SM))

    # ------------------------------------------------------------------ section 9
    s.append(Spacer(1, 4))
    s += section(9, "Ahmedabad Café: Raw-Material Model",
                 "Six sourcing strategies for a 200-beverage-a-day specialty café", ESPRESSO)
    assumptions = [[m, f"{int(share * 100)}%", f"{int(CUPS_MONTH * share):,}", f"{dose} g",
                    f"{milk} ml" if milk else "-"] for m, share, dose, milk in MENU_MIX]
    at = data_table(["Drink (menu mix)", "Share", "Cups / month", "Coffee dose", "Milk bought"],
                    assumptions, [98, 34, 50, 44, 48], head_color=ESPRESSO,
                    center_cols=(1, 2, 3, 4), font_size=7.2)
    notes = [P("Model assumptions", H3),
             P("200 drinks a day × 30 days = 6,000 drinks a month. +6% coffee for dial-in and "
               "purges, +~15% milk for steaming loss. Milk is full-cream at ₹68/L (Amul Gold "
               "MRP ₹70/L after the May 2026 revision, less a trade margin). 40% of drinks are "
               "takeaway at ₹9 per cup set. Sugar and syrups average ₹2.5 per drink. "
               "Water, filter papers and cleaning chemicals ₹9,000 a month. Filter kaapi uses an "
               "80:20 coffee-chicory blend at ₹750/kg in every scenario. Excludes rent, staff, "
               "food and equipment.", BODY_SM)]
    s.append(Table([[at, notes]], colWidths=[280, CONTENT_W - 280],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("LEFTPADDING", (1, 0), (1, 0), 10)]))

    rows, stack = [], []
    for sc in MODEL["scen"]:
        coffee, total = sc["coffee"], sc["total"]
        rows.append([sc["name"], f"{sc['price']:,}" +
                     (f" / {sc['pour_price']:,}" if sc["pour_price"] else ""),
                     f"{coffee / 1000:,.0f}k", f"{MODEL['milk'] / 1000:,.0f}k",
                     f"{sum(sc['comps'][2:]) / 1000:,.0f}k",
                     f"₹{total / 100000:.2f} L", f"₹{sc['per_drink']:.0f}",
                     f"{100 * coffee / total:.0f}%"])
        stack.append((sc["name"].split(" (")[0].replace("Recommended hybrid: ", "Hybrid: "),
                      sc["comps"]))
    main_kg, kaapi_kg, milk_l = MODEL["main_kg"], MODEL["kaapi_kg"], MODEL["milk_l"]
    s.append(Spacer(1, 5))
    s.append(data_table(["Scenario", "₹/kg roasted (main / pour-over)", "Coffee / mo",
                         "Milk / mo", "Other / mo", "Total / month", "Per drink", "Coffee share"],
                        rows, [150, 72, 50, 44, 46, 60, 40, CONTENT_W - 462],
                        head_color=ESPRESSO, center_cols=(1, 2, 3, 4, 5, 6, 7), font_size=7.3))
    s.append(P(f"Coffee needed: ~{main_kg:.0f} kg roasted beans + ~{kaapi_kg:.1f} kg filter blend per "
               f"month; milk ~{milk_l:,.0f} L. *Scenario D excludes roaster capex (typically several "
               "lakh rupees), gas and the roaster's time.", CAPTION))

    s.append(CondPageBreak(200))
    s.append(fig(stacked_scenarios(stack, CONTENT_W, 165),
                 "Figure 10. Monthly raw-material cost by scenario (L = lakh). Moving from "
                 f"commodity to good estate coffee adds only about ₹{UPGRADE_LO:.0f}-"
                 f"{UPGRADE_HI:.0f} per drink."))
    hy = _BY["R"]
    hy_price, pour_price = hy["price"], hy["pour_price"]
    w_, pk_ = COFFEE_WASTE, CUP_SET * TAKEAWAY_SHARE
    menu = [("Cappuccino / latte", 18 * w_ * hy_price / 1000, 0.23 * MILK_PER_L, 2.5, pk_, "220-280"),
            ("Espresso / Americano", 18 * w_ * hy_price / 1000, 0, 1, pk_, "160-220"),
            ("V60 pour-over (micro-lot)", 16 * w_ * pour_price / 1000, 0, 0, pk_ + 4, "300-400"),
            ("Cold brew", 22 * w_ * hy_price / 1000, 0, 2, pk_ + 2, "240-320"),
            ("Filter kaapi", 10 * w_ * KAAPI_BLEND_PER_KG / 1000, 0.13 * MILK_PER_L, 2, pk_,
             "80-140")]
    drink_rows = []
    for nm, cof, milk, sw, pk, price in menu:
        cost = cof + milk + sw + pk
        mid = sum(int(x) for x in price.split("-")) / 2
        drink_rows.append([nm, f"₹{cof:.0f}", f"₹{milk:.0f}" if milk else "-",
                           f"₹{sw + pk:.0f}", f"₹{cost:.0f}", f"₹{price}",
                           f"{100 * cost / mid:.0f}%"])
    dt = data_table(["Drink (hybrid sourcing)", "Coffee", "Milk", "Sweet + pack", "Raw cost",
                     "Typical Ahd menu price", "Beverage cost %"], drink_rows,
                    [120, 50, 44, 60, 52, 90, CONTENT_W - 416], head_color=ESPRESSO,
                    center_cols=(1, 2, 3, 4, 5, 6), font_size=7.4)
    s.append(P("Per-drink economics (recommended hybrid)", H2))
    s.append(dt)
    s.append(P("Menu prices are indicative for Ahmedabad specialty cafés (about ₹500-1,500 for "
               "two, per listings). A beverage cost under ~25% leaves room for rent and staff.",
               CAPTION))
    recs = [
        "<b>Espresso and cold brew:</b> one or two washed estate lots (Chikmagalur / BR Hills, "
        "S.795 or Sln 9, 83-85 pts) bought green and toll-roasted medium. Add 10-20% fine washed "
        "robusta (Kaapi Royale) to the house blend for body and crema in milk drinks.",
        "<b>Pour-over bar:</b> rotate one micro-lot a month (honey, natural or anaerobic from "
        "Ratnagiri / Kerehaklu-type producers). Buy 15-30 kg at a time and price it as a premium "
        "'flight'.",
        "<b>Filter kaapi:</b> Plantation A/PB plus robusta, roasted medium-dark, 80:20 with chicory. "
        "It is cheap, loved in Gujarat, and has the highest margin on the menu.",
        "<b>Lock in prices:</b> green coffee keeps 6-12 months in GrainPro bags. Contract part of the "
        "year's needs at harvest (Dec-Mar), and roast weekly to keep stock fresh.",
        f"<b>Risk check:</b> a 20% rise in coffee prices adds about ₹{0.2 * hy['coffee'] / CUPS_MONTH:.0f}"
        " per drink in the hybrid model. Milk (about "
        f"₹{MODEL['milk'] / 1000:.0f}k a month) is the second-biggest line, so size milk pitchers "
        "to the drink to cut steaming waste.",
    ]
    s.append(P("Recommendations", H2))
    s += bullets(recs, ParagraphStyle("rb", parent=BULLET, fontSize=8.6, leading=11.2))

    # ------------------------------------------------------------------ section 10
    s.append(CondPageBreak(400))
    s += section(10, "Ahmedabad Coffee Places, Rated",
                 "Who serves what, how it's brewed, and where to train your palate", PLUM)
    s.append(P("Ratings are based on public information (sourcing disclosures, brew menus, roasting "
               "set-up), aggregated listings and reviews from District, Swiggy and Zomato, and press "
               "coverage up to Oct 2026. I could not taste the coffee. <b>Score = 25% sourcing "
               "transparency + 20% roast freshness/control + 20% brew-method range + 20% review "
               "sentiment + 15% value.</b>", BODY_SM))
    cafes = [
        # name, area, beans/source, roasting, methods & signatures, price for two, public rating, sub-scores
        ["OCD Culture", "Bodakdev", "Multi-roaster 'deep bean menu'; rotating new / guest Indian roasters",
         "Curates guest roasts", "V60, AeroPress, iced pour-over, espresso; OCD Special Latte",
         "~₹500", "4.3-4.5", (8, 7.5, 9, 8.5, 9)],
        ["Blue Tokai Coffee Roasters", "CG Road (CG Square)*",
         "Direct-sourced Indian single estates (e.g. Attikan, Sandalwood); 100% arabica",
         "Own roasteries (national)", "Espresso, pour-over, coffee flights, cold brew",
         "est. ₹700-900", "n/a", (9.5, 8, 8.5, 8, 7)],
        ["Kaffa Coffee Roasters", "Vastrapur / Ambawadi; Brewed by Kaffa (Thaltej); KOMO",
         "In-house roasted; origins not publicly detailed", "Live roastery on site (one of the city's earliest)",
         "Espresso, extensive manual-brew menu, cold brew; French Vanilla Latte, Litchi Cold Brew",
         "₹1,400", "4.5", (6, 9, 8, 8.5, 6.5)],
        ["Roastery Cultúr", "Bodakdev (+ 2 outlets)", "Locally sourced (Indian) beans; specifics not published",
         "Own third-wave roasting", "Espresso, pour-over; Café con Leche, cinnamon cappuccino",
         "₹800-1,500", "4.6", (6, 8.5, 7.5, 8.5, 6)],
        ["Mainline Coffee", "Navrangpura", "Not publicly specified", "Buys in (roaster not named)",
         "Manual brew bar; Barrel-Aged Cold Brew, Caramel Iced Latte", "₹500-800",
         "4.6-4.8", (5, 7, 8.5, 9, 8.5)],
        ["Mleko", "Navrangpura", "'100% specialty arabica' (roaster not named)", "Buys in",
         "Espresso focus, 24-hr cold brew; bakery", "est. ₹600-800", "n/a",
         (5.5, 7, 7, 8.5, 7.5)],
        ["Third Wave Coffee", "CG Road, Prahlad Nagar, airport",
         "100% arabica from ~15 Indian estates, mostly Karnataka", "Central roasting (Bengaluru)",
         "Espresso & milk drinks, cold brew, some pour-over", "est. ₹700-900", "n/a",
         (7, 7.5, 7, 7.5, 7)],
        ["Fick's Coffee", "Bodakdev", "Not publicly specified", "Buys in",
         "Specialty espresso bar; Kafir Lime Espresso, Iced Salted Caramel Latte", "₹1,400",
         "4.5", (5, 7, 7, 8.5, 6.5)],
        ["Tochico Specialty Coffee Roasters", "Ambli", "Not yet published (new)",
         "Neighbourhood roastery", "Espresso drinks; Spanish Latte", "₹2,100", "new",
         (5.5, 8, 6.5, 7, 5.5)],
        ["Grace Coffee Co.", "Bodakdev", "Not publicly specified", "Buys in",
         "Self-service; OG Grace Cold Brew; late-night", "₹500", "4.6", (4.5, 6.5, 6, 8.5, 9)],
        ["Starbucks (Tata Starbucks)", "Several outlets",
         "Global blends + India Estates Blend from Tata Coffee's Coorg & Chikmagalur estates",
         "Centrally roasted; dark-roast house style", "Espresso, milk and Frappuccino drinks; tall cappuccino ~₹335",
         "est. ₹800-1,000", "n/a", (6.5, 6, 5.5, 7.5, 5.5)],
    ]
    w_ = (0.25, 0.20, 0.20, 0.20, 0.15)
    cafe_rows = []
    chart_items = []
    for c in cafes:
        score = round(sum(a * b for a, b in zip(c[7], w_)), 1)
        c.append(score)
    cafes.sort(key=lambda c: -c[8])
    for c in cafes:
        cafe_rows.append([c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[8]])
        chart_items.append((c[0].replace(" Coffee Roasters", "").replace(" (Tata Starbucks)", "")
                            .replace(" Specialty", ""), c[8]))
    s.append(data_table(["Place", "Area", "Beans / source", "Roasting", "Brew methods & signatures",
                         "For two", "Public rating", "My score"],
                        cafe_rows, [62, 56, 100, 62, 102, 50, 36, CONTENT_W - 468],
                        head_color=PLUM, score_cols=(7,), center_cols=(5, 6), font_size=6.9))
    s.append(Spacer(1, 4))
    sub_rows = [[c[0]] + list(c[7]) for c in cafes]
    sub = data_table(["Place", "Sourcing", "Roast", "Brew range", "Reviews", "Value"], sub_rows,
                     [94, 40, 32, 38, 40, 34], head_color=PLUM, score_cols=(1, 2, 3, 4, 5),
                     font_size=6.8, head_size=7.2)
    chart = cafe_score_chart(chart_items, CONTENT_W - 286, 190)
    s.append(Table([[sub, chart]], colWidths=[286, CONTENT_W - 286],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(P("Figure 11. Sub-scores (left) and weighted overall score (right). Public ratings are "
               "aggregator stars at the time of research ('n/a' = not found). 'For two' is the listed "
               "price; 'est.' = author's estimate. *Blue Tokai's CG Square listing is undated, so "
               "confirm it is open. Tochico is too new for a stable rating.", CAPTION))
    s.append(callout("How a novice should use Ahmedabad's cafés", [
        "<b>Week 1, OCD Culture:</b> order the same coffee as a V60 and as an AeroPress, then two "
        "different roasters' beans side by side. You'll learn what 'brew method' and 'origin' taste "
        "like.  <b>Week 2, Blue Tokai:</b> do a coffee flight (washed vs natural vs honey) and read the "
        "estate cards.  <b>Week 3, Kaffa:</b> watch the live roaster and ask for the roast date, then "
        "taste an espresso black before a latte.  <b>Week 4:</b> compare a Starbucks dark-roast "
        "cappuccino with a specialty cappuccino. The difference in sweetness and bitterness is the "
        "lesson."], color=PLUM, bg=HX("#F3EEF8")))

    # ------------------------------------------------------------------ final page
    s.append(CondPageBreak(200))
    s.append(P("Glossary for beginners", H2))
    gl = [
        ("Agtron", "Instrument reading of roast colour; higher = lighter."),
        ("Cupping", "Standard tasting protocol used to score coffee."),
        ("Decoction", "Concentrated filter-kaapi extract, mixed with milk."),
        ("Degassing", "CO₂ release after roasting; why beans need rest."),
        ("Development", "Roast time after first crack."),
        ("Extraction yield", "% of the grounds dissolved into the cup (aim 18-22%)."),
        ("Fine Robusta", "Specialty-graded robusta (Q-Robusta 80+)."),
        ("Micro-lot", "Small, separately processed batch from one plot or day."),
        ("Parchment", "Papery husk around washed beans; also India's term for washed robusta."),
        ("Peaberry (PB)", "Single round bean in a cherry; prized for filter coffee."),
        ("Q Grader", "Licensed professional coffee taster."),
        ("Quaker", "Pale, unripe bean that tastes like peanut or cereal."),
        ("Screen size", "Bean size in 1/64-inch steps (screen 18 ≈ 7.1 mm)."),
        ("TDS", "Total dissolved solids: the strength of the brew."),
        ("Toll roasting", "Paying a roaster to roast your own green coffee."),
    ]
    gl_rows = [[a, b] for a, b in gl]
    half = (len(gl_rows) + 1) // 2
    g1 = data_table(["Term", "Meaning"], gl_rows[:half], [70, CONTENT_W / 2 - 80],
                    head_color=ROAST, font_size=7.2)
    g2 = data_table(["Term", "Meaning"], gl_rows[half:], [70, CONTENT_W / 2 - 80],
                    head_color=ROAST, font_size=7.2)
    s.append(Table([[g1, g2]], colWidths=[CONTENT_W / 2, CONTENT_W / 2],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(Spacer(1, 6))
    s.append(P("Your 30-day palate plan", H2))
    plan = [
        "<b>Days 1-7:</b> buy a washed Indian estate coffee and a natural one, both medium roast, from "
        "the same roaster. Brew both the same way. Note acidity, body and sweetness.",
        "<b>Days 8-14:</b> brew one coffee three ways (V60, French press, filter kaapi) and see how the "
        "method changes body and clarity.",
        "<b>Days 15-21:</b> taste the same bean at day 3, day 10 and day 30 after roasting to learn what "
        "freshness tastes like.",
        "<b>Days 22-30:</b> compare an Indian micro-lot with an imported Ethiopian, then cup three "
        "coffees blind and rank them before reading the labels.",
    ]
    s += bullets(plan, ParagraphStyle("pb", parent=BULLET, fontSize=8.5, leading=11))
    s.append(Spacer(1, 4))
    s.append(P("Sources & method", H2))
    srcs = [
        "Specialty Coffee Association: cupping protocol and score bands, green grading (350 g defect "
        "count), water quality standard, Coffee Value Assessment (2024).",
        "Coffee Board of India / reported via AgroSpectrum (Sept 2025): 2025-26 post-blossom crop "
        "estimate (4.03 L t; arabica 118,125 t; robusta 284,875 t; state split). StoneX: 2026-27 "
        "first forecast and USDA comparison.",
        "Kirehalli daily coffee market reports (Oct 2026): Karnataka parchment and cherry prices per "
        "50 kg; ICE December arabica closes. Trading Economics / market reports: ICE arabica ~$2.93/lb "
        "(5 Oct 2026), 52-week range $2.44-4.23.",
        "IndiaMART and TradeIndia listings (May-Sept 2026): bulk Chikmagalur green arabica "
        "₹450-600/kg. Amazon.in and roaster sites: Blue Tokai Attikan ₹700 / Sandalwood "
        "₹750 per 250 g; Subko ₹895-1,369 per 250 g; Black Baza Otter ₹580 per 250 g.",
        "Treayo / eximpe HS-code pages: India BCD 100% on HS 0901 coffee, IGST 5%, SWS 10% (verify "
        "with CBIC). FSSAI advisory (Nov 2021): coffee-chicory mix must contain at least 51% coffee "
        "and declare the split.",
        "Business Today, Daily Pioneer, Zee Business (May 2026): Amul +₹2/L; Amul Gold ₹70/L, "
        "Taaza ₹57/L. PIB and Drishti IAS: Indian coffee GI tags.",
        "Counter Culture Coffee and Coffee Board research notes: S.795 (Sln 3), Sln 9, Chandragiri "
        "(Sln 13), Cauvery parentage. Roaster and producer pages: Ratnagiri, Kerehaklu, Baarbara and "
        "Attikan estate details. The Week (Apr 2025): Badra Estates, Flavour of India award.",
        "District blog 'Speciality Coffee Spots in Ahmedabad' (23 Sept 2026); Swiggy, Zomato, "
        "EazyDiner, Wanderlog and Justdial listings; r/ahmedabad discussion; Curly Tales and "
        "Retail4Growth (Third Wave Ahmedabad launch, Nov 2025); Restaurant India and Tata Consumer "
        "(Tata Starbucks sourcing).",
        "<b>Limitations:</b> direct access to several sites was blocked during research, so some "
        "figures come from search-index excerpts. Prices move daily, and ratings are informed "
        "opinion. Verify current prices with suppliers before committing capital.",
    ]
    for t in srcs:
        s.append(P(t, SOURCE))
    return s


def main():
    doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=27 * mm / 1.0 - 2 * mm, bottomMargin=13 * mm,
                          title="What Makes Coffee Great? A Novice's Field Guide (India Edition)",
                          author="Coffee research report", subject="Coffee quality, Indian sourcing, "
                          "Ahmedabad café costs and ratings", creator="ReportLab")
    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover", leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0)
    body_frame = Frame(MARGIN, 13 * mm, CONTENT_W, PAGE_H - 13 * mm - 25 * mm, id="body",
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover),
                          PageTemplate(id="body", frames=[body_frame], onPage=draw_body)])
    story = [Spacer(1, 1)] + build_story()
    doc.build(story)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
