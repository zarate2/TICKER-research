# Session 6 — What Has to Be True

**Elevance Health, Inc. (NYSE: ELV)** · **Valuation date: September 10, 2026**

The required FCFF model estimates **$537.84 per diluted share**, versus the latest verified quote of **$416.14**. Value/price is **1.2925×**, inside the lab's 0.5×–2× band. The sensitivity corners span **$346.14–$1,036.00**. The market target requires a **−4.445219 percentage-point shift** to each forecast growth rate, conditional on the fixed assumptions below. My call remains **watch-defer**, pending operating confirmation.

All monetary amounts are **USD millions**, shares are **millions**, and valuations are **USD per share**, unless explicitly stated otherwise. Reported facts, calculations, and analyst estimates are distinguished throughout. Figures retain full precision in [dcf.py](dcf.py); displayed rounding is not fed back into calculations.

## Sources and period convention

The historical foundation is the latest available annual filing, the **2025 Form 10-K**. I also reviewed the March and June 2026 10-Qs and July guidance. The [company annual-report index](https://ir.elevancehealth.com/annual-reports/) identifies the 2025 10-K; [quarterly results](https://ir.elevancehealth.com/financials/quarterly-results/default.aspx) and the SEC documents below provide the newer information. All links were accessed September 10, 2026. Page references mean the filing's printed pages; named tables and notes are also supplied for HTML navigation.

| Reference | Direct source | Exact sections used |
|---|---|---|
| K | [2025 SEC Form 10-K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm) | Cash-flow statement p. 74; Item 7 results and liquidity; Note 2 accounting policies p. 77; Note 4 investments, securities deposits/lending p. 93; Note 13 Debt; Note 19 EPS p. 125; Note 21 Statutory Information pp. 128–129 |
| Q1 | [March 2026 SEC Form 10-Q](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000043/elv-20260331.htm) | Cash-flow statement p. 6; Item 2 liquidity; Note 10, CMS Notice p. 26 |
| Q2 | [June 2026 SEC Form 10-Q](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm) | Balance sheets pp. 2–3; cash flows p. 6; Notes 6 Fair Value, 7 Income Taxes, 9 Debt p. 24, 10 CMS Notice p. 26, 12 EPS p. 30; Item 2 Financial Condition p. 49 |
| G | [July 15, 2026 earnings release, SEC Exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000058/a2q2026elvearningsrelease.htm) | Opening highlights and CEO outlook p. 1; enterprise highlights p. 2; segment discussion pp. 3–4; membership table p. 7 |
| L | [Lab 06 assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-03/lab-06-sensitivity-and-reverse-dcf.md) | “R,” “V,” “E,” and “Your conditional call” |

**Timing:** FY2025 actuals establish the history. The active starting FCFF is a separately labeled **FY2026 annual run-rate estimate**, not a reported 2025 number or a half-year amount. Years 1–5 are five full forward twelve-month periods ending **September 10, 2027–2031**. Each entire year's cash flow is discounted at that period's end, using exponents 1–5. This preserves the course's year-end convention without discounting already-earned 2026 cash flows as future receipts. Using a fiscal-year estimate as the current run-rate proxy sacrifices seasonal and stub-period precision; the model does not claim to be a calendar-year 2026–2030 DCF. Cash and debt use the same latest balance-sheet date, June 30, 2026; the diluted denominator is the quarter ending that date. These are the latest reported snapshots, not September 10 balances.

### Market target

| Input | Value/unit | Quote date and time | Classification and source locator |
|---|---:|---|---|
| Reverse-DCF target | **$416.14/share** | **September 10, 2026, 4:51 p.m. EDT (UTC−04:00)** | Observed after-hours snapshot; [Stock Analysis ELV overview](https://stockanalysis.com/stocks/elv/), top quote panel, “After-hours.” Page labels its feed “Real-Time Price”; this saved observation is not continuously live in the script. |
| Regular-session close, context only | $416.54/share | September 10, 2026, 4:00 p.m. EDT | Same page, “At close”; corroborated by [Google Finance](https://www.google.com/finance/quote/ELV:NYSE), “Closed,” 4:00:02 p.m. GMT−4. The later after-hours observation is the active target. |

## The five input groups

### 1. Starting FCFF: history and explicit normalization

| Input | FY2025 value/unit | Status | Direct source and exact locator |
|---|---:|---|---|
| Operating cash flow | 4,290 USD m | Reported, year ended December 31, 2025 | [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Consolidated Statements of Cash Flows p. 74, “Net cash provided by operating activities,” 2025 column |
| Interest **paid** | 1,410 USD m | Reported, FY2025 | [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Note 13 Debt, paragraph beginning “Interest paid on our total outstanding debt” |
| Effective income-tax rate | 15.6% | Reported, FY2025 | [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Item 7 Results of Operations table, “Effective tax rate,” 2025 column |
| Capital expenditures | 1,116 USD m outflow | Reported, FY2025 | [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), cash-flow statement p. 74, “Purchases of property and equipment” |
| Historical FCFF | **4,364.04 USD m** | Calculated, FY2025 | 4,290 + 1,410 × (1 − 0.156) − 1,116 |

This is the lab's FCFF definition, not a vendor's CFO-minus-capex measure. Cash interest differs from interest expense and is sourced from the debt note. Applying an effective tax rate to cash interest is itself an approximation to the usable interest tax shield.

| Active baseline component | Value/unit and period | Status and justification | Direct source/locator |
|---|---|---|---|
| Operating cash flow | 6,000 USD m, FY2026 estimate | Analyst adoption of management's **at least 6,000** guidance floor; not a reported result | [G](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000058/a2q2026elvearningsrelease.htm), p. 1 operating-cash-flow guidance |
| Interest paid | 1,410 USD m, FY2026 estimate | Hold FY2025 cash interest flat; do not relabel interim interest expense as interest paid | [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Note 13 cash-interest paragraph; analyst carry-forward |
| Normalized tax rate | 24.0%, FY2026 and forward | Analyst estimate; close to H1 2026's reported 24.2%, avoiding reliance on 2025's unusually low rate | [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), Note 7 Income Taxes, three/six-month effective-rate discussion |
| Capital expenditures | 1,116 USD m, FY2026 estimate | Hold FY2025 annual PP&E purchases flat. H1 2026 purchases of 522 imply 594 in H2; no assumption that all acquisition spending is capex | [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), p. 74; [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), p. 6 PP&E purchases |
| **Active starting FCFF** | **5,955.60 USD m annual run rate** | Calculated estimate at September 10, 2026 | **6,000 + 1,410 × (1 − 24%) − 1,116 = 5,955.60** |

The normalization adds 1,710 of CFO and removes 118.44 of tax-shield benefit relative to historical FCFF: 4,364.04 + 1,710 − 118.44 = 5,955.60. It does **not** add the 2025 settlement back a second time. Neither the guidance floor nor the interest/capex carry-forwards are guaranteed outcomes.

Historical comparison, with each year's own reported effective rate:

| FY ended December 31 | CFO, USD m | Cash interest, USD m | Tax rate | Capex, USD m | Calculated FCFF, USD m |
|---|---:|---:|---:|---:|---:|
| 2023 | 8,061 | 1,032 | 22.3% | 1,296 | 7,566.864 |
| 2024 | 5,808 | 1,239 | 24.5% | 1,256 | 5,487.445 |
| 2025 | 4,290 | 1,410 | 15.6% | 1,116 | 4,364.040 |

Source for all historical components: [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), p. 74 cash-flow statement, Note 13 cash-interest paragraph, and Item 7 effective-tax-rate row. FCFF is calculated, not a company-reported metric.

### 2. Annual FCFF growth: cash drivers rather than an EPS shortcut

The forecast retains the existing script's explicit CFO/capex assumptions, now documented. All five rows below are **analyst estimates made September 10, 2026**. Annual cash interest remains 1,410 and tax remains 24%, so the annual after-tax addback is 1,071.60. Growth is calculated from successive FCFF levels; editing CFO or capex in the input block updates the growth vector.

| Forward year ending | CFO, USD m | CFO growth | Capex, USD m | FCFF, USD m | FCFF growth | Rationale and evidence locator |
|---|---:|---:|---:|---:|---:|---|
| Sep. 10, 2027 | 6,300 | 5.0000% | 1,150 | 6,221.60 | **4.466385%** | Modest pricing/cash recovery from the guidance baseline; spending remains elevated. [G](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000058/a2q2026elvearningsrelease.htm), pp. 1–3 outlook and enterprise/Health Benefits commentary. |
| Sep. 10, 2028 | 6,650 | 5.5556% | 1,200 | 6,521.60 | **4.821911%** | A second year of rate catch-up and Carelon execution adds 350 CFO, with 50 more capex. [G](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000058/a2q2026elvearningsrelease.htm), pp. 3–4 segment discussion; recovery magnitude is my estimate. |
| Sep. 10, 2029 | 7,000 | 5.2632% | 1,250 | 6,821.60 | **4.600098%** | Another 350 CFO improvement, conditional on cost management converting to cash, rather than additional payable buildup. [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), Item 2 liquidity and cash-flow statement operating-liability rows. |
| Sep. 10, 2030 | 7,300 | 4.2857% | 1,300 | 7,071.60 | **3.664829%** | Recovery slows: 300 CFO improvement, 50 extra capex; competition and regulation limit extrapolation. [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Item 1A pricing/regulatory risks; analyst fade assumption. |
| Sep. 10, 2031 | 7,550 | 3.4247% | 1,350 | 7,271.60 | **2.828214%** | 250 CFO improvement, 50 extra capex; growth approaches the 2.5% terminal assumption. [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Item 7 historical liquidity; analyst maturity assumption. |

For example, Year 1 FCFF = 6,300 + 1,071.60 − 1,150 = 6,221.60; growth = 6,221.60 / 5,955.60 − 1. These forecasts are cash-flow judgments supported by the cited operating context; the sources do not supply these exact forecasts.

The evidence argues against simply extrapolating earnings or first-half cash generation:

- FY2025 CFO declined amid settlement payments, working-capital pressure and lower earnings. [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Item 7 “Liquidity—Year Ended December 31, 2025 Compared to Year Ended December 31, 2024.”
- Q1 2026 CFO was 4,332 versus 1,017 a year earlier; management attributed the increase primarily to working capital. [Q1](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000043/elv-20260331.htm), p. 6 and Item 2 liquidity.
- H1 2026 CFO was 6,245 versus 3,071, including a 4,124 inflow from accounts payable/other liabilities and 1,216 from policy liabilities. Thus, annualizing 6,245 would capitalize temporary financing effects. At the 6,000 guidance floor, H2 CFO could be −245; this is an arithmetic implication of the chosen floor, not new company guidance. [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), p. 6 operating cash-flow rows.
- Q2 benefit-expense ratio was 89.7% versus 88.9%, while operating margin fell to 3.5% from 4.9%. Medical membership was 44.949 million, down 1.5%. Premium repricing can help collections, but claims costs and member losses can offset it. [G](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000058/a2q2026elvearningsrelease.htm), pp. 2 and 7.
- July guidance raised adjusted EPS to at least $27 and discussed at least 12% adjusted EPS growth in 2027. That is **not** the FCFF growth assumption: buybacks, tax items, noncash adjustments, claims-payment timing and reinvestment separate EPS from total cash flow. [G](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000058/a2q2026elvearningsrelease.htm), p. 1.
- Q1's threatened CMS sanctions were superseded by the July 13 closure of that enforcement process. Q2 still reported a 593 accrual after a 342 payment against the original 935 exposure. The forecast assumes no repeat of the original charge but does not assume the remaining cash obligation disappears. [Q1](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000043/elv-20260331.htm) and [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), Note 10 “CMS Notice,” p. 26.

The projected five-year FCFF CAGR is **4.0737%**. Year 5 CFO of 7,550 remains below 2023's 8,061 despite nominal growth. Capex rises to 1,350, above all three historical years. This is a recovery case with reinvestment, not a claim that historical cash conversion has stabilized. Acquisition spending and incremental required regulatory capital are not separately forecast; this is a material limitation.

### 3. WACC estimated from components

| Input | Value/unit | Date/period; status | Direct source and exact locator |
|---|---:|---|---|
| USD risk-free proxy | 4.95% annual | Sep. 10, 2026; observed Treasury par yield | [U.S. Treasury 2026 table](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026), Daily Treasury Par Yield Curve Rates, 09/10/2026 row, **10 Yr** column |
| ELV equity beta | 0.70, unitless | Retrieved Sep. 10, 2026; vendor statistical estimate | [Stock Analysis statistics](https://stockanalysis.com/stocks/elv/statistics/), Stock Price Statistics, **Beta (5Y)** row |
| Equity risk premium | 4.14% annual | Sep. 1, 2026; market-implied estimate | [Damodaran](https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm), “Equity Risk Premiums (Data, Updates and Papers),” trailing 12-month **adjusted payout** estimate |
| Debt coupon anchor | 5.00% annual | Sep. 15, 2025 issuance; reported contractual coupon | [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Note 13, issuance of 1,000 of notes due 2036 |
| Treasury at issuance | 4.05% annual | Sep. 15, 2025; observed | [Treasury 2025 table](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2025), 09/15/2025 row, **10 Yr** column |
| Debt spread proxy | 0.95 percentage points | Analyst calculation; held constant to valuation date | 5.00% − 4.05%; sources in preceding two rows |
| Pretax cost of debt | 5.90% annual | Sep. 10, 2026 estimate | 4.95% + 0.95%; not an observed bond yield |
| Debt tax rate / after-tax cost | 24.0% / 4.484% annual | Normalized estimate / calculated | Tax justification in group 1; 5.90% × (1 − 24%) |
| Basic shares for capital weights only | 216.841146 m | June 30, 2026; reported point-in-time balance | [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), balance sheet p. 3, common-stock issued/outstanding row; convert 216,841,146 shares to millions |
| Equity market-value proxy | 90,236.274496 USD m | Sep. 10 price × latest reported basic shares; calculated | 416.14 × 216.841146; quote above and Q2 balance sheet |
| Debt weight balance | 31,044 USD m | June 30, 2026 carrying value; book approximation | [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), Note 9 total long-term debt; zero short-term borrowings |
| Equity / debt weights | 74.403092% / 25.596908% | Calculated | E/(E+D) and D/(E+D), using the two preceding balances |
| Cost of equity | **7.848% annual** | Calculated CAPM estimate | 4.95% + 0.70 × 4.14% |
| **Base WACC** | **6.98692002% annual** | Calculated valuation-date estimate | 74.403092% × 7.848% + 25.596908% × 4.484% |

The ERP is a contemporary forward-looking US market estimate, appropriate to predominantly USD cash flows; it is not the class's arbitrary training WACC. I use the ERP convention paired with unadjusted Treasury yields, without separately removing a US default spread. Beta is a backward-looking vendor estimate; its full sampling/regression specification was not independently verified. The coupon-minus-Treasury spread is a simple refinancing-cost proxy: coupon need not equal issuance yield, and credit spreads may have changed. Actual September 10 marginal borrowing yield remains unverified.

Book debt is an explicit simplification, not an assertion that debt trades at par. Q2 Note 6, “Financial Instruments Not Carried at Fair Value,” discloses **29,068** fair value for the **31,044** carrying-value notes. I retain the existing book-debt convention consistently for the bridge and approximate capital weights. The equity-weight calculation uses a current price with June shares, so intervening repurchases are another approximation. The lab's diluted EPS denominator is used only for value/share, as required. WACC is computed once and held fixed during reverse DCF; it does not change with each trial modeled price.

### 4. Terminal growth

| Input | Value/unit | Period/status | Source and rationale |
|---|---:|---|---|
| Perpetual nominal FCFF growth | **2.50% annual** | Year 6 onward; analyst estimate as of Sep. 10, 2026 | [Federal Reserve inflation FAQ](https://www.federalreserve.gov/faqs/economy_14400.htm), longer-run 2% PCE inflation objective; add approximately 0.5% real cash growth as my mature-business assumption |

This is deliberately slower than a sustained recovery rate and compatible with nominal USD cash flows. It is not a Fed forecast for ELV or a claim that current inflation is 2%. A mature insurer cannot indefinitely outgrow its economic base without additional capital. **2.5% < 6.98692002%**, and even the grid's 3.5% maximum remains below its 5.98692002% minimum WACC.

### 5. Cash, interest-bearing debt, and diluted shares

| Input | Value/unit | Period/status | Direct source and exact locator |
|---|---:|---|---|
| Consolidated cash, context only | 10,232 USD m | June 30, 2026; reported | [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), balance sheet p. 2, Cash and cash equivalents |
| **Selected cash bridge** | **2,062 USD m** | June 30, 2026; reported parent cash/equivalents/**investments**, used as an estimated excess-liquidity proxy | [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), Item 2 Financial Condition p. 49, parent funds available for general corporate use |
| Long-term debt excluding current maturities | 30,669 USD m | June 30, 2026; reported | [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), balance sheet p. 3; Note 9 p. 24 |
| Current maturities | 375 USD m | June 30, 2026; reported | Same balance sheet and Note 9 current-portion row |
| Short-term borrowings | 0 USD m | June 30, 2026; reported | Note 9 short-term-borrowing table: revolver, commercial paper, FHLB advances all zero |
| **Debt deducted** | **31,044 USD m** | June 30, 2026; calculated/reconciled carrying value | 30,669 + 375 + 0; Note 9 separately reconciles 31,019 senior unsecured notes + 25 surplus note |
| **Diluted weighted-average shares** | **217.9 m shares** | Three months ended June 30, 2026; reported | [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), Note 12 Shareholders' Earnings per Share p. 30: basic 217.0 + dilution 0.9 |

The denominator is the actual EPS-note quarterly diluted average, not the cover-page basic count or the prior lab's estimate of 217.7. Q2 Note 12 also reports H1 diluted shares of 219.1; K Note 19 reports FY2025 diluted shares of 224.6. Those represent different averaging periods and are not combined. The most recent quarter is selected to approximate current dilution, then held fixed; future repurchases/dilution are not forecast.

## Insurer cash and capital: what the bridge does and misses

The cash label in the script means **selected parent liquidity**, including investments; it is not a claim that the parent has 2,062 of cash alone. Consolidated assets are not all distributable:

| Reported item inspected | Amount/date | Treatment and source locator |
|---|---|---|
| Customer-benefit accounts and cash deposited for regulatory/contractual requirements | 348 USD m, Dec. 31, 2025 | Included in consolidated cash, not a separate “restricted cash” line. Do not assume all cash is free. [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Note 2 “Cash and Cash Equivalents,” p. 77. A June update to this specific amount was not located. |
| Securities deposited under regulatory requirements | 1,121 USD m, Dec. 31, 2025 | Excluded from the cash add-on. [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Note 4 Investments, regulatory-deposit paragraph p. 93. |
| Required statutory RBC / DMHC tangible net equity | Approximately 9,100 / 1,100 USD m, Dec. 31, 2025 | Capital constraints, not debt and not automatic cash deductions. [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Note 21 pp. 128–129; dividend approvals constrain transfers. |
| Fixed maturity investments, current / long-term; equity securities | 25,719 / 1,259 / 1,563 USD m, June 30, 2026 | No separate addition of the consolidated portfolios; subsidiary investments support operations and obligations. [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), balance sheet p. 2. |
| Medical claims / other policyholder liabilities / unearned income | 18,463 / 3,463 / 1,640 USD m, June 30, 2026 | Operating obligations, not financing debt. Their cash effects belong in CFO; subtracting all again would double count. [Q2](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000060/elv-20260630.htm), balance sheet p. 3 and cash-flow operating-liability rows. |
| Securities-lending collateral | 2,691 USD m, Dec. 31, 2025 | Matched other-current-asset/liability amounts; no unbacked cash bonus. [K](https://www.sec.gov/Archives/edgar/data/1156039/000115603926000013/elv-20251231.htm), Note 4 “Securities Lending Programs,” p. 93. |

I neither add consolidated investments nor subtract all policyholder liabilities as debt. This retains the lab's **EV + selected cash − interest-bearing debt** bridge. Parent liquidity is still an imperfect excess-cash proxy: debt service and subsidiary capital needs compete for it, and returns on parent investments may already contribute to modeled CFO. The exact distributable surplus and potential overlap are **unresolved**. Setting the cash addition to zero, with everything else fixed, would reduce value by **$9.46** to **$528.38**. Adding all consolidated cash instead would increase value by **$37.49**; I do not adopt that treatment.

The required model does not deduct incremental regulatory capital, separately value insurance float, or forecast securities purchases needed to support growth. Consequently, consolidated FCFF need not equal cash distributable to shareholders. Debt and operating liabilities also interact more closely for insurers than for industrial firms. This limits confidence in the absolute value; it does not justify changing the assigned formula.

The exact lab bridge also omits noncontrolling interests. Q2's balance-sheet carrying value is 139; subtracting that as an additional approximation would reduce value by **$0.64/share**. It is disclosed here rather than silently changing the requested bridge. Lease cash costs remain in CFO; no separate lease-debt capitalization adjustment is made.

## Base valuation

For annual forecast rate `g[t]`, `FCFF[t] = FCFF[t−1] × (1 + g[t])`. Each cash flow is discounted by `(1 + WACC)^t`. Positive starting FCFF permits a growth model; an explicit loss-recovery parameter is unnecessary.

| Year | FCFF, USD m | Present value, USD m |
|---|---:|---:|
| 1 | 6,221.6000 | 5,815.2903 |
| 2 | 6,521.6000 | 5,697.6109 |
| 3 | 6,821.6000 | 5,570.5002 |
| 4 | 7,071.6000 | 5,397.5285 |
| 5 | 7,271.6000 | 5,187.7203 |

| Calculation | Result |
|---|---:|
| PV of explicit FCFF | 27,668.6503 USD m |
| Terminal value = 7,271.60 × 1.025 / (0.06986920022785194 − 0.025) | 166,113.7253 USD m |
| PV of terminal value = TV / (1 + WACC)^5 | 118,509.2071 USD m |
| Enterprise value = explicit PV + terminal PV | **146,177.8574 USD m** |
| Equity = EV + 2,062 − 31,044 | **117,195.8574 USD m** |
| Equity / 217.9 diluted shares | **$537.84/share** |

These are model calculations, not reported company values. The first twelve printed lines preserve the course format: five FCFFs, five PVs, terminal value and terminal PV. Enterprise value, the equity bridge and per-share value follow immediately.

## Sensitivity grid

Only WACC and terminal growth change. The editable lists are base ±1 percentage point. Every other input, including the cash forecast and share count, stays fixed.

| WACC \\ terminal growth | 1.50% | 2.50% | 3.50% |
|---|---:|---:|---:|
| 5.986920% | $562.00 | $731.03 | $1,036.00 |
| 6.986920% | $434.38 | **$537.84 — base** | $700.64 |
| 7.986920% | $346.14 | $415.09 | $514.77 |

The **valid corner range is $346.14–$1,036.00**; all nine ELV cells are valid. Moving down raises WACC and lowers value; moving right raises perpetual growth and increases value. A cell with terminal growth ≥ WACC prints `INVALID`, because its perpetuity is not economically admissible. The corner range is a scenario range, not a statistical confidence interval.

## Reverse DCF: what the price requires

Solve for a single decimal shift `s` added to **each** of the five base FCFF growth rates. This is an additive percentage-point shift, not multiplying all rates by the same percentage. The underlying CFO/capex construction justifies the base rates; the reverse scenario adjusts aggregate FCFF growth, without claiming to identify a unique CFO/capex combination.

| Solver input or output | Value |
|---|---|
| Target | $416.14, September 10, 2026, 16:51 EDT (UTC−04:00), after-hours snapshot; [quote panel](https://stockanalysis.com/stocks/elv/) |
| Editable initial bracket | −5.00 to +10.00 percentage points |
| Price at −5 pp / +10 pp | $402.338481 / $895.062226 |
| Bracket check | Target lies between endpoints; every shifted annual rate exceeds −100% |
| Solved uniform shift | **−4.445219 percentage points** |
| Implied growth, Years 1–5 | **0.021166%, 0.376692%, 0.154880%, −0.780389%, −1.617004%** |
| Implied Year 5 FCFF | 5,845.7466 USD m |
| Implied five-year FCFF CAGR | **−0.3717%** |
| Modeled price at solution | **$416.14000000** |
| Modeled minus target | Approximately **−$0.0000000009**; absolute error < $0.00000001 |
| Held fixed numerically | Starting FCFF **5,955.60**; WACC **6.98692002%**; terminal growth **2.50%**; cash **2,062**; debt **31,044**; diluted shares **217.9**; five annual year-end periods |

Bisection halves a verified bracket until the absolute price error is ≤1e−8 dollars, with a 200-iteration cap. Invalid growth brackets and unreachable prices produce explicit errors; the code never widens the bracket or presents an unreachable endpoint as a solution. A target exactly at an endpoint is a legitimate solution and is tested separately.

At this WACC, the price is consistent with roughly flat-to-declining aggregate FCFF instead of the forecast's moderate recovery. But that conclusion is **conditional**: the grid shows that raising WACC by one percentage point, at the same terminal growth, produces **$415.09**, close to the target without reducing the base growth path. The reverse result is one assumption set consistent with price, not proof of mispricing or a direct observation of investors' beliefs.

## Reasonableness, uncertainty, and conditional call

**$537.84296 / $416.14 = 1.2925×**, inside **0.5×–2×**, with modeled upside of **29.25%**. I have not adjusted assumptions to hit that band. The range includes both values below price and values far above it. **81.07% of enterprise value comes from terminal value**, making the discount-rate/terminal-growth spread critical.

**The input I distrust most is WACC, especially the 0.70 beta-based cost of equity.** Historical market covariance may understate prospective Medicaid repricing, medical-cost, CMS and cash-distribution risk. The debt spread is also a proxy. A one-point WACC change erases almost all apparent upside; therefore a numerically precise CAPM estimate does not support equal precision in intrinsic value. The guidance-based starting FCFF is the next major uncertainty because temporary liability movements can inflate CFO.

**Initiate if the share price is at or below $430 and the next two reported quarters each show a benefit-expense ratio below 89.7% and no year-over-year deterioration, while management maintains annual operating-cash-flow guidance of at least 6,000 USD m; otherwise watch-defer.** The $430 threshold is an analyst decision rule, approximately a 20% discount to the model value, not a sourced fair-value fact. At the current $416.14 snapshot the price condition is met; the two-quarter operating confirmation is not yet established.

**Monitor ELV's quarterly benefit-expense ratio**, comparing both the absolute level and the same quarter last year to reduce seasonal distortion. Sustained improvement would support the forecast's pricing-to-cash recovery; deterioration would challenge it even though the reverse DCF currently implies a lower growth path. Recalculate the model when guidance, the capital bridge or WACC changes instead of mechanically retaining the $430 trigger.

**Unresolved, without blocking the arithmetic:** exact distributable parent surplus; updated customer/regulatory cash restrictions after December 2025; future regulatory-capital requirements and acquisition outlays; realized FY2026 cash interest/capex; the September 10 marginal bond yield and full beta regression details; September 10 balance-sheet/share balances. These are disclosed limitations or explicit estimates, not class-number substitutions. No required numerical model result is blocked, but the results are conditional on those estimates.

## Implementation and verification

Inspected `dcf.py`, `elv_dcf.py`, `Lab 5.md`, `LAB 4.md`, `9-1-2026.md`, and the September 3 company report before finalizing. Existing prior work is preserved. The earlier separate `elv_dcf.py` is an archived prior exercise, not a dependency or a Session 6 deliverable. Session 6 requires only **dcf.py and this Markdown report**. The active input block and twelve-line course output remain; historical inputs, current quote, period labels and additional validation visibility were added. No quiz was submitted and nothing was published.

Run from this folder:

```sh
python dcf.py
```

This prints ELV's base calculation, sensitivity grid and reverse DCF in one run. There are no external packages or network calls at runtime. Assumptions, grids, bounds and price tolerance are editable at the top. For the isolated calculation checks:

```sh
python dcf.py --check
```

**Environment detail:** this Mac exposes `/usr/bin/python3` but no bare `python` command. Both runs passed under `python3`; the exact course commands were also verified with a temporary shell function mapping `python` to `python3`. In a fresh terminal here, run `python3 dcf.py`, or enter `function python() { python3 "$@"; }` once and then use `python dcf.py`. No shell startup file or system Python installation was changed.

### Training-only check — not ELV inputs or valuation

The class fixture exists only inside `self_test()` and never overwrites the active ELV configuration: FCFF 100; growth 8%, 6%, 5%, 4%, 3%; WACC 10%; terminal growth 3%; cash 50; debt 300; shares 50. All nine rounded prices matched the assignment:

| Training WACC \\ terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | 28.60 | 32.94 | 39.02 |
| 10% | 24.36 | 27.50 | 31.69 |
| 11% | 21.06 | 23.41 | 26.44 |

The training $30 target solved to **+1.777948 pp**, matching approximately +1.78 pp. All original twelve base outputs also passed to their printed four-decimal precision. These are calculation checks only.

Additional checks passed: terminal growth equal to and above WACC returned invalid cells; a $1,000,000 unreachable training target returned “No solution”; a bracket reaching −100% annual growth was rejected; a genuine endpoint solution was accepted. ELV-specific output checks confirmed the marked central cell, monotonic grid directions, $346.14–$1,036.00 corners, reconciliation of enterprise/equity values, and reverse-price residual below tolerance. The final default run uses ELV throughout.
