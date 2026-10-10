"""Seventh round: farm management, processing risks, direct trade, pour schedules, espresso shot
anatomy, home buying guide, outlook."""
import build_report as R
import deep_charts as DC
from deep_base import (BERRY, CARAMEL, CONTENT_W, GOLD, LEAF, PLUM, ROAST, SAFFRON, SKY, TEAL, HX,
                       bl, figc, h2, p, side, src, tbl)

W = CONTENT_W


def farm_management():
    s = [h2("2.15 How an estate is managed through the year")]
    rows = [["Nutrition", "Fertiliser in three splits (pre-blossom, pre-monsoon, post-monsoon); lime every few "
             "years to correct acidic soils; compost and coffee pulp returned to the field", "Yield and bean "
             "size"],
            ["Bush training", "Arabica on a single stem 'centred' (topped) at about 1.2-1.5 m; robusta on "
             "multiple stems; 'handling' removes unwanted suckers after harvest", "Pickable height, "
             "productive wood"],
            ["Pruning", "Cut out old, dead and crossing branches after harvest; periodic rejuvenation of "
             "exhausted bushes", "Air, light, fewer pests"],
            ["Shade regulation", "Lop shade trees before the monsoon so light and air reach the bushes; keep "
             "two tiers", "Balance of yield and quality"],
            ["Water", "Sprinkler 'blossom' irrigation in dry years; mulching; farm ponds", "Flowering, crop "
             "security"],
            ["Weeds and soil", "Slashing or manual weeding 2-3 times a year; cover crops; contour trenches",
             "Soil conservation on slopes"],
            ["Pest and disease watch", "Trace and remove white-stem-borer plants; traps for berry borer; "
             "fungicide for rust and black rot when needed", "Protects the crop and the tree"]]
    s.append(tbl(["Practice", "What estates do", "Why"], rows, [86, 300, W - 386], font_size=7.3))
    s.append(src("CCRI and Coffee Board package of practices; TNAU Agritech portal."))
    return s


def processing_risks():
    s = [h2("4.14 Where quality is lost in processing")]
    rows = [["Delay before pulping", "Cherries ferment in sacks", "Sour, vinegar", "Pulp within 6-12 h"],
            ["Unsorted cherries", "Unripe and damaged mixed in", "Grassy, astringent, dirty", "Float and "
             "hand-sort"],
            ["Over-fermentation", "Too long or too warm", "Sour, onion, cheesy", "Monitor pH and time"],
            ["Dirty tanks and water", "Microbial taints", "Phenolic, medicinal", "Clean equipment daily"],
            ["Drying too fast", "Hot concrete, thick layers not turned", "Baked, cracked parchment",
             "Thin layers, raking, shade at noon"],
            ["Drying too slow / rain", "Mould", "Musty, earthy", "Covers, raised beds, dryers"],
            ["Re-wetting in storage", "Damp godowns", "Mouldy, faded", "Dry stores, hermetic bags, pallets"],
            ["Long storage", "Ageing green coffee", "Papery, woody ('past crop')", "Ship and roast within "
             "the year"]]
    s.append(tbl(["Failure point", "What goes wrong", "Taste", "Prevention"], rows, [100, 160, 110, W - 370],
                 font_size=7.3))
    return s


def direct_trade():
    s = [h2("6.9 Direct trade and specialty contracts")]
    s.append(p("Specialty buyers increasingly agree prices directly with estates instead of buying anonymous "
               "lots through traders. A typical Indian direct-trade arrangement for a café or roaster looks "
               "like this:"))
    rows = [["Pricing", "Fixed rupee price per kg of green (e.g. ₹900-1,100 for an 84+ point lot), agreed "
             "before harvest; sometimes a floor plus a quality premium"],
            ["Quality clause", "Pre-shipment sample must match the approved cup profile and score; moisture "
             "10-11.5%; defect limits"],
            ["Volume and timing", "e.g. 20 bags (1.2 t) from the 2026-27 crop, delivered in two lots to "
             "the toll roaster"],
            ["Payment", "Advance at contract (helps the grower finance harvest), balance on delivery"],
            ["Story and rights", "Estate name, photos and story may be used on menus and bags"],
            ["Relationship", "Multi-year intent; visits at harvest; feedback on cupping"]]
    s.append(tbl(["Term", "Typical content"], rows, [100, W - 100], font_size=7.3))
    s.append(p("For a single café the volumes are small (about 30 bags a year), so many cafés buy through "
               "their toll roaster's estate relationships at first and contract directly once volumes grow."))
    return s


