"""Additional depth for Part 1 chapters (history, estate economics, microbiology, cupping,
hedging, roast defects, decaf, espresso physics, caffeine, drink costing, kit guides, glossary)."""

import deep_charts as DC
from deep_base import (BERRY, CARAMEL, CONTENT_W, GOLD, ROAST, SAFFRON, SKY, TEAL, HX,
                       bl, figc, h2, h3, numbered, p, ps, side, src, tbl)

W = CONTENT_W

# Part 2 cost assumptions reused for drink costing (House blend, toll-roasted, FY28)
COFFEE_PER_G = 1482 / 1000      # ₹ per gram roasted
MILK_PER_ML = 68 / 1000         # ₹ per ml full-cream milk


# =============================================================================== ch1
def ch1():
    s = [h2("1.5 A short history of coffee")]
    events = [("~850 (legend)", "Kaldi, an Ethiopian goatherd, notices his goats dancing after eating "
               "red berries"),
              ("1400s", "Sufi monasteries in Yemen drink coffee to stay awake; port of Mocha"),
              ("1554", "First coffeehouses in Constantinople; later Venice (1645), London (1652)"),
              ("~1670", "Baba Budan smuggles seven seeds from Mocha to Chikmagalur's hills"),
              ("1696-99", "Dutch plant seedlings from India's Malabar coast in Java"),
              ("1720s", "De Clieu takes a plant to Martinique; coffee reaches Brazil (1727)"),
              ("1820s-40s", "British estates in Coorg, Chikmagalur, Wayanad, Nilgiris"),
              ("1870s", "Leaf rust destroys Ceylon's coffee and damages India's"),
              ("1884-1908", "Espresso patent in Turin (1884); paper filter (1908); instant (1901, "
               "Nescafé 1938)"),
              ("1936-57", "India Coffee House (1936); worker co-operatives take over (1957)"),
              ("1996-2016", "Café Coffee Day (1996), Tata Starbucks (2012), Blue Tokai (2013), "
               "Third Wave (2016)"),
              ("2026", "5,300+ branded cafés in India; Indian estates win global specialty "
               "recognition")]
    s.append(figc(DC.flow(events, W, 150, per_row=6, numbered=False,
                          colors_=[HX("#8E5B3E")] * 6 + [HX("#5B3A29")] * 6, sub_size=5.8, head_size=7.0),
                  "Figure 1.2. Twelve moments in coffee's history; India appears earlier than most people "
                  "think."))
    s.append(p("Coffee's spread followed trade and empire. Arab traders guarded the plant until "
               "pilgrims and colonial powers carried seeds out of Yemen. Indian coffee entered the story "
               "early: the Dutch planted Java with seedlings from the Malabar coast, and Baba Budan's "
               "seeds, planted in the hills that now bear his name, are among the oldest coffee "
               "plantings outside Arabia and Africa. British planters turned the Western Ghats into "
               "commercial estates in the 19th century; after rust struck, many switched to tea and to "
               "the hardier robusta, which still dominates India's crop."))
    s.append(h3("The 'waves' of coffee"))
    rows = [["First wave", "1800s-1960s", "Coffee as a mass commodity: vacuum tins, instant, percolators",
             "Instant and coffee-chicory blends; India Coffee House"],
            ["Second wave", "1970s-2000s", "Espresso-based café chains, flavoured milk drinks, branded "
             "experiences", "Café Coffee Day (1996), Barista (2000), Starbucks (2012)"],
            ["Third wave", "2000s-", "Coffee as craft: origin, traceability, lighter roasts, manual brewing",
             "Blue Tokai, Subko, KC Roasters, Black Baza and other estate-focused roasters"],
            ["'Fourth wave'", "2015-", "Science, experimental processing, sustainability, ready-to-drink "
             "specialty", "Anaerobic Indian micro-lots, cold-brew cans, specialty instant"]]
    s.append(tbl(["Wave", "Era", "What it means", "India's version"], rows, [68, 64, 190, W - 322],
                 font_size=7.5))
    s.append(h2("1.6 How to read a coffee bag"))
    rows = [["Origin / estate", "Country, region and farm, e.g. 'Ratnagiri Estate, Chikmagalur'",
             "The more specific, the more traceable"],
            ["Altitude", "Metres above sea level", "Higher usually means denser beans and brighter acidity"],
            ["Variety", "S.795, SL9, Chandragiri, Catuai, Gesha...", "Shapes the flavour potential"],
            ["Process", "Washed, natural, honey, anaerobic, monsooned", "Clean versus fruity (Chapter 4)"],
            ["Grade", "Plantation A/AA, PB, Robusta Parchment AB...", "Bean size and defect limits "
             "(Chapter 5)"],
            ["Roast date and level", "e.g. 'Roasted 2 Oct 2026, medium'", "Look for a roast date, not "
             "just 'best before'"],
            ["Tasting notes", "e.g. 'dark chocolate, orange, jaggery'", "Aromas the coffee resembles; "
             "nothing is added"],
            ["Score / award", "e.g. 'SCA 84', 'Fine Cup Award'", "80+ = specialty"],
            ["Blend ratio", "e.g. '80:20 coffee-chicory'", "Chicory is cheaper than coffee; check the share"]]
    s.append(tbl(["Label item", "Example", "Why it matters"], rows, [90, 220, W - 310], font_size=7.5))
    return s


