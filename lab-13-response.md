# Lab 13 — Portfolio Mandate Defense

**Case:** Meridian Foundation Reserve (fictional), USD 100 million.

**Preparation note:** The code and this written draft were prepared with AI assistance. Sections that the lab designates as personal or AI-closed are draft responses for the student to review and rewrite independently. No completed personal quiz response, partner conversation, or GitHub submission is claimed.

## Decision

A passes all five checkable allocation rules. B fails the reserve, five-business-day liquidity, and issuer concentration rules. C fails the reserve rule. Passing the checker does not establish full mandate compliance: the loss statement needs clarification, and the holdings alone do not establish achievement of the return objective, annual turnover compliance, or an appropriate optimization objective.

## S1–S10: classification and IPS mapping

This is an AI-assisted classification draft; the lab requests an independent initial sort.

| Statement | Type | Reason and place in the investment policy statement |
|---|---|---|
| S1 — Seven-year horizon; annual rebalancing. | Hard constraint | Specifies the planning horizon and implementation schedule; an allocation snapshot cannot establish future adherence. |
| S2 — CPI + 4% annually, net of costs, over rolling five years. | Objective | Defines the desired real return, cost basis, and evaluation period, but does not specify an optimization function or guarantee performance. |
| S3 — $0.75 million quarterly; twelve months of payouts in eligible reserves. | Hard constraint | Sets spending needs and a reserve floor of $3 million, or 3% of the initial portfolio. |
| S4 — 60% global equities / 40% U.S. investment-grade bonds benchmark. | Preference (evaluation reference) | Names the performance comparison portfolio; it does not require actual 60/40 weights or impose a tracking-error limit. |
| S5 — Long-only; no borrowing, short sales, or derivatives. | Hard constraint | Restricts implementation; the checker tests nonnegative weights and full allocation using only the permitted holdings. |
| S6 — No single issuer above 8%. | Hard constraint | Caps each nonexempt company's combined securities; cash, Treasury securities, and diversified funds are exempt under the case convention. |
| S7 — Annual turnover at most 25% without committee approval. | Hard constraint | Requires turnover measurement and an approval process; current weights alone cannot measure annual trading. |
| S8 — At least 90% redeemable within five business days. | Hard constraint | Sets a measurable liquidity floor using the supplied redemption times. |
| S9 — No calendar-year loss greater than 10%; no measure or breach rule. | Unverifiable promise | Expresses risk tolerance without an operational definition or breach response; do not convert it into an invented risk test or guarantee. |
| S10 — No sector, ESG, tax, or home-bias preference; pilot objective unspecified. | Missing | These absent preferences add no restrictions, while the missing optimization objective prevents defining what the pilot should choose. |

S4 is the least straightforward classification: a benchmark is an evaluation instruction, not necessarily a portfolio preference. Within the lab's five categories, “preference” is the closest fit for this reference allocation; it would become a portfolio constraint only if the CIO supplied an allocation or tracking requirement.

## Checker and verification

Run from this folder:

```sh
python3 mandate.py
```

This computer provides `python3`, not a `python` command. The script uses only the Python standard library. All holdings, candidates, limits, and payout inputs are editable at the top. Weights are percentage points and reserve amounts are USD millions.

The reserve minimum is computed as:

```text
4 quarters × $0.75 million / $100 million × 100 = 3.0%
```

The reserve check uses the case's eligibility flags. In particular, the ten-year Treasury note is eligible even though it has price risk; reserve eligibility and price stability are different concepts.

| Rule / measured percentage | A | B | C | D |
|---|---|---|---|---|
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only: lowest weight | 0.0 pass | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve ≥ 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL | 100.0 pass |
| Redeemable within five days ≥ 90% | 100.0 pass | 85.0 FAIL | 100.0 pass | 100.0 pass |
| Largest single company ≤ 8% | 0.0 pass | 9.0 FAIL | 8.0 pass | 0.0 pass |
| Calendar-year loss | Requires CIO clarification | Requires CIO clarification | Requires CIO clarification | Requires CIO clarification |
| Verdict | Passes every checkable rule | Fails 3 rules | Fails 1 rule | Passes every checkable rule |

Actual program output and assertion results are saved in [verification.txt](verification.txt). The printed verdict refers to the five allocation checks in the assignment, not every provision of the IPS. The code neither tests S9 nor estimates returns, risk, or optimal weights.

### Required negative-weight probe

In a temporary copy of A, Cash is changed from 2 to −2 and Global equity index fund from 60 to 64. Its sum remains 100.0%, lowest weight becomes −2.0% (FAIL), reserve becomes 10.0% (pass), five-day liquidity remains 100.0% (pass), and largest company remains 0.0% (pass). It fails exactly one rule. The saved candidate A retains the original 2% Cash and 60% Global equity index fund.

### Code quiz — student response pending

Explain this line before reading an explanation:

```python
company_weights[issuer] = company_weights.get(issuer, 0.0) + weight
```

What does it do when both Acme bonds and Acme stock appear, and why would checking each holding separately be wrong? If another line is the one you understand least, use that line instead. Record your own answer here after responding; no personal answer has been invented.

