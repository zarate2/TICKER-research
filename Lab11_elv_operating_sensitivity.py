"""ELV one-at-a-time operating sensitivity using the agreed FY2026-2030 paths.

Run directly or with lab10_proforma_elv.py --operating-sensitivity.
Writes a Markdown comparison and JSON containing every input and statement row.
"""
from copy import deepcopy
import json
from pathlib import Path

import lab10_proforma_elv as model


# Separate baseline; never used as a mutable scenario input.
BASE_INPUTS = deepcopy(model.ASSUMPTIONS)
DRIVERS = {
    "growth": {
        "label": "Revenue growth",
        "units": "% annual revenue growth",
        "lower": [.02] * 5,
        "base": [.03] * 5,
        "higher": [.04] * 5,
    },
    "margin": {
        "label": "Blended gross margin",
        "units": "% of operating revenue",
        "lower": [.138, .140, .142, .143, .143],
        "base": [.143, .145, .147, .148, .148],
        "higher": [.148, .150, .152, .153, .153],
    },
}
OUTPUTS = ("operating_income", "fcfe", "per_share")


def statement_checks(rows, inputs):
    """Keep annual check results visible, including failures and signed gaps."""
    checks = []
    for row in [model.OPENING, *rows]:
        error = ""
        try:
            model.check([row], inputs)
        except ValueError as exc:
            error = str(exc)
        cash_gap = None
        if "cfo" in row:
            cash_gap = (row["cash"] - row["opening_cash"] - row["cfo"]
                        - row["cfi"] - row["cff"])
        checks.append(dict(
            year=row["year"], valid=not error, error=error,
            balance_gap=model.totals(row)[2], cash_flow_gap=cash_gap,
            cash_above_floor=row["cash"] - inputs["minimum_cash"],
            revolver=row["revolver"],
            revolver_headroom=inputs["revolver_limit"] - row["revolver"],
        ))
    return checks


def run_case(name, driver=None, path=None):
    inputs = deepcopy(BASE_INPUTS)
    if driver is not None:
        inputs[driver] = deepcopy(path)
    changed = [key for key in inputs if inputs[key] != BASE_INPUTS[key]]
    if any(key != driver for key in changed):
        raise AssertionError("More than the selected independent input changed")
    # Retain signed statement rows even if a funding/accounting check fails.
    # The default model entry point still raises immediately on failed checks.
    rows = model.project(inputs, validate=False)
    checks = statement_checks(rows, inputs)
    valid = all(item["valid"] for item in checks)
    valuation, reason = None, ""
    if not valid:
        reason = "Accounting or funding checks failed; run excluded from comparisons."
    elif any(row["fcfe"] < 0 for row in rows):
        reason = ("Negative forecast FCFE retained. Existing valuation omits negative "
                  "interim years; value/share unavailable under this sensitivity workflow.")
    else:
        try:
            valuation = model.value(rows, inputs)
        except ValueError as exc:
            reason = str(exc)
    return dict(
        name=name, driver=driver, inputs=inputs, changed_inputs=changed,
        rows=rows, checks=checks, valid=valid, valuation=valuation,
        valuation_limitation=reason,
        outputs=dict(operating_income=rows[-1]["operating_income"],
                     fcfe=rows[-1]["fcfe"],
                     per_share=valuation["per_share"] if valuation else None),
    )


def compare(case, base):
    return {
        key: case["outputs"][key] - base["outputs"][key]
        if case["valid"] and base["valid"]
        and case["outputs"][key] is not None and base["outputs"][key] is not None
        else None
        for key in OUTPUTS
    }


def output_spans(cases):
    spans = {}
    for key in OUTPUTS:
        values = [case["outputs"][key] for case in cases
                  if case["valid"] and case["outputs"][key] is not None]
        spans[key] = dict(value=max(values) - min(values) if values else None,
                          valid_results=len(values))
    return spans


