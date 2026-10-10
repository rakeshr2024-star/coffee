"""Chart and diagram primitives for the deep-dive report (ReportLab canvas, no images).

Every function returns a CanvasFigure (a fixed-size flowable).  Fonts and palette are
the ones registered by build_report.py.
"""
import math

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle

import build_report as R
import illustrations as il
from illustrations import CanvasFigure, arrow, para, rgba, shade, text

HX = colors.HexColor
INK, MUTED, RULE, ROAST, CARAMEL = R.INK, R.MUTED, R.RULE, R.ROAST, R.CARAMEL
ESPRESSO, TEAL, SAFFRON, LEAF, BERRY, PLUM, SKY, GOLD = (R.ESPRESSO, R.TEAL, R.SAFFRON, R.LEAF,
                                                        R.BERRY, R.PLUM, R.SKY, R.GOLD)
PANEL = HX("#FBF6EF")
SERIES = [ROAST, CARAMEL, TEAL, SKY, SAFFRON, PLUM, LEAF, BERRY, GOLD]


def sw(s, font="Body", size=7):
    return pdfmetrics.stringWidth(s, font, size)


def nice_step(span, n=5):
    if span <= 0:
        return 1
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            return m * mag
    return 10 * mag


def axis_range(vmin, vmax, n=5, zero=True):
    if zero:
        vmin, vmax = min(0, vmin), max(0, vmax)
    if vmax == vmin:
        vmax = vmin + 1
    step = nice_step(vmax - vmin, n)
    lo = math.floor(vmin / step) * step
    hi = math.ceil(vmax / step) * step
    return lo, hi, step


def _title(c, w, h, title, sub=None):
    if title:
        text(c, 0, h - 9, title, 8.2, "Body-Bold", ROAST)
    if sub:
        text(c, 0, h - 19, sub, 6.8, "Body-Italic", MUTED)


def _legend(c, items, x, y, size=6.9, gap=12):
    for lab, col, kind in items:
        c.setFillColor(col)
        c.setStrokeColor(col)
        if kind == "line":
            c.setLineWidth(1.6)
            c.line(x, y + 2.5, x + 10, y + 2.5)
            c.circle(x + 5, y + 2.5, 1.6, stroke=0, fill=1)
        else:
            c.rect(x, y, 8, 6, stroke=0, fill=1)
        text(c, x + 12, y, lab, size, "Body", INK)
        x += 12 + sw(lab, "Body", size) + gap
    return x


