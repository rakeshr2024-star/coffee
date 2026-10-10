"""Part 2: the café financial model. Every number comes from cafe_model/results.json, which is
produced by running Cafe_Financial_Model.xlsx headlessly (cafe_model/export_results.py)."""
import json
import os

from reportlab.platypus import KeepTogether

import build_report as R
import deep_charts as DC
import deep_figs as DF
import deep_more5 as M5
from cafe_model import assumptions as A
from deep_base import (BERRY, CARAMEL, CONTENT_W, GOLD, LEAF, PLUM, ROAST, SAFFRON, SKY, TEAL, HX,
                       P, PageBreak, Spacer, bl, chapter, figc, h2, kpi_tiles, lead, money, note, p,
                       pct, ps, side, src, tbl, yrs)

W = CONTENT_W
HERE = os.path.dirname(os.path.abspath(__file__))
RES = json.load(open(os.path.join(HERE, "cafe_model", "results.json")))
SC = A.SCENARIOS
MODELS = RES["models"]
GRID = RES["grid"]
FY = [f"FY{int(y) % 100:02d}" for y in RES["years"]]
MCOL = {"A": TEAL, "B": SKY, "C": CARAMEL, "D": PLUM}
SHORT = {"Prahladnagar": "PN", "Sindhu Bhavan Road": "SBR", "GIFT City": "GIFT", "Sanand": "SAN"}


def m(fid, scen="Base"):
    return MODELS[fid]["scenarios"][scen]


def ser(fid, key, scen="Base"):
    return m(fid, scen)["series"][key]


def sc(fid, key, scen="Base"):
    return m(fid, scen)["scalars"][key]


def num(v, d=1):
    return "–" if v is None or (isinstance(v, (int, float)) and abs(v) < 0.05 and d <= 1) else money(v, d)


def irr_txt(v):
    return pct(v) if isinstance(v, (int, float)) else "n.m."


def label(fid):
    mm = MODELS[fid]
    return f"{fid}. {mm['name']}"


# =============================================================================== 13. brief & model
def ch14():
    s = chapter("c14", 14, "The brief and the model", "What we set out to decide, and how the Excel "
                "model is built", ROAST)
    s.append(lead("The question: should you open a specialty café in Prahladnagar, and if so how: rented "
                  "or owned premises, which roasting route, which beans? And is there a better spot in "
                  "Ahmedabad or Sanand? Part 2 answers with a full three-statement model and an FCFF "
                  "valuation for every combination."))
    s.append(h2("14.1 What the model decides"))
    rows = [["Location", "Prahladnagar (brief), Sindhu Bhavan Road, GIFT City, Sanand", "4"],
            ["Premises", "Rent (lease + deposit) or own (buy the unit, 60% loan against property)", "2"],
            ["Roasting route", "Buy roasted beans, toll-roast your own green coffee, or run an in-house "
             "3 kg roastery that also sells wholesale", "3"],
            ["Bean mix", "Value (commodity arabica/robusta), Specialty, Premium (40% micro-lot), "
             "House blend (recommended 15/70/15)", "4"],
            ["Scenario", "Best, Base, Worst: demand ramp, footfall, price growth, green prices, capex "
             "overrun, wholesale volume", "3"]]
    s.append(tbl(["Decision", "Options", "#"], rows, [80, W - 110, 30], font_size=7.6, center_cols=(2,)))
    s.append(p("That is 96 combinations, each in three scenarios. Twenty named configurations are "
               "compared side by side, and four are examined in depth in Chapter 18."))
    s.append(h2("14.2 How the workbook is built"))
    flow = [("Inputs", "Switches (drop-downs), Best/Base/Worst drivers, all operating assumptions"),
            ("Libraries", "Locations, Sourcing (beans & routes), Capex (equipment, property, funding)"),
            ("Model", "Revenue, COGS, opex, fixed-asset, tax, working-capital, debt and equity schedules"),
            ("Statements", "Income statement, cash flow, balance sheet (checks to zero every year)"),
            ("DCF", "Unlevered tax, FCFF, WACC, terminal value, NPV, IRRs, payback"),
            ("Scenarios", "Override panel and live data tables: scenarios, configurations, sensitivities")]
    s.append(figc(DC.flow(flow, W, 76, per_row=6, colors_=[R.SKY, R.SKY, ROAST, ROAST, PLUM, PLUM],
                          sub_size=5.9, head_size=7.0),
                  "Figure 14.1. Workbook flow, following the CFI modelling guidelines and the "
                  "'3-Statement Model' template structure."))
    s.append(bl(["<b>Conventions</b> (CFI guidelines): blue = input, black = formula, green = link to "
                 "another sheet; one font; units column on every row; every input entered once; "
                 "statements contain links only; a circularity switch on the Cover (interest on "
                 "opening balances by default).",
                 "<b>Timeline</b>: Y0 = FY27 (fit-out and pre-opening, ending 31 March 2027), then ten "
                 "operating years FY28-FY37. Annual periods, ₹ lakh.",
                 "<b>Valuation</b>: free cash flow to the firm (FCFF) discounted at WACC, with a Gordon-"
                 "growth terminal value at Y10 (4% nominal). Equity IRR uses free cash flow to equity. "
                 "For owned premises the terminal value is split: operations after a notional market "
                 "rent, plus the property's resale value net of selling costs and capital-gains tax.",
                 "<b>Funding rule</b>: all-equity if the capital need is ₹15 lakh or less (per the "
                 "brief); otherwise a term loan of 50% of capex at 11% over 5 years (rented) or 60% of "
                 "capex and property at 10% over 10 years (owned). A cash-credit line covers shortfalls.",
                 "<b>Checks</b>: balance sheet balances, cash never negative, sources equal uses, bean mixes "
                 "add to 100%, WACC above growth. All pass for every configuration exported here."]))
    s.append(h2("14.3 Inside the schedules: the key formulas"))
    rows = [["Bills per day", "Steady-state bills x scenario footfall x bean-mix footfall effect x ramp-up x "
             "volume index, capped at seats x 6 turns / dine-in share"],
            ["Revenue", "Bills per day x operating days x average bill (grows with menu-price increases); "
             "split into beverages, food and retail beans; plus wholesale beans if in-house"],
            ["Coffee cost", "Coffee kg = beverages x 85% x 18 g; cost per kg = green cost per kg roasted x "
             "green-price index + roasting-route conversion cost x inflation"],
            ["Other COGS", "Milk and inputs per beverage; packaging per takeaway/delivery bill; food at 38%; "
             "retail beans at route-specific cost"],
            ["Staff", "Roster x location staffing factor x (1 + 15% load) x wage growth x volume scale-up"],
            ["Occupancy", "Area x rent per sqft x escalation (rented) or property tax (owned); CAM both"],
            ["Capex & depreciation", "Item list x site quantities x (1 + overrun); straight-line book "
             "depreciation by class and vintage; WDV tax depreciation; deferred tax on the difference"],
            ["Tax", "Book profit + book depreciation - tax depreciation; losses carried forward; 25.17%"],
            ["Working capital", "Receivables (delivery 7 days, wholesale 30), inventory (18 days; green "
             "stock 40 days if roasting own coffee), payables (15 days)"],
            ["Debt", "Term loan sized by the funding rule, equal principal repayments; cash credit draws "
             "automatically if cash would fall below the minimum"],
            ["FCFF and value", "EBIT - unlevered tax + depreciation - capex - change in working capital - "
             "deposit; discounted at WACC; Gordon terminal value at Y10"]]
    s.append(tbl(["Schedule", "Logic"], rows, [96, W - 96], font_size=7.3))
    s.append(note("Using the Excel file", [
        "Open <b>Cafe_Financial_Model.xlsx</b>. On <b>Inputs</b>, pick location, premises, roasting, "
        "mix and scenario; the <b>Dashboard</b> updates instantly.",
        "Change any blue cell: rents on <b>Locations</b>, bean prices and mix shares on <b>Sourcing</b>, "
        "equipment on <b>Capex</b>, salaries on <b>Inputs</b>.",
        "The <b>Scenarios</b> sheet's data tables re-run the whole model for every configuration and "
        "sensitivity; <b>Configs</b> lets you define your own 20 combinations. If Excel is set to "
        "'automatic except tables', press F9."], TEAL))
    return s


# =============================================================================== 14. location
SCREEN = [  # hub, footfall, spend, competition (10 = little), rent affordability, growth, comment
    ("GIFT City", 6, 8, 9, 6, 9, "Captive, fast-growing finance workforce; few quality cafés"),
    ("Sindhu Bhavan Road", 9, 9, 5, 4, 7, "Premier F&B street; highest footfall and spend"),
    ("Sanand", 4, 5, 9, 9, 8, "Semiconductor & auto boom; cheap space; first mover"),
    ("Bopal / Shela", 5, 6, 7, 8, 7, "Young western suburbs; good back-up option"),
    ("SG Highway / Thaltej", 8, 8, 4, 5, 6, "Malls and offices; crowded with chains"),
    ("Prahladnagar", 7, 7, 4, 6, 6, "Office belt + upscale homes; chains already present"),
    ("Vastrapur / IIM Road", 7, 7, 5, 5, 5, "Students and residents; mature"),
    ("CG Road / Navrangpura", 7, 6, 5, 6, 5, "Older commercial core; value-seeking crowd")]
WEIGHTS = [0.30, 0.20, 0.15, 0.15, 0.20]