def pour_schedule():
    t = [f"{x // 60}:{x % 60:02d}" for x in range(0, 211, 15)]
    hoff = [0, 60, 60, 60, 180, 300, 400, 500, 500, 500, 500, 500, 500, 500, 500]
    k46 = [0, 60, 60, 120, 120, 120, 180, 180, 180, 240, 240, 240, 300, 300, 300]
    left = DC.line_chart(t, [("Hoffmann V60 (30 g : 500 g)", hoff, TEAL), ("Kasuya 4:6 (20 g : 300 g)", k46,
                                                                           SAFFRON)],
                         W * 0.5, 160, title="Pour schedules: cumulative water (g) over time", ylo=0, yhi=500,
                         label_every=2, markers=False)
    tt = [f"{x}s" for x in range(0, 33, 3)]
    press = [0, 2.5, 3, 8, 9, 9, 9, 9, 9, 8.5, 7.5, 6]
    yld = [0, 0, 0.5, 4, 9, 14, 19, 24, 29, 34, 37, 38]
    right = DC.line_chart(tt, [("Pressure (bar) x 4", [x * 4 for x in press[:11]], BERRY),
                               ("Espresso in the cup (g)", yld[:11], ROAST)],
                          W * 0.48, 160, title="Anatomy of an 18 g : 36 g espresso shot", ylo=0, yhi=40,
                          markers=False, label_every=2)
    return [h2("10.27 Timing the brew"),
            side([left], [right], lw=0.51),
            R.P("Figure 10.1. Left: two well-known pour-over schedules. Right: a typical shot with a few "
                "seconds of low-pressure pre-infusion, then ~9 bar; the first drops appear after 6-8 s and "
                "the shot reaches 36 g at about 28 s (illustrative).", R.CAPTION)]


def buying_guide():
    s = [h2("12.13 Buying coffee for home in India")]
    rows = [["V60, Chemex, AeroPress", "Light to medium single estates; washed or natural", "₹500-900 per "
             "250 g"],
            ["French press, cold brew", "Medium to medium-dark; Indian arabica or blends", "₹400-700"],
            ["Espresso at home, moka pot", "Medium-dark espresso blend, some robusta", "₹450-750"],
            ["Filter kaapi", "Filter-coffee powder: pure coffee or 80:20 / 90:10 with chicory", "₹250-450"],
            ["Instant", "Freeze-dried for best flavour; specialty instant sachets", "₹200-800 per 100 g"]]
    s.append(tbl(["If you brew with", "Buy", "Typical price"], rows, [130, 260, W - 390], font_size=7.3))
    s += bl(["Buy whole beans with a roast date; grind just before brewing if you have a burr grinder, or ask "
             "the roaster to grind for your method.",
             "Buy 250 g at a time and finish within 3-4 weeks; store airtight, away from heat and light.",
             "Try a sampler pack: three estates or processes side by side is the fastest way to learn your "
             "taste."])
    return s


def outlook():
    s = [h2("13.14 Outlook to 2030")]
    rows = [["World prices", "Record Brazilian crops in 2026/27 should ease prices from 2025's records, but "
             "low stocks and climate shocks keep volatility high", "Budget a ±30% green-price range"],
            ["Indian production", "Slow growth (~2% a year); quality and fine robusta improve; new areas in "
             "Odisha and the North-East", "More traceable Indian specialty supply"],
            ["Indian demand", "Café outlets to >10,000 by 2030 (13% a year); cold coffee, specialty and RTD "
             "lead", "Market growth supports new cafés, but competition rises"],
            ["Rules and trade", "EUDR traceability, trade deals with the UK and EFTA; GST cuts on coffee "
             "products", "Better export prices for estates; more documentation"],
            ["Costs in cafés", "Wages and rents rising faster than menu prices in many cities", "Productivity "
             "and pricing discipline matter"]]
    s.append(tbl(["Theme", "What to expect", "So what for a café"], rows, [80, 280, W - 360], font_size=7.3))
    return s


