"""Part 1, chapters 7-12: roasting, grinding, brewing science, methods, tasting, markets."""
from reportlab.platypus import KeepTogether, PageBreak

import brew_art as BA
import build_report as R
import deep_charts as DC
import deep_figs as DF
import deep_lastmile as LM
import deep_more as M
import deep_more2 as M2
import deep_more3 as M3
import deep_more4 as M4
import deep_more5 as M5
import deep_more6 as M6
import deep_more7 as M7
import illustrations as il
from deep_base import (BERRY, CARAMEL, CONTENT_W, PLUM, ROAST, SAFFRON, SKY, TEAL, HX,
                       Spacer, bl, chapter, figc, h2, h3, lead, method_card, note, p, side, src,
                       tbl)

W = CONTENT_W


# =============================================================================== 7. roasting
def ch7():
    s = chapter("c7", 7, "Roasting", "The chemistry in the drum, roast levels, machines, profiles, "
                "freshness and what roasting costs", ROAST)
    s.append(h2("7.1 What happens inside the roaster"))
    s.append(p("Roasting heats green beans to 180-240°C for roughly 8-15 minutes in a drum roaster. "
               "In that time the bean loses 12-20% of its weight (mostly water), nearly doubles in "
               "volume, turns from green to brown and develops the aromas we call coffee. Roasters "
               "describe four stages:"))
    s.append(bl(["<b>Drying (0-5 min).</b> Water evaporates; the bean turns yellow and smells of hay, "
                 "then bread, at around 150-160°C.",
                 "<b>Browning (Maillard) phase.</b> From about 150-160°C, sugars react with amino acids "
                 "(the Maillard reaction) to form brown melanoidins and hundreds of aroma compounds; "
                 "above about 170°C sucrose caramelises. Chlorogenic acids break down into bitter "
                 "compounds; trigonelline yields niacin and roasty aromas.",
                 "<b>First crack (~196-205°C).</b> Steam and CO2 pressure inside the cells fracture the "
                 "bean with an audible pop, like popcorn. Light roasts are dropped shortly after it.",
                 "<b>Development and second crack.</b> The time after first crack (typically 15-25% of "
                 "the roast, the 'development time ratio') sets sweetness and body. Near 224-230°C a "
                 "second, quieter crack begins, oils reach the surface and roasty, smoky, bitter "
                 "flavours take over: dark roast territory."]))
    s.append(figc(DF.roast_curve(W, 190),
                  "Figure 7.1. Roasters steer by a steadily falling rate of rise. A rate that spikes "
                  "scorches beans; one that crashes 'bakes' them flat."))
    s.append(h2("7.2 Roast levels and flavour"))
    s.append(R.roast_spectrum())
    s.append(Spacer(1, 4))
    rows = [["Light (cinnamon to city)", "Shortly after first crack, ~200-210°C", "Bright acidity, florals, "
             "fruit, tea-like; origin shows clearly", "Pour-over, AeroPress, cupping"],
            ["Medium (city+ to full city)", "~210-220°C", "Balanced: caramel, nuts, chocolate, gentle "
             "acidity", "Filter and espresso; crowd-pleasing"],
            ["Medium-dark (Vienna)", "Start of second crack, ~224-230°C", "Bittersweet chocolate, spice, "
             "heavier body, oil spots", "Espresso with milk, filter kaapi"],
            ["Dark (French, Italian)", "Into second crack, 235°C+", "Smoky, roasty, bitter, low acidity; "
             "origin hidden", "Traditional espresso, kaapi, instant"]]
    s.append(tbl(["Level", "Drop temperature", "Taste", "Best for"], rows, [98, 100, 180, W - 378],
                 font_size=7.6))
    s.append(figc(il.CanvasFigure(W, 112, il.beans_roast),
                  "Figure 7.2. The same bean from green to dark roast."))
    s.append(h2("7.3 Roasting machines"))
    s.append(figc(BA.figure(BA.draw_roaster, W, 168),
                  "Figure 7.3. A drum roaster and its main parts (schematic)."))
    s += ([p("<b>Drum roasters</b> (above) tumble beans in a rotating drum heated by gas or "
                     "electricity; heat arrives by conduction from the hot drum and convection from "
                     "hot air drawn through it. They range from 500 g shop roasters to 120 kg "
                     "production machines and dominate specialty roasting. India has local makers "
                     "such as Aaroasta in Rajkot (0.5-50 kg); imported brands include Probat, Giesen, "
                     "Diedrich and Loring."),
                   p("<b>Fluid-bed (hot-air) roasters</b> float the beans on a stream of hot air: "
                     "fast, even and bright-tasting, popular for sample roasting. Industrial plants use "
                     "continuous roasters for instant and supermarket coffee. In a city, an "
                     "<b>afterburner</b> or catalytic converter is needed to burn off smoke and smell.")])
    s.append(h2("7.4 Profiles, blends and consistency"))
    s.append(p("A <b>roast profile</b> is the recipe: charge temperature, when gas and airflow change, "
               "and when to drop. Software such as Artisan or Cropster logs bean temperature every "
               "second so a profile can be repeated batch after batch; colour meters (Agtron scale) "
               "and cupping check the result. Espresso roasts usually develop longer than filter "
               "roasts so they extract sweetly at high pressure. Blends may be roasted together "
               "(<i>pre-roast</i>) or separately and then mixed (<i>post-roast</i>), which lets each "
               "component reach its ideal level. Indian and Italian espresso blends often contain "
               "10-30% robusta for crema, body and lower cost."))
    s.append(h2("7.5 Resting, packing and freshness"))
    s.append(p("Freshly roasted coffee is full of carbon dioxide and must rest before brewing: about "
               "2-7 days for filter and 7-14 days for espresso, or the gas makes extraction uneven and "
               "flavours sharp. After that, aroma fades steadily as the coffee oxidises. Good roasters "
               "pack into <b>one-way valve bags</b> (the gas gets out, air does not), sometimes flushed "
               "with nitrogen. Whole beans are at their best roughly 7-30 days after roasting and "
               "noticeably flat after 4-6 weeks once the bag is opened. Ground coffee loses most of "
               "its aroma within an hour, which is why cafés grind to order."))
    s.append(R.freshness_timeline())
    s.append(h2("7.6 What roasting costs"))
    s.append(p("The economics hinge on the <b>roast loss</b> (14-20%; Part 2 uses 16%) and on how full "
               "the roaster is kept. A 3 kg drum roaster does three or four batches an hour, i.e. "
               "roughly 8-12 kg of roasted coffee per hour. A busy café uses about 1,100-1,600 kg a year "
               "including retail bags, which is only 100-200 hours of roasting. That is why most "
               "cafés buy roasted coffee or pay a roaster to <b>toll-roast</b> their own green beans; "
               "owning a roaster pays only when there is wholesale volume to fill it."))
    rows = [["Buy roasted", "Roaster's price, ₹1,650-1,850/kg for a specialty blend", "None", "Least "
             "control; roaster's brand on the bag unless private label"],
            ["Toll roasting", "Green cost ÷ 0.84 + ₹180 fee + ₹25 freight ≈ ₹1,300-1,500/kg",
             "Green stock (40 days)", "Your own green coffee, profile and label; minimum batch sizes"],
            ["In-house roastery", "Green ÷ 0.84 + ₹60 variable ≈ ₹1,160-1,340/kg, plus roaster salary, "
             "AMC, rent", "₹13 lakh roaster, afterburner, QC kit + fit-out", "Full control, theatre "
             "and a wholesale business; needs roughly 450-500 kg/month of wholesale to beat toll roasting"]]
    s.append(tbl(["Route", "Cost per kg (Specialty / House mix)", "Capital tied up", "Trade-off"], rows,
                 [70, 160, 100, W - 330], font_size=7.4))
    s.append(src("Part 2 model (Sourcing and Capex sheets); Aaroasta product range; roaster price lists."))
    s += M.ch7()
    s += M2.roast_profiles()
    s += M3.small_roastery()
    s += M6.agtron()
    return s


