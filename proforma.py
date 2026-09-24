"""Lab 09: ELV three-statement model plus the required ABG benchmark.
Standard library only. USD millions, shares in millions, except $/share.
Run: python3 proforma.py [--company ELV|ABG] [--check] [--break-cash]
Sources, assumptions and limitations: lab-09-elv.md.
"""
import argparse
from copy import deepcopy
import math

YEARS = range(2026, 2031)
TOL = 1e-6
# Historical ELV inputs: FY2025 Form 10-K, pp. 71, 72, 74; Note 13.
# https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm
# All forward assumptions below are judgments, not company guidance.
ABG = {
    "name": "ABG", "growth": [0.018] * 5, "margin": [0.1705] * 5,
    "sga_ratio": [0.665, 0.655, 0.645, 0.645, 0.645],
    "dep_ratio": 82.4 / 3070.4, "amort": 0., "impairment": 120.,
    "capex": 250., "tax": 0.255, "inventory_days": 2135.8 / (17999 - 3071.7) * 365,
    "floor_ratio": 2027 / 2135.8, "receivable_ratio": 0., "claims_ratio": 0.,
    "other_wc_ratio": 0.008, "investment_income": 0., "floor_rate": 0.0467,
    "debt_rate": 0.0544, "revolver_rate": 0.06, "repayment": 150.,
    "buyback": 150., "dividend": 0., "minimum_cash": 25., "revolver_limit": 850.,
    "ke": 0.10, "terminal_growth": 0.025, "shares": 17.951349,
    "opening": dict(revenue=17999., cash=40.4, inventory=2135.8, receivables=0.,
                    ppe=3070.4, investments=0., intangibles=0., other_assets=6371.6,
                    floor=2027., claims=0., debt=3572., revolver=0.,
                    other_liabilities=2127.5, equity=3891.7, nci=0.),
}
ELV = {
    "name": "ELV", "growth": [0.03] * 5,
    # Blended operating revenue less benefits and product costs, NOT a medical loss ratio.
    "margin": [0.143, 0.145, 0.147, 0.148, 0.148],
    "sga_ratio": [0.712, 0.708, 0.704, 0.700, 0.700],
    # PP&E-related D&A proxy; acquired-intangible amortization is separate.
    "dep_ratio": (1546 - 628) / 4679, "amort": 628., "impairment": 0.,
    "capex": 1116., "tax": 0.24, "inventory_days": 0., "floor_ratio": 0.,
    "receivable_ratio": (10073 + 5162 + 6307) / 197584,
    # Claims scale with combined benefits/product costs: a simplified fixed-mix driver.
    "claims_ratio": 17084 / (148223 + 21178),
    "other_wc_ratio": 5344 / 197584,
    # Normalize out equity-method earnings; assume remaining investment income is cash.
    "investment_income": 2194 - 398, "floor_rate": 0.,
    "debt_rate": 1402 / (150 + 1099 + 30797), "revolver_rate": 0.06,
    "repayment": 1000., "buyback": 2605., "dividend": 1529.,
    "minimum_cash": 9491., "revolver_limit": 5000.,
    "ke": 0.10, "terminal_growth": 0.025, "shares": 220.723898,
    "opening": dict(revenue=197584., cash=9491., inventory=0., receivables=21542.,
                    ppe=4679., investments=25884.+740.+1121.+10839., intangibles=11200.,
                    other_assets=28344.+5344.+2310., floor=0., claims=17084.,
                    debt=150.+1099.+30797., revolver=0., other_liabilities=28338.,
                    equity=43882., nci=144.),
}


def totals(row):
    assets = sum(row[k] for k in ("cash", "inventory", "receivables", "ppe",
                                  "investments", "intangibles", "other_assets"))
    liabilities = sum(row[k] for k in ("floor", "claims", "debt", "revolver",
                                       "other_liabilities"))
    return assets, liabilities, assets - liabilities - row["equity"] - row["nci"]


