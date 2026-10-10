#!/usr/bin/env python3
"""Build Cafe_Financial_Model.xlsx: an interactive 3-statement + FCFF DCF model
for a specialty café in Ahmedabad.

Conventions follow the CFI Financial Modeling Guidelines: blue = hard-coded input,
black = formula, green = link to another sheet; one font; annual timeline; inputs
entered once; Best/Base/Worst drivers chosen by a switch; IS -> CFS -> BS stacked
on one Model sheet with the supporting schedules underneath; checks and a
circularity switch on the Cover.

    python3 build_excel.py            # layout + formulas, then LibreOffice recalc
    python3 build_excel.py --no-calc  # formulas only (Excel recalculates on open)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import assumptions as A  # noqa: E402
from xlbook import (BAND, BLUE, GREY, HEAD_FILL, INFILL, NT, TC, TL0, Book)  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "Cafe_Financial_Model.xlsx")
SCRATCH = os.environ.get("MODEL_SCRATCH", os.path.join(HERE, ".build"))

SHEETS = [("Cover", BAND, "free"), ("Dashboard", "#C0504D", "timeline"),
          ("Inputs", BLUE, "timeline"), ("Locations", BLUE, "free"),
          ("Sourcing", BLUE, "free"), ("Capex", BLUE, "free"),
          ("Model", "#404040", "timeline"), ("DCF", "#404040", "timeline"),
          ("Scenarios", "#8064A2", "free"), ("Configs", "#8064A2", "free"),
          ("Sources", "#7F7F7F", "free")]
CLASSES = A.ASSET_CLASSES
DEP_CLASSES = [c for c in CLASSES if c != "Land"]
LOC_KEYS = [k for k, *_ in A.LOCATION_ROWS]


def pct_or(v):
    return "pct" if isinstance(v, float) and abs(v) < 1.5 and v != int(v) else "int"


# =============================================================================== Cover
def cover(B):
    ws = B.use("Cover")
    ws.set_column(0, 0, 2)
    ws.set_column(1, 1, 30)
    ws.set_column(2, 2, 64)
    ws.set_column(3, 3, 22)
    ws.set_column(4, 11, 10)
    ws.set_row(0, 30)
    ws.write_string(0, 1, "Specialty Café, Ahmedabad: 3-Statement & FCFF DCF Model",
                    B.f(None, bold=True, font_size=20, font_color=BAND))
    ws.write_string(1, 1, "Location × premises (rent/own) × roasting × bean-mix decision model. "
                    "Prepared October 2026. All figures in ₹ lakh unless stated (1 lakh = ₹1,00,000).",
                    B.f(None, italic=True, font_color=GREY))
    B.put(2, 1, '="Model running: "&{$cfg_label}', num=None, bold=True, color="#9C4A1A")
    B.r["Cover"] = 4
    B.band("Contents")
    toc = [("Dashboard", "Key outputs, charts, scenario and premises comparison"),
           ("Inputs", "Configuration switches, Best/Base/Worst drivers, all operating assumptions"),
           ("Locations", "Library of four Ahmedabad sites: rent, area, footfall, ticket, capex"),
           ("Sourcing", "Green-coffee prices, bean mixes, cost per kg by roasting route"),
           ("Capex", "Equipment & fit-out list, property purchase, sources & uses of funds"),
           ("Model", "Income statement, cash flow, balance sheet and supporting schedules"),
           ("DCF", "FCFF, WACC, terminal value, NPV, IRR, equity IRR, payback"),
           ("Scenarios", "Override panel and live data tables (scenarios, sensitivities, tornado)"),
           ("Configs", "19 pre-defined configurations compared side by side (editable)"),
           ("Sources", "Where the assumptions come from")]
    for name, desc in toc:
        r = B.nr()
        ws.write_url(r, 1, f"internal:'{name}'!A1", B.f(None, font_color=BLUE, underline=1),
                     string=name)
        B.put(r, 2, desc, num=None)
    B.skip()
    B.band("Model checks")
    checks = [
        ("chk_bs", "Balance sheet balances (all years)",
         '=IF(SUMPRODUCT(ABS({#bs_chk}))<0.01,"OK","ERROR")'),
        ("chk_cash", "Cash never negative",
         '=IF(MIN({#bs_cash})>=-0.001,"OK","ERROR")'),
        ("chk_su", "Sources of funds = uses of funds",
         '=IF(ABS({$u_tot}-{$s_tot})<0.001,"OK","ERROR")'),
        ("chk_mix", "Every bean mix adds up to 100%",
         '=IF(SUMPRODUCT(ABS(MixCheck-1))<0.0001,"OK","ERROR")'),
        ("chk_rev", "Revenue mix shares between 0% and 100%",
         '=IF(AND({$food_sh}>=0,{$food_sh}<=1),"OK","ERROR")'),
        ("chk_tv", "WACC above terminal growth",
         '=IF({$wacc}>{$g_used},"OK","ERROR")'),
        ("chk_cap", "Seating capacity does not cap demand",
         '=IF(SUMPRODUCT(--({#bills_dem}>{#cap_bills}+0.001))=0,"OK","INFO: capacity binds")'),
        ("chk_ovr", "Scenarios-sheet overrides switched off",
         '=IF(AND({$o_scn}=0,{$o_cfg}=0,{$o_loc}=0,{$o_prop}=0,{$o_roast}=0,{$o_mix}=0,'
         '{$o_bills}=1,{$o_atv}=1,{$o_rent}=1,{$o_green}=1,{$o_capex}=1,{$o_staff}=1,'
         '{$o_wacc}=0,{$o_g}=0,{$o_tv}=0,{$o_ts}=0,{$o_whs}=0),"OK","INFO: overrides active")'),
    ]
    first = B.r["Cover"]
    for key, label, fml in checks:
        r = B.nr()
        B._set(key, r, 3)
        B.put(r, 1, label, num=None)
        B.put(r, 3, fml, num=None, bold=True, align="center")
    last = B.r["Cover"] - 1
    r = B.nr()
    B.put(r, 1, "Overall model status", num=None, bold=True, top=1)
    B.put(r, 2, None, top=1)
    B.put(r, 3, f'=IF(COUNTIF(D{first + 1}:D{last - 1},"OK")={last - first - 1},"ALL CHECKS OK",'
                f'"REVIEW")', num=None, bold=True, align="center", top=1)
    ok = B.f(None, bold=True, bg_color="#D8F0DC", font_color="#1E6B2D", align="center")
    bad = B.f(None, bold=True, bg_color="#F8D7DA", font_color="#9C1C1C", align="center")
    info = B.f(None, bold=True, bg_color="#FFF1CC", font_color="#8A5A00", align="center")
    rng = f"D{first + 1}:D{r + 1}"
    ws.conditional_format(rng, {"type": "text", "criteria": "begins with", "value": "OK",
                                "format": ok})
    ws.conditional_format(rng, {"type": "text", "criteria": "begins with", "value": "ALL",
                                "format": ok})
    ws.conditional_format(rng, {"type": "text", "criteria": "begins with", "value": "INFO",
                                "format": info})
    ws.conditional_format(rng, {"type": "text", "criteria": "begins with", "value": "ERR",
                                "format": bad})
    ws.conditional_format(rng, {"type": "text", "criteria": "begins with", "value": "REV",
                                "format": bad})
    B.skip()
    B.band("Switches")
    r = B.nr()
    B._set("circ", r, 3)
    B.put(r, 1, "Circularity switch (1 = interest on average balances)", num=None)
    B.put(r, 2, "0 = interest on opening balances (no circular reference). 1 needs iterative "
                "calculation (enabled in this file).", num=None, italic=True, color=GREY,
          text_wrap=True)
    B.put(r, 3, 0, num="idx", align="center", bold=True)
    ws.set_row(r, 30)
    ws.data_validation(r, 3, r, 3, {"validate": "integer", "criteria": "between", "minimum": 0,
                                    "maximum": 1})
    B.define("Circ", f"=Cover!$D${r + 1}")
    B.skip()
    B.band("Conventions")
    conv = [("Blue on cream", "Hard-coded input: change these", dict(font_color=BLUE, bg_color=INFILL)),
            ("Black", "Formula on the same sheet", dict(font_color="#000000")),
            ("Green", "Formula linking to another sheet", dict(font_color="#00803C")),
            ("Units", "₹ lakh unless the Units column says otherwise; rupee inputs are in ₹", {}),
            ("Timeline", "Y0 = FY27 (fit-out, pre-opening; ends 31 Mar 2027). Y1-Y10 = FY28-FY37. "
                         "Annual periods, fiscal year to 31 March", {}),
            ("Signs", "Income statement costs and cash outflows are shown as negatives", {}),
            ("Tax", "Corporate tax under s.115BAA, 25.168% incl. surcharge & cess; WDV tax "
                    "depreciation; losses carried forward", {}),
            ("Leases", "Rent is an operating expense (Indian GAAP / AS for an unlisted SME, "
                       "no Ind AS 116 right-of-use asset)", {})]
    for a, b, st in conv:
        r = B.nr()
        ws.write_string(r, 1, a, B.f(None, bold=True, **st))
        B.put(r, 2, b, num=None)
    B.skip()
    B.band("How to use")
    steps = ["1. Inputs sheet, section 1: pick Location, Premises (Rent / Own), Roasting route, "
             "Bean mix and Scenario from the drop-downs.",
             "2. Read the result on the Dashboard; every statement and schedule is on the Model "
             "and DCF sheets.",
             "3. Change any blue cell (Inputs, Locations, Sourcing, Capex, Configs) to test your "
             "own numbers.",
             "4. Scenarios sheet: live data tables re-run the whole model for every scenario, "
             "configuration and sensitivity. Leave its override cells at their defaults.",
             "5. Configs sheet: edit or add combinations; their results update automatically.",
             "6. If Excel is set to 'Automatic except data tables', press F9 to refresh the tables."]
    for t in steps:
        r = B.nr()
        B.put(r, 1, t, num=None)


# =============================================================================== Inputs
def inputs(B):
    B.use("Inputs")
    B.ws["Inputs"].set_column(3, 3, 20)
    B.title("Inputs & Drivers", "Blue cells are inputs. Rupee inputs in ₹ (not lakh). "
            "Driver rows marked Live are picked by the Scenario switch.")
    B.timeline_header("in_fy", "in_t")
    B.band("1. Configuration: choose what to model")
    dv = lambda name: {"validate": "list", "source": "=" + name}  # noqa: E731
    sel = A.DEFAULT_SELECTION
    B.sc("sel_loc", "Location", "list", sel["location"], dv=dv("LocList"),
         note="Prahladnagar (base case), Sindhu Bhavan Road, GIFT City, Sanand: see Locations")
    B.sc("sel_prop", "Premises", "list", sel["property"], dv=dv("PropList"),
         note="Rent a unit, or buy it (60% funded by a loan against property)")
    B.sc("sel_roast", "Coffee roasting route", "list", sel["roasting"], dv=dv("RoastList"),
         note="Buy roasted beans / toll-roast your own green coffee / own 3 kg roaster")
    B.sc("sel_mix", "Bean mix", "list", sel["mix"], dv=dv("MixList"),
         note="Value / Specialty / Premium / House blends: see Sourcing")
    B.sc("sel_scn", "Scenario", "list", sel["scenario"], dv=dv("ScnList"),
         note="Best / Base / Worst drivers below")
    B.skip()
    B.head("Active configuration (after any Scenarios-sheet overrides)")
    act = [("loc", "Location", "LocList", "CfgLoc", "sel_loc", "o_loc"),
           ("prop", "Premises", "PropList", "CfgProp", "sel_prop", "o_prop"),
           ("roast", "Roasting route", "RoastList", "CfgRoast", "sel_roast", "o_roast"),
           ("mix", "Bean mix", "MixList", "CfgMix", "sel_mix", "o_mix")]
    for k, lab, lst, cfg, selk, ovr in act:
        r = B.sc("a_" + k, lab + " (index)", "#",
                 f"=IF({{${ovr}}}>0,{{${ovr}}},IF({{$o_cfg}}>0,MATCH(INDEX({cfg},{{$o_cfg}}),"
                 f"{lst},0),MATCH({{${selk}}},{lst},0)))", num="idx")
        B._set("a_" + k + "_n", r, 5)
        B.put(r, 5, B.fx(f"=INDEX({lst},{{$a_{k}}})"), num=None, bold=True)
    r = B.sc("a_scn", "Scenario (index)", "#",
             "=IF({$o_scn}>0,{$o_scn},MATCH({$sel_scn},ScnList,0))", num="idx")
    B._set("a_scn_n", r, 5)
    B.put(r, 5, B.fx("=INDEX(ScnList,{$a_scn})"), num=None, bold=True)
    B.sc("is_own", "Owned premises flag", "1/0", "=IF({$a_prop}=2,1,0)", num="idx")
    B.sc("is_inh", "In-house roastery flag", "1/0", "=IF({$a_roast}=3,1,0)", num="idx")
    B.sc("own_label", "Own-label beans flag (toll or in-house)", "1/0", "=IF({$a_roast}>=2,1,0)",
         num="idx")
    r = B.sc("cfg_label", "Configuration label", "text",
             '={$a_loc_n}&" | "&{$a_prop_n}&" | "&{$a_roast_n}&" | "&{$a_mix_n}&" mix | "'
             '&{$a_scn_n}&" case"', num=None)
    B.skip()
    B.band("2. General")
    B.sc("first_fy", "Year 0 (fit-out year) ends 31 March", "FY", A.FIRST_FY, num="idx",
         note="Y0 = FY2026-27: lease/purchase, fit-out, hiring. Café opens 1 April 2027 (Y1)")
    r = B.sc("lakh", "Rupees per lakh", "₹", A.LAKH, num="int")
    B.define("Lakh", f"=Inputs!$D${r + 1}")
    r = B.sc("tax_rate", "Corporate tax rate (s.115BAA)", "%", A.TAX_RATE, num="pct2",
             note="22% + 10% surcharge + 4% cess = 25.168%; no MAT under 115BAA")
    B.define("TaxRate", f"=Inputs!$D${r + 1}")
    B.skip()

    B.band("3. Scenario drivers: Best / Base / Worst (Live row = selected scenario)")
    for key, (label, unit, rows) in A.DRIVERS.items():
        B.head(label)
        for sname, vals in zip(A.SCENARIOS, rows):
            B.line(f"{key}_{sname.lower()}", sname, unit, [None] + list(vals),
                   num="ix" if unit == "x" else "pct")
        B.line(key, "Live", unit, "=CHOOSE({$a_scn},{%s_best},{%s_base},{%s_worst})" % (key, key, key),
               num="ix" if unit == "x" else "pct", start=1, bold=True)
    B.head("Wholesale ramp-up (in-house roastery only)")
    B.line("whs_ramp", "Share of mature wholesale volume", "%", [None] + A.WHOLESALE_RAMP, num="pct")
    B.skip()
    r = B.nr()
    hd = dict(bold=True, bg_color=HEAD_FILL, bottom=1, align="center")
    B.put(r, 1, "Single-value drivers", num=None, bold=True, bg_color=HEAD_FILL, bottom=1)
    B.put(r, 2, "Units", num=None, **hd)
    B.put(r, 3, "Live", num=None, **hd)
    for j, sname in enumerate(A.SCENARIOS):
        B.put(r, 5 + j, sname, num=None, **hd)
    for key, (label, unit, vals) in A.SINGLE_DRIVERS.items():
        num = "x" if unit == "x" else ("pct" if unit == "%" else "int")
        r = B.nr()
        B._set(key, r, 3)
        B.put(r, 1, label, num=None, indent=1)
        B.put(r, 2, unit, num=None, italic=True, color=GREY)
        for j, v in enumerate(vals):
            B._set(f"{key}_{j}", r, 5 + j)
            B.put(r, 5 + j, v, num=num)
        B.put(r, 3, B.fx("=CHOOSE({$a_scn},{$%s_0},{$%s_1},{$%s_2})" % (key, key, key)), num=num,
              bold=True)
    B.skip()

    B.band("4. Revenue, menu & capacity")
    R = A.REVENUE
    rows = [("bev_share", "Beverages share of café revenue", "%", R["bev_share"], ""),
            ("retail_share", "Retail beans share (bought-in bags)", "%", R["retail_share"], ""),
            ("own_label_uplift", "Extra retail share with own-label beans", "%",
             R["own_label_uplift"], "Applies to toll and in-house routes"),
            ("bev_price", "Average beverage price (FY28)", "₹", R["bev_price"],
             "Used only to convert beverage sales into cups"),
            ("coffee_share", "Beverages that contain coffee", "%", R["coffee_share"], ""),
            ("grams", "Coffee per coffee beverage", "g", R["grams"], "Double shot 18 g; filter 15-18 g"),
            ("milk_other", "Milk, syrups, sugar & garnish per beverage", "₹", R["milk_other"], ""),
            ("takeaway_share", "Takeaway share of bills (needs packaging)", "%", R["takeaway_share"], ""),
            ("pack_per_bill", "Packaging per takeaway/delivery bill", "₹", R["pack_per_bill"], ""),
            ("food_cogs", "Food cost as % of food sales", "%", R["food_cogs"], ""),
            ("resale_margin", "Gross margin on bought-in retail bags", "%", R["resale_margin"], ""),
            ("whs_selling", "Wholesale selling & delivery cost", "% of sales", R["whs_selling"], ""),
            ("whs_growth", "Wholesale volume growth after Y3", "% p.a.", R["whs_growth"], ""),
            ("cost_infl", "Food, packaging & supplies inflation", "% p.a.", R["cost_infl"], ""),
            ("max_turns", "Maximum seat turns per day (capacity cap)", "x", A.CAPACITY["max_turns"],
             "Dine-in bills per seat per day at full capacity")]
    for k, lab, u, v, n in rows:
        B.sc(k, lab, u, v, num="int" if u in ("₹", "₹/kg", "g") else ("x" if u == "x" else "pct"),
             note=n or None)
    B.head("Derived (do not edit)")
    B.sc("ret_eff", "Retail beans share, active route", "%",
         "={$retail_share}+{$own_label}*{$own_label_uplift}", num="pct")
    B.sc("food_sh", "Food share of café revenue", "%", "=1-{$bev_share}-{$ret_eff}", num="pct")
    B.sc("cups_per_bill", "Beverages per bill", "#", "={$Lx_atv}*{$bev_share}/{$bev_price}",
         num="lakh2")
    B.skip()

    B.band("5. People")
    r = B.nr()
    hd = dict(bold=True, bg_color=HEAD_FILL, bottom=1, align="center")
    for c, t in [(1, "Role"), (2, "Headcount"), (3, "Monthly salary ₹"), (5, "Roastery only"),
                 (6, "Monthly ₹")]:
        B.put(r, c, t, num=None, **hd)
    first = B.r["Inputs"]
    for role, hc, sal, roast in A.STAFF:
        r = B.nr()
        B.put(r, 1, role, num=None, indent=1)
        B.put(r, 2, hc, num="int")
        B.put(r, 3, sal, num="int")
        B.put(r, 5, 1 if roast else 0, num="idx", align="center")
        B.put(r, 6, f"=C{r + 1}*D{r + 1}", num="int")
    last = B.r["Inputs"] - 1
    hc_r, sal_r, fl_r = (f"$C${first + 1}:$C${last + 1}", f"$D${first + 1}:$D${last + 1}",
                         f"$F${first + 1}:$F${last + 1}")
    B.sc("payroll_cafe", "Café roster, monthly", "₹",
         f"=SUMPRODUCT({hc_r},{sal_r},1-{fl_r})", num="int")
    B.sc("payroll_roast", "Roastery roster, monthly", "₹", f"=SUMPRODUCT({hc_r},{sal_r},{fl_r})",
         num="int")
    O = A.OPEX
    B.sc("staff_load", "PF, ESI, bonus, meals & uniforms", "% of salary", O["staff_load"], num="pct")
    B.sc("wage_growth", "Annual wage increase", "% p.a.", O["wage_growth"], num="pct",
         note="Gujarat minimum wage ₹13,325-13,897/month from April 2026")
    B.sc("staff_elastic", "Extra staff per 1% bills above steady state", "%",
         A.CAPACITY["staff_elastic"], num="pct")
    B.sc("payroll_m", "Active monthly payroll (location staffing factor applied)", "₹",
         "={$payroll_cafe}*{$Lx_staff_f}+{$is_inh}*{$payroll_roast}", num="int", bold=True)
    B.skip()

    B.band("6. Operating costs")
    rows = [("kwh_psf", "Electricity use", "kWh/sqft/mth", O["kwh_psf"], "x"),
            ("tariff", "Electricity tariff, all-in (FY28)", "₹/kWh", O["tariff"], "lakh2",
             "Torrent Power non-RGP: 455 paise/unit energy + fixed + FPPPA + duty"),
            ("tariff_growth", "Tariff increase", "% p.a.", O["tariff_growth"], "pct"),
            ("gas_water_m", "LPG/PNG, water & cleaning supplies", "₹/mth", O["gas_water_m"], "int"),
            ("mkt_y1", "Marketing, launch year", "% of revenue", O["mkt_y1"], "pct"),
            ("mkt", "Marketing, later years", "% of revenue", O["mkt"], "pct"),
            ("rm_pct", "Repairs & maintenance", "% of revenue", O["rm_pct"], "pct"),
            ("amc", "Equipment AMC (espresso, grinders, RO)", "₹/yr", O["amc"], "int"),
            ("roaster_amc", "Roaster AMC & afterburner service", "₹/yr", O["roaster_amc"], "int"),
            ("aggregator", "Aggregator commission incl. GST & fees", "% of delivery sales",
             O["aggregator"], "pct", "Swiggy/Zomato effective 24-30% incl. discounts"),
            ("payment", "Card/UPI processing", "% of dine-in sales", O["payment"], "pct"),
            ("admin_fixed", "Admin, accounts, software, insurance, licences", "₹/yr",
             O["admin_fixed"], "int"),
            ("misc_pct", "Miscellaneous", "% of revenue", O["misc_pct"], "pct"),
            ("opex_infl", "General cost inflation", "% p.a.", O["opex_infl"], "pct"),
            ("rent_esc", "Rent escalation", "% p.a.", O["rent_esc"], "pct",
             "Equivalent to ~15% every 3 years"),
            ("roastery_area", "Extra area for an in-house roastery", "sqft", O["roastery_area"], "int")]
    for row in rows:
        k, lab, u, v, num = row[:5]
        B.sc(k, lab, u, v, num=num, note=row[5] if len(row) > 5 else None)
    B.skip()

    B.band("7. Pre-opening (Y0, expensed)")
    P = A.PREOPEN
    for k, lab, u, num in [("rent_months", "Rent-free fit-out not available: rent paid", "months", "x"),
                           ("training_months", "Payroll before opening (hiring & training)", "months", "x"),
                           ("launch_mkt", "Launch marketing", "₹", "int"),
                           ("licences", "FSSAI, Shop Act, fire NOC, GST, trade licence", "₹", "int"),
                           ("recruitment", "Recruitment", "₹", "int"),
                           ("utilities_misc", "Utilities & sundry before opening", "₹", "int")]:
        B.sc(k, lab, u, P[k], num=num)
    B.skip()

    B.band("8. Capex rules & depreciation")
    C = A.CAPEX_OTHER
    for k, lab, u, num, n in [
            ("maint_pct", "Maintenance capex", "% of revenue", "pct", "From Y1"),
            ("refurb_year", "Refurbishment year", "year", "idx", "Interiors & furniture refresh"),
            ("refurb_pct", "Refurbishment cost", "% of initial interiors+furniture", "pct", None),
            ("stamp", "Stamp duty & registration (own case)", "% of price", "pct",
             "Gujarat: 4.9% stamp duty + 1% registration"),
            ("legal", "Legal & brokerage on purchase", "% of price", "pct", None),
            ("land_share", "Land share of property cost (not depreciated)", "%", "pct", None),
            ("ongoing_life", "Book life of maintenance capex", "years", "idx", None),
            ("ongoing_tax", "Tax WDV rate on maintenance capex", "%", "pct", "Half rate in year added")]:
        B.sc(k, lab, u, C[k], num=num, note=n)
    B.skip()

    B.band("9. Working capital")
    W = A.WC
    for k, lab in [("ar_delivery_days", "Aggregator settlement (delivery sales)"),
                   ("ar_wholesale_days", "Wholesale customer credit"),
                   ("inv_days", "Inventory (food, milk, packaging, bought-in beans)"),
                   ("green_inv_days", "Coffee inventory if roasting your own (green stock)"),
                   ("ap_days", "Supplier credit")]:
        B.sc(k, lab, "days", W[k], num="int")
    B.skip()

    B.band("10. Financing")
    Fn = A.FIN
    for k, lab, u, num, n in [
            ("equity_threshold", "All-equity if total capital need is at or below", "₹", "int",
             "Per brief: ₹10-15 lakh projects are fully equity funded"),
            ("debt_pct_rent", "Term loan, rented premises", "% of capex", "pct",
             "MSME term loan under CGTMSE (collateral-free)"),
            ("debt_pct_own", "Loan, owned premises", "% of capex + property", "pct",
             "Lease-rental / loan against commercial property"),
            ("rate_rent", "Interest rate, rented case", "% p.a.", "pct", "Repo 5.50% + MSME spread"),
            ("rate_own", "Interest rate, owned case", "% p.a.", "pct", None),
            ("tenor_rent", "Tenor, rented case", "years", "idx", "Equal principal instalments"),
            ("tenor_own", "Tenor, owned case", "years", "idx", None),
            ("revolver_rate", "Cash-credit (overdraft) rate", "% p.a.", "pct", "Draws only if cash dips"),
            ("min_cash", "Minimum cash balance", "₹", "int", None),
            ("reserve_m", "Ramp-up reserve funded at start", "months of Y1 fixed costs", "x",
             "Covers early losses so the café does not lean on an overdraft"),
            ("cash_rate", "Interest earned on cash", "% p.a.", "pct", None),
            ("payout", "Dividend payout of profit", "%", "pct", "0% = all cash retained")]:
        B.sc(k, lab, u, Fn[k], num=num, note=n)
    B.skip()

    B.band("11. Valuation")
    D = A.DCF
    for k, lab, u, num, n in [
            ("rf", "Risk-free rate (India 10-yr G-sec)", "%", "pct2", "7.29% on 8 Oct 2026"),
            ("erp", "Equity risk premium, India", "%", "pct2", "Damodaran Jan 2026: 4.23% mature + 2.85% CRP"),
            ("beta_u", "Unlevered beta (restaurants & dining)", "x", "x", None),
            ("specific", "Size & single-outlet premium", "%", "pct2", "Key-person, single-site risk"),
            ("g", "Terminal growth (nominal)", "%", "pct2", "Below nominal GDP; one outlet"),
            ("exit_mult", "Exit EV/EBITDA cross-check", "x", "x", "Single cafés trade at 1.5-3x SDE"),
            ("sell_cost", "Property selling cost (own case)", "%", "pct", None),
            ("cgt", "Capital-gains tax on property gain (own case)", "%", "pct",
             "12.5% LTCG + surcharge & cess"),
            ("mid_year", "Mid-year discounting (1 = on)", "1/0", "idx", None),
            ("salvage", "Resale value of café capex if shut in Y3", "% of cost", "pct",
             "Used for the shut-down downside metric")]:
        B.sc(k, lab, u, D[k], num=num, note=n)
    B.skip()

    B.band("Lists (drop-down sources)")
    for key, lab, vals, name in [("lst_prop", "Premises options", A.PROPERTY, "PropList"),
                                 ("lst_scn", "Scenario options", A.SCENARIOS, "ScnList")]:
        r = B.nr()
        B.put(r, 1, lab, num=None, indent=1)
        for j, v in enumerate(vals):
            B.put(r, 5 + j, v, num=None, inp=True)
        B.define(name, f"=Inputs!$F${r + 1}:${TC[len(vals)]}${r + 1}")


# =============================================================================== Locations
def locations(B):
    ws = B.use("Locations")
    ws.set_column(0, 0, 2)
    ws.set_column(1, 1, 38)
    ws.set_column(2, 2, 12)
    ws.set_column(3, 7, 17)
    ws.set_column(8, 8, 2)
    ws.set_column(9, 9, 70)
    B.title("Location library", "Four candidate sites. Edit any blue cell; column H feeds the model.")
    r = B.nr()
    hd = dict(bold=True, bg_color=HEAD_FILL, bottom=1, align="center", text_wrap=True)
    ws.set_row(r, 30)
    B.put(r, 1, "Parameter", num=None, **{**hd, "align": "left"})
    B.put(r, 2, "Units", num=None, **hd)
    for j, name in enumerate(A.LOCATIONS):
        B.put(r, 3 + j, name, num=None, inp=True, bold=True, align="center", bottom=1)
    B.put(r, 7, "=INDEX(D{0}:G{0},{{$a_loc}})".format(r + 1), num=None, bold=True,
          bg_color="#E2EFDA", align="center", bottom=1)
    B.put(r, 9, "Notes & evidence", num=None, **{**hd, "align": "left"})
    B.define("LocList", f"=Locations!$D${r + 1}:$G${r + 1}")
    for key, label, unit, vals, note in A.LOCATION_ROWS:
        r = B.nr()
        num = "pct" if unit in ("%", "% p.a.") else ("x" if unit == "x" else "int")
        B.put(r, 1, label, num=None, indent=1)
        B.put(r, 2, unit, num=None, italic=True, color=GREY)
        for j, v in enumerate(vals):
            B._set(f"L_{key}_{j}", r, 3 + j)
            B.put(r, 3 + j, v, num=num)
        B._set("Lx_" + key, r, 7)
        B.put(r, 7, f"=INDEX(D{r + 1}:G{r + 1},{{$a_loc}})", num=num, bold=True, bg_color="#E2EFDA")
        if note:
            B.put(r, 9, note, num=None, italic=True, color=GREY)
    B.skip()
    B.head("Derived indicators (Base footfall, Specialty mix, rented)")
    derived = [
        ("Rent per seat per month", "₹", "=D{area}*D{rent}/D{seats}", "int"),
        ("Café revenue at steady state (FY28 prices)", "₹ lakh/yr",
         "=D{bills}*D{atv}*D{days}/Lakh", "lakh"),
        ("Rent as % of steady-state revenue", "%", "=D{area}*D{rent}*12/(D{bills}*D{atv}*D{days})", "pct"),
        ("Interiors cost", "₹ lakh", "=D{area}*D{fit}/Lakh", "lakh"),
        ("Purchase cost of the unit (own case)", "₹ lakh", "=D{area}*D{buy}/Lakh", "lakh"),
        ("Gross rental yield on purchase price", "%", "=D{rent}*12/D{buy}", "pct"),
    ]
    rowno = {k: B.reg.get(f"L_{k}_0", (None, 0, 0))[1] + 1 for k in LOC_KEYS}
    for label, unit, tmpl, num in derived:
        r = B.nr()
        B.put(r, 1, label, num=None, indent=1)
        B.put(r, 2, unit, num=None, italic=True, color=GREY)
        for j in range(5):
            col = "DEFGH"[j]
            f = tmpl.format(area=rowno["area"], rent=rowno["rent_psf"], seats=rowno["seats"],
                            bills=rowno["bills_ss"], atv=rowno["atv"], days=rowno["op_days"],
                            fit=rowno["fitout_psf"], buy=rowno["purchase_psf"])
            B.put(r, 3 + j, f.replace("D", col), num=num, bold=(j == 4),
                  bg_color="#E2EFDA" if j == 4 else None)
    B.skip()
    B.head("Site profiles")
    for j, name in enumerate(A.LOCATIONS):
        r = B.nr()
        ws.set_row(r, 32)
        B.put(r, 1, name, num=None, bold=True, indent=1, valign="top")
        ws.merge_range(r, 2, r, 9, A.LOCATION_PROFILE[name],
                       B.f(None, text_wrap=True, valign="top", font_color="#000000"))


# =============================================================================== Sourcing
def sourcing(B):
    ws = B.use("Sourcing")
    ws.set_column(0, 0, 2)
    ws.set_column(1, 1, 40)
    ws.set_column(2, 2, 10)
    ws.set_column(3, 4, 13)
    ws.set_column(5, 9, 12)
    ws.set_column(10, 10, 2)
    ws.set_column(11, 11, 60)
    B.title("Coffee sourcing & roasting economics",
            "Green prices in ₹/kg (Oct 2026). Mix shares must add to 100%. Column J = active mix.")
    S = A.SOURCING
    B.head("Roasting & packing parameters")
    for k, lab, u, num, n in [
            ("shrink", "Roast loss (moisture & chaff)", "%", "pct", "1 kg green -> 0.84 kg roasted"),
            ("toll_fee", "Toll-roasting fee", "₹/kg roasted", "int", "Contract roaster roasts your green"),
            ("freight", "Inbound freight, green or roasted", "₹/kg", "int", "Chikmagalur/Coorg to Ahmedabad"),
            ("inhouse_var", "In-house roasting variable cost (LPG, power, bags)", "₹/kg roasted", "int",
             "Roaster labour & AMC are in fixed costs"),
            ("cafe_pack", "Café bulk packing", "₹/kg", "int", None),
            ("retail_pack", "Retail bag, valve & label", "₹/kg", "int", "₹12 per 250 g bag"),
            ("whs_pack", "Wholesale packing", "₹/kg", "int", None)]:
        B.sc(k, lab, u, S[k], num=num, note=n, note_col=5)
    B.skip()
    r = B.nr()
    hd = dict(bold=True, bg_color=HEAD_FILL, bottom=1, align="center", text_wrap=True)
    ws.set_row(r, 30)
    for c, t in [(1, "Green coffee type"), (2, "Units"), (3, "Green ₹/kg"),
                 (4, "Roasted, bought ₹/kg")]:
        B.put(r, c, t, num=None, **hd)
    for j, m in enumerate(A.MIXES):
        B.put(r, 5 + j, m, num=None, inp=True, bold=True, align="center", bottom=1)
    B.put(r, 9, "=INDEX(F{0}:I{0},{{$a_mix}})".format(r + 1), num=None, bold=True,
          bg_color="#E2EFDA", align="center", bottom=1)
    B.define("MixList", f"=Sourcing!$F${r + 1}:$I${r + 1}")
    first = B.r["Sourcing"]
    for i, name in enumerate(A.GREEN_TYPES):
        r = B.nr()
        B.put(r, 1, name, num=None, indent=1)
        B.put(r, 2, "share", num=None, italic=True, color=GREY)
        B.put(r, 3, A.GREEN_PRICE[i], num="int")
        B.put(r, 4, A.WHOLESALE_ROASTED[i], num="int")
        for j, m in enumerate(A.MIXES):
            B.put(r, 5 + j, A.MIX_SHARES[m][i], num="pct")
        B.put(r, 9, f"=INDEX(F{r + 1}:I{r + 1},{{$a_mix}})", num="pct", bg_color="#E2EFDA")
    last = B.r["Sourcing"] - 1
    rows = {}

    def mixrow(key, label, unit, tmpl, num="int", bold=False, top=False):
        r = B.nr()
        rows[key] = r + 1
        st = {"bold": True} if bold else {}
        if top:
            st["top"] = 1
        B.put(r, 1, label, num=None, indent=0 if bold else 1, **st)
        B.put(r, 2, unit, num=None, italic=True, color=GREY, **({"top": 1} if top else {}))
        for c in (3, 4):
            if top:
                B.put(r, c, None, top=1)
        for j in range(4):
            col = "FGHI"[j]
            B.put(r, 5 + j, B.fx(tmpl.replace("§", col)) if isinstance(tmpl, str) else tmpl[j],
                  num=num, **st)
        B._set("sx_" + key, r, 9)
        B.put(r, 9, f"=INDEX(F{r + 1}:I{r + 1},{{$a_mix}})", num=num, bg_color="#E2EFDA", **st)
        return r

    r = mixrow("chk", "Share total (must be 100%)", "%", f"=SUM(§{first + 1}:§{last + 1})",
               num="pct", top=True)
    B.define("MixCheck", f"=Sourcing!$F${r + 1}:$I${r + 1}")
    mixrow("green", "Blended green price", "₹/kg",
           f"=SUMPRODUCT($D${first + 1}:$D${last + 1},§{first + 1}:§{last + 1})")
    mixrow("whs", "Blended roasted price if bought", "₹/kg",
           f"=SUMPRODUCT($E${first + 1}:$E${last + 1},§{first + 1}:§{last + 1})")
    mixrow("glink", "Green coffee in 1 kg roasted", "₹/kg roasted", "=§%d/(1-{$shrink})" % rows["green"])
    B.skip()
    B.head("Cost per kg of roasted coffee, by route (FY28, before green-price index)")
    mixrow("conv_buy", "Roaster's margin & conversion (buy roasted)", "₹/kg",
           "=§%d-§%d" % (rows["whs"], rows["glink"]))
    mixrow("conv_toll", "Toll fee + freight (toll roasting)", "₹/kg", "={$toll_fee}+{$freight}")
    mixrow("conv_inh", "Variable roasting cost + freight (in-house)", "₹/kg",
           "={$inhouse_var}+{$freight}")
    mixrow("cost_buy", "Total: Buy roasted", "₹/kg", "=§%d+§%d" % (rows["glink"], rows["conv_buy"]),
           bold=True, top=True)
    mixrow("cost_toll", "Total: Toll roasting", "₹/kg", "=§%d+§%d" % (rows["glink"], rows["conv_toll"]),
           bold=True)
    mixrow("cost_inh", "Total: In-house roastery (variable only)", "₹/kg",
           "=§%d+§%d" % (rows["glink"], rows["conv_inh"]), bold=True)
    mixrow("cup_cost", "Coffee cost per 18 g double shot, toll route", "₹",
           "=§%d*18/1000" % rows["cost_toll"], num="lakh")
    B.skip()
    B.head("Demand & price effects of the bean mix")
    for key, label, unit, vals, note in A.MIX_EFFECTS:
        r = mixrow(key, label, unit, vals, num="pct" if unit == "%" else "int")
        B.put(r, 11, note, num=None, italic=True, color=GREY)
    B.skip()
    B.head("Roasting routes (drop-down list)")
    r = B.nr()
    B.put(r, 1, "Route options", num=None, indent=1)
    for j, v in enumerate(A.ROASTING):
        B.put(r, 5 + j, v, num=None, inp=True)
    B.define("RoastList", f"=Sourcing!$F${r + 1}:$H${r + 1}")
    B.skip()
    B.head("Active coffee cost (feeds the Model)")
    B.sc("green_link_act", "Green coffee per kg roasted, active mix", "₹/kg", "={$sx_glink}",
         num="int", col=9)
    B.sc("conv_act", "Conversion cost per kg, active route", "₹/kg",
         "=CHOOSE({$a_roast},{$sx_conv_buy},{$sx_conv_toll},{$sx_conv_inh})", num="int", col=9)
    B.sc("cost_act", "Roasted coffee cost per kg (FY28 basis)", "₹/kg",
         "={$green_link_act}+{$conv_act}", num="int", col=9, bold=True)
    B.sc("retail_price_act", "Own-label retail price", "₹/kg", "={$sx_retail_price}", num="int", col=9)
    B.sc("whs_price_act", "Wholesale price, active mix", "₹/kg", "={$sx_whs_price}", num="int", col=9)
    B.sc("atv_prem_act", "Average-bill premium of active mix", "%", "={$sx_atv_prem}", num="pct",
         col=9)
    B.sc("foot_eff_act", "Footfall effect of active mix", "%", "={$sx_foot_eff}", num="pct", col=9)


# =============================================================================== Capex
def capex(B):
    ws = B.use("Capex")
    ws.set_column(0, 0, 2)
    ws.set_column(1, 1, 50)
    ws.set_column(2, 2, 13)
    ws.set_column(3, 3, 13)
    ws.set_column(4, 4, 10)
    ws.set_column(5, 5, 12)
    ws.set_column(6, 6, 12)
    ws.set_column(7, 7, 2)
    ws.set_column(8, 8, 55)
    B.title("Capex, property & funding", "Unit costs in ₹ (ex-GST, Oct 2026). Amounts in ₹ lakh "
            "include the scenario capex-overrun and any Scenarios-sheet capex multiplier.")
    B.band("Equipment & fit-out")
    r = B.nr()
    hd = dict(bold=True, bg_color=HEAD_FILL, bottom=1, align="center", text_wrap=True)
    ws.set_row(r, 30)
    for c, t in [(1, "Item"), (2, "Basis"), (3, "Unit cost ₹"), (4, "Quantity"), (5, "Asset class"),
                 (6, "₹ lakh"), (8, "Notes")]:
        B.put(r, c, t, num=None, **hd)
    basis_txt = {"lump": "lump sum", "psf": "per sqft", "seat": "per seat", "roast": "in-house only",
                 "roast_psf": "roastery sqft", "loc_psf": "per sqft (site)"}
    notes = {"espresso": "La Marzocco Linea PB 2GR ₹11.26 lakh + GST; Brewlyn 2GR ₹6.30 lakh",
             "roaster": "Aaroasta (Rajkot) ARST-3, LPG, 6-9 kg/hour",
             "interiors": "Site-specific rate from Locations"}
    first = B.r["Capex"]
    for key, item, basis, val, cls in A.CAPEX_ITEMS:
        r = B.nr()
        B.put(r, 1, item, num=None, indent=1)
        B.put(r, 2, basis_txt[basis], num=None, italic=True, color=GREY)
        if basis in ("loc_psf", "roast_psf"):
            B.put(r, 3, "={$Lx_fitout_psf}", num="int")
        else:
            B.put(r, 3, val, num="int")
        qty = {"lump": "=1", "psf": "={$Lx_area}", "seat": "={$Lx_seats}", "roast": "={$is_inh}",
               "roast_psf": "={$is_inh}*{$roastery_area}", "loc_psf": "={$Lx_area}"}[basis]
        B.put(r, 4, qty, num="int")
        B.put(r, 5, cls, num=None, align="center")
        B._set("cx_" + key, r, 6)
        B.put(r, 6, f"=D{r + 1}*E{r + 1}*(1+{{$overrun}})*{{$e_capex}}/Lakh", num="lakh")
        if key in notes:
            B.put(r, 8, notes[key], num=None, italic=True, color=GREY)
    last = B.r["Capex"] - 1
    r = B.nr()
    B._set("cap_cafe", r, 6)
    B.put(r, 1, "Café & roastery capex", num=None, bold=True, top=1)
    for c in range(2, 6):
        B.put(r, c, None, top=1)
    B.put(r, 6, f"=SUM(G{first + 1}:G{last + 1})", num="lakh", bold=True, top=1)
    item_cls, item_amt = f"$F${first + 1}:$F${last + 1}", f"$G${first + 1}:$G${last + 1}"
    B.skip()

    B.band("Premises (own case)")
    B.sc("area_tot", "Area occupied (café + roastery if in-house)", "sqft",
         "={$Lx_area}+{$is_inh}*{$roastery_area}", num="int", col=6)
    B.sc("prop_psf", "Purchase price, active location", "₹/sqft", "={$Lx_purchase_psf}", num="int",
         col=6)
    B.sc("prop_price", "Purchase price", "₹ lakh", "={$is_own}*{$area_tot}*{$prop_psf}/Lakh", col=6)
    B.sc("prop_stamp", "Stamp duty & registration", "₹ lakh", "={$prop_price}*{$stamp}", col=6)
    B.sc("prop_legal", "Legal & brokerage", "₹ lakh", "={$prop_price}*{$legal}", col=6)
    B.sc("prop_cost", "Total property cost", "₹ lakh", "={$prop_price}+{$prop_stamp}+{$prop_legal}",
         col=6, bold=True)
    B.sc("prop_land", "of which land (not depreciated)", "₹ lakh", "={$prop_cost}*{$land_share}",
         col=6)
    B.sc("prop_bldg", "of which building", "₹ lakh", "={$prop_cost}-{$prop_land}", col=6)
    B.skip()

    B.band("Initial capex by asset class")
    r = B.nr()
    for c, t in [(1, "Asset class"), (3, "₹ lakh"), (4, "Book life"), (5, "Tax WDV rate")]:
        B.put(r, c, t, num=None, **hd)
    for cls in CLASSES:
        r = B.nr()
        B.put(r, 1, cls, num=None, indent=1)
        B._set("ci_" + cls, r, 3)
        if cls == "Building":
            B.put(r, 3, "={$prop_bldg}", num="lakh")
        elif cls == "Land":
            B.put(r, 3, "={$prop_land}", num="lakh")
        else:
            B.put(r, 3, f'=SUMIF({item_cls},"{cls}",{item_amt})', num="lakh")
        B._set("cl_" + cls, r, 4)
        B.put(r, 4, A.BOOK_LIFE[cls], num="idx", align="center")
        B._set("cr_" + cls, r, 5)
        B.put(r, 5, A.TAX_WDV[cls], num="pct")
    r = B.nr()
    B._set("cap_init_tot", r, 3)
    B.put(r, 1, "Total initial capex incl. property", num=None, bold=True, top=1)
    B.put(r, 2, None, top=1)
    B.put(r, 3, "=SUM({0})".format(B.area("ci_Interiors", "ci_Land").split("!")[-1]), num="lakh",
          bold=True, top=1)
    B.note("Book: straight line from Y1 (land not depreciated). Tax: Income-tax Act block rates, WDV; "
           "furniture & fittings 10%, plant & machinery 15%, computers 40%, buildings 10%.")
    B.skip()

    B.band("Sources & uses of funds (Y0)")
    B.sc("u_capex", "Café & roastery capex", "₹ lakh", "={$cap_cafe}", col=6)
    B.sc("u_prop", "Property purchase incl. stamp duty", "₹ lakh", "={$prop_cost}", col=6)
    B.sc("u_preop", "Pre-opening expenses", "₹ lakh", "={preop@F}", col=6)
    B.sc("u_dep", "Rent deposit (refundable)", "₹ lakh",
         "=(1-{$is_own})*{$Lx_deposit_m}*{$area_tot}*{$Lx_rent_psf}*{$e_rent}/Lakh", col=6)
    B.sc("u_cash", "Opening cash: minimum balance + ramp-up reserve", "₹ lakh",
         "={$min_cash}/Lakh+{$reserve_m}*{opex_fixed@1}/12", col=6)
    B.sc("u_tot", "Total capital requirement", "₹ lakh",
         "={$u_capex}+{$u_prop}+{$u_preop}+{$u_dep}+{$u_cash}", col=6, bold=True, top=True)
    B.skip()
    B.sc("debt_pct", "Loan share, active premises", "%",
         "=IF({$is_own}=1,{$debt_pct_own},{$debt_pct_rent})", num="pct", col=6)
    B.sc("s_debt", "Term loan", "₹ lakh",
         "=IF({$u_tot}*Lakh<={$equity_threshold},0,ROUND({$debt_pct}*({$u_capex}+{$u_prop}),1))",
         col=6, note="All-equity if the requirement is within ₹15 lakh, else loan on capex/property",
         note_col=8)
    B.sc("s_eq", "Promoter equity", "₹ lakh", "={$u_tot}-{$s_debt}", col=6)
    B.sc("s_tot", "Total sources", "₹ lakh", "={$s_debt}+{$s_eq}", col=6, bold=True, top=True)
    B.sc("gearing", "Debt / total capital", "%", "={$s_debt}/{$s_tot}", num="pct", col=6)
    B.sc("loan_rate", "Loan interest rate", "%", "=IF({$is_own}=1,{$rate_own},{$rate_rent})",
         num="pct", col=6)
    B.sc("loan_tenor", "Loan tenor", "years", "=IF({$is_own}=1,{$tenor_own},{$tenor_rent})",
         num="idx", col=6)


# =============================================================================== Model
def model(B):
    B.use("Model")
    B.title("Model: three statements & schedules", "₹ lakh unless stated. Statements contain links "
            "only; all workings are in the schedules below.")
    B.timeline_header("m_fy", "m_t", src="in_fy")
    L = B.line
    OP = 1  # first operating year index
    L("opf", "Operating flag", "1/0", "=IF({m_t}>=1,1,0)", num="idx")
    L("ix_cost", "Food & supplies price index", "x", "=(1+{$cost_infl})^MAX(0,{m_t}-1)", num="ix")
    L("ix_opex", "General cost index", "x", "=(1+{$opex_infl})^MAX(0,{m_t}-1)", num="ix")
    B.skip()

    # ---------------------------------------------------------------- income statement
    B.band("Income statement")
    L("is_rev_bev", "Beverages", "₹ lakh", "={rev_bev}")
    L("is_rev_food", "Food", "₹ lakh", "={rev_food}")
    L("is_rev_ret", "Retail beans & merchandise", "₹ lakh", "={rev_ret}")
    L("is_rev_whs", "Wholesale roasted beans", "₹ lakh", "={rev_whs}")
    L("is_rev", "Revenue", "₹ lakh", "=SUM({is_rev_bev}:{is_rev_whs})", bold=True, top=True)
    L("is_growth", "growth", "%", "=IF({is_rev@p}>0,{is_rev}/{is_rev@p}-1,0)", num="pct", italic=True,
      start=2)
    L("is_cogs", "Cost of goods sold", "₹ lakh", "=-{cogs}")
    L("is_gp", "Gross profit", "₹ lakh", "={is_rev}+{is_cogs}", bold=True, top=True)
    L("is_gm", "gross margin", "%", "=IF({is_rev}>0,{is_gp}/{is_rev},0)", num="pct", italic=True)
    L("is_staff", "Staff costs", "₹ lakh", "=-{staff}")
    L("is_occ", "Rent, CAM & property tax", "₹ lakh", "=-({rent}+{cam}+{ptax})")
    L("is_util", "Electricity, gas & water", "₹ lakh", "=-({power}+{gaswater})")
    L("is_mkt", "Marketing", "₹ lakh", "=-{mkt_c}")
    L("is_chan", "Aggregator & payment fees", "₹ lakh", "=-({aggr}+{payfee})")
    L("is_rm", "Repairs, maintenance & AMC", "₹ lakh", "=-({rm_var}+{amc_c})")
    L("is_adm", "Admin, wholesale selling & other", "₹ lakh", "=-({admin}+{misc}+{whs_sell})")
    L("is_pre", "Pre-opening expenses", "₹ lakh", "=-{preop}")
    L("is_ebitda", "EBITDA", "₹ lakh", "=SUM({is_gp},{is_staff}:{is_pre})", bold=True, top=True)
    L("is_ebitda_m", "EBITDA margin", "%", "=IF({is_rev}>0,{is_ebitda}/{is_rev},0)", num="pct",
      italic=True)
    L("is_dep", "Depreciation", "₹ lakh", "=-{dep_book}")
    L("is_ebit", "EBIT", "₹ lakh", "={is_ebitda}+{is_dep}", bold=True, top=True)
    L("is_int", "Interest expense", "₹ lakh", "=-({tl_int}+{rev_int})")
    L("is_inc", "Interest income", "₹ lakh", "={int_inc}")
    L("is_pbt", "Profit before tax", "₹ lakh", "={is_ebit}+{is_int}+{is_inc}", bold=True, top=True)
    L("is_tax_cur", "Current tax", "₹ lakh", "=-{tax_cur}")
    L("is_tax_def", "Deferred tax", "₹ lakh", "=-{tax_def}")
    L("is_pat", "Profit after tax", "₹ lakh", "={is_pbt}+{is_tax_cur}+{is_tax_def}", bold=True,
      top=True)
    L("is_pat_m", "net margin", "%", "=IF({is_rev}>0,{is_pat}/{is_rev},0)", num="pct", italic=True)
    B.skip()

    # ---------------------------------------------------------------- cash flow
    B.band("Cash flow statement")
    L("cf_pat", "Profit after tax", "₹ lakh", "={is_pat}")
    L("cf_dep", "Add: depreciation", "₹ lakh", "={dep_book}")
    L("cf_def", "Add: deferred tax", "₹ lakh", "={tax_def}")
    L("cf_nwc", "Less: increase in working capital", "₹ lakh", "=-{dnwc}")
    L("cf_cfo", "Cash from operations", "₹ lakh", "=SUM({cf_pat}:{cf_nwc})", bold=True, top=True)
    L("cf_capex", "Capex incl. property", "₹ lakh", "=-{capex_tot}")
    L("cf_depo", "Rent deposit paid", "₹ lakh", "=-{dep_paid}")
    L("cf_cfi", "Cash from investing", "₹ lakh", "={cf_capex}+{cf_depo}", bold=True, top=True)
    L("cf_tl_draw", "Term loan drawn", "₹ lakh", "={tl_draw}")
    L("cf_tl_rep", "Term loan repaid", "₹ lakh", "=-{tl_rep}")
    L("cf_rev", "Cash credit drawn / (repaid)", "₹ lakh", "={rev_flow}")
    L("cf_eq", "Equity invested", "₹ lakh", "={eq_issue}")
    L("cf_div", "Dividends paid", "₹ lakh", "=-{div}")
    L("cf_cff", "Cash from financing", "₹ lakh", "=SUM({cf_tl_draw}:{cf_div})", bold=True, top=True)
    L("cf_net", "Net change in cash", "₹ lakh", "={cf_cfo}+{cf_cfi}+{cf_cff}", bold=True)
    L("cf_open", "Opening cash", "₹ lakh", "={cf_close@p}", start=1)
    L("cf_close", "Closing cash", "₹ lakh", "={cf_open}+{cf_net}", bold=True, top=True)
    B.skip()

    # ---------------------------------------------------------------- balance sheet
    B.band("Balance sheet (31 March)")
    L("bs_cash", "Cash", "₹ lakh", "={cf_close}")
    L("bs_ar", "Receivables", "₹ lakh", "={ar}")
    L("bs_inv", "Inventory", "₹ lakh", "={inv}")
    L("bs_depo", "Rent deposit", "₹ lakh", "={dep_bal}")
    L("bs_ppe", "Fixed assets, net (incl. property)", "₹ lakh", "={nbv_close}")
    L("bs_ta", "Total assets", "₹ lakh", "=SUM({bs_cash}:{bs_ppe})", bold=True, top=True)
    L("bs_ap", "Payables", "₹ lakh", "={ap}")
    L("bs_rev", "Cash credit", "₹ lakh", "={rv_close}")
    L("bs_tl", "Term loan", "₹ lakh", "={tl_close}")
    L("bs_dtl", "Deferred tax liability / (asset), net", "₹ lakh", "={dtl}")
    L("bs_tlb", "Total liabilities", "₹ lakh", "=SUM({bs_ap}:{bs_dtl})", bold=True, top=True)
    L("bs_sc", "Share capital", "₹ lakh", "={eq_close}")
    L("bs_re", "Retained earnings", "₹ lakh", "={re_close}")
    L("bs_eq", "Shareholders' equity", "₹ lakh", "={bs_sc}+{bs_re}", bold=True, top=True)
    L("bs_tle", "Total liabilities & equity", "₹ lakh", "={bs_tlb}+{bs_eq}", bold=True, top=True)
    L("bs_chk", "Check (assets - liabilities - equity)", "₹ lakh", "=ROUND({bs_ta}-{bs_tle},4)",
      italic=True)
    B.skip()

    # ---------------------------------------------------------------- revenue schedule
    B.band("Schedule 1: Revenue")
    L("m_ramp", "Ramp-up (Live driver)", "%", "={ramp}", num="pct", start=OP)
    L("m_vol_g", "Volume growth (Live driver)", "%", "={vol_g}", num="pct", start=OP)
    L("prem", "Location growth premium (Y2-Y6)", "%",
      "=IF(AND({m_t}>=2,{m_t}<=6),{$Lx_growth_prem},0)", num="pct", start=OP)
    L("vol_ix", "Volume index", "x", {1: "={opf}", "*": "={vol_ix@p}*(1+{m_vol_g})*(1+{prem})"},
      num="ix", start=OP)
    L("bills_dem", "Bills per day, demand", "#",
      "={$Lx_bills_ss}*{$footfall}*(1+{$foot_eff_act})*{$e_bills}*{m_ramp}*{vol_ix}", num="int",
      start=OP)
    L("cap_bills", "Bills per day, seating capacity", "#",
      "={$Lx_seats}*{$max_turns}/(1-{$takeaway_share}-{$Lx_delivery})*{opf}", num="int", start=OP)
    L("bills", "Bills per day", "#", "=MIN({bills_dem},{cap_bills})", num="int", start=OP, bold=True)
    L("util", "Capacity utilisation", "%", "=IF({cap_bills}>0,{bills}/{cap_bills},0)", num="pct",
      start=OP, italic=True)
    L("days", "Operating days", "days", "={$Lx_op_days}*{opf}", num="int", start=OP)
    L("bills_yr", "Bills per year", "#", "={bills}*{days}", num="int", start=OP)
    L("atv", "Average bill value (ex-GST)", "₹",
      {1: "={$Lx_atv}*(1+{$atv_prem_act})*{$e_atv}", "*": "={atv@p}*(1+{m_atv_g})"}, num="int",
      start=OP)
    L("m_atv_g", "Menu price increase (Live driver)", "%", "={atv_g}", num="pct", start=OP)
    L("rev_cafe", "Café revenue", "₹ lakh", "={bills_yr}*{atv}/Lakh", bold=True, top=True)
    L("rev_bev", "Beverages", "₹ lakh", "={rev_cafe}*{$bev_share}")
    L("rev_food", "Food", "₹ lakh", "={rev_cafe}*{$food_sh}")
    L("rev_ret", "Retail beans & merchandise", "₹ lakh", "={rev_cafe}*{$ret_eff}")
    L("whs_kg_m", "Wholesale beans sold (in-house roastery only)", "kg/month",
      "={$is_inh}*{$e_whs}*{$Lx_whs_f}*{whs_ramp}*(1+{$whs_growth})^MAX(0,{m_t}-3)", num="int",
      start=OP)
    L("whs_kg_yr", "Wholesale beans sold", "kg/yr", "={whs_kg_m}*12", num="int", start=OP)
    L("rev_whs", "Wholesale revenue", "₹ lakh", "={whs_kg_yr}*{$whs_price_act}*{ix_cost}/Lakh", start=OP)
    L("rev_tot", "Total revenue", "₹ lakh", "={rev_cafe}+{rev_whs}", bold=True, top=True)
    B.skip()

    # ---------------------------------------------------------------- COGS schedule
    B.band("Schedule 2: Cost of goods sold")
    L("cups", "Beverages sold", "#", "={bills_yr}*{$cups_per_bill}", num="int", start=OP)
    L("kg_cafe", "Coffee used in the café", "kg", "={cups}*{$coffee_share}*{$grams}/1000",
      num="int", start=OP)
    L("ret_kg", "Retail beans sold", "kg", "={rev_ret}*Lakh/({$retail_price_act}*{ix_cost})",
      num="int", start=OP)
    L("kg_roast", "Roasted coffee to source (own label)", "kg",
      "={kg_cafe}+{$own_label}*{ret_kg}+{whs_kg_yr}", num="int", start=OP)
    L("kg_green", "Green coffee to buy (toll / in-house)", "kg",
      "=IF({$a_roast}>=2,{kg_roast}/(1-{$shrink}),0)", num="int", start=OP)
    L("m_green_ix", "Green-coffee price index (Live x override)", "x", "={green_ix}*{$e_green}",
      num="ix", start=OP)
    L("cost_kg", "Roasted coffee cost", "₹/kg", "={$green_link_act}*{m_green_ix}+{$conv_act}*{ix_cost}",
      num="int", start=OP)
    L("cogs_coffee", "Coffee (café)", "₹ lakh", "={kg_cafe}*({cost_kg}+{$cafe_pack}*{ix_cost})/Lakh",
      start=OP)
    L("cogs_milk", "Milk, syrups & other beverage inputs", "₹ lakh",
      "={cups}*{$milk_other}*{ix_cost}/Lakh", start=OP)
    L("cogs_pack", "Takeaway & delivery packaging", "₹ lakh",
      "={bills_yr}*({$takeaway_share}+{$Lx_delivery})*{$pack_per_bill}*{ix_cost}/Lakh", start=OP)
    L("cogs_food", "Food", "₹ lakh", "={rev_food}*{$food_cogs}", start=OP)
    L("cogs_ret", "Retail beans", "₹ lakh",
      "=IF({$own_label}=1,{ret_kg}*({cost_kg}+{$retail_pack}*{ix_cost})/Lakh,"
      "{rev_ret}*(1-{$resale_margin}))", start=OP)
    L("cogs_whs", "Wholesale beans", "₹ lakh", "={whs_kg_yr}*({cost_kg}+{$whs_pack}*{ix_cost})/Lakh",
      start=OP)
    L("cogs", "Cost of goods sold", "₹ lakh", "=SUM({cogs_coffee}:{cogs_whs})", bold=True, top=True)
    L("cogs_pct", "COGS % of revenue", "%", "=IF({rev_tot}>0,{cogs}/{rev_tot},0)", num="pct",
      italic=True)
    L("coffee_cogs", "memo: coffee in COGS", "₹ lakh",
      "={cogs_coffee}+{$own_label}*{cogs_ret}+{cogs_whs}", italic=True)
    L("cup_cost", "memo: coffee cost per beverage", "₹",
      "=IF({cups}>0,{cogs_coffee}*Lakh/{cups},0)", num="lakh", italic=True, start=OP)
    B.skip()

    # ---------------------------------------------------------------- opex schedule
    B.band("Schedule 3: Operating expenses")
    L("staff_mult", "Staffing scale-up for volume above steady state", "x",
      "=1+{$staff_elastic}*MAX(0,{bills}/{$Lx_bills_ss}-1)", num="ix", start=OP)
    L("staff", "Staff costs", "₹ lakh",
      "={$payroll_m}*12*(1+{$staff_load})*(1+{$wage_growth})^({m_t}-1)*{staff_mult}*{$e_staff}/Lakh",
      start=OP)
    L("rent", "Rent", "₹ lakh",
      "=(1-{$is_own})*{$area_tot}*{$Lx_rent_psf}*{$e_rent}*12*(1+{$rent_esc})^({m_t}-1)/Lakh",
      start=OP)
    L("cam", "CAM / society maintenance", "₹ lakh", "={$area_tot}*{$Lx_cam_psf}*12*{ix_opex}/Lakh",
      start=OP)
    L("ptax", "Property tax (own case)", "₹ lakh", "={$is_own}*{$area_tot}*{$Lx_ptax_psf}*{ix_opex}/Lakh",
      start=OP)
    L("power", "Electricity", "₹ lakh",
      "={$area_tot}*{$kwh_psf}*12*{$tariff}*(1+{$tariff_growth})^({m_t}-1)/Lakh", start=OP)
    L("gaswater", "Gas, water & cleaning", "₹ lakh", "={$gas_water_m}*12*{ix_opex}/Lakh", start=OP)
    L("mkt_c", "Marketing", "₹ lakh", "={rev_tot}*IF({m_t}=1,{$mkt_y1},{$mkt})", start=OP)
    L("rm_var", "Repairs & maintenance", "₹ lakh", "={rev_tot}*{$rm_pct}", start=OP)
    L("amc_c", "Equipment AMC", "₹ lakh", "=({$amc}+{$is_inh}*{$roaster_amc})*{ix_opex}/Lakh", start=OP)
    L("aggr", "Aggregator commission", "₹ lakh", "={rev_cafe}*{$Lx_delivery}*{$aggregator}", start=OP)
    L("payfee", "Card / UPI fees", "₹ lakh", "={rev_cafe}*(1-{$Lx_delivery})*{$payment}", start=OP)
    L("admin", "Admin, accounts, software, insurance", "₹ lakh", "={$admin_fixed}*{ix_opex}/Lakh",
      start=OP)
    L("misc", "Miscellaneous", "₹ lakh", "={rev_tot}*{$misc_pct}", start=OP)
    L("whs_sell", "Wholesale selling & delivery", "₹ lakh", "={rev_whs}*{$whs_selling}", start=OP)
    L("preop", "Pre-opening expenses", "₹ lakh",
      {0: "=((1-{$is_own})*{$rent_months}*{$area_tot}*{$Lx_rent_psf}*{$e_rent}+{$training_months}"
          "*{$payroll_m}*(1+{$staff_load})*{$e_staff}+{$launch_mkt}+{$licences}+{$recruitment}"
          "+{$utilities_misc})/Lakh"}, end=0)
    L("opex", "Operating expenses", "₹ lakh", "=SUM({staff}:{preop})", bold=True, top=True)
    L("opex_fixed", "memo: fixed costs", "₹ lakh",
      "={staff}+{rent}+{cam}+{ptax}+{power}+{gaswater}+{amc_c}+{admin}", italic=True, start=OP)
    L("var_cost", "memo: variable costs incl. COGS", "₹ lakh",
      "={cogs}+{mkt_c}+{rm_var}+{aggr}+{payfee}+{misc}+{whs_sell}", italic=True, start=OP)
    L("cm_pct", "Contribution margin", "%", "=IF({rev_tot}>0,1-{var_cost}/{rev_tot},0)", num="pct",
      italic=True, start=OP)
    L("be_bills", "Break-even bills per day (EBITDA = 0)", "#",
      "=IF(AND({rev_tot}>0,{cm_pct}>0),{opex_fixed}/{cm_pct}/{rev_tot}*{bills},0)", num="int",
      start=OP, bold=True)
    L("mos", "Margin of safety (bills above break-even)", "%",
      "=IF({bills}>0,1-{be_bills}/{bills},0)", num="pct", italic=True, start=OP)
    B.skip()

    # ---------------------------------------------------------------- fixed assets
    B.band("Schedule 4: Fixed assets & depreciation")
    L("capex_init", "Initial capex incl. property (Capex sheet)", "₹ lakh", {0: "={$cap_init_tot}"},
      end=0)
    L("capex_maint", "Maintenance capex", "₹ lakh", "={rev_tot}*{$maint_pct}", start=OP)
    L("capex_refurb", "Refurbishment", "₹ lakh",
      "=IF({m_t}={$refurb_year},{$refurb_pct}*({$ci_Interiors}+{$ci_Furniture})*{ix_cost},0)",
      start=OP)
    L("capex_ong", "Ongoing capex", "₹ lakh", "={capex_maint}+{capex_refurb}", start=OP)
    L("capex_tot", "Total capex", "₹ lakh", "=SUM({capex_init},{capex_ong})", bold=True, top=True)
    B.head("Book depreciation (straight line)")
    for cls in DEP_CLASSES:
        L("dep_" + cls, cls, "₹ lakh",
          "=IF(AND({$cl_%s}>0,{m_t}<={$cl_%s}),{$ci_%s}/{$cl_%s},0)" % (cls, cls, cls, cls),
          start=OP)
    L("dep_ong", "Ongoing capex (vintages)", "₹ lakh",
      "=SUMPRODUCT({#capex_ong}*({#m_t}<{m_t})*({m_t}-{#m_t}<={$ongoing_life}))/{$ongoing_life}",
      start=OP)
    L("dep_book", "Book depreciation", "₹ lakh",
      "=SUM({dep_%s}:{dep_ong})" % DEP_CLASSES[0], bold=True, top=True)
    L("nbv_open", "Net book value, opening", "₹ lakh", "={nbv_close@p}", start=OP)
    L("nbv_close", "Net book value, closing", "₹ lakh", "={nbv_open}+{capex_tot}-{dep_book}",
      bold=True)
    B.head("Tax depreciation (written-down value)")
    for cls in DEP_CLASSES:
        L("tdep_" + cls, cls, "₹ lakh", "={$ci_%s}*{$cr_%s}*(1-{$cr_%s})^({m_t}-1)" % (cls, cls, cls),
          start=OP)
    L("tw_open", "Ongoing capex block, opening WDV", "₹ lakh", "={tw_close@p}", start=OP)
    L("tw_add", "Additions", "₹ lakh", "={capex_ong}", start=OP)
    L("tdep_ong", "Tax depreciation, ongoing block", "₹ lakh",
      "={$ongoing_tax}*({tw_open}+{tw_add}/2)", start=OP)
    L("tw_close", "Ongoing capex block, closing WDV", "₹ lakh", "={tw_open}+{tw_add}-{tdep_ong}",
      start=OP)
    L("dep_tax", "Tax depreciation", "₹ lakh",
      "=SUM({tdep_%s}:{tdep_%s})+{tdep_ong}" % (DEP_CLASSES[0], DEP_CLASSES[-1]), bold=True,
      top=True)
    L("wdv_tot", "Tax written-down value, closing", "₹ lakh",
      "=SUMPRODUCT(%s,(1-%s)^{m_t})+{tw_close}" % (B.area("ci_Interiors", "ci_Land"),
                                                 B.area("cr_Interiors", "cr_Land")))
    L("dtl", "Deferred tax liability / (asset)", "₹ lakh", "=({nbv_close}-{wdv_tot})*TaxRate")
    L("tax_def", "Deferred tax charge", "₹ lakh", {0: "={dtl}", "*": "={dtl}-{dtl@p}"})
    B.skip()

    # ---------------------------------------------------------------- tax
    B.band("Schedule 5: Income tax")
    L("tx_pbt", "Profit before tax", "₹ lakh", "={is_pbt}")
    L("tx_add", "Add back book depreciation", "₹ lakh", "={dep_book}")
    L("tx_less", "Less tax depreciation", "₹ lakh", "=-{dep_tax}")
    L("tx_ti0", "Taxable income before losses", "₹ lakh", "=SUM({tx_pbt}:{tx_less})", top=True)
    L("nol_open", "Losses brought forward", "₹ lakh", "={nol_close@p}", start=OP)
    L("nol_add", "Losses added", "₹ lakh", "=MAX(0,-{tx_ti0})")
    L("nol_use", "Losses used", "₹ lakh", "=MIN(N({nol_open}),MAX(0,{tx_ti0}))")
    L("nol_close", "Losses carried forward", "₹ lakh", "={nol_open}+{nol_add}-{nol_use}")
    L("tx_ti", "Taxable income", "₹ lakh", "=MAX(0,{tx_ti0})-{nol_use}", bold=True, top=True)
    L("tax_cur", "Current tax", "₹ lakh", "={tx_ti}*TaxRate")
    L("tax_tot", "Total tax charge", "₹ lakh", "={tax_cur}+{tax_def}", bold=True)
    B.skip()

    # ---------------------------------------------------------------- working capital
    B.band("Schedule 6: Working capital & deposit")
    L("ar", "Receivables", "₹ lakh",
      "={rev_cafe}*{$Lx_delivery}*{$ar_delivery_days}/365+{rev_whs}*{$ar_wholesale_days}/365")
    L("inv", "Inventory", "₹ lakh",
      "=({cogs}-{coffee_cogs})*{$inv_days}/365+{coffee_cogs}*IF({$a_roast}=1,{$inv_days},"
      "{$green_inv_days})/365")
    L("ap", "Payables", "₹ lakh", "={cogs}*{$ap_days}/365")
    L("nwc", "Net working capital", "₹ lakh", "={ar}+{inv}-{ap}", bold=True, top=True)
    L("dnwc", "Increase / (decrease)", "₹ lakh", {0: "={nwc}", "*": "={nwc}-{nwc@p}"})
    L("dep_paid", "Rent deposit paid", "₹ lakh", {0: "={$u_dep}"}, end=0)
    L("dep_bal", "Rent deposit balance", "₹ lakh", {0: "={dep_paid}", "*": "={dep_bal@p}+{dep_paid}"})
    B.skip()

    # ---------------------------------------------------------------- debt
    B.band("Schedule 7: Debt")
    B.head("Term loan")
    L("tl_open", "Opening", "₹ lakh", "={tl_close@p}", start=OP)
    L("tl_draw", "Drawn", "₹ lakh", {0: "={$s_debt}"}, end=0)
    L("tl_rep", "Repaid", "₹ lakh",
      "=MIN({tl_open},IF({m_t}<={$loan_tenor},{$s_debt}/{$loan_tenor},0))", start=OP)
    L("tl_close", "Closing", "₹ lakh", "={tl_open}+{tl_draw}-{tl_rep}", bold=True, top=True)
    L("tl_int", "Interest", "₹ lakh", "={$loan_rate}*IF(Circ=1,AVERAGE({tl_open},{tl_close}),{tl_open})",
      start=OP)
    B.head("Cash credit (revolver)")
    L("cash_pre", "Cash available before cash credit, above minimum", "₹ lakh",
      "={cf_open}+{cf_cfo}+{cf_cfi}+{tl_draw}-{tl_rep}+{eq_issue}-{div}-{$min_cash}/Lakh")
    L("rv_open", "Opening", "₹ lakh", "={rv_close@p}", start=OP)
    L("rev_flow", "Drawn / (repaid)", "₹ lakh", "=MAX(-{cash_pre},-{rv_open})")
    L("rv_close", "Closing", "₹ lakh", "={rv_open}+{rev_flow}", bold=True, top=True)
    L("rev_int", "Interest", "₹ lakh",
      "={$revolver_rate}*IF(Circ=1,AVERAGE({rv_open},{rv_close}),{rv_open})", start=OP)
    L("int_inc", "Interest earned on cash", "₹ lakh",
      "={$cash_rate}*IF(Circ=1,AVERAGE({cf_open},{cf_close}),{cf_open})", start=OP)
    L("dscr", "Debt service cover (EBITDA - tax) / (interest + principal)", "x",
      '=IF({tl_int}+{rev_int}+{tl_rep}>0,({is_ebitda}-{tax_cur})/({tl_int}+{rev_int}+{tl_rep}),"")',
      num="x", start=OP, italic=True)
    B.skip()

    # ---------------------------------------------------------------- equity
    B.band("Schedule 8: Equity")
    L("eq_open", "Share capital, opening", "₹ lakh", "={eq_close@p}", start=OP)
    L("eq_issue", "Equity invested", "₹ lakh", {0: "={$s_eq}"}, end=0)
    L("eq_close", "Share capital, closing", "₹ lakh", "={eq_open}+{eq_issue}", bold=True)
    L("re_open", "Retained earnings, opening", "₹ lakh", "={re_close@p}", start=OP)
    L("re_ni", "Profit after tax", "₹ lakh", "={is_pat}")
    L("div", "Dividends", "₹ lakh", "=IF({is_pat}>0,{$payout}*{is_pat},0)")
    L("re_close", "Retained earnings, closing", "₹ lakh", "={re_open}+{re_ni}-{div}", bold=True)


# =============================================================================== DCF
def dcf(B):
    B.use("DCF")
    B.title("DCF valuation (FCFF)", "Valuation date 31 March 2027 (end of Y0). Y0 investment is "
            "undiscounted; Y1-Y10 discounted at WACC; Gordon-growth terminal value at Y10.")
    B.timeline_header("d_fy", "d_t", src="m_fy")
    L = B.line
    B.band("Free cash flow to the firm")
    L("d_ebitda", "EBITDA", "₹ lakh", "={is_ebitda}")
    L("d_dep", "Less: depreciation", "₹ lakh", "=-{dep_book}")
    L("d_ebit", "EBIT", "₹ lakh", "={d_ebitda}+{d_dep}", bold=True, top=True)
    B.head("Unlevered tax (as if no debt)")
    L("u_ti0", "EBIT + book dep - tax dep", "₹ lakh", "={d_ebit}+{dep_book}-{dep_tax}")
    L("u_nol_open", "Losses brought forward", "₹ lakh", "={u_nol_close@p}", start=1)
    L("u_nol_add", "Losses added", "₹ lakh", "=MAX(0,-{u_ti0})")
    L("u_nol_use", "Losses used", "₹ lakh", "=MIN(N({u_nol_open}),MAX(0,{u_ti0}))")
    L("u_nol_close", "Losses carried forward", "₹ lakh", "={u_nol_open}+{u_nol_add}-{u_nol_use}")
    L("u_tax", "Unlevered tax", "₹ lakh", "=(MAX(0,{u_ti0})-{u_nol_use})*TaxRate")
    B.head("Free cash flow")
    L("d_nopat", "NOPAT (EBIT - unlevered tax)", "₹ lakh", "={d_ebit}-{u_tax}")
    L("d_da", "Add: depreciation", "₹ lakh", "={dep_book}")
    L("d_capex", "Less: capex incl. property", "₹ lakh", "=-{capex_tot}")
    L("d_nwc", "Less: increase in working capital", "₹ lakh", "=-{dnwc}")
    L("d_depo", "Less: rent deposit", "₹ lakh", "=-{dep_paid}")
    L("fcff", "Free cash flow to firm", "₹ lakh", "=SUM({d_nopat}:{d_depo})", bold=True, top=True)
    L("disc_n", "Discount period", "years", {0: "={d_t}", "*": "={d_t}-0.5*{$mid_year}"}, num="lakh2")
    L("df", "Discount factor", "x", "=1/(1+{$wacc})^{disc_n}", num="ix")
    L("pv_fcff", "Present value of FCFF", "₹ lakh", "={fcff}*{df}", bold=True)
    B.skip()

    B.band("Cost of capital")
    B.sc("w_rf", "Risk-free rate", "%", "={$rf}", num="pct2")
    B.sc("w_erp", "Equity risk premium", "%", "={$erp}", num="pct2")
    B.sc("w_bu", "Unlevered beta", "x", "={$beta_u}", num="x")
    B.sc("w_wd", "Debt / (debt + equity), from funding plan", "%", "={$gearing}", num="pct")
    B.sc("w_de", "Debt / equity", "x", "=IF({$w_wd}<1,{$w_wd}/(1-{$w_wd}),0)", num="x")
    B.sc("w_bl", "Relevered beta", "x", "={$w_bu}*(1+(1-TaxRate)*{$w_de})", num="x")
    B.sc("w_sp", "Size & single-outlet premium", "%", "={$specific}", num="pct2")
    B.sc("ke", "Cost of equity", "%", "={$w_rf}+{$w_bl}*{$w_erp}+{$w_sp}", num="pct2", bold=True)
    B.sc("w_kd", "Cost of debt, pre-tax", "%", "={$loan_rate}", num="pct2")
    B.sc("w_kdt", "Cost of debt, after tax", "%", "={$w_kd}*(1-TaxRate)", num="pct2")
    B.sc("wacc_calc", "WACC, calculated", "%", "=(1-{$w_wd})*{$ke}+{$w_wd}*{$w_kdt}", num="pct2")
    B.sc("wacc", "WACC used (incl. any Scenarios-sheet change)", "%",
         "={$wacc_calc}+{$e_wacc}", num="pct2", bold=True)
    B.sc("g_used", "Terminal growth used", "%", "={$e_g}", num="pct2", bold=True)
    B.skip()

    B.band("Terminal value at Y10")
    B.sc("tv_year", "Terminal year", "#", "=MAX({#d_t})", num="idx")
    B.sc("notional_rent", "Own case: market rent the site would pay in Y11", "₹ lakh",
         "={$is_own}*{$area_tot}*{$Lx_rent_psf}*{$e_rent}*12*(1+{$rent_esc})^{$tv_year}/Lakh")
    B.sc("refurb_norm", "Normalised refurbishment per year (cost / cycle)", "₹ lakh",
         "={$refurb_pct}*({$ci_Interiors}+{$ci_Furniture})*{ix_cost@L}*(1+{$cost_infl})/{$refurb_year}")
    B.sc("fcff_n1", "Operating FCFF in Y11 (after notional rent if owned)", "₹ lakh",
         "=({fcff@L}+{ptax@L}*(1-TaxRate))*(1+{$g_used})-{$notional_rent}*(1-TaxRate)"
         "-{$refurb_norm}")
    B.sc("tv_ops", "Terminal value of operations (Gordon growth)", "₹ lakh",
         "=IF({$wacc}>{$g_used},{$fcff_n1}/({$wacc}-{$g_used}),NA())")
    B.sc("prop_val", "Own case: property market value at Y10", "₹ lakh",
         "={$is_own}*{$prop_price}*(1+{$Lx_apprec})^{$tv_year}")
    B.sc("prop_sell", "less selling cost", "₹ lakh", "=-{$prop_val}*{$sell_cost}")
    B.sc("prop_cgt", "less capital-gains tax", "₹ lakh",
         "=-MAX(0,{$prop_val}+{$prop_sell}-{$prop_cost})*{$cgt}")
    B.sc("tv", "Terminal value (operations + property)", "₹ lakh",
         "={$tv_ops}+{$prop_val}+{$prop_sell}+{$prop_cgt}", bold=True, top=True)
    B.sc("tv_df", "Discount factor at Y10", "x", "=1/(1+{$wacc})^{$tv_year}", num="ix")
    B.sc("pv_tv", "Present value of terminal value", "₹ lakh", "={$tv}*{$tv_df}", bold=True)
    B.sc("tv_mult", "Implied EV / EBITDA of operations at Y10", "x",
         "=IF({d_ebitda@L}+{ptax@L}-{$notional_rent}/(1+{$rent_esc})>0,{$tv_ops}/({d_ebitda@L}+"
         "{ptax@L}-{$notional_rent}/(1+{$rent_esc})),0)", num="x")
    B.sc("tv_exit", "Cross-check: operations value at exit multiple", "₹ lakh",
         "={$exit_mult}*({d_ebitda@L}+{ptax@L}-{$notional_rent}/(1+{$rent_esc}))")
    B.skip()

    B.band("Valuation results")
    B.sc("sum_pv", "Sum of PV of FCFF, Y0-Y10", "₹ lakh", "=SUM({#pv_fcff})")
    B.sc("npv", "Project NPV at WACC", "₹ lakh", "={$sum_pv}+{$pv_tv}", bold=True, top=True)
    B.sc("tv_share", "Terminal value share of gross value", "%",
         "=IF(SUM({#pv_fcff:1})+{$pv_tv}<>0,{$pv_tv}/(SUM({#pv_fcff:1})+{$pv_tv}),0)", num="pct")
    L("irr_cf", "Project cash flows for IRR (FCFF + TV)", "₹ lakh",
      "={fcff}+IF({d_t}={$tv_year},{$tv},0)")
    B.sc("irr_p", "Project IRR", "%", '=IFERROR(IRR({#irr_cf}),"n.m.")', num="pct", bold=True)
    B.head("Equity view")
    L("fcfe", "Free cash flow to equity (Y0: equity in, net of cash kept)", "₹ lakh",
      "={cf_cfo}+{cf_cfi}+{cf_tl_draw}+{cf_tl_rep}+{cf_rev}")
    L("eq_cf", "Equity cash flows (Y10 adds TV less debt)", "₹ lakh",
      "={fcfe}+IF({d_t}={$tv_year},{$tv}-{tl_close}-{rv_close},0)")
    B.sc("irr_e", "Equity IRR", "%", '=IFERROR(IRR({#eq_cf}),"n.m.")', num="pct", bold=True)
    B.sc("npv_e", "Equity NPV at cost of equity", "₹ lakh", "={eq_cf@F}+NPV({$ke},{#eq_cf:1})",
         bold=True)
    B.sc("moic", "Equity multiple (money in : money out)", "x",
         '=IFERROR(SUMIF({#eq_cf},">0")/-SUMIF({#eq_cf},"<0"),0)', num="x")
    B.head("Payback")
    L("cum_fcff", "Cumulative FCFF", "₹ lakh", {0: "={fcff}", "*": "={cum_fcff@p}+{fcff}"})
    L("pb_h", "helper: payback year", "years",
      '=IF(AND({cum_fcff@p}<0,{cum_fcff}>=0),{d_t@p}+(-{cum_fcff@p})/{fcff},"")', num="lakh2",
      start=1, italic=True)
    L("cum_pv", "Cumulative PV of FCFF", "₹ lakh", {0: "={pv_fcff}", "*": "={cum_pv@p}+{pv_fcff}"})
    L("dpb_h", "helper: discounted payback year", "years",
      '=IF(AND({cum_pv@p}<0,{cum_pv}>=0),{d_t@p}+(-{cum_pv@p})/{pv_fcff},"")', num="lakh2",
      start=1, italic=True)
    B.sc("payback", "Payback (undiscounted, from opening)", "years",
         "=IF(COUNT({#pb_h:1})=0,99,MIN({#pb_h:1}))", num="yrs", bold=True)
    B.sc("dpayback", "Discounted payback", "years", "=IF(COUNT({#dpb_h:1})=0,99,MIN({#dpb_h:1}))",
         num="yrs")
    B.skip()

    B.band("Key metrics")
    B.sc("k_tcr", "Total capital requirement", "₹ lakh", "={$u_tot}")
    B.sc("k_eq", "Promoter equity", "₹ lakh", "={$s_eq}")
    B.sc("k_debt", "Term loan", "₹ lakh", "={$s_debt}")
    B.sc("y1_rev", "Revenue, Y1", "₹ lakh", "={rev_tot@1}")
    B.sc("y3_rev", "Revenue, Y3 (steady state)", "₹ lakh", "={rev_tot@3}")
    B.sc("y3_ebitda", "EBITDA, Y3", "₹ lakh", "={is_ebitda@3}")
    B.sc("y3_margin", "EBITDA margin, Y3", "%", "={is_ebitda_m@3}", num="pct")
    B.sc("y3_pat", "Profit after tax, Y3", "₹ lakh", "={is_pat@3}")
    B.sc("y3_bills", "Bills per day, Y3", "#", "={bills@3}", num="int")
    B.sc("be_y3", "Break-even bills per day, Y3", "#", "={be_bills@3}", num="int")
    B.sc("mos_y3", "Margin of safety, Y3", "%", "={mos@3}", num="pct")
    B.sc("y3_cogs", "COGS % of revenue, Y3", "%", "={cogs_pct@3}", num="pct")
    B.sc("y3_staff", "Staff % of revenue, Y3", "%", "=IF({rev_tot@3}>0,{staff@3}/{rev_tot@3},0)",
         num="pct")
    B.sc("y3_occ", "Occupancy % of revenue, Y3", "%",
         "=IF({rev_tot@3}>0,({rent@3}+{cam@3}+{ptax@3})/{rev_tot@3},0)", num="pct")
    B.sc("y1_ebitda", "EBITDA, Y1", "₹ lakh", "={is_ebitda@1}")
    B.sc("y10_rev", "Revenue, Y10", "₹ lakh", "={rev_tot@L}")
    B.sc("y10_ebitda", "EBITDA, Y10", "₹ lakh", "={is_ebitda@L}")
    B.sc("peak_rev", "Peak cash-credit draw", "₹ lakh", "=MAX({#rv_close})")
    B.sc("min_dscr", "Minimum DSCR after the ramp-up year (Y2 on)", "x",
         '=IF(COUNT({#dscr:2})=0,"n.a.",MIN({#dscr:2}))', num="x")
    B.sc("exit3", "Downside: net cash lost if shut at end of Y3", "₹ lakh",
         "=-MIN(0,{cum_fcff@3}+{$salvage}*{$u_capex}+{$u_dep}+{nwc@3}"
         "+{$is_own}*{$prop_price}*(1+{$Lx_apprec})^3*(1-{$sell_cost}))",
         note="Cumulative FCFF to Y3 + equipment resale + deposit + working capital "
              "+ property resale")
    B.sc("cash_y10", "Cash at Y10 (if never distributed)", "₹ lakh", "={cf_close@L}")
    B.sc("roce_y5", "Pre-tax return on capital employed, Y5", "%",
         "=IF({nbv_close@5}+{nwc@5}+{dep_bal@5}>0,{is_ebit@5}/({nbv_close@5}+{nwc@5}+{dep_bal@5}),0)",
         num="pct")


# =============================================================================== Scenarios
def scenarios(B):
    ws = B.use("Scenarios")
    ws.set_column(0, 0, 2)
    ws.set_column(1, 1, 36)
    ws.set_column(2, 2, 10)
    ws.set_column(3, 16, 11.5)
    B.title("Scenarios & sensitivities", "Live Excel data tables: each cell re-runs the full model. "
            "Keep the blue override cells at their default (0 or 1) for normal use.")
    B.band("Override panel (data-table input cells)")
    ovr = [("o_scn", "Scenario (0 = Inputs; 1 Best, 2 Base, 3 Worst)", 0, "idx"),
           ("o_cfg", "Configuration # from Configs sheet (0 = Inputs)", 0, "idx"),
           ("o_loc", "Location # (0 = Inputs/config)", 0, "idx"),
           ("o_prop", "Premises # (0 = Inputs/config; 1 Rent, 2 Own)", 0, "idx"),
           ("o_roast", "Roasting route # (0 = Inputs/config; 1 Buy, 2 Toll, 3 In-house)", 0, "idx"),
           ("o_mix", "Bean mix # (0 = Inputs/config; 1-4)", 0, "idx"),
           ("o_whs", "Wholesale kg/month at maturity (0 = Inputs)", 0, "int"),
           ("o_bills", "Bills-per-day multiplier", 1, "x"),
           ("o_atv", "Average-bill multiplier", 1, "x"),
           ("o_rent", "Rent multiplier", 1, "x"),
           ("o_green", "Green-coffee price multiplier", 1, "x"),
           ("o_capex", "Capex multiplier", 1, "x"),
           ("o_staff", "Staff-cost multiplier", 1, "x"),
           ("o_wacc", "WACC change (+/- percentage points)", 0, "pct"),
           ("o_g", "Terminal growth override (0 = Inputs)", 0, "pct"),
           ("o_tv", "Tornado variable # (0 = off)", 0, "idx"),
           ("o_ts", "Tornado side (1 low, 2 high)", 0, "idx")]
    for k, lab, v, num in ovr:
        B.sc(k, lab, "", v, num=num)
    B.skip()
    B.head("Tornado definitions (one variable at a time)")
    r = B.nr()
    for c, t in [(1, "Variable"), (2, "#"), (3, "Low"), (4, "High")]:
        B.put(r, c, t, num=None, bold=True, bg_color=HEAD_FILL, bottom=1, align="center")
    for k, (lab, lo, hi) in enumerate(A.TORNADO, 1):
        r = B.nr()
        B.put(r, 1, lab, num=None, indent=1)
        B.put(r, 2, k, num="idx", inp=False, align="center")
        num = "pct" if k >= 7 else "x"
        B._set(f"tlo_{k}", r, 3)
        B._set(f"thi_{k}", r, 4)
        B.put(r, 3, lo, num=num)
        B.put(r, 4, hi, num=num)
    B.skip()
    B.head("Effective values used by the model")

    def tor(k):
        return "IF(AND({$o_tv}=%d,{$o_ts}>0),CHOOSE({$o_ts},{$tlo_%d},{$thi_%d}),1)" % (k, k, k)
    B.sc("e_bills", "Bills-per-day multiplier", "x", "={$o_bills}*" + tor(1), num="x")
    B.sc("e_atv", "Average-bill multiplier", "x", "={$o_atv}*" + tor(2), num="x")
    B.sc("e_rent", "Rent multiplier", "x", "={$o_rent}*" + tor(3), num="x")
    B.sc("e_green", "Green-price multiplier", "x", "={$o_green}*" + tor(4), num="x")
    B.sc("e_capex", "Capex multiplier", "x", "={$o_capex}*" + tor(5), num="x")
    B.sc("e_staff", "Staff-cost multiplier", "x", "={$o_staff}*" + tor(6), num="x")
    B.sc("e_whs", "Wholesale kg/month at maturity", "kg", "=IF({$o_whs}>0,{$o_whs},{$whs_kg})",
         num="int")
    B.sc("e_wacc", "WACC change", "pp",
         "={$o_wacc}+IF(AND({$o_tv}=7,{$o_ts}>0),CHOOSE({$o_ts},{$tlo_7},{$thi_7}),0)", num="pct")
    B.sc("e_g", "Terminal growth", "%",
         "=IF(AND({$o_tv}=8,{$o_ts}>0),CHOOSE({$o_ts},{$tlo_8},{$thi_8}),IF({$o_g}>0,{$o_g},{$g}))",
         num="pct2")
    B.skip()

    outs_main = [("NPV ₹ lakh", "$npv", "lakh"), ("Project IRR", "$irr_p", "pct"),
                 ("Equity IRR", "$irr_e", "pct"), ("Equity NPV ₹ lakh", "$npv_e", "lakh"),
                 ("Payback", "$payback", "yrs"), ("Disc. payback", "$dpayback", "yrs"),
                 ("Capital need ₹ lakh", "$k_tcr", "lakh"), ("Y3 revenue ₹ lakh", "$y3_rev", "lakh"),
                 ("Y3 EBITDA margin", "$y3_margin", "pct"), ("Break-even bills/day", "$be_y3", "int"),
                 ("Peak cash credit ₹ lakh", "$peak_rev", "lakh")]
    B.band("T1. Scenario analysis (Best / Base / Worst) for the active configuration")
    B.data_table("scn", [1, 2, 3], "o_scn", outs=outs_main, down_labels=A.SCENARIOS,
                 head_down="Scenario")
    B.skip()

    B.band("T2. Location × premises (active roasting route, mix and scenario)")
    B.note("Project NPV, ₹ lakh")
    B.data_table("locprop_npv", [1, 2, 3, 4], "o_loc", across=[1, 2], across_in="o_prop",
                 out="$npv", down_labels=A.LOCATIONS, across_labels=A.PROPERTY,
                 head_down="Location ↓  Premises →")
    B.note("Project IRR")
    B.data_table("locprop_irr", [1, 2, 3, 4], "o_loc", across=[1, 2], across_in="o_prop",
                 out="$irr_p", num="pct", down_labels=A.LOCATIONS, across_labels=A.PROPERTY,
                 head_down="Location ↓  Premises →")
    B.note("Equity IRR")
    B.data_table("locprop_eirr", [1, 2, 3, 4], "o_loc", across=[1, 2], across_in="o_prop",
                 out="$irr_e", num="pct", down_labels=A.LOCATIONS, across_labels=A.PROPERTY,
                 head_down="Location ↓  Premises →")
    B.note("Total capital requirement, ₹ lakh")
    B.data_table("locprop_tcr", [1, 2, 3, 4], "o_loc", across=[1, 2], across_in="o_prop",
                 out="$k_tcr", down_labels=A.LOCATIONS, across_labels=A.PROPERTY,
                 head_down="Location ↓  Premises →")
    B.skip()

    B.band("T3. Roasting route × bean mix (active location, premises and scenario)")
    B.note("Project NPV, ₹ lakh")
    B.data_table("roastmix_npv", [1, 2, 3], "o_roast", across=[1, 2, 3, 4], across_in="o_mix",
                 out="$npv", down_labels=A.ROASTING, across_labels=A.MIXES,
                 head_down="Roasting ↓  Mix →")
    B.note("EBITDA margin, Y3")
    B.data_table("roastmix_m", [1, 2, 3], "o_roast", across=[1, 2, 3, 4], across_in="o_mix",
                 out="$y3_margin", num="pct", down_labels=A.ROASTING, across_labels=A.MIXES,
                 head_down="Roasting ↓  Mix →")
    B.skip()

    B.band("T4. Configurations (defined on the Configs sheet), active scenario")
    ncfg = len(A.CONFIGS)
    cfg_labels = ["={$cfgname_%d}" % i for i in range(1, ncfg + 1)]
    outs_cfg = outs_main[:3] + [outs_main[4], outs_main[6], ("Equity ₹ lakh", "$k_eq", "lakh"),
                                outs_main[7], ("Y3 EBITDA ₹ lakh", "$y3_ebitda", "lakh"),
                                outs_main[8], outs_main[9], ("Min DSCR", "$min_dscr", "x")]
    B.data_table("cfg", list(range(1, ncfg + 1)), "o_cfg", outs=outs_cfg, down_labels=cfg_labels,
                 head_down="Configuration")
    B.skip()
    B.band("T5. Configurations × scenario")
    B.note("Project NPV, ₹ lakh")
    B.data_table("cfgscn_npv", list(range(1, ncfg + 1)), "o_cfg", across=[1, 2, 3], across_in="o_scn",
                 out="$npv", down_labels=cfg_labels, across_labels=A.SCENARIOS,
                 head_down="Configuration ↓  Scenario →")
    B.note("Equity IRR")
    B.data_table("cfgscn_eirr", list(range(1, ncfg + 1)), "o_cfg", across=[1, 2, 3],
                 across_in="o_scn", out="$irr_e", num="pct", down_labels=cfg_labels,
                 across_labels=A.SCENARIOS, head_down="Configuration ↓  Scenario →")
    B.skip()

    B.band("T6. Sensitivities on the active configuration")
    B.note("Project NPV (₹ lakh): WACC change ↓ × terminal growth →")
    B.data_table("wacc_g", [-0.02, -0.01, 0, 0.01, 0.02], "o_wacc",
                 across=[0.03, 0.035, 0.04, 0.045, 0.05], across_in="o_g", out="$npv",
                 down_labels=["-2.0 pp", "-1.0 pp", "WACC as calculated", "+1.0 pp", "+2.0 pp"],
                 across_labels=["g 3.0%", "g 3.5%", "g 4.0%", "g 4.5%", "g 5.0%"],
                 head_down="WACC ↓  growth →")
    B.note("Project NPV (₹ lakh): bills per day ↓ × average bill →")
    B.data_table("bills_atv", [0.8, 0.9, 1.0, 1.1, 1.2], "o_bills",
                 across=[0.9, 0.95, 1.0, 1.05, 1.1], across_in="o_atv", out="$npv",
                 down_labels=["Bills -20%", "Bills -10%", "Bills as modelled", "Bills +10%",
                              "Bills +20%"],
                 across_labels=["Bill -10%", "Bill -5%", "Bill base", "Bill +5%", "Bill +10%"],
                 head_down="Bills ↓  Average bill →")
    B.note("Project IRR: rent ↓ × bills per day →")
    B.data_table("rent_bills", [0.8, 0.9, 1.0, 1.1, 1.2], "o_rent",
                 across=[0.8, 0.9, 1.0, 1.1, 1.2], across_in="o_bills", out="$irr_p", num="pct",
                 down_labels=["Rent -20%", "Rent -10%", "Rent as modelled", "Rent +10%", "Rent +20%"],
                 across_labels=["Bills -20%", "Bills -10%", "Bills base", "Bills +10%", "Bills +20%"],
                 head_down="Rent ↓  Bills →")
    B.note("Y3 EBITDA margin: green-coffee price ↓ × roasting route →")
    B.data_table("green_roast", [0.7, 0.85, 1.0, 1.15, 1.3, 1.6], "o_green", across=[1, 2, 3],
                 across_in="o_roast", out="$y3_margin", num="pct",
                 down_labels=["Green -30%", "Green -15%", "Green as modelled", "Green +15%",
                              "Green +30%", "Green +60%"],
                 across_labels=A.ROASTING, head_down="Green price ↓  Route →")
    B.skip()

    B.note("Project NPV (₹ lakh): wholesale volume ↓ × roasting route → (wholesale only with "
           "an in-house roastery)")
    B.data_table("whs_roast", [50, 150, 300, 450, 600, 800], "o_whs", across=[2, 3],
                 across_in="o_roast", out="$npv",
                 down_labels=["50 kg/month", "150 kg/month", "300 kg/month", "450 kg/month",
                              "600 kg/month", "800 kg/month"],
                 across_labels=A.ROASTING[1:], head_down="Wholesale volume ↓  Route →")
    B.skip()

    B.band("T7. Tornado: project NPV when one variable moves (₹ lakh)")
    first, _ = B.data_table("tornado", list(range(1, len(A.TORNADO) + 1)), "o_tv", across=[1, 2],
                            across_in="o_ts", out="$npv",
                            down_labels=[t[0] for t in A.TORNADO], across_labels=["Low", "High"],
                            head_down="Variable ↓  side →")
    hd = dict(bold=True, bg_color=HEAD_FILL, bottom=1, align="center", text_wrap=True)
    B.put(first - 2, 6, "Low vs base", num=None, **hd)
    B.put(first - 2, 7, "High vs base", num=None, **hd)
    B.put(first - 2, 8, "Swing", num=None, **hd)
    for i in range(len(A.TORNADO)):
        r = first + i
        B._set(f"tor_lo_{i}", r, 6)
        B._set(f"tor_hi_{i}", r, 7)
        B.put(r, 6, f"=D{r + 1}-{B.s('npv')}", num="lakh")
        B.put(r, 7, f"=E{r + 1}-{B.s('npv')}", num="lakh")
        B.put(r, 8, f"=ABS(H{r + 1}-G{r + 1})", num="lakh")
    B.skip()

    B.band("T8. Rent vs own: free cash flows of the active configuration under each premises option")
    outs = [(f"Y{i}", f"irr_cf@{i}" if i < NT - 1 else "irr_cf@L", "lakh") for i in range(NT)]
    outs += [("NPV", "$npv", "lakh"), ("Equity IRR", "$irr_e", "pct")]
    first, _ = B.data_table("rentown", [1, 2], "o_prop", outs=outs, down_labels=A.PROPERTY,
                            head_down="Premises (Y10 includes terminal value)")
    r = B.nr()
    B._set("inc_cf", r, 3)
    B.put(r, 1, "Incremental cash flow of buying (Own - Rent)", num=None, bold=True, top=1)
    B.put(r, 2, None, top=1)
    for j in range(NT):
        col = "DEFGHIJKLMN"[j]
        B.put(r, 3 + j, f"={col}{first + 2}-{col}{first + 1}", num="lakh", bold=True, top=1)
    r = B.nr()
    B._set("inc_irr", r, 3)
    B.put(r, 1, "Incremental IRR of buying instead of renting", num=None, bold=True)
    B.put(r, 3, f'=IFERROR(IRR(D{r}:N{r}),"n.m.")', num="pct", bold=True)
    B.note("Buying beats renting only if this IRR exceeds the cost of the extra capital tied up.")


# =============================================================================== Configs
def configs(B):
    ws = B.use("Configs")
    ws.set_column(0, 0, 2)
    ws.set_column(1, 1, 5)
    ws.set_column(2, 2, 16)
    ws.set_column(3, 3, 19)
    ws.set_column(4, 4, 9)
    ws.set_column(5, 5, 17)
    ws.set_column(6, 6, 10)
    ws.set_column(7, 7, 2)
    ws.set_column(8, 15, 11)
    B.title("Configurations compared", "Edit the blue cells to define your own combinations. "
            "Results come from data table T4 on the Scenarios sheet (active scenario).")
    r = B.nr()
    hd = dict(bold=True, bg_color=HEAD_FILL, bottom=1, align="center", text_wrap=True)
    ws.set_row(r, 30)
    heads = ["#", "Name", "Location", "Premises", "Roasting", "Mix", "", "NPV ₹ lakh",
             "Project IRR", "Equity IRR", "Payback", "Capital ₹ lakh", "Y3 EBITDA %",
             "Break-even bills", "Rank (NPV)"]
    for j, h in enumerate(heads):
        if h:
            B.put(r, 1 + j, h, num=None, **hd)
    first = B.r["Configs"]
    n = len(A.CONFIGS)
    links = [(0, "lakh"), (1, "pct"), (2, "pct"), (3, "yrs"), (4, "lakh"), (8, "pct"), (9, "int")]
    for i, (name, loc, prop, roast, mix) in enumerate(A.CONFIGS):
        r = B.nr()
        B.put(r, 1, i + 1, num="idx", inp=False, align="center")
        B._set(f"cfgname_{i + 1}", r, 2)
        B.put(r, 2, name, num=None, inp=True, bold=True)
        for j, (v, lst) in enumerate([(loc, "LocList"), (prop, "PropList"), (roast, "RoastList"),
                                      (mix, "MixList")]):
            B.put(r, 3 + j, v, num=None, inp=True)
            ws.data_validation(r, 3 + j, r, 3 + j, {"validate": "list", "source": "=" + lst})
        for k, (oj, num) in enumerate(links):
            B.put(r, 8 + k, "=" + B.dref("cfg", i, oj), num=num)
        B.put(r, 15, f"=RANK(I{r + 1},$I${first + 1}:$I${first + n})", num="idx", align="center")
    last = B.r["Configs"] - 1
    for c, name in [(2, "CfgName"), (3, "CfgLoc"), (4, "CfgProp"), (5, "CfgRoast"), (6, "CfgMix")]:
        col = "ABCDEFG"[c]
        B.define(name, f"=Configs!${col}${first + 1}:${col}${last + 1}")
    ws.conditional_format(f"I{first + 1}:I{last + 1}", {"type": "data_bar", "bar_color": "#C68B59",
                                                        "bar_solid": True})
    ws.conditional_format(f"K{first + 1}:K{last + 1}", {"type": "3_color_scale",
                                                        "min_color": "#F8D7DA", "mid_color": "#FFFFFF",
                                                        "max_color": "#D8F0DC"})
    B.skip()
    B.note("Naming: PN = Prahladnagar, SBR = Sindhu Bhavan Road, GIFT = GIFT City, SAN = Sanand; "
           "R = rent, O = own; Buy / Toll / InH = roasting route; Val / Prm = Value / Premium mix "
           "(default Specialty); Hse = House blend.")


# =============================================================================== Dashboard
def dashboard(B):
    ws = B.use("Dashboard")
    B.title("Dashboard", "Outputs for the configuration and scenario chosen on Inputs. ₹ lakh unless "
            "stated.")
    B.band("Selected configuration")
    for lab, key in [("Location", "a_loc_n"), ("Premises", "a_prop_n"), ("Roasting route", "a_roast_n"),
                     ("Bean mix", "a_mix_n"), ("Scenario", "a_scn_n")]:
        r = B.nr()
        B.put(r, 1, lab, num=None, indent=1)
        B.put(r, 3, "={$%s}" % key, num=None, bold=True)
    B.skip()
    B.band("Key outputs")
    left = [("Total capital requirement", "k_tcr", "lakh"), ("Promoter equity", "k_eq", "lakh"),
            ("Term loan", "k_debt", "lakh"), ("WACC", "wacc", "pct"), ("Cost of equity", "ke", "pct"),
            ("Project NPV", "npv", "lakh"), ("Project IRR", "irr_p", "pct"),
            ("Equity IRR", "irr_e", "pct"), ("Equity NPV at cost of equity", "npv_e", "lakh"),
            ("Equity multiple", "moic", "x"), ("Terminal value share of value", "tv_share", "pct"),
            ("Implied exit EV/EBITDA", "tv_mult", "x")]
    right = [("Payback from opening", "payback", "yrs"), ("Discounted payback", "dpayback", "yrs"),
             ("Revenue Y3", "y3_rev", "lakh"), ("EBITDA Y3", "y3_ebitda", "lakh"),
             ("EBITDA margin Y3", "y3_margin", "pct"), ("Bills per day Y3", "y3_bills", "int"),
             ("Break-even bills per day Y3", "be_y3", "int"), ("Margin of safety Y3", "mos_y3", "pct"),
             ("Peak cash-credit draw", "peak_rev", "lakh"), ("Minimum DSCR (Y2 on)", "min_dscr", "x"),
             ("Pre-tax ROCE Y5", "roce_y5", "pct"), ("Cash lost if shut after Y3", "exit3", "lakh")]
    for (l1, k1, n1), (l2, k2, n2) in zip(left, right):
        r = B.nr()
        B.put(r, 1, l1, num=None, indent=1)
        B.put(r, 3, "={$%s}" % k1, num=n1, bold=True)
        B.put(r, 5, l2, num=None)
        B.put(r, 9, "={$%s}" % k2, num=n2, bold=True)
    B.skip()
    B.band("Financial summary (₹ lakh)")
    r = B.nr()
    B._set("db_fy", r, TL0)
    for i, col in enumerate(TC):
        B.put(r, TL0 + i, B.fx("={m_fy}", col), num="fy", bold=True, bg_color=HEAD_FILL, bottom=1,
              align="right")
    B.put(r, 1, "₹ lakh", num=None, bold=True, bg_color=HEAD_FILL, bottom=1)
    for c in (2, 3, 4):
        B.put(r, c, None, bg_color=HEAD_FILL, bottom=1)
    summ = [("db_bills", "Bills per day", "#", "bills", "int"), ("db_atv", "Average bill (₹)", "₹", "atv", "int"),
            ("db_rev", "Revenue", "₹ lakh", "is_rev", "lakh"), ("db_gm", "Gross margin", "%", "is_gm", "pct"),
            ("db_ebitda", "EBITDA", "₹ lakh", "is_ebitda", "lakh"),
            ("db_ebm", "EBITDA margin", "%", "is_ebitda_m", "pct"), ("db_pat", "Profit after tax", "₹ lakh", "is_pat", "lakh"),
            ("db_cfo", "Cash from operations", "₹ lakh", "cf_cfo", "lakh"),
            ("db_capex", "Capex", "₹ lakh", "cf_capex", "lakh"), ("db_fcff", "Free cash flow to firm", "₹ lakh", "fcff", "lakh"),
            ("db_cum", "Cumulative FCFF", "₹ lakh", "cum_fcff", "lakh"),
            ("db_cash", "Closing cash", "₹ lakh", "bs_cash", "lakh"),
            ("db_debt", "Debt (term loan + cash credit)", "₹ lakh", None, "lakh"),
            ("db_eq", "Shareholders' equity", "₹ lakh", "bs_eq", "lakh")]
    for key, lab, unit, src, num in summ:
        spec = "={%s}" % src if src else "={tl_close}+{rv_close}"
        B.line(key, lab, unit, spec, num=num, bold=key in ("db_rev", "db_ebitda", "db_fcff"))
    B.skip()
    B.band("Scenario analysis (from Scenarios T1)")
    r = B.nr()
    cols = [(0, "NPV", "lakh"), (1, "Project IRR", "pct"), (2, "Equity IRR", "pct"),
            (4, "Payback", "yrs"), (7, "Y3 revenue", "lakh"), (8, "Y3 EBITDA %", "pct"),
            (9, "Break-even bills", "int"), (6, "Capital need", "lakh")]
    hd = dict(bold=True, bg_color=HEAD_FILL, bottom=1, align="center", text_wrap=True)
    ws.set_row(r, 30)
    B.put(r, 1, "Scenario", num=None, **{**hd, "align": "left"})
    for j, (_, h, _n) in enumerate(cols):
        B.put(r, TL0 + j, h, num=None, **hd)
    for i, s in enumerate(A.SCENARIOS):
        r = B.nr()
        B.put(r, 1, s, num=None, indent=1, bold=True)
        for j, (oj, _h, num) in enumerate(cols):
            B.put(r, TL0 + j, "=" + B.dref("scn", i, oj), num=num)
    B.skip()
    B.band("Rent vs own, by location (from Scenarios T2)")
    r = B.nr()
    ws.set_row(r, 30)
    B.put(r, 1, "Location", num=None, **{**hd, "align": "left"})
    heads = ["NPV Rent", "NPV Own", "IRR Rent", "IRR Own", "Eq. IRR Rent", "Eq. IRR Own",
             "Capital Rent", "Capital Own"]
    for j, h in enumerate(heads):
        B.put(r, TL0 + j, h, num=None, **hd)
    for i, loc in enumerate(A.LOCATIONS):
        r = B.nr()
        B.put(r, 1, loc, num=None, indent=1, bold=True)
        for j, (tab, side, num) in enumerate([("locprop_npv", 0, "lakh"), ("locprop_npv", 1, "lakh"),
                                              ("locprop_irr", 0, "pct"), ("locprop_irr", 1, "pct"),
                                              ("locprop_eirr", 0, "pct"), ("locprop_eirr", 1, "pct"),
                                              ("locprop_tcr", 0, "lakh"), ("locprop_tcr", 1, "lakh")]):
            B.put(r, TL0 + j, "=" + B.dref(tab, i, side), num=num)
    B.skip()
    B.band("Charts")
    anchor = B.r["Dashboard"]
    wb = B.wb
    sh = "Model"
    _, r_fy, _ = B._get("m_fy")
    _, r_rev, _ = B._get("is_rev")
    _, r_eb, _ = B._get("is_ebitda")
    _, r_pat, _ = B._get("is_pat")
    _, r_ebm, _ = B._get("is_ebitda_m")
    cats = [sh, r_fy, TL0 + 1, r_fy, TL0 + NT - 1]
    ch = wb.add_chart({"type": "column"})
    ch.add_series({"name": "Revenue", "categories": cats, "values": [sh, r_rev, TL0 + 1, r_rev, TL0 + NT - 1],
                   "fill": {"color": "#C68B59"}, "gap": 60})
    ch.add_series({"name": "EBITDA", "categories": cats, "values": [sh, r_eb, TL0 + 1, r_eb, TL0 + NT - 1],
                   "fill": {"color": "#4E342E"}})
    ln = wb.add_chart({"type": "line"})
    ln.add_series({"name": "EBITDA margin", "categories": cats,
                   "values": [sh, r_ebm, TL0 + 1, r_ebm, TL0 + NT - 1], "y2_axis": True,
                   "line": {"color": "#2E8B57", "width": 2.25}, "marker": {"type": "circle"}})
    ch.combine(ln)
    ch.set_title({"name": "Revenue, EBITDA (₹ lakh) and EBITDA margin", "name_font": {"size": 11}})
    ch.set_legend({"position": "bottom"})
    ln.set_y2_axis({"num_format": "0%"})
    ch.set_size({"width": 620, "height": 300})
    ws.insert_chart(anchor, 1, ch)

    dsh = "DCF"
    _, r_dfy, _ = B._get("d_fy")
    _, r_f, _ = B._get("fcff")
    _, r_c, _ = B._get("cum_fcff")
    cats2 = [dsh, r_dfy, TL0, r_dfy, TL0 + NT - 1]
    ch2 = wb.add_chart({"type": "column"})
    ch2.add_series({"name": "FCFF", "categories": cats2, "values": [dsh, r_f, TL0, r_f, TL0 + NT - 1],
                    "fill": {"color": "#C68B59"}, "invert_if_negative": False})
    l2 = wb.add_chart({"type": "line"})
    l2.add_series({"name": "Cumulative FCFF", "categories": cats2,
                   "values": [dsh, r_c, TL0, r_c, TL0 + NT - 1], "line": {"color": "#4E342E", "width": 2.25}})
    ch2.combine(l2)
    ch2.set_title({"name": "Free cash flow to firm (₹ lakh)", "name_font": {"size": 11}})
    ch2.set_legend({"position": "bottom"})
    ch2.set_size({"width": 620, "height": 300})
    ws.insert_chart(anchor, 8, ch2)

    _, r_t0, _ = B._get("tor_lo_0")
    nt = len(A.TORNADO)
    ch3 = wb.add_chart({"type": "bar"})
    ch3.add_series({"name": "Low", "categories": ["Scenarios", r_t0, 1, r_t0 + nt - 1, 1],
                    "values": ["Scenarios", r_t0, 6, r_t0 + nt - 1, 6], "fill": {"color": "#B5523B"}})
    ch3.add_series({"name": "High", "categories": ["Scenarios", r_t0, 1, r_t0 + nt - 1, 1],
                    "values": ["Scenarios", r_t0, 7, r_t0 + nt - 1, 7], "fill": {"color": "#2E8B57"},
                    "overlap": 100, "gap": 40})
    ch3.set_title({"name": "Tornado: change in NPV vs base (₹ lakh)", "name_font": {"size": 11}})
    ch3.set_y_axis({"reverse": True})
    ch3.set_legend({"position": "bottom"})
    ch3.set_size({"width": 620, "height": 320})
    ws.insert_chart(anchor + 16, 1, ch3)

    _, r_c0, _ = B._get("dt_cfg")
    nc = len(A.CONFIGS)
    ch4 = wb.add_chart({"type": "bar"})
    ch4.add_series({"name": "NPV", "categories": ["Scenarios", r_c0, 1, r_c0 + nc - 1, 1],
                    "values": ["Scenarios", r_c0, 3, r_c0 + nc - 1, 3], "fill": {"color": "#C68B59"},
                    "gap": 40})
    ch4.set_title({"name": "Project NPV by configuration (₹ lakh)", "name_font": {"size": 11}})
    ch4.set_y_axis({"reverse": True})
    ch4.set_legend({"none": True})
    ch4.set_size({"width": 620, "height": 420})
    ws.insert_chart(anchor + 16, 8, ch4)


# =============================================================================== Sources
SOURCES = [
    ("Rents, Prahladnagar", "99acres / MagicBricks / housing.com listings, Oct 2026: ₹55-120 per sqft "
     "per month (Titanium Heights, Corporate Road)", "https://www.99acres.com"),
    ("Rents, Sindhu Bhavan Road", "99acres F&B shop 495 sqft ₹1.08 lakh (~₹218/sqft); otloo Time Square-2 "
     "2,651 sqft ₹2.25 lakh", "https://www.99acres.com"),
    ("Purchase prices", "MagicBricks: SBR showroom ₹19,500/sqft; Prahladnagar ₹5,560-9,626/sqft (offices)",
     "https://www.magicbricks.com"),
    ("GIFT City", "99acres coffee shop ₹1 lakh/month; GIFT City RFPs for café/food zone (2026)",
     "https://www.giftgujarat.in"),
    ("Sanand", "Micron Sanand ATMP opened 28 Feb 2026 (~US$2.75 bn); 6 ISM projects in Gujarat, ~50,000 "
     "jobs (ET, Aug 2026)", "https://investors.micron.com"),
    ("Espresso machines", "West End Coffee price comparison: La Marzocco Linea PB 2GR ₹11.26 lakh + GST",
     "https://westendcoffee.co"),
    ("Roasters", "Aaroasta (Rajkot) drum roasters 0.5-50 kg", "https://aaroasta.com"),
    ("Electricity", "Torrent Power Ahmedabad tariff FY2026-27, non-RGP commercial 455 paise/unit + charges",
     "https://www.torrentpower.com"),
    ("Wages", "Gujarat minimum wages from 1 Apr 2026; Indeed/ERI barista pay in Ahmedabad",
     "https://in.indeed.com"),
    ("Risk-free rate & policy rate", "India 10-yr G-sec 7.29% (8 Oct 2026); RBI repo 5.50%",
     "https://tradingeconomics.com/india/government-bond-yield"),
    ("Equity risk premium", "Damodaran, Country risk premiums, Jan 2026 (India: ERP 7.08%, CRP 2.85%)",
     "https://pages.stern.nyu.edu/~adamodar/"),
    ("Café benchmarks", "Industry cost ratios: COGS 25-35%, rent 8-15%, labour, marketing; NRAI India Food "
     "Services Report", "https://nrai.org"),
    ("Chain economics", "Tata Starbucks FY25 revenue ₹1,277 cr (~₹2.7 cr per store); Blue Tokai, Third Wave "
     "filings", "https://www.worldcoffeeportal.com"),
    ("Aggregator fees", "Swiggy/Zomato effective commission ~24-30% incl. GST & discounts (2026 reports)",
     ""),
    ("Coffee prices", "Coffee Board of India; USDA FAS India Coffee Annual (May 2026); ICE Coffee C ~285 c/lb "
     "(9 Oct 2026)", "https://www.fas.usda.gov"),
    ("Tax", "Income-tax Act s.115BAA (25.168%), depreciation block rates (Appendix I)",
     "https://incometaxindia.gov.in"),
]


def sources(B):
    ws = B.use("Sources")
    ws.set_column(0, 0, 2)
    ws.set_column(1, 1, 28)
    ws.set_column(2, 2, 95)
    ws.set_column(3, 3, 45)
    B.title("Sources", "Evidence behind the main assumptions (gathered October 2026). Estimates "
            "without a public source are flagged as judgement in the notes columns.")
    r = B.nr()
    for c, t in [(1, "Topic"), (2, "What was used"), (3, "Source")]:
        B.put(r, c, t, num=None, bold=True, bg_color=HEAD_FILL, bottom=1)
    for topic, what, url in SOURCES:
        r = B.nr()
        B.put(r, 1, topic, num=None, bold=True)
        B.put(r, 2, what, num=None, text_wrap=True)
        if url:
            ws.write_url(r, 3, url, B.f(None, font_color=BLUE, underline=1))
        ws.set_row(r, 30)


# =============================================================================== build
def build(path, reg=None, cache=None, inject=True):
    B = Book(path, reg, cache)
    for name, tab, kind in SHEETS:
        B.add_sheet(name, tab, kind)
    cover(B)
    inputs(B)
    locations(B)
    sourcing(B)
    capex(B)
    model(B)
    dcf(B)
    scenarios(B)
    configs(B)
    dashboard(B)
    sources(B)
    B.wb.worksheets()[0].activate()
    B.close(inject)
    return B


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    tmp = os.path.join(SCRATCH, "pass1.xlsx")
    b1 = build(tmp)
    reg = b1.reg
    if "--no-calc" in sys.argv:
        build(OUT, reg)
        print("written (no cached values):", OUT)
        return
    import recalc
    calc_copy = os.path.join(SCRATCH, "calc_copy.xlsx")
    b2 = build(calc_copy, reg, inject=False)
    cache = recalc.values(calc_copy, b2.calc_cells, b2.tables)
    build(OUT, reg, cache)
    with open(os.path.join(SCRATCH, "layout.json"), "w") as fh:
        json.dump({"reg": {k: list(v) for k, v in reg.items()}}, fh)
    with open(os.path.join(SCRATCH, "cache.json"), "w") as fh:
        json.dump({f"{s}|{r}|{c}": v for (s, r, c), v in cache.items()}, fh)
    print("written with cached values:", OUT)


if __name__ == "__main__":
    main()