def ch15():
    s = chapter("c15", 15, "Where: choosing the hub", "Screening Ahmedabad's café hubs and the four "
                "sites modelled", SKY)
    s.append(p("Eight hubs were screened on five criteria (scores 1-10, author's assessment from rent "
               "listings, competitor mapping and employment news). Weights: footfall 30%, spending "
               "power 20%, competition 15% (10 = little), rent affordability 15%, growth 20%."))
    rows = []
    for hub, *sc_, cm in SCREEN:
        tot = sum(a * b for a, b in zip(sc_, WEIGHTS))
        rows.append([hub] + [float(x) for x in sc_] + [round(tot, 1), cm])
    rows.sort(key=lambda r: -r[6])
    s.append(tbl(["Hub", "Footfall", "Spend", "Competition", "Rent", "Growth", "Score", "Comment"], rows,
                 [86, 40, 36, 52, 34, 38, 36, W - 322], score_cols=(1, 2, 3, 4, 5, 6), font_size=7.4))
    s.append(p("<b>Shortlist.</b> GIFT City and Sindhu Bhavan Road score clearly above Prahladnagar. "
               "Sanand scores well on growth and cost but poorly on today's footfall; it is modelled "
               "because the semiconductor build-out (Micron's plant opened in February 2026; six "
               "approved projects in Gujarat with about 50,000 jobs) could make it a first-mover "
               "opportunity and a cheap base for a roastery. Prahladnagar is modelled as the brief's "
               "starting point. Bopal/Shela is the best unmodelled alternative."))
    s.append(h2("15.1 The four sites, as modelled"))
    rows = []
    for key, labl, unit, vals, _note in A.LOCATION_ROWS:
        f = (lambda v: f"{v:.0%}" if v < 1 else f"{v:,.0f}") if unit in ("%", "% p.a.") else (
            (lambda v: f"{v:.2f}") if unit == "x" else (lambda v: f"{v:,.0f}"))
        rows.append([f"{labl} ({unit})"] + [f(v) for v in vals])
    s.append(tbl(["Input"] + A.LOCATIONS, rows, [168] + [(W - 168) / 4] * 4, font_size=7.3,
                 center_cols=(1, 2, 3, 4)))
    s.append(src("Rents and prices: 99acres, MagicBricks, housing.com listings (Oct 2026). Demand inputs "
                 "(bills/day, average bill) are judgement, triangulated with chain revenue per store "
                 "(Starbucks India ~₹2.7 cr) and specialty-café spend levels in Ahmedabad listings."))
    s.append(h2("15.2 What the sites imply"))
    rows = []
    for loc in A.LOCATIONS:
        L = RES["locations"][loc]
        r1, r2 = L["Rent|Toll roasting"], L["Own|Toll roasting"]
        rows.append([loc, num(r1["y3_rev"]), pct(r1["y3_margin"]), f"{r1['be_y3']:.0f}",
                     num(r1["u_tot"]), num(r2["u_tot"]), num(r1["npv"]), num(r2["npv"]),
                     irr_txt(r1["irr_p"])])
    s.append(tbl(["Base case, toll roasting, House blend", "Y3 revenue", "Y3 EBITDA %", "Break-even "
                  "bills/day", "Capital: rent", "Capital: own", "NPV: rent", "NPV: own", "IRR: rent"],
                 rows, [118, 50, 50, 52, 50, 50, 46, 46, W - 462], font_size=7.3,
                 center_cols=(1, 2, 3, 4, 5, 6, 7, 8)))
    s.append(src("Model outputs, ₹ lakh. Capital = total capital requirement including pre-opening "
                 "costs, deposit and a three-month ramp-up cash reserve."))
    locs = [SHORT[x] for x in A.LOCATIONS]
    y3 = [RES["locations"][x]["Rent|Toll roasting"]["y3_rev"] for x in A.LOCATIONS]
    rent = [ser_loc_rent(x) for x in A.LOCATIONS]
    be = [RES["locations"][x]["Rent|Toll roasting"]["be_y3"] for x in A.LOCATIONS]
    bills = dict((r[0], r[3]) for r in A.LOCATION_ROWS)["bills_ss"]
    s.append(side([DC.bar_chart(locs, [("Y3 revenue", y3, CARAMEL), ("Y1 rent + CAM", rent, BERRY)], W * 0.49,
                                150, title="Revenue vs occupancy cost (₹ lakh, Base)", fmt="{:,.0f}")],
                  [DC.bar_chart(locs, [("Steady-state bills/day", bills, TEAL),
                                       ("Break-even bills/day (Y3)", be, BERRY)],
                                W * 0.49, 150, title="Demand vs break-even (bills per day)", fmt="{:,.0f}")],
                  lw=0.5))
    s.append(P("Figure 15.1. Sindhu Bhavan Road pays the most rent but earns far more; Sanand's break-even "
               "is close to its expected demand, leaving no margin for error.", R.CAPTION))
    rows = [["Prahladnagar", "Starbucks, Third Wave, Slay, The Dark Roast, Great Shakes", "High",
             "Office lunch and evening; strong delivery"],
            ["Sindhu Bhavan Road", "Many specialty and dessert cafés; new openings every year", "Very high",
             "Evening and weekend destination crowds"],
            ["GIFT City", "Few quality cafés; tenders for food zones", "Low", "Weekday office peaks; "
             "batch-brew and pre-order demand"],
            ["Sanand", "Mostly local tea stalls and QSR", "Very low", "Shift workers and managers; price-"
             "sensitive"]]
    s.append(tbl(["Site", "Competition today", "Intensity", "Demand pattern"], rows, [90, 220, 56, W - 366],
                 font_size=7.3))
    for loc in A.LOCATIONS:
        s.append(P(f"<b>{loc}.</b> {A.LOCATION_PROFILE[loc]}", R.BODY_SM))
    return s


def ser_loc_rent(loc):
    vals = dict((r[0], r[3]) for r in A.LOCATION_ROWS)
    i = A.LOCATIONS.index(loc)
    return vals["area"][i] * (vals["rent_psf"][i] + vals["cam_psf"][i]) * 12 / 1e5