# =============================================================================== bar chart
def bar_chart(cats, series, w, h, title=None, sub=None, fmt="{:,.0f}", stacked=False,
              line=None, line_fmt="{:.0%}", show_vals=True, val_size=6.0, ylab=None,
              cat_size=6.8, legend=True, colors_=None, highlight=None, line_axis_max=None):
    """series: [(name, [values], colour)]; line: (name, [values], colour) on right axis."""
    def draw(c, W, H):
        _title(c, W, H, title, sub)
        top = H - (24 if sub else 15 if title else 4)
        bottom = 22 if legend and (len(series) > 1 or line) else 14
        left, right = 34, 34 if line else 6
        x0, x1, y0, y1 = left, W - right, bottom, top - 6
        if stacked:
            pos = [sum(max(0, s[1][i] or 0) for s in series) for i in range(len(cats))]
            neg = [sum(min(0, s[1][i] or 0) for s in series) for i in range(len(cats))]
            vmin, vmax = min(neg), max(pos)
        else:
            vals = [v for s in series for v in s[1] if v is not None]
            vmin, vmax = min(vals), max(vals)
        lo, hi, step = axis_range(vmin, vmax)

        def Y(v):
            return y0 + (v - lo) / (hi - lo) * (y1 - y0)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        v = lo
        while v <= hi + 1e-9:
            c.line(x0, Y(v), x1, Y(v))
            text(c, x0 - 3, Y(v) - 2.2, fmt.format(v), 6.2, "Body", MUTED, "end")
            v += step
        c.setStrokeColor(MUTED)
        c.setLineWidth(0.7)
        c.line(x0, Y(0), x1, Y(0))
        n = len(cats)
        gw = (x1 - x0) / n
        ns = 1 if stacked else len(series)
        bw = min(gw * 0.78 / ns, 26)
        for i, cat in enumerate(cats):
            gx = x0 + i * gw + (gw - bw * ns) / 2
            base_p, base_n = 0, 0
            for k, (name, vals, col) in enumerate(series):
                v = vals[i]
                if v is None:
                    continue
                if stacked:
                    b = base_p if v >= 0 else base_n
                    ya, yb = Y(b), Y(b + v)
                    if v >= 0:
                        base_p += v
                    else:
                        base_n += v
                    bx = gx
                else:
                    ya, yb = Y(0), Y(v)
                    bx = gx + k * bw
                cc = col
                if highlight and i in highlight:
                    cc = highlight[i]
                c.setFillColor(cc)
                c.rect(bx + 0.6, min(ya, yb), bw - 1.2, abs(yb - ya), stroke=0, fill=1)
                if show_vals and not stacked and abs(yb - ya) >= 0 and ns <= 3:
                    ty = yb + 2 if v >= 0 else yb - 7
                    text(c, bx + bw / 2, ty, fmt.format(v), val_size, "Body", INK, "middle")
            if stacked and show_vals:
                tot = sum(s[1][i] or 0 for s in series)
                text(c, gx + bw / 2, Y(max(base_p, tot)) + 2, fmt.format(tot), val_size, "Body-Bold",
                     INK, "middle")
            text(c, x0 + i * gw + gw / 2, y0 - 9, str(cat), cat_size, "Body", INK, "middle")
        if line:
            lname, lvals, lcol = line
            lv = [v for v in lvals if v is not None]
            lhi = line_axis_max or max(lv) * 1.15
            llo = min(0, min(lv))

            def YL(v):
                return y0 + (v - llo) / (lhi - llo) * (y1 - y0)
            for k in range(5):
                vv = llo + (lhi - llo) * k / 4
                text(c, x1 + 3, YL(vv) - 2.2, line_fmt.format(vv), 6.2, "Body", lcol)
            c.setStrokeColor(lcol)
            c.setLineWidth(1.5)
            pts = [(x0 + i * gw + gw / 2, YL(v)) for i, v in enumerate(lvals) if v is not None]
            p = c.beginPath()
            p.moveTo(*pts[0])
            for pt in pts[1:]:
                p.lineTo(*pt)
            c.drawPath(p, stroke=1, fill=0)
            c.setFillColor(lcol)
            for pt in pts:
                c.circle(pt[0], pt[1], 1.8, stroke=0, fill=1)
        if ylab:
            c.saveState()
            c.translate(8, (y0 + y1) / 2)
            c.rotate(90)
            text(c, 0, 0, ylab, 6.6, "Body-Italic", MUTED, "middle")
            c.restoreState()
        if legend and (len(series) > 1 or line):
            items = [(s[0], s[2], "bar") for s in series]
            if line:
                items.append((line[0], line[2], "line"))
            _legend(c, items, x0, 2)
    return CanvasFigure(w, h, draw)


