"""Part 1, chapters 1-6: the big picture, growing, harvesting, processing, grading, trade."""
import build_report as R
import deep_charts as DC
import deep_figs as DF
import deep_more as M
import deep_more2 as M2
import deep_more3 as M3
import deep_more4 as M4
import deep_more5 as M5
import deep_more6 as M6
import deep_more7 as M7
import illustrations as il
from deep_base import (BERRY, CARAMEL, CONTENT_W, GOLD, LEAF, PLUM, ROAST, SAFFRON, SKY, TEAL, HX,
                       chapter, figc, h2, lead, note, p, side, src, tbl)

W = CONTENT_W


# =============================================================================== 1. big picture
def ch1():
    s = chapter("c1", 1, "The big picture", "What coffee is, how it travels from seed to cup, and where "
                "India fits", ESPRESSO_C)
    s.append(lead("Coffee is the roasted seed of a cherry. Between the research station that breeds the "
                  "plant and the cup in your hand sit a dozen steps, five or six owners, and between two "
                  "and six years. Each step can add flavour, destroy it, or simply add cost. "
                  "This part of the report walks that whole chain, then looks at the market it feeds."))
    s.append(h2("1.1 What coffee actually is"))
    s.append(p("Coffee shrubs belong to the genus <i>Coffea</i> in the Rubiaceae family (the gardenia "
               "family). Two species matter commercially. <b>Arabica</b> (<i>Coffea arabica</i>), "
               "originally from the highlands of Ethiopia and South Sudan, gives roughly 55-60% of the "
               "world's coffee and nearly all specialty coffee. <b>Robusta</b> (<i>Coffea canephora</i>), "
               "from the lowland forests of central and west Africa, gives the other 40-45%. It is "
               "hardier, higher-yielding and carries about twice the caffeine. India grows both, and "
               "robusta makes up about three quarters of its crop."))
    s.append(p("The fruit is a <b>coffee cherry</b>. Inside it, two seeds lie face to face: these are "
               "the coffee beans. In about 5-10% of cherries only one seed develops; it grows round and "
               "is sold separately as <b>peaberry</b>. A raw (\"green\") bean is hard, smells of peas "
               "and grass, and makes an unpleasant drink. Roasting creates more than 800 aroma "
               "compounds and turns the seed into what we recognise as coffee. Coffee is grown in "
               "about 70 countries in the tropical \"bean belt\" between the Tropics of Cancer and "
               "Capricorn, on roughly 12.5 million farms, most of them smaller than five hectares."))
    s.append(h2("1.2 The value chain at a glance"))
    steps = [("Research & seed", "Breeders select varieties; certified seed from mother plants (CCRI, "
              "Balehonnur)"),
             ("Nursery", "Seeds germinate in sand beds, grow 6-8 months in polybags"),
             ("Planting & growing", "Planted at monsoon; 3-4 years to first crop; 30+ years of bearing"),
             ("Flowering & fruit", "Blossom showers in Feb-Apr; cherries ripen in 8-11 months"),
             ("Harvest", "Arabica Nov-Jan, robusta Dec-Feb; mostly hand-picked in India"),
             ("Farm processing", "Washed, natural or honey; dried to 10-12% moisture in 1-4 weeks"),
             ("Curing (dry mill)", "Hulling, grading by size and density, colour sorting, bagging"),
             ("Trading & export", "Traders, curers and exporters price off New York and London futures"),
             ("Shipping & import", "Containers via Mangalore; 3-6 weeks to Europe"),
             ("Roasting", "8-15 minutes at 180-240°C; rest 2-14 days; packed in valve bags"),
             ("Distribution", "Cafés, hotels, supermarkets, online and quick-commerce"),
             ("Brewing & serving", "Grinding and brewing take 30 seconds to 24 hours")]
    s.append(figc(DC.flow(steps, W, 168, per_row=4, colors_=[LEAF, LEAF, LEAF, LEAF, R.BERRY, SAFFRON,
                                                              SAFFRON, SKY, SKY, ROAST, PLUM, PLUM]),
                  "Figure 1.1. Twelve steps from seed to cup. Green = farm, orange = processing, blue = "
                  "trade, brown = roasting, purple = selling and brewing."))
    rows = [["Grower", "Farm-gate parchment or cherry", "₹480-500/kg arabica parchment (₹24,100-24,800 "
             "per 50 kg, Oct 2026)", "Years of cultivation, picking, processing"],
            ["Curer / trader", "Clean green coffee, graded", "₹600-950/kg (commodity to estate specialty)",
             "Hulling, grading, sorting, logistics, risk"],
            ["Roaster", "Roasted beans, wholesale", "₹1,050-1,700/kg; micro-lots ₹3,000+",
             "16% weight loss, roasting skill, packing, brand"],
            ["Retailer", "Retail bag", "₹1,600-3,600/kg (₹400-900 per 250 g)", "Shelf, marketing, "
             "freshness"],
            ["Café", "Beverages", "~₹12,000 of drinks per kg of coffee (55 doubles at ₹220)",
             "Labour, rent, milk, skill, experience"]]
    s.append(tbl(["Owner", "What changes hands", "Typical price (India, Oct 2026)", "What they add"],
                 rows, [64, 120, 175, W - 359], font_size=7.6))
    s.append(src("Coffee Board indicative prices; Part 2 sourcing assumptions; Indian roaster price lists."))
    s.append(h2("1.3 The world of coffee in numbers"))
    prod = [("Brazil", 63.0), ("Vietnam", 30.8), ("Colombia", 13.8), ("Ethiopia", 12.0),
            ("Indonesia", 12.0), ("Uganda", 6.9), ("India", 6.4), ("Honduras", 5.8)]
    cons = [("United States", 26.55), ("Brazil", 22.28), ("Philippines", 6.75), ("Japan", 6.72),
            ("China", 5.85), ("Vietnam", 4.90), ("India", 1.36)]
    left = DC.hbar_chart([a for a, _ in prod], [b for _, b in prod], W / 2 - 6, 150,
                         title="Production 2025/26, million 60-kg bags",
                         colors_=[CARAMEL if a != "India" else BERRY for a, _ in prod], fmt="{:.1f}",
                         label_w=62)
    right = DC.hbar_chart([a for a, _ in cons], [b for _, b in cons], W / 2 - 6, 150,
                          title="Consumption 2025/26, million bags (selected)",
                          colors_=[SKY if a != "India" else BERRY for a, _ in cons], fmt="{:.1f}",
                          label_w=70)
    s.append(side([left], [right]))
    s.append(src("USDA FAS, Coffee: World Markets and Trade (Dec 2025, Jun 2026); India figure from USDA "
                 "Post (May 2026)."))
    s.append(p("The 2025/26 world crop was a record <b>178.8 million bags</b> (about 10.7 million tonnes), "
               "against consumption of 173.9 million bags. Even so, ending stocks fell for a fifth "
               "straight year to 20.1 million bags, which is why prices stayed high. Brazil alone "
               "grows more than a third of the world's coffee, and Vietnam dominates robusta. For "
               "2026/27 USDA expects another record crop, with Brazil at 71.9 million bags, while "
               "consumption also reaches a record 179.7 million bags."))
    s.append(h2("1.4 India's place"))
    s.append(side([p("India is the world's <b>7th-largest producer</b> (about 3.5% of output) and "
                     "<b>5th-largest exporter</b> (about 5% of trade). Coffee covers about 4.9 lakh "
                     "hectares in the Western and Eastern Ghats, supports more than two million "
                     "livelihoods, and about 70% of the crop is exported to 128 countries. Around "
                     "99% of holdings are smallholdings, and they produce roughly 70% of the coffee."),
                   p("Indian coffee is unusual in one respect: almost all of it is <b>shade-grown</b> "
                     "under a two-tier canopy of about 50 native and planted tree species, intercropped "
                     "with pepper, cardamom, vanilla, oranges and bananas. Exports set a record of "
                     "<b>US$1.8 billion in FY2024-25</b> and about <b>US$2.06 billion in calendar 2025</b>. "
                     "Italy is the largest buyer, using Indian robusta in espresso blends.")],
                  [DC.donut([18.09, 11.01, 7.47, 5.28, 5.09, 53.06],
                            ["Italy", "Germany", "Belgium", "Russia", "UAE", "128 others"],
                            [TEAL, SKY, SAFFRON, PLUM, GOLD, HX("#BDB3A7")], W * 0.45, 128,
                            centre="$1.8 bn", centre_sub="exports FY25",
                            title="Where India's coffee goes (share of FY25 value)")], lw=0.55))
    s.append(src("PIB backgrounder on India's coffee sector (29 Nov 2025); Coffee Board; export press "
                 "reports Jan 2026."))
    s += M.ch1()
    s += M3.numbers()
    s += M4.coffee_house()
    return s


