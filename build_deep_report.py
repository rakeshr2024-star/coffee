#!/usr/bin/env python3
"""Build Coffee_Deep_Dive_and_Cafe_Model.pdf.

Part 1: coffee from seed to cup and its market (research report).
Part 2: inputs and outputs of the Ahmedabad café financial model; every number is read from
cafe_model/results.json, produced by running Cafe_Financial_Model.xlsx (cafe_model/export_results.py).

Run:  python3 build_deep_report.py
"""
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, Frame, NextPageTemplate, PageBreak, PageTemplate,
                                Spacer, Table, TableStyle)

import build_report as R
import deep_base as B
import deep_part1a as P1
import deep_part1b as P1B
import deep_part2 as P2
import deep_lastmile as LM
from deep_base import (CARAMEL, CONTENT_W, CREMA, ESPRESSO, HX, ROAST, SAFFRON, TEAL, P,
                       PartDivider, PartMarker, bl, h2, note)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Coffee_Deep_Dive_and_Cafe_Model.pdf")
PAGE_W, PAGE_H = A4
MARGIN = R.MARGIN
W = CONTENT_W

PART1 = [(1, "The big picture"), (2, "Growing coffee"), (3, "Harvesting"), (4, "Processing"),
         (5, "Milling, grading and quality"), (6, "Trade, prices and the money"), (7, "Roasting"),
         (8, "Grinding"), (9, "The science of brewing"), (10, "Brewing methods, step by step"),
         (11, "Tasting and judging quality"), (12, "From roaster to customer"), (13, "The coffee market")]
PART2 = [(14, "The brief and the model"), (15, "Where: choosing the hub"), (16, "Inputs and assumptions"),
         (17, "Comparing the configurations"), (18, "The four models to pursue"),
         (19, "Risk: scenarios and sensitivities"), (20, "Recommendation and roadmap"), ("A", "Appendix")]


# --------------------------------------------------------------------------- page decorations
STRIPE = [HX("#8DB86A"), HX("#D9CC72"), HX("#D39A55"), HX("#A86A38"), HX("#7A4A2A"), HX("#4D2F1C"),
          HX("#24150E")]


def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(ESPRESSO)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    cx, cy = PAGE_W * 0.72, PAGE_H * 0.43
    for r, col, a in [(150, CARAMEL, 0.16), (122, CREMA, 0.09), (100, ROAST, 0.9), (85, HX("#3B2416"), 1),
                      (60, CARAMEL, 0.25), (34, CREMA, 0.18)]:
        c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=a))
        c.circle(cx, cy, r, stroke=0, fill=1)
    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.5))
    c.circle(cx, cy, 100, stroke=1, fill=0)
    sw = PAGE_W / len(STRIPE)
    for i, col in enumerate(STRIPE):
        c.setFillColor(col)
        c.rect(i * sw, PAGE_H - 14, sw + 1, 14, stroke=0, fill=1)
    c.setFillColor(SAFFRON)
    c.setFont("Body-Bold", 10)
    c.drawString(MARGIN + 2, PAGE_H - 66, "DEEP-DIVE RESEARCH REPORT  •  INDIA  •  OCTOBER 2026")
    c.setFillColor(colors.white)
    c.setFont("Head", 42)
    c.drawString(MARGIN, PAGE_H - 122, "From Seed to Cup")
    c.setFont("Head", 26)
    c.setFillColor(CREMA)
    c.drawString(MARGIN, PAGE_H - 156, "and a Café in Ahmedabad")
    c.setFont("Head-Italic", 13.5)
    lines = ["How coffee is grown, processed, traded, roasted, ground and brewed,",
             "how the market works, and a three-statement + DCF model of a",
             "specialty café across four sites, two premises options,",
             "three roasting routes and four bean mixes."]
    for i, ln in enumerate(lines):
        c.drawString(MARGIN, PAGE_H - 190 - i * 18, ln)
    y = PAGE_H - 290
    for title, items in (("PART 1  •  COFFEE, FROM SEED TO CUP", PART1),
                         ("PART 2  •  THE CAFÉ MODEL", PART2)):
        c.setFont("Body-Bold", 8.5)
        c.setFillColor(SAFFRON)
        c.drawString(MARGIN, y, title)
        y -= 14
        for num, t in items:
            c.setFillColor(CARAMEL)
            c.setFont("Head", 9.5)
            c.drawRightString(MARGIN + 16, y, str(num))
            c.setFillColor(CREMA)
            c.setFont("Body", 9.2)
            c.drawString(MARGIN + 22, y, t)
            y -= 12.6
        y -= 8
    a = P2.m("A")["scalars"]
    tiles = [("178.8 m", "bags: record world crop 2025/26"), ("0.04 kg", "coffee per Indian per year"),
             ("5,339", "branded cafés in India, +12.7%"),
             (f"₹{a['npv']:,.0f} lakh", "NPV, best café model (Base)")]
    tw = (PAGE_W - 2 * MARGIN - 3 * 8) / 4
    for i, (big, small) in enumerate(tiles):
        x = MARGIN + i * (tw + 8)
        yy = 70
        c.setFillColor(colors.Color(1, 1, 1, alpha=0.07))
        c.roundRect(x, yy, tw, 58, 6, stroke=0, fill=1)
        c.setFillColor(R.SERIES[i])
        c.rect(x, yy + 54, tw, 4, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Body-Bold", 17)
        c.drawString(x + 8, yy + 28, big)
        c.setFont("Body", 7.4)
        c.setFillColor(CREMA)
        c.drawString(x + 8, yy + 12, small)
    c.setFont("Body", 8)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.6))
    c.drawString(MARGIN, 34, "Desk research from public sources available to 10 Oct 2026. Model figures in ₹ "
                             "lakh (1 lakh = ₹1,00,000); see Cafe_Financial_Model.xlsx.")
    c.restoreState()


