"""Lab 10: Elevance Health (ELV), FY2026-2030 three-statement forecast.

Run: python3 lab10_proforma_elv.py [--check | --break-cash | --sensitivity]
Python standard library only. USD millions, shares in millions, except $/share.
Model origin: 2025-12-31. Historical-base exercise, not a current fair value.
All forecast choices are judgments; source details and reasons: lab-10-elv.md.
"""
import argparse
from copy import deepcopy
import math

SOURCES = {
    2023: "https://www.sec.gov/Archives/edgar/data/1156039/000115603924000015/elv-20231231.htm",
    2024: "https://s202.q4cdn.com/665319960/files/doc_financials/2025/ar/Elevance-Health-2024-10K-color.pdf",
    2025: "https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm",
}
# Each year's own 10-K: consolidated balance sheet, income and cash flows; Note 9.
# None means not separately disclosed/confirmed; it never means zero inventory.
HISTORY = {
    2023: dict(revenue=170209., prior_revenue=155660., benefits=124330., products=17293.,
               opex=20087., net_income=5991., common_income=5987., inventory=None,
               ppe=4359., equity=39306., dep=107., software_amort=765.,
               cf_da=1745., intangible_amort=885., capex=1296., tax=1724.,
               pretax=7715., claims=16111., cfo=8061.),
    2024: dict(revenue=175204., prior_revenue=170209., benefits=127567., products=19750.,
               opex=20025., net_income=5971., common_income=5980., inventory=None,
               ppe=4652., equity=41315., dep=105., software_amort=809.,
               cf_da=1393., intangible_amort=580., capex=1256., tax=1933.,
               pretax=7904., claims=15746., cfo=5808.),
    2025: dict(revenue=197584., prior_revenue=175204., benefits=148223., products=21178.,
               opex=20984., net_income=5661., common_income=5662., inventory=None,
               ppe=4679., equity=43882., dep=94., software_amort=885.,
               cf_da=1546., intangible_amort=628., capex=1116., tax=1049.,
               pretax=6710., claims=17084., cfo=4290.),
}
OPENING = dict(year=2025, revenue=197584., cash=9491., receivables=21542.,
               ppe=4679., investments=38584., intangibles=11200., other_assets=35998.,
               claims=17084., debt=32046., revolver=0., other_liabilities=28338.,
               equity=43882., nci=144.)
# Carrying historical ratios into future years is a judgment, not guidance.
ASSUMPTIONS = dict(
    growth=[.03]*5, margin=[.143, .145, .147, .148, .148],
    cash_opex_ratio=[.712, .708, .704, .700, .700],
    ppe_da_ratio=(94+885)/4679, intangible_amort=628., capex=1116., tax=.24,
    benefit_share=148223/(148223+21178), claims_to_benefits=17084/148223,
    receivables_ratio=21542/197584, other_wc_ratio=5344/197584,
    investment_income=2194-398, debt_rate=1402/32046, net_repayment=1000.,
    buyback=2605., dividend=1529., minimum_cash=9491.,
    revolver_limit=5000., revolver_rate=.06, ke=.10, terminal_growth=.025,
    shares=220.723898,
)
# Same-day intraday search snapshot; not a verified closing quote or live feed.
MARKET_PRICE = 396.98
MARKET_DATE = "2026-09-24 intraday; provider time 14:24:20 (zone unspecified)"
MARKET_SOURCE = "https://www.investing.com/equities/wellpoint-inc-historical-data"
TOL = 1e-6


def totals(r):
    assets = sum(r[k] for k in ("cash", "receivables", "ppe", "investments", "intangibles", "other_assets"))
    liabilities = sum(r[k] for k in ("claims", "debt", "revolver", "other_liabilities"))
    return assets, liabilities, assets-liabilities-r["equity"]-r["nci"]


def check(rows, a):
    """Recompute checks from components; raise rather than force a balance."""
    for r in rows:
        year = r["year"]
        if any(not math.isfinite(v) for v in r.values() if isinstance(v, (int, float))):
            raise ValueError(f"FY{year}: non-finite output")
        gap = totals(r)[2]
        if abs(gap) > TOL:
            raise ValueError(f"FY{year}: assets - liabilities - equity gap = {gap:.1f}")
        if r["cash"] < a["minimum_cash"]-TOL:
            raise ValueError(f"FY{year}: cash below floor by {a['minimum_cash']-r['cash']:.1f}")
        if not -TOL <= r["revolver"] <= a["revolver_limit"]+TOL:
            raise ValueError(f"FY{year}: revolver outside capacity")
        if min(r[k] for k in ("debt", "ppe", "intangibles")) < -TOL:
            raise ValueError(f"FY{year}: negative debt or long-lived asset")
        if "cfo" in r:
            cash_gap = r["cash"]-r["opening_cash"]-r["cfo"]-r["cfi"]-r["cff"]
            if abs(cash_gap) > TOL:
                raise ValueError(f"FY{year}: cash-flow reconciliation gap = {cash_gap:.1f}")