# =============================================================================== horizontal bars
def hbar_chart(labels, values, w, h, title=None, sub=None, fmt="{:,.0f}", colors_=None,
               label_w=110, val_size=6.6, lab_size=7.0, ref=None, ref_label=None, notes=None):
    def draw(c, W, H):
        _title(c, W, H, title, sub)
        top = H - (26 if sub else 15 if title else 2)
        x0, x1 = label_w, W - 30
        vmin, vmax = min(values + [0]), max(values + [0])
        lo, hi, step = axis_range(vmin, vmax, 5)

        def X(v):
            return x0 + (v - lo) / (hi - lo) * (x1 - x0)
        n = len(labels)
        rh = (top - 12) / n
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        v = lo
        while v <= hi + 1e-9:
            c.line(X(v), 10, X(v), top)
            text(c, X(v), 2, fmt.format(v), 6.0, "Body", MUTED, "middle")
            v += step
        c.setStrokeColor(MUTED)
        c.line(X(0), 10, X(0), top)
        for i, (lab, v) in enumerate(zip(labels, values)):
            y = top - (i + 1) * rh
            col = colors_[i] if isinstance(colors_, list) else (colors_ or CARAMEL)
            c.setFillColor(col)
            xa, xb = X(0), X(v)
            c.rect(min(xa, xb), y + rh * 0.18, abs(xb - xa), rh * 0.64, stroke=0, fill=1)
            text(c, x0 - 4, y + rh / 2 - 2.4, lab, lab_size, "Body", INK, "end")
            if v >= 0:
                text(c, xb + 3, y + rh / 2 - 2.2, fmt.format(v), val_size, "Body-Bold", INK)
            else:
                text(c, xb - 3, y + rh / 2 - 2.2, fmt.format(v), val_size, "Body-Bold", BERRY, "end")
            if notes and notes[i]:
                text(c, W - 2, y + rh / 2 - 2.2, notes[i], 6.0, "Body-Italic", MUTED, "end")
        if ref is not None:
            c.setStrokeColor(BERRY)
            c.setDash(2, 2)
            c.line(X(ref), 10, X(ref), top)
            c.setDash()
            if ref_label:
                text(c, X(ref) + 2, top - 6, ref_label, 6.2, "Body-Italic", BERRY)
    return CanvasFigure(w, h, draw)


# =============================================================================== line chart
def line_chart(xlabels, series, w, h, title=None, sub=None, fmt="{:,.0f}", ylo=None, yhi=None,
               markers=True, annotations=(), band=None, legend=True, label_every=1, zero=False):
    """series: [(name, [values], colour, dashed?)]; annotations: [(i, value, text)]."""
    def draw(c, W, H):
        _title(c, W, H, title, sub)
        top = H - (26 if sub else 15 if title else 4)
        bottom = 22 if legend and len(series) > 1 else 14
        x0, x1, y0, y1 = 34, W - 8, bottom, top - 4
        vals = [v for s in series for v in s[1] if v is not None]
        lo, hi, step = axis_range(min(vals) if ylo is None else ylo,
                                  max(vals) if yhi is None else yhi, 5, zero=zero)

        def Y(v):
            return y0 + (v - lo) / (hi - lo) * (y1 - y0)
        n = len(xlabels)

        def X(i):
            return x0 + i / max(1, n - 1) * (x1 - x0)
        if band:
            a, b, lab = band
            c.setFillColor(rgba(GOLD, 0.18))
            c.rect(X(a), y0, X(b) - X(a), y1 - y0, stroke=0, fill=1)
            text(c, (X(a) + X(b)) / 2, y1 - 8, lab, 6.2, "Body-Italic", MUTED, "middle")
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        v = lo
        while v <= hi + 1e-9:
            c.line(x0, Y(v), x1, Y(v))
            text(c, x0 - 3, Y(v) - 2.2, fmt.format(v), 6.2, "Body", MUTED, "end")
            v += step
        for i, xl in enumerate(xlabels):
            if i % label_every == 0:
                text(c, X(i), y0 - 9, str(xl), 6.3, "Body", INK, "middle")
        for s in series:
            vs, col = s[1], s[2]
            dashed = len(s) > 3 and s[3]
            pts = [(X(i), Y(v)) for i, v in enumerate(vs) if v is not None]
            if not pts:
                continue
            c.setStrokeColor(col)
            c.setLineWidth(1.6)
            if dashed:
                c.setDash(3, 2)
            p = c.beginPath()
            p.moveTo(*pts[0])
            for pt in pts[1:]:
                p.lineTo(*pt)
            c.drawPath(p, stroke=1, fill=0)
            c.setDash()
            if markers:
                c.setFillColor(col)
                for pt in pts:
                    c.circle(pt[0], pt[1], 1.7, stroke=0, fill=1)
        for i, v, t in annotations:
            il.label_box(c, X(i) + 3, Y(v) + 4, t, 6.2, "start", "Body", INK)
        if legend and len(series) > 1:
            _legend(c, [(s[0], s[2], "line") for s in series], x0, 2)
    return CanvasFigure(w, h, draw)