# =============================================================================== 8. grinding
def ch8():
    s = chapter("c8", 8, "Grinding", "Why particle size matters, burrs versus blades, the right grind "
                "for each method, and how to dial in", SAFFRON)
    s.append(h2("8.1 Why grinding matters"))
    s.append(p("Water can only dissolve what it can reach. A whole bean exposes very little surface, "
               "so grinding is what makes brewing possible: cut a 6 mm bean into 0.3 mm espresso "
               "particles and the surface area per gram rises about twentyfold. <b>Finer grinds "
               "extract faster and slow the water down</b>; coarser grinds extract slowly and let "
               "water run through. So grind size must match contact time: 25-30 seconds of espresso "
               "needs fine sand; four minutes in a French press needs coarse breadcrumbs."))
    s.append(p("Every grinder makes a <b>spread</b> of sizes. Tiny <b>fines</b> (under ~100 µm) "
               "over-extract and add bitterness and mud, and they can clog paper filters; big "
               "<b>boulders</b> under-extract and add sourness. A good grinder keeps the spread narrow, "
               "so the whole dose extracts at the same pace."))
    s.append(figc(DF.particle_dist(W, 150),
                  "Figure 8.1. Flat burrs give a tight, single peak; conical burrs a second 'fines' "
                  "peak (more body in espresso); blade grinders a smear of dust and chunks."))
    s.append(h2("8.2 Types of grinder"))
    s.append(figc(BA.figure(BA.draw_burrs, W, 132),
                  "Figure 8.2. Flat burrs, conical burrs and a blade grinder."))
    rows = [["Blade", "A spinning blade smashes beans; size depends on time", "Cheap (₹1,000-3,000)",
             "Very uneven; avoid for anything but spices"],
            ["Conical burr", "A cone turns inside a ring; grounds fall straight down",
             "Hand grinders ₹3,000-20,000; café ₹1-2 lakh", "Low heat and retention; bimodal grind adds "
             "body"],
            ["Flat burr", "Two parallel rings; beans travel outwards between them",
             "Café on-demand grinders ₹1.2-2.5 lakh+", "Very uniform; clarity; can retain coffee"],
            ["Roller", "Pairs of rollers crack beans in stages", "Industrial", "Most uniform; used for "
             "packaged ground coffee"]]
    s.append(tbl(["Type", "How it works", "Typical cost (India)", "Character"], rows,
                 [62, 172, 130, W - 364], font_size=7.6))
    s.append(p("Other details matter in a café: <b>burr size</b> (64-98 mm flat burrs grind fast and "
               "cool), motor speed and heat, <b>retention</b> (grounds left inside that go stale and "
               "mix into the next dose), stepless versus stepped adjustment, and <b>burr life</b>. "
               "Burrs dull after a few hundred kilograms to about a tonne, depending on their size, "
               "after which the grind gets dustier and shots run faster."))
    s.append(h2("8.3 The right grind for each method"))
    s.append(DF.grind_microns(W, 150))
    s.append(src("Honest Coffee Guide, Bean Box and The Coffee Locator grind charts (ranges vary by "
                 "grinder)."))
    s.append(h2("8.4 Dialling in: let taste steer the grinder"))
    s.append(side([p("'Dialling in' means adjusting the grind (and then dose and time) until the coffee "
                     "tastes right. The rules are simple:"),
                   *bl(["<b>Sour, salty, thin, quick</b> = under-extracted: grind <b>finer</b>.",
                        "<b>Bitter, dry, hollow, slow</b> = over-extracted: grind <b>coarser</b>.",
                        "Change one thing at a time, purge the grinder after each change, and taste.",
                        "Re-check every morning: humidity, bean age and burr temperature all shift the "
                        "grind."])],
                  [tbl(["Espresso: 18 g in, 36 g out", "Taste", "Action"],
                       [["Runs in 18 s", "Sour, thin", "Finer"],
                        ["Runs in 25-30 s", "Sweet, balanced", "Keep"],
                        ["Runs in 40 s", "Bitter, harsh", "Coarser"],
                        ["Channels or spurts", "Sour and bitter", "Fix distribution and tamping"]],
                       [W * 0.2, W * 0.13, W * 0.14], font_size=7.4)], lw=0.5))
    s.append(h2("8.5 A café grinding set-up"))
    s.append(bl(["Two on-demand espresso grinders: one for the house blend, one for a guest single "
                 "origin or decaf. Grinding by timer keeps doses consistent.",
                 "One bulk grinder for batch brew, pour-over and grinding retail bags for customers.",
                 "Daily: brush out the chute, purge stale grounds. Weekly: grinder-cleaning tablets. "
                 "Keep only a day's beans in the hopper; check burr alignment and wear every few months."]))
    s += M.ch8()
    s += M3.industrial_grinding()
    return s


