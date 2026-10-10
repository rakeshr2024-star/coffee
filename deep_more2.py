"""Further Part 1 depth: world origins, climate, roast profiles, chemistry, health, café recipes,
milk technique, cleaning, bar operations, menu engineering, price cycles, Indian coffee culture."""
import deep_charts as DC
from deep_base import (CONTENT_W, SKY, bl, h2, numbered, p, side, src, tbl)

W = CONTENT_W


def origins():
    s = [h2("2.12 The world's origins, and how India compares")]
    rows = [["Ethiopia", "Heirloom landraces; washed and natural; 1,800-2,200 m", "Jasmine, bergamot, "
             "lemon (washed); blueberry (natural)", "Birthplace of arabica; huge genetic diversity"],
            ["Kenya", "SL28, SL34, Ruiru 11, Batian; double-fermented washed", "Blackcurrant, grapefruit, "
             "tomato; vivid acidity", "Weekly auctions in Nairobi"],
            ["Colombia", "Castillo, Caturra; two harvests a year", "Caramel, red fruit, balanced",
             "Strong grower federation (FNC)"],
            ["Brazil", "Natural and pulped natural; flat, mechanised farms", "Nuts, chocolate, low acidity",
             "A third of world supply; base of most espresso blends"],
            ["Central America", "Guatemala, Costa Rica, Honduras, Panama; mostly washed", "Chocolate, "
             "citrus, stone fruit", "Panama Gesha sets auction records"],
            ["Vietnam", "Robusta, dry-processed", "Heavy, bitter, woody", "No.1 robusta producer; instant "
             "and blends"],
            ["Indonesia", "Sumatra, Java, Sulawesi; wet-hulled", "Earthy, herbal, cedar, syrupy",
             "Distinctive 'giling basah' process"],
            ["Yemen", "Ancient landraces, natural", "Winey, spicy, dried fruit", "Where the coffee trade began"],
            ["India", "Shade-grown arabica and robusta; washed, natural, monsooned", "Chocolate, spice, mild "
             "acidity, full body", "Leader in fine robusta; Monsooned Malabar"]]
    s.append(tbl(["Origin", "Typical coffees", "Cup profile", "Note"], rows, [64, 160, 150, W - 374],
                 font_size=7.3))
    s.append(p("Indian arabica is rarely as acidic or floral as East African coffee; its strengths are "
               "<b>balance, chocolate and spice, low bitterness and body</b>, which suit espresso and milk "
               "drinks. A café can still offer variety by rotating a guest East African or Latin American "
               "coffee on pour-over, but the commercial heart of an Indian specialty menu can be Indian."))
    s.append(h2("2.13 Climate change and adaptation"))
    s.append(p("Coffee is one of the crops most exposed to climate change. Warmer temperatures push "
               "arabica uphill, erratic rains disrupt flowering, and pests such as the berry borer spread "
               "to higher altitudes. India saw this in 2025, when an unusually long monsoon caused black "
               "rot and berry drop. Adaptation is already under way:"))
    s += bl(["<b>Shade and soil cover</b>: India's two-tier shade buffers heat; estates are adding "
             "mulching and cover crops to hold moisture.",
             "<b>Water management</b>: sprinkler irrigation to substitute for failed blossom showers, farm "
             "ponds and water harvesting.",
             "<b>Resilient planting material</b>: CCRI's rust- and drought-tolerant selections, and renewed "
             "interest in robusta and other hardy species (liberica, excelsa).",
             "<b>Diversification</b>: pepper, cardamom, oranges and agro-tourism (estate stays) spread "
             "income risk.",
             "<b>For buyers</b>: expect more volatile prices and quality; long-term relationships with "
             "estates are the best hedge."])
    return s


def roast_profiles():
    s = [h2("7.11 Starting-point roast profiles")]
    rows = [["Filter (light)", "9-10 min", "7:30-8:00", "1:15-1:30 (15-18%)", "200-205°C", "12-13%",
             "Origin character, acidity, florals"],
            ["Espresso (medium)", "10.5-12 min", "8:15-8:45", "2:00-2:30 (18-22%)", "210-218°C", "14-16%",
             "Sweetness, chocolate, body for milk"],
            ["Kaapi / dark", "12-14 min", "8:30-9:00", "into second crack", "225-232°C", "17-19%",
             "Roasty, bittersweet, low acidity; stands up to chicory and milk"]]
    s.append(tbl(["Style", "Total time", "First crack at", "Development", "Drop temp.", "Weight loss",
                  "Aim"], rows, [74, 50, 56, 82, 52, 50, W - 364], font_size=7.3, center_cols=(1, 2, 3, 4, 5)))
    s.append(p("These are typical starting points for a 3-5 kg drum roaster; every machine, batch size and "
               "bean behaves differently. A toll roaster will run sample roasts of your green coffee, "
               "cup them with you and log the agreed profile, so every later batch can be repeated."))
    return s