# =============================================================================== waterfall
def waterfall(steps, w, h, title=None, sub=None, fmt="{:,.0f}", lab_size=6.4):
    """steps: [(label, value, kind)] kind in {'total', 'delta'}; totals are absolute."""
    def draw(c, W, H):
        _title(c, W, H, title, sub)
        top = H - (26 if sub else 15 if title else 4)
        x0, x1, y0, y1 = 36, W - 6, 24, top - 8
        run, bars = 0, []
        for lab, v, kind in steps:
            if kind == "total":
                bars.append((lab, 0, v, kind))
                run = v
            else:
                bars.append((lab, run, run + v, kind))
                run += v
        allv = [b[1] for b in bars] + [b[2] for b in bars]
        lo, hi, step = axis_range(min(allv), max(allv), 5)

        def Y(v):
            return y0 + (v - lo) / (hi - lo) * (y1 - y0)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        v = lo
        while v <= hi + 1e-9:
            c.line(x0, Y(v), x1, Y(v))
            text(c, x0 - 3, Y(v) - 2.2, fmt.format(v), 6.2, "Body", MUTED, "end")
            v += step
        n = len(bars)
        gw = (x1 - x0) / n
        bw = gw * 0.62
        prev_top = None
        for i, (lab, a, b, kind) in enumerate(bars):
            x = x0 + i * gw + (gw - bw) / 2
            col = ROAST if kind == "total" else (TEAL if b >= a else BERRY)
            c.setFillColor(col)
            c.rect(x, Y(min(a, b)), bw, abs(Y(b) - Y(a)), stroke=0, fill=1)
            val = b if kind == "total" else b - a
            text(c, x + bw / 2, Y(max(a, b)) + 2.5, ("" if kind == "total" or val < 0 else "+")
                 + fmt.format(val), 6.2, "Body-Bold", INK, "middle")
            if prev_top is not None:
                c.setStrokeColor(MUTED)
                c.setLineWidth(0.4)
                c.setDash(1.5, 1.5)
                c.line(prev_top[0], prev_top[1], x, prev_top[1])
                c.setDash()
            prev_top = (x + bw, Y(b))
            for k, ln in enumerate(il.wrap_lines(lab, "Body", lab_size, gw - 2)[:2]):
                text(c, x + bw / 2, y0 - 9 - k * 7.5, ln, lab_size, "Body", INK, "middle")
    return CanvasFigure(w, h, draw)


# =============================================================================== tornado
def tornado(labels, lows, highs, base, w, h, title=None, sub=None, fmt="{:,.0f}",
            low_lab="Low case", high_lab="High case", ranges=None):
    def draw(c, W, H):
        _title(c, W, H, title, sub)
        top = H - (26 if sub else 15 if title else 4)
        lab_w = 112
        x0, x1 = lab_w, W - 40
        order = sorted(range(len(labels)), key=lambda i: -abs(highs[i] - lows[i]))
        vals = lows + highs + [base]
        lo, hi, step = axis_range(min(vals), max(vals), 5, zero=False)

        def X(v):
            return x0 + (v - lo) / (hi - lo) * (x1 - x0)
        n = len(labels)
        rh = (top - 26) / n
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        v = lo
        while v <= hi + 1e-9:
            c.line(X(v), 22, X(v), top)
            text(c, X(v), 14, fmt.format(v), 6.0, "Body", MUTED, "middle")
            v += step
        for k, i in enumerate(order):
            y = top - (k + 1) * rh
            for v, col in ((lows[i], BERRY if lows[i] < base else TEAL),
                           (highs[i], TEAL if highs[i] > base else BERRY)):
                c.setFillColor(col)
                c.rect(min(X(base), X(v)), y + rh * 0.2, abs(X(v) - X(base)), rh * 0.6, stroke=0,
                       fill=1)
                anc = "end" if v < base else "start"
                text(c, X(v) + (-3 if v < base else 3), y + rh / 2 - 2.2, fmt.format(v), 6.0,
                     "Body", INK, anc)
            lab = labels[i] + (f"  ({ranges[i]})" if ranges else "")
            text(c, x0 - 4, y + rh / 2 - 2.4, lab, 6.7, "Body", INK, "end")
        c.setStrokeColor(INK)
        c.setLineWidth(0.9)
        c.line(X(base), 22, X(base), top + 2)
        text(c, X(base), top + 4, "Base " + fmt.format(base), 6.4, "Body-Bold", INK, "middle")
        _legend(c, [(low_lab + " (worse)", BERRY, "bar"), (high_lab + " (better)", TEAL, "bar")],
                x0, 2)
    return CanvasFigure(w, h, draw)