# =============================================================================== 9. brewing science
def ch9():
    s = chapter("c9", 9, "The science of brewing", "Extraction and strength, the variables you control, "
                "water, why so many methods exist, and milk", TEAL)
    s.append(h2("9.1 Extraction: dissolving the right amount"))
    s.append(p("About 28-30% of a roasted bean's weight can dissolve in water, but a delicious cup takes "
               "only <b>18-22%</b> of it. Compounds dissolve in a predictable order: acids and salts first, "
               "then sugars and browning products, and bitter compounds last. Stop too early and the cup "
               "is sour and thin (<b>under-extracted</b>); go too far and it turns bitter and drying "
               "(<b>over-extracted</b>)."))
    s.append(DF.extraction_sequence(W, 104))
    s.append(p("Two numbers describe any cup. <b>Strength</b> is the concentration of dissolved coffee, "
               "measured as total dissolved solids (TDS) with a refractometer: about 1.15-1.35% for "
               "filter coffee and 8-12% for espresso. <b>Extraction yield</b> is the share of the dry "
               "coffee that ended up in the cup. Example: 30 g of coffee and 500 g of water give about "
               "450 g of brew; at 1.30% TDS it holds 5.85 g of coffee solids, an extraction of 19.5%. "
               "The SCA's 'Golden Cup' standard combines the two: 18-22% extraction at 1.15-1.35% TDS, "
               "with roughly 55 g of coffee per litre of water (1:18)."))
    s.append(figc(DC.control_chart(W, 210, points=[("V60 30 g : 500 g", 19.5, 1.30)]),
                  "Figure 9.1. Strength is mostly set by the ratio; extraction by grind, time and "
                  "temperature. The goal is the green box."))
    s.append(h2("9.2 The variables you control"))
    rows = [["Ratio (coffee : water)", "Strength", "1:15-1:17 filter; 1:2 espresso; 1:8 cold-brew "
             "concentrate", "Weigh, don't scoop"],
            ["Grind size", "Extraction speed, flow", "See Figure 8.3", "The main dial-in lever"],
            ["Contact time", "Extraction", "25-30 s espresso; 3-4 min pour-over; 12-24 h cold brew",
             "Linked to grind and method"],
            ["Water temperature", "Extraction speed", "90-96°C hot brews; cooler for dark roasts",
             "Hotter extracts more, faster"],
            ["Agitation", "Evenness, speed", "Stirring, swirling, pouring height", "More agitation = more "
             "extraction"],
            ["Filter medium", "Body versus clarity", "Paper (clean), metal (oily, full), cloth (in "
             "between)", "Paper removes oils and fines"],
            ["Freshness", "Aroma, evenness", "7-30 days from roast; grind just before", "Stale coffee "
             "tastes flat whatever you do"]]
    s.append(tbl(["Variable", "Mostly affects", "Typical setting", "Note"], rows, [96, 86, 190, W - 372],
                 font_size=7.6))
    s.append(h2("9.3 Water: 98% of the cup"))
    s.append(side([tbl(["Parameter (SCA)", "Target", "Acceptable"],
                       [["Total dissolved solids", "150 mg/L", "75-250"],
                        ["Total hardness (as CaCO3)", "68 mg/L", "50-175"],
                        ["Alkalinity (as CaCO3)", "40 mg/L", "40-75"],
                        ["pH", "7.0", "6.5-7.5"],
                        ["Sodium", "10 mg/L", "≤30"],
                        ["Chlorine", "0", "0"]],
                       [W * 0.24, W * 0.1, W * 0.1], font_size=7.4)],
                  [p("Minerals do real work: calcium and magnesium help pull flavour out of the coffee, "
                     "while bicarbonate (alkalinity) buffers acidity. Water that is too soft tastes flat "
                     "and sour; too hard tastes chalky and furs up boilers; high alkalinity mutes "
                     "acidity. Chlorine ruins aroma."),
                   p("Ahmedabad's municipal and bore-well water varies a lot in hardness, so cafés "
                     "use reverse osmosis followed by remineralisation to hit the target and protect "
                     "the espresso machine. The Part 2 model budgets ₹1 lakh for it.")], lw=0.48))
    s.append(src("SCA water quality standard as reproduced by industry guides (Pact Coffee, "
                 "Bartovation)."))
    s.append(h2("9.4 Why are there so many brewing methods?"))
    s.append(p("Every method is a different answer to four questions: <b>how water meets the coffee</b> "
               "(soaking or flowing through), <b>what filters it</b> (paper, metal, cloth or nothing), "
               "<b>whether pressure is used</b>, and <b>how long and how hot</b>. These choices trade "
               "clarity against body, strength against volume, and control against convenience. "
               "Culture and history did the rest: Italy's espresso bars, Turkey's coffee houses, "
               "Tamil Nadu's tumblers, Vietnam's condensed-milk phin and Japan's pour-over craft."))
    rows = [["Immersion (steeping)", "Coffee soaks in water, then is separated", "French press, cold brew, "
             "Clever, siphon, cupping", "Even extraction, full body, forgiving"],
            ["Percolation (gravity)", "Water flows through a bed of coffee", "V60, Kalita, Chemex, batch "
             "brew, filter kaapi, phin", "Clarity and sweetness; technique matters"],
            ["Pressure", "Water forced through compacted coffee", "Espresso (9 bar), moka pot (1-2 bar), "
             "AeroPress (low)", "Concentrated, syrupy, crema"],
            ["Boiling / decoction", "Coffee simmered with water", "Turkish cezve, traditional boiled",
             "Thick, unfiltered, intense"]]
    s.append(tbl(["Family", "Principle", "Examples", "Typical result"], rows, [90, 130, 160, W - 380],
                 font_size=7.6))
    s.append(figc(DF.method_map(W, 200), "Figure 9.2. Where the main methods sit on the clarity-body map."))
    s.append(h2("9.5 Milk: the other half of most Indian coffee"))
    s.append(p("Most coffee sold in Indian cafés contains milk. Steaming injects air and heat: whey and "
               "casein proteins wrap tiny air bubbles to make foam, while fat adds creaminess but "
               "weakens foam. Full-cream milk (3.5% fat or more) makes the silkiest microfoam for "
               "latte art. Sweetness peaks around 55-65°C; above about 70°C milk scalds and tastes "
               "eggy. Buffalo milk (6-7% fat) is rich but foams heavily, which is why many Indian cafés "
               "use full-cream cow's milk. Among plant milks, 'barista' oat milks foam best, while soy "
               "can curdle in acidic coffee."))
    s.append(figc(BA.figure(BA.draw_milk_drinks, W, 96),
                  "Figure 9.3. The espresso-and-milk family, shown as cross-sections."))
    s += M.ch9()
    s += M2.chemistry()
    s += M6.ratio_reference()
    return s