def draw_body_bg(c, doc):
    c.saveState()
    c.setFillColor(R.PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    sw = PAGE_W / len(STRIPE)
    for i, col in enumerate(STRIPE):
        c.setFillColor(col)
        c.rect(i * sw, PAGE_H - 5, sw + 1, 5, stroke=0, fill=1)
    c.restoreState()


def draw_body_fg(c, doc):
    c.saveState()
    c.setFont("Body-Bold", 7.4)
    c.setFillColor(ROAST)
    c.drawString(MARGIN, PAGE_H - 17, "FROM SEED TO CUP, AND A CAFÉ IN AHMEDABAD")
    c.setFont("Body", 7.4)
    c.setFillColor(R.MUTED)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 17, B.STATE["part"])
    c.setStrokeColor(R.RULE)
    c.setLineWidth(0.6)
    c.line(MARGIN, PAGE_H - 21, PAGE_W - MARGIN, PAGE_H - 21)
    c.line(MARGIN, 22, PAGE_W - MARGIN, 22)
    c.setFillColor(ROAST)
    c.circle(PAGE_W / 2, 13, 7.5, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Body-Bold", 7.5)
    c.drawCentredString(PAGE_W / 2, 10.6, str(doc.page))
    c.setFillColor(R.MUTED)
    c.setFont("Body", 6.8)
    c.drawString(MARGIN, 11, "Prices and data as of October 2026")
    c.drawRightString(PAGE_W - MARGIN, 11, "Model: Cafe_Financial_Model.xlsx")
    c.restoreState()


# --------------------------------------------------------------------------- front matter
def contents():
    s = [PartMarker("Contents"), P('<font name="Head" size="22" color="#2B1A12">Contents</font>', R.BODY),
         Spacer(1, 8)]
    st = ParagraphStyle("tc", parent=R.BODY, fontSize=9.2, leading=10.6, spaceAfter=0)
    stp = ParagraphStyle("tcp", parent=R.BODY, fontName="Body-Bold", fontSize=9, textColor=SAFFRON,
                         spaceBefore=6)
    rows, style = [], [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 1.2),
                       ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2)]

    def add(num, title, key, desc):
        pg = B.TOC.get(key, "")
        rows.append([P(f'<font name="Head" size="11" color="#C68B59">{num}</font>', st),
                     P(f"<b>{title}</b>  <font size='7.4' color='#7A6F66'>{desc}</font>", st),
                     P(f'<font name="Body-Bold">{pg}</font>', ParagraphStyle("pg", parent=st, alignment=2))])
        style.append(("LINEBELOW", (0, len(rows) - 1), (-1, len(rows) - 1), 0.4, R.RULE))

    rows.append([P("", st), P("FRONT MATTER", stp), P("", st)])
    add("", "Executive summary", "exec", "The answers in two pages")
    rows.append([P("", st), P("PART 1  •  COFFEE, FROM SEED TO CUP AND ITS MARKET", stp), P("", st)])
    descs1 = ["What coffee is, the value chain, world and India in numbers",
              "Plant, species, varieties, terroir, Indian regions, nurseries, the farming year",
              "Ripeness, picking methods, yield arithmetic",
              "Washed, natural, honey, monsooned, experimental; drying",
              "Curing works, Indian grades, defects, cupping",
              "How Indian coffee is sold, futures, price history, who earns what",
              "Chemistry, roast levels, machines, profiles, freshness, economics",
              "Particle size, burrs vs blades, grind by method, dialling in",
              "Extraction, variables, water, why so many methods, milk",
              "Espresso, pour-over, filter kaapi, French press, AeroPress, moka, cold brew and more",
              "Vocabulary, flavour wheel, defects in the cup, tasting plan",
              "Packaging, channels, café formats, the Indian coffee customer",
              "Global and Indian supply, demand, café chains, Ahmedabad; glossary"]
    for (num, t), d in zip(PART1, descs1):
        add(num, t, f"c{num}", d)
    rows.append([P("", st), P("PART 2  •  A SPECIALTY CAFÉ IN AHMEDABAD: THE MODEL", stp), P("", st)])
    descs2 = ["Decisions, workbook structure, conventions",
              "Eight hubs screened, four sites modelled",
              "Drivers, menu, beans, people, costs, capex, funding, WACC",
              "20 configurations; rent vs own; roasting and bean mix",
              "Sindhu Bhavan Road, GIFT City, Prahladnagar, SBR owned",
              "Tornado, two-way tables, unit economics, risks",
              "What to do, launch timeline, what to verify",
              "Full Base-case statements for the lead model; sources"]
    for (num, t), d in zip(PART2, descs2):
        add(num, t, f"c{num}" if num != "A" else "app", d)
    add("", "Sources", "sources", "Where the facts and numbers come from")
    t = Table(rows, colWidths=[28, W - 70, 42])
    t.setStyle(TableStyle(style))
    s.append(t)
    return s


