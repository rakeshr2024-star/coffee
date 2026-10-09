"""Illustrations for the Coffee 101 primer in Final_Coff.pdf.

Two kinds of artwork, both generated in code (no external images):
  * raster "specimen" renders of cherries and beans (PIL + numpy height-field shading),
  * vector scenes and diagrams drawn straight onto the ReportLab canvas.
Everything is an illustration, not a photograph.  Fonts ("Body", "Body-Bold",
"Body-Italic", "Head", "Sym") are registered by build_report.py before drawing.
"""
import math

import numpy as np
from PIL import Image, ImageFilter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Flowable

HX = colors.HexColor
INK = HX("#2D2A26")
MUTED = HX("#7A6F66")
RULE = HX("#E6DCCF")
CREAM = HX("#FBF6EF")
ROAST = HX("#6F4E37")
CARAMEL = HX("#C68B59")
ESPRESSO = HX("#2B1A12")
TEAL = HX("#1B998B")
SAFFRON = HX("#F29E4C")
LEAF_C = HX("#3A7D44")
BERRY = HX("#C0392B")
PLUM = HX("#6A4C93")
SKY = HX("#2E86AB")
GOLD = HX("#E9C46A")


def rgba(col, a):
    return colors.Color(col.red, col.green, col.blue, alpha=a)


def shade(col, f):
    """Darken (f<1) or lighten (f>1, towards white) a colour."""
    if f <= 1:
        return colors.Color(col.red * f, col.green * f, col.blue * f)
    t = f - 1
    return colors.Color(col.red + (1 - col.red) * t, col.green + (1 - col.green) * t,
                        col.blue + (1 - col.blue) * t)


class CanvasFigure(Flowable):
    """A fixed-size flowable whose content is drawn by draw_fn(canvas, width, height)."""

    def __init__(self, width, height, draw_fn):
        super().__init__()
        self.width, self.height, self.draw_fn = width, height, draw_fn

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.draw_fn(self.canv, self.width, self.height)
        self.canv.restoreState()


# =========================================================================== raster renders
_CACHE = {}