# =============================================================================== 10. methods
def ch10():
    s = chapter("c10", 10, "Brewing methods, step by step", "What each method is, where it came from, "
                "and exactly how to make it", BERRY)
    s.append(lead("Recipes below are starting points that professionals use. Weigh coffee and water with "
                  "a scale, use filtered water just off the boil (unless stated) and adjust the grind by "
                  "taste."))
    s += method_card("espresso", "Espresso", "pressure, 25-30 seconds, the base of most café drinks", [
        "Espresso forces hot water at about 9 bar through a compact puck of finely ground coffee, "
        "producing a small, concentrated, syrupy shot topped with crema (an emulsion of oils and CO2). "
        "Angelo Moriondo patented a steam-pressure machine in Turin in 1884; Bezzera and Pavoni added "
        "the portafilter in the early 1900s; Achille Gaggia's lever machine (1947-48) created crema as "
        "we know it; the pump-driven Faema E61 (1961) set the modern template.",
        "A café machine has a boiler (single, heat-exchanger or one per group), group heads, "
        "portafilters with baskets, a pump and steam wands. An SCA survey of professionals found the "
        "typical recipe is an 18-20 g dose producing about 36 g in 25-30 seconds at 9 bar and "
        "about 93°C."],
        [("Dose", "18-20 g (double basket)"), ("Yield", "36-40 g (ratio 1:2)"), ("Time", "25-30 s"),
         ("Grind", "Fine, like caster sugar"), ("Water", "92-94°C, 9 bar"),
         ("Variants", "Ristretto 1:1-1:1.5; lungo 1:3; americano = shot + hot water")],
        ["Flush the group head for 2 seconds; wipe the basket dry.",
         "Grind 18 g into the basket; level it by tapping or with a distribution tool.",
         "Tamp straight and level with firm, consistent pressure; wipe the rim.",
         "Lock in and start immediately; place the cup on a scale.",
         "Stop at 36 g; check time (25-30 s) and taste; adjust the grind, never the tamp."],
        ["Fresh coffee (7-30 days off roast) gives thicker crema; robusta adds crema too.",
         "Uneven shots (spurts, pale streaks) mean channelling: fix distribution first."], color=BERRY)
    s.append(KeepTogether([h3("The espresso-and-milk family"),
                           tbl(["Drink", "Espresso", "Milk and foam", "Cup"],
                               [["Macchiato", "Single or double", "A spoon of foam", "60-90 ml"],
                                ["Cortado", "Double", "Equal steamed milk, little foam", "120 ml"],
                                ["Flat white", "Double (often ristretto)", "Thin, glossy microfoam", "150-180 ml"],
                                ["Cappuccino", "Single or double", "Equal-ish milk and 1-2 cm foam", "150-200 ml"],
                                ["Latte", "Single or double", "Lots of milk, thin foam", "240-300 ml"],
                                ["Mocha", "Double", "Chocolate + latte milk", "240-300 ml"],
                                ["Iced latte / cold coffee", "Double", "Cold milk, ice; Indian 'cold coffee' "
                                 "often blended with ice cream", "300-400 ml"]],
                               [80, 100, 220, W - 400], font_size=7.6)]))
    s.append(Spacer(1, 6))
    s += method_card("v60", "Pour-over: V60, Kalita and Chemex", "percolation through paper, clean and "
                     "aromatic", [
                         "Pour-over brewers hold a paper filter in a cone; you pour water by hand and it "
                         "drains through the coffee bed. Melitta Bentz invented the paper filter in "
                         "Dresden in 1908. Hario's <b>V60</b> (2004) has a 60° cone, spiral ribs and one "
                         "large hole, so flow depends on your pouring: fast and expressive. The "
                         "<b>Kalita Wave</b> has a flat bed and three small holes: slower, more even, "
                         "more forgiving. The <b>Chemex</b> (Peter Schlumbohm, 1941) uses thick bonded "
                         "paper for an exceptionally clean, tea-like cup.",
                         "Pour-over shows off single-origin, light-to-medium roasts: florals, fruit and "
                         "acidity come through clearly. James Hoffmann's widely used V60 recipe is below."],
                     [("Dose", "30 g coffee"), ("Water", "500 g at 93-100°C"), ("Ratio", "1:16.7"),
                      ("Grind", "Medium-fine (table salt)"), ("Time", "~3:30 total"),
                      ("One cup", "15 g : 250 g in five 50 g pours")],
                     ["Rinse the paper with hot water and discard the water.",
                      "Add the coffee, make a small well; start the timer and pour 60 g to bloom; swirl. "
                      "Wait up to 45 s while CO2 escapes.",
                      "Pour steadily to 300 g by 1:15 (60% of the water).",
                      "Pour to 500 g by 1:45, then give a gentle stir and a final swirl to flatten the bed.",
                      "Let it drain (done by about 3:30). Flat bed = even extraction."],
                     ["Slow drawdown and bitterness: grind coarser. Fast and sour: finer.",
                      "Kalita: same ratio, pour in 4-5 pulses. Chemex: grind a little coarser; "
                      "expect 4-4:30."], color=TEAL, extra="chemex")
    s += method_card("kaapi", "South Indian filter kaapi", "slow percolation into a strong decoction, "
                     "then hot milk and sugar", [
                         "Filter coffee is the everyday coffee of Tamil Nadu and Karnataka. The "
                         "stainless-steel <b>filter</b> is two stacked cylinders: the upper one has a "
                         "perforated base and a pressing disc (the 'umbrella'); the lower one collects "
                         "the <b>decoction</b>. Fine coffee powder, often blended with roasted chicory, "
                         "percolates slowly for 10-20 minutes into a thick, strong extract. It is mixed "
                         "with boiling milk and sugar and served in a <b>tumbler and davara</b> "
                         "(dabarah): pouring between the two from a height cools and froths the coffee "
                         "('meter coffee').",
                         "<b>Chicory</b> (roasted root of Cichorium intybus) adds body, colour and "
                         "bitterness at lower cost; blends run 70:30, 80:20 or 90:10 coffee to chicory. "
                         "Kumbakonam '<b>degree coffee</b>' is said to take its name from the lactometer "
                         "'degree' that certified pure, undiluted milk."],
                     [("Powder", "20-25 g (2-3 heaped tbsp)"), ("Water", "100-150 ml near boiling"),
                      ("Decoction", "~60-80 ml, very strong"), ("Grind", "Fine, finer than pour-over"),
                      ("Time", "10-20 min percolation"), ("Serve", "1 part decoction : 2-3 parts hot "
                       "milk, sugar to taste")],
                     ["Put the powder in the upper chamber and rest the umbrella disc on it (no "
                      "hard tamping, or it will stall).",
                      "Pour near-boiling water over the disc, close the lid and wait 10-20 minutes.",
                      "Heat full-cream milk to a boil; add sugar to the tumbler.",
                      "Add 1 part decoction to 2-3 parts milk; 'pull' the coffee between tumbler and "
                      "davara 3-4 times until frothy."],
                     ["A specialty kaapi made with estate arabica and little or no chicory is a natural "
                      "menu signature for an Ahmedabad café (Part 2 prices drinks at ₹220 on average).",
                      "Decoction keeps for a few hours; make it fresh for each service."],
                     color=SAFFRON, extra="davara")
    s += method_card("french", "French press", "immersion with a metal mesh: rich, heavy, forgiving", [
        "A glass or steel jug with a mesh plunger. The coffee steeps, then the mesh separates the "
        "grounds; oils and fine particles pass through, giving a full, rounded body and a little "
        "sediment. Early versions were French (1850s); Italians Attilio Calimani (1929) and Faliero "
        "Bondanini (1958) patented the design that became the Bodum 'Chambord'."],
        [("Dose", "30 g"), ("Water", "500 g just off the boil"), ("Ratio", "1:16.7"),
         ("Grind", "Medium to medium-coarse"), ("Time", "4 min + 5-8 min settle")],
        ["Add coffee, pour all the water, and leave for 4 minutes.",
         "Stir the crust, then skim off the foam and floating grounds with two spoons.",
         "Wait 5-8 minutes more so fines settle.",
         "Press the plunger only to the surface and pour slowly."],
        ["Hoffmann's 'no-press' method gives a cleaner cup with less sludge."], color=SKY)
    s += method_card("aeropress", "AeroPress", "immersion plus gentle pressure through paper", [
        "Invented in 2005 by Alan Adler (of Aerobie frisbee fame), the AeroPress is a plastic syringe: "
        "coffee steeps in the chamber, then you press it through a small paper filter. It is fast, "
        "portable, almost unbreakable and endlessly adjustable; there has been a World AeroPress "
        "Championship since 2008."],
        [("Dose", "11 g"), ("Water", "200 g at ~99°C"), ("Ratio", "1:18"), ("Grind", "Fine-medium"),
         ("Time", "2 min steep + 30 s press")],
        ["Fit a rinsed paper, place on a mug and add the coffee.",
         "Pour all the water; insert the plunger slightly to stop dripping.",
         "At 2:00 swirl gently; wait 30 seconds.",
         "Press slowly for about 30 seconds."],
        ["Inverted brewing (upside down) avoids early dripping; many champions use it."], color=PLUM)
    s += method_card("moka", "Moka pot", "steam pressure on the stove: strong and bold", [
        "Alfonso Bialetti's aluminium Moka Express (1933, designed with Luigi De Ponti) put strong "
        "coffee into every Italian kitchen. Water in the lower chamber boils; steam pressure of about "
        "1-1.5 bar pushes it up through the coffee basket into the top chamber. It is not espresso "
        "(which needs about 9 bar) but it is intense, heavy and slightly bitter, and a popular home "
        "method in India too."],
        [("Water", "Hot water to just below the valve"), ("Coffee", "Basket level-filled, 15-20 g"),
         ("Grind", "Fine-medium, not espresso-fine"), ("Heat", "Medium; lid open")],
        ["Fill the base with hot water (shortens the time the coffee sits on heat).",
         "Fill the basket level without tamping; screw the top on firmly.",
         "Heat until coffee flows; remove as soon as it starts to gurgle and sputter.",
         "Cool the base under a tap to stop extraction; stir and serve."],
        ["Dilute with hot water for a smoother 'americano'."], color=BERRY)
    s += method_card("cold", "Cold brew, cold drip and Japanese iced", "time instead of heat", [
        "Cold brew steeps coarse coffee in cold or room-temperature water for 12-24 hours. Little "
        "acid and bitterness is extracted, so it tastes smooth, chocolatey and sweet, though less "
        "aromatic. <b>Cold drip</b> (Kyoto towers) drips iced water through coffee over 3-12 hours. "
        "<b>Japanese iced coffee</b> brews hot pour-over straight onto ice (for example 30 g coffee, "
        "300 g hot water, 200 g ice), keeping the aroma of hot brewing. Iced coffee is one of the "
        "fastest-growing café categories in India."],
        [("Ratio", "1:8 concentrate, or 1:12-1:15 ready to drink"), ("Grind", "Coarse"),
         ("Time", "12-24 h, then filter"), ("Keep", "Refrigerated, ~1 week")],
        ["Mix coffee and water in a jar or a cold-brew bag; stir to wet all grounds.",
         "Steep 12-18 h in the fridge (or 12 h at room temperature, then chill).",
         "Filter through paper or cloth; dilute concentrate 1:1 with water or milk over ice."],
        ["Medium-roast Indian arabica with some fine robusta makes excellent, cheap cold brew."],
        color=SKY)
    rows = [["Batch brew (drip machine)", "A machine showers hot water over a basket of coffee and drips "
             "into a flask; SCA-certified brewers control temperature and contact time",
             "60 g per litre (1:16-1:18); medium grind; 4-6 min", "Volume at speed: ideal for office "
             "crowds; hold in airpots 30-60 min"],
            ["Turkish (cezve / ibrik)", "Powder-fine coffee, water and often sugar or cardamom heated "
             "until it foams, 2-3 times, never boiled; served unfiltered; UNESCO heritage (2013)",
             "7-8 g per 60-70 ml", "Thick, intense, aromatic; grounds settle in the cup"],
            ["Vietnamese phin", "A small steel drip filter on a glass; dark robusta drips slowly onto "
             "sweetened condensed milk; with ice it becomes cà phê sữa đá", "20 g : 100 ml; 4-5 min",
             "Strong, sweet, chocolatey; a natural fit for Indian robusta"],
            ["Siphon (vacuum pot)", "Vapour pressure pushes water into the upper chamber to steep; "
             "when heat is removed, a vacuum pulls the coffee down through a cloth filter (1830s-40s, "
             "Germany and France)", "15 g : 225 g; 1-1.5 min steep", "Clean, aromatic, theatrical"],
            ["Clever dripper", "A cone with a shut-off valve: steep like a French press, drain through "
             "paper when placed on a cup", "18 g : 300 g; 3-4 min", "Easy consistency with paper "
             "clarity"]]
    s.append(KeepTogether([h3("Other methods worth knowing"),
                           BA.strip([("batch", "Batch brew"), ("cezve", "Cezve"), ("phin", "Phin"),
                                     ("siphon", "Siphon"), ("clever", "Clever")], W, 92),
                           Spacer(1, 4),
                           tbl(["Method", "What it is", "Recipe", "Result / use"], rows,
                               [80, 220, 100, W - 400], font_size=7.4)]))
    s.append(h3("Instant coffee: how it is made"))
    s.append(p("Instant (soluble) coffee is brewed in factories and dried. Roasted, ground coffee is "
               "extracted with hot water under pressure in counter-current columns (the extract leaves "
               "at about 15-30% solids), concentrated (up to ~60%), and then either <b>spray-dried</b> "
               "in tall towers into powder (often re-wetted and agglomerated into granules) or "
               "<b>freeze-dried</b>, which keeps more aroma. Aroma driven off during processing is "
               "captured and added back; final moisture is below 5%. Instant dominates Indian homes "
               "(roughly two-thirds to three-quarters of consumption, much of it coffee-chicory), and "
               "about 41% of India's coffee exports are instant, made by firms such as Tata Consumer, "
               "CCL Products and Nestlé."))
    s.append(h3("All methods compared"))
    rows = [["Espresso", "Pressure", "Fine", "1:2", "92-94°C", "25-30 s", "●●●●●", "●●", "Hard",
             "₹6-26 lakh café; ₹15k+ home"],
            ["Moka pot", "Pressure", "Fine-med", "~1:7", "Stove", "4-5 min", "●●●●", "●●", "Easy", "₹1.5-4k"],
            ["AeroPress", "Hybrid", "Fine-med", "1:15-18", "80-99°C", "2.5 min", "●●●", "●●●", "Easy",
             "₹3-4k"],
            ["V60 / Kalita", "Percolation", "Med-fine", "1:16-17", "93-100°C", "3-4 min", "●●", "●●●●●",
             "Medium", "₹0.8-3k"],
            ["Chemex", "Percolation", "Medium", "1:16", "93-100°C", "4-5 min", "●", "●●●●●", "Medium",
             "₹4-6k"],
            ["Filter kaapi", "Percolation", "Fine", "~1:5 dec.", "~95°C", "10-20 min", "●●●●", "●●",
             "Easy", "₹0.4-1.2k"],
            ["French press", "Immersion", "Coarse", "1:16", "~95°C", "4-9 min", "●●●●", "●●", "Easy",
             "₹0.8-2.5k"],
            ["Cold brew", "Immersion", "Coarse", "1:8-15", "Cold", "12-24 h", "●●●", "●●●", "Easy",
             "₹0.5-2k"],
            ["Batch brew", "Percolation", "Medium", "1:16-18", "92-96°C", "4-6 min", "●●", "●●●●", "Easy",
             "₹0.3-2 lakh"],
            ["Turkish", "Boiled", "Powder", "1:9", "Just foaming", "3-4 min", "●●●●●", "●", "Medium",
             "₹0.6-2k"],
            ["Phin", "Percolation", "Medium", "1:5", "~95°C", "4-5 min", "●●●●", "●●", "Easy", "₹0.5-1k"],
            ["Siphon", "Immersion", "Medium", "1:15", "~92°C", "1-2 min", "●●", "●●●●", "Hard", "₹4-10k"]]
    s.append(tbl(["Method", "Family", "Grind", "Ratio", "Water", "Time", "Body", "Clarity", "Skill",
                  "Kit cost (India)"], rows,
                 [58, 54, 44, 42, 50, 46, 40, 40, 34, W - 408], font_size=7.0, head_size=7.0))
    s.append(src("SCA; Hoffmann recipes (Hario, 2021-23); manufacturers; indicative Indian retail "
                 "prices (Oct 2026)."))
    s += M.ch10()
    s += M2.cafe_recipes()
    s += M3.iced_production()
    s += M4.espresso_deep()
    s += M4.kaapi_culture()
    s += M7.pour_schedule()
    s += M7.cheat_sheet()
    return s