def chemistry():
    s = [h2("9.8 What is in your cup: coffee chemistry")]
    rows = [["Polysaccharides (fibre)", "~50%", "~33-38%", "Body; mostly insoluble"],
            ["Lipids (oils)", "15-17% (arabica)", "~17%", "Aroma carrier, crema, mouthfeel"],
            ["Proteins & amino acids", "10-13%", "~7-10%", "Feed the Maillard reaction"],
            ["Sucrose", "6-9% (arabica)", "<0.5%", "Caramelises into sweetness and colour"],
            ["Chlorogenic acids", "5.5-8%", "1-3%", "Bitterness, astringency, antioxidants"],
            ["Caffeine", "1.2-1.5% (robusta 2.2-2.7%)", "~unchanged", "Bitterness, stimulation"],
            ["Trigonelline", "~1%", "~0.2-0.7%", "Breaks down into niacin and aromas"],
            ["Organic acids", "Citric, malic ~1-2%", "Citric, malic, quinic, acetic", "Brightness, "
             "sourness, staleness"],
            ["Melanoidins", "0%", "~20-25%", "Brown colour, body, roasty bitterness"],
            ["Minerals", "~4%", "~4.5%", "Potassium-rich"]]
    s.append(side([tbl(["Component", "Green bean", "Roasted (medium)", "Role in the cup"], rows,
                       [W * 0.17, W * 0.15, W * 0.13, W * 0.16], font_size=7.0)],
                  [p("Roasting turns a dense, starchy seed into a brittle, porous, aromatic one. Sugars "
                     "almost disappear, chlorogenic acids halve or more, and new brown compounds "
                     "(melanoidins) and more than 800 volatile aroma compounds appear."),
                   p("A handful of aroma compounds do most of the work: <b>2-furfurylthiol</b> (the "
                     "'roasted coffee' smell), <b>guaiacols</b> (spicy, smoky), <b>pyrazines</b> "
                     "(nutty, roasty), <b>furaneol</b> (caramel), <b>β-damascenone</b> (fruity, honey), "
                     "<b>2,3-butanedione</b> (buttery) and <b>3-methylbutanal</b> (malty). Many are "
                     "volatile and fragile, which is why freshly ground coffee smells so much better.")],
                  lw=0.62))
    s.append(src("Approximate composition ranges from standard coffee-chemistry references (Clarke & "
                 "Macrae; Illy & Viani) and the PMC10138461 review."))
    s.append(h2("9.9 Coffee and health"))
    s += bl(["<b>Moderate drinking is linked with benefits.</b> Large umbrella reviews of observational "
             "studies associate 3-4 cups a day with lower risks of type 2 diabetes, liver disease and "
             "Parkinson's disease and lower all-cause mortality (association, not proof).",
             "<b>Unfiltered coffee raises cholesterol.</b> Diterpenes (cafestol, kahweol) pass into French "
             "press, Turkish, boiled and, to a lesser degree, espresso and moka coffee; paper filters "
             "remove most of them.",
             "<b>Caffeine limits</b>: up to about 400 mg a day for healthy adults and 200 mg in pregnancy "
             "(EFSA). Caffeine's half-life is about 5 hours, so an evening cold brew affects sleep.",
             "<b>Acrylamide</b> forms early in roasting; levels in coffee are low and regulated by EU "
             "benchmark levels.",
             "<b>What goes in matters</b>: an Indian-style cold coffee with full-cream milk, sugar and ice "
             "cream can carry around 300 kcal; black coffee has almost none. A café can offer lighter "
             "options (less sugar, oat milk, small sizes)."])
    return s


