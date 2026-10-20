# Lab 14 — Portfolio Baselines Submission

**Case:** Meridian Foundation Reserve, carried forward from Lab 13.  
**Prepared:** October 20, 2026.  
**Company reference:** Elevance Health (NYSE: ELV). This assignment uses a fund universe and course asset-class inputs, so it does not require substituting ELV into the four-sleeve baseline.

## D — What does each portfolio earn and risk, and does it meet Meridian's mandate?

**None of the three baselines simultaneously meets the modeled 6.5% return objective and the checkable allocation rules.** The benchmark meets the expected-return target but has no eligible reserve. Equal weight and inverse volatility pass the five allocation checks, but their expected returns fall short. This does not establish that every possible allocation is infeasible; only these three baselines were evaluated.

The Lab 13 checker was rerun successfully before this work. Its original A–D verdicts remain unchanged. The [Lab 14 copy of mandate.py](mandate.py) adds the requested benchmark as candidate E and preserves the original Lab 13 file.

## R — Inputs and conventions

All expected returns, volatilities and correlations below are **course-authored training inputs**, not current market forecasts or estimates fitted to the downloaded fund prices. Return and volatility are annual. The objective follows the assignment's additive convention: estimated CPI of 2.5% + 4.0% = **6.5%**. Costs are not separately supplied or modeled, so this comparison does not prove achievement of the original net-of-cost, rolling-five-year mandate.

| Sleeve | Expected return | Volatility | Reserve eligible in the course case? |
|---|---:|---:|---|
| Treasury bills | 3.5% | 0.5% | Yes |
| Treasury 10-year note | 4.3% | 7.0% | Yes |
| Investment-grade bond fund | 5.0% | 6.0% | No |
| Global equity index fund | 8.0% | 16.0% | No |

| Correlation | Bills | 10-year | IG bonds | Equity |
|---|---:|---:|---:|---:|
| Bills | 1.00 | 0.10 | 0.05 | 0.00 |
| 10-year | 0.10 | 1.00 | 0.80 | −0.10 |
| IG bonds | 0.05 | 0.80 | 1.00 | 0.25 |
| Equity | 0.00 | −0.10 | 0.25 | 1.00 |

Weights, returns and volatilities are stored as decimal fractions in `portfolio.py`. The Lab 13 mandate checker takes weights in percentage points, so the verification script multiplies baseline weights by 100 before passing them to that checker. Calculations retain full precision; rounding occurs only for display.

## I — Implementation and rerun commands

Run these commands from the `Lab 14` folder:

```sh
python3 portfolio.py
python3 mandate.py
python3 support/check_results.py
```

This Mac uses `python3`. All Python files use only the standard library. The core [portfolio.py](portfolio.py) runs on its own without the price dataset or a network connection. It exposes reusable functions for covariance, weights, expected return, variance, volatility, reserve share and objective checks.

For sleeve volatilities σ and correlations ρ, the covariance entries are `Σ[i][j] = ρ[i][j] × σ[i] × σ[j]`. Expected return is `Σᵢ wᵢμᵢ`, portfolio variance is `ΣᵢΣⱼ wᵢwⱼΣ[i][j]`, and volatility is the square root of variance. Reserve share adds the weights of the two eligible Treasury sleeves. Inverse-volatility weights are `(1/σᵢ) / Σⱼ(1/σⱼ)`.

The engine refuses correlations outside −1 to +1, nonfinite values, asymmetry, incorrect dimensions and a diagonal other than one. It also checks positive volatilities and long-only weights summing to one. These are the lab's input safeguards, with basic consistency checks; there is no general positive-semidefinite matrix test or optimizer in this lab.

## V — Known-answer results

| Portfolio | Bills | 10-year | IG bonds | Equity | Expected return | Volatility | Reserve eligible | Meets 6.5%? |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Benchmark | 0.0% | 0.0% | 40.0% | 60.0% | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0% | 25.0% | 25.0% | 25.0% | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3% | 6.0% | 7.0% | 2.6% | 3.77% | 1.05% | 90.3% | No |

Every displayed value matches the assignment. The displayed inverse-volatility weights sum to 99.9% because of rounding; the underlying weights sum to 100%. Its expected-return shortfall is about 2.73 percentage points, versus 1.30 points for equal weight. The benchmark exceeds the assumed objective by 0.30 points.

Actual output is saved in [outputs/Portfolio.txt](outputs/Portfolio.txt), full-precision results in [outputs/Results.json](outputs/Results.json), and test evidence in [outputs/Verification.txt](outputs/Verification.txt).

