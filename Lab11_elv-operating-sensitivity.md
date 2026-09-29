# ELV operating sensitivity

FY2025-base model; forecast FY2026–FY2030. All monetary statement figures are USD millions; value per opening common share is USD/share.

Each run starts from a fresh deep copy of the separate base input set. Only the named driver changes; all linked statements recalculate. Cases are listed in lower/base/higher order. Ranges are those agreed in the chat; invalid runs are excluded from comparisons.

Operating profit is operating income after PP&E D&A and intangible amortization, before investment income, interest and tax. FCFE is CFO minus capex and scheduled net debt repayment, before buybacks, dividends and revolver activity.

Valuation retains the existing 10% cost of equity, 2.5% terminal growth, terminal debt-paydown addback and 220.723898 million opening shares. It is conditional on the model's simplified capital and terminal assumptions, not a current price target. Any negative FCFE remains signed and makes value/share unavailable in this workflow.

## Actual inputs by run

| Driver | Case | Units | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 |
|---|---|---|---:|---:|---:|---:|---:|
| Revenue growth | lower | % annual revenue growth | 2.0% | 2.0% | 2.0% | 2.0% | 2.0% |
| Revenue growth | base | % annual revenue growth | 3.0% | 3.0% | 3.0% | 3.0% | 3.0% |
| Revenue growth | higher | % annual revenue growth | 4.0% | 4.0% | 4.0% | 4.0% | 4.0% |
| Blended gross margin | lower | % of operating revenue | 13.8% | 14.0% | 14.2% | 14.3% | 14.3% |
| Blended gross margin | base | % of operating revenue | 14.3% | 14.5% | 14.7% | 14.8% | 14.8% |
| Blended gross margin | higher | % of operating revenue | 14.8% | 15.0% | 15.2% | 15.3% | 15.3% |

## Comparable outputs and signed changes from base

Changes use unrounded values; subtracting displayed rounded values can differ by 0.01 in the stated output unit.

| Run | Checks | FY2030 operating profit ($m) | Change ($m) | FY2030 FCFE ($m) | Change ($m) | Value/share ($) | Change ($/share) |
|---|---|---:|---:|---:|---:|---:|---:|
| Revenue growth — lower | PASS | 7,995.37 | -484.20 | 5,868.84 | -247.93 | 354.20 | -11.04 |
| Revenue growth — base | PASS | 8,479.57 | +0.00 | 6,116.77 | +0.00 | 365.24 | +0.00 |
| Revenue growth — higher | PASS | 8,982.94 | +503.37 | 6,370.22 | +253.46 | 376.51 | +11.27 |
| Blended gross margin — lower | PASS | 8,135.99 | -343.58 | 5,859.01 | -257.76 | 351.66 | -13.58 |
| Blended gross margin — base | PASS | 8,479.57 | +0.00 | 6,116.77 | +0.00 | 365.24 | +0.00 |
| Blended gross margin — higher | PASS | 8,823.15 | +343.58 | 6,374.52 | +257.76 | 378.82 | +13.58 |

## Output spans

Maximum minus minimum across valid lower/base/higher results, calculated before rounding. The count is specific to each output; unavailable values and invalid runs are excluded.

| Driver | Operating profit span ($m); valid count | FCFE span ($m); valid count | Value/share span ($); valid count |
|---|---:|---:|---:|
| Revenue growth | 987.56; 3/3 | 501.38; 3/3 | 22.31; 3/3 |
| Blended gross margin | 687.16; 3/3 | 515.51; 3/3 | 27.16; 3/3 |

## Annual accounting and funding checks

All gaps and cash/borrowing amounts are USD millions. PASS includes finite values, nonnegative debt/long-lived assets, balanced statements, cash-flow reconciliation, the cash floor and revolver capacity. Gap tolerance: $0.000001 million.