# ------------------------------------------------------------------ map & cheat sheet
from reportlab.lib import colors as _colors  # noqa: E402
from reportlab.platypus import PageBreak, Table, TableStyle  # noqa: E402

import brew_art as BA  # noqa: E402
import illustrations as il  # noqa: E402
from deep_base import P  # noqa: E402

COAST = [(72.8, 20.0), (72.9, 19.0), (73.3, 17.0), (73.7, 15.5), (74.1, 14.8), (74.5, 13.9), (74.8, 12.9),
         (75.4, 11.8), (75.8, 11.25), (76.2, 10.0), (76.6, 8.9), (76.9, 8.5), (77.5, 8.08), (78.1, 8.8),
         (79.1, 9.3), (79.8, 10.3), (79.85, 11.9), (80.3, 13.1), (80.15, 15.0), (81.0, 16.3), (82.3, 16.9),
         (83.3, 17.7), (84.9, 19.3), (86.0, 20.0)]
PLACES = [("Chikmagalur", 75.77, 13.32, LEAF, "r"), ("Coorg", 75.74, 12.42, SKY, "l"),
          ("BR Hills", 77.15, 11.99, TEAL, "r"), ("Wayanad", 76.08, 11.61, BERRY, "l"),
          ("Nilgiris", 76.70, 11.41, GOLD, "r"), ("Shevaroys", 78.21, 11.78, GOLD, "r"),
          ("Pulneys", 77.49, 10.24, SAFFRON, "r"), ("Travancore", 77.0, 9.6, PLUM, "l"),
          ("Araku", 82.88, 18.33, CARAMEL, "l"), ("Koraput", 82.71, 18.81, HX("#7A6F66"), "r")]


def _map(c, w, h):
    lon0, lon1, lat0, lat1 = 72.3, 86.5, 7.8, 20.3
    sc = min(w / (lon1 - lon0), (h - 14) / (lat1 - lat0))
    ox = (w - (lon1 - lon0) * sc) / 2

    def X(lon):
        return ox + (lon - lon0) * sc

    def Y(lat):
        return (lat - lat0) * sc + 4
    p_ = c.beginPath()
    p_.moveTo(X(COAST[0][0]), Y(COAST[0][1]))
    for lo, la in COAST[1:]:
        p_.lineTo(X(lo), Y(la))
    p_.close()
    c.setFillColor(HX("#F3EBDD"))
    c.setStrokeColor(HX("#B9A88F"))
    c.setLineWidth(0.8)
    c.drawPath(p_, stroke=1, fill=1)
    # Western Ghats band
    ghats = [(73.6, 19.0), (73.9, 17.0), (74.3, 15.3), (75.1, 13.6), (75.6, 12.2), (76.5, 11.3), (77.2, 9.8),
             (77.3, 8.6)]
    c.setStrokeColor(il.rgba(LEAF, 0.35))
    c.setLineWidth(9)
    c.setLineCap(1)
    pg = c.beginPath()
    pg.moveTo(X(ghats[0][0]), Y(ghats[0][1]))
    for lo, la in ghats[1:]:
        pg.lineTo(X(lo), Y(la))
    c.drawPath(pg, stroke=1, fill=0)
    il.text(c, X(73.4), Y(16.2), "Western", 6.2, "Body-Italic", LEAF, "end")
    il.text(c, X(73.4), Y(15.9), "Ghats", 6.2, "Body-Italic", LEAF, "end")
    for name, lo, la, col, side_ in PLACES:
        c.setFillColor(col)
        c.setStrokeColor(_colors.white)
        c.circle(X(lo), Y(la), 4, stroke=1, fill=1)
        if side_ == "r":
            il.label_box(c, X(lo) + 6, Y(la) - 2.5, name, 6.4, "start", "Body-Bold")
        else:
            il.label_box(c, X(lo) - 6, Y(la) - 2.5, name, 6.4, "end", "Body-Bold")
    c.setFillColor(il.ROAST)
    c.rect(X(74.86) - 3, Y(12.91) - 3, 6, 6, stroke=0, fill=1)
    il.label_box(c, X(74.86) - 6, Y(12.91) + 6, "Mangalore port", 6.2, "end", "Body")
    il.arrow(c, X(74.0), Y(19.0), X(73.2), Y(20.2), il.BERRY, 1.2, 4)
    il.text(c, X(74.1), Y(19.2), "Ahmedabad ~1,200 km north", 6.4, "Body-Bold", il.BERRY)
    il.text(c, w - 4, 6, "Schematic, not to survey accuracy", 6.0, "Body-Italic", il.MUTED, "end")


