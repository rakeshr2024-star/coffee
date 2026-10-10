"""Third round of Part 1 depth: numbers at a glance, estate day, small roastery, industrial grinding,
iced production, myths, pairing, café design, licences & GST, consumption per head."""
from reportlab.lib import colors

import deep_charts as DC
import illustrations as il
from deep_base import (BERRY, CONTENT_W, GOLD, LEAF, PLUM, ROAST, SAFFRON, SKY, TEAL, HX,
                       bl, h2, kpi_tiles, p, side, src, tbl)

W = CONTENT_W


def numbers():
    s = [h2("1.7 The coffee economy at a glance")]
    s.append(kpi_tiles([("178.8 m bags", "world crop 2025/26 (10.7 m tonnes)", ROAST),
                        ("~12.5 m", "coffee farms worldwide, mostly < 5 ha", LEAF),
                        ("~70", "producing countries in the bean belt", TEAL),
                        ("2 bn+", "cups drunk around the world every day", SAFFRON),
                        ("6.4 m bags", "India's crop; 7th-largest producer", BERRY),
                        ("US$2.06 bn", "India's coffee exports, 2025", SKY),
                        ("0.04 kg", "coffee per Indian per year (world 1.3 kg)", PLUM),
                        ("5,339", "branded cafés in India, +12.7% in a year", GOLD)], cols=4))
    s.append(src("USDA FAS; ICO; PIB; World Coffee Portal. Cups per day is a widely cited industry estimate."))
    return s


def estate_day():
    s = [h2("3.7 A harvest day at an Indian estate")]
    rows = [["7:00-12:30", "Picking", "Gangs work assigned blocks; selective picking of ripe cherries into "
             "baskets and sacks"],
            ["12:30-14:00", "Weighing", "Each picker's cherries weighed at the field shed; ripeness spot-checks; "
             "piece-rate recorded"],
            ["14:00-17:00", "Second round & transport", "Afternoon picking; cherries trucked to the pulper house"],
            ["17:00-21:00", "Floating & pulping", "Siphon tank removes floaters; pulper runs into the night; "
             "pulped beans go to fermentation tanks"],
            ["Overnight", "Fermentation", "12-36 hours depending on temperature; checked for 'grit'"],
            ["Next morning", "Washing & grading", "Channels wash off mucilage; heavy beans separated"],
            ["Following 1-2 weeks", "Drying", "Parchment spread on concrete 'barbecues' or raised beds, raked, "
             "covered at night"],
            ["Weeks later", "Rest & dispatch", "Parchment bagged, rested, then sent to curing works with lot "
             "records"]]
    s.append(tbl(["Time", "Step", "What happens"], rows, [70, 100, W - 170], font_size=7.4))
    s.append(p("Naturals follow a simpler path: after floating, cherries go straight to drying yards for "
               "12-15 days. For smallholders without a pulper, selling fresh cherry or dried cherry to a "
               "trader is the norm, which is one reason most Indian robusta is natural."))
    return s


def small_roastery():
    s = [h2("7.12 Setting up a small roastery")]
    rows = [["Space", "150-500 sqft in light-industrial or commercial premises; floor loading, drainage"],
            ["Roaster", "3-5 kg drum roaster (Indian makers in Rajkot and elsewhere; imported options); the "
             "Part 2 model budgets ₹9 lakh for a 3 kg machine"],
            ["Smoke control", "Afterburner or catalytic unit, chimney and ducting (₹2.5 lakh in the model); "
             "essential in a city"],
            ["Utilities", "LPG/PNG line or electric supply; three-phase power; ventilation"],
            ["Approvals", "FSSAI manufacturing licence; pollution-control consent (GPCB) where required; "
             "fire NOC; trade licence"],
            ["Quality kit", "Sample roaster, moisture meter, scales, sealer, cupping set (₹1.5 lakh)"],
            ["People", "A trained roaster who also manages green buying, QC and wholesale accounts"],
            ["Throughput", "~8-12 kg roasted per hour; one shift a week covers a single café's needs"]]
    s.append(tbl(["Item", "What it takes"], rows, [80, W - 80], font_size=7.4))
    s.append(p("The numbers explain the Part 2 verdict: the roastery's fixed costs (salary, AMC, extra space, "
               "depreciation) are about ₹7-9 lakh a year, while roasting a single café's 1,500 kg in "
               "house rather than by toll saves only about ₹2 lakh. Wholesale volume is what fills the "
               "machine and the profit gap."))
    return s


def industrial_grinding():
    s = [h2("8.7 Grinding at scale: packaged ground coffee and kaapi powder")]
    s.append(p("Supermarket ground coffee and South Indian filter powder are ground on industrial roller or "
               "large disc grinders that produce very uniform particles at high speed, often followed by "
               "'normalising' to set density. Because ground coffee stales fast, packers flush bags or tins "
               "with nitrogen and seal immediately; filter-coffee shops in South India traditionally "
               "roast and grind daily in small batches, which is why freshly ground kaapi powder from a "
               "neighbourhood shop tastes so different. For a café selling retail coffee, the best "
               "practice is to sell whole beans and offer to grind on request for the customer's "
               "brewer."))
    return s


