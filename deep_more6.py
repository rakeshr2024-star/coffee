"""Sixth round: specialty India, green spec sheet, roast colour scale, brew-ratio reference,
chain vs independent economics."""
from reportlab.lib import colors

import illustrations as il
from deep_base import (CONTENT_W, HX,
                       figc, h2, p, side, src, tbl)

W = CONTENT_W


def specialty_india():
    s = [h2("13.12 India's specialty coffee scene")]
    s.append(p("Indian specialty coffee has grown from a handful of pioneers to hundreds of roasters in a "
               "decade. <b>Blue Tokai</b> (founded 2013) and <b>Third Wave Coffee</b> (2016) built national "
               "café chains on Indian estate coffee; <b>Araku Coffee</b> took tribal-grown Andhra arabica to "
               "a café in Paris (2017) before opening in India; roasters such as <b>Subko, KC Roasters, Black "
               "Baza, Corridor Seven and Devans</b> sell single estates, micro-lots and experimental "
               "processes online and through cafés. The Specialty Coffee Association of India runs national "
               "barista and brewing championships, and the Coffee Board's Flavour of India and Know Your "
               "Kaapi awards showcase estates."))
    rows = [["Roaster-led cafés", "Blue Tokai, Third Wave, Subko", "Own roasting, estate stories, national "
             "scale"],
            ["Estate and origin brands", "Araku, estate-owned labels", "Grow, process and sell their own coffee"],
            ["Independent roasters", "KC Roasters, Black Baza, Corridor Seven, Devans and many more",
             "D2C, subscriptions, wholesale to cafés"],
            ["Specialty cafés", "Independents in every metro (OCD Culture, Kaffa, Roastery Cultúr in "
             "Ahmedabad)", "Multi-roaster or own roast; experience-led"],
            ["Ready-to-drink and instant", "Cold-brew cans, specialty instant", "Quick commerce and retail"]]
    s.append(tbl(["Type", "Examples", "Model"], rows, [100, 220, W - 320], font_size=7.4))
    s.append(src("Company websites and press coverage; World Coffee Portal."))
    return s


def spec_sheet():
    s = [h2("5.8 What a green-coffee offer sheet tells you")]
    rows = [["Lot", "Ratnagiri-type estate lot #24-117, 20 bags x 60 kg", "Traceability; buy a whole lot for "
             "consistency"],
            ["Origin & altitude", "Chikmagalur, Karnataka; 1,300-1,450 m", "Terroir and density"],
            ["Variety", "S.795 and Chandragiri", "Flavour potential"],
            ["Process", "Washed, 36 h dry fermentation, raised-bed drying 14 days", "Clean, bright profile"],
            ["Grade & screen", "Plantation A; 90% on screen 17", "Even roasting"],
            ["Moisture / water activity", "10.8% / 0.55 aw", "Stability in storage"],
            ["Density", "~720 g/L (free-flow)", "Higher = usually higher grown, roasts slower"],
            ["Defects (350 g)", "0 primary, 3 secondary", "Specialty grade"],
            ["Cup score & notes", "84.25: milk chocolate, orange, cane sugar", "Menu description"],
            ["Price & terms", "₹ per kg ex-curing works; delivery; payment", "Budget and cash flow"]]
    s.append(tbl(["Field", "Example (illustrative)", "Why it matters"], rows, [100, 230, W - 330], font_size=7.4))
    return s


def _agtron(c, w, h):
    tiles = [(95, "Very light", "#C9A06A"), (85, "Light", "#B88A55"), (75, "Moderately light", "#A47446"),
             (65, "Light medium", "#8E5E37"), (55, "Medium", "#784B2B"), (45, "Moderately dark", "#5F3821"),
             (35, "Dark", "#47281A"), (25, "Very dark", "#2E1A12")]
    il.text(c, 0, h - 9, "Roast colour on the Agtron / SCA tile scale (higher = lighter)", 8.2, "Body-Bold",
            il.ROAST)
    tw = w / len(tiles)
    for i, (n, lab, col) in enumerate(tiles):
        x = i * tw
        c.setFillColor(HX(col))
        c.roundRect(x + 2, 22, tw - 4, h - 44, 4, stroke=0, fill=1)
        il.text(c, x + tw / 2, (h - 44) / 2 + 18, f"#{n}", 11, "Head", colors.white, "middle")
        il.text(c, x + tw / 2, 10, lab, 6.6, "Body-Bold", il.INK, "middle")
    il.text(c, 0, 1, "Filter roasts typically sit around #65-75, espresso #50-60, traditional kaapi #35-45.",
            6.4, "Body-Italic", il.MUTED)


def agtron():
    return [h2("7.13 Measuring roast colour"),
            figc(il.CanvasFigure(W, 96, _agtron),
                 "Figure 7.4. Roasters measure colour with a near-infrared meter (Agtron or similar) so a "
                 "'medium' roast means the same thing every batch.")]


def ratio_reference():
    s = [h2("9.10 Brew-ratio quick reference")]
    cups = [150, 250, 350, 500]
    ratios = [15, 16, 17, 18]
    rows = [[f"{v} ml water"] + [f"{v / r:.1f} g" for r in ratios] for v in cups]
    s.append(side([tbl(["Water", "1:15 (strong)", "1:16", "1:17", "1:18 (light)"], rows,
                       [W * 0.13, W * 0.09, W * 0.08, W * 0.08, W * 0.1], font_size=7.4,
                       center_cols=(1, 2, 3, 4))],
                  [p("Dose = water ÷ ratio. Start at 1:16 for pour-over and French press; go stronger (1:15) "
                     "for darker roasts or with milk, lighter (1:17-1:18) for delicate light roasts. A gram "
                     "scale costing ₹500-800 is the single most useful brewing tool after a burr grinder.")],
                  lw=0.5))
    return s


def chain_economics():
    s = [h2("13.13 Chains versus independents")]
    rows = [["Revenue per outlet", "~₹2.7 crore a year (Tata Starbucks FY25: ₹1,277 cr / ~479 stores)",
             "₹1.5-2.7 crore in the Part 2 models (Y3)"],
            ["Ticket", "₹350-550 per bill", "₹320-360 average bill (Part 2)"],
            ["Costs carried", "Head office, regional teams, central roasting, brand marketing", "Owner "
             "management, local marketing, toll roaster"],
            ["Profitability", "Store-level profit, but company-level losses while expanding (Starbucks "
             "India FY25 loss ₹136 cr; Blue Tokai FY24 loss ₹63 cr)", "Store-level EBITDA 19-24% in "
             "Part 2's Base cases"],
            ["Advantages", "Brand pull, purchasing scale, prime sites", "Agility, local menu, community, "
             "lower overheads"]]
    s.append(tbl(["", "National chains", "A strong independent (Part 2)"], rows, [100, (W - 100) / 2,
                                                                                    (W - 100) / 2],
                 font_size=7.4))
    s.append(p("An independent cannot match a chain's purchasing or marketing, but it does not carry a "
               "head office either. A well-run single café on a good street can earn store-level margins "
               "similar to a chain store's, and that is the economic case for Part 2."))
    return s
