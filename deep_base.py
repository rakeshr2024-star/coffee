"""Shared layout pieces for the deep-dive report (built on the house style of build_report)."""
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (CondPageBreak, Flowable, KeepTogether, PageBreak, Spacer, Table,
                                TableStyle)

import brew_art as BA
import build_report as R
from build_report import (BODY, BODY_SM, CAPTION, CONTENT_W, H2, H3, HX, LEAD, MUTED, P, ROAST,
                          SOURCE, bullets, callout, data_table)

ESPRESSO, CARAMEL, CREMA, PAPER, INK, RULE = R.ESPRESSO, R.CARAMEL, R.CREMA, R.PAPER, R.INK, R.RULE
TEAL, SAFFRON, LEAF, BERRY, PLUM, SKY, GOLD = R.TEAL, R.SAFFRON, R.LEAF, R.BERRY, R.PLUM, R.SKY, R.GOLD

# slightly larger body text than the 19-page field guide, for a long read
BODY.fontSize, BODY.leading = 9.8, 13.2
BODY_SM.fontSize, BODY_SM.leading = 8.7, 11.5

TOC = {}          # chapter key -> page number (filled while building)
STATE = {"part": ""}

H2N = ParagraphStyle("h2n", parent=H2, spaceBefore=6, spaceAfter=3, keepWithNext=1)
H3N = ParagraphStyle("h3n", parent=H3, spaceBefore=3, spaceAfter=1.5, keepWithNext=1)
STEP = ParagraphStyle("step", parent=BODY_SM, leftIndent=12, firstLineIndent=-12, spaceAfter=1.4)
SMALL = ParagraphStyle("small", parent=BODY_SM, fontSize=7.8, leading=10)
KPI_BIG = ParagraphStyle("kpib", fontName="Body-Bold", fontSize=15, leading=17, textColor=ESPRESSO)


class Chapter(R.SectionBand):
    """Section band that records its page number for the contents page."""

    def __init__(self, key, num, title, subtitle, color=ROAST):
        super().__init__(num, title, subtitle, color)
        self.key = key

    def draw(self):
        TOC[self.key] = self.canv.getPageNumber()
        super().draw()


class PartMarker(Flowable):
    """Zero-size flowable that sets the running header text from this page on."""

    def __init__(self, label):
        super().__init__()
        self.label = label

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        STATE["part"] = self.label


class PartDivider(Flowable):
    def __init__(self, key, num, title, blurb, chapters, color):
        super().__init__()
        self.key, self.num, self.title, self.blurb = key, num, title, blurb
        self.chapters, self.color = chapters, color

    def wrap(self, aw, ah):
        self.width, self.height = aw, ah - 2
        return aw, self.height

    def draw(self):
        TOC[self.key] = self.canv.getPageNumber()
        c = self.canv
        w, h = self.width, self.height
        c.saveState()
        c.setFillColor(self.color)
        c.roundRect(0, 0, w, h, 10, stroke=0, fill=1)
        c.setFillColor(colors.Color(1, 1, 1, alpha=0.07))
        for r, (x, y) in [(150, (w * 0.85, h * 0.2)), (95, (w * 0.95, h * 0.62)), (60, (w * 0.1, h * 0.08))]:
            c.circle(x, y, r, stroke=0, fill=1)
        c.setFillColor(SAFFRON)
        c.setFont("Body-Bold", 11)
        c.drawString(28, h - 60, f"PART {self.num}")
        c.setFillColor(colors.white)
        c.setFont("Head", 34)
        y = h - 108
        for ln in self.title.split("\n"):
            c.drawString(28, y, ln)
            y -= 40
        c.setFont("Head-Italic", 12.5)
        c.setFillColor(CREMA)
        import illustrations as il
        y -= 6
        for ln in il.wrap_lines(self.blurb, "Head-Italic", 12.5, w - 70):
            c.drawString(28, y, ln)
            y -= 17
        y -= 18
        c.setFont("Body-Bold", 9)
        c.setFillColor(SAFFRON)
        c.drawString(28, y, "CHAPTERS")
        y -= 20
        for num, t in self.chapters:
            c.setFillColor(CARAMEL)
            c.setFont("Head", 13)
            c.drawRightString(52, y, str(num))
            c.setFillColor(colors.white)
            c.setFont("Body", 11.5)
            c.drawString(62, y, t)
            y -= 21
        c.restoreState()


# ------------------------------------------------------------------ text helpers
def chapter(key, num, title, subtitle, color=ROAST, new_page=True):
    out = [PageBreak()] if new_page else [CondPageBreak(330)]
    return out + [Chapter(key, num, title, subtitle, color), Spacer(1, 6)]