ESPRESSO_C = R.ESPRESSO


# =============================================================================== 2. growing
def ch2():
    s = chapter("c2", 2, "Growing coffee", "The plant, the two species, varieties, terroir, India's "
                "regions, nurseries and the farming year", LEAF)
    s.append(h2("2.1 The plant"))
    s.append(p("Left alone, an arabica plant grows into a small tree of 5-10 metres; on estates it is "
               "pruned to 1.5-2 metres so pickers can reach the fruit. Glossy, dark-green leaves grow "
               "in opposite pairs. White, jasmine-scented flowers appear in clusters where leaves meet "
               "the branch, open 8-10 days after a good shower of rain, and wilt within two or three "
               "days. The pollinated flowers become green berries that swell, then ripen from green to "
               "yellow to red (some varieties stay yellow). Arabica takes 8-9 months from flower to "
               "ripe cherry; robusta takes 10-11 months."))
    s.append(figc(il.CanvasFigure(W, 190, il.estate_scene),
                  "Figure 2.1. A shade-grown Indian estate: coffee bushes under silver oak and native "
                  "trees, with pepper vines climbing the shade trees."))
    s.append(p("The two species differ in their genetics, and that shapes everything downstream. "
               "<b>Arabica</b> has four sets of chromosomes (44) and pollinates itself, so its varieties "
               "breed true from seed. <b>Robusta</b> has two sets (22) and cannot pollinate itself; "
               "bees and wind must carry pollen between plants, so every robusta plant is genetically "
               "a little different. Robusta is often multiplied by rooting cuttings (clones) of the "
               "best bushes."))
    s.append(figc(il.CanvasFigure(W, 170, il.branch_scene),
                  "Figure 2.2. A fruiting branch: paired leaves, jasmine-like flowers and cherries ripening "
                  "unevenly along the same branch, which is why selective picking takes several passes."))
    s.append(h2("2.2 Arabica versus robusta"))
    rows = [["Share of world output", "~55-60%", "~40-45%"],
            ["Altitude in India", "1,000-1,500 m (up to 2,000 m in the Pulneys)", "500-1,000 m"],
            ["Comfortable temperature", "15-25°C", "20-30°C"],
            ["Chromosomes / pollination", "44, self-pollinating", "22, needs cross-pollination"],
            ["Caffeine (dry weight)", "1.2-1.5%", "2.2-2.7%"],
            ["Sugars (sucrose)", "6-9%", "3-7%"],
            ["Lipids (oils)", "15-17%", "10-11.5%"],
            ["Chlorogenic acids (bitterness precursors)", "5.5-8%", "7-10%"],
            ["Bean shape", "Oval, S-shaped centre cut", "Rounder, straight centre cut"],
            ["Yield in India (2026/27)", "452 kg/ha", "1,239 kg/ha"],
            ["Main threats", "Leaf rust, white stem borer", "Berry borer, drought"],
            ["Cup character", "Sweeter, aromatic, brighter acidity", "Heavy body, cocoa-woody, bitter, "
             "thick crema"],
            ["Price signal (ICO, Apr 2025, US¢/lb)", "Colombian milds 394", "Robustas 246"]]
    s.append(tbl(["", "Arabica", "Robusta"], rows, [150, (W - 150) / 2, (W - 150) / 2], font_size=7.6))
    s.append(src("USDA FAS India Coffee Annual (May 2026); ICO Coffee Market Report (Apr 2025); "
                 "composition ranges from coffee chemistry literature."))
    s.append(h2("2.3 Varieties: the cultivars behind the names"))
    s.append(p("Within each species there are many varieties (strictly, \"cultivars\"). They differ in "
               "plant height, yield, disease resistance and, above all, cup quality. Most of India's "
               "arabica comes from local selections bred for resistance to leaf rust, the fungus that "
               "wiped out coffee in Ceylon (Sri Lanka) in the 1870s and pushed many Indian planters "
               "towards robusta and tea."))
    rows = [["Typica, Bourbon", "Global heirlooms", "Tall, low-yield; sweet, complex cup; rust-susceptible"],
            ["Kent's", "India, 1920s", "Selected on Kent's estate (Doddengooda); early rust tolerance"],
            ["S.795 (Sln 795)", "India, 1940s", "Kent's x S.288; India's most planted arabica; balanced, "
             "mild acidity, chocolate and spice"],
            ["Sln 9, Sln 5", "India (CCRI)", "Rust-tolerant selections involving Hibrido de Timor; good cup"],
            ["Chandragiri", "India (CCRI)", "Semi-dwarf, bold beans, rust-tolerant, high-yielding"],
            ["Cauvery (Catimor)", "India", "Caturra x Hibrido de Timor; dwarf, very high yield; plainer cup"],
            ["SL28 / SL34", "Kenya", "Blackcurrant, vivid acidity; drought-tolerant"],
            ["Gesha (Geisha)", "Ethiopia via Panama", "Jasmine, bergamot, tea; record auction prices"],
            ["S.274 (Sln 274)", "India (robusta)", "Most popular Indian robusta; vigorous, bold beans"],
            ["CxR", "India (robusta)", "C. congensis x robusta; compact bush, smoother cup"]]
    s.append(tbl(["Variety", "Origin", "Why it matters"], rows, [92, 92, W - 184], font_size=7.6))
    s.append(src("Central Coffee Research Institute releases; TNAU Agritech portal; Counter Culture "
                 "Coffee, India's arabica varieties."))
    s.append(h2("2.4 Terroir: why place shows up in the cup"))
    s.append(side([p("<b>Terroir</b> is the sum of place: altitude, latitude, soil, rainfall, sunshine "
                     "and shade. The single biggest lever is <b>temperature</b>, and altitude is mostly "
                     "a proxy for it: the air cools by roughly 0.6°C for every 100 m of height. In "
                     "cooler air the cherry ripens slowly, the seed packs in more sugars and acids, "
                     "and the bean grows denser. Dense, slow-grown beans give brighter acidity and "
                     "more complex aromas, and they stand up to lighter roasts."),
                   p("Closer to the equator, coffee must grow higher to find the same coolness, so "
                     "1,200 m in Coorg (12°N) is roughly equivalent to 1,600-1,800 m in Colombia. Soils "
                     "matter too: coffee likes deep, well-drained, slightly acidic (pH 4.5-6.5), "
                     "humus-rich forest soils. <b>Shade</b> slows ripening, protects soil and "
                     "biodiversity, and is one reason Indian coffees are mellow and low in "
                     "harshness.")],
                  [il.CanvasFigure(W * 0.46, 170, il.mountain)], lw=0.53))
    s.append(figc(il.CanvasFigure(W, 150, il.lat_alt_chart),
                  "Figure 2.3. Latitude and altitude together set temperature: Indian estates at 11-14°N "
                  "reach specialty-grade coolness at lower altitudes than equatorial origins."))
    s.append(h2("2.5 India's growing regions"))
    rows = [["Chikmagalur & Bababudangiri", "Karnataka", "1,000-1,500 m", "Arabica, robusta",
             "Birthplace of Indian coffee; GI Chikmagalur & Bababudangiri arabica; chocolate, spice"],
            ["Coorg (Kodagu)", "Karnataka", "800-1,100 m", "Mostly robusta",
             "Largest district; GI Coorg arabica; robusta for espresso blends"],
            ["Biligiris (BR Hills)", "Karnataka", "1,000-1,500 m", "Arabica", "Source of Mysore Nuggets EB"],
            ["Wayanad", "Kerala", "700-1,200 m", "Robusta", "GI Wayanad robusta; smallholder belt"],
            ["Travancore, Nelliampathy", "Kerala", "500-1,600 m", "Both", "Mixed estates with spices"],
            ["Pulneys", "Tamil Nadu", "1,000-2,000 m", "Arabica", "India's highest coffee; bright, fruity"],
            ["Nilgiris, Shevaroys, Anamalais", "Tamil Nadu", "900-1,800 m", "Mostly arabica",
             "Shevaroys (Yercaud) mild and sweet"],
            ["Araku Valley", "Andhra Pradesh", "900-1,100 m", "Arabica",
             "Tribal, organic-leaning smallholders; GI; award-winning"],
            ["Koraput & North-East", "Odisha, NE states", "600-1,200 m", "Arabica",
             "Non-traditional areas; small but growing (Koraput award at KYK 2024)"]]
    s.append(tbl(["Region", "State", "Altitude", "Species", "Notes"], rows,
                 [118, 64, 60, 62, W - 304], font_size=7.4))
    s.append(p("Karnataka produces about 70% of India's coffee (2.80 lakh tonnes in 2025-26), Kerala "
               "about a fifth and Tamil Nadu about 5-6%; together they make up 96%. The Coffee Board "
               "recognises 13 agro-climatic zones. Six names carry Geographical Indication (GI) tags: "
               "Coorg Arabica, Wayanad Robusta, Chikmagalur Arabica, Araku Valley Arabica, "
               "Bababudangiris Arabica and Monsooned Malabar (arabica and robusta)."))
    s.append(src("PIB (Nov 2025); Coffee Board post-blossom estimate 2025-26; Coffee Board GI list."))
    s.append(h2("2.6 Before the estate: research, seed and the nursery"))
    s.append(p("The chain starts in a research station. India's <b>Central Coffee Research Institute</b> "
               "(CCRI), founded in 1925 at Balehonnur in Chikmagalur and backed by regional stations, "
               "breeds and releases varieties and supplies certified seed. Growers can also select "
               "seed from their own healthiest, highest-yielding plants."))
    nursery = [("Seed", "Fully ripe cherries from mother plants; pulped, washed, shade-dried; viable "
                "only a few months"),
               ("Germination bed", "Raised sand beds under shade; seedlings at the 'button' stage in "
                "~45-60 days"),
               ("Polybag nursery", "Transplanted to soil-filled polybags; 6-8 months (or 12-18 "
                "months as bare-root stumps)"),
               ("Field planting", "At monsoon onset; pits ~45 cm cube; arabica ~1,600-4,400 plants/ha "
                "by size, robusta ~1,100/ha"),
               ("Young plant", "Temporary shade, mulching, weeding; first light crop in year 3"),
               ("Bearing bush", "Full yield in 5-7 years; productive 30-50 years with rejuvenation "
                "pruning")]
    s.append(figc(DC.flow(nursery, W, 92, per_row=6, colors_=[LEAF] * 6, sub_size=5.9, head_size=6.9),
                  "Figure 2.4. From seed to bearing bush takes three to five years, which is why "
                  "replanting decisions are slow and costly."))
    s.append(h2("2.7 The farming year in India"))
    rows = [("Blossom showers & flowering", [(1, 4)], HX("#E8A0BF"), "flowering"),
            ("Backing showers (fruit set)", [(3, 5)], HX("#8FBCD4"), "fruit set"),
            ("Berry development", [(3, 11)], HX("#8DB86A"), "cherries growing"),
            ("South-west monsoon", [(5, 9)], HX("#5B8DB8"), "heavy rain"),
            ("Weeding & fertiliser", [(1, 3), (5, 6), (8, 10)], GOLD, ""),
            ("Pruning & shade lopping", [(1, 4)], HX("#A98467"), "after harvest"),
            ("White-stem-borer tracing", [(3, 5), (9, 11)], BERRY, ""),
            ("Arabica harvest", [(10, 12), (0, 1)], R.BERRY, "Nov-Jan"),
            ("Robusta harvest", [(11, 12), (0, 3)], HX("#8E3B46"), "Dec-Feb"),
            ("Pulping, drying & curing", [(10, 12), (0, 4)], SAFFRON, ""),
            ("Coffee Board crop estimates", [(4, 6), (9, 11), (2, 4)], PLUM, "")]
    s.append(figc(DC.gantt(rows, W, 172, lab_w=140),
                  "Figure 2.5. The Indian coffee calendar. A good blossom shower in February-March, "
                  "followed by a 'backing' shower two to three weeks later, sets the size of the "
                  "whole crop."))
    s.append(p("The year turns on rain. After the dry winter, a soaking <b>blossom shower</b> (or "
               "sprinkler irrigation that imitates it) triggers simultaneous flowering across an "
               "estate; a <b>backing shower</b> a few weeks later helps the fruit set. A failed "
               "blossom shower, or unseasonal rain that knocks flowers off, can cut a crop by a "
               "fifth. The south-west monsoon (June-September) brings most of the year's rain; too "
               "much of it causes black rot and berry drop, as in 2025. The Coffee Board publishes "
               "three crop estimates a season: post-blossom (May-June), post-monsoon (October-"
               "November) and final (March-April)."))
    s.append(h2("2.8 Estate economics and risks"))
    s.append(p("Indian yields are modest by world standards: about 450-475 kg of clean coffee per "
               "hectare for arabica and 1,150-1,250 kg for robusta. Coffee is labour-intensive: "
               "<b>about 70% of the cost of production is labour</b>, most of it at harvest, and "
               "estates increasingly rely on migrant workers. Farm-gate prices are volatile: after "
               "two very profitable years, arabica farm-gate prices fell 16% and robusta 11% between "
               "October 2025 and May 2026 as the world crop recovered."))
    rows = [["White stem borer", "Beetle larvae tunnel through arabica stems",
             "The main arabica pest in India; managed by shade, tracing and uprooting infested plants"],
            ["Coffee berry borer", "Tiny beetle bores into the berry",
             "Damaged beans taste dirty; traps, field sanitation, clean picking"],
            ["Leaf rust", "Fungus (Hemileia vastatrix) strips leaves",
             "Reason for India's rust-tolerant selections; fungicide sprays"],
            ["Black rot, berry drop", "Fungal rot in prolonged monsoon rain", "Hit 2025-26 crop estimates"],
            ["Climate change", "Hotter, more erratic rainfall",
             "Studies warn that up to half of today's arabica land may become unsuitable by 2050"]]
    s.append(tbl(["Risk", "What it is", "Impact and response"], rows, [90, 160, W - 250], font_size=7.6))
    s.append(src("USDA FAS India Coffee Annual (May 2026); CCRI; Deccan Herald and StoneX reports on the "
                 "2025-26 crop."))
    s += M.ch2()
    s += M2.origins()
    s += M4.atlas()
    s += M7.region_map()
    s += M7.farm_management()
    return s


