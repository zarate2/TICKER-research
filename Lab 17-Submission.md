# Lab 17 — Point-in-Time Audit

**Prepared and downloaded:** October 29, 2026.  
**Project 2:** Oak Grove Scholarship Reserve; BIL, IEF, LQD and VT.  
**Additional series:** CPIAUCSL, selected here because Oak Grove's mandate targets CPI + 3%; no earlier prework series selection was found.  
**Preparation:** AI-assisted implementation, research and verification. Peer discussions below are explicitly simulated, not records of actual participation.

## D — Was the number knowable, and may Project 2 use it?

**Quarantine today's CPIAUCSL history as an input to historical trading decisions.** On September 30, 2026, the latest available CPI observation was August, **334.131**. Today's file also contains September, **336.298**, which was not available at the September month-end. A comparison with the January 15, 2025 vintage additionally identifies **60 revised observations**. Project 2 may admit CPI only after implementing the decision-date vintage and availability rules below.

This continues [Lab 16's provenance gate](../Lab%2016/Lab%2016-Submission.md): the period measured and the publication date are different. It also continues [Lab 15's Oak Grove portfolio](../Lab%2015/Lab%2015-Submission.md). Its 2.5% assumed inflation and 5.5% nominal target remain the prior exercise assumptions; this audit does not silently replace them with realized CPI or rerun the allocation.

**Opener — simulated peer summary:** The discussion focused on the 10-year Treasury yield, DGS10. A rise in market yields tends to lower the prices of existing fixed-rate bonds, making the rate relevant to IEF and to the Treasury-rate component of LQD; corporate credit spreads also affect LQD. The hypothetical partner summarized the link as “higher required yields reduce the value of fixed future payments.” In the swap, the partner proposed FEDFUNDS as a driver of short-term reinvestment yields relevant to BIL, and we distinguished that mechanism from a guaranteed ETF return.

## R and I — Sources and app

[asof_app.py](asof_app.py) uses the assignment's public CSV URLs with no API key:

- Current: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES`
- Historical: `https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=SERIES&vintage_date=YYYY-MM-DD`

The separate `download_current` and `download_vintage` functions cache each series/date request for one hour. A download-day cache key also prevents yesterday's cache from being labeled as today's. The shared reader uses `curl`, installed on this Mac, with certificate verification, HTTP-error handling and a timeout. No shell interpolation or API credentials are used.

The four default rate series are selected at launch; charts begin January 1, 2020 and the as-known date defaults to today. The text box accepts another series such as CPIAUCSL or PAYEMS. Each chart uses current data and states the latest nonmissing measured date available in the selected historical snapshot. Source links and actual UTC download timestamps appear beneath each chart. Unknown IDs show a series-specific error while other series remain usable.

Run from the `Lab 17` folder using the existing Lab 15 environment:

```sh
../Lab\ 15/.venv/bin/python -m streamlit run asof_app.py
```

Standalone installation and verification commands are in [README.md](README.md).

**Counting rules:** A dot is missing, never zero or a forward-filled observation. “Later observations” counts nonmissing current observations after the final nonmissing observation in the vintage. “Revised observations” counts changed values on dates present and nonmissing in both downloads, using an absolute tolerance of 0.000000001. Counts use all downloaded history; the chart's start date does not truncate the audit. An empty historical snapshot remains empty. The app never substitutes today's data for a failed vintage download. Monthly CSV dates such as `2026-09-01` identify September's measured period, not a September 1 publication.

## V — Known answer reproduced

The app and live downloads reproduce all four answers for **October 5, 2026**. Rates are in percent.

| Series | Last measured period known then | Value known then | Last measured period today | Value today | Later observations | Revised observations |
|---|---|---:|---|---:|---:|---:|
| BAA | September 2026 | 6.47 | September 2026 | 6.47 | 0 | 0 |
| FEDFUNDS | September 2026 | 3.75 | September 2026 | 3.75 | 0 | 0 |
| DGS10 | October 2, 2026 | 5.28 | October 27, 2026 | 4.99 | 16 | 0 |
| MORTGAGE30US | October 1, 2026 | 7.28 | October 29, 2026 | 7.24 | 4 | 0 |

**PAYEMS probe, January 15, 2025:** The latest known month is December 2024 at **159,536 thousand jobs**. Today's value for that same December is **158,316 thousand**, lower by **1,220 thousand jobs**. There are **381 revised observations** on common dates and **21 later observations**. Today's latest month is September 2026 at 159,044 thousand, but that is not the same-month revision comparison. These results establish that the two functions did not simply read today's series twice.

**Evidence:** [Results.json](outputs/Results.json), [Known-answer.csv](outputs/Known-answer.csv), [Verification.txt](outputs/Verification.txt), and [download manifest](sources/Downloads.json). The manifest includes each URL, UTC retrieval timestamp, retained CSV filename and SHA-256 hash. The app contains no hard-coded answer values; expected values occur only in the independent verification script and this report.

All **18 checks passed**: live known-answer checks, the payroll probe, three CPI page comparisons, missing/empty-data behavior, and Streamlit widget tests. UI tests replay the actual downloaded CSV payloads to avoid duplicate network requests; their error-path test deliberately supplies an unknown ID. This is automated verification, not a claim of a partner-operated test.

**Live source limitation:** On this run, the October 29 DGS10 ALFRED snapshot extends to October 28 at 5.05, while the current FRED download ends October 27 at 4.99. The retained files document that the two endpoints are not synchronized; the app displays each source as received, rather than forcing today's snapshots to match. This does not change the successful October 5 check. It reinforces why each download needs its own timestamp and why endpoint disagreements must be reviewed before production use.

The running app was also inspected in Chrome on October 29: all four charts, the sidebar, historical-date captions and linked comparison table rendered, and entering CPIAUCSL added a fifth series with September's 336.298 value. See [UI verification record](outputs/UI-verification.md).

## E — CPIAUCSL data card

| Field | Record |
|---|---|
| Series and source | CPIAUCSL; U.S. Bureau of Labor Statistics, distributed through [FRED](https://fred.stlouisfed.org/series/CPIAUCSL) and [ALFRED](https://alfred.stlouisfed.org/series?seid=CPIAUCSL). |
| Measure | All-items consumer price index for urban consumers, U.S. city average. |
| Units and frequency | Monthly; index, 1982–1984 = 100; seasonally adjusted. An index level is not a percent inflation rate. |
| Publication lag | Generally in the following month; consult the actual release calendar instead of assuming a constant lag. September 2026 was scheduled for October 14 at 8:30 a.m. Eastern, 14 calendar days after month-end. |
| Availability evidence | The September 30 vintage ends in August; the October 29 vintage includes September. The FRED page reports an October 14 update. |
| Revisions | Yes. Annual seasonal-factor updates can revise the preceding five years. The short September-to-October comparison has zero revisions; the January 2025 comparison has 60. |
| Missing values and transformations | Preserve missing observations. For annual inflation calculate `100 × (CPI[t] / CPI[t−12] − 1)` using both levels from the same eligible vintage. Do not treat the level 336.298 as 336.298% or automatically substitute historical inflation for an expected-inflation assumption. |
| Download date and retention | October 29, 2026; exact UTC timestamps, URLs and hashes in [Downloads.json](sources/Downloads.json), with raw responses in [sources/csv](sources/csv/). |
| Decision-time rule | Use the prior calendar day's ALFRED snapshot for a trade on day D. This conservative rule excludes same-day releases whose time cannot be established by the date-only download. Missing required vintage or comparison month means no signal. |

Source details: [FRED series metadata](https://fred.stlouisfed.org/series/CPIAUCSL), [BLS October 2026 release calendar](https://www.bls.gov/schedule/2026/10_sched.htm), and [BLS seasonal adjustment policy](https://www.bls.gov/cpi/seasonal-adjustment/). The app's snapshot records what the source provides for a date; it does not expose an intraday availability timestamp for each observation.

**Partner attack — simulated:** “I trust the revisions field least: your one-month audit says zero, so why call CPI revised?”

**Two-sentence response:** Zero is specific to these two snapshots: comparing the January 15, 2025 vintage with today's file produces 60 revised CPI observations, including December 2024 changing from 317.685 to 317.604. BLS explains that annual seasonal-factor updates can revise five years of seasonally adjusted history, so Project 2 must retain historical vintages rather than infer revision safety from one quiet month.

### Last month versus today

| As known on | Latest measured period | Value known then | Later observations in today's file | Revisions on common dates |
|---|---|---:|---:|---:|
| September 30, 2026 | August 2026 | 334.131 | 1 | 0 |
| October 29, 2026 | September 2026 | 336.298 | 0 | 0 |
| January 15, 2025 — additional revision check | December 2024 | 317.685 | 20 | 60 |

September's observation disappears when the cutoff moves back to September 30 because it was not yet published. Comparing the two most recent snapshots demonstrates release lag, while the older snapshot exposes revisions. Evidence: [CPI-audit.csv](outputs/CPI-audit.csv).

### Three values checked against the FRED page

| Measured month | Downloaded current CSV | FRED page | Match |
|---|---:|---:|---|
| July 2026 | 332.813 | 332.813 | Yes |
| August 2026 | 334.131 | 334.131 | Yes |
| September 2026 | 336.298 | 336.298 | Yes |

These were independently read from the [FRED page](https://fred.stlouisfed.org/series/CPIAUCSL) by the AI assistant on October 29 and compared with the downloaded file. They are not a claim that the student performed the required personal check.

## Explain the code — preparation and simulated discussion

The relevant function is `download_vintage` in [asof_app.py](asof_app.py). This explanation is study preparation; the required six-minute, no-AI explanation remains a personal activity.

| Code | Explanation |
|---|---|
| `@st.cache_data(ttl=3600, show_spinner=False)` | Cache successful results for an hour, keyed by the function arguments. |
| `def download_vintage(series_id, as_of, download_day):` | Receive the series, historical knowledge date and retrieval-day cache key. |
| `series_id = validate_id(series_id)` | Normalize the ID and reject invalid characters. |
| `as_of = date.fromisoformat(str(as_of))` | Convert the cutoff to a validated date. |
| `if as_of > download_day:` and the following `raise` | Reject future knowledge dates. |
| `params = {"id": series_id, "vintage_date": as_of.isoformat()}` | Ask for this series as known on this exact date. |
| The `url = ... + urlencode(params)` line | Construct the ALFRED CSV request with encoded parameters. |
| `frame = read_csv_url(url)` | Download once, parse dates/numbers, preserve missing values, validate structure and retain source metadata. |
| `return frame.loc[frame.index <= pd.Timestamp(as_of)].copy()` | Return the historical snapshot, additionally excluding any observation dates beyond the cutoff. This final date filter alone would not remove revisions from a current-data download. |

**Simulated peer question:** “Why not download FRED and keep rows dated before September 30?”  
**Answer from the code:** The critical distinction is `vintage_date` in the ALFRED URL: it requests the version that existed then. A current-data date filter could retain September's first-of-month label before its October release and could keep later revisions to older months.

**Simulated swap summary:** The hypothetical partner explained the cache key and showed how the same series can return different values for different as-known dates. I asked whether changing only the chart start could alter the revision count; the answer was no, because `compare_series` receives the complete current and historical frames before the chart window is applied.

## Your call — quarantine, with an admission condition

**Quarantine CPIAUCSL for Project 2's historical decision engine until the engine uses the eligible ALFRED vintage at every rebalance.** The observed September release lag and the 60 older revisions show why today's values with an assumed fixed lag are insufficient.

For a trade on day D, select the prior calendar day's vintage, retain the latest nonmissing observation in that snapshot, and compute any inflation transformation entirely within that snapshot. Save the decision date, vintage date, observation dates, units/transformation, URL, retrieval time and input snapshot with the decision. Do not forward-fill a missing monthly level to manufacture an inflation calculation. The same-day date option in the teaching app remains useful for investigation; it does not by itself authorize a trade before a release's actual time.

**What would change my call:** Admit the series after Project 2 implements that rule, reproduces the September 30 exclusion and the January 2025 vintage values, and retains auditable inputs for every rebalance. Also confirm whether Oak Grove's formal CPI benchmark should use the seasonally adjusted series or the unadjusted CPI-U; this lab does not settle that mandate definition. If the required historical snapshot cannot be obtained, keep that decision's CPI input quarantined instead of replacing it with current data. Admission establishes availability, not predictive power.

## Learn — What a data card does

**1. What is it?** A data card is a compact record of a dataset's meaning, origin, timing, transformations and limitations, with enough detail to decide whether a particular use is valid.

**2. Which fields prevent a leak?** The observation period says what was measured; the release/availability date says when it first became usable; the vintage says which version existed at the decision time. Revision policy warns that older measured dates can still contain newer information. The decision-time rule turns those facts into an eligibility filter. Units and transformations prevent interpretation errors, while the retrieval timestamp and saved response let another person reproduce the audit. A download date alone does not prove historical availability.

**3. Why is “cleaned the data” insufficient?** Removing duplicate rows or replacing missing values does not establish who produced the series, whether it is an index or a percentage, when it was released, or whether its historical values were revised. A clean-looking September row can still leak October information into a September decision.

**Simulated peer summary:** We compared a tidy two-column CSV with the data card. The hypothetical partner initially treated the observation date as the release date; the September example showed why the publication and vintage fields must survive cleaning. We agreed that a tidy dataset needs documented availability rules before it can support a historical trading signal.

## Reflect

**1. Publication lag and the as-known date:** September CPI was released in October; the September 30 snapshot stops at August. The app makes the missing information visible by showing one later observation in today's file. The exact schedule matters, and a date-only vintage needs a conservative execution rule when release-time eligibility is uncertain.

**2. What would today's data overstate?** A backtest treating September's label as September availability would overstate how early the strategy knew inflation. Revised history would also give it a version of the past unavailable at the time. That can make inflation-sensitive allocation decisions look more informed and performance appear more credible than warranted; the numerical return bias and even its direction cannot be established without a specified strategy and a paired backtest.

**Simulated closing discussion:** The hypothetical partner summarized the lesson as “the number's month is not the day I could trade on it.” We connected that to Lab 15: stability across estimation windows does not validate an allocation if the input history leaks future publications. The final shared call was to quarantine the current-history shortcut and admit only a tested, recorded vintage rule.

## Checkout

The app, written analysis and retained source/verification evidence are complete. The peer summaries are simulations; the independent no-AI explanation and the student's personal three-value check are not claimed as completed. No GitHub destination is configured in this workspace, and no GitHub upload or Brightspace quiz submission has been made.

Upload this folder to the intended course repository, excluding `.venv` and `__pycache__`, and submit links to this document and [asof_app.py](asof_app.py). Include [requirements.txt](requirements.txt), [README.md](README.md), `sources/`, `outputs/`, and `support/` for reproduction. Keep this chat and the quarantine call for the next lab.