def analyze():
    saved_base, saved_model = deepcopy(BASE_INPUTS), deepcopy(model.ASSUMPTIONS)
    for driver, spec in DRIVERS.items():
        if spec["base"] != BASE_INPUTS[driver]:
            raise ValueError(f"{driver}: agreed base path no longer matches model; review ranges")
    base = run_case("Initial base")
    cases, spans = [], {}
    for driver, spec in DRIVERS.items():
        group = []
        for level in ("lower", "base", "higher"):
            case = run_case(f"{spec['label']} — {level}", driver, spec[level])
            case["level"] = level
            case["changes_from_base"] = compare(case, base)
            cases.append(case)
            group.append(case)
        spans[driver] = output_spans(group)
    # Final linked-model run uses a fresh, unmodified base copy.
    restored = run_case("Restored base")
    restored_matches = all(restored[key] == base[key] for key in
                           ("inputs", "rows", "checks", "outputs", "valuation"))
    if not restored_matches or BASE_INPUTS != saved_base or model.ASSUMPTIONS != saved_model:
        raise AssertionError("Base restoration or input isolation failed")
    return dict(
        units="USD millions except value per opening common share in USD/share",
        forecast_years=list(range(2026, 2031)), opening=deepcopy(model.OPENING),
        base_inputs=deepcopy(BASE_INPUTS), drivers=deepcopy(DRIVERS),
        base=base, cases=cases, spans=spans, restored_base=restored,
        base_restoration_passed=restored_matches,
    )


def number(value, signed=False):
    if value is None:
        return "Unavailable"
    if abs(value) < .005:
        value = 0.
    return format(value, "+,.2f" if signed else ",.2f")