# =============================================================================== 3. harvest
def ch3():
    s = chapter("c3", 3, "Harvesting", "Ripeness, picking methods, the yield arithmetic and what "
                "happens on picking day", R.BERRY)
    s.append(lead("Quality is mostly made or lost on picking day. A cup can only be as good as the "
                  "ripest, cleanest cherries that went into it."))
    s.append(h2("3.1 Why ripeness matters"))
    s.append(p("A coffee cherry is a fruit, and like any fruit it is sweetest when fully ripe. As it "
               "ripens from green to deep red, starches turn into sugars (ripe cherries typically "
               "measure 18-24° Brix, similar to grapes), acids mellow, and the seed finishes "
               "developing. Unripe cherries give grassy, astringent, \"peanutty\" coffee and pale "
               "beans that refuse to roast evenly (roasters call them <i>quakers</i>). Overripe or "
               "dried-on-the-bush cherries start to ferment and add winey, boozy or mouldy notes."))
    s.append(figc(il.CanvasFigure(W, 112, il.ripeness_plate),
                  "Figure 3.1. Ripeness stages. Only the ripe red (or ripe yellow in yellow varieties) "
                  "cherries should go to the pulper."))
    s.append(h2("3.2 How coffee is picked"))
    rows = [["Selective hand-picking", "Pickers take only ripe cherries; 3-5 passes over the season",
             "45-55 kg of cherry a day on average (50-120 kg for skilled pickers)", "Highest; standard "
             "on Indian arabica estates"],
            ["Strip picking", "All cherries stripped off a branch onto sheets in one pass",
             "2-3 times faster than selective", "Mixed ripeness; needs sorting; common for robusta"],
            ["Mechanical", "Tractor-drawn machines shake the branches", "Very fast; low cost per kg",
             "Needs flat, open land (Brazil); not feasible on India's steep, shaded slopes"],
            ["Gleaning", "Fallen cherries collected from the ground", "Cleans the field", "Low; "
             "should be kept out of quality lots"]]
    s.append(tbl(["Method", "How it works", "Productivity", "Quality and where used"], rows,
                 [86, 150, 122, W - 358], font_size=7.6))
    s.append(src("Springer (2026) picker study; Barista Hustle; USDA FAS."))
    s.append(h2("3.3 The yield arithmetic"))
    s.append(side([p("It takes a surprising amount of fruit to make a cup. Roughly <b>5-6 kg of ripe "
                     "cherry</b> give 1 kg of green coffee; roasting then loses another 14-20% of the "
                     "weight. One picker's day of about 50 kg of cherry therefore becomes roughly 9 kg "
                     "of green coffee, about 7.5 kg roasted, which is enough for around 420 double "
                     "espressos."),
                   p("The arithmetic explains two things. First, why careful selective picking is "
                     "expensive: labour is paid per kilo of cherry, and every pass through the field "
                     "costs money. Second, why the grower's share of a café's cup price is small: the "
                     "coffee in an 18 g double shot costs the café ₹21-30, and the green coffee "
                     "inside it, which is what the grower and curer are paid for, is only ₹13-20 "
                     "of a ₹220 drink.")],
                  [il.CanvasFigure(W * 0.48, 120, il.yield_funnel)], lw=0.5))
    s.append(h2("3.4 On picking day"))
    s.append(p("Good estates process cherries the same day, ideally within 6-12 hours, before they "
               "start to ferment in the sacks. On arrival cherries are tipped into a water tank: ripe, "
               "dense cherries sink, while <b>floaters</b> (unripe, insect-damaged or dried cherries) "
               "rise and are skimmed off and sold as a lower grade. Many estates also hand-sort on "
               "tables or sheets. Pickers are paid by weight, so the weighing shed doubles as the "
               "estate's quality checkpoint."))
    s.append(note("What this means for a café buyer", [
        "Ask roasters and estates about <b>picking and sorting</b>: selective picking and floating are "
        "the cheapest insurance against defects in the cup.",
        "Robusta is often strip-picked. Washed, selectively picked robusta (sold as \"fine robusta\" "
        "or Kaapi Royale) is a different, much cleaner product, and is worth paying for in an "
        "espresso blend."], TEAL))
    s += M.ch3()
    s += M3.estate_day()
    return s