def exec_summary():
    a, b, c, d = (P2.m(x)["scalars"] for x in "ABCD")
    s = [PageBreak(), PartMarker("Executive summary"), B.Chapter("exec", "i", "Executive summary",
                                                                 "The answers in two pages", ESPRESSO),
         Spacer(1, 6)]
    s.append(h2("Part 1: coffee from seed to cup"))
    s += bl(["<b>Coffee is a fruit seed with a long chain.</b> From research station and nursery to cup takes "
             "3-5 years for a new plant and 6-18 months for each crop, passing through grower, curing "
             "works, trader or exporter, roaster, distributor and café.",
             "<b>Quality is made upstream and lost downstream.</b> Variety, altitude, ripe-only picking and "
             "careful processing set the ceiling; stale roasts, bad grinding, wrong water and sloppy recipes "
             "decide how much of it reaches the cup.",
             "<b>Processing is a flavour choice.</b> Washed coffees are clean and bright; naturals and "
             "honeys fruity and full; India's monsooned coffee is mellow and heavy; new anaerobic and "
             "carbonic methods are loud and expensive.",
             "<b>Every brewing method trades clarity for body.</b> Pressure (espresso, moka), percolation "
             "(pour-over, kaapi), immersion (French press, cold brew) and boiling (Turkish) exist because "
             "they produce different cups from the same bean, each suited to a culture and a moment.",
             "<b>Grinding and water are under-rated.</b> Uniform particles and SCA-standard water improve "
             "every cup more than a pricier machine.",
             "<b>The market is volatile and growing.</b> World prices roughly tripled between 2019 and 2025; "
             "India grows about 6.4 million bags, exports 70% and drinks just 0.04 kg per person, but its "
             "café market (5,339 branded outlets) is growing about 13% a year.",
             "<b>In a café, the coffee itself is ~6-10% of the price.</b> The grower receives roughly ₹13-20 "
             "of a ₹220 cappuccino; labour, rent, milk and service make up most of the rest."])
    s.append(h2("Part 2: the Ahmedabad café"))
    rows = []
    for fid in "ABCD":
        q = P2.m(fid)["scalars"]
        rows.append([P2.label(fid), P2.num(q["u_tot"]), P2.num(q["npv"]), P2.irr_txt(q["irr_p"]),
                     P2.irr_txt(q["irr_e"]), B.yrs(q["payback"]), P2.num(P2.sc(fid, "npv", "Worst"))])
    s.append(B.tbl(["Model (toll roasting, House blend)", "Capital ₹ L", "NPV ₹ L", "Proj. IRR", "Eq. IRR",
                    "Payback", "NPV Worst"], rows, [180, 52, 52, 52, 52, 52, W - 440], font_size=7.6,
                   center_cols=(1, 2, 3, 4, 5, 6)))
    s += bl([f"<b>Go to Sindhu Bhavan Road, rented, toll-roasted House blend (Model A)</b>: ₹{a['u_tot']:.0f} "
             f"lakh capital, NPV ₹{a['npv']:.0f} lakh, project IRR {P2.irr_txt(a['irr_p'])}, equity IRR "
             f"{P2.irr_txt(a['irr_e'])}, payback {B.yrs(a['payback'])}.",
             f"<b>GIFT City (Model B)</b> is the capital-light, most resilient alternative (₹{b['u_tot']:.0f} "
             f"lakh, NPV ₹{b['npv']:.0f} lakh) and the ideal second outlet.",
             f"<b>Prahladnagar (Model C)</b> works (NPV ₹{c['npv']:.0f} lakh, IRR {P2.irr_txt(c['irr_p'])}) but "
             "has thinner margins and more chain competition. <b>Sanand</b> is NPV-negative today.",
             f"<b>Rent, don't buy.</b> Owning at SBR (Model D) raises NPV to ₹{d['npv']:.0f} lakh but needs "
             f"₹{d['u_tot']:.0f} lakh and cuts the IRR to {P2.irr_txt(d['irr_p'])}.",
             "<b>Toll-roast from day one</b>: it beats buying roasted beans everywhere. Build an in-house "
             "roastery only once wholesale sales reach roughly 450-500 kg a month.",
             "<b>Demand is the risk.</b> Bills per day and average bill move value most; in the Worst case "
             "every site loses money, and shutting after year 3 would cost close to the whole investment. "
             "Validate footfall before signing a lease."])
    s.append(note("Deliverables", [
        "<b>Coffee_Deep_Dive_and_Cafe_Model.pdf</b>: this report.",
        "<b>Cafe_Financial_Model.xlsx</b>: the full working (Cover with checks, Dashboard, Inputs, "
        "Locations, Sourcing, Capex, Model, DCF, Scenarios, Configs, Sources). Change any blue cell to "
        "test your own numbers."], TEAL))
    return s


