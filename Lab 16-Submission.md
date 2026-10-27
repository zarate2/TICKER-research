# Lab 16 — Provenance Gate

**Prepared:** October 27, 2026.  
**Decision date:** March 31, 2026.  
**Training case:** The assignment's fictional AAA, BBB and CCC one-year zero-coupon bond funds.  
**Preparation:** Built and verified with AI assistance. A simulated partner exercise summary appears at the end.

## D — What was knowable on the decision date

On March 31, the latest knowable monthly price change was **+1.98% for AAA, −1.02% for BBB and +0.91% for CCC**, all for February. The naive calculation gives **+5.83%, −5.15% and +1.82%**, respectively, because it uses publications that arrived in April. The filter reproduces every supplied known answer, retains the original row numbers, and demonstrates why a historical decision must use only information available at that time.

### Connection to Lab 15

[Lab 15](../Lab%2015/Lab%2015-Submission.md) tested whether Oak Grove's portfolio choice survived changes in return estimates and estimation windows. Its all-months allocation was 75% BIL / 25% VT, versus 90% BIL / 10% VT using the last 36 months. Lab 16 adds a prior question: were the inputs available when the decision would have been made?

Lab 15's [source record](../Lab%2015/sources/Prices.json) identifies the monthly adjusted prices as downloaded on October 20, 2026. Its first-of-month dates label monthly bars; they do not establish when the completed monthly prices became knowable. The saved download supports reproducibility of that snapshot, but does not establish which historical versions were available on earlier decision dates. A historical backtest would need publication or availability records and the appropriate vintage for each decision date before estimating returns and selecting weights.

This lab applies the assigned fictional training table to demonstrate that gate. It does not substitute the training funds for Oak Grove's BIL, IEF, LQD and VT universe or claim to reconstruct historical vintages of Lab 15's prices.

## R — Inputs and rules

The complete 12-row input table is editable at the top of [asof.py](asof.py). The original [assignment](sources/Assignment.md) is retained for comparison.

**Month measured** is the period described by a number. **Published on** is the date that version became available. A February number can first appear in March and be revised in April. In the assignment's API example, `date` identifies the measured month, `realtime_start` identifies the version's publication date, and `realtime_end` ends its validity interval. A revision is another record for the same observation month.

The gate applies these rules in order:

1. Quarantine a row with no ticker.
2. Remove an exact duplicate, keeping its first occurrence. Compare ticker, month, publication date and price; the row number is an audit identifier, not part of duplicate identity.
3. Remove a row published after the decision date. A publication on the decision date is eligible.
4. For each ticker and measured month, keep the latest publication among the remaining eligible rows.

Rule 3 must precede rule 4. Otherwise an April revision could displace the version that was actually available in March. Quarantined and removed rows are excluded from the calculation while their row numbers remain in the funnel.

## I — Implementation and reproduction

[asof.py](asof.py) is one standalone Python file using only the standard library. Run from the `Lab 16` folder:

```sh
python3 asof.py
```

`python asof.py` also works when `python` selects Python 3. No package installation is needed.

The file prints the row funnel, remaining panel, and both signals for each ticker. Every result is computed from `TABLE` and `DECISION_DATE`; the program contains no typed-in expected answers. The naive comparison retains ticker and duplicate cleanup, then selects each ticker/month's latest publication without the cutoff.

The signal is `(latest price / previous calendar month's price − 1) × 100`. The latest month is chosen separately for each ticker. If a prior calendar month is missing, the program reports the signal as unavailable instead of treating a multi-month change as a one-month return.

### Rule 4 block for the independent code explanation

The relevant function is `latest_vintages`. Its selection block is:

```python
latest = {}
for row in rows:
    key = (row.ticker, row.month)
    if key not in latest or row.published > latest[key].published:
        latest[key] = row
```

For the required no-AI partner exercise, explain the dictionary, the two-part key, the date comparison and the assignment line. Also trace where `provenance_gate` restricts the rows to eligible publications before calling this function. The function flags conflicting prices with the same publication date instead of silently resolving an ambiguity; no such conflict exists in the assigned table.

## V — Verification against the known answer

### Row funnel