| Required verification | Actual result |
|---|---|
| Course known answers | All weights, returns, volatilities, reserve shares and objective verdicts match |
| Change IG–equity correlation to 0.50 in both cells | Benchmark volatility rises from 10.46% to **11.00%** |
| Restore 0.25 in both cells | Benchmark volatility returns to **10.46%** |
| Set both IG–equity cells to 1.3 | Clear error; exit status **1** |
| Change only one cell to 0.50 | Asymmetry error; exit status **1** |
| Run eight automated tests | **8 passed**, including known answers, hand calculation and candidate E |

The mutation tests ran disposable copies of the file. The delivered correlation table remains at the original values. These were local verification runs, not a claimed exchange with a human partner.

## Read it — The benchmark breaks the reserve rule

Meridian needs four quarterly distributions of $0.75 million in eligible reserves. On its $100 million base, the minimum is `4 × 0.75 / 100 = 3.0%`.

Candidate E is 40% investment-grade bond fund and 60% global equity index fund, with every other holding at zero. The extended checker reports:

| Check | Candidate E measurement | Result |
|---|---:|---|
| Weights sum to 100% | 100.0% | Pass |
| Long-only: lowest holding weight | 0.0% | Pass |
| Eligible reserve at least 3% | 0.0% | **FAIL** |
| Redeemable within five business days at least 90% | 100.0% | Pass |
| Largest nonexempt company at most 8% | 0.0% | Pass |

Candidate E fails exactly one allocation rule. The client's benchmark is a performance comparison, not necessarily a permitted implementation. The bond fund is liquid but is not reserve eligible under the supplied case. Output for candidates A–E is in [outputs/Mandate.txt](outputs/Mandate.txt).

Equal weight and inverse volatility pass these five allocation checks using the same holdings definitions. None of these checks resolves S9's ambiguous calendar-year loss statement, verifies turnover or annual rebalancing, or guarantees future returns. Standard deviation is not a maximum-loss limit.

## Diversification — What it is and how it works

Diversification spreads exposure across assets whose returns do not move together perfectly. With correlation below +1, the covariance contribution is smaller than it would be under perfect positive correlation, lowering volatility for a fixed mix relative to that perfectly correlated case. It can make a portfolio less risky than either asset under suitable weights, volatilities and correlations; it does not always do so.

For this benchmark, 10.46% is below equities' 16.0% volatility but above the bond fund's 6.0%. With perfect positive correlation, the same mix would have volatility `0.4 × 6 + 0.6 × 16 = 12.00%`. The supplied correlation lowers that to 10.46%.

### Benchmark volatility by hand

Use percentage-point units: bond volatility is 6 and equity volatility is 16.

```text
Expected return = 0.40 × 5.0 + 0.60 × 8.0 = 6.80%

Variance = (0.40² × 6²) + (0.60² × 16²)
           + (2 × 0.40 × 0.60 × 0.25 × 6 × 16)
         = 5.76 + 92.16 + 11.52
         = 109.44 percentage-points squared

Volatility = √109.44 = 10.461357...% = 10.46%

At correlation 0.50:
Variance = 5.76 + 92.16 + 23.04 = 120.96
Volatility = √120.96 = 10.998182...% = 11.00%

If covariance is incorrectly omitted:
Volatility = √(5.76 + 92.16) = 9.895453...% = 9.90%
```

Ignoring the cross-asset covariance here assumes zero correlation and understates the supplied benchmark risk.

## Reflection draft

**Why inverse volatility piles into bills:** The inputs assign bills only 0.5% volatility. Its reciprocal is 200, compared with approximately 14.286 for the Treasury note, 16.667 for IG bonds and 6.25 for equity. Normalizing those reciprocals places approximately 84.3% in bills. This rule uses each sleeve's own volatility to set weights; it does not target the required return, optimize the full covariance matrix or guarantee equal risk contributions. Its low modeled volatility comes with an expected return of only 3.77%.

**Which baseline to show the CIO first:** I would start with the benchmark because it is the client's stated comparison and it makes the central conflict visible: 6.80% expected return exceeds the 6.5% assumption, while its 0% reserve fails the 3% floor. Then I would compare equal weight and inverse volatility to show that reducing modeled risk and adding reserves can leave the return objective unmet. The next design task is to seek a mix satisfying both requirements and clarify the remaining mandate questions. No such mix is optimized in this lab.

These are written drafts for review and discussion. No partner explanation or personal reflection is represented as already performed.

## Before Thursday — Project 2 fund universe