def _noise(h, w, cell, rng):
    small = rng.random((max(2, h // cell), max(2, w // cell)))
    img = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(img, dtype=np.float32) / 255.0


def _lighting(height, light=(-0.45, -0.55, 0.70)):
    gy, gx = np.gradient(height)
    n = np.dstack([-gx, -gy, np.ones_like(height)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    L = np.array(light, dtype=np.float32)
    L /= np.linalg.norm(L)
    diff = np.clip((n * L).sum(2), 0, 1)
    half = L + np.array([0, 0, 1.0], dtype=np.float32)
    half /= np.linalg.norm(half)
    spec = np.clip((n * half).sum(2), 0, 1)
    return diff, spec


def _shadow(alpha, W, H, ss, dx=0.025, dy=0.045, blur=0.03, opacity=0.33):
    a = Image.fromarray((alpha * 255).astype(np.uint8))
    a = a.transform(a.size, Image.AFFINE, (1, 0, -dx * W * ss, 0, 1, -dy * W * ss))
    a = a.filter(ImageFilter.GaussianBlur(blur * W * ss))
    return np.asarray(a, dtype=np.float32) / 255.0 * opacity


def _compose(rgb, alpha, shadow, shadow_rgb=(45, 28, 18)):
    a_out = alpha + shadow * (1 - alpha)
    sh = np.array(shadow_rgb, dtype=np.float32) / 255.0
    col = (rgb * alpha[..., None] + sh * (shadow * (1 - alpha))[..., None])
    col = col / np.maximum(a_out[..., None], 1e-4)
    out = np.dstack([np.clip(col, 0, 1), np.clip(a_out, 0, 1)])
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


BEANS = {
    # colour, shape, size (relative), crease depth, mottle, grain, specular, shininess, chaff, oil
    "parchment": dict(rgb=(226, 210, 172), shape="arabica", size=1.10, crease=0.22, mottle=0.04,
                      grain=0.05, spec=0.06, shin=8, streaks=True),
    "green": dict(rgb=(126, 148, 118), shape="arabica", size=1.0, crease=1.0, mottle=0.13,
                  grain=0.04, spec=0.12, shin=14),
    "green_natural": dict(rgb=(156, 150, 104), shape="arabica", size=1.0, crease=1.0, mottle=0.14,
                          grain=0.04, spec=0.10, shin=14),
    "robusta": dict(rgb=(140, 138, 106), shape="robusta", size=0.86, crease=0.9, mottle=0.12,
                    grain=0.05, spec=0.10, shin=14),
    "peaberry": dict(rgb=(126, 148, 118), shape="peaberry", size=0.84, crease=0.0, mottle=0.12,
                     grain=0.04, spec=0.14, shin=14),
    "monsooned": dict(rgb=(214, 188, 128), shape="arabica", size=1.16, crease=0.8, mottle=0.08,
                      grain=0.05, spec=0.06, shin=10),
    "yellow": dict(rgb=(206, 180, 110), shape="arabica", size=1.03, crease=1.0, mottle=0.07,
                   grain=0.04, spec=0.08, shin=12, chaff=0.8),
    "cinnamon": dict(rgb=(176, 118, 66), shape="arabica", size=1.08, crease=1.0, mottle=0.05,
                     grain=0.04, spec=0.10, shin=14, chaff=0.7),
    "light": dict(rgb=(144, 91, 50), shape="arabica", size=1.13, crease=1.0, mottle=0.05,
                  grain=0.04, spec=0.12, shin=16, chaff=0.55),
    "medium": dict(rgb=(110, 67, 37), shape="arabica", size=1.17, crease=1.0, mottle=0.04,
                   grain=0.04, spec=0.16, shin=18, chaff=0.35),
    "medium_dark": dict(rgb=(80, 48, 28), shape="arabica", size=1.20, crease=1.0, mottle=0.04,
                        grain=0.04, spec=0.20, shin=24, chaff=0.12, oil=0.25),
    "dark": dict(rgb=(46, 28, 18), shape="arabica", size=1.23, crease=1.0, mottle=0.03,
                 grain=0.04, spec=0.45, shin=30, oil=1.0),
}


def render_bean(kind, px=300, seed=3):
    """Flat face of a coffee bean (crease side up), lit from the top-left, with a soft shadow."""
    key = ("bean", kind, px, seed)
    if key in _CACHE:
        return _CACHE[key]
    st = BEANS[kind]
    ss = 2
    W, H = px, int(px * 0.78)
    w, h = W * ss, H * ss
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w * 0.47, h * 0.46
    ratio = {"arabica": 0.70, "robusta": 0.80, "peaberry": 0.64}[st["shape"]]
    a = 0.34 * w * st["size"]
    b = a * ratio
    if st["shape"] == "peaberry":
        a *= 0.96
    u = (xx - cx) / a
    v = (yy - cy) / (b * (1 - 0.07 * u))  # slightly egg-shaped: one end narrower
    r2 = u * u + v * v
    r = np.sqrt(r2)
    inside = np.clip(1 - r2, 0, 1)
    z = inside ** (0.5 if st["shape"] == "peaberry" else 0.40)
    # crease: S-curve (arabica), straight (robusta); tapers towards the tips
    s_amp = {"arabica": 0.11, "robusta": 0.02, "peaberry": 0.0}[st["shape"]]
    yc = s_amp * np.sin(np.pi * u * 0.95)
    taper = np.sqrt(np.clip(1 - (u / 0.84) ** 2, 0, 1))
    wid = 0.075 * taper + 1e-3
    d = v - yc
    crease = np.exp(-(d / wid) ** 2) * (taper > 0)
    lips = np.exp(-((np.abs(d) - 1.9 * wid) / (1.2 * wid + 1e-3)) ** 2) * (taper > 0)
    height = z - 0.42 * st["crease"] * crease + 0.05 * st["crease"] * lips
    if st["shape"] == "peaberry":
        height = height - 0.10 * np.exp(-(v / 0.05) ** 2) * taper  # faint seam
    diff, spec = _lighting(height * b * 0.55)
    base = np.array(st["rgb"], dtype=np.float32) / 255.0
    tex = 1 + st["mottle"] * (_noise(h, w, 22 * ss, rng) - 0.5) * 2 \
        + st["grain"] * (_noise(h, w, 2 * ss, rng) - 0.5) * 2
    if st.get("streaks"):
        tex += 0.07 * (_noise(h, w // 14, 1, rng)[:, np.minimum(np.arange(w) // 14, w // 14 - 1)]
                       - 0.5)
    light = 0.40 + 0.78 * diff
    col = base * (tex * light)[..., None]
    col *= (1 - 0.50 * st["crease"] * crease)[..., None]
    chaff = st.get("chaff", 0)
    if chaff:
        core = np.exp(-(d / (0.38 * wid)) ** 2) * (taper > 0.15)
        chaff_rgb = np.array([0.86, 0.76, 0.58]) * (0.55 + 0.5 * diff)[..., None]
        col = col * (1 - chaff * core)[..., None] + chaff_rgb * (chaff * core)[..., None]
    oil = st.get("oil", 0)
    spec_amt = st["spec"] * np.ones_like(diff)
    if oil:
        blobs = _noise(h, w, 18 * ss, rng)
        oil_mask = np.clip((blobs - (0.62 - 0.45 * oil)) * 4, 0, 1) * oil
        spec_amt = spec_amt + 0.55 * oil_mask
        col *= (1 - 0.12 * oil_mask)[..., None]
    col += (spec ** st["shin"] * spec_amt)[..., None]
    col *= (0.86 + 0.14 * z)[..., None]
    alpha = np.clip((1 - r) / 0.018, 0, 1)
    img = _compose(np.clip(col, 0, 1), alpha, _shadow(alpha, W, H, ss))
    img = img.resize((W, H), Image.LANCZOS)
    _CACHE[key] = img
    return img


CHERRIES = {
    "unripe": dict(rgb=(92, 146, 54)),
    "turning": dict(rgb=(170, 182, 58)),
    "orange": dict(rgb=(228, 150, 38)),
    "ripe": dict(rgb=(188, 24, 34)),
    "overripe": dict(rgb=(98, 16, 38)),
    "dried": dict(rgb=(84, 38, 30), dried=True),
}


def render_cherry(kind, px=160, seed=5):
    key = ("cherry", kind, px, seed)
    if key in _CACHE:
        return _CACHE[key]
    st = CHERRIES[kind]
    ss = 2
    W = H = px
    w, h = W * ss, H * ss
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w * 0.47, h * 0.47
    rx, ry = 0.37 * w, 0.325 * w
    if st.get("dried"):
        rx, ry = rx * 0.86, ry * 0.84
        ang = np.arctan2(yy - cy, xx - cx)
        wob = 1 + 0.035 * np.sin(5 * ang + 1.3) + 0.02 * np.sin(9 * ang)
        rx_m, ry_m = rx * wob, ry * wob
    else:
        rx_m, ry_m = rx, ry
    u, v = (xx - cx) / rx_m, (yy - cy) / ry_m
    r2 = u * u + v * v
    r = np.sqrt(r2)
    z = np.sqrt(np.clip(1 - r2, 0, 1))
    height = z.copy()
    if st.get("dried"):
        height += 0.10 * (_noise(h, w, 9 * ss, rng) - 0.5) + 0.05 * (_noise(h, w, 4 * ss, rng) - 0.5)
    # navel (the little disc at the blossom end), lower right
    nu, nv = 0.38, 0.40
    nd = np.sqrt((u - nu) ** 2 + (v - nv) ** 2)
    height -= 0.06 * np.exp(-(nd / 0.07) ** 2)
    diff, spec = _lighting(height * ry * 0.9)
    base = np.array(st["rgb"], dtype=np.float32) / 255.0
    tex = 1 + 0.07 * (_noise(h, w, 30 * ss, rng) - 0.5) * 2
    col = base * (tex * (0.30 + 0.85 * diff))[..., None]
    ring = np.exp(-((nd - 0.085) / 0.022) ** 2)
    disc = np.exp(-(nd / 0.05) ** 2)
    col *= (1 - 0.55 * ring)[..., None]
    col = col * (1 - 0.6 * disc)[..., None] + np.array([0.42, 0.30, 0.18]) * (0.6 * disc)[..., None]
    gloss = 0.12 if st.get("dried") else 0.50
    col += (spec ** (12 if st.get("dried") else 46) * gloss)[..., None]
    col += (spec ** 6 * (0.03 if st.get("dried") else 0.10))[..., None]
    alpha = np.clip((1 - r) / 0.02, 0, 1)
    img = _compose(np.clip(col, 0, 1), alpha, _shadow(alpha, W, H, ss, dx=0.02, dy=0.04,
                                                       blur=0.035, opacity=0.28))
    img = img.resize((W, H), Image.LANCZOS)
    _CACHE[key] = img
    return img


def draw_pil(c, img, x, y, w, h=None):
    if h is None:
        h = w * img.size[1] / img.size[0]
    c.saveState()
    c.setFillAlpha(1)
    c.drawImage(ImageReader(img), x, y, w, h, mask="auto")
    c.restoreState()


# =========================================================================== vector helpers
def text(c, x, y, s, size=7.4, font="Body", color=INK, anchor="start"):
    c.setFont(font, size)
    c.setFillColor(color)
    if anchor == "middle":
        c.drawCentredString(x, y, s)
    elif anchor == "end":
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)


def wrap_lines(s, font, size, max_w):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if pdfmetrics.stringWidth(t, font, size) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def para(c, x, y, s, max_w, size=7.2, font="Body", color=INK, leading=None, anchor="start"):
    leading = leading or size * 1.22
    for i, ln in enumerate(wrap_lines(s, font, size, max_w)):
        text(c, x, y - i * leading, ln, size, font, color, anchor)
    return len(wrap_lines(s, font, size, max_w)) * leading


def label_box(c, x, y, s, size=7, anchor="start", font="Body-Bold", fg=INK,
              bg=colors.Color(1, 1, 1, alpha=0.86), pad=2.6):
    tw = pdfmetrics.stringWidth(s, font, size)
    bx = x if anchor == "start" else (x - tw - 2 * pad if anchor == "end" else x - tw / 2 - pad)
    c.setFillColor(bg)
    c.setStrokeColor(rgba(ROAST, 0.35))
    c.setLineWidth(0.4)
    c.roundRect(bx, y - pad, tw + 2 * pad, size + 2 * pad - 1, 2.5, stroke=1, fill=1)
    text(c, bx + pad, y + 0.6, s, size, font, fg)
    return bx, tw + 2 * pad


def leader(c, x0, y0, x1, y1, color=ROAST):
    c.setStrokeColor(color)
    c.setLineWidth(0.6)
    c.line(x0, y0, x1, y1)
    c.setFillColor(color)
    c.circle(x1, y1, 1.4, stroke=0, fill=1)


def callout_num(c, x, y, n, color=ROAST, r=6):
    c.setFillColor(color)
    c.circle(x, y, r, stroke=0, fill=1)
    text(c, x, y - 2.6, str(n), 7.4, "Body-Bold", colors.white, "middle")


def grad_fill(c, path, kind, args, cols, positions=None):
    c.saveState()
    c.clipPath(path, stroke=0, fill=0)
    if kind == "linear":
        c.linearGradient(*args, cols, positions)
    else:
        c.radialGradient(*args, cols, positions)
    c.restoreState()


def arrow(c, x0, y0, x1, y1, color=MUTED, width=1.0, head=4):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x0, y0, x1, y1)
    ang = math.atan2(y1 - y0, x1 - x0)
    p = c.beginPath()
    p.moveTo(x1, y1)
    p.lineTo(x1 - head * math.cos(ang - 0.45), y1 - head * math.sin(ang - 0.45))
    p.lineTo(x1 - head * math.cos(ang + 0.45), y1 - head * math.sin(ang + 0.45))
    p.close()
    c.setFillColor(color)
    c.drawPath(p, stroke=0, fill=1)


def leaf(c, x, y, length, width, angle, light=HX("#4F8A3C"), dark=HX("#1E4A22")):
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    p = c.beginPath()
    p.moveTo(0, 0)
    p.curveTo(length * 0.14, width * 0.50, length * 0.33, width * 0.60, length * 0.52, width * 0.50)
    p.curveTo(length * 0.62, width * 0.44, length * 0.66, width * 0.50, length * 0.76, width * 0.36)
    p.curveTo(length * 0.88, width * 0.20, length * 0.95, width * 0.06, length, 0)
    p.curveTo(length * 0.93, -width * 0.10, length * 0.84, -width * 0.30, length * 0.70, -width * 0.42)
    p.curveTo(length * 0.58, -width * 0.52, length * 0.50, -width * 0.44, length * 0.38, -width * 0.54)
    p.curveTo(length * 0.22, -width * 0.62, length * 0.10, -width * 0.42, 0, 0)
    p.close()
    grad_fill(c, p, "linear", (0, width * 0.6, length * 0.3, -width * 0.6), (light, dark))
    c.setStrokeColor(shade(dark, 0.7))
    c.setLineWidth(0.4)
    c.drawPath(p, stroke=1, fill=0)
    c.setStrokeColor(rgba(HX("#CFE3B8"), 0.75))
    c.setLineWidth(0.7)
    c.line(0, 0, length * 0.96, 0)
    c.setLineWidth(0.35)
    for t in (0.16, 0.30, 0.44, 0.58, 0.72):
        for sgn in (1, -1):
            q = c.beginPath()
            q.moveTo(length * t, 0)
            q.curveTo(length * (t + 0.05), sgn * width * 0.16, length * (t + 0.10), sgn * width * 0.28,
                      length * (t + 0.15), sgn * width * 0.36 * (1 - t * 0.6))
            c.drawPath(q, stroke=1, fill=0)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.13))
    hl = c.beginPath()
    hl.moveTo(length * 0.1, width * 0.12)
    hl.curveTo(length * 0.3, width * 0.42, length * 0.55, width * 0.36, length * 0.75, width * 0.12)
    hl.curveTo(length * 0.5, width * 0.22, length * 0.3, width * 0.22, length * 0.1, width * 0.12)
    c.drawPath(hl, stroke=0, fill=1)
    c.restoreState()


def flower(c, x, y, r, angle=0):
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    for k in range(5):
        c.saveState()
        c.rotate(k * 72)
        p = c.beginPath()
        p.moveTo(0, 0)
        p.curveTo(r * 0.25, r * 0.30, r * 0.85, r * 0.28, r, 0)
        p.curveTo(r * 0.85, -r * 0.28, r * 0.25, -r * 0.30, 0, 0)
        grad_fill(c, p, "linear", (0, 0, r, 0), (HX("#EDEDE6"), colors.white))
        c.setStrokeColor(HX("#C9C9BE"))
        c.setLineWidth(0.3)
        c.drawPath(p, stroke=1, fill=0)
        c.restoreState()
    c.setStrokeColor(HX("#E8E2C0"))
    c.setLineWidth(0.4)
    for k in range(5):
        a = math.radians(k * 72 + 36)
        c.line(0, 0, r * 0.62 * math.cos(a), r * 0.62 * math.sin(a))
        c.setFillColor(HX("#C9B458"))
        c.circle(r * 0.62 * math.cos(a), r * 0.62 * math.sin(a), r * 0.07, stroke=0, fill=1)
    c.setFillColor(HX("#D9E4B0"))
    c.circle(0, 0, r * 0.12, stroke=0, fill=1)
    c.restoreState()


def bud(c, x, y, r, angle):
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    c.setFillColor(HX("#F4F2E8"))
    c.setStrokeColor(HX("#C9C9BE"))
    c.setLineWidth(0.3)
    c.ellipse(0, -r * 0.35, r * 1.6, r * 0.35, stroke=1, fill=1)
    c.restoreState()


# =========================================================================== scenes
def estate_scene(c, w, h):
    """Shade-grown Indian coffee estate in the Western Ghats (stylised)."""
    frame = c.beginPath()
    frame.roundRect(0, 0, w, h, 6)
    c.saveState()
    c.clipPath(frame, stroke=0, fill=0)
    c.linearGradient(0, h, 0, 0, (HX("#BFDDEE"), HX("#F5EFE2")))
    # far hills
    for k, (base, amp, col) in enumerate([(0.62, 0.10, HX("#A7C3B7")), (0.52, 0.09, HX("#87AF94"))]):
        p = c.beginPath()
        p.moveTo(0, 0)
        p.lineTo(0, h * base)
        for i in range(0, 41):
            x = w * i / 40
            y = h * (base + amp * math.sin(i * 0.55 + k * 1.7) * math.sin(i * 0.17 + 0.4 + k))
            p.lineTo(x, y)
        p.lineTo(w, 0)
        p.close()
        c.setFillColor(col)
        c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.25))
    c.rect(0, h * 0.42, w, h * 0.16, stroke=0, fill=1)

    def ground_y(x):
        return h * 0.40 - x / w * h * 0.10

    g = c.beginPath()
    g.moveTo(0, 0)
    g.lineTo(0, ground_y(0))
    g.lineTo(w, ground_y(w))
    g.lineTo(w, 0)
    g.close()
    grad_fill(c, g, "linear", (0, h * 0.4, 0, 0), (HX("#7BA35A"), HX("#4C7536")))

    def canopy_tree(x, top, rad):
        gy = ground_y(x)
        c.setFillColor(HX("#5B4636"))
        c.rect(x - 3.5, gy - 4, 7, top - gy, stroke=0, fill=1)
        rng = np.random.default_rng(int(x))
        for _ in range(9):
            ox, oy = rng.uniform(-1.3, 1.3) * rad, rng.uniform(-0.45, 0.6) * rad
            rr = rad * rng.uniform(0.55, 0.85)
            p = c.beginPath()
            p.circle(x + ox, top + oy, rr)
            grad_fill(c, p, "radial", (x + ox - rr * 0.4, top + oy + rr * 0.4, rr * 1.4),
                      (HX("#6E9E4E"), HX("#2F5B2B")))

    def silver_oak(x, top):
        gy = ground_y(x)
        c.setFillColor(HX("#6B5B4E"))
        c.rect(x - 1.8, gy - 3, 3.6, top - gy, stroke=0, fill=1)
        for i in range(9):
            yy = top - i * 7
            ww = 7 + 3 * math.sin(i * 1.3)
            c.setFillColor(HX("#7F9C6E") if i % 2 else HX("#6D8B5E"))
            c.ellipse(x - ww, yy - 5, x + ww, yy + 5, stroke=0, fill=1)
        # black-pepper vine spiralling up the trunk
        for i in range(26):
            yy = gy + 2 + i * (top - 48 - gy) / 26
            xx = x + 3.2 * math.sin(i * 1.1)
            c.setFillColor(HX("#24502A"))
            c.ellipse(xx - 2.4, yy - 1.4, xx + 2.4, yy + 1.4, stroke=0, fill=1)

    for x, top, rad in [(40, h * 0.86, 30), (215, h * 0.90, 34), (418, h * 0.84, 30)]:
        canopy_tree(x, top, rad)
    for x, top in [(118, h * 0.94), (300, h * 0.95), (480, h * 0.90)]:
        silver_oak(x, top)

    rng = np.random.default_rng(11)

    def bush(x, scale):
        gy = ground_y(x) - (1 - scale) * 0
        bh, bw = 34 * scale, 26 * scale
        for ox, oy, rr in [(-0.55, 0.45, 0.62), (0.55, 0.45, 0.62), (0, 0.75, 0.70), (0, 0.35, 0.75)]:
            p = c.beginPath()
            p.ellipse(x + ox * bw - rr * bw, gy + oy * bh - rr * bh * 0.75,
                      2 * rr * bw, 1.5 * rr * bh)
            grad_fill(c, p, "radial", (x + ox * bw - rr * bw * 0.3, gy + oy * bh + rr * bh * 0.4,
                                       rr * bw * 1.6), (HX("#3F7A35"), HX("#1C3F1E")))
        for _ in range(int(16 * scale)):
            px_ = x + rng.uniform(-1.1, 1.1) * bw
            py_ = gy + rng.uniform(0.15, 1.05) * bh
            c.setFillColor(HX("#C0392B") if rng.random() > 0.3 else HX("#E0A13A"))
            c.circle(px_, py_, 1.3 * scale + 0.3, stroke=0, fill=1)

    for row, (dy, scale, xs) in enumerate([(-14, 0.62, range(20, int(w), 38)),
                                            (-34, 0.80, range(5, int(w), 50)),
                                            (-58, 1.0, range(30, int(w), 62))]):
        for x in xs:
            gy0 = ground_y(x)
            c.saveState()
            c.translate(0, dy)
            bush(x, scale)
            c.restoreState()

    # picker with a basket, for scale
    px0 = 262
    py0 = ground_y(px0) - 60
    c.setFillColor(HX("#3B2A20"))
    c.circle(px0, py0 + 41, 3.6, stroke=0, fill=1)
    sari = c.beginPath()
    sari.moveTo(px0 - 4, py0 + 37)
    sari.lineTo(px0 + 4, py0 + 37)
    sari.lineTo(px0 + 7, py0)
    sari.lineTo(px0 - 7, py0)
    sari.close()
    c.setFillColor(HX("#E07A2E"))
    c.drawPath(sari, stroke=0, fill=1)
    c.setFillColor(HX("#B35B1E"))
    c.rect(px0 - 4, py0 + 24, 8, 3, stroke=0, fill=1)
    c.setFillColor(HX("#A27B4E"))
    c.roundRect(px0 + 5, py0 + 14, 9, 8, 2, stroke=0, fill=1)
    c.setStrokeColor(HX("#3B2A20"))
    c.setLineWidth(1.4)
    c.line(px0 + 3, py0 + 33, px0 + 9, py0 + 22)
    c.restoreState()

    # labels
    leader(c, 70, h * 0.93, 46, h * 0.86)
    label_box(c, 72, h * 0.92, "Upper canopy: native shade trees", 6.8)
    leader(c, 135, h * 0.72, 120, h * 0.68)
    label_box(c, 137, h * 0.71, "Silver oak trees carrying black-pepper vines", 6.8)
    leader(c, 340, 70, 330, 52)
    label_box(c, 342, 69, "Coffee bushes, pruned to ~1.5-2 m for hand-picking", 6.8)
    leader(c, 240, 18, 258, 28)
    label_box(c, 160, 12, "Pickers take only ripe cherries", 6.8)
    label_box(c, w - 6, h - 14, "Western Ghats hills: arabica at ~1,000-1,600 m", 6.8, anchor="end")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.roundRect(0, 0, w, h, 6, stroke=1, fill=0)