# =============================================================================== bubble / scatter
def bubble(points, w, h, title=None, sub=None, xlab="", ylab="", xfmt="{:,.0f}", yfmt="{:.0%}",
           xr=None, yr=None, size_scale=1.0, label_size=6.2, quad=None, show_labels=None):
    """points: [(label, x, y, size, colour)]"""
    def draw(c, W, H):
        _title(c, W, H, title, sub)
        top = H - (26 if sub else 15 if title else 4)
        x0, x1, y0, y1 = 40, W - 10, 26, top - 4
        xs = [p[1] for p in points]
        ys = [p[2] for p in points]
        xlo, xhi, xst = axis_range(*(xr or (min(xs), max(xs))), 5, zero=False)
        ylo, yhi, yst = axis_range(*(yr or (min(ys), max(ys))), 5, zero=False)

        def X(v):
            return x0 + (v - xlo) / (xhi - xlo) * (x1 - x0)

        def Y(v):
            return y0 + (v - ylo) / (yhi - ylo) * (y1 - y0)
        c.setFillColor(PANEL)
        c.rect(x0, y0, x1 - x0, y1 - y0, stroke=0, fill=1)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        v = xlo
        while v <= xhi + 1e-9:
            c.line(X(v), y0, X(v), y1)
            text(c, X(v), y0 - 8, xfmt.format(v), 6.0, "Body", MUTED, "middle")
            v += xst
        v = ylo
        while v <= yhi + 1e-9:
            c.line(x0, Y(v), x1, Y(v))
            text(c, x0 - 3, Y(v) - 2.2, yfmt.format(v), 6.0, "Body", MUTED, "end")
            v += yst
        if quad:
            qx, qy = quad
            c.setStrokeColor(MUTED)
            c.setDash(2, 2)
            if qx is not None:
                c.line(X(qx), y0, X(qx), y1)
            if qy is not None:
                c.line(x0, Y(qy), x1, Y(qy))
            c.setDash()
        for lab, x, y, s, col in sorted(points, key=lambda p: -p[3]):
            r = max(2.5, math.sqrt(max(s, 0)) * size_scale)
            c.setFillColor(rgba(col, 0.75))
            c.setStrokeColor(colors.white)
            c.setLineWidth(0.8)
            c.circle(X(x), Y(y), r, stroke=1, fill=1)
        for lab, x, y, s, col in points:
            if show_labels is not None and lab not in show_labels:
                continue
            r = max(2.5, math.sqrt(max(s, 0)) * size_scale)
            text(c, X(x) + r + 2, Y(y) - 2, lab, label_size, "Body", INK)
        text(c, (x0 + x1) / 2, 6, xlab, 6.8, "Body-Bold", MUTED, "middle")
        c.saveState()
        c.translate(9, (y0 + y1) / 2)
        c.rotate(90)
        text(c, 0, 0, ylab, 6.8, "Body-Bold", MUTED, "middle")
        c.restoreState()
    return CanvasFigure(w, h, draw)


