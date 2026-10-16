"""Lab 13: check the supplied Meridian allocations, without optimizing.

Run: python3 mandate.py
Weights use percentage points (60 means 60%), not fractions.
"""

# Editable inputs: reserve amounts are USD millions.
HOLDINGS = {
    "Cash": {"issuer": "none", "days": 0, "reserve_eligible": True},
    "Treasury bills": {"issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    "Treasury 10-year note": {"issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    "Global equity index fund": {"issuer": "diversified fund", "days": 2, "reserve_eligible": False},
    "Investment-grade bond fund": {"issuer": "diversified fund", "days": 3, "reserve_eligible": False},
    "Private real estate fund": {"issuer": "diversified fund", "days": 90, "reserve_eligible": False},
    "Acme Corp bonds": {"issuer": "Acme Corp", "days": 4, "reserve_eligible": False},
    "Acme Corp stock": {"issuer": "Acme Corp", "days": 1, "reserve_eligible": False},
}
CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    "D": {
        "Cash": 100, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 0, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}
RESERVE_SIZE = 100
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5
MINIMUM_LIQUID_SHARE = 90
ISSUER_LIMIT = 8
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}

from math import isclose, isfinite


def reserve_minimum():
    return QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100


def check_candidate(weights):
    """Return (rule, measured percent, passed) for each checkable rule."""
    if set(weights) != set(HOLDINGS):
        raise ValueError("List every holding exactly once; use zero for unused holdings.")
    if not all(isfinite(weight) for weight in weights.values()):
        raise ValueError("Every weight must be a finite number.")

    total = sum(weights.values())
    lowest = min(weights.values())
    reserve = 0.0
    liquid = 0.0
    company_weights = {}
    for holding, weight in weights.items():
        details = HOLDINGS[holding]
        if details["reserve_eligible"]:
            reserve += weight
        if details["days"] <= LIQUIDITY_WINDOW:
            liquid += weight
        issuer = details["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            company_weights[issuer] = company_weights.get(issuer, 0.0) + weight
    largest_company = max(company_weights.values(), default=0.0)

    # A tiny tolerance handles floating-point addition for the sum check.
    # Compare unrounded measurements; round only for printed output.
    return [
        ("Weights sum to 100", total, isclose(total, 100, rel_tol=0, abs_tol=1e-9)),
        ("Long-only (lowest weight)", lowest, lowest >= 0),
        (f"Reserve >= {reserve_minimum():.1f}%", reserve, reserve >= reserve_minimum()),
        (f"Redeemable in {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE:.1f}%",
         liquid, liquid >= MINIMUM_LIQUID_SHARE),
        (f"Largest single company <= {ISSUER_LIMIT:.1f}%",
         largest_company, largest_company <= ISSUER_LIMIT),
    ]


def print_candidate(name, weights):
    print(f"\nCandidate {name}")
    failures = 0
    for rule, value, passed in check_candidate(weights):
        print(f"  {rule}: {value:.1f}% {'pass' if passed else 'FAIL'}")
        failures += not passed
    print("  Calendar-year loss: requires CIO clarification")
    verdict = "passes every checkable rule" if failures == 0 else f"fails {failures} rule(s)"
    print(f"  Verdict: {verdict}")


def main():
    print(f"Reserve minimum: {reserve_minimum():.1f}%")
    for name, weights in CANDIDATES.items():
        print_candidate(name, weights)


if __name__ == "__main__":
    main()
