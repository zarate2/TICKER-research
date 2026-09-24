# Lab 09 — Generated Statements and Checks

Generated from `proforma.py`. USD millions except per-share values.

## ELV — default case

```text
LAB 09 — ELV — FY2025-end model origin; five year-end forecasts
Forecasts are assumptions, not reported results. Units: USD millions.

INCOME STATEMENT
USD millions                               FY2026E      FY2027E      FY2028E      FY2029E      FY2030E
Operating revenue                        203,511.5    209,616.9    215,905.4    222,382.5    229,054.0
Direct costs                            -174,409.4   -179,222.4   -184,167.3   -189,469.9   -195,154.0
Gross profit (model subtotal)             29,102.1     30,394.4     31,738.1     32,912.6     33,900.0
SG&A / cash operating expense            -20,720.7    -21,519.3    -22,343.6    -23,038.8    -23,730.0
Depreciation / PP&E D&A proxy               -918.0       -956.8       -988.1     -1,013.2     -1,033.3
Intangible amortization                     -628.0       -628.0       -628.0       -628.0       -628.0
Impairment                                     0.0          0.0          0.0          0.0          0.0
Operating income (after D&A)               6,835.4      7,290.3      7,778.4      8,232.6      8,508.7
Normalized investment income               1,796.0      1,796.0      1,796.0      1,796.0      1,796.0
Interest on opening balances              -1,402.0     -1,358.3     -1,314.5     -1,270.8     -1,227.0
Pretax income                              7,229.4      7,728.1      8,259.9      8,757.9      9,077.7
Tax                                       -1,735.1     -1,854.7     -1,982.4     -2,101.9     -2,178.6
Net income                                 5,494.4      5,873.3      6,277.5      6,656.0      6,899.0

BALANCE SHEET
USD millions                               FY2026E      FY2027E      FY2028E      FY2029E      FY2030E
Cash                                       9,979.9     10,842.7     12,129.3     13,829.8     15,805.6
Receivables                               22,188.3     22,853.9     23,539.5     24,245.7     24,973.1
PP&E                                       4,877.0      5,036.2      5,164.1      5,266.9      5,349.6
Investments                               38,584.0     38,584.0     38,584.0     38,584.0     38,584.0
Intangibles                               10,572.0      9,944.0      9,316.0      8,688.0      8,060.0
Other assets                              36,158.3     36,323.4     36,493.5     36,668.7     36,849.2
TOTAL ASSETS                             122,359.4    123,584.2    125,226.4    127,283.1    129,621.4
Medical claims payable                    17,589.1     18,074.5     18,573.2     19,107.9     19,681.2
Debt                                      31,046.0     30,046.0     29,046.0     28,046.0     27,046.0
Revolver                                       0.0          0.0          0.0          0.0          0.0
Other liabilities                         28,338.0     28,338.0     28,338.0     28,338.0     28,338.0
TOTAL LIABILITIES                         76,973.1     76,458.5     75,957.2     75,491.9     75,065.2
Common shareholders' equity               45,242.4     46,981.7     49,125.2     51,647.2     54,412.2
Noncontrolling interests                     144.0        144.0        144.0        144.0        144.0
TOTAL LIABILITIES + EQUITY               122,359.4    123,584.2    125,226.4    127,283.1    129,621.4

CASH FLOW STATEMENT
USD millions                               FY2026E      FY2027E      FY2028E      FY2029E      FY2030E
Net income                                 5,494.4      5,873.3      6,277.5      6,656.0      6,899.0
Depreciation                                 918.0        956.8        988.1      1,013.2      1,033.3
Amortization                                 628.0        628.0        628.0        628.0        628.0
Impairment                                     0.0          0.0          0.0          0.0          0.0
Increase in receivables                     -646.3       -665.6       -685.6       -706.2       -727.4
Increase in other working capital           -160.3       -165.1       -170.1       -175.2       -180.4
Increase in claims payable                   505.1        485.4        498.7        534.8        573.2
CASH FROM OPERATIONS                       6,738.9      7,112.8      7,536.6      7,950.5      8,225.8
Capex / CASH FROM INVESTING               -1,116.0     -1,116.0     -1,116.0     -1,116.0     -1,116.0
Debt repayment                            -1,000.0     -1,000.0     -1,000.0     -1,000.0     -1,000.0
FCFE (before distributions/plug)           4,622.9      4,996.8      5,420.6      5,834.5      6,109.8
Buybacks                                  -2,605.0     -2,605.0     -2,605.0     -2,605.0     -2,605.0
Dividends                                 -1,529.0     -1,529.0     -1,529.0     -1,529.0     -1,529.0
Revolver draw / (repayment)                    0.0          0.0          0.0          0.0          0.0
CASH FROM FINANCING                       -5,134.0     -5,134.0     -5,134.0     -5,134.0     -5,134.0
CHANGE IN CASH                               488.9        862.8      1,286.6      1,700.5      1,975.8
Opening cash                               9,491.0      9,979.9     10,842.7     12,129.3     13,829.8
Closing cash                               9,979.9     10,842.7     12,129.3     13,829.8     15,805.6

CHECKS
USD millions                               FY2026E      FY2027E      FY2028E      FY2029E      FY2030E
Assets - liabilities - equity                  0.0          0.0          0.0          0.0          0.0
Cash above minimum                           488.9      1,351.7      2,638.3      4,338.8      6,314.6
All five years: balance, minimum cash, revolver limit and cash reconciliation PASS.

EQUITY VALUATION: cost of equity 10.00%; terminal growth 2.50%
PV of 2026-2030 FCFE: 20,183.53
2031 normalized FCFE: 7,287.53
Terminal value at FY2030 end: 97,167.07
PV of terminal value: 60,333.10
Equity value: 80,516.64
Share of value after 2030: 74.93%
Opening shares (millions): 220.723898
Value per share: $364.78
FCFE is discounted directly: no second cash addition or debt subtraction.
```