def report(result):
    lines = [
        "# ELV operating sensitivity",
        "",
        "FY2025-base model; forecast FY2026–FY2030. All monetary statement figures are "
        "USD millions; value per opening common share is USD/share.",
        "",
        "Each run starts from a fresh deep copy of the separate base input set. Only the "
        "named driver changes; all linked statements recalculate. Cases are listed in "
        "lower/base/higher order. Ranges are those agreed in the chat; invalid runs are "
        "excluded from comparisons.",
        "",
        "Operating profit is operating income after PP&E D&A and intangible amortization, "
        "before investment income, interest and tax. FCFE is CFO minus capex and scheduled "
        "net debt repayment, before buybacks, dividends and revolver activity.",
        "",
        "Valuation retains the existing 10% cost of equity, 2.5% terminal growth, terminal "
        "debt-paydown addback and 220.723898 million opening shares. It is conditional on "
        "the model's simplified capital and terminal assumptions, not a current price target. "
        "Any negative FCFE remains signed and makes value/share unavailable in this workflow.",
        "",
        "## Actual inputs by run",
        "",
        "| Driver | Case | Units | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for case in result["cases"]:
        spec = DRIVERS[case["driver"]]
        path = " | ".join(f"{x:.1%}" for x in case["inputs"][case["driver"]])
        lines.append(f"| {spec['label']} | {case['level']} | {spec['units']} | {path} |")
    lines += ["", "## Comparable outputs and signed changes from base", "",
              "Changes use unrounded values; subtracting displayed rounded values can differ "
              "by 0.01 in the stated output unit.", "",
              "| Run | Checks | FY2030 operating profit ($m) | Change ($m) | FY2030 FCFE ($m) | Change ($m) | Value/share ($) | Change ($/share) |",
              "|---|---|---:|---:|---:|---:|---:|---:|"]
    for case in result["cases"]:
        cells = []
        for key in OUTPUTS:
            cells.extend([number(case["outputs"][key]),
                          number(case["changes_from_base"][key], True)])
        status = "PASS" if case["valid"] else "INVALID — excluded"
        lines.append(f"| {case['name']} | {status} | " + " | ".join(cells) + " |")
        if case["valuation_limitation"]:
            lines += ["", f"{case['name']}: {case['valuation_limitation']}", ""]
    lines += ["", "## Output spans", "",
              "Maximum minus minimum across valid lower/base/higher results, calculated "
              "before rounding. The count is specific to each output; unavailable values "
              "and invalid runs are excluded.", "",
              "| Driver | Operating profit span ($m); valid count | FCFE span ($m); valid count | Value/share span ($); valid count |",
              "|---|---:|---:|---:|"]
    for driver, spans in result["spans"].items():
        cells = [f"{number(spans[key]['value'])}; {spans[key]['valid_results']}/3" for key in OUTPUTS]
        lines.append(f"| {DRIVERS[driver]['label']} | " + " | ".join(cells) + " |")
    lines += ["", "## Annual accounting and funding checks", "",
              "All gaps and cash/borrowing amounts are USD millions. PASS includes finite "
              "values, nonnegative debt/long-lived assets, balanced statements, cash-flow "
              "reconciliation, the cash floor and revolver capacity. Gap tolerance: $0.000001 million.", "",
              "| Run | Year | Balance gap | Cash-flow gap | Cash above floor | Revolver | Revolver headroom | Status / reason |",
              "|---|---:|---:|---:|---:|---:|---:|---|"]
    for case in [result["base"], *result["cases"], result["restored_base"]]:
        for check in case["checks"]:
            cells = [number(check[key]) if check[key] is not None else "N/A — opening"
                     for key in ("balance_gap", "cash_flow_gap", "cash_above_floor", "revolver", "revolver_headroom")]
            status = "PASS" if check["valid"] else "INVALID: " + check["error"]
            lines.append(f"| {case['name']} | {check['year']} | " + " | ".join(cells) + f" | {status} |")
    lines += ["", "## Statement trace", "",
              "[Full inputs, opening balances, annual statement rows, valuation components "
              "and checks for every run](Lab11_elv-operating-sensitivity-details.json) are retained "
              "at full precision. Select a run by its `name` in `cases`; each `rows` entry "
              "is one forecast year. `inputs` records all assumptions used for that run.", "",
              "The following bridge traces revenue growth — lower, FY2030. Expenses and "
              "cash outflows are shown as negative amounts. The model's other annual rows "
              "remain available in the linked details.", "",
              "| Component | FY2030 ($m) |", "|---|---:|"]
    row = result["cases"][0]["rows"][-1]
    for label, key, sign in [
        ("Revenue", "revenue", 1), ("Benefit expense", "benefits", -1),
        ("Product costs", "products", -1), ("Gross profit", "gross_profit", 1),
        ("Cash operating expense", "cash_opex", -1), ("PP&E D&A expense", "ppe_da", -1),
        ("Intangible amortization expense", "amort", -1), ("Operating profit", "operating_income", 1),
        ("Investment income", "investment_income", 1), ("Interest", "interest", -1),
        ("Tax", "tax", -1), ("Net income", "net_income", 1),
        ("PP&E D&A addback", "ppe_da", 1), ("Intangible amortization addback", "amort", 1),
        ("Increase in receivables", "receivables_change", -1),
        ("Increase in other working-capital assets", "other_wc_change", -1),
        ("Increase in claims payable", "claims_change", 1), ("CFO", "cfo", 1),
        ("Capex", "capex", -1), ("Scheduled net debt repayment", "repayment", -1),
        ("FCFE", "fcfe", 1),
    ]:
        lines.append(f"| {label} | {number(row[key] * sign)} |")
    restored = result["restored_base"]
    lines += ["", "## Base restored and rerun", "",
              "PASS: the final run uses the original base inputs. All annual statement "
              "rows, checks, valuation components and outputs exactly match the initial "
              "base before rounding; the source model's assumptions remain unchanged.", "",
              f"FY2030 operating profit: **${number(restored['outputs']['operating_income'])} million**; "
              f"FY2030 FCFE: **${number(restored['outputs']['fcfe'])} million**; "
              f"value per opening share: **{number(restored['outputs']['per_share'])} USD/share**.", "",
              "Rerun: `python3 lab10_proforma_elv.py --operating-sensitivity`.", ""]
    lines += review_sections(result)
    return "\n".join(lines)


def review_sections(result):
    base, selected = result["base"], result["cases"][0]
    labels = {"operating_income": "FY2030 operating profit ($m)",
              "fcfe": "FY2030 FCFE ($m)", "per_share": "Value/share ($)"}
    lines = ["## V — Verification evidence", "",
             "Base inputs and all five annual statement rows match exactly before and after "
             "the analysis. This is stricter than the display tolerance of 0.01 in each "
             "output unit. Accounting gap tolerance is $0.000001 million.", "",
             "Selected result: revenue growth changes from 3% to 2% in every forecast year. "
             "The JSON `changed_inputs` list contains only `growth`; margin remains "
             "14.3%, 14.5%, 14.7%, 14.8%, 14.8%, and every other independent input equals base. "
             "The full linked forecast, including receivables and medical claims payable, "
             "was recalculated.", "",
             "| Output | Base | Changed result | Changed minus base |",
             "|---|---:|---:|---:|"]
    for key, label in labels.items():
        b, c = base["outputs"][key], selected["outputs"][key]
        if base["valid"] and selected["valid"] and b is not None and c is not None:
            lines.append(f"| {label} | {b:,.6f} | {c:,.6f} | {c-b:+,.6f} |")
        else:
            lines.append(f"| {label} | {number(b)} | {number(c)} | Unavailable |")
    usable = sum(case["valid"] for case in result["cases"])
    lines += ["", f"Accounting/funding checks pass for {usable}/6 sensitivity runs. "
              "The annual evidence and any failure reasons appear above. Changes and spans "
              "are calculated from full-precision results retained in JSON.", "",
              "## E — Comparison over these ranges", ""]
    for key, label in labels.items():
        available = [(driver, result["spans"][driver][key]) for driver in DRIVERS]
        if any(span["valid_results"] != 3 for _, span in available):
            lines.append(f"- {label}: comparison unavailable because a driver has incomplete valid results.")
            continue
        largest = max(span["value"] for _, span in available)
        winners = [DRIVERS[driver]["label"] for driver, span in available if span["value"] == largest]
        lines.append(f"- {label}: **{' and '.join(winners)}** has the largest span, "
                     f"**{number(largest)}**, over these ranges.")
    lines += ["", "The revenue-growth range is 2%–4% annually; the margin range spans "
              "1.0 percentage point in each forecast year. The ordering depends on these "
              "chosen ranges and the model structure; it does not establish inherent driver "
              "importance or support ranking unlike companies by raw dollar changes.", "",
              "### Causal evidence from the higher cases", "",
              "The bridge below shows signed changes in FY2030 cash flow relative to base. "
              "Higher revenue requires more receivables and other working-capital assets, "
              "partly offset by more claims payable. Higher margin changes direct costs and "
              "claims payable while revenue-based receivables stay unchanged. These linked "
              "cash effects help explain why the operating-profit span and FCFE span can "
              "identify different drivers.", "",
              "| FY2030 change ($m) | Growth higher minus base | Margin higher minus base |",
              "|---|---:|---:|"]
    higher = [case for case in result["cases"] if case["level"] == "higher"]
    b = base["rows"][-1]
    for label, key, sign in [
        ("Operating profit", "operating_income", 1),
        ("Net income after tax", "net_income", 1),
        ("PP&E D&A addback", "ppe_da", 1), ("Intangible amortization addback", "amort", 1),
        ("Cash effect of receivables", "receivables_change", -1),
        ("Cash effect of other working-capital assets", "other_wc_change", -1),
        ("Cash effect of claims payable", "claims_change", 1),
        ("Cash effect of capex", "capex", -1),
        ("Cash effect of debt repayment", "repayment", -1), ("FCFE", "fcfe", 1),
    ]:
        values = [number((case["rows"][-1][key] - b[key]) * sign, True)
                  if case["valid"] and base["valid"] else "Unavailable" for case in higher]
        lines.append(f"| {label} | " + " | ".join(values) + " |")
    lines += ["", "Value/share also reflects cash-flow changes in all five years and the "
              "terminal cash flow, with discount rates unchanged.", "",
              "## Personal records still to complete", "",
              "The actual locked prediction and partner exchanges have not been provided. "
              "No pre-run timestamp, prediction error, partner confirmation, or personal "
              "valuation conclusion is claimed. Use "
              "[the personal record](Lab11_elv-sensitivity-personal-record.md) to attach the actual "
              "result to the original locked record and record the exchanges after they occur.", ""]
    return lines


def main():
    result = analyze()
    folder = Path(__file__).resolve().parent
    (folder / "Lab11_elv-operating-sensitivity-details.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (folder / "Lab11_elv-operating-sensitivity.md").write_text(report(result), encoding="utf-8")
    print("Saved Lab11_elv-operating-sensitivity.md and Lab11_elv-operating-sensitivity-details.json")
    print("Base restored and rerun; unchanged inputs and exact base reproduction verified.")


if __name__ == "__main__":
    main()