| Step | Number excluded | Original row numbers | Rows remaining |
|---|---:|---|---:|
| Input | — | 1 through 12 | 12 |
| 1 — Quarantined for missing ticker | 1 | 11 | 11 |
| 2 — Exact duplicate removed | 1 | 7 | 10 |
| 3 — Published after March 31 | 3 | 3, 8, 10 | 7 |
| 4 — Older vintage replaced | 1 | 2 | 6 |

### As-of panel

| Row | Ticker | Month measured | Published on | Price |
|---:|---|---|---|---:|
| 1 | AAA | 2026-01 | 2026-02-10 | 101.0 |
| 4 | AAA | 2026-02 | 2026-03-25 | 103.0 |
| 5 | BBB | 2026-01 | 2026-02-10 | 98.0 |
| 6 | BBB | 2026-02 | 2026-03-10 | 97.0 |
| 9 | CCC | 2026-01 | 2026-02-10 | 110.0 |
| 12 | CCC | 2026-02 | 2026-03-10 | 111.0 |

### Signals and arithmetic

| Ticker | As-of calculation | As-of signal and month | Naive calculation | Naive signal and month |
|---|---|---|---|---|
| AAA | `(103 / 101 − 1) × 100` | **+1.98%, February** | `(109 / 103 − 1) × 100` | **+5.83%, March** |
| BBB | `(97 / 98 − 1) × 100` | **−1.02%, February** | `(92 / 97 − 1) × 100` | **−5.15%, March** |
| CCC | `(111 / 110 − 1) × 100` | **+0.91%, February** | `(112 / 110 − 1) × 100` | **+1.82%, February revised** |

AAA's March price of 109 and BBB's March price of 92 were published on April 10. CCC's February revision to 112 was published on April 5. None was available on March 31. Keeping AAA row 2 instead of row 4 would incorrectly give `(104 / 101 − 1) × 100 = +2.97%`.

The two columns do not always cover the same month: AAA and BBB advance from February to March; CCC stays in February but changes vintage. Their differences reveal unavailable information, rather than a same-period revision effect for every ticker.

### Sanity check with the arithmetic shown

Each fictional one-year zero pays 100 at maturity. Its yield in percent is `(100 / price − 1) × 100`.

| Row | Fund | Month | Price | Yield calculation | Yield | What it breaks in this exercise |
|---:|---|---|---:|---|---:|---|
| 1 | AAA | Jan | 101.0 | `(100 / 101 − 1) × 100` | −0.99% | Negative yield |
| 4 | AAA | Feb | 103.0 | `(100 / 103 − 1) × 100` | −2.91% | Negative yield |
| 5 | BBB | Jan | 98.0 | `(100 / 98 − 1) × 100` | +2.04% | Nothing |
| 6 | BBB | Feb | 97.0 | `(100 / 97 − 1) × 100` | +3.09% | Nothing |
| 9 | CCC | Jan | 110.0 | `(100 / 110 − 1) × 100` | −9.09% | Negative yield; priced above BBB and AAA |
| 12 | CCC | Feb | 111.0 | `(100 / 111 − 1) × 100` | −9.91% | Negative yield; priced above BBB and AAA |

Under the training assumptions, the same-maturity price ordering should be AAA > BBB > CCC. Instead, January is CCC 110 > AAA 101 > BBB 98, and February is CCC 111 > AAA 103 > BBB 97. All six rows pass provenance, but four fail the stated economic sanity checks. Availability alone does not establish plausibility.

### Later-date test

The verification script changed `DECISION_DATE` to `2026-04-15` in a temporary copy of `asof.py` and executed that copy. The delivered file retains `2026-03-31`.

| Ticker | April 15 as-of signal | Naive signal | Match |
|---|---|---|---|
| AAA | +5.83%, March | +5.83%, March | Yes |
| BBB | −5.15%, March | −5.15%, March | Yes |
| CCC | +1.82%, February revised | +1.82%, February revised | Yes |

On April 15, rule 3 removes no rows and rule 4 removes rows 2 and 12. The panel contains **1, 3, 4, 5, 6, 8, 9 and 10**. All publications in this particular table are now available, so the two signals match ticker for ticker.

