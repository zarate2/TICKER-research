# ELV — Operating sensitivity, individual submission draft

**David Zarate · Elevance Health, Inc. (NYSE: ELV)**  
**Model:** FY2025 opening balances; forecast FY2026–FY2030.

**Completion status:** The sensitivity results, restored-base check and driver explanation are complete below. The original locked prediction and the check performed on a partner's analysis have not been supplied, so those requirements remain incomplete. A previously saved partner question and response are included with their source; their applicability to this sensitivity exercise is awaiting confirmation.

## Inputs and method

The two independent inputs are `growth` and `margin` in the existing ELV model. Every case uses a fresh deep copy of the separate base input set and reruns all linked statements. Only the selected input path changes. All other independent assumptions reset to base before every run. The final run restores the original base.

| Input and case | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 |
|---|---:|---:|---:|---:|---:|
| Revenue growth — lower | 2.0% | 2.0% | 2.0% | 2.0% | 2.0% |
| Revenue growth — base | 3.0% | 3.0% | 3.0% | 3.0% | 3.0% |
| Revenue growth — higher | 4.0% | 4.0% | 4.0% | 4.0% | 4.0% |
| Blended gross margin — lower | 13.8% | 14.0% | 14.2% | 14.3% | 14.3% |
| Blended gross margin — base | 14.3% | 14.5% | 14.7% | 14.8% | 14.8% |
| Blended gross margin — higher | 14.8% | 15.0% | 15.2% | 15.3% | 15.3% |

Revenue growth is the annual percentage change in operating revenue. Gross margin is gross profit divided by operating revenue, after benefit expense and product costs. It is not the medical benefit ratio. The revenue-growth paths shift by ±1.0 **percentage point** from base; margin paths shift by ±0.5 **percentage points** in every forecast year.

These are the previously agreed judgment ranges. The growth range brackets the base near 2024's 2.93% reported growth without assuming that acquisition-supported 2025 growth of 12.77% repeats. The margin range tests weaker or stronger profitability against historical blended margins of 16.79%, 15.92% and 14.26% in 2023–2025. Source: [existing history and assumptions](lab-10-elv.md).

## Visible sensitivity results

Operating profit is operating income after PP&E D&A and intangible amortization, before investment income, interest and tax. **FCFE** is CFO less capex and scheduled net debt repayment, before distributions and revolver activity. Statement outputs and their changes are **USD millions**. Value and its change are **USD per opening common share**.

| Case | FY2030 operating profit | Change from base | FY2030 FCFE | Change from base | Value/share | Change from base | Checks |
|---|---:|---:|---:|---:|---:|---:|---|
| Growth — lower | 7,995.37 | -484.20 | 5,868.84 | -247.93 | 354.20 | -11.04 | PASS |
| Growth — base | 8,479.57 | +0.00 | 6,116.77 | +0.00 | 365.24 | +0.00 | PASS |
| Growth — higher | 8,982.94 | +503.37 | 6,370.22 | +253.46 | 376.51 | +11.27 | PASS |
| Margin — lower | 8,135.99 | -343.58 | 5,859.01 | -257.76 | 351.66 | -13.58 | PASS |
| Margin — base | 8,479.57 | +0.00 | 6,116.77 | +0.00 | 365.24 | +0.00 | PASS |
| Margin — higher | 8,823.15 | +343.58 | 6,374.52 | +257.76 | 378.82 | +13.58 | PASS |

Changes equal changed output minus base output using unrounded values. Subtracting rounded display values can differ by 0.01 in the output's units. All six runs have positive FCFE throughout the forecast and pass the accounting and funding checks. Invalid runs are excluded from comparisons; negative cash flows would be retained and valuation marked unavailable under this sensitivity workflow.

Valuation holds the existing 10% cost of equity, 2.5% terminal growth and 220.723898 million opening shares constant. It retains the terminal assumption that net debt paydown stops after 2030. It remains conditional on the model's simplified regulatory-capital and terminal assumptions and is not a current market-price target.

## Passing restored-base check

| Check | Before sensitivity | Restored and rerun | Result |
|---|---:|---:|---|
| Revenue-growth path, FY2026–2030 | 3%, 3%, 3%, 3%, 3% | 3%, 3%, 3%, 3%, 3% | PASS |
| Gross-margin path, FY2026–2030 | 14.3%, 14.5%, 14.7%, 14.8%, 14.8% | 14.3%, 14.5%, 14.7%, 14.8%, 14.8% | PASS |
| FY2030 operating profit ($m) | 8,479.567201 | 8,479.567201 | PASS |
| FY2030 FCFE ($m) | 6,116.765964 | 6,116.765964 | PASS |
| Value/share ($) | 365.238954 | 365.238954 | PASS |
| All other independent inputs | Original base | Exactly identical | PASS |
| All five annual statement rows | Initial base | Exactly identical | PASS |

