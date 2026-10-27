"""Lab 16: a point-in-time provenance gate. Standard library only."""

# Editable inputs: row number, ticker, month measured, published on, price.
DECISION_DATE = "2026-03-31"
TABLE = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]

from collections import namedtuple
from datetime import date

Row = namedtuple("Row", "number ticker month published price")


def clean_rows(table):
    """Rules 1 and 2; preserve row IDs, exclude the ID from duplicate identity."""
    rows = [Row(n, t, m, date.fromisoformat(p), v) for n, t, m, p, v in table]
    quarantined = [r for r in rows if not r.ticker.strip()]
    identified = [r for r in rows if r.ticker.strip()]
    seen, unique, duplicates = set(), [], []
    for row in identified:
        key = (row.ticker, row.month, row.published, row.price)
        if key in seen:
            duplicates.append(row)
        else:
            seen.add(key)
            unique.append(row)
    return unique, [("1. Quarantined: no ticker", quarantined),
                    ("2. Removed: exact duplicate", duplicates)]


def latest_vintages(rows):
    """Rule 4: choose the latest publication for each ticker/month pair."""
    latest = {}
    for row in rows:
        key = (row.ticker, row.month)
        if key not in latest or row.published > latest[key].published:
            latest[key] = row
        elif row.published == latest[key].published and row.price != latest[key].price:
            raise ValueError(f"Conflicting prices for {key} on {row.published}")
    panel = sorted(latest.values(), key=lambda row: row.number)
    kept_ids = {row.number for row in panel}
    replaced = [row for row in rows if row.number not in kept_ids]
    return panel, replaced


def provenance_gate(table, decision_date):
    unique, funnel = clean_rows(table)
    cutoff = date.fromisoformat(decision_date)
    future = [r for r in unique if r.published > cutoff]
    eligible = [r for r in unique if r.published <= cutoff]
    funnel.append(("3. Removed: published after decision date", future))
    panel, replaced = latest_vintages(eligible)
    funnel.append(("4. Removed: older vintage replaced", replaced))
    return panel, funnel


def naive_panel(table):
    # Keep identity/duplicate cleanup, but ignore the publication-date cutoff.
    unique, _ = clean_rows(table)
    panel, _ = latest_vintages(unique)
    return panel


def signals(panel):
    """Return {ticker: (latest month, percent change or None)}."""
    result = {}
    for ticker in sorted({r.ticker for r in panel}):
        rows = sorted((r for r in panel if r.ticker == ticker), key=lambda r: r.month)
        current = rows[-1]
        year, month = map(int, current.month.split("-"))
        previous_month = f"{year - 1}-12" if month == 1 else f"{year}-{month - 1:02d}"
        previous = next((r for r in rows if r.month == previous_month), None)
        change = None
        if previous is not None and previous.price != 0:
            change = (current.price / previous.price - 1) * 100
        result[ticker] = (current.month, change)
    return result


def describe_signal(value):
    if value is None:
        return "N/A (no knowable month)"
    month, change = value
    month_name = date.fromisoformat(month + "-01").strftime("%B %Y")
    if change is None:
        return f"N/A ({month_name}; missing previous month or zero base price)"
    return f"{change:+.2f}% ({month_name})"


def main():
    panel, funnel = provenance_gate(TABLE, DECISION_DATE)
    print(f"Decision date: {DECISION_DATE}\nInput rows: {len(TABLE)}\n\nROW FUNNEL")
    remaining = len(TABLE)
    for label, excluded in funnel:
        remaining -= len(excluded)
        numbers = ", ".join(str(r.number) for r in excluded) or "none"
        print(f"{label}: {len(excluded)} row(s); IDs: {numbers}; remaining: {remaining}")
    print("\nAS-OF PANEL")
    print("Row | Ticker | Month measured | Published on | Price")
    for r in panel:
        print(f"{r.number:>3} | {r.ticker} | {r.month} | {r.published} | {r.price:.1f}")
    print(f"Kept row IDs: {', '.join(str(r.number) for r in panel) or 'none'}")
    asof, naive = signals(panel), signals(naive_panel(TABLE))
    print("\nSIGNALS: (latest price / previous calendar month price - 1) * 100")
    for ticker in sorted(naive):
        print(f"{ticker}: as-of {describe_signal(asof.get(ticker))}; "
              f"naive {describe_signal(naive[ticker])}")
    print("\nNaive uses the latest publication per ticker/month, ignoring the cutoff.")
    print("The four rules check provenance; they do not check economic plausibility.")


if __name__ == "__main__":
    main()
