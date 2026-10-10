"""Default inputs for the Ahmedabad café financial model (single source of truth).

Every value here is written into the Excel workbook as a blue input cell, so the
user can change it there.  Units: rupees unless stated; model outputs are in
₹ lakh (1 lakh = ₹100,000).  Prices are as researched in Oct 2026.
"""

FIRST_FY = 2027          # Year 0 = FY2026-27 (fit-out, pre-opening, ends 31 Mar 2027)
N_YEARS = 10             # operating years FY2028 ... FY2037
LAKH = 100_000

# --------------------------------------------------------------------------- selectors
LOCATIONS = ["Prahladnagar", "Sindhu Bhavan Road", "GIFT City", "Sanand"]
PROPERTY = ["Rent", "Own"]
ROASTING = ["Buy roasted", "Toll roasting", "In-house roastery"]
MIXES = ["Value", "Specialty", "Premium", "House"]
SCENARIOS = ["Best", "Base", "Worst"]

DEFAULT_SELECTION = dict(location="Prahladnagar", property="Rent", roasting="Toll roasting",
                         mix="House", scenario="Base")

# --------------------------------------------------------------------------- locations
# (key, label, units, [Prahladnagar, Sindhu Bhavan Road, GIFT City, Sanand], note)
LOCATION_ROWS = [
    ("area", "Café carpet area", "sqft", [1000, 1200, 900, 1000],
     "Ground-floor, street-facing unit; 36-52 seats"),
    ("seats", "Seats", "#", [40, 52, 36, 40], "~22-25 sqft per seat incl. counter & kitchen"),
    ("rent_psf", "Rent", "₹/sqft/mth", [115, 175, 110, 50],
     "Listings Oct 2026: Prahladnagar ₹55-120, SBR ₹85-220 (F&B frontage at top end), "
     "GIFT ~₹110, Sanand est."),
    ("cam_psf", "CAM / maintenance", "₹/sqft/mth", [4, 5, 15, 2], "Grade-A towers in GIFT charge high CAM"),
    ("deposit_m", "Security deposit", "months", [4, 6, 6, 3], "Refundable; 2-6 months typical"),
    ("fitout_psf", "Interiors, civil & MEP", "₹/sqft", [2600, 3000, 2600, 2000],
     "Incl. design fees; excludes equipment"),
    ("purchase_psf", "Purchase price (own case)", "₹/sqft", [17500, 24000, 14000, 6500],
     "Ground-floor retail, carpet basis; SBR showrooms listed ₹19.5-21.5k on built-up area"),
    ("bills_ss", "Steady-state bills per day", "#", [140, 170, 150, 110],
     "Year-3 demand at 100% ramp (Base footfall factor 1.0)"),
    ("atv", "Average bill value (ex-GST, FY28)", "₹", [320, 360, 330, 260],
     "Specialty cafés ₹500-1,500 for two in Ahmedabad listings"),
    ("op_days", "Operating days per year", "days", [360, 360, 290, 350],
     "GIFT City: weekday-heavy demand"),
    ("delivery", "Delivery share of café revenue", "%", [0.15, 0.10, 0.06, 0.15],
     "Swiggy/Zomato orders"),
    ("growth_prem", "Extra volume growth, Y2-Y6", "% p.a.", [0.0, 0.005, 0.04, 0.05],
     "GIFT workforce & Sanand semiconductor jobs growth"),
    ("staff_f", "Staffing factor", "x", [1.00, 1.20, 0.95, 0.90], "Headcount scale vs base roster"),
    ("whs_f", "Wholesale potential factor", "x", [1.0, 1.0, 1.2, 1.3],
     "Office pantries (GIFT), industrial canteens (Sanand)"),
    ("ptax_psf", "Property tax & society charges (own)", "₹/sqft/yr", [35, 40, 30, 15], ""),
    ("apprec", "Property appreciation (own)", "% p.a.", [0.05, 0.06, 0.07, 0.06], ""),
]
LOCATION_PROFILE = {
    "Prahladnagar": "Corporate Road / 100 ft road office & upscale-residential belt. Dense chain "
                    "competition (Starbucks, Third Wave, Slay, The Dark Roast).",
    "Sindhu Bhavan Road": "Ahmedabad's premier F&B high street (Bodakdev). Highest footfall and "
                          "spend, evening/weekend peaks, highest rents.",
    "GIFT City": "India's IFSC: captive, fast-growing white-collar workforce (>12k, target 1 lakh "
                 "jobs by 2030), few quality cafés, weekday demand.",
    "Sanand": "Industrial boom town: Micron ATMP (opened Feb 2026), Tata EV plants; ~50k semicon "
              "jobs planned in Gujarat. Cheap space, low ATV, first-mover play.",
}