# =============================================================================== 11. tasting
def ch11():
    s = chapter("c11", 11, "Tasting and judging quality", "How to taste like a professional and what "
                "the words mean", PLUM)
    s.append(side([p("Most of what we call 'taste' is smell. The tongue reads only sweet, sour, salty, "
                     "bitter and umami; aromas reach the nose from the back of the mouth when you "
                     "swallow or slurp (retro-nasal smell). That is why professional tasters slurp "
                     "noisily: it sprays coffee across the palate and pushes aroma up to the nose."),
                   p("Taste coffee at several temperatures: hot coffee hides flaws and sweetness; as it "
                     "cools, acidity and defects show. Compare two coffees side by side; the "
                     "differences are far easier to notice than absolute qualities.")],
                  [il.CanvasFigure(W * 0.46, 130, il.taste_smell)], lw=0.52))
    s.append(h2("11.1 The vocabulary"))
    s.append(side([il.CanvasFigure(W * 0.5, 140, il.acidity_scale)],
                  [il.CanvasFigure(W * 0.46, 140, il.body_glasses)], lw=0.52))
    rows = [["Acidity", "Bright, lively sharpness (like apple or citrus), not sourness", "Clean washed "
             "high-grown arabica"],
            ["Body", "Weight and texture in the mouth: tea-like to syrupy", "Naturals, robusta, "
             "French press, espresso"],
            ["Sweetness", "Caramel, honey, ripe fruit; sign of ripe cherries and good roasting", "Most "
             "prized quality marker"],
            ["Balance", "No one attribute shouts over the others", "Good blends"],
            ["Clean cup", "No off-flavours from first sip to finish", "Careful processing"],
            ["Aftertaste / finish", "How long pleasant flavour lingers; dry or bitter finish is a flaw",
             "Well-developed roasts"],
            ["Flavour notes", "Descriptors like jasmine, peach, chocolate: aromas the coffee resembles, "
             "nothing is added", "Use the flavour wheel"]]
    s.append(tbl(["Word", "Meaning", "Where you find it"], rows, [82, 260, W - 342], font_size=7.6))
    s.append(h2("11.2 The flavour wheel and defects in the cup"))
    s.append(side([il.CanvasFigure(W * 0.46, 190, il.flavour_wheel)],
                  [tbl(["Off-flavour", "Likely cause"],
                       [["Sour, vinegar, onion", "Over-fermentation, sour beans"],
                        ["Musty, earthy, mouldy", "Damp drying or storage"],
                        ["Medicinal, 'rioy', iodine", "Microbial taint, robusta faults"],
                        ["Grassy, peanut, astringent", "Unripe cherries, underdeveloped roast"],
                        ["Papery, woody, cardboard", "Old green coffee or stale roast"],
                        ["Burnt, ashy, smoky", "Over-roasting or scorching"],
                        ["Hollow, flat", "Stale beans, too-soft water"],
                        ["Bitter, drying", "Over-extraction, too fine or too hot"]],
                       [W * 0.25, W * 0.27], font_size=7.4)], lw=0.48))
    s.append(h2("11.3 Linking the chain to the cup"))
    rows = [["Species & variety", "Sets the potential: sweetness, acidity, complexity"],
            ["Altitude & terroir", "Density, acidity, aromatic complexity"],
            ["Picking", "Sweetness and cleanliness (ripe-only picking)"],
            ["Processing", "Clarity (washed) versus fruit and body (natural, honey, experimental)"],
            ["Drying & storage", "Freshness of the green coffee; absence of must and ferment"],
            ["Roast", "Which flavours are expressed: acidity and florals (light) or chocolate and "
             "roastiness (dark)"],
            ["Freshness", "Aroma intensity; flat after 4-6 weeks opened"],
            ["Grind & brew", "Whether the potential is extracted: sour, sweet or bitter"],
            ["Water & milk", "Clarity, sweetness, texture"]]
    s.append(tbl(["Link in the chain", "What it contributes to the cup"], rows, [110, W - 110],
                 font_size=7.6))
    s += M.ch11()
    s += M3.myths()
    s += M4.wheel_categories()
    return s