def cafe_recipes():
    s = [h2("10.20 Signature drinks: recipes for a café menu")]
    rows = [["Spanish latte", "Double shot + 25-30 ml condensed milk + 150 ml steamed (or cold) milk",
             "Sweet, creamy; huge in Indian cafés"],
            ["Cardamom (elaichi) latte", "Double shot + 10 ml cardamom syrup + 180 ml steamed milk",
             "Local flavour; works iced"],
            ["Affogato", "Double shot poured over a 60 g scoop of vanilla ice cream", "Dessert menu"],
            ["Espresso tonic", "150 ml tonic over ice; float a double shot; orange peel", "Light, bitter-"
             "sweet summer drink"],
            ["Cold brew with jaggery", "150 ml cold brew + 20 ml jaggery syrup + ice (+ milk)", "Indian twist "
             "on sweet cold brew"],
            ["Vietnamese-style iced", "Phin: 20 g dark robusta : 100 ml over 30 ml condensed milk, on ice",
             "Uses Indian robusta"],
            ["Iced filter kaapi", "40 ml decoction + 150 ml cold milk + sugar or jaggery, shaken with ice",
             "Signature for an Ahmedabad café"],
            ["Mocha", "Double shot + 20 g chocolate sauce + 200 ml steamed milk", "Crowd-pleaser"],
            ["Japanese iced pour-over", "30 g coffee : 300 g hot water brewed onto 200 g ice",
             "Showcases micro-lots cold"],
            ["Indian cold coffee", "Double shot + 200 ml cold milk + 40 g ice cream + sugar, blended",
             "Best-seller; highest ingredient cost"]]
    s.append(tbl(["Drink", "Specification", "Why"], rows, [100, 260, W - 360], font_size=7.3))
    s.append(h2("10.21 Steaming milk and latte art"))
    s += numbered(["Start with cold milk (fridge-cold, about 4°C) filled to the bottom of the jug's spout; "
                   "purge the steam wand.",
                   "<b>Stretch</b>: tip just below the surface, steam on full; let it 'tear paper' gently "
                   "to add air until the jug feels hand-warm (~37°C). Short stretch for a latte, longer for "
                   "a cappuccino.",
                   "<b>Texture</b>: raise the jug so the tip sits a little deeper and the milk spins in a "
                   "whirlpool, folding bubbles into silky microfoam, until 60-65°C (too hot to hold for "
                   "more than a second or two).",
                   "Wipe and purge the wand; tap the jug to burst big bubbles and swirl until glossy.",
                   "<b>Pour</b>: start high to sink milk under the crema, then bring the spout close to the "
                   "surface so foam flows on top: a dot becomes a heart; wiggle for a rosetta; stack for a "
                   "tulip."])
    s.append(h2("10.22 Equipment care schedule"))
    rows = [["After every shot", "Flush group head; knock out and wipe the basket"],
            ["After every milk drink", "Purge and wipe the steam wand"],
            ["Daily (closing)", "Back-flush groups with detergent; soak portafilters, baskets and jugs; "
             "clean grinder chute and hopper; empty and wash drip trays; clean brewers"],
            ["Weekly", "Brush group gaskets and shower screens; grinder-cleaning tablets; deep-clean "
             "batch brewer"],
            ["Monthly", "Check water filter capacity and TDS; inspect gaskets and steam-wand tips"],
            ["Quarterly / annually", "Replace gaskets and shower screens; service boilers and pumps (AMC); "
             "check burr wear; replace RO membranes and remineralisation cartridges as rated"]]
    s.append(tbl(["When", "What"], rows, [100, W - 100], font_size=7.4))
    return s


def bar_ops():
    s = [h2("12.6 Running the bar: workflow and capacity")]
    s.append(side([p("A double espresso takes 25-30 seconds to brew but about a minute of barista time "
                     "with grinding, tamping, milk and hand-off. One barista on a two-group machine "
                     "comfortably makes <b>60-90 drinks an hour</b>; two baristas 120-150. The Part 2 "
                     "base case for Prahladnagar has about 140 bills and 125 drinks a day, so even if a "
                     "fifth of them arrive in the busiest hour (25 drinks), one skilled barista copes. "
                     "Weekend evenings on Sindhu Bhavan Road need two."),
                   p("Speed comes from layout and preparation: a straight line from <b>POS to espresso "
                     "to milk to hand-off</b>, batch-brewed coffee and pre-made cold brew for queues, "
                     "syrups and garnishes prepared off-peak, and a separate pour-over station so manual "
                     "brews do not block the espresso line.")],
                  [tbl(["Peak-hour check", "Prahladnagar", "SBR"],
                       [["Bills per day (Y3, Base)", "140", "170"], ["Drinks per day", "~126", "~174"],
                        ["Peak hour (20%)", "~25 drinks", "~35 drinks"],
                        ["Weekend peak (x1.8)", "~45 drinks", "~63 drinks"],
                        ["Baristas needed at peak", "1-2", "2"]],
                       [W * 0.16, W * 0.13, W * 0.08], font_size=7.3)], lw=0.62))
    s.append(h2("12.7 Menu engineering"))
    s.append(side([tbl(["", "High margin", "Low margin"],
                       [["High popularity", "<b>Stars</b>: promote, protect quality (cappuccino, cold "
                         "brew, Spanish latte)", "<b>Plough-horses</b>: re-price or re-cost (Indian cold "
                         "coffee with ice cream)"],
                        ["Low popularity", "<b>Puzzles</b>: reposition, train staff to suggest (pour-over "
                         "micro-lots, kaapi)", "<b>Dogs</b>: drop or redesign"]],
                       [W * 0.09, W * 0.175, W * 0.175], font_size=7.0)],
                  [p("Menu engineering sorts items by popularity and margin per item. Coffee drinks are "
                     "mostly 'stars'; food items and elaborate cold drinks need closer costing because "
                     "ingredients are a larger share of price."),
                   p("Practical rules: keep the drinks menu to 15-20 items; put the highest-margin "
                     "signatures at the top right; pair coffee with food (food is ~30% of café sales in "
                     "the model); and revisit prices every year, because wages rise faster than menu "
                     "prices in the model's base case.")], lw=0.48))
    return s