# =============================================================================== ch2
def ch2():
    s = [h2("2.9 Why India grows mostly robusta: the economics per hectare")]
    s.append(side([DC.bar_chart(["Arabica", "Robusta"], [("Revenue per hectare, ₹ lakh",
                                                           [452 * 600 / 1e5, 1239 * 440 / 1e5], CARAMEL)],
                                W * 0.4, 130, title="Gross revenue per hectare (₹ lakh)",
                                sub="2026/27 yields x Oct-2026 green prices", fmt="{:.1f}")],
                  [p("Arabica sells for more per kilo, but robusta yields almost three times as much "
                     "per hectare in India (1,239 against 452 kg). At October 2026 prices (about ₹600/kg "
                     "for commodity arabica and ₹440/kg for robusta), a hectare of robusta grosses about "
                     "<b>₹5.5 lakh</b> against <b>₹2.7 lakh</b> for arabica, and robusta needs less labour "
                     "for pest control and is less exposed to white stem borer and rust. Arabica makes "
                     "sense at altitude, where quality premiums (estate specialty lots fetch ₹900-1,000/kg "
                     "and micro-lots far more) close the gap."),
                   p("This is why robusta makes up roughly three quarters of the crop, and why India's "
                     "specialty future depends on both better arabica and <b>fine (washed, selectively "
                     "picked) robusta</b>, a category where India is a world leader.")], lw=0.42))
    s.append(h2("2.10 Shade, biodiversity and sustainability"))
    s.append(p("Most Indian coffee grows under a two-tier canopy: tall native forest trees above and "
               "planted shade trees such as silver oak and dadap below, often with pepper vines climbing "
               "them. The Western Ghats are a global biodiversity hotspot, and shaded estates act as "
               "wildlife corridors for birds, elephants and other animals. Shade lowers yields "
               "slightly but slows ripening (better flavour), protects soil, reduces the need for "
               "chemicals and gives growers second incomes from pepper, cardamom, oranges and timber."))
    rows = [["Rainforest Alliance", "Environmental and social farm standard", "Widely used by Indian "
             "estates selling to Europe"],
            ["Fairtrade", "Minimum price + premium for smallholder co-operatives", "Limited in India"],
            ["Organic (NPOP / EU / USDA)", "No synthetic fertilisers or pesticides", "Araku, some Kerala "
             "and Karnataka growers"],
            ["Bird-friendly / shade", "Shade-cover standards (e.g. Smithsonian)", "A natural fit for "
             "Indian estates; used by brands such as Black Baza"],
            ["C.A.F.E. Practices, 4C", "Buyer-led (Starbucks) and baseline sustainability codes",
             "Large estates and exporters"],
            ["EU deforestation rule (EUDR)", "Proof that coffee was not grown on land deforested after "
             "2020", "Geolocation of every plot; costly for smallholders"]]
    s.append(tbl(["Scheme", "What it certifies", "Relevance in India"], rows, [110, 200, W - 310],
                 font_size=7.5))
    s.append(h2("2.11 Estate names worth knowing"))
    s.append(p("India's specialty reputation rests on a set of estates and growing communities. Examples "
               "that appear on Indian roasters' menus include <b>Ratnagiri, Baarbara, Kelagur and "
               "Thogarihunkal</b> (Chikmagalur), <b>Attikan</b> (Biligiris), <b>Balanoor, Watapi, "
               "Palthope and Yellikodige</b> (Karnataka's coffee belt), and the tribal farmer "
               "co-operatives of <b>Araku Valley</b>. Many sell micro-lots by variety and process, "
               "for example a natural S.795 or an anaerobic Chandragiri, which is exactly what a "
               "specialty café's pour-over menu and retail shelf need."))
    return s


# =============================================================================== ch3
def ch3():
    s = [h2("3.5 Measuring ripeness and harvest quality")]
    s.append(p("Specialty estates measure what they pick. A <b>colour count</b> of a sample (the share "
               "of ripe red cherries; specialty lots aim for 90-95% or more) and a <b>Brix "
               "refractometer</b> reading of the fruit's sugar (about 18-24° when ripe) tell the "
               "supervisor whether pickers are being selective enough. Because altitude delays "
               "ripening, the harvest moves uphill through the season: lower blocks are picked first, "
               "high blocks last, and estates make three to five passes through each block."))
    rows = [["Ripe-only picking", "Share of ripe cherries ≥ 90-95% in a sample"],
            ["Same-day processing", "Cherries pulped or laid out to dry within 6-12 hours"],
            ["Floating and sorting", "Floaters removed and sold as a separate lower grade"],
            ["Lot separation", "Each day's picking, block and variety kept apart and labelled"],
            ["Clean equipment", "Bags, tanks and pulpers washed daily to avoid ferment taints"],
            ["Records", "Weight, ripeness, Brix and processing notes per lot for traceability"]]
    s.append(tbl(["Good practice", "What to check"], rows, [130, W - 130], font_size=7.5))
    s.append(h2("3.6 Labour, cost and mechanisation"))
    s.append(p("Harvesting is the single largest labour job on an Indian estate, and labour is about "
               "70% of the cost of growing coffee. Pickers are paid by the kilo of cherry, so "
               "selective picking, which yields fewer kilos per day, must be rewarded with higher "
               "rates or quality bonuses. Labour has become scarcer and more expensive, and many "
               "estates rely on seasonal workers from other states. The Coffee Board has published "
               "planting designs that would allow small machines and mechanical aids between rows, "
               "but on steep, shaded, terraced slopes the full mechanical harvesting used in Brazil "
               "remains impractical. Expect Indian specialty coffee to stay hand-picked, and labour "
               "costs to keep rising faster than general inflation."))
    return s