def iced_production():
    s = [h2("10.23 Producing cold drinks for a café")]
    rows = [["Cold brew", "Batch of 1-2 kg coffee in 10-20 litres; steep 16 h in the fridge; filter; store "
             "≤5°C", "5-7 days", "Label batch date; discard after shelf life"],
            ["Japanese iced", "Brewed to order on ice", "Immediate", "Showcase drink; uses micro-lots"],
            ["Iced espresso drinks", "Fresh shot over ice and cold milk", "Immediate", "Speed; pre-portion "
             "milk and syrups"],
            ["Indian cold coffee", "Blended to order or from a pre-mixed base", "Base: same day", "Highest "
             "ingredient cost; watch portion control"],
            ["Syrups", "Jaggery, cardamom, vanilla made in-house", "2-3 weeks refrigerated", "Cheaper and a "
             "point of difference"]]
    s.append(tbl(["Drink", "Production", "Shelf life", "Notes"], rows, [90, 210, 70, W - 370], font_size=7.4))
    s.append(p("In Ahmedabad's long hot season cold drinks can be half of beverage sales, so the bar needs "
               "ice capacity (a commercial ice machine is in the model's kitchen budget), fridge space for "
               "cold brew and a fast blender station that does not block the espresso line."))
    return s


def myths():
    s = [h2("11.6 Common myths")]
    rows = [["'Dark roast has more caffeine'", "Roasting barely changes caffeine; by volume a dark roast "
             "has slightly less because beans are lighter"],
            ["'Espresso has the most caffeine'", "Per serving a 240 ml filter coffee usually has more than a "
             "single espresso"],
            ["'Robusta is always bad'", "Washed, carefully processed fine robusta can score 80+ and is "
             "prized in espresso"],
            ["'Thick crema means quality'", "Crema shows freshness and robusta content, not flavour quality"],
            ["'Fresher is always better'", "Coffee needs a few days to degas; very fresh coffee brews "
             "unevenly"],
            ["'Store beans in the fridge'", "Moisture and odours ruin them; use an airtight container in a "
             "cool cupboard (freeze only sealed, portioned bags)"],
            ["'Boiling water burns coffee'", "Just-off-boil water (93-96°C) is ideal for most filter brewing"],
            ["'Chicory is fake coffee'", "It is a traditional, labelled ingredient in South Indian filter "
             "coffee; the issue is only undeclared or excessive use"]]
    s.append(tbl(["Myth", "Reality"], rows, [150, W - 150], font_size=7.4))
    s.append(h2("11.7 Pairing coffee with food"))
    rows = [["Washed light-roast pour-over", "Fresh fruit, citrus tarts, light cakes", "Acidity echoes fruit"],
            ["Indian espresso / cappuccino", "Dark chocolate, croissants, almond biscotti", "Chocolate notes "
             "match"],
            ["Natural or anaerobic micro-lot", "Berry desserts, cheesecake", "Fruit-forward pairing"],
            ["Filter kaapi", "Idli, vada, upma, Mysore pak", "The classic South Indian breakfast"],
            ["Cold brew", "Savoury sandwiches, khakhra, nachos", "Low acidity, smooth"],
            ["Monsooned Malabar / dark", "Gujarati farsan, spiced cookies", "Spice meets spice"]]
    s.append(tbl(["Coffee", "Food", "Why it works"], rows, [140, 200, W - 340], font_size=7.4))
    return s


def _floorplan(c, w, h):
    sc = min(w / 50, h / 26)
    ox, oy = (w - 40 * sc) / 2, 10

    def box(x, y, bw, bh, col, lab, sub="", tc=il.INK):
        c.setFillColor(col)
        c.setStrokeColor(colors.white)
        c.setLineWidth(1)
        c.rect(ox + x * sc, oy + y * sc, bw * sc, bh * sc, stroke=1, fill=1)
        il.text(c, ox + (x + bw / 2) * sc, oy + (y + bh / 2) * sc + 1, lab, 7.0, "Body-Bold", tc, "middle")
        if sub:
            il.text(c, ox + (x + bw / 2) * sc, oy + (y + bh / 2) * sc - 7, sub, 5.8, "Body", tc, "middle")
    c.setStrokeColor(il.ROAST)
    c.setLineWidth(1.6)
    c.rect(ox, oy, 40 * sc, 25 * sc, stroke=1, fill=0)
    box(0, 17, 12, 8, HX("#D9CBB8"), "Kitchen", "prep, cold room")
    box(12, 21, 6, 4, HX("#E8DFD2"), "Store", "dry + bean stock")
    box(18, 21, 6, 4, HX("#E8DFD2"), "Wash-", "room")
    box(0, 11, 12, 6, HX("#C68B59"), "Coffee bar", "espresso, grinders", colors.white)
    box(0, 8, 12, 3, HX("#A86A38"), "Counter + POS", "pick-up & delivery", colors.white)
    box(24, 18, 16, 7, HX("#F3E5D0"), "Lounge seating", "sofas, 10-12 seats")
    box(14, 4, 26, 13, HX("#FBF1E3"), "Café floor", "tables, 26-30 seats")
    box(0, 0, 12, 7, HX("#EAF3F8"), "Retail shelf", "beans, gear")
    box(12, 0, 2, 3, HX("#8DB86A"), "", "")
    c.setFillColor(il.BERRY)
    il.arrow(c, ox + 26 * sc, oy - 6, ox + 26 * sc, oy + 3 * sc, il.BERRY, 1.4, 5)
    il.text(c, ox + 26 * sc + 6, oy - 4, "Entrance (street frontage)", 6.6, "Body-Bold", il.BERRY)
    il.text(c, ox, oy + 25 * sc + 5, "Schematic 1,000 sqft café (not to exact scale)", 7.4, "Body-Bold",
            il.ROAST)