# =============================================================================== 4. processing
def ch4():
    s = chapter("c4", 4, "Processing", "Turning a juicy cherry into a dry, stable green bean: "
                "washed, natural, honey, monsooned and the new experimental methods", SAFFRON)
    s.append(h2("4.1 What processing has to do"))
    s.append(p("A fresh cherry is 55-60% water and spoils within a day. Processing removes the fruit "
               "layers around the seed and dries the seed to about <b>10-12% moisture</b>, at which "
               "point it can be stored and shipped for a year. How the fruit is removed, and how "
               "long the seed sits in contact with sugary fruit and microbes while drying, shapes the "
               "flavour as much as variety or altitude."))
    s.append(side([il.CanvasFigure(W * 0.5, 165, il.cherry_cross_section)],
                  [il.CanvasFigure(W * 0.46, 165, il.process_layers)], lw=0.52))
    s.append(P_CAP("Figure 4.1. The cherry's layers (left) and what each process removes when (right): "
                   "skin and pulp, the sticky mucilage, the papery parchment and the silver skin."))
    s.append(h2("4.2 The washed (wet) process, step by step"))
    steps = [("Receive & float", "Cherries tipped into a siphon tank; floaters removed"),
             ("Pulp", "Disc or drum pulper squeezes beans out of skin and pulp, the same day"),
             ("Ferment", "Beans with sticky mucilage sit in tanks 12-48 h while microbes digest it"),
             ("Wash & grade", "Washed in channels; dense beans sink and are kept as the top grade"),
             ("Dry parchment", "On patios or raised beds 7-15 days (or dryers) to 10.5-12% moisture"),
             ("Rest & store", "Parchment rests 30-60 days to even out moisture, then goes to curing")]
    s.append(figc(DC.flow(steps, W, 76, per_row=6, colors_=[TEAL] * 6, sub_size=5.9, head_size=6.9),
                  "Figure 4.2. Washed processing. In India, washed arabica is sold as 'Plantation' and "
                  "washed robusta as 'Parchment'."))
    s.append(p("<b>Fermentation</b> is the delicate step. Natural yeasts and bacteria break down the "
               "mucilage (a pectin-rich layer) so it can be washed off; workers rub a handful of beans "
               "and stop when they feel gritty rather than slippery. Too short and mucilage remains; "
               "too long and the coffee turns sour, vinegary or onion-like. Some mills skip "
               "fermentation altogether and scrub the mucilage off mechanically (\"demucilaged\" or "
               "semi-washed). Washed coffees taste <b>clean, bright and transparent</b>: you taste "
               "the variety and the place rather than the process. Washing needs water and creates "
               "effluent, which modern eco-pulpers and recirculation reduce."))
    s.append(h2("4.3 Natural (dry) process"))
    s.append(p("The oldest method: whole cherries are dried with the fruit on. They are spread 3-4 cm "
               "deep on patios or raised beds, raked several times a day so they dry evenly, and "
               "covered at night and in rain. In bright Indian winter sun this takes 12-15 days; in "
               "humid places three to four weeks. The dried husk is removed later at the curing works. "
               "Because the seed dries inside the sugary fruit, naturals taste <b>fruity, sweet and "
               "heavy-bodied</b>, sometimes winey, with less clarity. The risk is mould or over-"
               "fermentation if drying stalls. Most Indian robusta, and arabica sold as 'Cherry', is "
               "natural."))
    s.append(figc(il.CanvasFigure(W, 128, il.pipelines),
                  "Figure 4.3. Washed, honey and natural processing side by side."))
    s.append(h2("4.4 Honey, semi-washed and wet-hulled"))
    s.append(p("<b>Honey</b> (or pulped natural) coffee is pulped like a washed coffee but dried with some "
               "or all of the sticky mucilage left on. Yellow, red and black honey indicate "
               "increasing amounts of mucilage and slower drying; the cup sits between washed and "
               "natural, sweet with a rounded body. <b>Wet-hulled</b> coffee (Indonesia's <i>giling "
               "basah</i>) is hulled while still at 30-35% moisture, which gives bluish beans and an "
               "earthy, heavy, low-acid cup."))
    s.append(h2("4.5 Monsooned Malabar: India's own process"))
    s.append(side([p("In the age of sail, Indian coffee spent up to six months in damp ships' holds "
                     "on the way to Europe and arrived swollen, pale and mellow. When the Suez Canal "
                     "(1869) and steamships shortened the voyage, European buyers missed that taste, "
                     "so Indian exporters recreated it on land."),
                   p("Today naturally processed coffee is spread in open-sided warehouses on the "
                     "Malabar coast (around Mangalore and Tellicherry) during the south-west monsoon. "
                     "For <b>12-16 weeks</b> (June-September) the beans absorb moist sea air, are "
                     "regularly raked and re-bagged, and swell to nearly twice their size, turning "
                     "pale gold. The result has almost no acidity, a syrupy body and earthy, spicy, "
                     "woody notes. It carries a GI tag and is prized in espresso blends.")],
                  [il.CanvasFigure(W * 0.40, 120,
                                   lambda c, w, h: _monsoon_beans(c, w, h))], lw=0.6))
    s.append(h2("4.6 Experimental processes"))
    rows = [["Anaerobic fermentation", "Cherries or pulped beans sealed in tanks without oxygen; "
             "temperature and time controlled", "Intense fruit, cinnamon, tropical, sometimes boozy"],
            ["Carbonic maceration", "Whole cherries in CO2-flushed tanks, a method borrowed from "
             "Beaujolais wine", "Red fruit, bubble-gum, wine-like"],
            ["Yeast / culture inoculation", "Selected wine or brewing yeasts or lactic bacteria added",
             "More control and repeatability"],
            ["Thermal shock, co-ferments", "Hot and cold water treatments; fermenting with fruit, "
             "spices or hops", "Very loud flavours; co-ferments are controversial because flavour is "
             "added, not grown"]]
    s.append(tbl(["Process", "What happens", "Typical flavour"], rows, [110, 220, W - 330], font_size=7.6))
    s.append(p("These methods command large premiums in competitions and specialty cafés. Several Indian "
               "estates now sell anaerobic and carbonic lots, but they suit pour-over menus and retail "
               "shelves more than a café's everyday espresso."))
    s.append(h2("4.7 Drying, storage and moisture"))
    rows = [["Patio (concrete or brick)", "Cheap, large volumes", "Slow and uneven if not raked; dust"],
            ["Raised beds (African beds)", "Air flows underneath; even, clean drying", "Labour; more "
             "space per kg"],
            ["Polytunnels / solar dryers", "Protect against rain; useful in monsoon regions",
             "Can overheat if not ventilated"],
            ["Mechanical dryers", "Rotating drums at 40-45°C; weather-proof", "Fuel cost; can 'bake' the "
             "coffee if too hot"]]
    s.append(tbl(["Method", "Strength", "Watch-out"], rows, [120, 170, W - 290], font_size=7.6))
    s.append(p("Target moisture under Coffee Board standards is <b>10.5%</b> for Plantation and Robusta "
               "Parchment and <b>11.5%</b> for Cherry grades. Too wet (above about 12.5%) and the coffee "
               "grows mould; too dry and it tastes papery and roasts unevenly. Green coffee is stored in "
               "jute or in hermetic liners (such as GrainPro) and keeps well for 6-12 months; older "
               "\"past crop\" coffee tastes woody and flat."))
    s.append(h2("4.8 Process and flavour"))
    s.append(side([R.process_map(W * 0.56, 150)],
                  [p("The map summarises the trade-off: washed coffees win on clarity, naturals and "
                     "honeys on fruit and sweetness, and experimental processes push fruit and "
                     "fermentation to the extreme. Monsooned and wet-hulled coffees trade acidity for "
                     "body and earthiness."),
                   p("<b>For a café menu</b>, a washed Indian arabica with a share of washed robusta gives "
                     "a clean, chocolatey espresso that works with milk; a natural or anaerobic "
                     "micro-lot is best kept for pour-over and retail.")], lw=0.58))
    s += M.ch4()
    s += M5.processing_equipment()
    s += M7.processing_risks()
    return s