# =============================================================================== ch4
def ch4():
    s = [h2("4.9 The microbiology of fermentation")]
    s.append(side([p("Fermentation is not just 'rotting off' the mucilage. Yeasts (such as "
                     "<i>Saccharomyces</i>, <i>Pichia</i> and <i>Candida</i>), lactic acid bacteria "
                     "and, later, acetic acid bacteria feed on the sugars and pectin. They produce "
                     "organic acids, alcohols and fruity esters, and the pH of the fermenting mass "
                     "falls from about 6 to 4-4.5. Some of these compounds migrate into the bean and "
                     "change its flavour."),
                   p("Time and temperature decide the outcome: a cool, short ferment gives clean "
                     "coffee; a warm, long one gives fruit, then wine, then vinegar. Over-fermentation "
                     "creates acetic, butyric and propionic acids (sour, cheesy, rancid). That is why "
                     "producers now monitor pH and temperature, and some add selected yeast or bacterial "
                     "cultures for repeatable results.")],
                  [DC.line_chart(["0 h", "6 h", "12 h", "18 h", "24 h", "30 h", "36 h", "48 h"],
                                 [("pH of fermenting mass", [6.0, 5.7, 5.2, 4.8, 4.6, 4.5, 4.4, 4.2],
                                   SAFFRON)], W * 0.42, 130,
                                 title="pH falls as microbes work (illustrative)", ylo=4.0, yhi=6.5,
                                 band=(3, 5, "typical stop window"))], lw=0.56))
    s.append(h2("4.10 Drying curves: slow and steady wins"))
    days = [str(d) for d in range(0, 22, 2)]
    washed = [52, 44, 36, 29, 23, 18, 14, 12, 11, 10.8, 10.6]
    natural = [60, 55, 49, 43, 37, 31, 25, 20, 16, 13, 11.5]
    s.append(side([DC.line_chart(days, [("Washed parchment", washed, TEAL), ("Natural cherry", natural, BERRY)],
                                 W * 0.5, 140, title="Moisture content while sun-drying (%, illustrative)",
                                 ylo=0, yhi=60, band=(8, 10, "target 10-12%"))],
                  [p("Coffee should dry evenly over one to three weeks. Drying too fast on hot concrete "
                     "cracks the parchment and 'bakes' flavour; drying too slowly invites mould and "
                     "ferment. Producers turn the coffee several times a day, cover it at night, and "
                     "stop at 10-12%, measured with a moisture meter."),
                   p("After drying, parchment rests for 30-60 days so moisture evens out between "
                     "beans before hulling. Water activity (a<sub>w</sub>, ideally 0.50-0.60) is "
                     "increasingly measured alongside moisture because it predicts shelf life.")],
                  lw=0.52))
    s.append(h2("4.11 Water, waste and by-products"))
    rows = [["Pulp and skin", "~40% of the cherry's weight", "Compost, biogas, or dried as "
             "<b>cascara</b> (a fruity 'coffee cherry tea')"],
            ["Mucilage and wash water", "Acidic, high in sugars; pollutes streams if untreated",
             "Settling ponds, biodigesters, recirculating eco-pulpers"],
            ["Parchment and husk", "Removed at curing", "Fuel for dryers and boilers, mulch"],
            ["Silver skin (chaff)", "Comes off in the roaster", "Compost; must be collected (fire risk)"],
            ["Spent coffee grounds", "~1 kg wet grounds per 55 doubles in a café", "Compost, mushroom "
             "growing, biofuel pilots"]]
    s.append(tbl(["By-product", "Where it comes from", "Uses"], rows, [100, 170, W - 270], font_size=7.5))
    s.append(p("Traditional wet mills used large volumes of water per kilo of green coffee; modern "
               "eco-pulpers and recirculation cut this sharply, and Indian pollution rules require "
               "effluent treatment. For a café, spent grounds are a visible sustainability story: "
               "partner with a composting or urban-farming group."))
    s.append(h2("4.12 Indian processing in practice"))
    rows = [["Plantation (washed arabica)", "Arabica", "Washed", "Estates in Chikmagalur, Biligiris, "
             "Pulneys, Shevaroys", "Clean, balanced, mild acidity"],
            ["Arabica Cherry", "Arabica", "Natural", "Smallholders and estates", "Heavier, fruit, less "
             "clean"],
            ["Robusta Parchment", "Robusta", "Washed", "Coorg, Wayanad estates", "Clean, chocolate, "
             "low bitterness; Kaapi Royale"],
            ["Robusta Cherry", "Robusta", "Natural", "Most smallholders", "Heavy, woody; bulk for "
             "instant and blends"],
            ["Monsooned Malabar", "Both", "Natural, then monsooned", "Malabar coast warehouses",
             "No acidity, syrupy, spicy"],
            ["Micro-lots", "Mostly arabica", "Honey, anaerobic, carbonic", "Specialty estates",
             "Fruit-forward, premium-priced"]]
    s.append(tbl(["Trade name", "Species", "Process", "Where", "Cup"], rows, [110, 50, 80, 140, W - 380],
                 font_size=7.4))
    return s