## ABG — required known answer

```text
LAB 09 — ABG — FY2025-end model origin; five year-end forecasts
Forecasts are assumptions, not reported results. Units: USD millions.

INCOME STATEMENT
USD millions                               FY2026E      FY2027E      FY2028E      FY2029E      FY2030E
Operating revenue                         18,323.0     18,652.8     18,988.5     19,330.3     19,678.3
Direct costs                             -15,198.9    -15,472.5    -15,751.0    -16,034.5    -16,323.1
Gross profit (model subtotal)              3,124.1      3,180.3      3,237.5      3,295.8      3,355.1
SG&A / cash operating expense             -2,077.5     -2,083.1     -2,088.2     -2,125.8     -2,164.1
Depreciation / PP&E D&A proxy                -82.4        -86.9        -91.3        -95.5        -99.7
Intangible amortization                        0.0          0.0          0.0          0.0          0.0
Impairment                                  -120.0       -120.0       -120.0       -120.0       -120.0
Operating income (after D&A)                 844.2        890.3        938.1        954.5        971.4
Normalized investment income                   0.0          0.0          0.0          0.0          0.0
Interest on opening balances                -289.0       -282.5       -276.1       -269.7       -263.4
Pretax income                                555.2        607.8        661.9        684.8        708.0
Tax                                         -141.6       -155.0       -168.8       -174.6       -180.5
Net income                                   413.6        452.8        493.1        510.1        527.5

BALANCE SHEET
USD millions                               FY2026E      FY2027E      FY2028E      FY2029E      FY2030E
Cash                                         101.8        206.9        356.6        527.5        719.8
Inventory                                  2,174.7      2,213.8      2,253.7      2,294.2      2,335.5
Receivables                                    0.0          0.0          0.0          0.0          0.0
PP&E                                       3,238.0      3,401.1      3,559.8      3,714.3      3,864.6
Investments                                    0.0          0.0          0.0          0.0          0.0
Intangibles                                    0.0          0.0          0.0          0.0          0.0
Other assets                               6,254.2      6,136.8      6,019.5      5,902.3      5,785.0
TOTAL ASSETS                              11,768.7     11,958.6     12,189.6     12,438.2     12,704.9
Floor-plan loans                           2,063.9      2,101.0      2,138.9      2,177.4      2,216.5
Medical claims payable                         0.0          0.0          0.0          0.0          0.0
Debt                                       3,422.0      3,272.0      3,122.0      2,972.0      2,822.0
Revolver                                       0.0          0.0          0.0          0.0          0.0
Other liabilities                          2,127.5      2,127.5      2,127.5      2,127.5      2,127.5
TOTAL LIABILITIES                          7,613.4      7,500.5      7,388.4      7,276.9      7,166.0
Common shareholders' equity                4,155.3      4,458.1      4,801.2      5,161.4      5,538.9
Noncontrolling interests                       0.0          0.0          0.0          0.0          0.0
TOTAL LIABILITIES + EQUITY                11,768.7     11,958.6     12,189.6     12,438.2     12,704.9

CASH FLOW STATEMENT
USD millions                               FY2026E      FY2027E      FY2028E      FY2029E      FY2030E
Net income                                   413.6        452.8        493.1        510.1        527.5
Depreciation                                  82.4         86.9         91.3         95.5         99.7
Amortization                                   0.0          0.0          0.0          0.0          0.0
Impairment                                   120.0        120.0        120.0        120.0        120.0
Increase in inventory                        -38.9        -39.1        -39.8        -40.6        -41.3
Increase in receivables                        0.0          0.0          0.0          0.0          0.0
Increase in other working capital             -2.6         -2.6         -2.7         -2.7         -2.8
Increase in claims payable                     0.0          0.0          0.0          0.0          0.0
CASH FROM OPERATIONS                         574.6        617.9        661.9        682.4        703.1
Capex / CASH FROM INVESTING                 -250.0       -250.0       -250.0       -250.0       -250.0
Increase in floor-plan loans                  36.9         37.1         37.8         38.5         39.2
Debt repayment                              -150.0       -150.0       -150.0       -150.0       -150.0
FCFE (before distributions/plug)             211.4        255.1        299.7        320.9        342.3
Buybacks                                    -150.0       -150.0       -150.0       -150.0       -150.0
Dividends                                      0.0          0.0          0.0          0.0          0.0
Revolver draw / (repayment)                    0.0          0.0          0.0          0.0          0.0
CASH FROM FINANCING                         -263.1       -262.9       -262.2       -261.5       -260.8
CHANGE IN CASH                                61.4        105.1        149.7        170.9        192.3
Opening cash                                  40.4        101.8        206.9        356.6        527.5
Closing cash                                 101.8        206.9        356.6        527.5        719.8

CHECKS
USD millions                               FY2026E      FY2027E      FY2028E      FY2029E      FY2030E
Assets - liabilities - equity                  0.0          0.0          0.0          0.0          0.0
Cash above minimum                            76.8        181.9        331.6        502.5        694.8
All five years: balance, minimum cash, revolver limit and cash reconciliation PASS.

EQUITY VALUATION: cost of equity 10.00%; terminal growth 2.50%
PV of 2026-2030 FCFE: 1,059.87
2031 normalized FCFE: 504.59
Terminal value at FY2030 end: 6,727.85
PV of terminal value: 4,177.46
Equity value: 5,237.34
Share of value after 2030: 79.76%
Opening shares (millions): 17.951349
Value per share: $291.75
FCFE is discounted directly: no second cash addition or debt subtraction.
```

## Verification

```text
PASS: all ten ABG endpoint values and $291.75/share match the handout.
PASS: broken-cash valuation refused: FY2026E: assets - liabilities - equity gap = -61.4
PASS: ELV statements balance and cash reconciles in every year.
PASS: temporary cash shortfall draws revolver; later surplus repays it first.
PASS: inadequate financing refused: FY2026E: cash below minimum; gap = -923.2
PASS: terminal growth equal to cost of equity refused.
```
