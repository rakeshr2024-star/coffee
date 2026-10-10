"""Fifth round: a seed-to-cup case study, the whole chain on one page, processing equipment and a
first-time café owner's coffee FAQ."""
import build_report as R
import deep_charts as DC
from deep_base import (BERRY, CONTENT_W, LEAF, PLUM, ROAST, SAFFRON, SKY, TEAL, HX,
                       P, PageBreak, figc, h2, p, side, tbl)

W = CONTENT_W


def case_study():
    s = [h2("12.11 Case study: one bag from Chikmagalur to Ahmedabad")]
    s.append(p("Follow one 60 kg bag of washed arabica from a Chikmagalur estate to cups in an Ahmedabad "
               "café, using the prices and yields in this report."))
    rows = [["Mar 2025", "Blossom shower; flowers open, fruit sets", "Estate", "-"],
            ["Dec 2025", "~330 kg of ripe cherry picked over several passes (5.5 kg cherry per kg green)",
             "6-7 picker-days", "Labour paid per kg of cherry"],
            ["Dec 2025", "Pulped the same evening, fermented ~24 h, washed, dried 10-12 days to 10.5%",
             "Estate pulper house", "~75 kg of parchment"],
            ["Jan-Feb 2026", "Parchment rests, then sold to a curing works", "Grower → curer",
             "₹24,500 per 50 kg = ~₹36,750"],
            ["Feb 2026", "Hulled, graded Plantation A, colour-sorted, bagged: 60 kg green", "Curing works",
             "~₹612/kg green (estate specialty lot: ~₹950/kg)"],
            ["Mar 2026", "Trucked ~1,200 km to Gujarat; 3-4 days", "Transporter", "₹25/kg = ₹1,500"],
            ["Mar-Apr 2026", "Toll-roasted in batches to the café's espresso profile; 16% loss → 50.4 kg",
             "Roaster", "₹180/kg roasted = ₹9,072"],
            ["Apr-May 2026", "Rested 7 days, delivered fortnightly, ground to order", "Café", "-"],
            ["Apr-Jun 2026", "50.4 kg ÷ 18 g = ~2,800 double-shot drinks at ~₹220", "Customers",
             "~₹6.2 lakh of beverage sales (ex-GST)"]]
    s.append(tbl(["When", "What happens", "Who", "Money"], rows, [64, 250, 80, W - 394], font_size=7.3))
    spec = (57000 + 1500 + 9072) / 2800
    comm = (36750 + 1500 + 9072) / 2800
    s.append(side([DC.bar_chart(["Commodity Plantation A", "Estate specialty lot"],
                                [("Coffee cost per drink (₹)", [comm, spec], ROAST)], W * 0.42, 120,
                                title="Coffee cost per double-shot drink (₹)", fmt="{:.1f}")],
                  [p(f"From flower to cup took about 14 months, and from tree to cup five to six. The "
                     f"coffee inside each drink cost the café about <b>₹{comm:.0f}</b> for commodity "
                     f"Plantation A or <b>₹{spec:.0f}</b> for an estate specialty lot, against a ₹220 menu "
                     "price. The grower's ₹36,750-57,000 for the bag compares with roughly ₹6.2 lakh of "
                     "drinks sold: about <b>6-9%</b>, consistent with the value-chain estimates in "
                     "Chapter 6."),
                   p("The extra ₹7 a drink for an estate lot is why paying for quality is almost free "
                     "for a café, and why specialty cafés can afford to pay growers well above commodity "
                     "prices.")], lw=0.44))
    return s


def chain_on_a_page():
    steps = [("Research & seed", "Who: CCRI, Coffee Board, growers. Time: years of breeding; seed viable "
              "months. Value: certified seed."),
             ("Nursery", "Who: estate nurseries. Time: 6-8 months in polybags. Value: a healthy seedling."),
             ("Planting & growing", "Who: grower. Time: 3-4 years to first crop, 30+ years of bearing. Value: "
              "the variety and terroir potential."),
             ("Flowering & fruit", "Who: nature + grower. Time: blossom Feb-Apr, 8-11 months to ripe. "
              "Value: crop size."),
             ("Harvest", "Who: pickers. Time: Nov-Feb, 3-5 passes. Value: ripeness = sweetness. ~₹480-500/kg "
              "parchment at farm gate."),
             ("Farm processing", "Who: estate or trader. Time: 1 day pulping + 1-4 weeks drying. Value: "
              "clean or fruity profile; moisture 10-12%."),
             ("Curing", "Who: curing works. Time: weeks to months of storage, hours of milling. Value: grade, "
              "sorting. ~₹600-950/kg green."),
             ("Trade & export", "Who: traders, exporters. Time: contracts months ahead; 3-6 weeks shipping. "
              "Value: logistics, finance, risk."),
             ("Roasting", "Who: roaster. Time: 8-15 minutes + 2-14 days rest. Value: flavour development. "
              "~₹1,300-1,700/kg roasted."),
             ("Packaging & distribution", "Who: roaster, distributor, retailer. Time: days. Value: "
              "freshness, convenience. ~₹1,600-3,600/kg retail."),
             ("Grinding & brewing", "Who: barista or customer. Time: 30 s to 24 h. Value: extraction of the "
              "potential."),
             ("The cup", "Who: café and customer. Value: ~₹12,000 of drinks per kg of coffee; experience, "
              "service, place.")]
    cols = [LEAF, LEAF, LEAF, LEAF, BERRY, SAFFRON, SAFFRON, SKY, ROAST, PLUM, PLUM, HX("#2B1A12")]
    return [PageBreak(), h2("The whole chain on one page"),
            figc(DC.flow(steps, W, 560, per_row=3, colors_=cols, sub_size=7.6, head_size=9.0),
                 "Figure 13.1. Seed to cup: who does what, how long it takes and what each step adds. Prices "
                 "are Indian, October 2026.")]


