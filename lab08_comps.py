"""Lab 08 ELV comparison, adapted from lab07_comps.py.
Run: python3 lab08_comps.py. Standard library only; no network calls.
Sources, dates, policy decisions and DCF comparison: lab-08-elv.md.
"""

import math
from statistics import median

# EDITABLE INPUTS: USD per NYSE common share; FY2025 total GAAP diluted EPS.
# Close column (not dividend-adjusted close), September 10, 2026.
# FY2025 is the latest completed annual period public by the valuation date.
VALUATION_DATE = "2026-09-10"
TARGET = {
    "ticker": "ELV", "name": "Elevance Health", "price": 416.54, "eps": 25.21,
    "fiscal_year_end": "2025-12-31", "earnings_publication": "2026-01-28",
    "price_source": "https://stockanalysis.com/stocks/elv/history/",
    "earnings_source": "https://www.elevancehealth.com/newsroom/elv-quarterly-earnings-q4-2025",
}
PEERS = [
    {
        "ticker": "UNH", "name": "UnitedHealth Group", "price": 388.28,
        "eps": 13.23, "policy": "QUALIFY",
        "fiscal_year_end": "2025-12-31", "earnings_publication": "2026-01-27",
        "price_source": "https://stockanalysis.com/stocks/unh/history/",
        "earnings_source": "https://www.unitedhealthgroup.com/newsroom/2026/2026-01-27-uhg-reports-2025-results-and-issues-2026-outlook.html",
    },
    {
        "ticker": "CI", "name": "The Cigna Group", "price": 280.91,
        "eps": 22.18, "policy": "QUALIFY",
        "fiscal_year_end": "2025-12-31", "earnings_publication": "2026-02-05",
        "price_source": "https://stockanalysis.com/stocks/ci/history/",
        "earnings_source": "https://newsroom.thecignagroup.com/2026-02-05-The-Cigna-Group-Reports-Strong-Fourth-Quarter-and-Full-Year-2025-Results,-Establishes-2026-Outlook-and-Increases-Dividend",
    },
]
# QUALIFY admits a peer with the limitations documented in the Markdown.
# Set missing numerical inputs to None. USE and QUALIFY enter the calculation;
# EXCLUDE does not. First normalized ticker wins. The target is never a peer.
# Dates and earnings definitions must be source-checked when editing inputs.
# Never substitute adjusted EPS, quarterly EPS, or future annual results.


def positive_number(value):
    """Accept finite positive numeric inputs; reject missing values and booleans."""
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) and number > 0 else None


def ticker(row):
    return str(row.get("ticker") or "").strip().upper()


def pe_ratio(row):
    price, eps = positive_number(row.get("price")), positive_number(row.get("eps"))
    if price is None or eps is None:
        return None
    return positive_number(price / eps)


def implied_price(multiple, eps):
    if multiple is None or eps is None:
        return None
    return positive_number(multiple * eps)