def project(a=ASSUMPTIONS):
    p = dict(OPENING)
    check([p], a)
    rows = []
    for i, year in enumerate(range(2026, 2031)):
        r = dict(p, year=year)
        r["revenue"] = p["revenue"]*(1+a["growth"][i])
        r["gross_profit"] = r["revenue"]*a["margin"][i]
        r["direct_costs"] = r["revenue"]-r["gross_profit"]
        r["benefits"] = r["direct_costs"]*a["benefit_share"]
        r["products"] = r["direct_costs"]-r["benefits"]
        r["cash_opex"] = r["gross_profit"]*a["cash_opex_ratio"][i]
        r["ppe_da"] = p["ppe"]*a["ppe_da_ratio"]
        r["amort"] = a["intangible_amort"]
        r["operating_income"] = r["gross_profit"]-r["cash_opex"]-r["ppe_da"]-r["amort"]
        r["investment_income"] = a["investment_income"]
        r["interest"] = p["debt"]*a["debt_rate"]+p["revolver"]*a["revolver_rate"]
        r["pretax"] = r["operating_income"]+r["investment_income"]-r["interest"]
        r["tax"] = max(0., r["pretax"])*a["tax"]
        r["net_income"] = r["pretax"]-r["tax"]
        r["receivables"] = r["revenue"]*a["receivables_ratio"]
        r["claims"] = r["benefits"]*a["claims_to_benefits"]
        r["other_wc_change"] = (r["revenue"]-p["revenue"])*a["other_wc_ratio"]
        r["other_assets"] = p["other_assets"]+r["other_wc_change"]
        r["capex"] = a["capex"]
        r["ppe"] = p["ppe"]+r["capex"]-r["ppe_da"]
        r["intangibles"] = p["intangibles"]-r["amort"]
        r["repayment"] = min(a["net_repayment"], p["debt"])
        r["debt"] = p["debt"]-r["repayment"]
        r["buyback"], r["dividend"] = a["buyback"], a["dividend"]
        r["equity"] = p["equity"]+r["net_income"]-r["buyback"]-r["dividend"]
        # Investment assets, other liabilities and NCI flat; no future OCI or NCI income.
        r["receivables_change"] = r["receivables"]-p["receivables"]
        r["claims_change"] = r["claims"]-p["claims"]
        r["cfo"] = (r["net_income"]+r["ppe_da"]+r["amort"]-r["receivables_change"]
                    -r["other_wc_change"]+r["claims_change"])
        r["cfi"] = -r["capex"]
        r["fcfe"] = r["cfo"]+r["cfi"]-r["repayment"]
        r["opening_cash"] = p["cash"]
        available = p["cash"]+r["fcfe"]-r["buyback"]-r["dividend"]
        if available < a["minimum_cash"]:
            r["revolver_change"] = min(a["minimum_cash"]-available, a["revolver_limit"]-p["revolver"])
        else:
            r["revolver_change"] = -min(available-a["minimum_cash"], p["revolver"])
        r["revolver"] = p["revolver"]+r["revolver_change"]
        r["cff"] = -r["repayment"]-r["buyback"]-r["dividend"]+r["revolver_change"]
        r["cash_change"] = r["cfo"]+r["cfi"]+r["cff"]
        r["cash"] = p["cash"]+r["cash_change"]
        check([r], a)
        rows.append(r)
        p = r
    return rows


def value(rows, a=ASSUMPTIONS):
    check(rows, a)
    ke, g = a["ke"], a["terminal_growth"]
    if not (-1 < g < ke) or ke <= -1 or a["shares"] <= 0:
        raise ValueError("Require -100% < terminal growth < cost of equity; shares > 0")
    # Lab 09 terminal convention: net scheduled debt paydown stops after 2030.
    terminal_fcfe = (rows[-1]["fcfe"]+rows[-1]["repayment"])*(1+g)
    if rows[-1]["fcfe"] <= 0 or terminal_fcfe <= 0:
        raise ValueError("No terminal value on nonpositive final FCFE; model recovery explicitly")
    # Lab 10 specifies valuing only positive years if an interim FCFE is negative.
    # This classroom convention is optimistic; a full economic DCF includes funding needs.
    pv_flows = sum(max(0., r["fcfe"])/(1+ke)**t for t, r in enumerate(rows, 1))
    terminal = terminal_fcfe/(ke-g)
    pv_terminal = terminal/(1+ke)**len(rows)
    equity = pv_flows+pv_terminal
    return dict(pv_flows=pv_flows, terminal_fcfe=terminal_fcfe, terminal=terminal,
                pv_terminal=pv_terminal, equity=equity, per_share=equity/a["shares"],
                terminal_share=pv_terminal/equity)