def cafe_design():
    s = [h2("12.8 Designing the café")]
    s.append(side([il.CanvasFigure(W * 0.5, 210, _floorplan)],
                  [p("A 1,000 sqft specialty café (the Part 2 size for Prahladnagar) typically gives about "
                     "60% of its area to customers and 40% to the bar, kitchen, storage and washroom. "
                     "Design choices that matter most:"),
                   *bl(["<b>Bar visible from the entrance</b>: the espresso machine is theatre and signals "
                        "quality.",
                        "<b>Separate order, pick-up and delivery points</b> so aggregator riders do not "
                        "crowd seated guests.",
                        "<b>Seating mix</b>: two-tops for work and dates, a long communal table, a lounge for "
                        "evening groups; power points and good Wi-Fi.",
                        "<b>Acoustics and light</b>: soft surfaces, warm light in the evening, daylight in "
                        "the morning.",
                        "<b>Back of house</b>: RO plant, ice machine, cold room, dishwash and bean storage "
                        "away from heat."])], lw=0.52))
    s.append(h2("12.9 Licences, GST and the rules of the game"))
    rows = [["FSSAI", "Registration (turnover up to ₹12 lakh) or State licence (₹12 lakh-₹20 crore)",
             "Mandatory before opening; display the number"],
            ["Shop & Establishment", "Gujarat Shops and Establishments registration", "Within 30 days of "
             "opening"],
            ["GST", "Restaurant services at 5% without input-tax credit (standalone cafés); packaged beans "
             "and instant coffee at 5%", "GST registration above the turnover threshold"],
            ["Fire NOC", "From the fire department for eating houses above size thresholds", "Before "
             "opening"],
            ["Trade / eating-house licence", "From the municipal corporation (AMC) and police where "
             "applicable", "Annual renewal"],
            ["Signage & music", "Signage permission; IPRS/PPL licences for background music", "Before use"],
            ["Labour", "PF, ESI registration and minimum wages (Gujarat schedule)", "On hiring"]]
    s.append(tbl(["Area", "What is needed", "When"], rows, [100, 260, W - 360], font_size=7.3))
    s.append(src("FSSAI licensing thresholds; GST rates for restaurant services; Gujarat labour rules. "
                 "Check current rules with a consultant before opening."))
    return s


def per_capita():
    s = [h2("13.10 How much coffee the world drinks per person")]
    data = [("Finland", 12.0), ("Norway", 9.9), ("Netherlands", 8.4), ("Sweden", 8.2), ("Brazil", 6.3),
            ("Germany", 5.5), ("USA", 4.7), ("Japan", 3.3), ("Vietnam", 2.9), ("World average", 1.3),
            ("China", 0.25), ("India", 0.04)]
    s.append(side([DC.hbar_chart([a for a, _ in data], [b for _, b in data], W * 0.52, 190,
                                 title="Coffee per person per year (kg of green coffee, approximate)",
                                 colors_=[SKY] * 9 + [GOLD, BERRY, BERRY], fmt="{:.1f}", label_w=70)],
                  [p("Nordic countries drink the most coffee in the world, about 10-12 kg per person a year, "
                     "or three to four cups a day. India drinks about 0.04 kg per person, roughly one "
                     "three-hundredth of Finland's level and a thirtieth of the world average. China, "
                     "starting from a similar base, has seen explosive café growth over the past decade."),
                   p("The arithmetic of India's opportunity is simple: if Indian consumption rose to just "
                     "0.1 kg per head, the domestic market would more than double, absorbing part of today's "
                     "exports. Café culture, specialty coffee and cold coffee are the "
                     "channels through which that is happening in cities like Ahmedabad.")], lw=0.54))
    s.append(src("Nordic countries and Germany: ICO and industry estimates (rounded); others: USDA FAS "
                 "2025/26 consumption divided by population; India: USDA Post (May 2026)."))
    return s