## Attack: candidate D

Candidate D holds 100% Cash and 0% of every other holding. It passes all five checks: it is fully invested and long-only, holds ample eligible reserves, is immediately liquid, and has no nonexempt company exposure. Nevertheless, the CIO could reasonably reject it under **S2** because satisfying CPI + 4% net over rolling five-year periods has not been supported by any cash-return analysis. This is a suitability objection, not a demonstrated future return failure; no returns were supplied or assumed.

**Two-sentence judgment draft for independent rewriting:** The objection holds as a reason to withhold approval: a 100% cash portfolio satisfies the allocation rules but has no demonstrated ability to achieve the required real return. S2 decides the objection because CPI + 4% net over rolling five-year periods remains the objective even when every mechanical check passes.

**Sceptical-colleague role draft:** The case instructs an individual student to play both roles. Against D, cite S2 and ask what evidence supports the target return; S4 alone is insufficient to reject D because the benchmark does not mandate matching weights. This is a drafted self-review, not a report of an actual partner exchange.

## One question for the CIO

**Draft for independent rewriting:** What should the pilot optimize: the probability of meeting CPI + 4% net over rolling five-year periods, or tracking the 60/40 benchmark?

**Answer that would change the design:** If the CIO chooses benchmark tracking, the design would target small deviations from the reference portfolio subject to the hard constraints. If the CIO chooses the probability of meeting the real-return target, the design would compare modeled inflation-adjusted outcomes net of costs and could accept greater benchmark deviation. That answer changes the optimization objective and potentially the allocation; the present data do not justify numerical optimal weights. S9 still requires an agreed loss measure and breach response before implementing either design.

## Investment policy statement: what it is and how it works

An investment policy statement (IPS) is the written agreement connecting a client's purpose and return objectives to investment limits, implementation responsibilities, and performance review. It gives decision-makers a common basis for selecting, monitoring, and revising a portfolio.

Objectives describe desired outcomes; constraints define the feasible choices. Preferences guide selection within those choices, and a benchmark supports evaluation. A usable IPS also states how compliance is measured, who approves exceptions, and what happens after a breach. A return aspiration is not a guaranteed outcome.

For Meridian, S2 sets the return objective; S1 sets the horizon and rebalance schedule; S3 and S8 set spending and liquidity requirements; S5 and S6 restrict holdings and concentration; S7 governs turnover and approval; and S4 supplies the comparison benchmark. S9 records an unresolved risk requirement, while S10 exposes the missing pilot objective. These mappings appear alongside the individual classifications above.

## Reflection draft

1. A portfolio can pass every checkable allocation rule and still be wrong because those checks establish only part of suitability. D shows the gap: adequate liquidity and diversification-limit compliance do not establish achievement of S2. Likewise, annual turnover requires trading history and a measurement convention, annual rebalancing requires implementation over time, and S9 lacks an agreed test and response. No borrowing or derivative use outside the supplied holdings can be inferred from the weight table alone.
2. The least certain type in this draft is S4. A named benchmark sounds prescriptive, but it does not state that weights must equal 60/40. Treating it as a hard allocation constraint would invent a requirement. S9 also sounds absolute, yet its undefined measure and breach rule make it an unverifiable promise in the requested classification.

## Project 2 — proposed client mandate

**Assumption:** No personal Project 2 client was provided. The following is an explicitly fictional proposed client for adaptation, not a claim about an existing client's instructions.

**Client:** Oak Grove Scholarship Reserve, a fictional nonprofit with USD 10 million and a seven-year horizon.

**Objective:** Seek CPI + 3% annually, net of all investment costs, over rolling five-year periods while funding USD 50,000 quarterly scholarship distributions.

**Hard constraints:**

- Maintain twelve months of scheduled distributions in cash or daily-liquid U.S. government securities: initially $200,000, or 2% of the $10 million reserve.
- Keep at least 90% redeemable within five business days.
- Use long-only, fully funded positions; no borrowing, short sales, or derivatives.
- Limit any single company's combined securities to 8%; exempt cash, U.S. Treasury securities, and diversified funds.
- Review and rebalance annually, subject to the turnover limit; meet distributions and the reserve requirement throughout the year.
- Limit annual turnover to 25% without committee approval. For this proposed IPS, define turnover as the lesser of annual security purchases and sales divided by average month-end net asset value, excluding cash movements themselves; trades used to fund payouts remain included.

**One question for the client:** Should the pilot maximize the modeled probability of achieving CPI + 3% net over rolling five-year periods, or minimize modeled volatility while targeting that return?

If the client chooses the second objective, the model would favor lower-volatility feasible allocations that still meet the modeled return target; if no such allocation exists, it would report infeasibility for a client decision. No allocation is optimized here.

## Checkout status

- Prepared: [lab-13-response.md](lab-13-response.md), [mandate.py](mandate.py), and [verification.txt](verification.txt).
- Student action: independently review/rewrite the AI-closed portions and answer the code quiz.
- GitHub destination is not yet provided; no push or quiz submission is claimed. Upload these files to the course repository, then paste the individual Markdown and Python file links into the Lab 13 quiz. The verification file can be linked as supporting evidence.