def assert_balanced(rows, assumptions):
    """Recalculate from components: never trust a stored balance-sheet total."""
    for row in rows:
        year = row.get("year", "FY2025A")
        if any(not math.isfinite(v) for v in row.values() if isinstance(v, (int, float))):
            raise ValueError(f"{year}: non-finite model output")
        gap = totals(row)[2]
        if abs(gap) > TOL:
            raise ValueError(f"{year}: assets - liabilities - equity gap = {gap:.1f}")
        cash_gap = row["cash"] - assumptions["minimum_cash"]
        if cash_gap < -TOL:
            raise ValueError(f"{year}: cash below minimum; gap = {cash_gap:.1f}")
        if not -TOL <= row["revolver"] <= assumptions["revolver_limit"] + TOL:
            raise ValueError(f"{year}: revolver outside limit; gap = "
                             f"{row['revolver'] - assumptions['revolver_limit']:.1f}")
        if min(row[k] for k in ("debt", "ppe", "intangibles", "other_assets")) < -TOL:
            raise ValueError(f"{year}: negative debt or modeled long-lived asset")
        if "cash_change" in row:
            cash_gap = row["cash"] - row["opening_cash"] - row["cash_change"]
            if abs(cash_gap) > TOL:
                raise ValueError(f"{year}: cash-flow reconciliation gap = {cash_gap:.1f}")


def project(a):
    previous = dict(a["opening"])
    assert_balanced([previous], a)
    rows = []
    for i, year in enumerate(YEARS):
        r = dict(previous)
        r["year"] = f"FY{year}E"
        r["revenue"] = previous["revenue"] * (1 + a["growth"][i])
        r["gross_profit"] = r["revenue"] * a["margin"][i]
        r["direct_costs"] = r["revenue"] - r["gross_profit"]
        r["sga"] = r["gross_profit"] * a["sga_ratio"][i]
        r["depreciation"] = previous["ppe"] * a["dep_ratio"]
        r["amortization"] = a["amort"]
        r["impairment"] = a["impairment"]
        r["operating_income"] = (r["gross_profit"] - r["sga"] - r["depreciation"]
                                 - r["amortization"] - r["impairment"])
        r["investment_income"] = a["investment_income"]
        r["interest"] = (previous["floor"] * a["floor_rate"]
                         + previous["debt"] * a["debt_rate"]
                         + previous["revolver"] * a["revolver_rate"])
        r["pretax"] = r["operating_income"] + r["investment_income"] - r["interest"]
        r["tax"] = max(0., r["pretax"]) * a["tax"]
        r["net_income"] = r["pretax"] - r["tax"]
        r["inventory"] = r["direct_costs"] * a["inventory_days"] / 365
        r["floor"] = r["inventory"] * a["floor_ratio"]
        r["receivables"] = r["revenue"] * a["receivable_ratio"]
        r["claims"] = r["direct_costs"] * a["claims_ratio"]
        r["capex"] = a["capex"]
        r["ppe"] = previous["ppe"] + r["capex"] - r["depreciation"]
        r["intangibles"] = previous["intangibles"] - r["amortization"]
        r["other_wc_change"] = a["other_wc_ratio"] * (r["revenue"] - previous["revenue"])
        r["other_assets"] = previous["other_assets"] + r["other_wc_change"] - r["impairment"]
        r["repayment"] = min(a["repayment"], previous["debt"])
        r["debt"] = previous["debt"] - r["repayment"]
        r["buyback"], r["dividend"] = a["buyback"], a["dividend"]
        r["equity"] = previous["equity"] + r["net_income"] - r["buyback"] - r["dividend"]
        # Investments, other liabilities and NCI remain flat; future NCI earnings = 0.
        for key in ("inventory", "receivables", "floor", "claims"):
            r[key + "_change"] = r[key] - previous[key]
        r["cfo"] = (r["net_income"] + r["depreciation"] + r["amortization"]
                    + r["impairment"] - r["inventory_change"] - r["receivables_change"]
                    - r["other_wc_change"] + r["claims_change"])
        r["cfi"] = -r["capex"]
        # Lab convention: floor-plan financing inside FCFE; revolver plug excluded.
        r["fcfe"] = r["cfo"] + r["cfi"] + r["floor_change"] - r["repayment"]
        r["opening_cash"] = previous["cash"]
        cash_before_revolver = previous["cash"] + r["fcfe"] - r["buyback"] - r["dividend"]
        if cash_before_revolver < a["minimum_cash"]:
            r["revolver_change"] = min(a["minimum_cash"] - cash_before_revolver,
                                        a["revolver_limit"] - previous["revolver"])
        else:
            r["revolver_change"] = -min(cash_before_revolver - a["minimum_cash"],
                                         previous["revolver"])
        r["revolver"] = previous["revolver"] + r["revolver_change"]
        r["cff"] = (r["floor_change"] - r["repayment"] - r["buyback"]
                    - r["dividend"] + r["revolver_change"])
        r["cash_change"] = r["cfo"] + r["cfi"] + r["cff"]
        r["cash"] = previous["cash"] + r["cash_change"]
        assert_balanced([r], a)
        rows.append(r)
        previous = r
    return rows


