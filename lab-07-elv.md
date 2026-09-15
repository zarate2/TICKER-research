# Lab 07 — P/E comparable-company policy and implied range

**Prior-project company: Elevance Health (NYSE: ELV).** The required calculator uses the reference's frozen Asbury training case. Its numerical results value **ABG**, not ELV. ELV supplies the connection to the previous DCF assignment.

Specification: [CODEX_LAB07_REFERENCE.md](../CODEX_LAB07_REFERENCE.md), especially “COPY THIS INTO CODEX.” No outside data was fetched and no packages were installed.

## Run the calculator

From the `AI in finance` folder:

```sh
python3 lab07_comps.py
```

[lab07_comps.py](lab07_comps.py) is one standalone standard-library file. Target and peer inputs are editable at the top. Prices are December 31, 2024 closes; EPS is FY2024 total GAAP diluted EPS subsequently reported. This is a retrospective exercise, not a contemporaneous trading signal.

## What P/E measures

P/E = share price / diluted earnings per share. A 10× multiple means investors pay $10 for each $1 of annual earnings per share. Dividing price by per-share earnings helps compare businesses of different sizes, provided their earnings periods, accounting measures, growth and risks are reasonably comparable.

For this exercise, implied target price = peer P/E × target EPS. P/E already relates equity price to earnings attributable to shareholders: **do not add cash or subtract debt**.

A lower P/E does not automatically make a stock attractive. Earnings may be temporarily high, future growth may be weaker, or risks may be greater. Negative or zero EPS makes this P/E exercise not meaningful; positive but unusual profits can still make a calculated multiple misleading.

## Peer policy for the frozen ABG case

| Candidate | Decision | Business rationale and limitation |
|---|---|---|
| AutoNation (AN) | USE | The reference identifies franchised vehicle retail and service/parts as important common activities. These are a more useful basis for comparison than an automotive industry label alone. |
| Group 1 Automotive (GPI) | QUALIFY | Include conditionally on the same operating comparison, retaining the reference's qualified-candidate designation. The supplied data do not establish identical business mix, geography, growth, leverage or earnings quality. These dimensions would require review before relying on the multiple for an investment decision. |

Both USE and QUALIFY enter the numerical case if price and EPS are valid. EXCLUDE does not. GPI's higher multiple is not itself a reason to include or exclude it. Leave-one-out analysis measures its influence; it does not establish business comparability.

## Calculated results and validation

| Check | Calculated result | Reference match |
|---|---:|---|
| AutoNation P/E | 10.037825× | PASS |
| Group 1 P/E | 11.450149× | PASS |
| Peer median P/E | 10.743987× | PASS |
| ABG implied range | $215.81–$246.18 | PASS |
| ABG at peer median | $231.00 | PASS |
| Remove GPI: remaining AN estimate | $215.81 | PASS |
| Change from full-peer median estimate | −$15.18 | PASS |

ABG's frozen observed price is $243.03 and its own observed P/E is 11.303721×. Its own multiple is excluded from the peer statistics. The peer-implied range brackets that frozen price, but does not prove fair valuation: the peer selection, earnings quality and market pricing may all be imperfect.

### Leave one peer out

| Removed | Remaining peer | Remaining median P/E | ABG reference estimate | Change from full-peer estimate |
|---|---|---:|---:|---:|
| AN | GPI | 11.450149× | $246.18 | +$15.18 |
| GPI | AN | 10.037825× | $215.81 | −$15.18 |

With two observations, the median is their arithmetic average. Removing the higher-multiple GPI leaves the lower AN multiple, reducing implied ABG value. With one peer, there is a **reference estimate, no range**; no cross-company spread remains. With zero valid peers, there are **no usable peers**. Removing the only valid peer produces **no estimate**.

All computations use unrounded floating-point values. P/E displays six decimals and prices display two. In particular, subtracting displayed $231.00 from displayed $215.81 yields −$15.19; the required calculation subtracts the unrounded estimates and correctly displays **−$15.18**.

## Connection to the prior ELV project

Rerunning [dcf.py](dcf.py) reproduced the saved [Lab 06 ELV analysis](lab-06-elv.md):

| Existing ELV model output | Reproduced value |
|---|---:|
| Base DCF value per diluted share | $537.84 |
| WACC / terminal growth | 6.986920% / 2.50% |
| Sensitivity corner range | $346.14–$1,036.00 |
| Terminal value share of enterprise value | 81.07% |
| Saved September 10, 2026 price input | $416.14 |

These are outputs from existing local assumptions and a saved price input, not newly verified market data. Run the earlier model with `python3 dcf.py`.

The ELV sensitivity range changes WACC and perpetual growth by ±1 percentage point around their base assumptions, keeping other inputs fixed. Higher WACC reduces value; higher perpetual growth increases value. Because terminal value supplies 81.07% of enterprise value, the gap between WACC and terminal growth has a large effect. Starting cash flow and the assumed cash-flow recovery also matter, although this grid holds them fixed. The range is a set of scenarios, not a confidence interval.

A properly selected ELV P/E peer set would add a market-based comparison to this forecast-based DCF. Disagreement would prompt a review of normalized earnings, cash conversion, growth, risk and peer selection. It would not automatically validate either method. The ABG case's numerical multiples should not be applied to ELV: franchised vehicle retail and service/parts do not provide the required business comparison to ELV's health benefits and Carelon operations described in the prior project.

For an ELV-specific extension, evaluate peers on health-benefit exposure, payer mix, services operations, medical-cost risk and growth. Supply comparable dated prices and total GAAP diluted EPS for ELV and at least two acceptable peers. The reference provides none of those ELV peer inputs, so this deliverable does not invent an ELV comparable-company valuation or combine adjusted guidance with the frozen GAAP EPS case.

## Verification and remaining work

All seven expected validation rows passed. Additional checks passed for ticker deduplication, target exclusion, missing/nonpositive/nonfinite price and EPS, policy exclusions, zero/one/three valid peers, and leave-one-out behavior. An independent exact-rational calculation confirmed the unrounded leave-one-out dollar change. Invalid target price affects its observed P/E; valid target EPS still permits peer-implied prices. Invalid target EPS makes implied prices and dollar changes not meaningful.

**No calculation issue remains for the required frozen case.** An ELV-specific P/E valuation requires the separate input set described above. The Python and Markdown files are local deliverables; GitHub submission links have not been created.