| Run | Year | Balance gap | Cash-flow gap | Cash above floor | Revolver | Revolver headroom | Status / reason |
|---|---:|---:|---:|---:|---:|---:|---|
| Initial base | 2025 | 0.00 | N/A — opening | 0.00 | 0.00 | 5,000.00 | PASS |
| Initial base | 2026 | 0.00 | 0.00 | 503.51 | 0.00 | 5,000.00 | PASS |
| Initial base | 2027 | 0.00 | 0.00 | 1,378.51 | 0.00 | 5,000.00 | PASS |
| Initial base | 2028 | 0.00 | 0.00 | 2,675.24 | 0.00 | 5,000.00 | PASS |
| Initial base | 2029 | 0.00 | 0.00 | 4,384.20 | 0.00 | 5,000.00 | PASS |
| Initial base | 2030 | 0.00 | 0.00 | 6,366.96 | 0.00 | 5,000.00 | PASS |
| Revenue growth — lower | 2025 | 0.00 | N/A — opening | 0.00 | 0.00 | 5,000.00 | PASS |
| Revenue growth — lower | 2026 | 0.00 | 0.00 | 539.76 | 0.00 | 5,000.00 | PASS |
| Revenue growth — lower | 2027 | 0.00 | 0.00 | 1,388.23 | 0.00 | 5,000.00 | PASS |
| Revenue growth — lower | 2028 | 0.00 | 0.00 | 2,588.80 | 0.00 | 5,000.00 | PASS |
| Revenue growth — lower | 2029 | 0.00 | 0.00 | 4,125.71 | 0.00 | 5,000.00 | PASS |
| Revenue growth — lower | 2030 | 0.00 | 0.00 | 5,860.55 | 0.00 | 5,000.00 | PASS |
| Revenue growth — base | 2025 | 0.00 | N/A — opening | 0.00 | 0.00 | 5,000.00 | PASS |
| Revenue growth — base | 2026 | 0.00 | 0.00 | 503.51 | 0.00 | 5,000.00 | PASS |
| Revenue growth — base | 2027 | 0.00 | 0.00 | 1,378.51 | 0.00 | 5,000.00 | PASS |
| Revenue growth — base | 2028 | 0.00 | 0.00 | 2,675.24 | 0.00 | 5,000.00 | PASS |
| Revenue growth — base | 2029 | 0.00 | 0.00 | 4,384.20 | 0.00 | 5,000.00 | PASS |
| Revenue growth — base | 2030 | 0.00 | 0.00 | 6,366.96 | 0.00 | 5,000.00 | PASS |
| Revenue growth — higher | 2025 | 0.00 | N/A — opening | 0.00 | 0.00 | 5,000.00 | PASS |
| Revenue growth — higher | 2026 | 0.00 | 0.00 | 467.26 | 0.00 | 5,000.00 | PASS |
| Revenue growth — higher | 2027 | 0.00 | 0.00 | 1,368.09 | 0.00 | 5,000.00 | PASS |
| Revenue growth — higher | 2028 | 0.00 | 0.00 | 2,760.87 | 0.00 | 5,000.00 | PASS |
| Revenue growth — higher | 2029 | 0.00 | 0.00 | 4,643.87 | 0.00 | 5,000.00 | PASS |
| Revenue growth — higher | 2030 | 0.00 | 0.00 | 6,880.09 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — lower | 2025 | 0.00 | N/A — opening | 0.00 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — lower | 2026 | 0.00 | 0.00 | 383.41 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — lower | 2027 | 0.00 | 0.00 | 1,028.90 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — lower | 2028 | 0.00 | 0.00 | 2,085.94 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — lower | 2029 | 0.00 | 0.00 | 3,544.65 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — lower | 2030 | 0.00 | 0.00 | 5,269.66 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — base | 2025 | 0.00 | N/A — opening | 0.00 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — base | 2026 | 0.00 | 0.00 | 503.51 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — base | 2027 | 0.00 | 0.00 | 1,378.51 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — base | 2028 | 0.00 | 0.00 | 2,675.24 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — base | 2029 | 0.00 | 0.00 | 4,384.20 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — base | 2030 | 0.00 | 0.00 | 6,366.96 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — higher | 2025 | 0.00 | N/A — opening | 0.00 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — higher | 2026 | 0.00 | 0.00 | 623.61 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — higher | 2027 | 0.00 | 0.00 | 1,728.13 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — higher | 2028 | 0.00 | 0.00 | 3,264.53 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — higher | 2029 | 0.00 | 0.00 | 5,223.74 | 0.00 | 5,000.00 | PASS |
| Blended gross margin — higher | 2030 | 0.00 | 0.00 | 7,464.27 | 0.00 | 5,000.00 | PASS |
| Restored base | 2025 | 0.00 | N/A — opening | 0.00 | 0.00 | 5,000.00 | PASS |
| Restored base | 2026 | 0.00 | 0.00 | 503.51 | 0.00 | 5,000.00 | PASS |
| Restored base | 2027 | 0.00 | 0.00 | 1,378.51 | 0.00 | 5,000.00 | PASS |
| Restored base | 2028 | 0.00 | 0.00 | 2,675.24 | 0.00 | 5,000.00 | PASS |
| Restored base | 2029 | 0.00 | 0.00 | 4,384.20 | 0.00 | 5,000.00 | PASS |
| Restored base | 2030 | 0.00 | 0.00 | 6,366.96 | 0.00 | 5,000.00 | PASS |

## Statement trace

