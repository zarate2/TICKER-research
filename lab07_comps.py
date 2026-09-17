"""Lab 07 frozen P/E case. Run: python3 lab07_comps.py. Standard library only."""

import math
from statistics import median

# EDITABLE INPUTS: USD/share; FY2024 total GAAP diluted EPS.
# Prices are 2024-12-31 closes, paired retrospectively with annual earnings.
# This required training case is separate from the prior ELV DCF.
TARGET = {"ticker": "ABG", "name": "Asbury Automotive", "price": 243.03, "eps": 21.50}
PEERS = [
    {"ticker": "AN", "name": "AutoNation", "price": 169.84, "eps": 16.92,
     "policy": "USE"},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "eps": 36.81,
     "policy": "QUALIFY"},
]
# USE and QUALIFY enter calculations when their numerical inputs are valid.
# EXCLUDE does not. Deduplication uses trimmed uppercase tickers; first row wins.
# Set missing numerical inputs to None. Never add cash or subtract debt here.


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
    print("LAB 07 — P/E COMPARABLE-COMPANY VALUATION")
    print("Frozen 2024-12-31 prices / FY2024 total GAAP diluted EPS; retrospective training case.")
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