def branch_scene(c, w, h):
    """A fruiting branch (uneven ripening) and a flowering sprig."""
    c.setFillColor(CREAM)
    c.roundRect(0, 0, w, h, 6, stroke=0, fill=1)
    # ---- fruiting branch
    x0, y0, x1, y1 = 6, 92, 318, 112

    def bpt(t):
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + 10 * math.sin(math.pi * t)
        return x, y
    c.setStrokeColor(HX("#6B4A33"))
    c.setLineCap(1)
    for t0 in np.linspace(0, 0.98, 40):
        xa, ya = bpt(t0)
        xb, yb = bpt(t0 + 0.025)
        c.setLineWidth(4.2 - 2.6 * t0)
        c.line(xa, ya, xb, yb)
    nodes = [(0.12, ["overripe", "ripe", "ripe", "ripe", "overripe", "ripe"]),
             (0.32, ["ripe", "ripe", "orange", "ripe", "ripe", "orange", "ripe"]),
             (0.52, ["orange", "turning", "ripe", "orange", "turning", "orange"]),
             (0.72, ["turning", "unripe", "turning", "unripe", "unripe"]),
             (0.90, ["unripe", "unripe", "unripe"])]
    for t, _ in nodes:
        xn, yn = bpt(t)
        ln = 78 - 26 * t
        leaf(c, xn, yn + 2, ln, ln * 0.40, 64 - 18 * t)
        leaf(c, xn, yn - 2, ln * 0.95, ln * 0.40, -62 + 14 * t)
    for k, (t, kinds) in enumerate(nodes):
        xn, yn = bpt(t)
        n = len(kinds)
        for i, kd in enumerate(kinds):
            ang = math.pi * (0.15 + 0.7 * i / max(1, n - 1)) + (0.0 if i % 2 else math.pi)
            rad = 7 + (i % 3) * 2
            cxp = xn + rad * math.cos(ang) * 0.9
            cyp = yn + rad * math.sin(ang) * 0.75
            sz = 17 - 2 * (k >= 3) - 2 * (k >= 4)
            draw_pil(c, render_cherry(kd, 140, seed=i + 3 * k), cxp - sz / 2, cyp - sz / 2, sz)
    # ---- flowering sprig
    fx0, fy0, fx1, fy1 = 355, 26, w - 18, 150
    c.setStrokeColor(HX("#6B4A33"))
    c.setLineWidth(2.2)
    c.line(fx0, fy0, fx1, fy1)
    for t in (0.22, 0.52, 0.80):
        xn = fx0 + (fx1 - fx0) * t
        yn = fy0 + (fy1 - fy0) * t
        leaf(c, xn, yn, 52 - 10 * t, 20, 112 - 10 * t)
        leaf(c, xn, yn, 50 - 10 * t, 19, -18)
    for t in (0.22, 0.52, 0.80):
        xn = fx0 + (fx1 - fx0) * t
        yn = fy0 + (fy1 - fy0) * t
        for i in range(6):
            a = 2 * math.pi * i / 6 + t
            flower(c, xn + 8 * math.cos(a), yn + 6 * math.sin(a), 7.5, i * 23)
        bud(c, xn + 3, yn + 10, 3, 60)
        bud(c, xn - 6, yn - 9, 3, -120)
    # labels
    label_box(c, 8, h - 15, "Fruiting branch", 7.4, font="Head", bg=colors.Color(1, 1, 1, 0))
    label_box(c, w - 8, h - 15, "Flowering branch", 7.4, font="Head", anchor="end",
              bg=colors.Color(1, 1, 1, 0))
    xa, ya = bpt(0.12)
    leader(c, 20, 22, xa - 2, ya - 10)
    label_box(c, 6, 10, "Older nodes ripen first: red = ripe", 6.8)
    xa, ya = bpt(0.72)
    leader(c, 250, 22, xa + 4, ya - 10)
    label_box(c, 180, 10, "Tip of the branch: still green", 6.8)
    xa, ya = bpt(0.42)
    leader(c, 190, h - 30, xa + 10, ya + 34)
    label_box(c, 150, h - 26, "Glossy, wavy-edged leaves in pairs", 6.8)
    fxm = fx0 + (fx1 - fx0) * 0.52
    fym = fy0 + (fy1 - fy0) * 0.52
    leader(c, 330, h - 46, fxm - 10, fym + 6)
    label_box(c, 236, h - 42, "White flowers smell of jasmine", 6.8)
    label_box(c, w - 8, 10, "A bloom lasts only 2-3 days", 6.8, anchor="end")