def processing_equipment():
    s = [h2("4.13 The equipment of processing")]
    rows = [["Siphon / flotation tank", "Separates floaters from dense ripe cherries", "Estate pulper house"],
            ["Disc or drum pulper", "Squeezes beans out of skin and pulp", "Estate"],
            ["Eco-pulper / demucilager", "Pulps and scrubs off mucilage mechanically with little water", "Modern "
             "estates, co-operatives"],
            ["Fermentation tanks", "Concrete or steel tanks where mucilage breaks down", "Estate"],
            ["Washing channels", "Water channels that wash and density-grade parchment", "Estate"],
            ["Drying yards ('barbecues')", "Concrete or brick patios for parchment and cherry", "Estate, "
             "smallholders"],
            ["Raised beds and polytunnels", "Mesh beds with airflow; rain protection", "Specialty estates"],
            ["Mechanical dryers", "Rotating drums or vertical dryers at 40-45°C", "Large estates, curers"],
            ["Moisture meter", "Checks 10-12% target", "Everywhere"],
            ["Huller and polisher", "Remove parchment / husk and silver skin", "Curing works"],
            ["Screens, gravity table, optical sorter", "Grade by size and density; reject defects by colour",
             "Curing works"]]
    s.append(tbl(["Equipment", "Job", "Where"], rows, [130, 250, W - 380], font_size=7.4))
    return s


def faq():
    s = [h2("12.12 A first-time café owner's coffee FAQ")]
    qa = [("Which beans should I start with?", "A house blend of washed Indian estate arabica (about 70%), "
           "washed fine robusta (about 15%) for body and crema, and a micro-lot share for character; "
           "toll-roasted to your profile. Add one rotating single origin for pour-over."),
          ("Do I need my own roaster?", "Not at the start. Part 2 shows toll roasting beats an in-house "
           "roastery until you sell roughly 450-500 kg a month wholesale."),
          ("How fresh should the beans be?", "Use them 7-30 days after roasting; order every one to two "
           "weeks; never pre-grind."),
          ("Which espresso machine and grinders?", "A two-group multi-boiler machine (₹6-14 lakh + GST) and "
           "two on-demand espresso grinders plus one bulk grinder. Budget for AMC and spares."),
          ("How much coffee will I use?", "About 700-950 kg a year for drinks at 140-170 bills a day, plus "
           "450-650 kg for retail bags if you sell your own label (Part 2, year 3)."),
          ("How many baristas?", "A head barista plus four baristas covers two shifts and peaks; train them "
           "with your roaster and SCA courses, and dial in together every morning."),
          ("What water set-up?", "RO with remineralisation to about 150 mg/L TDS; about ₹1 lakh; change "
           "cartridges as rated."),
          ("How should I price drinks?", "Ingredients cost ₹25-65 a drink; price at ₹160-320 so beverage "
           "gross margins stay at 75-85%, and review prices every year."),
          ("Is robusta or chicory a problem?", "Not if declared and used for a purpose: fine robusta improves "
           "espresso and cold brew; a premium filter kaapi can use little or no chicory."),
          ("How do I know my coffee is good?", "Cup new lots blind, keep recipes written and weighed, track "
           "freshness, and read reviews weekly. A refractometer helps but is optional.")]
    for q, a in qa:
        s.append(P(f"<b>{q}</b> {a}", R.BODY_SM))
    return s


def scenario_paths(m_series, years):
    """Part 2 helper: revenue and EBITDA by scenario for one model."""
    rev = [(sn, m_series[sn]["is_rev"][1:], col) for sn, col in (("Best", TEAL), ("Base", ROAST),
                                                                   ("Worst", BERRY))]
    eb = [(sn, m_series[sn]["is_ebitda"][1:], col) for sn, col in (("Best", TEAL), ("Base", ROAST),
                                                                    ("Worst", BERRY))]
    return side([DC.line_chart(years[1:], rev, W * 0.49, 160, title="Revenue by scenario (₹ lakh)",
                               zero=True)],
                [DC.line_chart(years[1:], eb, W * 0.49, 160, title="EBITDA by scenario (₹ lakh)", zero=True)],
                lw=0.5)