def analyze(target, peers):
    """Calculate with unrounded floats; formatting occurs only when printing."""
    target_ticker = ticker(target)
    if not target_ticker:
        raise ValueError("Target ticker is required to exclude it from peers.")
    valid, notes, seen = [], [], set()
    for row in peers:
        symbol = ticker(row)
        if not symbol:
            notes.append("Missing peer ticker: excluded; cannot identify/deduplicate peer.")
            continue
        if symbol == target_ticker:
            notes.append(f"{symbol}: excluded because it is the target.")
            continue
        if symbol in seen:
            notes.append(f"{symbol}: duplicate skipped; first row retained.")
            continue
        seen.add(symbol)
        policy = str(row.get("policy", "USE")).strip().upper()
        if policy not in {"USE", "QUALIFY"}:
            notes.append(f"{symbol}: excluded by policy ({policy or 'missing'}).")
            continue
        multiple = pe_ratio(row)
        if multiple is None:
            notes.append(f"{symbol}: P/E not meaningful; price/EPS must be finite and positive "
                         "and yield a finite positive ratio. Excluded from calculations.")
            continue
        valid.append({"ticker": symbol, "policy": policy, "pe": multiple})

    eps = positive_number(target.get("eps"))
    multiples = [row["pe"] for row in valid]
    middle = median(multiples) if multiples else None
    full_price = implied_price(middle, eps)
    leave_out = []
    for index, row in enumerate(valid):
        remaining = multiples[:index] + multiples[index + 1:]
        remaining_median = median(remaining) if remaining else None
        price = implied_price(remaining_median, eps)
        leave_out.append({
            "removed": row["ticker"], "count": len(remaining), "pe": remaining_median,
            "price": price,
            "change": price - full_price if price is not None and full_price is not None else None,
        })
    return {
        "target_pe": pe_ratio(target), "target_eps": eps, "peers": valid, "notes": notes,
        "minimum": min(multiples) if multiples else None, "median": middle,
        "maximum": max(multiples) if multiples else None, "median_price": full_price,
        "low_price": implied_price(min(multiples), eps) if multiples else None,
        "high_price": implied_price(max(multiples), eps) if multiples else None,
        "leave_out": leave_out,
    }


def multiple_text(value):
    return "not meaningful" if value is None else f"{value:.6f}x"


def price_text(value):
    return "not meaningful" if value is None else f"${value:.2f}"


def report(target, result):
    print("LAB 08 — ELEVANCE HEALTH P/E COMPARISON")
    print(f"Valuation date: {VALUATION_DATE}; regular-session closing prices, USD/share.")
    print("FY2025 total GAAP diluted EPS; all annual releases public before valuation date.")
    print("Sources and policy qualifications: lab-08-elv.md")
    print(f"Target price: {price_text(target.get('price'))}; EPS: {price_text(target.get('eps'))}")
    print(f"Target: {target.get('name', ticker(target))} ({ticker(target)})")
    print(f"Target observed P/E: {multiple_text(result['target_pe'])}")
    if result["target_pe"] is None:
        print("Target observed P/E requires finite positive price and EPS.")
    if result["target_eps"] is None:
        print("Target implied prices and dollar changes: not meaningful; invalid target EPS.")
    for note in result["notes"]:
        print(note)
    for row in result["peers"]:
        print(f"{row['ticker']} ({row['policy']}) P/E: {multiple_text(row['pe'])}")

    count = len(result["peers"])
    if count == 0:
        print("No usable peers. Peer statistics and implied prices: not meaningful.")
        return
    if count == 1:
        print("1 valid peer: reference estimate, no range.")
        print(f"Reference P/E: {multiple_text(result['median'])}")
        print(f"Target reference estimate: {price_text(result['median_price'])}")
    else:
        print(f"{count} valid peers")
        for label in ["minimum", "median", "maximum"]:
            print(f"Peer {label} P/E: {multiple_text(result[label])}")
        print(f"Target implied minimum: {price_text(result['low_price'])}")
        print(f"Target implied median: {price_text(result['median_price'])}")
        print(f"Target implied maximum: {price_text(result['high_price'])}")

    print("\nLEAVE ONE VALID PEER OUT")
    for row in result["leave_out"]:
        if row["count"] == 0:
            print(f"Remove {row['removed']}: no estimate; no peers remain.")
            continue
        status = "reference estimate, no range" if row["count"] == 1 else "median estimate"
        change = "not meaningful" if row["change"] is None else f"{row['change']:+.2f} USD/share"
        print(f"Remove {row['removed']}: {row['count']} remaining; {status}; "
              f"median P/E {multiple_text(row['pe'])}; "
              f"target price {price_text(row['price'])}; change {change}")
    print("\nImplied price = peer P/E x target diluted EPS. No cash/debt adjustment.")
    print("Display rounding is never used in subsequent calculations.")


if __name__ == "__main__":
    report(TARGET, analyze(TARGET, PEERS))