[Full inputs, opening balances, annual statement rows, valuation components and checks for every run](Lab11_elv-operating-sensitivity-details.json) are retained at full precision. Select a run by its `name` in `cases`; each `rows` entry is one forecast year. `inputs` records all assumptions used for that run.

The following bridge traces revenue growth — lower, FY2030. Expenses and cash outflows are shown as negative amounts. The model's other annual rows remain available in the linked details.

| Component | FY2030 ($m) |
|---|---:|
| Revenue | 218,148.70 |
| Benefit expense | -162,626.70 |
| Product costs | -23,235.99 |
| Gross profit | 32,286.01 |
| Cash operating expense | -22,600.21 |
| PP&E D&A expense | -1,062.43 |
| Intangible amortization expense | -628.00 |
| Operating profit | 7,995.37 |
| Investment income | 1,796.00 |
| Interest | -1,227.00 |
| Tax | -2,055.45 |
| Net income | 6,508.92 |
| PP&E D&A addback | 1,062.43 |
| Intangible amortization addback | 628.00 |
| Increase in receivables | -466.36 |
| Increase in other working-capital assets | -115.69 |
| Increase in claims payable | 367.53 |
| CFO | 7,984.84 |
| Capex | -1,116.00 |
| Scheduled net debt repayment | -1,000.00 |
| FCFE | 5,868.84 |

## Base restored and rerun

PASS: the final run uses the original base inputs. All annual statement rows, checks, valuation components and outputs exactly match the initial base before rounding; the source model's assumptions remain unchanged.

FY2030 operating profit: **$8,479.57 million**; FY2030 FCFE: **$6,116.77 million**; value per opening share: **365.24 USD/share**.

Rerun: `python3 lab10_proforma_elv.py --operating-sensitivity`.

## V — Verification evidence

Base inputs and all five annual statement rows match exactly before and after the analysis. This is stricter than the display tolerance of 0.01 in each output unit. Accounting gap tolerance is $0.000001 million.

Selected result: revenue growth changes from 3% to 2% in every forecast year. The JSON `changed_inputs` list contains only `growth`; margin remains 14.3%, 14.5%, 14.7%, 14.8%, 14.8%, and every other independent input equals base. The full linked forecast, including receivables and medical claims payable, was recalculated.

| Output | Base | Changed result | Changed minus base |
|---|---:|---:|---:|
| FY2030 operating profit ($m) | 8,479.567201 | 7,995.371558 | -484.195643 |
| FY2030 FCFE ($m) | 6,116.765964 | 5,868.838973 | -247.926991 |
| Value/share ($) | 365.238954 | 354.199999 | -11.038955 |

Accounting/funding checks pass for 6/6 sensitivity runs. The annual evidence and any failure reasons appear above. Changes and spans are calculated from full-precision results retained in JSON.

## E — Comparison over these ranges

- FY2030 operating profit ($m): **Revenue growth** has the largest span, **987.56**, over these ranges.
- FY2030 FCFE ($m): **Blended gross margin** has the largest span, **515.51**, over these ranges.
- Value/share ($): **Blended gross margin** has the largest span, **27.16**, over these ranges.

The revenue-growth range is 2%–4% annually; the margin range spans 1.0 percentage point in each forecast year. The ordering depends on these chosen ranges and the model structure; it does not establish inherent driver importance or support ranking unlike companies by raw dollar changes.

### Causal evidence from the higher cases

The bridge below shows signed changes in FY2030 cash flow relative to base. Higher revenue requires more receivables and other working-capital assets, partly offset by more claims payable. Higher margin changes direct costs and claims payable while revenue-based receivables stay unchanged. These linked cash effects help explain why the operating-profit span and FCFE span can identify different drivers.

| FY2030 change ($m) | Growth higher minus base | Margin higher minus base |
|---|---:|---:|
| Operating profit | +503.37 | +343.58 |
| Net income after tax | +382.56 | +261.12 |
| PP&E D&A addback | +0.00 | +0.00 |
| Intangible amortization addback | +0.00 | +0.00 |
| Cash effect of receivables | -280.67 | +0.00 |
| Cash effect of other working-capital assets | -69.63 | +0.00 |
| Cash effect of claims payable | +221.20 | -3.36 |
| Cash effect of capex | +0.00 | +0.00 |
| Cash effect of debt repayment | +0.00 | +0.00 |
| FCFE | +253.46 | +257.76 |

Value/share also reflects cash-flow changes in all five years and the terminal cash flow, with discount rates unchanged.

## Personal records still to complete

The actual locked prediction and partner exchanges have not been provided. No pre-run timestamp, prediction error, partner confirmation, or personal valuation conclusion is claimed. Use [the personal record](Lab11_elv-sensitivity-personal-record.md) to attach the actual result to the original locked record and record the exchanges after they occur.