def price_cycles():
    s = [h2("6.8 A century of boom and bust")]
    rows = [["1975-77", "Brazil's 'black frost' destroys trees", "New York prices top $3/lb in 1977"],
            ["1962-89", "International Coffee Agreements set export quotas", "Prices held in a band"],
            ["1989", "Quota system collapses", "Prices roughly halve within months"],
            ["2001-02", "Vietnam's robusta expansion + Brazil oversupply", "'Coffee crisis': ~45-50¢/lb, "
             "a century low in real terms"],
            ["2011", "Tight supply, strong demand", "C contract peaks near $3/lb"],
            ["2019", "Big Brazilian crops, weak real", "ICO composite falls below $1/lb (lowest since 2006)"],
            ["2021-25", "Brazil frost and drought, Vietnam drought, falling stocks", "Record >$4.20/lb "
             "(Feb 2025)"],
            ["2026", "Record Brazilian crop expected", "C around $2.85/lb (Oct 2026)"]]
    s.append(tbl(["When", "What happened", "Price outcome"], rows, [60, 230, W - 290], font_size=7.4))
    s.append(p("The pattern repeats: a weather shock in Brazil or Vietnam lifts prices; high prices "
               "encourage planting; three to four years later new trees bear fruit and prices fall. "
               "Growers live with this volatility; a café should simply expect it."))
    return s


def india_culture():
    s = [h2("13.9 Coffee culture in India")]
    s.append(p("India remains a tea country: it drinks more than ten times as much tea as coffee by weight. "
               "Coffee culture developed in two separate streams. In the <b>south</b>, filter kaapi has "
               "been a daily ritual for a century, served at home and in 'darshinis', Udupi restaurants "
               "and the Indian Coffee House co-operatives. In the <b>north and west</b>, coffee meant "
               "instant (Nescafé arrived in the 1960s and became the household name) and, from 1996, "
               "cafés: Café Coffee Day's slogan 'A lot can happen over coffee' captured how cafés became "
               "meeting places for young Indians at a time when there were few others."))
    s.append(p("Since the 2010s a third stream has grown: specialty coffee led by Indian roasters who "
               "name estates, varieties and processes, and international chains that made Rs 300 "
               "drinks normal in big cities. In Gujarat, prohibition and a strong evening food culture "
               "give cafés an unusually central social role, while the state's large office and student "
               "populations in Ahmedabad and Gandhinagar sustain daytime trade."))
    rows = [["IMARC", "India café market", "US$425 m (2025) to US$1.15 bn (2034), ~11% CAGR"],
            ["Grand View Research", "Coffee retail chains", "US$564 m (2023), 8.1% CAGR"],
            ["Expert Market Research", "India coffee market", "US$754 m (2025) to US$1.8 bn (2035), 9.1% "
             "CAGR"],
            ["PIB / Coffee Board", "Out-of-home coffee", "15-20% CAGR to US$2.6-3.2 bn by 2028"],
            ["World Coffee Portal", "Branded coffee-shop outlets", "5,339 (2025) to >10,000 (2030), 13.2% "
             "CAGR"],
            ["NRAI", "Indian food services (all)", "~₹5.69 lakh crore, to ₹7.77 lakh crore by 2028"]]
    s.append(tbl(["Source", "Measure", "Estimate"], rows, [100, 130, W - 230], font_size=7.4))
    s.append(src("Market sizing estimates differ in scope; use them for direction, not precision."))
    exp = DC.bar_chart(["FY2023-24", "FY2024-25", "CY2025"], [("Exports, US$ bn", [1.29, 1.80, 2.06], SKY)],
                       W * 0.45, 120, title="India's coffee export earnings (US$ bn)", fmt="{:.2f}")
    s.append(side([exp], [p("Export earnings jumped as world prices rose: from US$1.29 billion in FY2023-24 "
                            "to a record US$1.8 billion in FY2024-25 and about US$2.06 billion in calendar "
                            "2025, even though export volume fell 4.5% in 2025. Value-added (mostly instant) "
                            "coffee is about 38-41% of exports, a sign of India's strength in soluble "
                            "manufacturing.")], lw=0.47))
    s.append(src("PIB (Nov 2025); export reports (Jan 2026); USDA FAS (May 2026)."))
    return s