# =============================================================================== ch5
def ch5():
    s = [h2("5.5 Inside a cupping session")]
    s.append(side([*numbered(["Roast samples lightly (8-12 minutes) the day before; rest 8-24 hours.",
                              "Weigh 8.25 g per cup (five cups per coffee to check uniformity); grind "
                              "just before; smell the dry fragrance.",
                              "Pour 150 ml of water at 93°C; start the timer; smell the wet aroma.",
                              "At about 4 minutes, break the crust with a spoon, smell, then skim the "
                              "foam.",
                              "From about 70°C, slurp from the spoon and score; re-taste as it cools "
                              "to room temperature.",
                              "Compare scores and notes; flag any defective cup."])],
                  [tbl(["Attribute", "What is judged"],
                       [["Fragrance / aroma", "Dry and wet smell"], ["Flavour", "Overall taste + aroma"],
                        ["Aftertaste", "Length and pleasantness"], ["Acidity", "Brightness, quality"],
                        ["Body", "Texture, weight"], ["Balance", "Harmony"],
                        ["Uniformity, clean cup, sweetness", "Per cup, 2 points each"],
                        ["Overall", "Taster's judgement"], ["Defects", "Taints and faults subtracted"]],
                       [W * 0.2, W * 0.24], font_size=7.3)], lw=0.53))
    rows = [["Commercial robusta cherry", "Heavy, woody, bitter, earthy", "~70-78 (robusta protocol)",
             "Instant, low-cost blends"],
            ["Washed Plantation A arabica", "Chocolate, nuts, mild citrus, clean", "~80-83",
             "House espresso base"],
            ["Washed fine robusta (Kaapi Royale)", "Dark chocolate, malt, low bitterness", "~80-83 "
             "(Fine Robusta scale)", "Espresso blends, cold brew"],
            ["Estate natural S.795 micro-lot", "Berries, jaggery, wine, heavy body", "~84-86",
             "Pour-over, retail"],
            ["Anaerobic or carbonic micro-lot", "Tropical fruit, spice, boozy", "~86-88", "Showcase, "
             "competition"]]
    s.append(tbl(["Typical Indian coffee", "Cup profile", "Indicative score", "Best use"], rows,
                 [130, 160, 90, W - 380], font_size=7.4))
    s.append(src("Score ranges are indicative, based on published cupping scores of Indian lots in "
                 "roaster and competition listings; robusta is scored on the CQI Fine Robusta protocol."))
    s.append(h2("5.6 Specialty versus commercial coffee"))
    rows = [["Defects (per 350 g)", "0 primary, ≤5 full defects", "Many tolerated"],
            ["Cup score", "80+ on the SCA scale", "Usually 70-79"],
            ["Traceability", "Estate, lot, variety, process known", "Region or country at best"],
            ["Picking and processing", "Ripe-only, controlled processing", "Strip-picked, variable"],
            ["Roast", "Light to medium, roast date shown", "Often dark, 'best before' only"],
            ["Price to grower", "Premium over futures, often fixed by contract", "Futures ± differential"],
            ["Where sold", "Specialty cafés, roasters' websites", "Supermarkets, instant, vending"]]
    s.append(tbl(["", "Specialty", "Commercial"], rows, [110, (W - 110) / 2, (W - 110) / 2], font_size=7.5))
    s.append(h2("5.7 Grading and quality institutions in India"))
    s.append(bl(["<b>Coffee Board of India</b>: sets grade specifications, runs quality labs and "
                 "liquoring (cupping), certifies exports, and organises the Flavour of India Fine Cup "
                 "Award (since 2002) and Know Your Kaapi.",
                 "<b>Q Graders</b>: professional cuppers certified by the Coffee Quality Institute; India "
                 "now has a growing pool, many at exporters and specialty roasters.",
                 "<b>Competitions</b>: the India Barista, Brewers and AeroPress championships (run with "
                 "the Specialty Coffee Association of India) push café standards upward."]))
    return s