def valuation(rows, a):
    assert_balanced(rows, a)  # Refuse broken statements BEFORE computing any valuation.
    ke, g = a["ke"], a["terminal_growth"]
    if not (-1 < g < ke) or a["shares"] <= 0:
        raise ValueError("Require -100% < terminal growth < cost of equity and positive shares")
    pv_flows = sum(r["fcfe"] / (1 + ke) ** t for t, r in enumerate(rows, 1))
    terminal_fcfe = (rows[-1]["fcfe"] + rows[-1]["repayment"]) * (1 + g)
    terminal = terminal_fcfe / (ke - g)
    pv_terminal = terminal / (1 + ke) ** len(rows)
    equity = pv_flows + pv_terminal
    return dict(pv_flows=pv_flows, terminal_fcfe=terminal_fcfe, terminal=terminal,
                pv_terminal=pv_terminal, equity=equity,
                terminal_share=pv_terminal / equity, per_share=equity / a["shares"])


def table(title, rows, fields):
    print("\n" + title)
    print(f"{'USD millions':<37}" + "".join(f"{r['year']:>13}" for r in rows))
    for label, key, sign in fields:
        values = [r[key] * sign for r in rows]
        print(f"{label:<37}" + "".join(f"{0. if abs(v) < TOL else v:>13,.1f}" for v in values))


def show(rows, a):
    print(f"LAB 09 — {a['name']} — FY2025-end model origin; five year-end forecasts")
    print("Forecasts are assumptions, not reported results. Units: USD millions.")
    for r in rows:
        r["assets"], r["liabilities"], r["balance_gap"] = totals(r)
        r["liabilities_equity"] = r["liabilities"] + r["equity"] + r["nci"]
        r["cash_headroom"] = r["cash"] - a["minimum_cash"]
    income = [("Operating revenue", "revenue", 1), ("Direct costs", "direct_costs", -1),
              ("Gross profit (model subtotal)", "gross_profit", 1),
              ("SG&A / cash operating expense", "sga", -1),
              ("Depreciation / PP&E D&A proxy", "depreciation", -1),
              ("Intangible amortization", "amortization", -1), ("Impairment", "impairment", -1),
              ("Operating income (after D&A)", "operating_income", 1),
              ("Normalized investment income", "investment_income", 1),
              ("Interest on opening balances", "interest", -1), ("Pretax income", "pretax", 1),
              ("Tax", "tax", -1), ("Net income", "net_income", 1)]
    balance = [(label, key, 1) for label, key in [
        ("Cash", "cash"), ("Inventory", "inventory"), ("Receivables", "receivables"),
        ("PP&E", "ppe"), ("Investments", "investments"), ("Intangibles", "intangibles"),
        ("Other assets", "other_assets"), ("TOTAL ASSETS", "assets"),
        ("Floor-plan loans", "floor"), ("Medical claims payable", "claims"),
        ("Debt", "debt"), ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"),
        ("TOTAL LIABILITIES", "liabilities"), ("Common shareholders' equity", "equity"),
        ("Noncontrolling interests", "nci"), ("TOTAL LIABILITIES + EQUITY", "liabilities_equity")]]
    cash_flow = [("Net income", "net_income", 1), ("Depreciation", "depreciation", 1),
                 ("Amortization", "amortization", 1), ("Impairment", "impairment", 1),
                 ("Increase in inventory", "inventory_change", -1),
                 ("Increase in receivables", "receivables_change", -1),
                 ("Increase in other working capital", "other_wc_change", -1),
                 ("Increase in claims payable", "claims_change", 1),
                 ("CASH FROM OPERATIONS", "cfo", 1), ("Capex / CASH FROM INVESTING", "cfi", 1),
                 ("Increase in floor-plan loans", "floor_change", 1),
                 ("Debt repayment", "repayment", -1), ("FCFE (before distributions/plug)", "fcfe", 1),
                 ("Buybacks", "buyback", -1), ("Dividends", "dividend", -1),
                 ("Revolver draw / (repayment)", "revolver_change", 1),
                 ("CASH FROM FINANCING", "cff", 1), ("CHANGE IN CASH", "cash_change", 1),
                 ("Opening cash", "opening_cash", 1), ("Closing cash", "cash", 1)]
    if a["name"] == "ELV":
        hidden = {"inventory", "floor", "inventory_change", "floor_change"}
        balance = [x for x in balance if x[1] not in hidden]
        cash_flow = [x for x in cash_flow if x[1] not in hidden]
    table("INCOME STATEMENT", rows, income)
    table("BALANCE SHEET", rows, balance)
    table("CASH FLOW STATEMENT", rows, cash_flow)
    table("CHECKS", rows, [("Assets - liabilities - equity", "balance_gap", 1),
                            ("Cash above minimum", "cash_headroom", 1)])
    v = valuation(rows, a)
    print("All five years: balance, minimum cash, revolver limit and cash reconciliation PASS.")
    print(f"\nEQUITY VALUATION: cost of equity {a['ke']:.2%}; terminal growth {a['terminal_growth']:.2%}")
    print(f"PV of 2026-2030 FCFE: {v['pv_flows']:,.2f}")
    print(f"2031 normalized FCFE: {v['terminal_fcfe']:,.2f}")
    print(f"Terminal value at FY2030 end: {v['terminal']:,.2f}")
    print(f"PV of terminal value: {v['pv_terminal']:,.2f}")
    print(f"Equity value: {v['equity']:,.2f}")
    print(f"Share of value after 2030: {v['terminal_share']:.2%}")
    print(f"Opening shares (millions): {a['shares']:.6f}")
    print(f"Value per share: ${v['per_share']:.2f}")
    print("FCFE is discounted directly: no second cash addition or debt subtraction.")