def sources_page():
    s = [PageBreak(), B.Chapter("sources", "S", "Sources", "Main public sources consulted (accessed "
                                                           "October 2026)", HX("#7A6F66")), Spacer(1, 4)]
    items = [
        "Press Information Bureau, 'India's coffee sector' backgrounder (29 Nov 2025): area, livelihoods, "
        "exports, GI tags, KYK - pib.gov.in/PressReleasePage.aspx?PRID=2196210",
        "USDA FAS GAIN, India Coffee Annual IN2026-0026 (May 2026): production, yields, consumption, "
        "trade, costs - fas.usda.gov",
        "USDA FAS, Coffee: World Markets and Trade (Dec 2025; Jun 2026) - fas.usda.gov / apps.fas.usda.gov",
        "International Coffee Organization, monthly Indicator Prices (2019-2025) and Coffee Market Report "
        "(Apr 2025) - icocoffee.org",
        "Coffee Board of India: quality specifications ('Coffee Karma'), consumption surveys, crop "
        "estimates, Fine Cup / KYK - coffeeboard.gov.in",
        "Central Coffee Research Institute releases; TNAU Agritech portal (coffee); Counter Culture Coffee, "
        "India's arabica varieties",
        "StoneX and Deccan Herald on the 2025-26 Indian crop; Daily Coffee News India reports (2024-25)",
        "Specialty Coffee Association: espresso survey (25 Magazine #3), Golden Cup and water standards, "
        "green grading handbook, cupping protocol and CVA",
        "FAO post-harvest manual; Sweet Maria's processing glossary; Barista Hustle; Perfect Daily Grind",
        "Roasting science: thermal contaminants review (PMC10138461); roaster guides (Gevi, Coffeeness, "
        "Royal NY); Aaroasta (Rajkot) product range",
        "Grinding: Counter Culture, Mahlkönig and Niche notes on burr geometry; Honest Coffee Guide, Bean "
        "Box and The Coffee Locator grind charts",
        "Brewing recipes: James Hoffmann via Hario USA; Lamose; Seven Coffee Roasters; Food & Wine and "
        "Wikipedia on Indian filter coffee",
        "Instant coffee: ScienceDirect topic pages (spray and freeze drying), Sinothermo, Sucafina",
        "Value chain: AgEcon Search study of India's robusta chain; GCP/IDH/Solidaridad 'The Grounds for "
        "Sharing' (2024); Selina Wamucii",
        "Market: World Coffee Portal Project Café India 2025 (via Comunicaffe); IMARC, Grand View, EMR "
        "market sizing; company filings and press (Tata Starbucks, Blue Tokai, Third Wave, CCD)",
        "Ahmedabad real estate: 99acres, MagicBricks, housing.com, otloo listings (Oct 2026)",
        "Sanand and GIFT City: Micron investor relations (Feb 2026); ET Electronics (Aug 2026); GIFT City "
        "RFPs and releases",
        "Costs: West End Coffee (La Marzocco pricing), Torrent Power tariff FY2026-27, Gujarat minimum "
        "wages (Apr 2026), Indeed/ERI barista pay, Swiggy/Zomato commission reports",
        "Finance: Trading Economics (India 10-year yield 7.29%, 8 Oct 2026), RBI policy (Oct 2026), "
        "Damodaran country risk premiums (Jan 2026), Income-tax Act (s.115BAA, depreciation rates)",
        "Modelling conventions: CFI Financial Modeling Guidelines; CFI 3-Statement Model template "
        "(supplied by the client)"]
    s += [P(f"{i}. {t}", R.SOURCE) for i, t in enumerate(items, 1)]
    s.append(Spacer(1, 6))
    s.append(note("How to read the numbers", [
        "Research facts are as published by the sources above; some (market sizes, chain revenues) come "
        "from secondary summaries and are flagged as indicative.",
        "Café demand inputs (bills per day, average bill, ramp-up) and the location scores are the "
        "author's judgement, triangulated with chain economics and local listings. They are the inputs "
        "to validate first.",
        "Illustrations are drawn in code; they are diagrams, not photographs."], R.MUTED, bg=HX("#F4F1EC")))
    return s