# =============================================================================== 15. inputs
def ch16():
    s = chapter("c16", 16, "Inputs and assumptions", "Drivers, menu, beans, people, costs, capex, funding "
                "and valuation inputs (all editable in the workbook)", R.ROAST)
    s.append(h2("16.1 Scenario drivers"))
    D = A.DRIVERS
    rows = []
    for key, (labl, unit, vals) in D.items():
        for sname, v in zip(SC, vals):
            f = (lambda x: f"{x:.0%}") if unit != "x" else (lambda x: f"{x:.2f}")
            rows.append([labl if sname == "Best" else "", sname] + [f(x) for x in v[:5]] + [f(v[9])])
    for key, (labl, unit, vals) in A.SINGLE_DRIVERS.items():
        f = (lambda x: f"{x:.2f}") if unit == "x" else ((lambda x: f"{x:.0%}") if unit == "%" else
                                                        (lambda x: f"{x:,.0f}"))
        rows.append([f"{labl} ({unit})", " / ".join(SC)] + [" / ".join(f(v) for v in vals)] + [""] * 5)
    s.append(tbl(["Driver", "Case", "Y1", "Y2", "Y3", "Y4", "Y5", "Y10"], rows,
                 [170, 60] + [(W - 230) / 6] * 6, font_size=7.0, center_cols=(2, 3, 4, 5, 6, 7),
                 bold_first=False))
    s.append(p("<b>Base</b> assumes a café reaches 65% of steady-state bills in year 1 and 85% in year 2, "
               "raises prices 5% a year from year 2 and grows volume 2.5% a year from year 4. "
               "<b>Worst</b> is a struggling café: 82% of expected footfall, slow ramp to 95%, prices "
               "+3.5%, green coffee 25% dearer and capex 15% over budget. <b>Best</b> is a hit: 115% "
               "footfall and a fast ramp."))
    s.append(h2("16.2 Revenue and menu"))
    Rv = A.REVENUE
    rows = [["Revenue mix", f"Beverages {Rv['bev_share']:.0%}, retail beans {Rv['retail_share']:.0%} "
             f"(+{Rv['own_label_uplift']:.0%} with own-label beans), food = remainder (30-32%)"],
            ["Beverages", f"Average price ₹{Rv['bev_price']} (FY28); {Rv['coffee_share']:.0%} contain coffee; "
             f"{Rv['grams']} g per coffee drink; milk & other inputs ₹{Rv['milk_other']} per drink"],
            ["Takeaway & delivery", f"Takeaway {Rv['takeaway_share']:.0%} of bills, delivery 6-15% of sales "
             f"by site; packaging ₹{Rv['pack_per_bill']} per bill; aggregator commission 25% of "
             "delivery sales"],
            ["Food & retail", f"Food cost {Rv['food_cogs']:.0%} of food sales; bought-in retail bags at "
             f"{Rv['resale_margin']:.0%} margin; own-label retail at mix-specific prices"],
            ["Capacity", f"Up to {A.CAPACITY['max_turns']:.0f} seat turns a day (dine-in); demand above "
             "this is capped"],
            ["Bean-mix effects", "Average bill vs Specialty: Value -10%, Premium +5%, House +2%. Footfall: "
             "Value +5%, Premium -5%. Wholesale price per kg: Value ₹900, Specialty ₹1,450, Premium "
             "₹2,300, House ₹1,700"]]
    s.append(tbl(["Item", "Assumption"], rows, [90, W - 90], font_size=7.5))
    s.append(h2("16.3 Beans, mixes and roasting routes"))
    rows = []
    for i, gname in enumerate(A.GREEN_TYPES):
        rows.append([gname, f"₹{A.GREEN_PRICE[i]:,}", f"₹{A.WHOLESALE_ROASTED[i]:,}"] +
                    [f"{A.MIX_SHARES[mx][i]:.0%}" if A.MIX_SHARES[mx][i] else "–" for mx in A.MIXES])
    srcd = RES["sourcing"]
    rows.append(["Blended green price, ₹/kg", "", ""] + [f"₹{v:,.0f}" for v in srcd["green"]])
    rows.append(["Roasted cost: buy roasted", "", ""] + [f"₹{v:,.0f}" for v in srcd["cost_buy"]])
    rows.append(["Roasted cost: toll roasting", "", ""] + [f"₹{v:,.0f}" for v in srcd["cost_toll"]])
    rows.append(["Roasted cost: in-house (variable)", "", ""] + [f"₹{v:,.0f}" for v in srcd["cost_inh"]])
    rows.append(["Coffee cost per 18 g shot (toll)", "", ""] + [f"₹{v:,.1f}" for v in srcd["cup_cost"]])
    s.append(tbl(["Green coffee type", "Green ₹/kg", "Roasted, bought"] + A.MIXES, rows,
                 [150, 50, 56] + [(W - 256) / 4] * 4, font_size=7.3, center_cols=(1, 2, 3, 4, 5, 6)))
    S = A.SOURCING
    s.append(p(f"Roast loss {S['shrink']:.0%}; toll fee ₹{S['toll_fee']}/kg; freight ₹{S['freight']}/kg; "
               f"in-house variable roasting ₹{S['inhouse_var']}/kg (LPG, power, bags) plus a roaster on "
               "₹32,000 a month, AMC and 150 sqft of extra space. Green-coffee costs move with the "
               "scenario's price index (+3% a year in Base); roasting and packing costs with inflation."))
    s.append(src("Coffee Board indicative prices (Oct 2026); Indian green-coffee traders and roaster "
                 "price lists; Part 1, Chapter 6."))
    s.append(h2("16.4 People and operating costs"))
    staff_rows = [[r, str(hc), f"₹{sal:,}", "In-house only" if flag else ""] for r, hc, sal, flag in A.STAFF]
    O = A.OPEX
    op_rows = [["Payroll load (PF, ESI, bonus, meals)", f"{O['staff_load']:.0%}"],
               ["Wage growth", f"{O['wage_growth']:.0%} a year"],
               ["Electricity", f"{O['kwh_psf']:.0f} kWh/sqft/month at ₹{O['tariff']}/kWh"],
               ["Gas, water, cleaning", f"₹{O['gas_water_m']:,}/month"],
               ["Marketing", f"{O['mkt_y1']:.0%} of sales in Y1, then {O['mkt']:.0%}"],
               ["Repairs + AMC", f"{O['rm_pct']:.1%} of sales + ₹{O['amc'] / 1000:.0f}k/yr"],
               ["Card/UPI fees", f"{O['payment']:.1%} of dine-in sales"],
               ["Admin, accounts, insurance", f"₹{O['admin_fixed'] / 1e5:.0f} lakh/yr"],
               ["Rent escalation", f"{O['rent_esc']:.0%} a year; CAM by site"],
               ["Pre-opening", "2 months' rent, 1 month payroll, ₹3 lakh launch, ₹1.5 lakh licences"]]
    s.append(side([tbl(["Role", "#", "₹/month", ""], staff_rows, [W * 0.22, 18, 52, W * 0.46 - 70 - W * 0.22 + 18],
                       font_size=7.2, center_cols=(1,)),
                   ps("Headcount scales by a site staffing factor (SBR 1.2, GIFT 0.95, Sanand 0.9) and by "
                      "half of any volume above steady state. Gujarat's minimum wage is about ₹13,300-13,900 "
                      "a month (April 2026); specialty baristas earn ₹11,000-23,000.")],
                  [tbl(["Cost line", "Assumption"], op_rows, [W * 0.24, W * 0.26], font_size=7.2)], lw=0.48))
    s.append(h2("16.5 Capex and funding"))
    cx = m("C")["capex"]
    cxa = m("A")["capex"]
    rows = []
    for key, item, basis, val, cls in A.CAPEX_ITEMS:
        if cx[key] or cxa[key]:
            rows.append([item, cls, num(cx[key]), num(cxa[key])])
    rows.append(["In-house roastery adds (any site)", "Roastery", "₹13.0 lakh + 150 sqft fit-out", ""])
    rows.append(["Total café capex incl. 5% contingency", "", num(sc("C", "u_capex")), num(sc("A", "u_capex"))])
    s.append(tbl(["Item", "Asset class", "Prahladnagar ₹ lakh", "SBR ₹ lakh"], rows,
                 [W - 200, 70, 65, 65], font_size=7.2, center_cols=(2, 3)))
    s.append(p("Book depreciation is straight-line (interiors 9 years, equipment 8, furniture 8, IT 4, "
               "roaster 10, building 60; land none). Tax depreciation uses Income-tax Act WDV block rates "
               "(furniture & fittings 10%, plant & machinery 15%, computers 40%, buildings 10%), which "
               "creates a deferred-tax balance. Maintenance capex is 1.5% of sales a year, with a 25% "
               "refurbishment of interiors and furniture in year 6. Corporate tax is 25.17% (s.115BAA) "
               "with losses carried forward."))
    rows = []
    for fid in ("C", "A", "D"):
        q = m(fid)["scalars"]
        rows.append([label(fid), num(q["u_capex"]), num(q["u_prop"]), num(q["u_preop"]), num(q["u_dep"]),
                     num(q["u_cash"]), num(q["u_tot"]), num(q["s_debt"]), num(q["s_eq"]),
                     pct(q["gearing"], 0)])
    s.append(tbl(["Sources & uses, Base (₹ lakh)", "Café capex", "Property", "Pre-opening", "Deposit",
                  "Cash reserve", "Total need", "Loan", "Equity", "Debt %"], rows,
                 [130, 42, 42, 44, 38, 42, 44, 36, 40, W - 458], font_size=7.0,
                 center_cols=(1, 2, 3, 4, 5, 6, 7, 8, 9)))
    rows = []
    for loc in A.LOCATIONS:
        L = RES["locations"][loc]
        rows.append([loc] + [num(L[f"{pr}|{ro}"]["u_tot"]) for pr in A.PROPERTY for ro in A.ROASTING])
    s.append(tbl(["Total capital need (₹ lakh, Base)"] + [f"{pr}: {ro.split()[0]}" for pr in A.PROPERTY
                                                          for ro in A.ROASTING], rows,
                 [120] + [(W - 120) / 6] * 6, font_size=7.2, center_cols=(1, 2, 3, 4, 5, 6)))
    s.append(src("House blend. Capital = capex + property + pre-opening + deposit + cash reserve."))
    s.append(h2("16.6 Cost of capital"))
    rows = []
    for fid in ("A", "B", "C", "D"):
        q = m(fid)["scalars"]
        rows.append([label(fid), pct(q["w_wd"], 0), f"{q['w_bl']:.2f}", pct(q["ke"]), pct(q["loan_rate"]),
                     pct(q["wacc"]), pct(q["g_used"]), pct(q["tv_share"], 0)])
    s.append(tbl(["Model", "Debt / capital", "Relevered beta", "Cost of equity", "Loan rate", "WACC",
                  "Terminal g", "TV share of value"], rows, [150] + [(W - 150) / 7] * 7, font_size=7.3,
                 center_cols=(1, 2, 3, 4, 5, 6, 7)))
    s.append(p("Cost of equity = risk-free 7.29% (10-year G-sec, 8 Oct 2026) + relevered beta × India "
               "equity risk premium 7.08% (Damodaran, January 2026) + a 5% size and single-outlet "
               "premium, starting from an unlevered beta of 0.80. The resulting 20-24% cost of equity "
               "and 15-16% WACC are deliberately demanding for a first café."))
    return s