def self_test():
    rows = project(ABG)
    expected = {"revenue": (18323.0, 19678.3), "operating_income": (844.2, 971.4),
                "net_income": (413.6, 527.5), "fcfe": (211.4, 342.3), "cash": (101.8, 719.8)}
    for key, answers in expected.items():
        actual = tuple(round(r[key], 1) for r in (rows[0], rows[-1]))
        if actual != answers:
            raise AssertionError(f"ABG {key}: {actual} != {answers}")
    if round(valuation(rows, ABG)["per_share"], 2) != 291.75:
        raise AssertionError("ABG known price did not match $291.75")
    print("PASS: all ten ABG endpoint values and $291.75/share match the handout.")
    broken = deepcopy(rows)
    broken[0]["cash"] = ABG["opening"]["cash"]
    try:
        valuation(broken, ABG)
    except ValueError as error:
        if "FY2026E" not in str(error) or "-61.4" not in str(error):
            raise
        print(f"PASS: broken-cash valuation refused: {error}")
    else:
        raise AssertionError("Broken statements were valued")
    assert_balanced(project(ELV), ELV)
    print("PASS: ELV statements balance and cash reconciles in every year.")
    stressed = deepcopy(ABG)
    stressed["buyback"] = 230.
    stress_rows = project(stressed)
    if not (stress_rows[0]["revolver_change"] > 0 and
            any(r["revolver_change"] < 0 for r in stress_rows[1:])):
        raise AssertionError("Revolver draw/repayment paths were not exercised")
    print("PASS: temporary cash shortfall draws revolver; later surplus repays it first.")
    stressed["buyback"] = 2000.
    try:
        project(stressed)
    except ValueError as error:
        if "cash below minimum" not in str(error):
            raise
        print(f"PASS: inadequate financing refused: {error}")
    else:
        raise AssertionError("Revolver-limit breach was accepted")
    invalid = dict(ABG, terminal_growth=ABG["ke"])
    try:
        valuation(rows, invalid)
    except ValueError:
        print("PASS: terminal growth equal to cost of equity refused.")
    else:
        raise AssertionError("Invalid terminal growth was accepted")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--company", choices=["ELV", "ABG"], default="ELV")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--break-cash", action="store_true",
                        help="Deliberately substitute opening cash in FY2026; expect refusal")
    args = parser.parse_args()
    if args.check:
        self_test()
        return
    a = ELV if args.company == "ELV" else ABG
    rows = project(a)
    if args.break_cash:
        rows[0]["cash"] = a["opening"]["cash"]
    show(rows, a)


if __name__ == "__main__":
    main()