# =============================================================================== gantt
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def gantt(rows, w, h, title=None, lab_w=150, labels=MONTHS):
    """rows: [(label, [(start, end)], colour, note)] in month units (0 = Jan)."""
    def draw(c, W, H):
        _title(c, W, H, title)
        top = H - (16 if title else 2) - 10
        x0, x1 = lab_w, W - 2
        n = len(labels)
        mw = (x1 - x0) / n
        rh = (top - 2) / len(rows)
        for i, m in enumerate(labels):
            if i % 2 == 0:
                c.setFillColor(HX("#F7F1E8"))
                c.rect(x0 + i * mw, 2, mw, top - 2, stroke=0, fill=1)
            text(c, x0 + i * mw + mw / 2, top + 3, m, 6.6, "Body-Bold", MUTED, "middle")
        for r, row in enumerate(rows):
            lab, spans, col = row[:3]
            note = row[3] if len(row) > 3 else ""
            y = top - (r + 1) * rh
            text(c, lab_w - 5, y + rh / 2 - 2.4, lab, 6.9, "Body", INK, "end")
            for a, b in spans:
                c.setFillColor(col)
                c.roundRect(x0 + a * mw + 1, y + 2, (b - a) * mw - 2, rh - 4, 2.5, stroke=0, fill=1)
            if note and spans:
                a, b = spans[0]
                txtc = colors.white if col not in (GOLD, HX("#F2C6D5")) else INK
                if sw(note, "Body", 6.0) < (b - a) * mw - 6:
                    text(c, x0 + a * mw + 4, y + rh / 2 - 2.2, note, 6.0, "Body", txtc)
    return CanvasFigure(w, h, draw)


# =============================================================================== process flow
def flow(steps, w, h, title=None, per_row=None, box_h=None, colors_=None, numbered=True,
         sub_size=6.2, head_size=7.4):
    """steps: [(head, sub)] drawn as a snake of rounded boxes joined by arrows."""
    def draw(c, W, H):
        _title(c, W, H, title)
        top = H - (14 if title else 0)
        n = len(steps)
        pr = per_row or n
        nrows = math.ceil(n / pr)
        gap = 12
        bw = (W - gap * (pr - 1)) / pr
        bh = box_h or (top - (nrows - 1) * 14) / nrows
        for i, (hd, sb) in enumerate(steps):
            r, k = divmod(i, pr)
            if r % 2 == 1:
                k = pr - 1 - k
            x = k * (bw + gap)
            y = top - (r + 1) * bh - r * 14
            col = colors_[i] if colors_ else SERIES[i % len(SERIES)]
            c.setFillColor(HX("#FFFFFF"))
            c.setStrokeColor(col)
            c.setLineWidth(1.0)
            c.roundRect(x, y, bw, bh, 4, stroke=1, fill=1)
            c.setFillColor(col)
            c.roundRect(x, y + bh - 13, bw, 13, 4, stroke=0, fill=1)
            c.rect(x, y + bh - 13, bw, 6, stroke=0, fill=1)
            head = (f"{i + 1}. " if numbered else "") + hd
            text(c, x + 4, y + bh - 9.6, head, head_size, "Body-Bold", colors.white)
            para(c, x + 4, y + bh - 21, sb, bw - 8, sub_size, "Body", INK, sub_size * 1.2)
            if i < n - 1:
                r2, k2 = divmod(i + 1, pr)
                if r2 == r:
                    if r % 2 == 0:
                        arrow(c, x + bw + 1, y + bh / 2, x + bw + gap - 1, y + bh / 2, MUTED, 0.9, 3.5)
                    else:
                        arrow(c, x - 1, y + bh / 2, x - gap + 1, y + bh / 2, MUTED, 0.9, 3.5)
                else:
                    arrow(c, x + bw / 2, y - 1, x + bw / 2, y - 13, MUTED, 0.9, 3.5)
    return CanvasFigure(w, h, draw)