# =============================================================================== 16. comparisons
def ch17():
    s = chapter("c17", 17, "Comparing the configurations", "Twenty combinations of site, premises, "
                "roasting and beans, in three scenarios", PLUM)
    rows = []
    for name, loc, prop, roast, mix in A.CONFIGS:
        k = GRID[name]["Base"]
        rows.append([name, f"{loc} | {prop} | {roast} | {mix}", num(k["k_tcr"]), num(k["npv"]),
                     irr_txt(k["irr_p"]), irr_txt(k["irr_e"]), yrs(k["payback"]), pct(k["y3_margin"]),
                     f"{k['be_y3']:.0f}", num(GRID[name]["Best"]["npv"]), num(GRID[name]["Worst"]["npv"])])
    s.append(tbl(["Config", "Site | premises | roasting | mix", "Capital", "NPV", "Proj. IRR", "Eq. IRR",
                  "Payback", "Y3 EBITDA", "BE bills", "NPV Best", "NPV Worst"], rows,
                 [56, 124, 34, 34, 36, 36, 38, 38, 30, 38, W - 464], font_size=6.8, head_size=6.8,
                 center_cols=(2, 3, 4, 5, 6, 7, 8, 9, 10)))
    s.append(src("Model outputs, ₹ lakh, Base scenario unless stated. Payback counted from opening "
                 "(start of Y1). BE bills = break-even bills per day in Y3."))
    names = [c[0] for c in A.CONFIGS]
    npvs = [GRID[n]["Base"]["npv"] for n in names]
    cols = [{"Prahladnagar": CARAMEL, "Sindhu Bhavan Road": TEAL, "GIFT City": SKY, "Sanand": BERRY}[c[1]]
            for c in A.CONFIGS]
    pts = [(n, GRID[n]["Base"]["k_tcr"], GRID[n]["Base"]["irr_p"] if isinstance(GRID[n]["Base"]["irr_p"], float)
            else 0, max(GRID[n]["Base"]["npv"], 5) / 6, cols[i]) for i, n in enumerate(names)]
    s.append(KeepTogether([side([DC.hbar_chart(names, npvs, W * 0.47, 250, title="Project NPV, Base (₹ lakh)",
                                              colors_=cols, label_w=70, lab_size=6.4, val_size=6.0)],
                               [DF_bubble(pts)], lw=0.48),
                          P("Figure 17.1. NPV by configuration (left) and capital needed versus project IRR (right; "
               "bubble size = NPV). Teal = Sindhu Bhavan Road, blue = GIFT City, caramel = Prahladnagar, "
               "red = Sanand.", R.CAPTION)]))
    s.append(h2("17.1 What drives the ranking"))
    s.append(bl(["<b>Location dominates.</b> With the same roasting route and beans, NPV ranges from "
                 f"about ₹{GRID['SAN-R-Toll']['Base']['npv']:.0f} lakh (Sanand) to "
                 f"₹{GRID['SBR-R-Toll']['Base']['npv']:.0f} lakh (Sindhu Bhavan Road). Footfall and "
                 "average bill matter far more than rent: SBR pays the highest rent and still wins.",
                 "<b>Toll roasting beats both alternatives at every site.</b> It is cheaper per kilo "
                 "than buying roasted beans (₹1,308 against ₹1,665/kg for the Specialty mix) and lifts "
                 "retail-bean margins, without the fixed costs of a roastery.",
                 "<b>The House blend wins on beans</b>: a 15% micro-lot share supports a slightly higher "
                 "average bill at a coffee cost of about ₹27 a shot. Value beans save cost but lose more "
                 "in price and image; Premium (40% micro-lot) costs more than it earns.",
                 "<b>Owning raises NPV at the best sites but cuts returns.</b> It roughly triples the "
                 "capital needed (2.3-3.2 times), cuts the project IRR by about a third and depends on property "
                 "appreciation.",
                 "<b>Sanand is not ready.</b> It is NPV-negative in the Base case and positive only if "
                 "the Best case's footfall arrives."]))
    t = RES["tables_default"]
    rows = []
    for i, loc in enumerate(A.LOCATIONS):
        rows.append([loc, num(t["locprop_tcr"]["values"][i][0]), num(t["locprop_tcr"]["values"][i][1]),
                     num(t["locprop_npv"]["values"][i][0]), num(t["locprop_npv"]["values"][i][1]),
                     irr_txt(t["locprop_irr"]["values"][i][0]), irr_txt(t["locprop_irr"]["values"][i][1]),
                     irr_txt(t["locprop_eirr"]["values"][i][0]), irr_txt(t["locprop_eirr"]["values"][i][1])])
    s.append(h2("17.2 Rent versus own"))
    s.append(tbl(["Toll roasting, House blend, Base", "Capital: rent", "Capital: own", "NPV: rent",
                  "NPV: own", "IRR: rent", "IRR: own", "Eq. IRR: rent", "Eq. IRR: own"], rows,
                 [120] + [(W - 120) / 8] * 8, font_size=7.2, center_cols=(1, 2, 3, 4, 5, 6, 7, 8)))
    ro = t["rentown"]["values"]
    inc = [b - a for a, b in zip(ro[0][:11], ro[1][:11])]
    s.append(side([DC.bar_chart(FY, [("Own minus rent", inc, PLUM)], W * 0.5, 140,
                                title="Prahladnagar: extra cash flow from buying (₹ lakh)",
                                sub="Y10 includes the difference in terminal values", fmt="{:,.0f}",
                                show_vals=False, cat_size=6.0)],
                  [p("Buying means paying about ₹1.7-2.8 crore more up front to save rent, and getting the "
                     "property back at the end. For Prahladnagar the <b>incremental IRR of buying is "
                     f"about {incremental_irr(inc):.1%}</b>: above the 10% cost of the property loan, but well "
                     "below the ~20% cost of equity. At Sindhu Bhavan Road and GIFT City, faster "
                     "appreciation makes owning add NPV."),
                   p("But owning concentrates two risks (café and property) in one asset, ties up "
                     "₹1.0-1.8 crore of equity, and makes the café harder to relocate if the street "
                     "falls out of fashion. <b>Verdict: rent first</b>; consider buying only for a "
                     "proven site with spare capital.")], lw=0.5))
    s.append(h2("17.3 Roasting route and bean mix"))
    rm = t["roastmix_npv"]["values"]
    rmm = t["roastmix_m"]["values"]
    rows = [[A.ROASTING[i]] + [num(v) for v in rm[i]] + [pct(v) for v in rmm[i]] for i in range(3)]
    s.append(tbl(["Prahladnagar, rented, Base"] + [f"NPV {mx}" for mx in A.MIXES] +
                 [f"Y3 margin {mx}" for mx in A.MIXES], rows, [110] + [(W - 110) / 8] * 8, font_size=7.0,
                 center_cols=(1, 2, 3, 4, 5, 6, 7, 8)))
    w = MODELS["A"]["tables"]["whs_roast"]
    wc = MODELS["C"]["tables"]["whs_roast"]
    xs = [f"{d} kg" for d in w["down"]]
    s.append(side([DC.line_chart(xs, [("SBR in-house", [r[1] for r in w["values"]], TEAL),
                                      ("SBR toll", [r[0] for r in w["values"]], TEAL, True),
                                      ("PN in-house", [r[1] for r in wc["values"]], CARAMEL),
                                      ("PN toll", [r[0] for r in wc["values"]], CARAMEL, True)],
                                 W * 0.52, 150, title="When does an in-house roastery pay? NPV (₹ lakh)",
                                 sub="Wholesale beans sold per month at maturity", zero=True)],
                  [p("An in-house roastery adds about ₹13 lakh of equipment, a roaster's salary, AMC and "
                     "extra space. Roasting the café's own needs (about 1,500 kg a year including retail "
                     "bags) saves only ₹145/kg against toll roasting, which does not cover those fixed "
                     "costs."),
                   p(f"It pays once the roastery also sells <b>about "
                     f"{min(roastery_breakeven(w), roastery_breakeven(wc)):.0f}-"
                     f"{max(roastery_breakeven(w), roastery_breakeven(wc)):.0f} kg a month wholesale</b> to offices, hotels and other "
                     "cafés: the crossover point in the chart. That makes it a phase-two decision for "
                     "a brand with several outlets and wholesale accounts, not a launch decision.")],
                  lw=0.54))
    s.append(h2("17.4 Roasting route and bean mix at Sindhu Bhavan Road"))
    ta = MODELS["A"]["tables"]
    s.append(side([DC.heat_table(A.ROASTING, A.MIXES, ta["roastmix_npv"]["values"], lambda v: f"{v:,.0f}", 52,
                                 80, corner="SBR NPV ₹ lakh", mid=100, font=6.8, bold_cell=(1, 3))],
                  [DC.heat_table(A.ROASTING, A.MIXES, ta["roastmix_m"]["values"], lambda v: f"{v:.1%}", 52, 80,
                                 corner="SBR Y3 EBITDA %", mid=0.19, font=6.8, bold_cell=(1, 3))], lw=0.5))
    s.append(p("At Sindhu Bhavan Road the ranking is the same as at Prahladnagar: toll roasting with the House "
               "blend is best (boxed). Premium beans earn more per bill but lose footfall; Value beans lose "
               "price. In-house roasting narrows the gap only with the Premium mix, where wholesale margins "
               "per kilo are highest."))
    s.append(h2("17.5 Every configuration in every scenario"))
    rows = []
    for name, *_ in A.CONFIGS:
        rows.append([name] + [GRID[name][sn]["npv"] for sn in SC] + [GRID[name][sn]["irr_e"] for sn in SC])
    vals = [[r[1], r[2], r[3]] for r in rows]
    evals = [[r[4], r[5], r[6]] for r in rows]
    s.append(side([DC.heat_table([r[0] for r in rows], SC, vals, lambda v: f"{v:,.0f}", 40, 70,
                                 corner="NPV ₹ lakh", mid=0, font=6.6)],
                  [DC.heat_table([r[0] for r in rows], SC, evals, lambda v: f"{v:.0%}", 40, 70,
                                 corner="Equity IRR", mid=0.20, font=6.6)], lw=0.5))
    s.append(P("Figure 17.2. Every configuration in every scenario: NPV (left) and equity IRR (right; "
               "n.m. = not meaningful because cash flows never turn positive).", R.CAPTION))
    s.append(p("The spread between scenarios is wide for every configuration: a single café is a "
               "high-variance bet. The <b>Worst case</b> (82% of expected footfall with a slow "
               "ramp) makes every configuration NPV-negative, because a café that never "
               "reaches break-even keeps losing money as wages outgrow prices. GIFT City has the mildest "
               "Worst case, thanks to its growing captive workforce; Sindhu Bhavan Road has the best Best "
               "case."))
    s.append(p("In practice nobody runs a loss-making café for ten years. The model therefore also "
               "reports the <b>cash lost if the café is shut at the end of year 3</b> (after "
               "equipment resale, deposit refund and working-capital release): about "
               f"₹{GRID['PN-R-Toll-Hse']['Worst']['exit3']:.0f}-"
               f"{GRID['SBR-R-Toll-Hse']['Worst']['exit3']:.0f} lakh in the Worst case for the rented "
               "toll-roasted models. That is close to the whole investment, and it is the real "
               "downside to plan for."))
    return s


