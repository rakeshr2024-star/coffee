"""Fourth round of Part 1 depth: regions atlas, climate, global traders & roasters, espresso and
pour-over deep dives, kaapi culture, flavour-wheel categories, sustainability, quality checklist."""
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table, TableStyle

import build_report as R
import deep_charts as DC
from deep_base import (BERRY, CARAMEL, CONTENT_W, GOLD, LEAF, PLUM, ROAST, SAFFRON, SKY, TEAL, HX, P,
                       bl, h2, p, side, src, tbl)

W = CONTENT_W

REGIONS = [
    ("Chikmagalur & Baba Budan Giri", "Karnataka", LEAF,
     [("Altitude", "1,000-1,600 m"), ("Rain", "~1,500-2,500 mm"), ("Coffee", "Arabica (S.795, Sln 9, "
      "Chandragiri) and robusta"), ("Process", "Washed, natural, micro-lots"), ("Estates", "Ratnagiri, "
      "Baarbara, Kelagur, Thogarihunkal"), ("Cup", "Chocolate, spice, citrus, full body")]),
    ("Coorg (Kodagu)", "Karnataka", SKY,
     [("Altitude", "750-1,100 m"), ("Rain", "~1,500-4,000 mm (wetter west)"), ("Coffee", "Mostly robusta "
      "(S.274, CxR); arabica higher up"), ("Process", "Natural 'cherry' and washed 'parchment'"),
      ("GI", "Coorg Arabica"), ("Cup", "Robusta: cocoa, nutty; arabica: mild, sweet")]),
    ("Biligiris (BR Hills)", "Karnataka", TEAL,
     [("Altitude", "1,000-1,500 m"), ("Coffee", "Arabica"), ("Process", "Washed"), ("Estates", "Attikan"),
      ("Grade", "Source of Mysore Nuggets EB"), ("Cup", "Balanced, sweet, clean")]),
    ("Wayanad", "Kerala", BERRY,
     [("Altitude", "700-1,200 m"), ("Coffee", "Robusta, smallholder-grown"), ("Process", "Mostly natural"),
      ("GI", "Wayanad Robusta"), ("Cup", "Heavy body, chocolate, earthy")]),
    ("Travancore & Nelliampathy", "Kerala", PLUM,
     [("Altitude", "500-1,600 m"), ("Coffee", "Both species"), ("Farming", "Intercropped with pepper, "
      "cardamom"), ("Cup", "Varied; spice notes")]),
    ("Pulneys", "Tamil Nadu", SAFFRON,
     [("Altitude", "1,000-2,000 m (India's highest)"), ("Coffee", "Arabica"), ("Process", "Washed"),
      ("Cup", "Bright acidity, fruit, complexity")]),
    ("Nilgiris & Shevaroys", "Tamil Nadu", GOLD,
     [("Altitude", "900-1,800 m"), ("Coffee", "Mostly arabica"), ("Place", "Shevaroys around Yercaud"),
      ("Cup", "Mild, sweet, gentle acidity")]),
    ("Araku Valley", "Andhra Pradesh", CARAMEL,
     [("Altitude", "900-1,100 m (Eastern Ghats)"), ("Coffee", "Arabica"), ("Growers", "Tribal "
      "smallholders, organic-leaning"), ("GI", "Araku Valley Arabica"), ("Cup", "Fruity, sweet; award-"
      "winning lots")]),
    ("Koraput & North-East", "Odisha, NE states", HX("#7A6F66"),
     [("Altitude", "600-1,200 m"), ("Coffee", "Arabica"), ("Status", "Non-traditional, expanding; "
      "Koraput won KYK awards (2024)"), ("Cup", "Light, clean, developing")])]