# =============================================================================== ch6
def ch6():
    s = [h2("6.5 Price risk for a café, in rupees")]
    green_kg = 1500 / 0.84
    s.append(side([p("A busy specialty café uses about 1,500 kg of roasted coffee a year including "
                     f"retail bags, i.e. roughly <b>{green_kg:,.0f} kg of green coffee</b> (about 30 bags "
                     "of 60 kg). At the House blend's ₹1,073/kg green cost:"),
                   *bl([f"a <b>+30% price shock</b> costs about ₹{green_kg * 1073 * 0.3 / 1e5:.1f} lakh a "
                        "year, around 2-3 points of EBITDA margin;",
                        "a <b>-15%</b> move saves about "
                        f"₹{green_kg * 1073 * 0.15 / 1e5:.1f} lakh."]),
                   p("Small buyers cannot use futures easily (one contract is 17 tonnes), so the "
                     "practical hedges are <b>fixed-price contracts</b> with estates or curing works "
                     "for 6-12 months of supply, holding 2-3 months of green stock, and menu prices "
                     "reviewed every year.")],
                  [tbl(["Price driver", "Why it matters"],
                       [["Brazil weather", "Frost (2021) and drought (2023-24) hit a third of world supply"],
                        ["Vietnam robusta", "Drought cut output and lifted robusta prices"],
                        ["Stocks", "Five years of falling stocks (to 20.1 m bags)"],
                        ["Currencies", "A weak real boosts Brazil's sales; a weak rupee lifts Indian "
                         "prices"],
                        ["Funds", "Speculative positions amplify moves"],
                        ["Freight, rules", "Shipping costs, EUDR compliance, tariffs"]],
                       [W * 0.14, W * 0.3], font_size=7.2)], lw=0.53))
    s.append(h2("6.6 How an export shipment works"))
    steps = [("Register", "Exporter registers with the Coffee Board"),
             ("Contract", "Price fixed as futures ± differential, or flat; FOB or CIF terms"),
             ("Sample", "Pre-shipment sample cupped and approved by the buyer"),
             ("Prepare lot", "Curing works grades, sorts and bags to contract specs"),
             ("Certify", "ICO certificate of origin, quality and phyto certificates"),
             ("Ship", "Container stuffed and shipped, mostly from Mangalore"),
             ("Get paid", "Letter of credit or cash against documents")]
    s.append(figc(DC.flow(steps, W, 76, per_row=7, colors_=[SKY] * 7, sub_size=5.9, head_size=7.0),
                  "Figure 6.4. The steps of an Indian green-coffee export."))
    s.append(h2("6.7 The cast of characters"))
    rows = [["Growers", "~2.5 lakh, 98% smallholders; a few large estate companies", "Sell cherry/parchment "
             "or branded estate lots"],
            ["Consolidators & traders", "Village agents, dealers in coffee towns", "Aggregate, finance "
             "and transport small lots"],
            ["Curing works", "Dry mills in Chikmagalur, Hassan, Kushalnagar, Mangalore", "Hull, grade, "
             "sort; often also trade"],
            ["Exporters", "Global trading houses and Indian exporters", "Contract, hedge, ship to "
             "128 countries"],
            ["Instant makers", "Tata Consumer, CCL Products, Nestlé India, HUL", "41% of exports; most "
             "domestic consumption"],
            ["Roasters", "National brands (Coffee Day, Bru, Narasu's...) and 300+ specialty roasters",
             "Blend, roast, brand"],
            ["Cafés and retailers", "Chains, independents, supermarkets, online, quick commerce",
             "Brew, serve, sell to the end customer"],
            ["Institutions", "Coffee Board, CCRI, planters' associations, SCAI", "Research, standards, "
             "promotion"]]
    s.append(tbl(["Actor", "Who", "Role"], rows, [100, 220, W - 320], font_size=7.4))
    return s


# =============================================================================== ch7
def ch7():
    s = [h2("7.7 Roast defects and how to spot them")]
    rows = [["Underdeveloped", "Too little time after first crack; centre still pale",
             "Grassy, peanut, sour, astringent"],
            ["Baked", "Rate of rise stalled or crashed; roast dragged on", "Flat, bready, papery, dull"],
            ["Scorched", "Drum too hot at charge; burn marks on the flat side", "Smoky, ashy, bitter"],
            ["Tipped", "Too much heat early; burnt tips of the bean", "Burnt, sharp"],
            ["Overdeveloped / dark", "Too long or too hot after first crack", "Bitter, carbon, origin lost"],
            ["Quakers", "Unripe beans that will not brown", "Peanut, cereal; pick them out"]]
    s.append(tbl(["Defect", "Cause", "Taste"], rows, [90, 220, W - 310], font_size=7.5))
    s.append(h2("7.8 Building an espresso blend"))
    s.append(p("Blends exist to produce a consistent, balanced espresso all year as single lots come and "
               "go. Each component has a job. A good Indian espresso blend can be built entirely from "
               "Indian coffees:"))
    rows = [["Base (50-70%)", "Washed Plantation arabica, medium roast", "Chocolate, nuts, sweetness, "
             "balance", "S.795 or Chandragiri from Chikmagalur"],
            ["Fruit / acidity (10-20%)", "Natural or honey arabica, or high-grown washed", "Lift, berry, "
             "citrus", "Natural micro-lot, Pulneys arabica"],
            ["Body / crema (10-30%)", "Washed fine robusta", "Crema, body, cocoa; cuts through milk",
             "Robusta Kaapi Royale"],
            ["Spice / depth (0-10%)", "Monsooned Malabar", "Syrupy body, spice, low acid",
             "Monsooned Malabar AA"]]
    s.append(tbl(["Role", "Component", "Contribution", "Indian example"], rows, [90, 140, 140, W - 370],
                 font_size=7.4))
    s.append(p("The Part 2 'House blend' (15% washed robusta, 70% estate arabica, 15% micro-lot) follows "
               "this logic: chocolatey and milk-friendly, with a micro-lot share that justifies a "
               "specialty price."))
    s.append(h2("7.9 Decaffeination"))
    rows = [["Swiss Water / water process", "Green beans soaked in a caffeine-free extract of green "
             "coffee; caffeine filtered out with carbon", "Chemical-free; premium"],
            ["Supercritical CO2", "CO2 under high pressure dissolves caffeine selectively", "Good flavour "
             "retention; industrial"],
            ["Ethyl acetate ('sugarcane')", "Solvent derived from fermentation (often of sugarcane)",
             "Common for Colombian decaf; fruity"],
            ["Methylene chloride", "Direct or indirect solvent method", "Cheapest; residues tightly "
             "limited"]]
    s.append(tbl(["Method", "How", "Notes"], rows, [120, 230, W - 350], font_size=7.4))
    s.append(p("Decaf is not caffeine-free: EU rules require roasted decaf to contain no more than 0.1% "
               "caffeine (about 97% removed). Indian demand is small, so most cafés buy imported decaf "
               "beans; it is still worth offering for evening customers."))
    s.append(h2("7.10 Packaging and shelf life"))
    rows = [["Whole beans, one-way valve bag", "Best 7-30 days after roast; 2-3 months sealed",
             "Specialty retail, cafés"],
            ["Ground, valve bag", "Best within 1-2 weeks of opening", "Convenience; filter kaapi powder"],
            ["Nitrogen-flushed tins / bags", "6-12 months sealed", "Supermarkets"],
            ["Drip bags and steep bags", "Weeks to months (single-serve, sealed)", "Offices, travel, gifting"],
            ["Capsules / pods", "Months (oxygen barrier)", "Home and office machines"],
            ["Cold brew bottles / cans", "Days (fresh) to months (retorted)", "Retail fridges, quick "
             "commerce"],
            ["Instant jars and sachets", "12-24 months", "Mass market"]]
    s.append(tbl(["Format", "Freshness", "Used for"], rows, [140, 200, W - 340], font_size=7.4))
    return s