def ripeness_plate(c, w, h):
    items = [("unripe", "Unripe", "sour, grassy: never pick", False),
             ("turning", "Turning", "not sweet yet", False),
             ("orange", "Almost ripe", "nearly there", False),
             ("ripe", "Ripe", "sweet: pick now", True),
             ("overripe", "Overripe", "winey; ferment risk", False),
             ("dried", "Dried cherry", "how naturals are dried", None)]
    cw = w / len(items)
    for i, (kd, name, desc, ok) in enumerate(items):
        cx = cw * i + cw / 2
        sz = 56
        draw_pil(c, render_cherry(kd, 220, seed=i + 1), cx - sz / 2, h - sz - 2, sz)
        text(c, cx, h - sz - 12, name, 8, "Body-Bold", INK, "middle")
        text(c, cx, h - sz - 22, desc, 6.8, "Body", MUTED, "middle")
        if ok is not None:
            col = TEAL if ok else HX("#E76F51")
            c.setFillColor(col)
            c.roundRect(cx - 17, h - sz - 37, 34, 10, 3, stroke=0, fill=1)
            text(c, cx, h - sz - 34.4, "PICK" if ok else "WAIT" if i < 3 else "LATE", 6.6,
                 "Body-Bold", colors.white, "middle")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(cw * 5 + 2, 8, cw * 5 + 2, h - 6)