**Verification evidence:** [March 31 output](outputs/AsOf-2026-03-31.txt), [April 15 output](outputs/AsOf-2026-04-15.txt), and [passing checks](outputs/Verification.txt). Six automated tests cover the known funnel and signals, the later date, publication-day inclusion, input-order independence of vintage selection, and unavailable signals. The checker additionally executes the literal date edit and verifies that the delivered file remains unchanged.

Reproduce the checks and saved outputs with:

```sh
python3 support/check_results.py
```

This is an automated verification of my file. It is not a claim that a partner's file was run.

## Learn — Look-ahead bias

**What it is:** Look-ahead bias occurs when a historical decision uses information that became available only after that decision. This gives the backtest access to information the trader did not have.

**How it works:** Event time identifies the month measured. Publication time determines when a value first becomes eligible. A revision changes the value for an already measured month, but is eligible only from its own publication date. Filtering only on the measured month can therefore admit both unpublished observations and future revisions.

**AAA example:** The naive +5.83% uses the March price of 109, published April 10. On March 31, the latest eligible prices were January's 101 and February's revised 103, giving +1.98%. The higher number makes AAA's recent performance look stronger, but it uses a later month's information. It is a historical price-change signal, not a return guaranteed to be earned after the decision.

## Reflect

**1. Which rule removed the row that mattered most?** For AAA's misleading +5.83%, rule 3 is decisive: removing row 3 prevents the use of the March price before its April 10 publication. Rule 4 also matters because it removes row 2 and selects the February revision that was available by March 31. Without that revision rule, even the February signal would be wrong.

**2. What would a backtest built on the naive column claim?** It would treat AAA's +5.83%, BBB's −5.15% and CCC's +1.82% as available signals on March 31, suggesting stronger recent AAA and CCC performance and weaker BBB performance than was knowable. A strategy could then appear to benefit from responding early to April information. The exact effect on portfolio performance cannot be calculated without a trading rule; the bias does not mechanically make every individual signal more positive.

**3. What fifth rule would quarantine rows 1, 4, 9 and 12?** After the provenance gate, quarantine any price above 100 in this training case because `(100 / price − 1)` is negative. This catches exactly those four rows. A companion same-month rating-order check would also flag CCC for being priced above both AAA and BBB. These are the assignment's sanity assumptions, not universal filters for all real bond funds or Lab 15 ETF prices. Keep these flags separate from the four-rule output so the required provenance result remains auditable.

## Partner exercise summary

*Simulated exercise summary drafted with AI; the numerical results are verified, but the partner participation described here is hypothetical.*

The discussion began with the difference between the month a number measures and the date it becomes available. We used AAA to show that a February observation could be published in March and revised later that same month. This helped clarify why filtering by the observation month alone would allow information into a backtest before a trader could have known it.

The code review focused on rule 4. We traced how the dictionary groups rows by ticker and month, compares publication dates, and replaces an older eligible record with a newer one. The main point raised during the review was why the code keeps AAA's February price of 103 instead of 104. The explanation was that the March 25 revision was already available by the March 31 decision date. We also checked that the publication-date filter runs first, so a future revision cannot replace an eligible observation.

For the swap-and-break exercise, we compared the March 31 results with the known answer, then changed the decision date to April 15. The as-of signals became +5.83% for AAA, −5.15% for BBB and +1.82% for CCC, matching the naive column. We then restored March 31 and confirmed the original signals returned. The comparison illustrated that the gap came from publication timing and revisions, rather than a different return formula.

The final discussion connected the result to Lab 15: changing estimates can move an allocation, but using information unavailable on the decision date can undermine the backtest before optimization even begins. We also reviewed the negative yields and CCC's price ranking. The shared conclusion was that a provenance gate establishes whether information was available, while a separate sanity check is needed to flag questionable values.

## GitHub checkout

The calculations, written responses and automated date-change test are complete. The summary above is a simulation, not evidence of a completed partner session. The individual AI code quiz also remains unrecorded.

For GitHub checkout, upload this folder and submit links to **this Markdown document** and **[asof.py](asof.py)**. Include `outputs/`, `support/` and `sources/` as reproducibility evidence. Exclude `__pycache__/`. No repository destination is configured in this workspace, so no GitHub upload or course submission is claimed.