# --------------------------------------------------------------------------- sourcing
GREEN_TYPES = ["Commodity arabica (Plantation A)", "Commodity robusta", "Fine robusta (washed)",
               "Estate specialty arabica (83-85)", "Micro-lot (86+)"]
GREEN_PRICE = [600, 440, 520, 950, 2200]            # ₹/kg green, Oct 2026
WHOLESALE_ROASTED = [1050, 900, 1150, 1700, 3200]   # ₹/kg roasted bought from a roaster
MIX_SHARES = {                                      # share of each green type
    "Value":     [0.50, 0.50, 0.00, 0.00, 0.00],
    "Specialty": [0.00, 0.00, 0.20, 0.75, 0.05],
    "Premium":   [0.00, 0.00, 0.10, 0.50, 0.40],
    "House":     [0.00, 0.00, 0.15, 0.70, 0.15],
}
SOURCING = dict(shrink=0.16, toll_fee=180, freight=25, inhouse_var=35, cafe_pack=10,
                retail_pack=48, whs_pack=45)
# demand & price effects of the bean mix (vs the Specialty mix), own-label retail and wholesale prices.
# "House" is the recommended blend: 15% washed robusta, 70% estate arabica, 15% micro-lot.
MIX_EFFECTS = [  # key, label, units, [Value, Specialty, Premium, House], note
    ("atv_prem", "Average-bill premium vs Specialty", "%", [-0.10, 0.0, 0.05, 0.02],
     "Menu pricing the bean quality supports"),
    ("foot_eff", "Footfall effect vs Specialty", "%", [0.05, 0.0, -0.05, 0.0],
     "Value draws a broader crowd; Premium narrows it"),
    ("retail_price", "Retail bean price (own label)", "₹/kg", [1600, 2400, 3600, 2800],
     "₹400 / ₹600 / ₹900 / ₹700 per 250 g bag"),
    ("whs_price", "Wholesale roasted-bean price (FY28)", "₹/kg", [900, 1450, 2300, 1700],
     "To offices, cafés & hotels (in-house roastery only)"),
]

# --------------------------------------------------------------------------- revenue & COGS
REVENUE = dict(bev_share=0.62, retail_share=0.06, own_label_uplift=0.02, bev_price=220,
               coffee_share=0.85, grams=18, milk_other=24, takeaway_share=0.25, pack_per_bill=15,
               food_cogs=0.38, retail_price=2400, resale_margin=0.30,
               whs_selling=0.08, whs_growth=0.05, cost_infl=0.05)
WHOLESALE_RAMP = [0.30, 0.60] + [1.0] * 8          # Y1..Y10 share of maturity volume

# --------------------------------------------------------------------------- operating costs
STAFF = [  # role, headcount, monthly salary ₹, in-house-roastery only?
    ("Café manager", 1, 45000, False),
    ("Head barista", 1, 30000, False),
    ("Baristas", 4, 19000, False),
    ("Kitchen lead", 1, 28000, False),
    ("Kitchen assistants", 2, 16000, False),
    ("Service staff", 3, 15000, False),
    ("Housekeeping & dishwash", 2, 13500, False),
    ("Roaster & wholesale (in-house only)", 1, 32000, True),
]
CAPACITY = dict(max_turns=6.0, staff_elastic=0.5)   # seat turns/day cap; staff growth per 1% extra bills
OPEX = dict(staff_load=0.15, wage_growth=0.08, kwh_psf=5.0, tariff=9.5, tariff_growth=0.04,
            gas_water_m=15000, mkt_y1=0.05, mkt=0.03, rm_pct=0.015, amc=60000, roaster_amc=60000,
            aggregator=0.25, payment=0.007, admin_fixed=300000, misc_pct=0.01, opex_infl=0.05,
            rent_esc=0.05, roastery_area=150)
