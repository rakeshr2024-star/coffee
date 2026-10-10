"""Part 1, chapter 12: from roaster to customer (packaging, channels, the café, the customer)."""
import deep_charts as DC
import deep_figs as DF
import deep_more2 as M2
import deep_more3 as M3
import deep_more4 as M4
import deep_more5 as M5
import deep_more7 as M7
from deep_base import (BERRY, CARAMEL, CONTENT_W, GOLD, LEAF, PLUM, ROAST, SAFFRON, SKY, TEAL, HX,
                       bl, chapter, figc, h2, lead, note, p, side, src, tbl)

W = CONTENT_W


def ch12():
    s = chapter("c12", 12, "From roaster to customer", "Packaging, distribution channels, the café as "
                "the last step, and who India's coffee customers are", HX("#8E3B46"))
    s.append(lead("The last mile is where most of coffee's value is added. Once roasted, coffee is a "
                  "perishable, aromatic product that has to reach the customer fresh, in the right format "
                  "and through the right channel."))
    s.append(h2("12.1 How coffee reaches the customer"))
    steps = [("Roaster", "Roasts, blends, packs, rests coffee; quality control"),
             ("Distributor / own logistics", "Warehousing, delivery to cities; cold chain for RTD"),
             ("Channel", "Café, hotel, office, supermarket, kirana, marketplace, website, quick commerce"),
             ("Brewing point", "Barista, office machine or the customer's own kitchen"),
             ("Customer", "Drinks it: minutes to weeks after roasting")]
    s.append(figc(DC.flow(steps, W, 70, per_row=5, colors_=[ROAST, SKY, PLUM, BERRY, LEAF], sub_size=6.0,
                          head_size=7.2),
                  "Figure 12.1. The downstream chain. Freshness is lost at every hand-off."))
    rows = [["Cafés and restaurants (HoReCa)", "Whole beans, 1 kg bags; often with equipment on loan or "
             "lease and barista training", "Consistency, service, price per kg", "Largest specialty "
             "channel; sticky accounts"],
            ["Hotels and offices", "Beans for bean-to-cup machines, drip bags, batch brew", "Uptime, "
             "simplicity", "GIFT City-type office clusters"],
            ["Supermarkets and kiranas", "Instant jars and sachets, filter-coffee powder, ground coffee",
             "Price, brand, shelf life", "Mass market; dominated by Nescafé, Bru and filter brands"],
            ["E-commerce marketplaces", "Beans, ground, drip bags, instant", "Ratings, discounts",
             "Wide reach; high commissions and returns"],
            ["Roaster websites (D2C) and subscriptions", "Fresh beans by roast date; gear", "Freshness, "
             "story, convenience", "Core of Indian specialty roasters' growth"],
            ["Quick commerce (10-minute apps)", "Cold brew bottles/cans, instant, drip bags, beans",
             "Speed, impulse", "Fastest-growing urban channel since 2023"],
            ["Vending and kiosks", "Instant premixes, bean-to-cup", "Speed, price", "Railways, offices, "
             "campuses"]]
    s.append(tbl(["Channel", "Typical products", "What wins", "Notes"], rows, [110, 170, 90, W - 370],
                 font_size=7.3))
    s.append(h2("12.2 What a bag of specialty coffee pays for"))
    bag = [("Green coffee (297 g)", 276, ROAST), ("Roasting & labour", 30, CARAMEL),
           ("Bag, valve, label", 12, GOLD), ("Shipping to customer", 70, SKY),
           ("Payment & platform fees", 14, HX("#9A8C80")), ("Marketing & acquisition", 86, PLUM),
           ("Overheads & margin", 83, LEAF)]
    s.append(figc(DF.cup_anatomy(bag, W, 74, "Illustrative build-up of a ₹571 (ex-GST) 250 g bag sold "
                                             "direct to consumers"),
                  "Figure 12.2. Green cost uses the Part 2 Specialty mix (₹926/kg green, 16% roast loss). "
                  "Other items are typical ranges for Indian D2C roasters and are illustrative."))
    s.append(p("Two lessons follow. First, specialty roasting is a thin-margin business once marketing "
               "and delivery are paid for; scale and repeat customers (subscriptions, café accounts) make "
               "it work. Second, a café that sells its own beans skips most of the distribution cost: "
               "the customer is already in the room. That is why the Part 2 model gives own-label "
               "routes a higher retail share (8% of sales against 6%)."))
    s.append(h2("12.3 The café: the final and most valuable step"))
    rows = [["Kiosk / cart", "100-300", "0-6", "₹8-20 lakh", "Espresso, cold coffee, grab-and-go",
             "Malls, metro stations, campuses"],
            ["Express / takeaway", "300-700", "8-20", "₹20-45 lakh", "Espresso bar, pastries, delivery",
             "Office districts, high streets"],
            ["Full-service café", "800-1,500", "30-60", "₹50-90 lakh", "Espresso, manual brew, full food "
             "menu", "Neighbourhood and high-street sites"],
            ["Roastery café", "2,000+", "60+", "₹1.5 crore+", "On-site roaster, retail, training",
             "Flagship of a brand"],
            ["Drive-thru", "1,000+ plus lanes", "Few", "₹1 crore+", "Speed, cold drinks", "Highways, "
             "suburbs"]]
    s.append(tbl(["Format", "Size (sqft)", "Seats", "Typical capex", "Offer", "Where"], rows,
                 [80, 56, 40, 66, 140, W - 382], font_size=7.3, center_cols=(1, 2, 3)))
    s.append(src("Capex ranges from Part 2's equipment and fit-out costs and Indian fit-out quotes; "
                 "indicative."))
    s.append(p("Customers in a café pay for far more than coffee: a place to sit, Wi-Fi, service, "
               "speed, music, food and the feeling of a treat. That is why a café can charge ₹200-350 for "
               "a drink whose ingredients cost ₹25-65 (Chapter 10), and also why its costs are dominated "
               "by staff and rent rather than beans."))
    s.append(h2("12.4 Who India's coffee customers are"))
    seg = [("Students and young professionals", "Cold coffee, frappés, value combos; social media "
            "driven", "Evenings, weekends"),
           ("Office workers", "Morning espresso and batch brew, delivery to desks, meetings",
            "8-11 am, 3-5 pm"),
           ("Families and friends", "Desserts, food, larger groups; Gujarat's dry law makes cafés the "
            "evening social venue", "After 5 pm, weekends"),
           ("Enthusiasts", "Pour-over, single estates, retail beans, brewing gear", "Weekends"),
           ("South Indian households", "Filter kaapi at home; buy powder and chicory blends", "Morning "
            "ritual"),
           ("Remote workers", "Long stays, Wi-Fi, power points; low spend per hour", "Weekday daytime")]
    s.append(tbl(["Segment", "What they buy", "When"], [list(x) for x in seg], [120, 260, W - 380],
                 font_size=7.4))
    s.append(side([DC.donut([24, 33, 43], ["Daily visitors", "Weekly (not daily)", "Less often"],
                            [BERRY, SAFFRON, HX("#BDB3A7")], W * 0.44, 106, centre="4,000",
                            centre_sub="surveyed, 2025", title="How often Indians visit coffee shops")],
                  [p("World Coffee Portal's 2025 survey of 4,000 Indian consumers found <b>24% visit a "
                     "coffee shop daily</b> and 57% at least weekly, preferring to sit in with friends "
                     "and family; a third of visits happen after 5 pm. Food is a big part of the bill: "
                     "in Indian cafés it is typically 30% or more of sales, which the Part 2 model "
                     "reflects."),
                   p("<b>Implications for the café:</b> design for evening crowds and groups (seating, "
                     "desserts), win the office morning with speed (batch brew, pre-orders), and "
                     "convert enthusiasts into retail-bean customers.")], lw=0.46))
    s.append(src("World Coffee Portal, Project Café India 2025 (via Comunicaffe, Sep 2025)."))
    s.append(h2("12.5 Freshness from roaster to cup"))
    rows = [["Roaster", "Roast to order; rest; pack in valve bags with roast date", "Day 0-2"],
            ["Logistics", "Ship within days; avoid heat (Ahmedabad summers exceed 40°C)", "Day 2-5"],
            ["Café storage", "Cool, dark, sealed; first-in-first-out; small hopper loads", "Day 5-30"],
            ["Grinding", "Grind to order; never pre-grind for the day", "Seconds"],
            ["Retail customer", "Buy 250 g at a time; finish within 3-4 weeks", "Day 7-40"]]
    s.append(tbl(["Stage", "Good practice", "Timing after roast"], rows, [80, 300, W - 380], font_size=7.4))
    s.append(note("Why this matters for the café plan", [
        "Toll roasting near Ahmedabad or fortnightly deliveries keep coffee in the 7-30 day sweet spot "
        "without owning a roaster.",
        "Retail beans and drip bags sold at the counter add high-margin revenue and keep the brand at "
        "customers' homes.",
        "Quick-commerce listings of cold brew and drip bags can follow once the café brand is known."],
        TEAL))
    s += M2.bar_ops()
    s += M3.cafe_design()
    s += M4.sustainability()
    s += M5.case_study()
    s += M5.faq()
    s += M7.buying_guide()
    return s