def DF_bubble(pts):
    return DC.bubble(pts, W * 0.5, 250, title="Capital needed vs project IRR (Base)",
                     xlab="total capital requirement, ₹ lakh", ylab="project IRR", xfmt="{:,.0f}",
                     yfmt="{:.0%}", size_scale=0.95, label_size=6.0, yr=(0.0, 0.40),
                     show_labels={"SBR-R-Toll-Hse", "GIFT-R-Toll-Hse", "PN-R-Toll-Hse", "SBR-O-Toll", "PN-O-Toll",
                                  "GIFT-O-Toll", "SAN-R-Toll", "SAN-R-InH", "SAN-O-Toll", "PN-R-InH"})


def incremental_irr(flows):
    lo, hi = -0.9, 1.0
    f = lambda r: sum(v / (1 + r) ** i for i, v in enumerate(flows))  # noqa: E731
    if f(lo) * f(hi) > 0:
        return float("nan")
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def roastery_breakeven(tab):
    xs, vals = tab["down"], tab["values"]
    for i in range(1, len(xs)):
        d0 = vals[i - 1][1] - vals[i - 1][0]
        d1 = vals[i][1] - vals[i][0]
        if d0 < 0 <= d1:
            return xs[i - 1] + (xs[i] - xs[i - 1]) * (-d0) / (d1 - d0)
    return float("nan")


# =============================================================================== 17. featured models
def ch18():
    s = chapter("c18", 18, "The four models to pursue", "Location, premises, roasting and beans: the "
                "shortlist, in depth", TEAL)
    s.append(p("Four configurations stand out. All use <b>toll roasting</b> and the <b>House blend</b>; "
               "three rent their premises. They are ranked by value created per rupee of risk "
               "capital, with Prahladnagar kept as the brief's reference point."))
    rows = []
    for fid in ("A", "B", "C", "D"):
        q = m(fid)["scalars"]
        rows.append([label(fid), num(q["u_tot"]), num(q["s_eq"]), num(q["npv"]), irr_txt(q["irr_p"]),
                     irr_txt(q["irr_e"]), yrs(q["payback"]), num(q["y3_rev"]), pct(q["y3_margin"]),
                     num(sc(fid, "npv", "Best")), num(sc(fid, "npv", "Worst"))])
    s.append(tbl(["Model (all toll roasting, House blend)", "Capital", "Equity", "NPV", "Proj. IRR",
                  "Eq. IRR", "Payback", "Y3 revenue", "Y3 EBITDA %", "NPV Best", "NPV Worst"], rows,
                 [124, 38, 36, 36, 38, 36, 40, 40, 40, 38, W - 466], font_size=7.0,
                 center_cols=tuple(range(1, 11))))
    s.append(src("Model outputs, Base scenario unless stated (₹ lakh)."))
    rows = [["Capital needed", 7.0, 8.5, 8.0, 3.0], ["Value created (NPV)", 8.5, 7.5, 6.0, 9.0],
            ["Return on capital (IRR)", 9.0, 9.0, 8.0, 6.0], ["Downside resilience", 6.5, 8.0, 5.5, 6.0],
            ["Competition", 5.0, 9.0, 5.0, 5.0], ["Execution effort", 6.5, 7.0, 7.5, 5.0],
            ["Strategic fit (brand, phase 2)", 9.0, 8.0, 6.5, 6.0]]
    for r in rows:
        r.append(None)
    sc_rows = [[r[0]] + r[1:5] for r in rows]
    tot = [round(sum(r[i] for r in rows) / len(rows), 1) for i in range(1, 5)]
    sc_rows.append(["<b>Average score</b>"] + tot)
    cum = {fid: [sum(ser(fid, "eq_cf")[:i + 1]) for i in range(11)] for fid in "ABCD"}
    s.append(side([tbl(["Criterion (10 = best)", "A", "B", "C", "D"], sc_rows,
                       [W * 0.2, W * 0.065, W * 0.065, W * 0.065, W * 0.065], score_cols=(1, 2, 3, 4),
                       font_size=7.2)],
                  [DC.line_chart(FY, [(f"Model {fid}", cum[fid], MCOL[fid]) for fid in "ABCD"], W * 0.5, 170,
                                 title="Cumulative cash to the promoter (FCFE, ₹ lakh)",
                                 sub="Y0 = equity invested net of cash kept; excludes terminal value",
                                 zero=True)], lw=0.48))
    s.append(P("Figure 18.1. Qualitative ranking (left; author's assessment combining the model with site "
               "research) and cumulative equity cash flows (right). Model D needs the most money and takes "
               "longest to pay back.", R.CAPTION))
    why = {
        "A": ["Highest NPV of the rented options: Ahmedabad's strongest evening and weekend café street, "
              "the highest average bill (₹367 incl. House-blend premium) and 170 bills a day at steady "
              "state.",
              "Rent is the city's highest (₹175/sqft) but is still only about 11% of sales.",
              "Risks: intense competition (new specialty openings every few months), fit-out quality "
              "expectations, parking. Mitigate with a strong signature menu (specialty kaapi, cold brew) "
              "and retail beans."],
        "B": ["Lowest capital and the most resilient model: captive office demand, few quality cafés and a "
              "workforce targeted to reach 1 lakh by 2030 (+4% a year volume premium in Y2-Y6).",
              "Trade-offs: weekday-heavy (290 operating-day equivalents), high CAM in Grade-A towers, "
              "and leasing via GIFT's RFP processes.",
              "Batch brew and pre-ordering suit office peaks; wholesale coffee to office pantries is a "
              "natural add-on."],
        "C": ["The brief's site works: positive NPV, about 30% project IRR and payback within five years "
              "in the Base case.",
              "But margins are thinner (19.5% EBITDA in Y3), Starbucks, Third Wave and others are already "
              "there, and the Worst case loses money.",
              "Treat as viable but third choice, or as a second outlet once the brand is known."],
        "D": ["Buying the SBR unit adds the most absolute NPV, because rent is saved and the property "
              "appreciates about 6% a year.",
              "But it needs about three times the capital, with ₹1.8 crore of equity, a 10-year "
              "property loan, and a project IRR of about 22%.",
              "It mixes a property investment with a café; consider it only after model A proves the "
              "site."]}
    for fid in ("A", "B", "C", "D"):
        s += model_pages(fid, why[fid])
    return s