PREOPEN = dict(rent_months=2, training_months=1.0, launch_mkt=300000, licences=150000,
               recruitment=50000, utilities_misc=50000)

# --------------------------------------------------------------------------- capex
# key, item, basis ('lump' ₹, 'psf' ₹/sqft of café area, 'seat' ₹/seat, 'roast' lump in-house only,
# 'roast_psf' ₹/sqft of roastery area), value, asset class
CAPEX_ITEMS = [
    ("interiors", "Interiors, civil, MEP & design", "loc_psf", 0, "Interiors"),
    ("hvac", "HVAC (ductable / split ACs)", "psf", 450, "Equipment"),
    ("electrical", "Electrical upgrade, UPS & DG share", "lump", 250000, "Equipment"),
    ("espresso", "Espresso machine, 2-group multi-boiler", "lump", 800000, "Equipment"),
    ("grinders", "Grinders: 2 on-demand espresso + 1 filter", "lump", 420000, "Equipment"),
    ("brewbar", "Brew bar, cold-brew kit & water boiler", "lump", 150000, "Equipment"),
    ("kitchen", "Kitchen equipment & refrigeration", "lump", 550000, "Equipment"),
    ("water", "Water treatment (RO + softener + remineralisation)", "lump", 100000, "Equipment"),
    ("furniture", "Furniture & seating", "seat", 12000, "Furniture"),
    ("smallwares", "Crockery, glassware & smallwares", "lump", 150000, "Furniture"),
    ("signage", "Signage & branding", "lump", 200000, "Furniture"),
    ("it", "POS, CCTV, audio & Wi-Fi", "lump", 180000, "IT"),
    ("roaster", "3 kg drum roaster (Indian-made) incl. install", "roast", 900000, "Roastery"),
    ("afterburner", "Afterburner, chimney & ducting", "roast", 250000, "Roastery"),
    ("qc", "QC & packing kit (moisture meter, sealer, sample roaster)", "roast", 150000, "Roastery"),
    ("roast_fitout", "Roastery area fit-out (150 sqft)", "roast_psf", 0, "Interiors"),
]
ASSET_CLASSES = ["Interiors", "Equipment", "Furniture", "IT", "Roastery", "Building", "Land"]
BOOK_LIFE = dict(Interiors=9, Equipment=8, Furniture=8, IT=4, Roastery=10, Building=60, Land=0)
TAX_WDV = dict(Interiors=0.10, Equipment=0.15, Furniture=0.10, IT=0.40, Roastery=0.15,
               Building=0.10, Land=0.0)
CAPEX_OTHER = dict(maint_pct=0.015, refurb_year=6, refurb_pct=0.25, stamp=0.059, legal=0.005,
                   land_share=0.40, ongoing_life=5, ongoing_tax=0.15)

# --------------------------------------------------------------------------- working capital, financing, tax
WC = dict(ar_delivery_days=7, ar_wholesale_days=30, inv_days=18, green_inv_days=40, ap_days=15)
FIN = dict(equity_threshold=1500000, debt_pct_rent=0.50, debt_pct_own=0.60, rate_rent=0.110,
           rate_own=0.100, tenor_rent=5, tenor_own=10, revolver_rate=0.125, min_cash=300000, reserve_m=3,
           cash_rate=0.04, payout=0.0)
TAX_RATE = 0.25168          # s.115BAA: 22% + 10% surcharge + 4% cess
DCF = dict(rf=0.0729, erp=0.0708, beta_u=0.80, specific=0.05, g=0.04, exit_mult=5.0,
           sell_cost=0.02, cgt=0.143, mid_year=0, salvage=0.30)

# --------------------------------------------------------------------------- scenario drivers
def _grow(start, g, n=N_YEARS):
    return [round(start * (1 + g) ** i, 4) for i in range(n)]