# =============================================================================== ch8
def ch8():
    s = [h2("8.6 Buying a café grinder: what to look for")]
    rows = [["Burr size and type", "64-98 mm flat or 60-80 mm conical", "Speed, heat, uniformity"],
            ["Dosing", "By time (on-demand) or by weight (grind-by-weight)", "Consistency at peak hours"],
            ["Retention", "Grams left inside after grinding", "Stale grounds in the next shot"],
            ["Adjustment", "Stepless micrometric adjustment", "Fine control when dialling in"],
            ["Heat and speed", "Cooling fans, slower RPM", "Stable grind through rush hours"],
            ["Service", "Local spares, burr availability, AMC", "Uptime in India"]]
    s.append(tbl(["Feature", "Good spec", "Why"], rows, [110, 220, W - 330], font_size=7.5))
    s.append(p("Practical tips: a light spritz of water on beans before grinding (the 'Ross droplet "
               "technique') reduces static and clumping; single-dose grinders suit pour-over bars; and "
               "for filter kaapi grind fine but not powdery, adding chicory after grinding if used."))
    return s


# =============================================================================== ch9
def ch9():
    s = [h2("9.6 Espresso physics")]
    s.append(side([p("Espresso is percolation under pressure. The pump pushes water at about 9 bar into "
                     "a puck of fine coffee that resists the flow; a well-made puck lets roughly 1.5-2 g "
                     "of espresso through per second. Gases and oils emulsify into crema. Because "
                     "contact time is short, espresso needs fine grinding, fresh coffee and very stable "
                     "temperature."),
                   p("<b>Channelling</b> is the enemy: if the puck has a weak spot (uneven "
                     "distribution, a crack, a tilted tamp), water rushes through it, over-extracting "
                     "that path and under-extracting the rest; the shot tastes sour and bitter at "
                     "once. <b>Pre-infusion</b> (wetting the puck at low pressure for a few seconds) "
                     "and <b>pressure profiling</b> (ramping pressure up and down) reduce channelling "
                     "and let baristas shape flavour.")],
                  [tbl(["Espresso target", "Typical range"],
                       [["Brew ratio (dose : yield)", "1:1.5 to 1:2.5"], ["Strength (TDS)", "8-12%"],
                        ["Extraction yield", "18-22%"], ["Pressure", "~9 bar at the puck"],
                        ["Temperature", "90-96°C"], ["Flow", "~1.5-2 g per second"],
                        ["Time", "25-30 s for 1:2"]], [W * 0.22, W * 0.2], font_size=7.4)], lw=0.56))
    s.append(h2("9.7 How much caffeine is in each drink?"))
    drinks = [("Black tea, 240 ml", 45), ("Decaf coffee, cup", 4), ("Instant, 1 tsp", 70),
              ("Filter kaapi, tumbler", 75), ("Single espresso", 70), ("Double espresso / cappuccino", 135),
              ("Filter / pour-over, 240 ml", 140), ("Cold brew, 240 ml", 190),
              ("Robusta-heavy double espresso", 220)]
    s.append(side([DC.hbar_chart([a for a, _ in drinks], [b for _, b in drinks], W * 0.55, 150,
                                 title="Typical caffeine per serving (mg, midpoint of usual ranges)",
                                 colors_=[GOLD, HX("#BDB3A7"), SAFFRON, SAFFRON, ROAST, ROAST, TEAL, SKY,
                                          BERRY], label_w=118, ref=200, ref_label="200 mg single dose")],
                  [p("Caffeine varies with species (robusta has about twice as much), dose, and method. "
                     "The European Food Safety Authority considers up to <b>400 mg a day</b> safe for "
                     "healthy adults (about three cappuccinos or two large filter coffees), single doses "
                     "up to 200 mg, and up to 200 mg a day in pregnancy."),
                   p("For a café menu, label strong drinks (cold brew, robusta-heavy shots) and offer "
                     "decaf and half-caf; evening trade in Ahmedabad is large.")], lw=0.58))
    s.append(src("EFSA Scientific Opinion on caffeine safety (2015); typical ranges from USDA FoodData "
                 "Central and café menus."))
    return s