def region_map():
    return [figc(il.CanvasFigure(W, 230, _map),
                 "Figure 2.6. Where India's coffee grows: the Western Ghats of Karnataka, Kerala and Tamil "
                 "Nadu, plus the Eastern Ghats of Andhra Pradesh and Odisha.")]


CHEAT = [("espresso", "Espresso", [("Dose : yield", "18 g : 36 g"), ("Grind", "fine"), ("Water", "93°C, 9 bar"),
                                   ("Time", "25-30 s")]),
         ("v60", "V60 pour-over", [("Dose : water", "15 g : 250 g"), ("Grind", "medium-fine"),
                                   ("Water", "93-100°C"), ("Time", "2:30-3:00")]),
         ("chemex", "Chemex", [("Dose : water", "30 g : 500 g"), ("Grind", "medium-coarse"),
                               ("Water", "93-100°C"), ("Time", "4:00-4:30")]),
         ("french", "French press", [("Dose : water", "30 g : 500 g"), ("Grind", "medium-coarse"),
                                     ("Water", "just off boil"), ("Time", "4 min + 5-8 settle")]),
         ("aeropress", "AeroPress", [("Dose : water", "11 g : 200 g"), ("Grind", "fine-medium"),
                                     ("Water", "~99°C"), ("Time", "2:00 + 30 s press")]),
         ("moka", "Moka pot", [("Coffee", "basket level, 15-20 g"), ("Grind", "fine-medium"),
                               ("Water", "hot, to the valve"), ("Time", "4-5 min, off at gurgle")]),
         ("kaapi", "Filter kaapi", [("Powder : water", "20-25 g : 120 ml"), ("Grind", "fine"),
                                    ("Serve", "1 decoction : 2-3 milk"), ("Time", "10-20 min drip")]),
         ("cold", "Cold brew", [("Ratio", "1:8 concentrate"), ("Grind", "coarse"), ("Water", "cold / room"),
                                ("Time", "12-18 h, fridge")]),
         ("cezve", "Turkish", [("Dose : water", "7-8 g : 70 ml"), ("Grind", "powder"),
                               ("Heat", "to foam, 2-3 times"), ("Serve", "unfiltered")])]


def cheat_sheet():
    cw = (W - 12) / 3
    ks = R.ParagraphStyle("chk", fontName="Body-Bold", fontSize=7.4, leading=9, textColor=ROAST)
    vs = R.ParagraphStyle("chv", fontName="Body", fontSize=7.4, leading=9)
    hs = R.ParagraphStyle("chh", fontName="Head", fontSize=11.5, leading=13, textColor=R.ESPRESSO)
    cards = []
    for key, name, kv in CHEAT:
        inner = Table([[P(k, ks), P(v, vs)] for k, v in kv], colWidths=[cw * 0.42 - 6, cw * 0.58 - 6])
        inner.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 2)]))
        card = Table([[BA.icon(key, cw - 10, 128)], [P(name, hs)], [inner]], colWidths=[cw])
        card.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), HX("#FBF6EF")),
                                  ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                                  ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                                  ("LINEABOVE", (0, 0), (-1, 0), 2, CARAMEL)]))
        cards.append(card)
    grid = Table([cards[i:i + 3] for i in range(0, 9, 3)], colWidths=[cw + 6] * 3)
    grid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return [PageBreak(), h2("10.28 Brewing cheat sheet (print me)"), grid,
            R.P("Weigh coffee and water; adjust grind by taste: sour = finer, bitter = coarser.", R.CAPTION)]