DRIVERS = {  # per-year (Y1..Y10) or single values, by scenario [Best, Base, Worst]
    "ramp": ("Ramp-up (% of steady-state bills)", "%",
             [[0.80, 0.95] + [1.0] * 8,
              [0.65, 0.85] + [1.0] * 8,
              [0.50, 0.70, 0.88] + [0.95] * 7]),
    "atv_g": ("Menu price increase", "% p.a.",
              [[0.0] + [0.06] * 9, [0.0] + [0.05] * 9, [0.0] + [0.035] * 9]),
    "vol_g": ("Volume growth after ramp (Y4+)", "% p.a.",
              [[0, 0, 0] + [0.04] * 7, [0, 0, 0] + [0.025] * 7, [0, 0, 0] + [0.005] * 7]),
    "green_ix": ("Green-coffee price index (Oct 2026 = 1.00)", "x",
                 [_grow(0.90, 0.03), _grow(1.00, 0.03), _grow(1.25, 0.03)]),
}
SINGLE_DRIVERS = {
    "footfall": ("Footfall factor on steady-state bills", "x", [1.15, 1.00, 0.82]),
    "overrun": ("Capex overrun", "%", [0.0, 0.05, 0.15]),
    "whs_kg": ("Wholesale beans at maturity (in-house only)", "kg/mth", [250, 150, 60]),
}

# --------------------------------------------------------------------------- configurations compared
CONFIGS = [  # name, location, property, roasting, mix
    ("PN-R-Buy", "Prahladnagar", "Rent", "Buy roasted", "Specialty"),
    ("PN-R-Toll", "Prahladnagar", "Rent", "Toll roasting", "Specialty"),
    ("PN-R-InH", "Prahladnagar", "Rent", "In-house roastery", "Specialty"),
    ("PN-O-Toll", "Prahladnagar", "Own", "Toll roasting", "Specialty"),
    ("PN-R-Toll-Val", "Prahladnagar", "Rent", "Toll roasting", "Value"),
    ("PN-R-Toll-Prm", "Prahladnagar", "Rent", "Toll roasting", "Premium"),
    ("PN-R-Toll-Hse", "Prahladnagar", "Rent", "Toll roasting", "House"),
    ("SBR-R-Buy", "Sindhu Bhavan Road", "Rent", "Buy roasted", "Specialty"),
    ("SBR-R-Toll", "Sindhu Bhavan Road", "Rent", "Toll roasting", "Specialty"),
    ("SBR-R-InH", "Sindhu Bhavan Road", "Rent", "In-house roastery", "Specialty"),
    ("SBR-O-Toll", "Sindhu Bhavan Road", "Own", "Toll roasting", "Specialty"),
    ("SBR-R-Toll-Hse", "Sindhu Bhavan Road", "Rent", "Toll roasting", "House"),
    ("GIFT-R-Buy", "GIFT City", "Rent", "Buy roasted", "Specialty"),
    ("GIFT-R-Toll", "GIFT City", "Rent", "Toll roasting", "Specialty"),
    ("GIFT-R-InH", "GIFT City", "Rent", "In-house roastery", "Specialty"),
    ("GIFT-O-Toll", "GIFT City", "Own", "Toll roasting", "Specialty"),
    ("GIFT-R-Toll-Hse", "GIFT City", "Rent", "Toll roasting", "House"),
    ("SAN-R-Toll", "Sanand", "Rent", "Toll roasting", "Specialty"),
    ("SAN-R-InH", "Sanand", "Rent", "In-house roastery", "Specialty"),
    ("SAN-O-Toll", "Sanand", "Own", "Toll roasting", "Specialty"),
]

# --------------------------------------------------------------------------- tornado (one at a time)
TORNADO = [  # label, low, high (multipliers unless stated)
    ("Bills per day", 0.85, 1.15),
    ("Average bill value", 0.90, 1.10),
    ("Rent", 0.80, 1.20),
    ("Green-coffee price", 0.70, 1.30),
    ("Capex", 0.85, 1.20),
    ("Staff cost", 0.90, 1.15),
    ("WACC (+/- pp)", -0.02, 0.02),
    ("Terminal growth (abs.)", 0.03, 0.05),
]