def model_pages(fid, why):
    mm = MODELS[fid]
    q = m(fid)["scalars"]
    col = MCOL[fid]
    out = [PageBreak(),
           P(f'<font name="Head" size="15" color="{col.hexval().replace("0x", "#")}">Model {fid}: '
             f'{mm["name"]}</font>', R.BODY),
           P(f"{mm['location']} | {mm['premises']} | {mm['roasting']} | {mm['mix']} blend", R.CAPTION),
           kpi_tiles([(f"₹{q['u_tot']:,.0f} L", "total capital need", col),
                      (f"₹{q['npv']:,.0f} L", "project NPV at WACC", col),
                      (irr_txt(q["irr_p"]) + " / " + irr_txt(q["irr_e"]), "project / equity IRR", col),
                      (yrs(q["payback"]), "payback from opening", col)], cols=4),
           Spacer(1, 6)]
    rev = ser(fid, "is_rev")[1:]
    eb = ser(fid, "is_ebitda")[1:]
    ebm = ser(fid, "is_ebitda_m")[1:]
    ff = ser(fid, "fcff")
    out.append(side([DC.bar_chart(FY[1:], [("Revenue", rev, CARAMEL), ("EBITDA", eb, ROAST)], W * 0.5, 160,
                                  title="Revenue and EBITDA, Base (₹ lakh)", fmt="{:,.0f}",
                                  line=("EBITDA margin", ebm, col), show_vals=False, cat_size=6.0)],
                    [DC.bar_chart(FY, [("FCFF", ff, col)], W * 0.48, 160,
                                  title="Free cash flow to firm, Base (₹ lakh)", fmt="{:,.0f}",
                                  line=None, show_vals=False, cat_size=6.0)], lw=0.51))
    out.append(Spacer(1, 6))
    rows = []
    for sn in SC:
        k = m(fid, sn)["scalars"]
        rows.append([sn, num(k["npv"]), irr_txt(k["irr_p"]), irr_txt(k["irr_e"]), yrs(k["payback"]),
                     num(k["y3_rev"]), pct(k["y3_margin"]), f"{k['y3_bills']:.0f}", f"{k['be_y3']:.0f}",
                     num(k["peak_rev"]), num(k["exit3"]) if k["exit3"] > 0.05 else "nil"])
    out.append(tbl(["Scenario", "NPV", "Proj. IRR", "Eq. IRR", "Payback", "Y3 revenue", "Y3 EBITDA %",
                    "Bills/day Y3", "Break-even", "Peak overdraft", "Loss if shut Y3"], rows,
                   [52, 40, 42, 40, 44, 46, 46, 46, 44, 50, W - 450], font_size=7.0,
                   center_cols=tuple(range(1, 11))))
    out.append(Spacer(1, 8))
    out.append(note(f"Why model {fid}", why, col))
    # ---- second page: statements, funding, unit economics, balance sheet trajectory
    out.append(PageBreak())
    out.append(P(f'<font name="Head" size="12" color="{col.hexval().replace("0x", "#")}">Model {fid} in '
                 f'detail: statements, funding and unit economics</font>', R.BODY))
    out.append(statement_table(fid))
    out.append(Spacer(1, 8))
    S = m(fid)["series"]
    i = 3
    bills_yr = S["bills_yr"][i]

    def per(v):
        return v * 1e5 / bills_yr
    occ = S["rent"][i] + S["cam"][i] + S["ptax"][i]
    oth = sum(S[k][i] for k in ("power", "gaswater", "mkt_c", "rm_var", "amc_c", "aggr", "payfee", "admin",
                                "misc", "whs_sell"))
    ue = [["Revenue per bill", f"₹{per(S['is_rev'][i]):,.0f}"],
          ["Ingredients & packaging", f"₹{per(S['cogs'][i]):,.0f}"],
          ["Staff", f"₹{per(S['staff'][i]):,.0f}"], ["Rent, CAM, property tax", f"₹{per(occ):,.0f}"],
          ["Utilities, marketing, fees, other", f"₹{per(oth):,.0f}"],
          ["<b>EBITDA per bill</b>", f"<b>₹{per(S['is_ebitda'][i]):,.0f}</b>"],
          ["Coffee cost per beverage", f"₹{S['cogs_coffee'][i] * 1e5 / max(1, S['cups'][i]):,.1f}"],
          ["Bills per day / break-even", f"{S['bills'][i]:.0f} / {S['be_bills'][i]:.0f}"]]
    su = [["Café & roastery capex", num(q["u_capex"])], ["Property incl. stamp duty", num(q["u_prop"])],
          ["Pre-opening expenses", num(q["u_preop"])], ["Rent deposit", num(q["u_dep"])],
          ["Cash reserve", num(q["u_cash"])], ["<b>Total need</b>", f"<b>{num(q['u_tot'])}</b>"],
          ["Term loan", num(q["s_debt"])], ["Promoter equity", num(q["s_eq"])],
          ["Loan rate / tenor", f"{q['loan_rate']:.0%} / {q['loan_tenor']:.0f} yrs"],
          ["WACC / cost of equity", f"{q['wacc']:.1%} / {q['ke']:.1%}"]]
    cash = S["bs_cash"]
    debt = [a2 + b2 for a2, b2 in zip(S["bs_tl"], S["bs_rev"])]
    out.append(side([tbl(["Unit economics, Y3 Base", ""], ue, [W * 0.2, W * 0.1], font_size=7.2),
                     Spacer(1, 6),
                     tbl(["Sources & uses (₹ lakh)", ""], su, [W * 0.2, W * 0.1], font_size=7.2)],
                    [DC.line_chart(FY, [("Cash", cash, col), ("Debt", debt, BERRY),
                                        ("Shareholders' equity", S["bs_eq"], ROAST, True)], W * 0.62, 200,
                                   title="Balance sheet trajectory, Base (₹ lakh)", zero=True),
                     ps("Cash accumulates because the model pays no dividends (payout 0%); in practice "
                        "surplus cash would fund a second outlet or be distributed. Equity IRR assumes free "
                        "cash flow to equity is paid out each year.")], lw=0.33))
    return out


def statement_table(fid):
    idx = [0, 1, 2, 3, 5, 10]
    S = m(fid)["series"]

    def row(lab, vals, bold=False):
        cells = [f"<b>{lab}</b>" if bold else lab] + [
            (f"<b>{num(vals[i])}</b>" if bold else num(vals[i])) for i in idx]
        return cells

    occ = [a + b + c for a, b, c in zip(S["rent"], S["cam"], S["ptax"])]
    other = [sum(S[k][i] for k in ("power", "gaswater", "mkt_c", "rm_var", "amc_c", "aggr", "payfee", "admin",
                                   "misc", "whs_sell", "preop")) for i in range(11)]
    net_int = [a + b for a, b in zip(S["is_int"], S["is_inc"])]
    tax = [a + b for a, b in zip(S["is_tax_cur"], S["is_tax_def"])]
    debt = [a + b for a, b in zip(S["bs_tl"], S["bs_rev"])]
    nwc_bs = [a + b - c for a, b, c in zip(S["bs_ar"], S["bs_inv"], S["bs_ap"])]
    rows = [row("Bills per day", S["bills"]), row("Revenue", S["is_rev"], True),
            row("Cost of goods sold", [-v for v in S["cogs"]]), row("Staff", [-v for v in S["staff"]]),
            row("Rent, CAM & property tax", [-v for v in occ]), row("Other opex & pre-opening",
                                                                    [-v for v in other]),
            row("EBITDA", S["is_ebitda"], True), row("Depreciation", S["is_dep"]),
            row("Net interest", net_int), row("Tax", tax), row("Profit after tax", S["is_pat"], True),
            row("Cash from operations", S["cf_cfo"]), row("Capex & deposit", S["cf_cfi"]),
            row("Free cash flow to firm", S["fcff"], True), row("Closing cash", S["bs_cash"]),
            row("Fixed assets (net)", S["bs_ppe"]), row("Net working capital", nwc_bs),
            row("Debt", debt), row("Shareholders' equity", S["bs_eq"], True),
            row("Balance-sheet check", S["bs_chk"])]
    hdr = ["Condensed statements, Base (₹ lakh)"] + [FY[i] for i in idx]
    return tbl(hdr, rows, [W - 6 * 56] + [56] * 6, font_size=6.9, head_size=7.0,
               center_cols=(1, 2, 3, 4, 5, 6), bold_first=False)