def season_gantt(c, w, h):
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    lab_w = 128
    x0, x1 = lab_w, w - 4
    mw = (x1 - x0) / 12
    top = h - 14
    rows = [("Blossom showers & flowering", [(1, 4)], HX("#F2C6D5")),
            ("Cherries growing on the bush", [(3, 11)], HX("#8DB86A")),
            ("Monsoon rains", [(5, 9)], HX("#7FB3D5")),
            ("Arabica harvest", [(10, 12), (0, 1)], BERRY),
            ("Robusta harvest", [(11, 12), (0, 3)], HX("#8E3B46")),
            ("Pulping, drying & curing", [(10, 12), (0, 4)], SAFFRON)]
    rh = (top - 4) / len(rows)
    for i, m in enumerate(months):
        xm = x0 + i * mw
        if i % 2 == 0:
            c.setFillColor(HX("#F7F1E8"))
            c.rect(xm, 2, mw, top - 2, stroke=0, fill=1)
        text(c, xm + mw / 2, top + 3, m, 6.8, "Body-Bold", MUTED, "middle")
    for r, (lab, spans, col) in enumerate(rows):
        y = top - (r + 1) * rh
        text(c, lab_w - 5, y + rh / 2 - 2.4, lab, 7, "Body", INK, "end")
        for a, b in spans:
            c.setFillColor(col)
            c.roundRect(x0 + a * mw + 1, y + 2, (b - a) * mw - 2, rh - 4, 2.5, stroke=0, fill=1)


def cherry_cross_section(c, w, h):
    """Lengthwise cut through a ripe cherry, with numbered layers."""
    cx, cy = w * 0.40, h * 0.50
    rx, ry = min(w * 0.34, 98), min(h * 0.42, 96)
    # stalk
    c.setStrokeColor(HX("#5E4630"))
    c.setLineWidth(3)
    c.line(cx, cy - ry + 2, cx - 4, cy - ry - 14)
    # skin
    p = c.beginPath()
    p.ellipse(cx - rx, cy - ry, 2 * rx, 2 * ry)
    grad_fill(c, p, "radial", (cx - rx * 0.3, cy + ry * 0.3, rx * 1.4),
              (HX("#E2453F"), HX("#B3161F"), HX("#6E0E16")), (0, 0.6, 1))
    # pulp
    t = 6
    p = c.beginPath()
    p.ellipse(cx - rx + t, cy - ry + t, 2 * (rx - t), 2 * (ry - t))
    grad_fill(c, p, "radial", (cx, cy, rx), (HX("#FFF4D6"), HX("#F6D7A8"), HX("#EBA58D")),
              (0, 0.65, 1))
    # navel (blossom end) on top
    c.setFillColor(HX("#5E2A22"))
    c.ellipse(cx - 7, cy + ry - 3.5, cx + 7, cy + ry + 2, stroke=0, fill=1)
    # mucilage blob around the two beans
    bx, by = 33, 60
    g = 5.0
    m = c.beginPath()
    m.roundRect(cx - bx - 9, cy - by - 8, 2 * bx + 18, 2 * by + 16, 30)
    grad_fill(c, m, "radial", (cx - 20, cy + 30, 90),
              (rgba(HX("#FFF9C9"), 0.95), rgba(HX("#F3D774"), 0.85)))
    c.setStrokeColor(rgba(HX("#D9B54A"), 0.8))
    c.setLineWidth(0.6)
    c.drawPath(m, stroke=1, fill=0)

    def d_shape(side, inset):
        """Half-ellipse bean outline; side=-1 left bean, +1 right bean."""
        k = 0.5523
        fx = cx + side * g
        ax, ay = bx - inset, by - inset
        p = c.beginPath()
        p.moveTo(fx, cy + ay)
        p.curveTo(fx + side * k * ax * 1.0, cy + ay, fx + side * ax, cy + k * ay, fx + side * ax, cy)
        p.curveTo(fx + side * ax, cy - k * ay, fx + side * k * ax, cy - ay, fx, cy - ay)
        p.lineTo(fx, cy - 5)
        p.curveTo(fx + side * 7, cy - 4, fx + side * 9, cy - 1, fx + side * 9, cy)
        p.curveTo(fx + side * 9, cy + 1, fx + side * 7, cy + 4, fx, cy + 5)
        p.close()
        return p
    for side in (-1, 1):
        par = d_shape(side, 0)
        c.setFillColor(HX("#F1E6CC"))
        c.setStrokeColor(HX("#C8B58A"))
        c.setLineWidth(0.8)
        c.drawPath(par, stroke=1, fill=1)
        sil = d_shape(side, 2.6)
        c.setFillColor(HX("#DADFE2"))
        c.drawPath(sil, stroke=0, fill=1)
        bean = d_shape(side, 3.8)
        grad_fill(c, bean, "radial", (cx + side * 18, cy + 22, 70),
                  (HX("#B9CDB0"), HX("#86A47E"), HX("#5E7C5A")), (0, 0.6, 1))
        c.setStrokeColor(HX("#9FB8C2"))
        c.setLineWidth(0.6)
        c.drawPath(bean, stroke=1, fill=0)
    # numbered callouts with leaders to the right
    rx_lab = w - 14
    spots = [(1, cx + rx * 0.80, cy + ry * 0.56, rx_lab, cy + ry * 0.86),
             (2, cx + rx * 0.66, cy + ry * 0.28, rx_lab, cy + ry * 0.50),
             (3, cx + g + bx + 6, cy + by * 0.08, rx_lab, cy + ry * 0.12),
             (4, cx + g + bx - 0.5, cy - by * 0.22, rx_lab, cy - ry * 0.26),
             (5, cx + g + bx - 2.9, cy - by * 0.45, rx_lab, cy - ry * 0.62),
             (6, cx + g + 16, cy - by * 0.55, rx_lab, cy - ry * 0.98)]
    for n, sx, sy, lx, ly in spots:
        c.setStrokeColor(ESPRESSO)
        c.setLineWidth(0.6)
        c.line(sx, sy, lx - 7, ly)
        c.setFillColor(ESPRESSO)
        c.circle(sx, sy, 1.5, stroke=0, fill=1)
        callout_num(c, lx, ly, n, ESPRESSO)
    text(c, cx, cy - ry - 24, "stalk", 6.6, "Body-Italic", MUTED, "middle")
    text(c, cx, cy + by + 12, "two beans, flat sides facing", 6.4, "Body-Italic", ROAST, "middle")
    text(c, cx, cy + ry + 6, "blossom end", 6.6, "Body-Italic", MUTED, "middle")


def process_layers(c, w, h):
    """Which cherry layers are still on the bean while it dries, by process."""
    layers = [("Skin", HX("#B3161F")), ("Pulp (fruit flesh)", HX("#F2C79A")),
              ("Mucilage (sticky 'honey')", HX("#F3D774")), ("Parchment (papery husk)", HX("#E9DCBC")),
              ("Silver skin", HX("#C9D0D4")), ("Bean (seed)", HX("#86A47E"))]
    procs = [("WASHED", [0, 0, 0, 1, 1, 1], "Clean, bright, clear"),
             ("HONEY", [0, 0, 1, 1, 1, 1], "Sweet, rounded"),
             ("NATURAL", [1, 1, 1, 1, 1, 1], "Fruity, heavy, winey")]
    lab_w = 118
    top = h - 58
    rh = (top - 22) / len(layers)
    cw = (w - lab_w) / len(procs)
    # column heads with an illustration of what goes onto the drying bed
    for j, (name, flags, flav) in enumerate(procs):
        xc = lab_w + cw * j + cw / 2
        c.setFillColor(HX("#F7F1E8"))
        c.roundRect(lab_w + cw * j + 3, 2, cw - 6, h - 4, 5, stroke=0, fill=1)
        text(c, xc, h - 12, name, 8.4, "Head", ESPRESSO, "middle")
        if name == "NATURAL":
            draw_pil(c, render_cherry("dried", 140, seed=9), xc - 17, top + 3, 34)
        else:
            draw_pil(c, render_bean("parchment", 200, seed=4), xc - 22, top + 6, 44)
            if name == "HONEY":
                c.setFillColor(rgba(HX("#E7B93A"), 0.45))
                c.ellipse(xc - 17, top + 12, xc + 14, top + 31, stroke=0, fill=1)
        text(c, xc, 8, flav, 7, "Body-Italic", ROAST, "middle")
    text(c, lab_w - 4, h - 12, "On the bean while it dries?", 7.2, "Body-Bold", ROAST, "end")
    for i, (lab, col) in enumerate(layers):
        y = top - (i + 1) * rh
        c.setFillColor(col)
        c.roundRect(4, y + rh / 2 - 4, 9, 8, 2, stroke=0, fill=1)
        text(c, 17, y + rh / 2 - 2.5, lab, 7.2, "Body", INK)
        for j, (name, flags, flav) in enumerate(procs):
            xc = lab_w + cw * j + cw / 2
            yc = y + rh / 2
            if flags[i]:
                c.setFillColor(col)
                c.setStrokeColor(shade(col, 0.7))
                c.setLineWidth(0.6)
                c.roundRect(xc - 26, yc - 5.5, 52, 11, 5, stroke=1, fill=1)
                text(c, xc, yc - 2.3, "stays on", 6.6, "Body-Bold",
                     colors.white if i in (0, 5) else INK, "middle")
            else:
                c.setStrokeColor(HX("#C9BFB4"))
                c.setDash(2, 2)
                c.setLineWidth(0.6)
                c.roundRect(xc - 26, yc - 5.5, 52, 11, 5, stroke=1, fill=0)
                c.setDash()
                text(c, xc, yc - 2.3, "removed", 6.6, "Body", MUTED, "middle")