def P_CAP(t):
    from build_report import CAPTION, P
    return P(t, CAPTION)


def _monsoon_beans(c, w, h):
    items = [("green_natural", "Before: dry-processed", "green-yellow, firm"),
             ("monsooned", "After 12-16 weeks", "swollen, pale gold")]
    cw = w / 2
    for i, (kd, a, b) in enumerate(items):
        cx = cw * i + cw / 2
        iw = cw - 12
        il.draw_pil(c, il.render_bean(kd, 300, seed=i + 7), cx - iw / 2, h - iw * 0.78 - 4, iw)
        il.text(c, cx, h - iw * 0.78 - 13, a, 7.2, "Body-Bold", il.INK, "middle")
        il.text(c, cx, h - iw * 0.78 - 22, b, 6.5, "Body", il.MUTED, "middle")


# =============================================================================== 5. grading & quality
def ch5():
    s = chapter("c5", 5, "Milling, grading and quality", "Curing works, India's grade names, defects "
                "and how professionals score coffee", PLUM)
    s.append(h2("5.1 The curing works"))
    s.append(p("In India, dry mills are called <b>curing works</b>; there are clusters around "
               "Chikmagalur, Hassan, Kushalnagar, Mangalore and Coimbatore. They turn parchment or "
               "dried cherry into export-ready green coffee and grade it. The <b>outturn</b> (the "
               "share of clean coffee that comes out) is roughly 80% for parchment and about 50% for "
               "dried cherry."))
    steps = [("Pre-clean", "Remove stones, sticks and metal (sieves, magnets)"),
             ("Hull", "Strip off parchment or the dried husk"),
             ("Polish", "Optional: rub off silver skin for a cleaner look"),
             ("Size-grade", "Shake over round-hole screens 13-19"),
             ("Density-grade", "Gravity tables separate light, hollow beans"),
             ("Colour-sort", "Optical sorters reject blacks, sours, discoloured beans"),
             ("Hand-pick", "'Garbling' by hand on belts or tables"),
             ("Bag & mark", "Jute bags (usually 60 kg), lot marks, samples")]
    s.append(figc(DC.flow(steps, W, 90, per_row=8, colors_=[PLUM] * 8, sub_size=5.8, head_size=6.6),
                  "Figure 5.1. Inside a curing works."))
    s.append(h2("5.2 India's grade names, decoded"))
    s.append(p("Indian grades combine a <b>processing name</b> with a <b>size letter</b>. Washed arabica "
               "is <b>Plantation</b>, washed robusta is <b>Parchment</b>, and naturals of either species "
               "are <b>Cherry</b>. The letters describe bean size, measured by the round-hole screen "
               "the beans sit on, plus limits on defects (\"clean garbled\" means hand-picked clean)."))
    s.append(side([DF.sieve_sizes(W * 0.42, 150)],
                  [tbl(["Grade", "Sieve requirement"],
                       [["Plantation AA", "≥90% on screen 18 (7.10 mm)"],
                        ["Plantation A", "≥90% on screen 17 (6.65 mm); ≤1.5% through 15"],
                        ["Plantation B", "≥75% on screen 15 (6.00 mm)"],
                        ["Plantation C", "≥75% on screen 14 (5.50 mm); 100% on 13"],
                        ["Plantation PB", "Peaberry; no sieve rule; ≤2% flats"],
                        ["Arabica Cherry AB", "≥90% on screen 15"],
                        ["Robusta Parchment AB", "≥90% on screen 15; the base of Kaapi Royale"],
                        ["Robusta Cherry AB", "≥90% on screen 15; India's commonest robusta"],
                        ["Mysore Nuggets EB", "Plantation A from Mysore, Biligiris, Shevaroys; ≥90% on "
                         "screen 19 (7.5 mm)"],
                        ["Robusta Kaapi Royale", "≥90% on screen 17; whole, defect-free washed robusta"],
                        ["Monsooned Malabar AA", "Monsooned arabica, screen 18+"]],
                       [96, W * 0.56 - 106], font_size=7.2)], lw=0.43))
    s.append(src("Coffee Board of India quality specifications ('Coffee Karma'); Josuma Coffee; "
                 "trade grade guides."))
    s.append(p("Size is not flavour. A Plantation AA from a low, hot farm can taste plainer than a "
               "Plantation B from a cool, high one. But even size matters to a roaster, because small "
               "and large beans roast at different speeds. A lot with one screen size roasts evenly."))
    s.append(figc(il.CanvasFigure(W, 104, il.beans_before),
                  "Figure 5.2. Green coffee as it leaves the curing works: washed and natural arabica, robusta, "
                  "peaberry and monsooned beans look clearly different."))
    s.append(h2("5.3 Defects: what they are and what they taste like"))
    s.append(p("The Specialty Coffee Association (SCA) grades green coffee by counting defects in a "
               "350 g sample. A <b>specialty grade</b> lot may have <b>no primary defects and at most "
               "five full defects</b> in total; premium grade allows up to eight."))
    rows = [["Full black", "1", "Dead or over-fermented cherries", "Sour, phenolic, dirty"],
            ["Full sour", "1", "Over-fermentation, slow drying", "Vinegar, onion, rotten fruit"],
            ["Dried cherry / pod", "1", "Poor hulling", "Fermented, mouldy"],
            ["Fungus damage", "1", "Mould in drying or storage", "Musty, earthy, risk of toxins"],
            ["Severe insect damage", "5", "Berry borer holes", "Dirty, rioy, sour"],
            ["Partial black / sour", "3", "As above, milder", "Muddy or sour notes"],
            ["Immature / unripe", "5", "Unripe cherries picked", "Grassy, astringent; pale 'quakers'"],
            ["Broken, chipped, cut", "5", "Pulper or huller damage", "Uneven roast, scorching"],
            ["Floater, shell, parchment", "5", "Light, deformed or unhulled beans", "Stale, uneven"]]
    s.append(tbl(["Defect", "Beans = 1 defect", "Cause", "Taste in the cup"], rows,
                 [100, 66, 150, W - 316], font_size=7.6, center_cols=(1,)))
    s.append(src("SCA Green Coffee Grading Handbook (defect equivalents)."))
    s.append(h2("5.4 Cupping: how coffee is scored"))
    s.append(side([p("Professionals judge coffee by <b>cupping</b>, a standardised tasting. The SCA "
                     "protocol uses 8.25 g of lightly roasted coffee per 150 ml of water (1:18), "
                     "ground just before tasting, steeped at 93°C for about four minutes. The taster "
                     "breaks the crust of grounds, smells the released aroma, skims, and then slurps "
                     "from a spoon as the coffee cools, because flavours change with temperature."),
                   p("Each coffee is scored on fragrance and aroma, flavour, aftertaste, acidity, "
                     "body, balance, uniformity, clean cup, sweetness and overall impression, for a "
                     "total out of 100. <b>80+ points is 'specialty'</b>, 85+ excellent and 90+ "
                     "outstanding. In 2023-24 the SCA introduced the Coffee Value Assessment, which "
                     "separates descriptive notes from preference scores. In India the Coffee Board "
                     "runs the <b>Flavour of India: Fine Cup Award</b> (since 2002) and Know Your Kaapi "
                     "competitions.")],
                  [R.sca_ladder()], lw=0.55))
    s.append(note("Quality control checklist for a café", [
        "On arrival: check roast date, bag integrity, aroma; keep a sample.",
        "Cup every new lot and every roast batch, ideally blind against last week's coffee.",
        "Track three numbers per blend: roast date to use (target 7-30 days), shot recipe (dose, "
        "yield, time) and customer complaints. Drift in any of them is an early warning."], PLUM,
        bg=HX("#F3EEF8")))
    s += M.ch5()
    s += M6.spec_sheet()
    return s