def history_ratios():
    for year, h in HISTORY.items():
        gp = h["revenue"]-h["benefits"]-h["products"]
        ppe_da = h["dep"]+h["software_amort"]
        yield year, dict(gross_profit=gp, gross_margin=gp/h["revenue"],
                         opex_gp=h["opex"]/gp, cash_opex_gp=(h["opex"]-ppe_da)/gp,
                         depreciation_ppe=h["dep"]/h["ppe"], ppe_da_ppe=ppe_da/h["ppe"],
                         tax_rate=h["tax"]/h["pretax"], growth=h["revenue"]/h["prior_revenue"]-1,
                         claims_days=h["claims"]/h["benefits"]*365)


def table(title, rows, fields):
    print(f"\n{title}\n")
    print("| USD millions | " + " | ".join(f"FY{r['year']}E" for r in rows) + " |")
    print("|---|" + "---:|"*len(rows))
    for label, key, sign in fields:
        nums = [r[key]*sign for r in rows]
        print(f"| {label} | " + " | ".join(f"{0 if abs(n)<TOL else n:,.1f}" for n in nums) + " |")


def show(rows, a=ASSUMPTIONS):
    check(rows, a)
    print("# Lab 10 results - Elevance Health, Inc. (NYSE: ELV)\n\nOrigin: December 31, 2025. Forecasts are judgments.")
    print("Units: USD millions, except shares in millions and value per share.")
    v = value(rows, a)
    print(f"\nThe ELV forecast implies **${v['per_share']:.2f} per opening common share**, "
          f"or **${v['equity']/1000:.2f} billion of common-equity value**.")
    print(f"Revenue increases from ${rows[0]['revenue']/1000:.2f} billion in 2026 "
          f"to ${rows[-1]['revenue']/1000:.2f} billion in 2030; annual FCFE rises "
          f"from ${rows[0]['fcfe']/1000:.2f} billion to ${rows[-1]['fcfe']/1000:.2f} billion.")
    print("Medical claims payable is modeled from benefit expense, with its change in operating cash flow.")
    print(f"Cash flows after 2030 contribute {v['terminal_share']:.2%} of value. "
          "This historical-base model does not establish a current share-price target.")
    for r in rows:
        r["assets"], r["liabilities"], r["balance_gap"] = totals(r)
        r["le"] = r["liabilities"]+r["equity"]+r["nci"]
        r["cash_headroom"] = r["cash"]-a["minimum_cash"]
        r["cash_gap"] = r["cash"]-r["opening_cash"]-r["cfo"]-r["cfi"]-r["cff"]
    table("## Income statement", rows, [(label,key,sign) for label,key,sign in [
        ("Operating revenue","revenue",1),("Benefit expense","benefits",-1),
        ("Product costs","products",-1),("Blended gross profit","gross_profit",1),
        ("Cash operating expense","cash_opex",-1),("PP&E depreciation and amortization","ppe_da",-1),
        ("Other intangible amortization","amort",-1),("Operating income after D&A","operating_income",1),
        ("Normalized investment income","investment_income",1),("Interest","interest",-1),
        ("Pretax income","pretax",1),("Tax expense","tax",-1),("Net income to common","net_income",1)]])
    table("## Balance sheet", rows, [(label,key,1) for label,key in [
        ("Cash","cash"),("Receivables","receivables"),("PP&E","ppe"),("Investments","investments"),
        ("Intangibles","intangibles"),("Other assets","other_assets"),("TOTAL ASSETS","assets"),
        ("Medical claims payable","claims"),("Debt","debt"),("Revolver","revolver"),
        ("Other liabilities","other_liabilities"),("TOTAL LIABILITIES","liabilities"),
        ("Common equity","equity"),("Noncontrolling interests","nci"),("LIABILITIES + EQUITY","le")]])
    table("## Cash flow statement", rows, [
        ("Net income","net_income",1),("PP&E D&A","ppe_da",1),("Intangible amortization","amort",1),
        ("Increase in receivables","receivables_change",-1),("Increase in other working capital","other_wc_change",-1),
        ("Increase in medical claims payable","claims_change",1),("CASH FROM OPERATIONS","cfo",1),
        ("Capex / CASH FROM INVESTING","cfi",1),("Net debt repayment","repayment",-1),
        ("FCFE before distributions and revolver","fcfe",1),("Buybacks","buyback",-1),
        ("Dividends","dividend",-1),("Revolver draw / (repayment)","revolver_change",1),
        ("CASH FROM FINANCING","cff",1),("CHANGE IN CASH","cash_change",1),
        ("Opening cash","opening_cash",1),("Closing cash","cash",1)])
    table("## Checks", rows, [("Assets - liabilities - equity","balance_gap",1),
        ("Cash-flow reconciliation gap","cash_gap",1),("Cash above floor","cash_headroom",1),
        ("Revolver drawn","revolver",1)])
    print("\nPASS: every year balances, cash reconciles, cash meets the floor, and borrowing is within capacity.")
    for r in rows:
        if r["fcfe"] < 0:
            print(f"FY{r['year']}: negative FCFE; omitted from PV under lab convention, overstating economic value.")
        if r["revolver_change"] > TOL:
            print(f"FY{r['year']}: revolver draw funds cash shortfall after reinvestment and distributions.")
    v = value(rows, a)
    print("\n## Equity valuation\n")
    for label, key in (("PV of 2026-2030 FCFE", "pv_flows"),
                       ("Normalized 2031 FCFE", "terminal_fcfe"),
                       ("Terminal value at 2030 year-end", "terminal"),
                       ("PV of terminal value", "pv_terminal"),
                       ("Common-equity value", "equity")):
        print(f"- {label}: {v[key]:,.2f}")
    print(f"- Cost of equity: {a['ke']:.2%}; terminal growth: {a['terminal_growth']:.2%}")
    print(f"- Post-2030 contribution: {v['terminal_share']:.2%}")
    print(f"- Opening common shares: {a['shares']:.6f} million")
    print(f"- Value per opening share: ${v['per_share']:.2f}")
    print(f"\nMarket snapshot: ${MARKET_PRICE:.2f}, {MARKET_DATE}. Source: {MARKET_SOURCE}")
    print(f"Market price times the SAME opening share count: {MARKET_PRICE*a['shares']:,.2f} million.")
    print("This is a common-denominator comparison, not today's actual market cap or a same-date DCF.")
    print("Question: what different growth, margins, risk or capital needs explain the gap?")