def pipelines(c, w, h):
    rows = [("Washed", TEAL, [("Pick ripe", "cherries"), ("Pulp", "skin + flesh off"),
                              ("Ferment", "12-48 h in tank"), ("Wash", "mucilage off"),
                              ("Dry", "1-3 weeks"), ("Hull", "parchment off"),
                              ("Sort", "size, defects")]),
            ("Honey", GOLD, [("Pick ripe", "cherries"), ("Pulp", "skin + flesh off"),
                             ("Dry sticky", "mucilage left, 2-3 wk"), ("Hull", "parchment off"),
                             ("Sort & grade", "by size, defects")]),
            ("Natural", BERRY, [("Pick ripe", "cherries"), ("Float & sort", "remove light ones"),
                                ("Dry whole", "cherry, 3-4 weeks"), ("Hull", "dried husk off"),
                                ("Sort & grade", "by size, defects")])]
    lab_w = 50
    rh = (h - 6) / len(rows)
    for r, (name, col, steps) in enumerate(rows):
        y = h - (r + 1) * rh + 3
        c.setFillColor(col)
        c.roundRect(0, y + 3, lab_w - 6, rh - 8, 4, stroke=0, fill=1)
        text(c, (lab_w - 6) / 2, y + rh / 2 - 3, name, 7.8, "Body-Bold",
             INK if col == GOLD else colors.white, "middle")
        n = len(steps) + 1
        bw = (w - lab_w) / n - 8
        for i, (t1, t2) in enumerate(steps + [("Green coffee", "ready to roast")]):
            x = lab_w + i * (bw + 8)
            last = i == len(steps)
            c.setFillColor(HX("#E9F3E6") if last else HX("#F7F1E8"))
            c.setStrokeColor(LEAF_C if last else rgba(col, 0.9))
            c.setLineWidth(0.8)
            c.roundRect(x, y + 3, bw, rh - 8, 4, stroke=1, fill=1)
            text(c, x + bw / 2, y + rh / 2 + 0.5, t1, 7.2, "Body-Bold", INK, "middle")
            text(c, x + bw / 2, y + rh / 2 - 8, t2, 6.0, "Body", MUTED, "middle")
            if not last:
                arrow(c, x + bw + 1, y + rh / 2 - 1, x + bw + 7, y + rh / 2 - 1, MUTED, 0.8, 3)


def beans_before(c, w, h):
    items = [("parchment", "Parchment coffee", "still in its papery husk"),
             ("green", "Green arabica, washed", "blue-green, S-shaped crease"),
             ("green_natural", "Green arabica, natural", "yellower, from drying in fruit"),
             ("robusta", "Green robusta", "smaller, rounder, straight crease"),
             ("peaberry", "Peaberry", "one round bean per cherry"),
             ("monsooned", "Monsooned Malabar", "swollen and pale gold")]
    cw = w / len(items)
    for i, (kd, name, desc) in enumerate(items):
        cx = cw * i + cw / 2
        iw = cw - 6
        draw_pil(c, render_bean(kd, 320, seed=i + 2), cx - iw / 2, h - iw * 0.78 - 2, iw)
        text(c, cx, h - iw * 0.78 - 10, name, 7.4, "Body-Bold", INK, "middle")
        text(c, cx, h - iw * 0.78 - 19, desc, 6.6, "Body", MUTED, "middle")


def beans_roast(c, w, h):
    items = [("green", "Green", "raw", "0%", HX("#8FA57E")),
             ("yellow", "Yellow", "~150-160°C", "~5%", HX("#D7C08A")),
             ("cinnamon", "Cinnamon", "~196°C", "~11%", HX("#B8854F")),
             ("light", "Light", "~205°C", "~13%", HX("#94643A")),
             ("medium", "Medium", "~215°C", "~15%", HX("#6F4626")),
             ("medium_dark", "Medium-dark", "~225°C", "~17%", HX("#4D2F1A")),
             ("dark", "Dark", "~235°C", "~20%", HX("#2A1A10"))]
    cw = w / len(items)
    img_top = h - 4
    for i, (kd, name, temp, loss, ground) in enumerate(items):
        cx = cw * i + cw / 2
        iw = cw - 4
        draw_pil(c, render_bean(kd, 300, seed=7), cx - iw / 2, img_top - iw * 0.78, iw)
        y = img_top - iw * 0.78 - 9
        text(c, cx, y, name, 7.6, "Body-Bold", INK, "middle")
        text(c, cx, y - 9, temp, 6.6, "Body", MUTED, "middle")
        c.setFillColor(ground)
        c.roundRect(cx - 20, y - 22, 40, 8, 2, stroke=0, fill=1)
        text(c, cx, y - 31, f"weight lost {loss}", 6.4, "Body", MUTED, "middle")
    # crack markers
    for i, lab in [(3, "1st crack"), (6, "2nd crack")]:
        x = cw * i
        c.setStrokeColor(BERRY)
        c.setDash(2, 2)
        c.setLineWidth(0.8)
        c.line(x, 30, x, h - 8)
        c.setDash()
        label_box(c, x, h - 12, lab, 6.6, anchor="middle", fg=BERRY)
    text(c, 2, 2, "Swatches = colour of the ground coffee.  Beans grow ~50-90% in volume "
                  "but lose weight as water and gases leave.", 6.6, "Body-Italic", MUTED)


# =========================================================================== terroir
def mountain(c, w, h):
    bands = [(0, 600, HX("#E9D8A6"), "0-600 m", "hot: little coffee in India"),
             (600, 1000, HX("#C8D9A0"), "600-1,000 m", "India's robusta belt"),
             (1000, 1600, HX("#9CC48A"), "1,000-1,600 m", "India's arabica"),
             (1600, 2300, HX("#6FA77A"), "1,600-2,300 m", "Ethiopia, Kenya, Colombia")]
    x0, x1 = 66, w * 0.64
    y0, y1 = 8, h - 14
    maxa = 2300

    def ya(alt):
        return y0 + alt / maxa * (y1 - y0)
    prof = c.beginPath()
    prof.moveTo(x0, y0)
    pts = [(0.0, 0), (0.12, 260), (0.22, 700), (0.33, 1150), (0.44, 1800), (0.55, 2300),
           (0.66, 1900), (0.78, 1300), (0.90, 700), (1.0, 250)]
    for f, alt in pts:
        prof.lineTo(x0 + (x1 - x0) * f, ya(alt))
    prof.lineTo(x1, y0)
    prof.close()
    for lo, hi, col, rng, lab in bands:
        c.saveState()
        c.clipPath(prof, stroke=0, fill=0)
        c.setFillColor(col)
        c.rect(x0, ya(lo), x1 - x0, ya(hi) - ya(lo), stroke=0, fill=1)
        c.restoreState()
        c.setStrokeColor(rgba(MUTED, 0.45))
        c.setDash(1.5, 2)
        c.setLineWidth(0.5)
        c.line(x0, ya(hi), w - 2, ya(hi))
        c.setDash()
        mid = (ya(lo) + ya(hi)) / 2
        text(c, x1 + 6, mid + 1.5, rng, 6.8, "Body-Bold", INK)
        text(c, x1 + 6, mid - 6.5, lab, 6.6, "Body", MUTED)
    c.setStrokeColor(HX("#5C7A4E"))
    c.setLineWidth(1)
    c.drawPath(prof, stroke=1, fill=0)
    # altitude axis with average temperature (falls ~6 C per 1,000 m)
    for alt, temp in [(0, "~27\u00b0C"), (500, None), (1000, "~21\u00b0C"), (1500, None),
                      (2000, "~15\u00b0C")]:
        y = ya(alt)
        c.setStrokeColor(MUTED)
        c.setLineWidth(0.5)
        c.line(x0 - 3, y, x0, y)
        text(c, x0 - 5, y - 2.3, f"{alt:,} m", 6.2, "Body", MUTED, "end")
        if temp:
            text(c, x0 - 34, y - 2.3, temp, 6.4, "Body-Bold", SKY, "end")
    text(c, x0 - 34, y1 + 3, "avg temp", 6, "Body-Italic", SKY, "end")
    # shade trees on the slopes
    for f in (0.30, 0.38, 0.72, 0.80):
        xx = x0 + (x1 - x0) * f
        alt = np.interp(f, [p[0] for p in pts], [p[1] for p in pts])
        c.setFillColor(HX("#2F5B2B"))
        c.circle(xx, ya(alt) + 5, 3.6, stroke=0, fill=1)