# =============================================================================== 6. trade & prices
def ch6():
    s = chapter("c6", 6, "Trade, prices and the money", "How Indian coffee is sold, how world prices "
                "are set, and who earns what from farm to cup", SKY)
    s.append(h2("6.1 How Indian coffee changes hands"))
    hist = [("1600s", "Baba Budan brings seven seeds from Yemen to the Chandragiri hills"),
            ("1800s", "British estates in Coorg, Chikmagalur, Wayanad; rust hits in the 1870s"),
            ("1925", "Coffee research station at Balehonnur (today's CCRI)"),
            ("1942", "Coffee Act: Coffee Board pools all coffee; ~70% exported"),
            ("1992-2001", "Free-sale quota rises from 30% to 100%; pooling ends"),
            ("Today", "Free market; Board advises, promotes, publishes prices")]
    s.append(figc(DC.flow(hist, W, 74, per_row=6, numbered=False, colors_=[SKY] * 6, sub_size=5.9,
                          head_size=7.0),
                  "Figure 6.1. From a state monopoly to a free market."))
    s.append(p("For half a century every grower had to deliver coffee to the Coffee Board's pool, "
               "which sold about 70% abroad and auctioned the rest at home; growers received a pooled "
               "price months later. Liberalisation in the 1990s let growers sell freely, and pooling "
               "ended in 1996. Today the conventional chain runs <b>grower to village consolidator to "
               "trader to huller or curing works to exporter or roaster to retailer</b>. Larger estates "
               "sell directly to exporters, and a growing number sell micro-lots straight to Indian "
               "specialty roasters, who publicise the estate name."))
    s.append(h2("6.2 How the world price is set"))
    s.append(p("Physical coffee is priced off two futures markets. <b>Arabica</b> trades on ICE's "
               "Coffee \"C\" contract in New York: one contract is 37,500 lb (about 17 tonnes or 283 "
               "bags), quoted in US cents per pound, and each 0.05¢ tick is worth $18.75. "
               "<b>Robusta</b> trades in London in 10-tonne lots priced in US dollars per tonne. A "
               "physical lot is priced as <b>futures plus or minus a 'differential'</b> that reflects "
               "origin, quality and timing. India's coffee is deliverable on the C contract at a "
               "discount, and Indian exporters hedge with futures. At home, prices track world prices "
               "converted at the rupee rate, which is why a weak rupee (about ₹96 per dollar in "
               "October 2026) props up Indian farm-gate prices."))
    s.append(note("Worked example: from New York to Chikmagalur", [
        "ICE C price, 9 Oct 2026: about 285 US¢/lb = US$6.28 per kg = <b>₹603 per kg</b> at ₹96/US$.",
        "Indian arabica parchment, 6 Oct 2026: ₹24,100-24,800 per 50 kg = ₹482-496 per kg of "
        "parchment. At an 80% outturn this is <b>₹600-620 per kg of clean coffee</b>, almost exactly "
        "the New York price.",
        "That is why Part 2 assumes ₹600/kg for commodity (Plantation A) arabica and ₹950/kg for "
        "estate specialty lots that earn a quality premium."], SKY, bg=HX("#EAF3F8")))
    months = ["Mar-19", "Feb-23", "Jun-23", "Jul-24", "Dec-24", "Jan-25", "Apr-25", "May-25", "Jun-25",
              "Jul-25", "Aug-25", "Sep-25", "Oct-25", "Nov-25", "Dec-25"]
    vals = [97.5, 174.8, 174.1, 236.5, 299.6, 304.2, 335.8, 334.4, 295.1, 259.3, 297.1, 324.6, 326.4,
            330.4, 304.7]
    s.append(figc(DC.line_chart(months, [("ICO composite indicator", vals, ROAST)], W, 150,
                                title="Coffee prices tripled in six years (ICO composite, monthly "
                                      "average, US cents per lb)",
                                annotations=[(0, 97.5, "lowest since 2006"),
                                             (6, 335.8, "ICE C hit a record >420¢ in Feb 2025")],
                                ylo=50, yhi=400, label_every=1),
                  "Figure 6.2. Selected monthly averages. Drought in Brazil and Vietnam, four years of "
                  "falling stocks and a strong dollar pushed prices to records in 2025; a larger "
                  "2026 crop has since pulled ICE arabica back to about 285¢ (Oct 2026)."))
    s.append(src("ICO Indicator Prices monthly sheets (2019-2025); ICE; Trading Economics."))
    s.append(h2("6.3 From farm to cup: where the money goes"))
    steps = [("Green coffee (estate specialty)", 1103, "total"),
             ("Toll roasting & freight", 205, "delta"),
             ("Roaster brand & margin", 357, "delta"),
             ("Wholesale price", 1665, "total"),
             ("Retail markup", 735, "delta"),
             ("Retail bag (₹600/250 g)", 2400, "total")]
    s.append(figc(DC.waterfall(steps, W * 0.55, 160,
                               title="₹ per kg of roasted specialty coffee",
                               sub="Green cost is per kg roasted (after 16% roast loss)"),
                  "Figure 6.3. Price build-up for a Specialty-mix coffee (Part 2 sourcing assumptions)."))
    s.append(p("The waterfall shows a familiar pattern: the grower's green coffee is less than half of "
               "the retail shelf price. In a café the multiplier is far larger. One kilogram of "
               "roasted coffee makes about 55 double shots, and at an average ₹220 per drink that is "
               "<b>about ₹12,000 of beverage sales per kg</b>. The coffee in an 18 g double shot costs "
               "₹21-27; the grower's share of a ₹220 cappuccino is roughly <b>₹13-20, or 6-9%</b>. "
               "Most of the café's price pays for labour, rent, milk and service, as the Part 2 model "
               "shows."))
    shares = [("Grower", 43.0), ("Retailers", 18.6), ("Roasters", 14.6), ("Curers / MNCs", 13.9),
              ("Hullers", 6.3), ("Agents", 2.0), ("Village consolidator", 1.1)]
    s.append(side([DC.hbar_chart([a for a, _ in shares], [b for _, b in shares], W * 0.5, 138,
                                 title="Who keeps the margin? Indian robusta chain (% of total margin)",
                                 colors_=[LEAF, PLUM, ROAST, SKY, SAFFRON, GOLD, CARAMEL], fmt="{:.1f}%",
                                 label_w=88)],
                  [p("A study of India's conventional robusta chain found the grower keeping about "
                     "43% of the total margin, with roasters and retailers together taking a third. "
                     "Global studies put farmers' share of the final retail value of roasted coffee "
                     "at between 3% and 15%; for India one estimate is about 15.7%."),
                   p("Certification premiums are small (₹50-150 per 50 kg bag, or 2-3%). The bigger "
                     "gains come from quality and from selling direct: estate-branded Indian coffees "
                     "now fetch prices close to export levels at home.")], lw=0.52))
    s.append(src("AgEcon Search study of India's robusta value chain; Selina Wamucii; GCP, IDH and "
                 "Solidaridad, 'The Grounds for Sharing' (2024); USDA FAS (May 2026)."))
    s.append(h2("6.4 Logistics and trade rules"))
    rows = [["Bags & containers", "Green coffee ships in 60 kg jute bags; a 20-ft container holds "
             "275-320 bags (16.5-19.2 t)"],
            ["Ports", "About 61% of India's exports leave through Mangalore; 3-6 weeks to Europe"],
            ["What India exports", "6.22 million bags in 2026/27: 59% green beans, 41% instant coffee; "
             "Europe takes 44-45%"],
            ["Imports", "~1.39 million bags, mostly robusta for instant-coffee re-export; 100% duty on "
             "green/roasted coffee imported for the home market"],
            ["Trade deals", "India-UK CETA: duty-free roasted and instant coffee; India-EFTA TEPA (Oct "
             "2025): zero duty in Switzerland, Norway, Iceland"],
            ["EU deforestation rule", "Shipments to the EU must prove no deforestation after 31 Dec "
             "2020; the rule has been simplified and postponed"],
            ["Taxes at home", "GST on instant coffee cut from 18% to 5% in 2025, cutting retail prices "
             "by 11-12%"]]
    s.append(tbl(["Topic", "What to know"], rows, [100, W - 100], font_size=7.6))
    s.append(src("USDA FAS (May 2026); PIB (Nov 2025); EU EUDR updates (Dec 2025)."))
    s += M.ch6()
    s += M2.price_cycles()
    s += M7.direct_trade()
    return s