# =============================================================================== brewing control chart
def control_chart(w, h, points=()):
    def draw(c, W, H):
        _title(c, W, H, "The brewing control chart: strength vs extraction",
               "Filter coffee. Diagonal lines = brew ratio (grams of water per gram of coffee)")
        x0, x1, y0, y1 = 40, W - 70, 28, H - 32
        exlo, exhi, tdlo, tdhi = 14, 26, 0.9, 1.6

        def X(e):
            return x0 + (e - exlo) / (exhi - exlo) * (x1 - x0)

        def Y(t):
            return y0 + (t - tdlo) / (tdhi - tdlo) * (y1 - y0)
        zones = [((14, 18), (1.35, 1.6), "STRONG\nUNDER-EXTRACTED", HX("#F9E0D9")),
                 ((18, 22), (1.35, 1.6), "STRONG", HX("#FBEBD5")),
                 ((22, 26), (1.35, 1.6), "STRONG\nBITTER", HX("#F9E0D9")),
                 ((14, 18), (1.15, 1.35), "UNDER-EXTRACTED\nsour, thin", HX("#FBEBD5")),
                 ((18, 22), (1.15, 1.35), "IDEAL", HX("#D8F0DC")),
                 ((22, 26), (1.15, 1.35), "OVER-EXTRACTED\nbitter, dry", HX("#FBEBD5")),
                 ((14, 18), (0.9, 1.15), "WEAK\nUNDER-EXTRACTED", HX("#F9E0D9")),
                 ((18, 22), (0.9, 1.15), "WEAK", HX("#FBEBD5")),
                 ((22, 26), (0.9, 1.15), "WEAK\nBITTER", HX("#F9E0D9"))]
        for (ea, eb), (ta, tb), lab, col in zones:
            c.setFillColor(col)
            c.rect(X(ea), Y(ta), X(eb) - X(ea), Y(tb) - Y(ta), stroke=0, fill=1)
            for k, ln in enumerate(lab.split("\n")):
                text(c, (X(ea) + X(eb)) / 2, (Y(ta) + Y(tb)) / 2 + 2 - k * 7.5, ln, 6.2 if k else 6.8,
                     "Body-Bold" if k == 0 else "Body-Italic",
                     LEAF if lab == "IDEAL" else MUTED, "middle")
        c.setStrokeColor(colors.white)
        c.setLineWidth(1.2)
        for e in (18, 22):
            c.line(X(e), y0, X(e), y1)
        for t in (1.15, 1.35):
            c.line(x0, Y(t), x1, Y(t))
        for e in range(14, 27, 2):
            text(c, X(e), y0 - 9, f"{e}%", 6.2, "Body", MUTED, "middle")
        for t in (0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6):
            text(c, x0 - 3, Y(t) - 2.2, f"{t:.1f}%", 6.2, "Body", MUTED, "end")
        # brew-ratio diagonals: TDS = EY * dose / beverage ; beverage = water - 2*dose
        c.setStrokeColor(rgba(ROAST, 0.55))
        c.setLineWidth(0.7)
        for ratio in (14, 15, 16, 17, 18, 19, 20):
            k = 1 / (ratio - 2.0)
            pts = []
            for e in (exlo, exhi):
                t = e / 100 * k * 100
                pts.append((e, t))
            (ea, ta), (eb, tb) = pts
            # clip to box
            def clip(e, t):
                if t > tdhi:
                    e = tdhi / (k * 100) * 100
                    t = tdhi
                if t < tdlo:
                    e = tdlo / (k * 100) * 100
                    t = tdlo
                return e, t
            ea, ta = clip(ea, ta)
            eb, tb = clip(eb, tb)
            c.setDash(2, 2)
            c.line(X(ea), Y(ta), X(eb), Y(tb))
            c.setDash()
            text(c, X(eb) + 2, Y(tb) - 2, f"1:{ratio}", 6.0, "Body", ROAST)
        for lab, e, t in points:
            c.setFillColor(BERRY)
            c.circle(X(e), Y(t), 2.4, stroke=0, fill=1)
            text(c, X(e) + 4, Y(t) + 1, lab, 6.2, "Body-Bold", BERRY)
        text(c, (x0 + x1) / 2, 6, "Extraction yield: % of the coffee's weight dissolved into the cup  →",
             6.8, "Body-Bold", MUTED, "middle")
        c.saveState()
        c.translate(9, (y0 + y1) / 2)
        c.rotate(90)
        text(c, 0, 0, "Strength: total dissolved solids (TDS)  →", 6.8, "Body-Bold", MUTED, "middle")
        c.restoreState()
    return CanvasFigure(w, h, draw)