def lat_alt_chart(c, w, h):
    origins = [("Kenya", 0.4, 1500, 2100, BERRY), ("Colombia", 2.5, 1500, 2000, SAFFRON),
               ("Ethiopia", 6.5, 1800, 2300, SKY), ("Panama", 8.8, 1500, 1900, PLUM),
               ("India: Chikmagalur", 13.3, 1000, 1500, TEAL), ("India: Araku", 18.2, 900, 1100, TEAL),
               ("Brazil", 19.0, 800, 1300, GOLD), ("Hawaii (Kona)", 19.6, 150, 900, LEAF_C)]
    x0, x1, y0, y1 = 34, w - 8, 22, h - 18
    maxlat, maxalt = 22, 2550

    def X(lat):
        return x0 + lat / maxlat * (x1 - x0)

    def Y(alt):
        return y0 + alt / maxalt * (y1 - y0)
    band = c.beginPath()
    band.moveTo(X(0), Y(1450))
    band.lineTo(X(22), Y(350))
    band.lineTo(X(22), Y(1250))
    band.lineTo(X(0), Y(2350))
    band.close()
    c.setFillColor(rgba(TEAL, 0.10))
    c.drawPath(band, stroke=0, fill=1)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(x0, y0, x1, y0)
    c.line(x0, y0, x0, y1)
    for lat in (0, 5, 10, 15, 20):
        text(c, X(lat), y0 - 9, f"{lat}°", 6.4, "Body", MUTED, "middle")
    for alt in (0, 500, 1000, 1500, 2000):
        text(c, x0 - 3, Y(alt) - 2, f"{alt:,}", 6.2, "Body", MUTED, "end")
    text(c, (x0 + x1) / 2, 2, "distance from the equator (degrees latitude)", 6.6, "Body-Italic",
         MUTED, "middle")
    text(c, x0, h - 9, "Typical growing altitude (m) by origin", 7.6, "Body-Bold", ROAST)
    place = {"Kenya": "top", "Colombia": "right", "Ethiopia": "top", "Panama": "right",
             "India: Chikmagalur": "left", "India: Araku": "below", "Brazil": "top",
             "Hawaii (Kona)": "left-low"}
    for name, lat, lo, hi, col in origins:
        c.setStrokeColor(col)
        c.setLineWidth(4.5)
        c.setLineCap(1)
        c.line(X(lat), Y(lo), X(lat), Y(hi))
        c.setLineCap(0)
        where = place[name]
        if where == "top":
            text(c, X(lat), Y(hi) + 5, name, 6.6, "Body-Bold", INK, "middle")
        elif where == "right":
            text(c, X(lat) + 5, Y((lo + hi) / 2) - 2.4, name, 6.6, "Body-Bold", INK)
        elif where == "left":
            text(c, X(lat) - 5, Y((lo + hi) / 2) - 2.4, name, 6.6, "Body-Bold", INK, "end")
        elif where == "left-low":
            text(c, X(lat) - 5, Y(lo + 150) - 2.4, name, 6.6, "Body-Bold", INK, "end")
        else:
            text(c, X(lat) - 2, Y(lo) - 10, name, 6.6, "Body-Bold", INK, "end")
    text(c, X(14.5), Y(2050), "'cool enough' zone", 6.6, "Body-Italic", TEAL)


# =========================================================================== tasting language
def taste_smell(c, w, h):
    bw = (w - 36) / 2
    boxes = [(0, "TONGUE: 5 basic tastes", "sweet • sour • bitter • salty • umami",
              HX("#F6D5D3"), BERRY),
             (bw + 36, "NOSE: thousands of aromas", "jasmine • peach • cocoa • caramel • cardamom",
              HX("#D9ECF2"), SKY)]
    for x, title, body, bg, fg in boxes:
        c.setFillColor(bg)
        c.roundRect(x, 30, bw, h - 34, 6, stroke=0, fill=1)
        text(c, x + bw / 2, h - 18, title, 7.8, "Body-Bold", fg, "middle")
        para(c, x + bw / 2, h - 32, body, bw - 12, 7, "Body", INK, anchor="middle")
    text(c, bw + 18, (h + 30) / 2 - 2, "+", 18, "Head", ROAST, "middle")
    arrow(c, w / 2, 28, w / 2, 16, ROAST, 1.2, 4)
    c.setFillColor(ROAST)
    c.roundRect(w / 2 - 92, 0, 184, 14, 4, stroke=0, fill=1)
    text(c, w / 2, 4, "= FLAVOUR (what the tasting notes describe)", 7, "Body-Bold", colors.white,
         "middle")


def acidity_scale(c, w, h):
    stops = [(0.00, "Flat / dull", "like plain hot water; low-grown, old or very dark", HX("#B9AFA5")),
             (0.25, "Soft / mellow", "Indian, Brazilian: gentle, chocolatey", HX("#E9C46A")),
             (0.50, "Bright", "Colombian: crisp like a red apple", HX("#F4A261")),
             (0.75, "Juicy / vibrant", "Kenyan: blackcurrant, citrus, mouth-watering", HX("#E76F51"))]
    x0, x1 = 6, w - 6
    y = h - 32
    steps = 60
    for i in range(steps):
        t = i / steps
        col = stops[min(3, int(t * 4))][3]
        c.setFillColor(col)
        c.rect(x0 + (x1 - x0) * t, y, (x1 - x0) / steps + 0.5, 10, stroke=0, fill=1)
    for t, name, desc, col in stops:
        x = x0 + (x1 - x0) * (t + 0.125)
        text(c, x, y + 14, name, 7.6, "Body-Bold", INK, "middle")
        para(c, x, y - 10, desc, (x1 - x0) / 4 - 10, 6.6, "Body", MUTED, anchor="middle")
    text(c, x0, h - 8, "ACIDITY = pleasant brightness (good)", 7.6, "Body-Bold", ROAST)
    text(c, x1, h - 8, "SOURNESS = sharp, wince-making, thin (a fault: under-extracted or under-roasted)",
         6.8, "Body-Italic", BERRY, "end")