# =============================================================================== ch10
def ch10():
    s = [h2("10.16 Espresso machines for a café")]
    rows = [["Single boiler", "One boiler for brewing and steam; switch between them", "Home only",
             "₹15,000-60,000"],
            ["Heat exchanger (HX)", "Steam boiler heats brew water through a coil", "Small cafés; needs "
             "flushing", "₹2-6 lakh (commercial)"],
            ["Multi-boiler", "Separate, temperature-controlled boiler per group + steam boiler",
             "Specialty cafés", "Brewlyn 2GR ₹6.3 lakh; La Marzocco Linea PB 2GR ₹11.3 lakh (+GST)"],
            ["Pressure / flow profiling", "Programmable pressure or paddle-controlled flow", "High-end "
             "specialty", "La Marzocco PBX ₹13.7 lakh; Strada X ₹26 lakh+"],
            ["Super-automatic", "Grinds, tamps, brews and steams at a button", "Offices, QSR, hotels",
             "₹1.5-8 lakh"]]
    s.append(tbl(["Type", "How it works", "Suits", "Indicative price (India, Apr 2026)"], rows,
                 [90, 190, 90, W - 370], font_size=7.4))
    s.append(src("West End Coffee price comparison (Apr 2026); Kaapi Machines; distributor listings."))
    s.append(h2("10.17 Troubleshooting"))
    rows = [["Espresso sour, fast", "Grind too coarse, dose too low, coffee too fresh or stale",
             "Grind finer; check dose; rest beans 7+ days"],
            ["Espresso bitter, slow", "Grind too fine, dose too high, water too hot", "Grind coarser; "
             "lower dose or temperature"],
            ["Pour-over stalls", "Too fine, fines clogging paper, too much agitation", "Coarser; gentler "
             "pours"],
            ["French press muddy", "Too fine; plunged too hard", "Coarser; skim and wait; plunge to "
             "surface only"],
            ["Kaapi drips too slowly", "Powder too fine or pressed hard", "Slightly coarser; rest the disc "
             "lightly"],
            ["Milk big bubbles", "Wand too high, milk too warm", "Start cold; keep tip just under surface; "
             "stop at 60-65°C"]]
    s.append(tbl(["Problem", "Likely cause", "Fix"], rows, [100, 200, W - 300], font_size=7.4))
    s.append(h2("10.18 What each drink costs a café to make"))
    drinks = [("Double espresso", 18, 0, 2, 160), ("Cappuccino", 18, 180, 3, 230), ("Latte", 18, 250, 3, 250),
              ("Indian cold coffee", 18, 200, 25, 260), ("Cold brew (300 ml)", 22, 0, 6, 240),
              ("V60, House blend", 15, 0, 4, 220), ("V60, micro-lot", 15, 0, 4, 320),
              ("Specialty filter kaapi", 12, 120, 1, 160)]
    rows, costs, margins = [], [], []
    for name, g, ml, other, price in drinks:
        cg = g * (COFFEE_PER_G if "micro" not in name else (2200 / 0.84 + 205) / 1000)
        cm = ml * MILK_PER_ML
        tot = cg + cm + other
        rows.append([name, f"{g} g", f"₹{cg:.0f}", f"{ml} ml" if ml else "–", f"₹{cm:.0f}" if ml else "–",
                     f"₹{other:.0f}", f"₹{tot:.0f}", f"₹{price}", f"{1 - tot / price:.0%}"])
        costs.append(tot)
        margins.append(price - tot)
    s.append(tbl(["Drink", "Coffee", "Coffee ₹", "Milk", "Milk ₹", "Other ₹", "Total cost", "Menu price",
                  "Gross margin"], rows, [100] + [(W - 100) / 8] * 8, font_size=7.3,
                 center_cols=(1, 2, 3, 4, 5, 6, 7, 8)))
    s.append(side([DC.bar_chart([d[0].replace("Specialty ", "").replace(", House blend", "")
                                 .replace("Double ", "").replace("Indian ", "") for d in drinks],
                                [("Ingredient cost", costs, ROAST), ("Gross margin", margins, CARAMEL)],
                                W * 0.6, 150, title="Cost and gross margin per drink (₹)", stacked=True,
                                fmt="{:,.0f}", cat_size=5.8)],
                  [p("Coffee drinks earn gross margins of <b>75-90%</b>; 'other' covers sugar, syrups, ice "
                     "cream, filter papers and cup. Milk drinks cost more but sell for more. The real "
                     "costs of a café sit below the gross margin: staff, rent and overheads (Part 2)."),
                   ps("Costing uses Part 2's House-blend, toll-roasted coffee at ₹1,482/kg (₹2,824/kg "
                      "for a micro-lot) and full-cream milk at ₹68/litre; menu prices are indicative for "
                      "Ahmedabad specialty cafés (ex-GST).")], lw=0.62))
    s.append(h2("10.19 Getting started at home"))
    rows = [["Under ₹3,000", "V60 or filter-kaapi set, paper filters, kitchen scale (₹500-800)",
             "Pre-ground fresh coffee from a local roaster, used within 2 weeks"],
            ["₹10,000-15,000", "Hand burr grinder (₹4,000-8,000), V60 or AeroPress, gooseneck kettle, scale",
             "Whole-bean single estates; grind fresh"],
            ["₹50,000+", "Entry espresso machine with steam wand, espresso grinder, tamper, milk jug",
             "Medium-roast espresso blend; learn to dial in"]]
    s.append(tbl(["Budget", "Kit", "Beans"], rows, [80, 260, W - 340], font_size=7.4))
    return s