def h2(t):
    return [CondPageBreak(110), P(t, H2N)]


def h3(t):
    return P(t, H3N)


def p(t):
    return P(t, BODY)


def ps(t):
    return P(t, BODY_SM)


def lead(t):
    return P(t, LEAD)


def bl(items, color="#C68B59"):
    return bullets(items, color=color)


def src(t):
    return P("Source: " + t, SOURCE)


def note(title, items, color=TEAL, bg=None):
    return callout(title, items, color=color, bg=bg)


def figc(flowable, caption):
    return KeepTogether([flowable, P(caption, CAPTION)])


def tbl(header, rows, widths, **kw):
    return data_table(header, rows, widths, **kw)


def side(left, right, lw=0.5, gap=10):
    """Two columns of flowables; lw = share of width for the left column."""
    lwid = CONTENT_W * lw - gap / 2
    rwid = CONTENT_W * (1 - lw) - gap / 2
    t = Table([[left, right]], colWidths=[lwid + gap / 2, rwid + gap / 2])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (0, -1), gap / 2),
                           ("LEFTPADDING", (1, 0), (1, -1), gap / 2),
                           ("RIGHTPADDING", (1, 0), (1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return t


def numbered(items, color="#6F4E37"):
    return [P(f'<font name="Body-Bold" color="{color}">{i}.</font>&nbsp; {t}', STEP)
            for i, t in enumerate(items, 1)]


def recipe_table(rows, width):
    st = ParagraphStyle("rk", parent=BODY_SM, fontSize=7.6, leading=9.4)
    stb = ParagraphStyle("rkb", parent=st, fontName="Body-Bold", textColor=ROAST)
    data = [[P(k, stb), P(v, st)] for k, v in rows]
    t = Table(data, colWidths=[width * 0.36, width * 0.64])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), HX("#F7F1E8")),
                           ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.white),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.8), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
                           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    return t


def method_card(icon_key, name, tagline, body, recipe, steps, tips, color=ROAST, icon_h=118,
                extra=None):
    """A brewing-method card: icon + recipe on the left, explanation and steps on the right."""
    lw = 132
    rw = CONTENT_W - lw - 10
    left = [BA.icon(icon_key, lw, icon_h)]
    if extra:
        left += [Spacer(1, 4), BA.icon(extra, lw, icon_h * 0.75)]
    left += [Spacer(1, 4), recipe_table(recipe, lw)]
    right = [P(f'<font name="Head" size="13" color="{color.hexval().replace("0x", "#")}">{name}</font>'
               f'&nbsp;&nbsp;<font name="Body-Italic" size="8.4" color="#7A6F66">{tagline}</font>',
               ParagraphStyle("mc", parent=BODY, spaceAfter=3))]
    right += [P(t, BODY_SM) for t in body]
    if steps:
        right.append(P("<b>How to make it</b>", ParagraphStyle("mh", parent=BODY_SM, textColor=ROAST,
                                                            spaceBefore=2)))
        right += numbered(steps)
    if tips:
        right.append(Spacer(1, 2))
        right += bullets(tips, ParagraphStyle("mt", parent=BODY_SM, leftIndent=10, bulletIndent=1,
                                              spaceAfter=1.2), color="#1B998B")
    t = Table([[left, right]], colWidths=[lw + 10, rw])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (0, -1), 10),
                           ("RIGHTPADDING", (1, 0), (1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                           ("LINEABOVE", (0, 0), (-1, 0), 1.2, color)]))
    return [Spacer(1, 4), t, Spacer(1, 8)]


def kpi_tiles(items, cols=4):
    """items: [(big, small, colour)]"""
    return R.number_tiles(items, cols)


def money(v, d=0):
    if v is None or isinstance(v, str):
        return str(v)
    s = f"{abs(v):,.{d}f}"
    return f"({s})" if v < 0 else s


def pct(v, d=1):
    if v is None or isinstance(v, str):
        return "n.m."
    return f"{v * 100:.{d}f}%"


def yrs(v):
    if isinstance(v, str):
        return v
    return ">10 yrs" if v >= 99 else f"{v:.1f} yrs"


__all__ = ["CondPageBreak", "KeepTogether", "PageBreak", "Spacer", "Table", "TableStyle",
           "BODY", "BODY_SM", "CAPTION", "CONTENT_W", "H2", "H3", "HX", "LEAD", "MUTED", "P",
           "ROAST", "SOURCE", "bullets", "callout", "data_table"]