# =============================================================================== donut
def donut(values, labels, cols, w, h, centre="", centre_sub="", title=None, fmt="{:.0%}"):
    def draw(c, W, H):
        _title(c, W, H, title)
        cy = (H - (14 if title else 0)) / 2
        r = min(cy - 4, W * 0.22)
        cx = r + 6
        tot = sum(values)
        ang = 90
        for v, col in zip(values, cols):
            ext = 360 * v / tot
            c.setFillColor(col)
            c.setStrokeColor(colors.white)
            c.setLineWidth(1)
            p = c.beginPath()
            p.moveTo(cx, cy)
            p.arcTo(cx - r, cy - r, cx + r, cy + r, ang, -ext)
            p.close()
            c.drawPath(p, stroke=1, fill=1)
            ang -= ext
        c.setFillColor(R.PAPER)
        c.circle(cx, cy, r * 0.58, stroke=0, fill=1)
        text(c, cx, cy + 1, centre, 10, "Body-Bold", ESPRESSO, "middle")
        text(c, cx, cy - 8, centre_sub, 6.2, "Body", MUTED, "middle")
        lx = cx + r + 14
        lh = min(13, (2 * r) / max(1, len(labels)))
        ly = cy + lh * len(labels) / 2 - lh
        for i, (lab, v, col) in enumerate(zip(labels, values, cols)):
            y = ly - i * lh
            c.setFillColor(col)
            c.rect(lx, y, 8, 7, stroke=0, fill=1)
            text(c, lx + 12, y + 0.8, lab, 6.9, "Body", INK)
            text(c, W - 4, y + 0.8, fmt.format(v / tot) if fmt else "", 6.9, "Body-Bold", INK, "end")
    return CanvasFigure(w, h, draw)


# =============================================================================== heat table
def heat_color(v, lo, mid, hi):
    if v is None or isinstance(v, str):
        return HX("#EEEEEE")
    if v < mid:
        t = max(0.0, min(1.0, (mid - v) / max(1e-9, mid - lo)))
        return colors.Color(1 - 0.05 * t, 1 - 0.38 * t, 1 - 0.40 * t)
    t = max(0.0, min(1.0, (v - mid) / max(1e-9, hi - mid)))
    return colors.Color(1 - 0.42 * t, 1 - 0.12 * t, 1 - 0.36 * t)


def heat_table(row_labels, col_labels, values, fmt, col_w, first_w, corner="", mid=0,
               lo=None, hi=None, font=7.4, bold_cell=None, head_color=ROAST):
    flat = [v for r in values for v in r if isinstance(v, (int, float))]
    lo = min(flat) if lo is None else lo
    hi = max(flat) if hi is None else hi
    cs = R.ParagraphStyle("ht", fontName="Body", fontSize=font, leading=font + 2, alignment=1)
    csb = R.ParagraphStyle("htb", parent=cs, fontName="Body-Bold")
    hs = R.ParagraphStyle("hth", fontName="Body-Bold", fontSize=font, leading=font + 2,
                          textColor=colors.white, alignment=1)
    ls = R.ParagraphStyle("htl", fontName="Body-Bold", fontSize=font, leading=font + 2)
    data = [[R.P(corner, hs)] + [R.P(cl, hs) for cl in col_labels]]
    style = [("BACKGROUND", (0, 0), (-1, 0), head_color), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
             ("GRID", (0, 0), (-1, -1), 0.6, colors.white),
             ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]
    for i, (rl, row) in enumerate(zip(row_labels, values), start=1):
        cells = [R.P(rl, ls)]
        for j, v in enumerate(row, start=1):
            s = fmt(v) if isinstance(v, (int, float)) else str(v)
            cells.append(R.P(s, csb if bold_cell == (i - 1, j - 1) else cs))
            style.append(("BACKGROUND", (j, i), (j, i), heat_color(v, lo, mid, hi)))
            if bold_cell == (i - 1, j - 1):
                style.append(("BOX", (j, i), (j, i), 1.2, ESPRESSO))
        style.append(("BACKGROUND", (0, i), (0, i), HX("#F7F1E8")))
        data.append(cells)
    t = Table(data, colWidths=[first_w] + [col_w] * len(col_labels))
    t.setStyle(TableStyle(style))
    return t


def shade_of(col, f):
    return shade(col, f)