# =============================================================================== ch11
def ch11():
    s = [h2("11.4 A four-week tasting plan")]
    s += numbered(["<b>Week 1, processing:</b> taste a washed and a natural coffee from the same region side "
                   "by side as pour-over. Note clarity versus fruit and body.",
                   "<b>Week 2, roast:</b> compare a light and a dark roast of similar beans as French "
                   "press. Note acidity, sweetness and bitterness.",
                   "<b>Week 3, method:</b> brew one coffee three ways (V60, French press, AeroPress). "
                   "Note how body and clarity change.",
                   "<b>Week 4, espresso and milk:</b> taste a shot alone, then as a cortado and a latte. "
                   "Note how milk changes acidity and sweetness, and why espresso blends include "
                   "robusta.",
                   "Throughout, write three words for each cup using the flavour wheel. Within a month most "
                   "people can tell washed from natural and light from dark."])
    s.append(h2("11.5 Judging a café, not just a cup"))
    rows = [["Sourcing", "Estate and roast date on the menu or bag; staff can explain the beans"],
            ["Freshness", "Beans 7-30 days off roast; ground to order"],
            ["Brewing", "Weighed doses and yields; clean group heads and grinders"],
            ["Milk", "Glossy microfoam, not scalded (no hotter than ~65°C)"],
            ["Range", "Espresso, at least one manual method, a cold option, decaf"],
            ["Water and hygiene", "Filtered water; clean cups, jugs and steam wands"],
            ["Experience", "Speed at rush hour, seating, service, value"]]
    s.append(tbl(["Area", "Signs of a good café"], rows, [90, W - 90], font_size=7.5))
    return s


# =============================================================================== glossary
GLOSSARY = [
    ("Arabica / robusta", "The two commercial coffee species (Coffea arabica, C. canephora)"),
    ("Bloom", "Bubbling release of CO2 when hot water first wets fresh grounds"),
    ("Body", "Weight and texture of coffee in the mouth"),
    ("Brix", "Sugar content of cherry fruit, measured with a refractometer"),
    ("Channelling", "Water finding a weak path through an espresso puck"),
    ("Cherry (grade)", "Indian name for natural (dry-processed) coffee"),
    ("Chicory", "Roasted root blended with coffee in South Indian filter powder"),
    ("Crema", "Golden foam on espresso: emulsified oils and CO2"),
    ("Cupping", "Standardised professional tasting and scoring of coffee"),
    ("Curing works", "Indian dry mill: hulls, grades and sorts green coffee"),
    ("Decoction", "Strong coffee extract from a South Indian filter"),
    ("Development time", "Roast time after first crack (typically 15-25% of the roast)"),
    ("Differential", "Premium or discount of a physical lot over the futures price"),
    ("Extraction yield", "Share of the coffee's weight dissolved into the drink"),
    ("First crack", "Audible popping as beans expand at ~196-205°C"),
    ("Fines / boulders", "Very small / very large particles in a grind"),
    ("Green coffee", "Unroasted, processed and hulled coffee beans"),
    ("Honey process", "Pulped coffee dried with some mucilage left on"),
    ("ICE 'C'", "New York arabica futures contract, priced in US cents per lb"),
    ("Kaapi Royale", "Premium Indian washed robusta grade"),
    ("Maillard reaction", "Browning reaction between sugars and amino acids"),
    ("Micro-lot", "Small, separately processed lot from one farm block or variety"),
    ("Monsooned", "Indian process: coffee exposed to monsoon winds for 12-16 weeks"),
    ("Mucilage", "Sticky, sugary layer between pulp and parchment"),
    ("Natural process", "Cherries dried whole with the fruit on"),
    ("Outturn", "Share of clean coffee obtained from parchment or dried cherry"),
    ("Parchment", "Papery husk around the bean; Indian name for washed robusta"),
    ("Peaberry (PB)", "A single round bean in a cherry"),
    ("Plantation (grade)", "Indian name for washed arabica"),
    ("Q grader", "Cupper certified by the Coffee Quality Institute"),
    ("Rate of rise", "Speed at which bean temperature rises during roasting"),
    ("Ratio", "Coffee to water (or espresso yield) by weight, e.g. 1:16"),
    ("Screen size", "Sieve hole size used to grade beans (in 64ths of an inch)"),
    ("Specialty coffee", "Coffee scoring 80+ with minimal defects"),
    ("TDS", "Total dissolved solids: the strength of brewed coffee"),
    ("Third wave", "Coffee as craft: origin, traceability, careful roasting and brewing"),
    ("Toll roasting", "Paying a roaster to roast your own green coffee"),
    ("Washed process", "Fruit removed and mucilage fermented off before drying")]


def glossary():
    half = (len(GLOSSARY) + 1) // 2
    left = tbl(["Term", "Meaning"], [list(x) for x in GLOSSARY[:half]], [74, W / 2 - 80], font_size=7.0)
    right = tbl(["Term", "Meaning"], [list(x) for x in GLOSSARY[half:]], [74, W / 2 - 80], font_size=7.0)
    return [h2("Glossary of coffee terms"), side([left], [right])]