# =============================================================================== 12. markets
def ch13():
    s = chapter("c13", 13, "The coffee market", "Global supply and demand, India's production, exports "
                "and drinking habits, the café boom, and Ahmedabad", SKY)
    s.append(h2("13.1 Global supply, demand and price"))
    s.append(side([p("World production reached a record 178.8 million bags in 2025/26 and USDA expects "
                     "another record in 2026/27, led by Brazil (71.9 million). Consumption keeps "
                     "growing about 1-2% a year to a forecast 179.7 million bags, driven by Asia: "
                     "China, Indonesia, the Philippines, Vietnam and India are the fastest-growing "
                     "markets. Stocks fell for five years to 20.1 million bags, which together with "
                     "Brazilian and Vietnamese droughts pushed prices to records in early 2025."),
                   p("For a café the lesson is that <b>green-coffee prices swing by 30-50%</b> within a "
                     "couple of years. Part 2's model carries a green-price index with Best (0.90), "
                     "Base (1.00) and Worst (1.25) starting points and a sensitivity to ±30%.")],
                  [DC.bar_chart(["Production", "Consumption", "Exports", "Ending stocks"],
                                [("2025/26", [178.8, 173.9, 123.8, 20.1], CARAMEL),
                                 ("2026/27F", [189.6, 179.7, 131.4, None], ROAST)], W * 0.46, 150,
                                title="World balance, million 60-kg bags", fmt="{:.0f}")], lw=0.52))
    s.append(src("USDA FAS Coffee: World Markets and Trade (Dec 2025; Jun 2026). 2026/27 production = "
                 "2025/26 + 10.8 million bags."))
    s.append(h2("13.2 India: production and exports"))
    s.append(side([DC.bar_chart(["10-yr avg", "2024/25", "2025/26", "2026/27F"],
                                [("Total", [5.67, 6.06, 6.43, 6.14], CARAMEL)], W * 0.48, 150,
                                title="India's crop, million 60-kg bags (USDA)", fmt="{:.2f}")],
                  [p("India grows about 6-6.4 million bags (360-385 thousand tonnes) a year, about three "
                     "quarters robusta. Area planted is about 4.75 lakh ha with some 645 million trees; "
                     "production has grown only about 2% a year over the past decade because yields are "
                     "flat and replanting is slow. The Coffee Board's goal is 9 lakh tonnes by 2047, "
                     "mostly by expanding into non-traditional areas such as Odisha and the North-East."),
                   p("Exports reached <b>6.22 million bags</b> forecast for 2026/27: 59% green beans and "
                     "41% instant coffee. About 61% leaves through Mangalore, and Europe takes 44-45%.")],
                  lw=0.5))
    s.append(src("USDA FAS India Coffee Annual (May 2026); PIB (Nov 2025)."))
    s.append(h2("13.3 India: who drinks coffee and how"))
    s.append(side([DC.donut([73, 27], ["Instant / soluble", "Roast & ground (filter, café, beans)"],
                            [SAFFRON, ROAST], W * 0.46, 110, centre="1.58 m", centre_sub="bags, 2026/27",
                            title="Domestic consumption by type")],
                  [p("India drinks only about 1.6 million bags (about 95,000 tonnes) a year: <b>0.04 kg "
                     "per person</b>, against a world average of 1.3 kg. Consumption has grown from about "
                     "80,000 tonnes in 2020 to 90-95,000 tonnes in 2024. Instant coffee, much of it "
                     "blended with chicory, accounts for roughly two-thirds to three-quarters of the "
                     "volume; Nestlé (Nescafé) and Hindustan Unilever (Bru) hold more than 70% of the "
                     "instant market."),
                   p("Geography matters: the south drinks filter coffee at home, while the north, east "
                     "and west mostly drink instant, and increasingly cafés. The growth is young and "
                     "urban: a 2025 World Coffee Portal survey of 4,000 Indians found 24% visit a coffee "
                     "shop daily and 57% weekly, and a third of visits happen after 5 pm.")], lw=0.48))
    s.append(src("USDA FAS (May 2026); Ken Research; Coffee Board consumption surveys; World Coffee "
                 "Portal Project Café India 2025."))
    s.append(h2("13.4 India's café boom"))
    chains = [("Tata Starbucks", 480), ("Barista", 465), ("Café Coffee Day", 425), ("Third Wave", 172),
              ("Café Buddy's", 145)]
    s.append(side([DC.hbar_chart([a for a, _ in chains], [b for _, b in chains], W * 0.48, 118,
                                 title="Largest branded chains (outlets, 2025)",
                                 colors_=[TEAL, SKY, BERRY, PLUM, SAFFRON], label_w=78),
                   DC.line_chart(["2024", "2025", "2026F", "2030F"], [("Branded outlets", [4739, 5339, 6110,
                                                                                            10000], ROAST)],
                                 W * 0.48, 110, title="Branded coffee-shop outlets in India", ylo=0,
                                 yhi=10000)],
                  [p("India had <b>5,339 branded coffee shops</b> in 2025, 600 more than a year earlier "
                     "(+12.7%), and World Coffee Portal expects more than 10,000 by 2030. Specialty "
                     "chains grow fastest: Blue Tokai and Third Wave each added 56 stores in a year."),
                   R.data_table(["Chain", "Latest revenue", "Note"],
                                [["Tata Starbucks", "₹1,277 cr (FY25)", "Loss ₹136 cr; ~₹2.7 cr per store; "
                                  "500th store Apr 2026"],
                                 ["Café Coffee Day", "₹1,035 cr (FY25)", "Restructured chain"],
                                 ["Blue Tokai", "₹341 cr (FY25)", "+58%; FY24 loss ₹63 cr"],
                                 ["Third Wave", "₹241 cr (FY24)", "+67%"]],
                                [62, 64, W * 0.5 - 136], font_size=7.0),
                   p("The leaders are growing quickly but most still lose money at company level once "
                     "head-office and expansion costs are included. Individual stores, however, can earn "
                     "healthy margins, which is what Part 2 models.")], lw=0.5))
    s.append(src("World Coffee Portal via Comunicaffe (Sep 2025); company filings and press summaries "
                 "(Inc42, The Arc Web, LinkedIn)."))
    s.append(h2("13.5 Ahmedabad's coffee scene"))
    s.append(p("Ahmedabad is a city of about 8-9 million with high incomes, a young workforce, a strong "
               "vegetarian food culture and, under Gujarat's prohibition law, no bars. Cafés and dessert "
               "places therefore do the work that pubs do elsewhere: they are where friends meet in the "
               "evening. The specialty scene has grown from Zen Café (2008) to national chains (Tata "
               "Starbucks, Third Wave, Blue Tokai, Barista, CCD) and local brands such as Slay Coffee, "
               "The Dark Roast, OCD Culture and Kaffa, with new specialty openings on Sindhu Bhavan Road "
               "(for example Beanora in 2025-26)."))
    rows = [["Sindhu Bhavan Road (Bodakdev)", "Premier F&B high street; evening and weekend crowds; "
             "highest spend", "₹85-220/sqft/month"],
            ["Prahladnagar / Corporate Road", "Office belt and upscale homes; dense chain competition",
             "₹55-120"],
            ["SG Highway, Thaltej, Vastrapur", "Malls, offices, IIM-A belt; established cafés", "₹80-180"],
            ["CG Road, Navrangpura, Law Garden", "Older commercial heart, students", "₹70-160"],
            ["Bopal, South Bopal, Shela", "Fast-growing western suburbs, young families", "₹40-80"],
            ["GIFT City (Gandhinagar)", "International finance hub; captive office workforce; few cafés",
             "~₹110 + high maintenance"],
            ["Sanand", "Semiconductor and auto cluster 25 km west; Micron plant opened Feb 2026",
             "~₹40-60 (estimate)"]]
    s.append(tbl(["Hub", "Character", "Ground-floor rent (indicative)"], rows, [140, 230, W - 370],
                 font_size=7.6))
    s.append(src("99acres, MagicBricks, housing.com listings (Oct 2026); Micron investor relations; GIFT City "
                 "releases; Perfect Daily Grind."))
    s += LM.market_more()
    s += M2.india_culture()
    s += M3.per_capita()
    s += M4.global_players()
    s += M6.specialty_india()
    s += M6.chain_economics()
    s += M7.outlook()
    s += M4.checklist()
    s += M5.chain_on_a_page()
    s.append(note("Ten takeaways from Part 1 for a café founder", [
        "1. Quality is decided upstream: variety, altitude, picking and processing set the ceiling.",
        "2. Indian washed arabica plus washed ('fine') robusta makes a clean, chocolatey, affordable "
        "espresso that suits milk drinks.",
        "3. Green coffee is a volatile commodity; prices tripled from 2019 to 2025. Budget for swings.",
        "4. Roast date matters: buy or roast little and often, and serve beans 7-30 days off roast.",
        "5. A good grinder and treated water improve every cup more than an expensive machine.",
        "6. Weigh everything; use recipes; dial in by taste every morning.",
        "7. Offer a range: espresso and milk drinks for volume, pour-over for showcase lots, cold coffee "
        "for summer, and a specialty filter kaapi as a signature.",
        "8. Coffee is only ~10% of a café's price; labour, rent and service make up most of the rest.",
        "9. Toll roasting gives own-label control without a roaster's fixed costs; an in-house roastery "
        "needs wholesale volume.",
        "10. India's café market is growing about 13% a year, and Ahmedabad's dry-state social life "
        "favours cafés."], ROAST, bg=HX("#F7F1E8")))
    s += [PageBreak()] + M.glossary()
    return s