Lab 13 proposed the fictional **Oak Grove Scholarship Reserve** with a seven-year horizon, CPI + 3% net return objective, 2% initial reserve floor and at least 90% five-day liquidity. I carry that proposed client forward. At the same labelled 2.5% CPI estimate, its additive nominal target would be **5.5%**, distinct from Meridian's 6.5% target. Its optimization objective still requires a client decision.

The four funds below cover the requested roles. Fund identity and role were checked against issuer descriptions. They are educational candidates for the next exercise, not a completed allocation.

| Ticker | Fund name | Proposed role | Issuer source |
|---|---|---|---|
| BIL | State Street SPDR Bloomberg 1–3 Month T-Bill ETF | Cash and Treasury-bill reserve proxy | [State Street](https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil) |
| IEF | iShares 7–10 Year Treasury Bond ETF | Intermediate government bonds | [iShares](https://www.ishares.com/us/products/239456/ishares-7-10-year-treasury-bond-etf) |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Investment-grade corporate fixed income | [iShares](https://www.ishares.com/us/products/239566/lqd-ishares-iboxx-investment-grade-corporate-bond-etf) |
| VT | Vanguard Total World Stock ETF | Diversified global equity | [Vanguard](https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etfp) |

IEF is a fund holding a maturity range, not a single ten-year note. BIL and IEF are proposed Treasury exposures; their reserve treatment should be confirmed for the final fund-based mandate rather than automatically inherited from the course's direct-security flags. Fund price histories will be used in the next exercise, separately from today's authored risk inputs.

**ELV remains the company selection** for any company-specific extension. It is an individual stock, so it does not replace a required fund in this fund-only universe. No ELV allocation, return assumption or invented company dataset has been added.

### Monthly adjusted prices

[prices.csv](prices.csv) contains `Date,BIL,IEF,LQD,VT`, with the oldest month first. There are **61 aligned monthly price levels, September 2021 through September 2026**, giving **60 monthly return intervals** from October 2021 through September 2026. The unfinished October 2026 month is excluded. Prices are Yahoo Finance's USD **Adj Close** field, which incorporates distribution and split adjustments, not unadjusted Close.

| Ticker | Historical-data source | Download date |
|---|---|---|
| BIL | [Yahoo Finance monthly history](https://finance.yahoo.com/quote/BIL/history/?frequency=1mo) | October 20, 2026 |
| IEF | [Yahoo Finance monthly history](https://finance.yahoo.com/quote/IEF/history/?frequency=1mo) | October 20, 2026 |
| LQD | [Yahoo Finance monthly history](https://finance.yahoo.com/quote/LQD/history/?frequency=1mo) | October 20, 2026 |
| VT | [Yahoo Finance monthly history](https://finance.yahoo.com/quote/VT/history/?frequency=1mo) | October 20, 2026 |

The browser retrieval of the history pages was unavailable; the data were successfully downloaded through Yahoo's chart endpoint using `interval=1mo` and `indicators.adjclose[0].adjclose`. Exact URLs, UTC timestamps and source hashes are retained in [sources/Prices.json](sources/Prices.json), with original responses in [original Yahoo responses](sources/yahoo/). The date labels the monthly bar by its first calendar day; it is not a claim that the closing trade occurred on that day. No missing values were filled, and no months were silently dropped. Yahoo may revise historical adjustments in later downloads.

To refresh this fixed date window, run `python3 support/fetch_prices.py` with internet access, then `python3 support/check_results.py`. A monthly total-return approximation is `AdjClose[t] / AdjClose[t−1] − 1`; do not add the distributions again.

## Personal checkout items

The computational work and written analysis were prepared with AI assistance. The following activities need the student's own participation:

- **Code quiz:** Why does the variance calculation include both the IG-bond/equity term and the equity/IG-bond term? Your answer: **pending**. Answer before requesting the AI explanation.
- **No-AI code explanation:** Explain the variance block to your partner line by line, and record their actual question and your answer: **pending**.
- **Partner swap and break:** The local refusal test is complete; a run of a partner's actual file and exchange are **not recorded**.
- **Reflection discussion:** Review the draft and explain your reasoning to your partner: **pending**.
- **GitHub checkout:** Upload the files and supply the individual file links. No repository destination was provided and no publication is claimed.

## Submission files

See [README.md](README.md) for the exact upload list and rerun commands. The main deliverables are this document, [portfolio.py](portfolio.py), [mandate.py](mandate.py), and [prices.csv](prices.csv). Supporting outputs, source records and checks are grouped in their own folders.
