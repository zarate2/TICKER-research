# Lab 08 — Calculation Output

Lab 08 verification output — generated September 17, 2026

```text
$ python3 lab08_comps.py
LAB 08 — ELEVANCE HEALTH P/E COMPARISON
Valuation date: 2026-09-10; regular-session closing prices, USD/share.
FY2025 total GAAP diluted EPS; all annual releases public before valuation date.
Sources and policy qualifications: lab-08-elv.md
Target price: $416.54; EPS: $25.21
Target: Elevance Health (ELV)
Target observed P/E: 16.522808x
UNH (QUALIFY) P/E: 29.348450x
CI (QUALIFY) P/E: 12.665014x
2 valid peers
Peer minimum P/E: 12.665014x
Peer median P/E: 21.006732x
Peer maximum P/E: 29.348450x
Target implied minimum: $319.28
Target implied median: $529.58
Target implied maximum: $739.87

LEAVE ONE VALID PEER OUT
Remove UNH: 1 remaining; reference estimate, no range; median P/E 12.665014x; target price $319.28; change -210.29 USD/share
Remove CI: 1 remaining; reference estimate, no range; median P/E 29.348450x; target price $739.87; change +210.29 USD/share

Implied price = peer P/E x target diluted EPS. No cash/debt adjustment.
Display rounding is never used in subsequent calculations.

$ python3 dcf.py
FCFF Year 1: 6221.6000
FCFF Year 2: 6521.6000
FCFF Year 3: 6821.6000
FCFF Year 4: 7071.6000
FCFF Year 5: 7271.6000
PV of FCFF Year 1: 5815.2903
PV of FCFF Year 2: 5697.6109
PV of FCFF Year 3: 5570.5002
PV of FCFF Year 4: 5397.5285
PV of FCFF Year 5: 5187.7203
Terminal Value at Year 5: 166113.7253
PV of Terminal Value: 118509.2071

ELV BASE VALUATION — USD millions except dollars per diluted share
FY2025 historical FCFF: 4364.0400; active baseline is an FY2026 estimate.
Forecast: five full years ending September 10, 2027-2031; year-end discounting.
Starting FCFF: 5955.6000; WACC: 6.986920%; terminal growth: 2.50%
Forecast growth rates: 4.466385%, 4.821911%, 4.600098%, 3.664829%, 2.828214%
Enterprise Value: 146177.8574
Equity Value = EV + 2062.00 cash - 31044.00 debt: 117195.8574
Value per Diluted Share = Equity / 217.9: $537.84
Value / target price: 1.2925x
PV terminal value / enterprise value: 81.07%

ELV SENSITIVITY — value per diluted share; * = base cell
WACC / terminal            1.50%         2.50%         3.50%
5.986920%                $562.00       $731.03      $1036.00
6.986920%                $434.38      $537.84*       $700.64
7.986920%                $346.14       $415.09       $514.77
Valid corner range: $346.14 to $1036.00
For these positive cash flows, value falls as WACC rises and rises as terminal growth rises.

ELV REVERSE DCF — uniform percentage-point shift to all five growth rates
Target: $416.14; 2026-09-10 16:51 EDT (UTC-04:00), real-time after-hours snapshot
Source: https://stockanalysis.com/stocks/elv/
Fixed: FCFF=5955.6000; WACC=6.98692002%; terminal growth=2.50%; cash=2062.00; debt=31044.00; diluted shares=217.9.
Shift bracket: -5.00 to +10.00 pp
Bracket endpoint prices: $402.338481 to $895.062226
Solved shift: -4.445219 percentage points
Implied growth rates: 0.021166%, 0.376692%, 0.154880%, -0.780389%, -1.617004%
Implied Year 5 FCFF: 5845.7466
Modeled price: $416.14000000; difference from target: $-0.0000000009
Conditional on fixed assumptions; this is not proof of mispricing.
```