def _card(name, state, col, items, width):
    hs = ParagraphStyle("cardh", fontName="Body-Bold", fontSize=8.6, leading=10.4, textColor=R.colors.white)
    ks = ParagraphStyle("cardk", fontName="Body-Bold", fontSize=7.0, leading=8.6, textColor=ROAST)
    vs = ParagraphStyle("cardv", fontName="Body", fontSize=7.0, leading=8.6)
    rows = [[P(f"{name}<br/><font size='6.8'>{state}</font>", hs), ""]]
    for k, v in items:
        rows.append([P(k, ks), P(v, vs)])
    t = Table(rows, colWidths=[width * 0.27, width * 0.73])
    t.setStyle(TableStyle([("SPAN", (0, 0), (1, 0)), ("BACKGROUND", (0, 0), (1, 0), col),
                           ("BACKGROUND", (0, 1), (-1, -1), HX("#FBF6EF")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
                           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    return t


def atlas():
    s = [h2("2.14 An atlas of India's coffee regions")]
    cw = (W - 12) / 3
    cards = [_card(n, st, c, it, cw) for n, st, c, it in REGIONS]
    grid = [cards[i:i + 3] for i in range(0, 9, 3)]
    t = Table(grid, colWidths=[cw + 6] * 3)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    s.append(t)
    s.append(src("Coffee Board region profiles and GI registry; CCRI; estate and roaster listings. Altitude "
                 "and rainfall ranges are indicative."))
    months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
    rain = [2, 3, 12, 55, 110, 290, 470, 340, 180, 160, 60, 15]
    s.append(side([DC.bar_chart(months, [("Rainfall (mm)", rain, SKY)], W * 0.5, 140,
                                title="Chikmagalur: approximate monthly rainfall (mm)", fmt="{:,.0f}",
                                show_vals=False, cat_size=6.4)],
                  [p("The rainfall pattern of a typical coffee district explains the calendar in Figure 2.5: "
                     "a dry winter (harvest and drying weather), a few critical showers in March-April "
                     "(blossom and backing showers), and a heavy south-west monsoon from June to September "
                     "that fills the berries but can also cause rot. Western slopes facing the monsoon can "
                     "receive two or three times the rain of eastern estates a few kilometres away, one "
                     "reason micro-climates and estates differ so much.")], lw=0.52))
    s.append(src("Approximate long-term averages for Chikmagalur town (India Meteorological Department "
                 "climate normals, rounded)."))
    return s


def global_players():
    s = [h2("13.11 Who trades and roasts the world's coffee")]
    rows = [["Green-coffee traders", "Neumann Kaffee Gruppe, ECOM, ofi (Olam), Louis Dreyfus, Sucafina, "
             "Volcafe", "Buy from exporters and co-operatives, finance, hedge, ship and blend to order"],
            ["Global roasters", "Nestlé, JDE Peet's, Starbucks, Lavazza, Tchibo, Strauss, Keurig Dr Pepper, "
             "UCC", "A handful of firms roast a large share of the world's coffee"],
            ["Instant manufacturers", "Nestlé, JDE, Tata Consumer, CCL Products and others", "India is a "
             "major contract manufacturer of instant coffee"],
            ["Specialty importers", "Small importers and roasters buying micro-lots", "Direct trade, "
             "traceability, premiums"],
            ["Exchanges", "ICE US (arabica 'C'), ICE Europe (robusta)", "Price discovery and hedging"]]
    s.append(tbl(["Layer", "Examples", "Role"], rows, [100, 230, W - 330], font_size=7.3))
    s.append(p("Market power sits downstream: traders and roasters are far more concentrated than the "
               "world's 12.5 million farms. That is why value is captured mostly in consuming countries and "
               "in cafés, and why producer-country brands, including Indian estates and roasters selling "
               "at home, are a way for more value to stay at origin."))
    return s


def espresso_deep():
    s = [h2("10.24 Espresso, a closer look")]
    s.append(side([p("Modern espresso has moved away from the traditional Italian single (7 g making 25 ml) "
                     "towards larger, weighed doses and ratios. Precision baskets with uniform holes, "
                     "distribution tools (stirring the grounds with fine needles, known as WDT) and puck "
                     "screens all aim at one thing: an even puck with no channels."),
                   p("Research has pushed further. A 2020 study by Cameron and colleagues in the journal "
                     "<i>Matter</i>, 'Systematically improving espresso', showed that slightly <b>coarser "
                     "grinding with lower doses</b> gave more consistent, higher extractions and less "
                     "waste, because very fine grounds clog unevenly. Some cafés now pull 'turbo' shots: "
                     "coarser grind, ratio around 1:3, about 15 seconds.")],
                  [tbl(["Style", "Dose : yield", "Time", "Taste"],
                       [["Traditional Italian", "7 g : 25 ml (single)", "20-25 s", "Dense, roasty"],
                        ["Modern normale", "18 g : 36 g", "25-30 s", "Balanced, sweet"],
                        ["Ristretto", "18 g : 25 g", "20-25 s", "Syrupy, intense"],
                        ["Lungo", "18 g : 54 g+", "35-40 s", "Lighter, more bitter"],
                        ["Turbo", "15-18 g : 45-54 g", "~15 s", "Clean, bright"],
                        ["Allongé", "18 g : 90 g", "30-40 s", "Filter-like, light roasts"]],
                       [W * 0.12, W * 0.12, W * 0.07, W * 0.11], font_size=7.0)], lw=0.56))
    s.append(h2("10.25 Pour-over, a closer look"))
    s.append(p("Three refinements make pour-over consistent. <b>Pouring</b>: a gooseneck kettle gives a "
               "thin, controllable stream; pour in circles that avoid the paper walls. <b>Paper</b>: rinse "
               "it to remove papery taste and pre-heat the brewer; bleached papers taste cleaner than "
               "unbleached. <b>Bed</b>: a flat bed at the end means even extraction; a crater or grounds "
               "stuck high on the walls mean channelling."))
    s.append(p("<b>Tetsu Kasuya's 4:6 method</b>, which won the 2016 World Brewers Cup, is a good way to "
               "learn how pours shape the cup: 20 g of coarse-ground coffee and 300 g of water poured in "
               "five equal 60 g pours, 45 seconds apart. The first 40% of the water (two pours) controls "
               "sweetness and acidity: make the first pour smaller for sweeter coffee, larger for "
               "brighter. The remaining 60% (three pours) controls strength: fewer, larger pours for a "
               "lighter cup, more pours for a stronger one."))
    return s


def kaapi_culture():
    s = [h2("10.26 Filter kaapi: culture, chicory and serving it at scale")]
    s.append(p("Filter coffee spread through South India in the 20th century, first in middle-class homes "
               "and then in Udupi restaurants, darshinis and the Indian Coffee Houses. Its taste is defined "
               "by three choices: a <b>dark roast</b> (often of Plantation and Peaberry arabica with "
               "robusta), <b>chicory</b> (which adds bitterness, body and colour and stretches the coffee), "
               "and <b>full-cream milk</b> with sugar. Indian rules require coffee-chicory blends to be "
               "labelled as such, with the proportions declared."))
    s.append(p("Restaurants serving hundreds of cups use large multi-litre filters or brewing urns, make "
               "decoction in batches through service, and keep milk simmering. For a specialty café, the "
               "opportunity is a <b>premium kaapi</b>: estate arabica, a medium-dark roast, no or little "
               "chicory, decoction made fresh every hour and served in a steel tumbler and davara, hot or "
               "iced. At about ₹27 of ingredients and a ₹150-180 menu price (section 10.18) it is one of "
               "the highest-margin drinks a café can sell, and a strong signature in Gujarat, where most "
               "customers have never tasted good filter coffee."))
    return s


def wheel_categories():
    s = [h2("11.8 The flavour wheel, category by category")]
    rows = [["Fruity", "Berry, dried fruit, citrus, stone fruit", "Ethiopian and Kenyan washed; naturals; "
             "anaerobics"],
            ["Floral", "Jasmine, rose, black tea", "Gesha, high-grown washed arabica"],
            ["Sweet", "Brown sugar, caramel, honey, vanilla", "Ripe picking and good roast development"],
            ["Nutty / cocoa", "Almond, hazelnut, chocolate, dark chocolate", "Brazil, India, medium roasts"],
            ["Spices", "Clove, cinnamon, pepper", "Indian and Sumatran coffees; monsooned"],
            ["Roasted", "Cereal, malt, tobacco, burnt", "Darker roasts; burnt = roast fault"],
            ["Green / vegetative", "Grassy, peapod, beany, olive oil", "Underdeveloped roast or unripe beans"],
            ["Sour / fermented", "Winey, whisky, vinegar, over-ripe", "Fermentation; positive in moderation, a "
             "defect when sharp"],
            ["Other (faults)", "Papery, musty, earthy, rubber, medicinal", "Old coffee, storage and "
             "microbial taints"]]
    s.append(tbl(["Category", "Notes in this family", "Usually comes from"], rows, [90, 200, W - 290],
                 font_size=7.4))
    s.append(src("SCA and World Coffee Research Coffee Taster's Flavor Wheel and Sensory Lexicon (2016)."))
    return s


def coffee_house():
    s = [h2("1.8 India's coffee houses")]
    s.append(p("The Coffee Board opened its first India Coffee House in Bombay in 1936 to promote coffee "
               "drinking. When the Board closed them in the 1950s, laid-off workers, backed by the "
               "communist leader A. K. Gopalan, took them over as co-operatives (from 1957). The Indian "
               "Coffee House chain, run by workers' co-operatives to this day, became a meeting place for "
               "writers, students and politicians, with College Street in Kolkata and Connaught Place in "
               "Delhi among the most famous branches. It shows that cafés as social spaces are not new in "
               "India; what is new is the scale, the specialty focus and the prices."))
    return s


def sustainability():
    s = [h2("12.10 The footprint of a cup")]
    s.append(p("Life-cycle studies of coffee consistently find two hot spots: <b>farming</b> (fertiliser, "
               "land-use change if forests are cleared, processing energy and water) and, for milk drinks, "
               "<b>the milk itself</b>, which usually accounts for most of a latte's carbon footprint. "
               "Brewing energy, cups and waste come next. India's shade-grown, largely deforestation-free "
               "coffee starts with an advantage."))
    s += bl(["Offer plant milks and smaller milk drinks; price them fairly.",
             "Avoid single-use cups for dine-in; offer a discount for reusable cups.",
             "Compost or donate spent grounds; recycle valve bags where possible.",
             "Buy from estates that can document shade cover and deforestation-free land (EUDR data helps)."])
    return s


def checklist():
    s = [h2("Seed-to-cup quality checklist")]
    rows = [["Variety & altitude", "Which variety? How high? Shade-grown?", "Unknown origin, 'blend' with no "
             "details"],
            ["Picking", "Selective? Ripeness checks? Floating?", "Strip-picked, mixed ripeness"],
            ["Processing", "Washed / natural / honey; fermentation control; drying method and days",
             "Sour, mouldy or 'ferment' notes"],
            ["Grading", "Grade, screen size, defect count, moisture 10-12%", "Many broken or black beans"],
            ["Green storage", "Harvest date; hermetic bags; cool store", "Past-crop, woody, papery"],
            ["Roasting", "Profile, roast date, roast level for the method", "Scorched, baked or tipped "
             "beans"],
            ["Packaging", "Valve bag, roast date, 7-30 day window", "Only a 'best before' date"],
            ["Grinding", "Burr grinder, ground to order, right size", "Pre-ground, blade grinder"],
            ["Water", "Filtered, ~150 mg/L TDS", "Hard tap water or pure RO"],
            ["Recipe", "Weighed dose and yield; correct temperature and time", "Scoops and guesses"],
            ["Serving", "Clean cups and wands; milk at 60-65°C", "Scalded milk, dirty equipment"]]
    s.append(tbl(["Link", "What to ask or check", "Red flags"], rows, [90, 240, W - 330], font_size=7.4))
    return s