The restored inputs and outputs match exactly before rounding. Display tolerance is 0.01 in each output unit. The accounting gap tolerance is $0.000001 million. Across all six sensitivity runs, the maximum absolute balance-sheet gap is $0.00000000002183 million and the maximum cash-flow reconciliation gap is $0.00000000000091 million, both below tolerance. Cash floors, borrowing capacity and nonnegative debt/long-lived-asset checks also pass.

## Main driver over the tested ranges

| Driver | Operating-profit span ($m) | FCFE span ($m) | Value/share span ($) |
|---|---:|---:|---:|
| Revenue growth | 987.56 | 501.38 | 22.31 |
| Blended gross margin | 687.16 | 515.51 | 27.16 |

Each span is maximum minus minimum across the three valid lower/base/higher results, before rounding.

**Over these ranges, revenue growth is the larger driver of final-year operating profit, while blended gross margin is the larger driver of FCFE and value per share.** Faster growth increases profit but also requires more receivables and other working-capital assets, partially offset by higher claims payable. In the higher-growth case, final-year net income increases by $382.56 million, but the net working-capital cash effect is approximately -$129.10 million, leaving FCFE up $253.46 million. In the higher-margin case, net income rises by $261.12 million and the claims-payable cash effect is -$3.36 million, leaving FCFE up $257.76 million. Revenue-based receivables do not change in that margin case. Value reflects all forecast cash flows and the terminal cash flow, not only final-year operating profit.

The ordering depends on the tested growth and margin ranges; it does not establish that one input is inherently more important. The FCFE spans are close. Raw dollar spans should not be used to rank unlike companies.

## Locked prediction reconciliation — original record required

**Status: incomplete.** No original timestamped prediction or pre-run Git commit has been supplied. The post-run result below is available for reconciliation if it matches the actual locked change; it is not a substitute for a pre-run prediction.

Selected example: revenue growth **3% → 2% in each year FY2026–FY2030**, with every other independent input at base.

| Output | Base | Actual changed output | Actual signed change | Original predicted change | Prediction error |
|---|---:|---:|---:|---|---|
| FY2030 operating profit ($m) | 8,479.567201 | 7,995.371558 | -484.195643 | Pending | Pending |
| FY2030 FCFE ($m) | 6,116.765964 | 5,868.838973 | -247.926991 | Pending | Pending |
| Value/share ($) | 365.238954 | 354.199999 | -11.038955 | Pending | Pending |

- Original locked record, timestamp/time zone or Git commit: **pending**.
- Prediction error = actual signed change minus originally predicted signed change, in matching units: **pending original prediction**.
- Explanation of any prediction error: **pending**.
- Whether the result changes the student's valuation conclusion or research priority, and why (including a no-change reason): **pending student judgment**.

## Partner evidence

**Previously recorded question**, from [lab10-output.md, Part E](lab10-output.md): “How come your liabilities are increasing even though expected life expectency is increasing?”

**Recorded response, summarized:** ELV's medical claims payable represents healthcare claims incurred but not yet paid. The model holds claims payable at approximately 11.53% of benefit expense, so that liability grows with benefit expense rather than following a direct life-expectancy assumption. Claims payable rises from $17.08 billion at the opening date to $19.68 billion in 2030. Total liabilities nevertheless decline from $76.97 billion in 2026 to $75.07 billion in 2030 as debt is repaid. Life expectancy is not an explicit model input.

This is a saved prior exchange, not evidence that the current sensitivity partner exchanges occurred. Confirm its applicability or replace it with the actual sensitivity question and response.

- Partner name and actual exchange date: **pending**.
- Actual sensitivity question received and response, if different from the prior exchange: **pending**.
- Check performed on the partner's analysis: **pending**. Record their company, selected input and range, base and changed outputs with units, the difference recomputed, other independent inputs checked against base, and the statement link traced.
- Question or correction raised on their analysis and its resolution: **pending**.

## Supporting evidence

The tables above are visible output; no code execution is needed to read the results. The [full sensitivity report](Lab11_elv-operating-sensitivity.md) includes annual accounting checks and a selected statement trace. [Full-precision inputs and annual statements](Lab11_elv-operating-sensitivity-details.json) retain all six runs and both base runs. The [existing model](lab10_proforma_elv.py) calls the [sensitivity runner](Lab11_elv_operating_sensitivity.py) with `python3 lab10_proforma_elv.py --operating-sensitivity`.