# --------------------------------------------------------------------------- story
def story():
    s = [NextPageTemplate("body"), PageBreak()]
    s += contents()
    s += exec_summary()
    s += [PageBreak(), PartMarker("Part 1 • Coffee, from seed to cup"),
          PartDivider("p1", 1, "Coffee, from\nseed to cup",
                      "How coffee is bred, grown, harvested, processed, graded, traded, roasted, ground and "
                      "brewed, and how the global and Indian markets work.", PART1, HX("#3B2416"))]
    for fn in (P1.ch1, P1.ch2, P1.ch3, P1.ch4, P1.ch5, P1.ch6, P1B.ch7, P1B.ch8, P1B.ch9, P1B.ch10,
               P1B.ch11, LM.ch12, P1B.ch13):
        s += fn()
    s += [PageBreak(), PartMarker("Part 2 • The café model"),
          PartDivider("p2", 2, "A specialty café\nin Ahmedabad",
                      "Inputs and outputs of the three-statement and FCFF valuation model: four sites, rent "
                      "or own, three roasting routes and four bean mixes, in three scenarios.", PART2,
                      HX("#1F4E5A"))]
    for fn in (P2.ch14, P2.ch15, P2.ch16, P2.ch17, P2.ch18, P2.ch19, P2.ch20, P2.appendix):
        s += fn()
    s += sources_page()
    return flatten(s)


def flatten(items):
    out = []
    for it in items:
        if isinstance(it, (list, tuple)):
            out += flatten(it)
        else:
            out.append(it)
    return out


def build():
    doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=25 * mm_(),
                          bottomMargin=13 * mm_(), title="From Seed to Cup, and a Café in Ahmedabad",
                          author="Coffee research report", subject="Coffee value chain, brewing, market; "
                          "Ahmedabad café 3-statement and DCF model", creator="ReportLab")
    cover = Frame(0, 0, PAGE_W, PAGE_H, id="cover", leftPadding=0, rightPadding=0, topPadding=0,
                  bottomPadding=0)
    body = Frame(MARGIN, 13 * mm_(), CONTENT_W, PAGE_H - 13 * mm_() - 25 * mm_(), id="body",
                 leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="cover", frames=[cover], onPage=draw_cover),
                          PageTemplate(id="body", frames=[body], onPage=draw_body_bg,
                                       onPageEnd=draw_body_fg)])
    doc.build([Spacer(1, 1)] + story())
    return doc


def mm_():
    from reportlab.lib.units import mm
    return mm


def main():
    build()                 # pass 1: collect page numbers
    first = dict(B.TOC)
    build()                 # pass 2: contents with page numbers
    if first != B.TOC:
        build()
    from pypdf import PdfReader
    n = len(PdfReader(OUT).pages)
    print("wrote", OUT, "pages:", n)


if __name__ == "__main__":
    main()