# =============================================================================== 18. risk
def ch19():
    s = chapter("c19", 19, "Risk: scenarios and sensitivities", "What moves value most, and how much "
                "room for error each model has", BERRY)
    for fid in ("A", "B", "C", "D"):
        t = MODELS[fid]["tables"]["tornado"]["values"]
        labs = [x[0].replace(" (+/- pp)", "").replace(" (abs.)", "") for x in A.TORNADO]
        rng = [f"{lo - 1:+.0%} / {hi - 1:+.0%}" for _n, lo, hi in A.TORNADO[:6]] + ["-2 / +2 pp",
                                                                                    "3% / 5%"]
        base = sc(fid, "npv")
        lows = [min(r) if i != 7 else r[0] for i, r in enumerate(t)]
        highs = [max(r) if i != 7 else r[1] for i, r in enumerate(t)]
        s.append(figc(DC.tornado(labs, lows, highs, base, W, 138,
                                 title=f"Model {fid} ({MODELS[fid]['name']}): project NPV when one input "
                                       "moves (₹ lakh)", ranges=rng),
                      f"Figure 19.{'ABCD'.index(fid) + 1}. Each bar moves one input to its low or high "
                      "value and keeps everything else at Base."))
    s.append(p("Demand inputs dominate: <b>bills per day and the average bill</b> each swing NPV by more "
               "than the next three inputs combined. Staff costs and WACC come next; rent and coffee "
               "prices matter, but far less. The practical message: spend money on location research "
               "(footfall counts at the shortlisted units at different times of day) and on the menu "
               "and service that drive repeat visits, rather than over-optimising the bean price."))
    tA = MODELS["A"]["tables"]
    g = tA["wacc_g"]
    s.append(side([DC.heat_table(["WACC -2pp", "WACC -1pp", "WACC as calc.", "WACC +1pp", "WACC +2pp"],
                                 ["g 3.0%", "g 3.5%", "g 4.0%", "g 4.5%", "g 5.0%"], g["values"],
                                 lambda v: f"{v:,.0f}", 44, 66, corner="Model A NPV", mid=0, font=6.8,
                                 bold_cell=(2, 2)),
                   Spacer(1, 6),
                   DC.heat_table(["Bills -20%", "Bills -10%", "Bills base", "Bills +10%", "Bills +20%"],
                                 ["Bill -10%", "Bill -5%", "Base", "Bill +5%", "Bill +10%"],
                                 tA["bills_atv"]["values"], lambda v: f"{v:,.0f}", 44, 66,
                                 corner="Model A NPV", mid=0, font=6.8, bold_cell=(2, 2))],
                  [DC.heat_table(["Rent -20%", "Rent -10%", "Rent base", "Rent +10%", "Rent +20%"],
                                 ["Bills -20%", "-10%", "Base", "+10%", "+20%"], tA["rent_bills"]["values"],
                                 lambda v: f"{v:.0%}" if isinstance(v, float) else str(v), 40, 64,
                                 corner="Model A project IRR", mid=0.16, font=6.8, bold_cell=(2, 2)),
                   Spacer(1, 6),
                   DC.heat_table(["Green -30%", "Green -15%", "Green base", "Green +15%", "Green +30%",
                                  "Green +60%"], ["Buy", "Toll", "In-house"], tA["green_roast"]["values"],
                                 lambda v: f"{v:.1%}", 56, 64, corner="Model A Y3 EBITDA %", mid=0.15,
                                 font=6.8, bold_cell=(2, 1))], lw=0.5))
    s.append(P("Figure 19.5. Two-way sensitivities for Model A (green = better, red = worse; the boxed cell "
               "is the Base case). Owners can re-run every table for any configuration on the Scenarios "
               "sheet.", R.CAPTION))
    mults = [0.8, 0.9, 1.0, 1.1, 1.2]
    s.append(side([DC.line_chart([f"{int(x * 100)}%" for x in mults],
                                 [(f"Model {fid}", [r[2] for r in MODELS[fid]["tables"]["bills_atv"]["values"]],
                                   MCOL[fid]) for fid in "ABCD"], W * 0.5, 170,
                                 title="NPV vs customers (bills/day as % of plan)", zero=True)],
                  [p("<b>How many customers do you need?</b> The chart re-runs each model with bills per day "
                     "at 80-120% of plan, holding everything else at Base. Models A, B and D stay NPV-positive "
                     "even at 80% of planned bills; Model C turns negative at about 83%. Model D, carrying "
                     "property, swings the most in absolute terms."),
                   p("That makes <b>footfall verification before signing a lease</b> the single most "
                     "valuable piece of due diligence: count people and competitor queues at the actual "
                     "unit across weekday mornings, evenings and weekends.")], lw=0.52))
    s.append(h2("19.1 How the scenarios play out (Model A)"))
    s.append(M5.scenario_paths({sn: m("A", sn)["series"] for sn in SC}, FY))
    s.append(P("Figure 19.6. In the Worst case the café never escapes thin margins: revenue grows only with "
               "prices while wages grow faster, so EBITDA peaks in year 4 and then declines.", R.CAPTION))
    s.append(h2("19.2 Where each ₹100 of sales goes"))
    S = m("C")["series"]
    i = 3
    tot = S["is_rev"][i]
    occ = S["rent"][i] + S["cam"][i] + S["ptax"][i]
    util = S["power"][i] + S["gaswater"][i]
    sell = S["mkt_c"][i] + S["aggr"][i] + S["payfee"][i]
    oth = S["rm_var"][i] + S["amc_c"][i] + S["admin"][i] + S["misc"][i] + S["whs_sell"][i]
    dep = -S["is_dep"][i]
    intr = -(S["is_int"][i] + S["is_inc"][i])
    tax = -(S["is_tax_cur"][i] + S["is_tax_def"][i])
    pat = S["is_pat"][i]
    parts = [("Ingredients & packaging", S["cogs"][i], HX("#6B4430")), ("Staff", S["staff"][i], CARAMEL),
             ("Rent & CAM", occ, GOLD), ("Power, gas, water", util, SKY),
             ("Marketing & channel fees", sell, PLUM), ("Repairs, admin, other", oth, HX("#9A8C80")),
             ("Depreciation", dep, HX("#7F7F7F")), ("Interest", intr, BERRY), ("Tax", tax, HX("#555555")),
             ("Profit after tax", pat, LEAF)]
    parts = [(a, v / tot * 100, c) for a, v, c in parts]
    s.append(figc(DF.cup_anatomy(parts, W, 74, "Model C (Prahladnagar), Y3: every ₹100 of sales"),
                  "Figure 19.7. Coffee beans themselves are only about ₹6-7 of every ₹100. Staff and "
                  "ingredients are the big levers; rent is about ₹9."))
    s.append(h2("19.3 Key risks and how to manage them"))
    rows = [["Demand below plan", "Biggest value driver (tornado)", "Count footfall at candidate units; "
             "pre-launch community and office tie-ups; menu with a signature; delivery from day one"],
            ["Slow ramp-up", "Year-1 losses and cash burn", "Three-month cash reserve in the funding plan; "
             "rent-free fit-out period; staged hiring"],
            ["Wage inflation above price growth", "Margins erode over time", "Annual price reviews; "
             "productivity (batch brew, POS), scheduling to footfall"],
            ["Green-coffee price spike", "Coffee is ~6% of sales; +30% costs ~2.5-3 points of margin",
             "Toll roasting with 2-3 months' green stock; forward contracts with estates"],
            ["Competition", "New openings on SBR and Corporate Road", "Differentiate on Indian estate "
             "coffees, kaapi, retail beans; loyalty app"],
            ["Lease risk", "Rent escalations, eviction", "9-year lease with 3-year lock-in and capped "
             "escalation (5%/yr or 15% per 3 years)"]]
    s.append(tbl(["Risk", "Why it matters", "Mitigation"], rows, [100, 140, W - 240], font_size=7.4))
    return s


# =============================================================================== 19. recommendation
def ch20():
    s = chapter("c20", 20, "Recommendation and roadmap", "What to do, in what order, and what to check "
                "before signing", LEAF)
    a, b, c = m("A")["scalars"], m("B")["scalars"], m("C")["scalars"]
    s.append(note("Recommendation", [
        f"<b>1. Open the first café on Sindhu Bhavan Road (Model A)</b>: rented unit, toll-roasted House "
        f"blend. Capital about ₹{a['u_tot']:.0f} lakh (₹{a['s_eq']:.0f} lakh equity), NPV "
        f"₹{a['npv']:.0f} lakh, project IRR {irr_txt(a['irr_p'])}, payback {yrs(a['payback'])}.",
        f"<b>2. If capital or a good SBR unit is not available, choose GIFT City (Model B)</b>: "
        f"₹{b['u_tot']:.0f} lakh capital, NPV ₹{b['npv']:.0f} lakh, the most resilient downside. It is "
        "also the natural second outlet.",
        f"<b>3. Prahladnagar (Model C) is viable but third</b> (NPV ₹{c['npv']:.0f} lakh, IRR "
        f"{irr_txt(c['irr_p'])}): thinner margins and more chain competition. Choose it only for an "
        "exceptional unit at or below ₹115/sqft rent with strong visibility.",
        "<b>4. Rent, don't buy</b>, for the first café. Revisit buying once a site has proven itself.",
        "<b>5. Toll-roast from day one</b> (own green coffee, own label, no roaster capex). Add an "
        "in-house roastery only when wholesale demand passes roughly 450-500 kg a month.",
        "<b>6. Not Sanand yet.</b> Re-examine in 2028 as the semiconductor workforce arrives; it could "
        "then host a low-cost roastery."], LEAF, bg=HX("#EEF6EC")))
    rows = [("Shortlist units, footfall counts", [(9, 11)], SKY, "Oct-Nov 2026"),
            ("Lease negotiation & sign", [(10, 12)], SKY, "Nov-Dec"),
            ("Bank loan (CGTMSE) & company set-up", [(10, 12), (0, 1)], PLUM, ""),
            ("Design & fit-out (8-10 weeks)", [(0, 3)], ROAST, "Jan-Mar 2027"),
            ("Equipment, toll-roast trials, menu", [(1, 3)], SAFFRON, ""),
            ("Hiring & training", [(2, 3)], GOLD, ""),
            ("Licences: FSSAI, Shop Act, fire NOC", [(0, 3)], BERRY, ""),
            ("Soft launch & opening (Y1 starts)", [(3, 4)], LEAF, "Apr 2027")]
    labels = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"]
    rows = [(lab, [(a2 - 9 if a2 >= 9 else a2 + 3, b2 - 9 if b2 >= 9 else b2 + 3) for a2, b2 in spans], col,
             nt) for lab, spans, col, nt in rows]
    s.append(figc(DC.gantt(rows, W, 120, title="Launch timeline (October 2026 to May 2027)", lab_w=170,
                           labels=labels),
                  "Figure 20.1. Six months from site search to opening, matching the model's Y0."))
    s.append(h2("20.1 Before signing: what to verify"))
    s.append(bl(["<b>Footfall and bills</b>: count passers-by and competitors' queues at the unit on "
                 "weekday mornings, evenings and weekends; the model needs about 110-170 bills a day.",
                 "<b>Rent and terms</b>: carpet versus super area, CAM, escalation, lock-in, rent-free "
                 "fit-out months, deposit (model: 4-6 months).",
                 "<b>Fit-out reality</b>: power load (kW), drainage, exhaust, fire NOC and society rules "
                 "for cafés; landlord contributions.",
                 "<b>Toll roaster</b>: cup samples, minimum batch, lead time, price per kg, private-label "
                 "terms; green-coffee contracts with two or three estates.",
                 "<b>Team</b>: a head barista with specialty experience is the most important hire."]))
    s.append(h2("20.2 Funding options"))
    rows = [["Promoter equity", "Founder and family; angel investors", "No repayment; dilution if outside "
             "investors", "Model: ₹66-182 lakh depending on model"],
            ["MSME term loan + CGTMSE guarantee", "Banks and NBFCs; collateral-free credit guarantee (cover "
             "raised to ₹10 crore in Budget 2025)", "~10-12%, 5-7 years", "Model: 50% of capex at 11%, "
             "5 years"],
            ["PM MUDRA (Tarun / Tarun Plus)", "Up to ₹20 lakh for micro enterprises", "Small top-up",
             "Useful for equipment or working capital"],
            ["Equipment leasing / vendor finance", "Espresso machines and grinders on lease", "Preserves cash; "
             "higher effective cost", "Alternative for ₹10-15 lakh of kit"],
            ["Loan against property", "For the owned-premises option", "~9.5-10.5%, 10-15 years",
             "Model D: 60% of capex + property at 10%"],
            ["Cash credit / overdraft", "Working-capital line", "~12-13%", "The model draws only if cash dips"]]
    s.append(tbl(["Source", "What it is", "Typical terms", "In the model"], rows, [104, 170, 100, W - 374],
                 font_size=7.3))
    s.append(h2("20.3 The monthly dashboard to run the café by"))
    rows = [["Bills per day (and by daypart)", "Plan: Y1 65%, Y2 85%, Y3 100% of steady state (170 at SBR)",
             "Weekly"],
            ["Average bill (ex-GST)", "₹367 at SBR in Y1, rising with menu prices", "Weekly"],
            ["Ingredient cost % of sales", "~29-31%", "Monthly stock count"],
            ["Staff cost % of sales", "~22-26% at steady state", "Monthly"],
            ["Rent + CAM % of sales", "~11% (SBR), ~9% (Prahladnagar)", "Monthly"],
            ["EBITDA margin", "Break-even in year 1 (SBR plan); 20%+ by year 3", "Monthly"],
            ["Cash in bank", "Never below the minimum + one month of fixed costs", "Weekly"],
            ["Coffee freshness", "Beans served 7-30 days from roast", "Daily"],
            ["Reviews and repeat rate", "4.5+ ratings; loyalty-app repeat visits", "Weekly"]]
    s.append(tbl(["KPI", "Target (from the model)", "Review"], rows, [150, 250, W - 400], font_size=7.3))
    s.append(h2("20.4 Phase two"))
    s += bl(["<b>Second outlet</b> (Model B at GIFT City if Model A opened first) once the first café beats "
             "plan for six consecutive months.",
             "<b>Own roastery</b> when wholesale demand passes roughly 450-500 kg a "
             "month: a 3-5 kg roaster with an afterburner in a light-industrial unit (Sanand or the "
             "city's edge) can then supply all outlets and wholesale accounts.",
             "<b>Retail and quick commerce</b>: own-label beans, drip bags and cold-brew bottles once the "
             "brand has local recognition."])
    s.append(h2("20.5 How to use the workbook from here"))
    s.append(p("Replace the judgement inputs with your own data as you learn it: real rent quotes on "
               "<b>Locations</b>, menu prices and mix on <b>Inputs</b>, quotes on <b>Capex</b>, and bean "
               "prices on <b>Sourcing</b>. The <b>Dashboard</b>, <b>Configs</b> ranking and the "
               "<b>Scenarios</b> tables update automatically, so the comparison in this report can be "
               "re-run in minutes as facts replace assumptions."))
    return s