def market_more():
    """Extra sections for the market chapter (now Chapter 13)."""
    s = [h2("13.6 India's retail coffee market structure")]
    rows = [["Instant coffee", "Nescafé (Nestlé), Bru (HUL), Tata, Continental (CCL), Davidoff",
             "Supermarkets, kiranas, quick commerce", "~65-75% of volume; GST cut to 5% in 2025"],
            ["Filter coffee powder", "Bru filter, Narasu's, Cothas, Leo, Coffee Day, Hatti Kaapi",
             "South Indian retail, kiranas", "Coffee-chicory blends; regional brands"],
            ["Specialty roasters", "Blue Tokai, Subko, KC Roasters, Black Baza, Araku, Corridor Seven, "
             "Devans and hundreds more", "D2C, marketplaces, own cafés", "Single estates, roast dates"],
            ["Café chains", "Tata Starbucks, Barista, CCD, Third Wave, Blue Tokai, Café Buddy's",
             "Own outlets, delivery apps", "5,339 branded outlets (2025)"],
            ["Ready-to-drink", "Cold brew cans and bottles from specialty brands and chains",
             "Quick commerce, modern trade", "Small but fast-growing"]]
    s.append(tbl(["Segment", "Leading names", "Channels", "Notes"], rows, [80, 200, 110, W - 390],
                 font_size=7.3))
    s.append(h2("13.7 Ahmedabad's specialty cafés, compared"))
    cafes = [["OCD Culture", "Bodakdev", "Rotating guest Indian roasters", "Curates guest roasts",
              "V60, AeroPress, espresso", "~₹500"],
             ["Blue Tokai", "CG Road", "Direct-sourced single estates", "Own national roasteries",
              "Espresso, pour-over, flights", "₹700-900"],
             ["Kaffa Coffee Roasters", "Vastrapur / Thaltej", "In-house roasted", "Live roastery",
              "Manual brew, cold brew", "₹1,400"],
             ["Roastery Cultúr", "Bodakdev", "Indian beans", "Own roasting", "Espresso, pour-over",
              "₹800-1,500"],
             ["Mainline Coffee", "Navrangpura", "Not specified", "Buys in", "Manual brew, barrel-aged "
              "cold brew", "₹500-800"],
             ["Third Wave Coffee", "CG Road, Prahladnagar", "~15 Indian estates", "Central roasting",
              "Espresso, cold brew", "₹700-900"],
             ["Tata Starbucks", "Several", "Global + India Estates blend", "Central, dark style",
              "Espresso, Frappuccino", "₹800-1,000"],
             ["Slay, The Dark Roast, Fick's, Grace...", "Prahladnagar, Bodakdev", "Mostly bought-in",
              "Buy in", "Espresso and iced drinks", "₹500-1,400"]]
    s.append(tbl(["Café", "Area", "Beans", "Roasting", "Methods", "For two"], cafes,
                 [90, 80, 110, 76, 100, W - 456], font_size=7.1))
    s.append(src("Café menus, aggregator listings (District, Swiggy, Zomato) and press up to Oct 2026; "
                 "see the companion field guide (Final_Coff.pdf) for ratings."))
    s.append(p("The pattern is clear: Ahmedabad already has chains and a handful of serious specialty "
               "players, mostly in Bodakdev, Vastrapur and CG Road, but few cafés that combine "
               "<b>Indian estate traceability, an own-label roast and a full food menu</b> on the "
               "city's best evening street, and almost none in GIFT City. That gap shapes the Part 2 "
               "recommendation."))
    s.append(h2("13.8 Trends to watch"))
    s += bl(["<b>Cold coffee everywhere</b>: iced lattes, cold brew and Indian 'cold coffee' lead café "
             "menus for eight months of Ahmedabad's year.",
             "<b>Indian estates as heroes</b>: roasters and cafés increasingly name the estate, variety "
             "and process; the Coffee Board's GI tags and awards support this.",
             "<b>Filter kaapi goes premium</b>: specialty kaapi made with estate arabica and little chicory "
             "is appearing on metro café menus.",
             "<b>Quick commerce and RTD</b>: 10-minute delivery has made cold brew cans and drip bags an "
             "impulse buy.",
             "<b>Plant milks and lower sugar</b>: oat milk for an extra ₹40-60 is now standard in "
             "specialty cafés.",
             "<b>Sustainability and traceability</b>: EUDR, shade-grown and bird-friendly claims, "
             "compostable packaging and spent-ground recycling."])
    return s