def self_test():
    rows = project()
    check(rows, ASSUMPTIONS)
    print("PASS: all five ELV statements balance and cash reconciles.")
    broken = deepcopy(rows)
    broken[0]["cash"] = OPENING["cash"]
    try:
        value(broken)
    except ValueError as e:
        if "FY2026" not in str(e) or "-503.5" not in str(e):
            raise
        print(f"PASS: valuation refuses broken cash: {e}")
    else:
        raise AssertionError("Broken statements accepted")
    stressed = dict(ASSUMPTIONS, buyback=3300.)
    funding = project(stressed)
    assert funding[0]["revolver_change"] > 0
    assert any(r["revolver_change"] < 0 for r in funding[1:])
    print("PASS: a temporary shortfall draws the revolver and later surplus repays it.")
    try:
        project(dict(ASSUMPTIONS, buyback=12000.))
    except ValueError as e:
        if "cash below floor" not in str(e):
            raise
        print(f"PASS: insufficient funding refused: {e}")
    else:
        raise AssertionError("Insufficient funding accepted")
    try:
        value(rows, dict(ASSUMPTIONS, terminal_growth=.10))
    except ValueError:
        print("PASS: growth equal to discount rate refused.")
    else:
        raise AssertionError("Invalid terminal growth accepted")


def sensitivity():
    rows = project()
    print("| Cost of equity / terminal growth | 2.0% | 2.5% | 3.0% |")
    print("|---|---:|---:|---:|")
    for ke in (.09,.10,.11):
        prices = [value(rows, dict(ASSUMPTIONS, ke=ke, terminal_growth=g))["per_share"] for g in (.02,.025,.03)]
        print(f"| {ke:.0%} | " + " | ".join(f"${x:.2f}" for x in prices)+" |")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--break-cash", action="store_true")
    mode.add_argument("--sensitivity", action="store_true")
    args = parser.parse_args()
    if args.check:
        self_test()
    elif args.sensitivity:
        sensitivity()
    else:
        rows = project()
        if args.break_cash:
            rows[0]["cash"] = OPENING["cash"]
        show(rows)


if __name__ == "__main__":
    main()