# =============================================================================== appendix
def appendix():
    s = chapter("app", "A", "Appendix", "Full Base-case statements for Model A, sources and glossary",
                HX("#7A6F66"))
    S = m("A")["series"]
    keys = [("Revenue", "is_rev", True), ("Cost of goods sold", "is_cogs_neg", False),
            ("Gross profit", "is_gp", True), ("Staff", "staff_neg", False), ("Occupancy", "occ_neg", False),
            ("Other opex", "oth_neg", False), ("EBITDA", "is_ebitda", True), ("Depreciation", "is_dep", False),
            ("EBIT", "is_ebit", True), ("Interest expense", "is_int", False), ("Interest income", "is_inc", False),
            ("Tax", "tax", False), ("Profit after tax", "is_pat", True),
            ("Cash from operations", "cf_cfo", True), ("Cash from investing", "cf_cfi", False),
            ("Cash from financing", "cf_cff", False), ("Closing cash", "cf_close", True),
            ("Cash", "bs_cash", False), ("Receivables + inventory", "arinv", False),
            ("Rent deposit", "bs_depo", False), ("Fixed assets", "bs_ppe", False), ("Total assets", "bs_ta", True),
            ("Payables", "bs_ap", False), ("Debt", "debt", False), ("Deferred tax", "bs_dtl", False),
            ("Equity", "bs_eq", False), ("Liabilities + equity", "bs_tle", True), ("Check", "bs_chk", False),
            ("FCFF", "fcff", True), ("FCFE", "fcfe", False)]
    der = {"is_cogs_neg": [-v for v in S["cogs"]], "staff_neg": [-v for v in S["staff"]],
           "occ_neg": [-(a + b + c) for a, b, c in zip(S["rent"], S["cam"], S["ptax"])],
           "oth_neg": [-sum(S[k][i] for k in ("power", "gaswater", "mkt_c", "rm_var", "amc_c", "aggr", "payfee",
                                               "admin", "misc", "whs_sell", "preop")) for i in range(11)],
           "tax": [a + b for a, b in zip(S["is_tax_cur"], S["is_tax_def"])],
           "arinv": [a + b for a, b in zip(S["bs_ar"], S["bs_inv"])],
           "debt": [a + b for a, b in zip(S["bs_tl"], S["bs_rev"])]}
    rows = []
    for labl, k, bold in keys:
        v = der.get(k, S.get(k))
        rows.append([f"<b>{labl}</b>" if bold else labl] + [num(x) for x in v])
    s.append(tbl(["Model A, Base, ₹ lakh"] + FY, rows, [96] + [(W - 96) / 11] * 11, font_size=6.5,
                 head_size=6.6, center_cols=tuple(range(1, 12)), bold_first=False))
    s.append(src("Cafe_Financial_Model.xlsx with Inputs set to Sindhu Bhavan Road | Rent | Toll roasting | "
                 "House | Base. Rows are links to the Model sheet; the check row is zero in every year."))
    s.append(Spacer(1, 10))
    s.append(full_statements("C"))
    s.append(src("Model C: Prahladnagar | Rent | Toll roasting | House | Base."))
    s.append(PageBreak())
    s.append(full_statements("B"))
    s.append(src("Model B: GIFT City | Rent | Toll roasting | House | Base."))
    s.append(Spacer(1, 10))
    s.append(full_statements("D"))
    s.append(src("Model D: Sindhu Bhavan Road | Own | Toll roasting | House | Base. Property is carried at "
                 "cost (land not depreciated); its market value enters the terminal value."))
    s.append(h2("Glossary of financial terms"))
    gl = [["NPV", "Net present value: today's value of all future cash flows minus the investment"],
          ["IRR", "Internal rate of return: the discount rate at which NPV is zero"],
          ["Project IRR / FCFF", "Return on all capital, using free cash flow to the firm (before debt)"],
          ["Equity IRR / FCFE", "Return on the promoter's money, after debt flows"],
          ["WACC", "Weighted average cost of capital: blended required return of equity and debt"],
          ["Cost of equity", "Risk-free rate + beta x equity risk premium + specific premium"],
          ["Terminal value", "Value of cash flows after Y10, here a perpetuity growing at 4%"],
          ["EBITDA", "Earnings before interest, tax, depreciation and amortisation"],
          ["Payback", "Years until cumulative free cash flow turns positive"],
          ["DSCR", "Debt service cover: cash available / (interest + principal)"],
          ["Break-even bills", "Bills per day at which EBITDA is zero"],
          ["WDV depreciation", "Tax depreciation at a fixed % of the declining written-down value"],
          ["Deferred tax", "Tax effect of the gap between book and tax depreciation"],
          ["Data table", "Excel what-if tool that re-runs the model for many input values"]]
    s.append(tbl(["Term", "Meaning"], gl, [100, W - 100], font_size=7.3))
    return s


def full_statements(fid):
    S = m(fid)["series"]
    keys = [("Revenue", "is_rev", True), ("Cost of goods sold", "cogs_neg", False), ("Gross profit", "is_gp", True),
            ("Staff", "staff_neg", False), ("Occupancy", "occ_neg", False), ("Other opex", "oth_neg", False),
            ("EBITDA", "is_ebitda", True), ("Depreciation", "is_dep", False), ("EBIT", "is_ebit", True),
            ("Net interest", "net_int", False), ("Tax", "tax", False), ("Profit after tax", "is_pat", True),
            ("Cash from operations", "cf_cfo", True), ("Cash from investing", "cf_cfi", False),
            ("Cash from financing", "cf_cff", False), ("Closing cash", "cf_close", True),
            ("Fixed assets", "bs_ppe", False), ("Total assets", "bs_ta", True), ("Debt", "debt", False),
            ("Equity", "bs_eq", False), ("Check", "bs_chk", False), ("FCFF", "fcff", True)]
    der = {"cogs_neg": [-v for v in S["cogs"]], "staff_neg": [-v for v in S["staff"]],
           "occ_neg": [-(a + b + c) for a, b, c in zip(S["rent"], S["cam"], S["ptax"])],
           "oth_neg": [-sum(S[k][i] for k in ("power", "gaswater", "mkt_c", "rm_var", "amc_c", "aggr", "payfee",
                                               "admin", "misc", "whs_sell", "preop")) for i in range(11)],
           "net_int": [a + b for a, b in zip(S["is_int"], S["is_inc"])],
           "tax": [a + b for a, b in zip(S["is_tax_cur"], S["is_tax_def"])],
           "debt": [a + b for a, b in zip(S["bs_tl"], S["bs_rev"])]}
    rows = []
    for labl, k, bold in keys:
        v = der.get(k, S.get(k))
        rows.append([f"<b>{labl}</b>" if bold else labl] + [num(x) for x in v])
    return tbl([f"Model {fid}, Base, ₹ lakh"] + FY, rows, [96] + [(W - 96) / 11] * 11, font_size=6.5,
               head_size=6.6, center_cols=tuple(range(1, 12)), bold_first=False)

