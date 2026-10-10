#!/usr/bin/env python3
"""Run the Excel model headlessly (LibreOffice) for every configuration and scenario
and write results.json, which feeds Part 2 of the PDF report.  Every number in the
report therefore comes from the same workbook the reader can open."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import assumptions as A  # noqa: E402
import build_excel as BE  # noqa: E402
import recalc  # noqa: E402

OUT = os.path.join(HERE, "results.json")
SCRATCH = BE.SCRATCH

FEATURED = [  # id, short name, location, premises, roasting, mix
    ("A", "Sindhu Bhavan Road flagship", "Sindhu Bhavan Road", "Rent", "Toll roasting", "House"),
    ("B", "GIFT City captive café", "GIFT City", "Rent", "Toll roasting", "House"),
    ("C", "Prahladnagar neighbourhood café", "Prahladnagar", "Rent", "Toll roasting", "House"),
    ("D", "Sindhu Bhavan Road, owned unit", "Sindhu Bhavan Road", "Own", "Toll roasting", "House"),
]

SERIES = ["bills", "atv", "days", "bills_yr", "rev_cafe", "rev_bev", "rev_food", "rev_ret", "rev_whs",
          "rev_tot", "cups", "kg_cafe", "kg_roast", "cost_kg", "cogs_coffee", "cogs_milk", "cogs_pack",
          "cogs_food", "cogs_ret", "cogs_whs", "cogs", "staff", "rent", "cam", "ptax", "power", "gaswater",
          "mkt_c", "rm_var", "amc_c", "aggr", "payfee", "admin", "misc", "whs_sell", "preop", "opex",
          "opex_fixed", "be_bills", "is_rev", "is_gp", "is_gm", "is_ebitda", "is_ebitda_m", "is_dep",
          "is_ebit", "is_int", "is_inc", "is_pbt", "is_tax_cur", "is_tax_def", "is_pat", "cf_cfo",
          "cf_capex", "cf_depo", "cf_cfi", "cf_tl_draw", "cf_tl_rep", "cf_rev", "cf_eq", "cf_cff",
          "cf_net", "cf_close", "bs_cash", "bs_ar", "bs_inv", "bs_depo", "bs_ppe", "bs_ta", "bs_ap",
          "bs_rev", "bs_tl", "bs_dtl", "bs_tlb", "bs_sc", "bs_re", "bs_eq", "bs_tle", "bs_chk",
          "capex_tot", "dep_book", "dep_tax", "nwc", "fcff", "pv_fcff", "fcfe", "eq_cf", "cum_fcff",
          "u_tax", "d_nopat", "dscr", "util", "cap_bills", "mos", "m_fy"]
SCALARS = ["npv", "irr_p", "irr_e", "npv_e", "moic", "payback", "dpayback", "k_tcr", "k_eq", "k_debt",
           "wacc", "ke", "w_bl", "w_wd", "g_used", "tv", "pv_tv", "tv_ops", "tv_share", "tv_mult",
           "sum_pv", "y1_rev", "y3_rev", "y3_ebitda", "y3_margin", "y3_pat", "y3_bills", "be_y3",
           "mos_y3", "y3_cogs", "y3_staff", "y3_occ", "y1_ebitda", "y10_rev", "y10_ebitda", "peak_rev",
           "min_dscr", "exit3", "roce_y5", "u_capex", "u_prop", "u_preop", "u_dep", "u_cash", "u_tot",
           "s_debt", "s_eq", "gearing", "loan_rate", "loan_tenor", "area_tot", "prop_price",
           "prop_cost", "cost_act", "payroll_m", "cups_per_bill", "food_sh", "ret_eff",
           "notional_rent", "prop_val"]
KPIS = ["npv", "irr_p", "irr_e", "npv_e", "payback", "dpayback", "k_tcr", "k_eq", "k_debt", "y1_rev",
        "y3_rev", "y3_ebitda", "y3_margin", "y3_pat", "be_y3", "y3_bills", "mos_y3", "peak_rev",
        "min_dscr", "exit3", "wacc", "tv_share", "y10_ebitda", "y3_cogs", "y3_staff", "y3_occ"]
CAPEX_KEYS = [k for k, *_ in A.CAPEX_ITEMS]
TABLES_FEATURED = ["tornado", "wacc_g", "bills_atv", "rent_bills", "green_roast", "whs_roast",
                   "roastmix_npv", "roastmix_m"]
TABLES_DEFAULT = ["locprop_npv", "locprop_irr", "locprop_eirr", "locprop_tcr", "rentown",
                  "roastmix_npv", "roastmix_m", "whs_roast", "scn", "cfg", "cfgscn_npv",
                  "cfgscn_eirr"]


def clean(v):
    if isinstance(v, float):
        return round(v, 6)
    return v


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    b1 = BE.build(os.path.join(SCRATCH, "x_pass1.xlsx"))
    reg = b1.reg
    calc = os.path.join(SCRATCH, "x_calc.xlsx")
    b2 = BE.build(calc, reg, inject=False)
    tspec = {t["sheet"] + ":" + t["cell"]: t for t in b2.tables}
    by_name = {}
    for k, (sh, r, c) in reg.items():
        if k.startswith("dt_"):
            for t in b2.tables:
                if t["sheet"] == sh and t["first"] == r:
                    by_name[k[3:]] = t
    assert tspec
    res = {"configs": [list(c) for c in A.CONFIGS], "featured": [list(f) for f in FEATURED],
           "scenarios": A.SCENARIOS, "years": [], "grid": {}, "models": {}, "tables_default": {}}

    with recalc.Office() as o:
        o.open(calc)

        def g(key, i=None):
            sh, r, c = reg[key]
            return clean(o.get(sh, r, c + (i or 0)))

        def series(key):
            return [g(key, i) for i in range(BE.NT)]

        def setov(**kw):
            for k, v in kw.items():
                o.set(*reg["o_" + k], v)

        def run_tables(names):
            out = {}
            tabs = [by_name[n] for n in names]
            cache = {}
            recalc.emulate_tables(o, tabs, cache)
            for n, t in zip(names, tabs):
                rows = []
                ncol = len(t["across"]) if t["across"] else len(t["outs"])
                for i in range(len(t["down"])):
                    rows.append([clean(cache[(t["sheet"], t["first"] + i, 3 + j)]) for j in range(ncol)])
                out[n] = {"down": t["down"], "across": t["across"], "values": rows}
            return out

        res["years"] = series("m_fy")
        # every configuration in every scenario
        for ci, cfg in enumerate(A.CONFIGS, 1):
            res["grid"][cfg[0]] = {}
            for si, sname in enumerate(A.SCENARIOS, 1):
                setov(cfg=ci, scn=si)
                o.recalc()
                res["grid"][cfg[0]][sname] = {k: g(k) for k in KPIS}
        setov(cfg=0, scn=0)
        o.recalc()
        # default selection (Inputs) tables
        res["tables_default"] = run_tables(TABLES_DEFAULT)
        res["default"] = {k: g(k) for k in SCALARS}
        # featured models
        for fid, fname, loc, prop, roast, mix in FEATURED:
            setov(loc=A.LOCATIONS.index(loc) + 1, prop=A.PROPERTY.index(prop) + 1,
                  roast=A.ROASTING.index(roast) + 1, mix=A.MIXES.index(mix) + 1)
            m = {"name": fname, "location": loc, "premises": prop, "roasting": roast, "mix": mix,
                 "scenarios": {}}
            for si, sname in enumerate(A.SCENARIOS, 1):
                setov(scn=si)
                o.recalc()
                m["scenarios"][sname] = {
                    "series": {k: series(k) for k in SERIES},
                    "scalars": {k: g(k) for k in SCALARS},
                    "capex": {k: g("cx_" + k) for k in CAPEX_KEYS},
                    "classes": {c: g("ci_" + c) for c in A.ASSET_CLASSES},
                }
            setov(scn=0)
            o.recalc()
            m["tables"] = run_tables(TABLES_FEATURED)
            res["models"][fid] = m
        setov(loc=0, prop=0, roast=0, mix=0)
        o.recalc()
        # location-level capex & capital need under each premises option (Base, Toll, House)
        res["locations"] = {}
        for li, loc in enumerate(A.LOCATIONS, 1):
            res["locations"][loc] = {}
            for pi, prop in enumerate(A.PROPERTY, 1):
                for ri, roast in enumerate(A.ROASTING, 1):
                    setov(loc=li, prop=pi, roast=ri, mix=A.MIXES.index("House") + 1)
                    o.recalc()
                    res["locations"][loc][f"{prop}|{roast}"] = {k: g(k) for k in
                                                               ["u_capex", "u_prop", "u_preop", "u_dep",
                                                                "u_cash", "u_tot", "s_debt", "s_eq",
                                                                "npv", "irr_p", "irr_e", "y3_rev",
                                                                "y3_margin", "payroll_m", "be_y3"]}
        setov(loc=0, prop=0, roast=0, mix=0)
        o.recalc()
        # sourcing matrix straight from the Sourcing sheet
        res["sourcing"] = {}
        for key in ["green", "whs", "glink", "conv_buy", "conv_toll", "conv_inh", "cost_buy",
                    "cost_toll", "cost_inh", "cup_cost"]:
            sh, r, c = reg["sx_" + key]
            res["sourcing"][key] = [clean(o.get(sh, r, 5 + j)) for j in range(4)]
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