def body_glasses(c, w, h):
    items = [("Tea-like", "thin, delicate", "Chemex; washed Ethiopian", HX("#C98A4B"), 0.35, 0.0),
             ("Light", "like skim milk", "V60; Colombian", HX("#8C5A2E"), 0.6, 0.1),
             ("Medium / round", "like whole milk", "AeroPress; Indian washed", HX("#5E3A1E"), 0.8, 0.25),
             ("Full / syrupy", "like cream or syrup", "French press, espresso; Monsooned Malabar",
              HX("#3A2213"), 0.95, 0.5)]
    cw = w / len(items)
    for i, (name, like, where, col, opa, crema) in enumerate(items):
        cx = cw * i + cw / 2
        gw, gh = 34, 46
        gx, gy = cx - gw / 2, h - gh - 12
        p = c.beginPath()
        p.moveTo(gx, gy + gh)
        p.lineTo(gx + 4, gy)
        p.lineTo(gx + gw - 4, gy)
        p.lineTo(gx + gw, gy + gh)
        c.setStrokeColor(HX("#9AA5AD"))
        c.setLineWidth(1)
        c.drawPath(p, stroke=1, fill=0)
        liquid = c.beginPath()
        lv = gh * 0.72
        liquid.moveTo(gx + 4, gy + 1)
        liquid.lineTo(gx + gw - 4, gy + 1)
        liquid.lineTo(gx + gw - 4 + 4 * lv / gh, gy + lv)
        liquid.lineTo(gx + 4 - 4 * lv / gh + 0.0, gy + lv)
        liquid.close()
        c.setFillColor(rgba(col, opa))
        c.drawPath(liquid, stroke=0, fill=1)
        if crema:
            c.setFillColor(rgba(HX("#C99A5E"), 0.9))
            c.rect(gx + 4 - 4 * lv / gh + 0.6, gy + lv - 4 * crema, gw - 8 + 8 * lv / gh - 1.2,
                   4 * crema, stroke=0, fill=1)
        c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.6))
        c.setLineWidth(1.2)
        c.line(gx + 7, gy + 6, gx + 9, gy + gh - 6)
        text(c, cx, gy - 10, name, 7.6, "Body-Bold", INK, "middle")
        text(c, cx, gy - 19, like, 6.8, "Body-Italic", ROAST, "middle")
        para(c, cx, gy - 28, where, cw - 10, 6.4, "Body", MUTED, anchor="middle")
    text(c, 4, h - 8, "BODY = weight and texture in the mouth", 7.6, "Body-Bold", ROAST)
    arrow(c, w * 0.42, h - 5.5, w - 8, h - 5.5, MUTED, 0.8, 3.5)
    text(c, w - 10, h - 3, "more body", 6.4, "Body-Italic", MUTED, "end")


WHEEL = [
    ("Floral", HX("#D98CB3"), ["jasmine", "rose", "black tea"]),
    ("Fruity", HX("#E76F51"), ["berry", "citrus", "peach", "mango", "raisin"]),
    ("Winey", HX("#E9C46A"), ["winey", "fermented"]),
    ("Green", HX("#8DB86A"), ["grassy", "peapod"]),
    ("Roasted", HX("#6F4E37"), ["toast", "smoky", "burnt"]),
    ("Spices", HX("#B5651D"), ["cardamom", "clove", "pepper"]),
    ("Cocoa/nut", HX("#8B5E3C"), ["almond", "hazelnut", "dark choc", "cocoa"]),
    ("Sweet", HX("#F4A261"), ["caramel", "honey", "jaggery", "vanilla"]),
    ("Defects", HX("#9AA5AD"), ["papery", "musty", "rubber"]),
]


def flavour_wheel(c, w, h):
    cx, cy = w / 2, h / 2 - 2
    r_in, r_mid, r_out = min(w, h) * 0.11, min(w, h) * 0.285, min(w, h) * 0.47
    total = sum(len(d) for _, _, d in WHEEL)
    ang = 90.0
    for cat, col, descs in WHEEL:
        span = 360.0 * len(descs) / total
        # inner ring: category
        p = c.beginPath()
        p.moveTo(cx + r_in * math.cos(math.radians(ang)), cy + r_in * math.sin(math.radians(ang)))
        p.arcTo(cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid, ang, -span)
        p.arcTo(cx - r_in, cy - r_in, cx + r_in, cy + r_in, ang - span, span)
        p.close()
        c.setFillColor(col)
        c.setStrokeColor(colors.white)
        c.setLineWidth(1)
        c.drawPath(p, stroke=1, fill=1)
        mid = math.radians(ang - span / 2)
        rr = (r_in + r_mid) / 2
        c.saveState()
        c.translate(cx + rr * math.cos(mid), cy + rr * math.sin(mid))
        rot = math.degrees(mid)
        if 90 < rot % 360 < 270:
            rot += 180
        c.rotate(rot)
        text(c, 0, -2.4, cat, 6.0, "Body-Bold", colors.white if cat not in ("Winey", "Green")
             else INK, "middle")
        c.restoreState()
        # outer ring: descriptors
        a = ang
        step = span / len(descs)
        for dsc in descs:
            p = c.beginPath()
            p.moveTo(cx + r_mid * math.cos(math.radians(a)), cy + r_mid * math.sin(math.radians(a)))
            p.arcTo(cx - r_out, cy - r_out, cx + r_out, cy + r_out, a, -step)
            p.arcTo(cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid, a - step, step)
            p.close()
            c.setFillColor(shade(col, 1.45))
            c.setStrokeColor(colors.white)
            c.drawPath(p, stroke=1, fill=1)
            m2 = math.radians(a - step / 2)
            r2 = (r_mid + r_out) / 2
            c.saveState()
            c.translate(cx + r2 * math.cos(m2), cy + r2 * math.sin(m2))
            rot = math.degrees(m2)
            if 90 < rot % 360 < 270:
                rot += 180
            c.rotate(rot)
            text(c, 0, -2.2, dsc, 6.0, "Body", INK, "middle")
            c.restoreState()
            a -= step
        ang -= span
    c.setFillColor(CREAM)
    c.circle(cx, cy, r_in - 1, stroke=0, fill=1)
    text(c, cx, cy + 1, "COFFEE", 6.6, "Body-Bold", ROAST, "middle")
    text(c, cx, cy - 7, "flavours", 6.2, "Body", MUTED, "middle")


def yield_funnel(c, w, h):
    """From 100 kg of ripe cherries to cups of coffee (approximate conversion ratios)."""
    steps = [("cherries", "100 kg", "ripe cherries"), ("parchment", "~20-22 kg", "dried parchment"),
             ("green", "~16-18 kg", "green coffee"), ("medium", "~14-15 kg", "roasted coffee"),
             ("cup", "~900-1,000", "cups (15 g each)")]
    n = len(steps)
    cw = w / n
    band_h = h - 34
    for i, (kind, big, small) in enumerate(steps):
        cx = cw * i + cw / 2
        hh = band_h * (1 - 0.12 * i)
        c.setFillColor(rgba(CARAMEL, 0.10 + 0.05 * i))
        c.roundRect(cx - cw / 2 + 4, 30 + (band_h - hh) / 2, cw - 8, hh, 6, stroke=0, fill=1)
        ic_y = 30 + band_h / 2 - 12
        if kind == "cherries":
            for j, (dx, dy, kd) in enumerate([(-14, -2, "ripe"), (2, -4, "ripe"), (-6, 9, "ripe"),
                                              (10, 8, "overripe"), (16, -2, "ripe")]):
                draw_pil(c, render_cherry(kd, 120, seed=20 + j), cx + dx - 11, ic_y + dy, 22)
        elif kind == "cup":
            c.setFillColor(colors.white)
            c.setStrokeColor(ROAST)
            c.setLineWidth(1.2)
            c.roundRect(cx - 14, ic_y - 2, 28, 22, 5, stroke=1, fill=1)
            c.circle(cx + 17, ic_y + 9, 5, stroke=1, fill=0)
            c.setFillColor(HX("#5A3620"))
            c.ellipse(cx - 12, ic_y + 15, cx + 12, ic_y + 20, stroke=0, fill=1)
            c.setFillColor(HX("#C99A5E"))
            c.ellipse(cx - 8, ic_y + 16, cx + 8, ic_y + 19, stroke=0, fill=1)
        else:
            for dx, dy, sd in [(-16, 0, 1), (4, -3, 2), (-6, 10, 3)]:
                draw_pil(c, render_bean(kind, 160, seed=sd), cx + dx - 2, ic_y + dy - 4, 30)
        text(c, cx, 17, big, 9, "Body-Bold", ESPRESSO, "middle")
        text(c, cx, 7, small, 6.8, "Body", MUTED, "middle")
        if i < n - 1:
            arrow(c, cx + cw / 2 - 7, 30 + band_h / 2, cx + cw / 2 + 7, 30 + band_h / 2,
                  CARAMEL, 1.4, 4.5)
