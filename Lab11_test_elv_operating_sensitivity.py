"""Checks for scenario isolation, linked reruns and invalid-result handling."""
from copy import deepcopy
import unittest
from unittest.mock import patch

import Lab11_elv_operating_sensitivity as sensitivity


class OperatingSensitivityTests(unittest.TestCase):
    def test_fresh_runs_and_final_base_restoration(self):
        original = deepcopy(sensitivity.model.ASSUMPTIONS)
        with patch.object(sensitivity.model, "project", wraps=sensitivity.model.project) as project:
            result = sensitivity.analyze()
        self.assertEqual(project.call_count, 8)  # Initial + six cases + final base.
        inputs = [call.args[0] for call in project.call_args_list]
        self.assertEqual(len({id(a) for a in inputs}), 8)
        self.assertEqual(len({id(a["growth"]) for a in inputs}), 8)
        self.assertEqual(inputs[-1], original)
        self.assertEqual(result["base"]["rows"], result["restored_base"]["rows"])
        self.assertEqual(sensitivity.model.ASSUMPTIONS, original)
        for case in result["cases"]:
            self.assertTrue(case["valid"])
            expected = [] if case["level"] == "base" else [case["driver"]]
            self.assertEqual(case["changed_inputs"], expected)
        result["cases"][0]["inputs"]["margin"][0] = -1
        self.assertEqual(result["cases"][1]["inputs"]["margin"], original["margin"])
        self.assertEqual(sensitivity.BASE_INPUTS, original)

    def test_linked_growth_forecast_and_fcfe_bridge(self):
        result = sensitivity.analyze()
        lower = result["cases"][0]
        row = lower["rows"][-1]
        self.assertAlmostEqual(row["revenue"], sensitivity.model.OPENING["revenue"] * 1.02**5)
        self.assertAlmostEqual(row["operating_income"],
                               row["revenue"] * .148 * (1 - .70) - row["ppe_da"] - 628)
        self.assertAlmostEqual(row["fcfe"],
                               row["net_income"] + row["ppe_da"] + row["amort"]
                               - row["receivables_change"] - row["other_wc_change"]
                               + row["claims_change"] - row["capex"] - row["repayment"])
        self.assertNotEqual(row["claims"], result["base"]["rows"][-1]["claims"])
        self.assertNotEqual(row["receivables"], result["base"]["rows"][-1]["receivables"])
        self.assertAlmostEqual(result["base"]["outputs"]["per_share"], 365.24, places=2)

    def test_signed_changes_and_spans_recompute(self):
        result = sensitivity.analyze()
        for case in result["cases"]:
            for key in sensitivity.OUTPUTS:
                self.assertEqual(case["changes_from_base"][key],
                                 case["outputs"][key] - result["base"]["outputs"][key])
        for driver in sensitivity.DRIVERS:
            group = [case for case in result["cases"] if case["driver"] == driver]
            for key in sensitivity.OUTPUTS:
                ordered = sorted(case["outputs"][key] for case in group)
                self.assertEqual(result["spans"][driver][key]["value"], ordered[-1] - ordered[0])
                self.assertEqual(result["spans"][driver][key]["valid_results"], 3)

    def test_negative_interim_fcfe_is_retained_and_never_valued(self):
        # Deliberate test fault in returned rows; not a new company scenario.
        rows = sensitivity.model.project()
        rows[0]["fcfe"] = -123.0
        with patch.object(sensitivity.model, "project", return_value=rows), \
                patch.object(sensitivity.model, "value") as value:
            case = sensitivity.run_case("negative-FCFE test fixture")
        value.assert_not_called()
        self.assertEqual(case["rows"][0]["fcfe"], -123.0)
        self.assertIsNone(case["outputs"]["per_share"])
        self.assertIn("Negative forecast FCFE", case["valuation_limitation"])
        self.assertIsNotNone(case["outputs"]["operating_income"])

    def test_accounting_failure_is_flagged_and_excluded(self):
        base = sensitivity.run_case("base")
        broken = deepcopy(base["rows"])
        broken[0]["cash"] += 1
        with patch.object(sensitivity.model, "project", return_value=broken):
            case = sensitivity.run_case("broken-accounting test fixture")
        self.assertFalse(case["valid"])
        self.assertIsNone(case["outputs"]["per_share"])
        self.assertTrue(all(value is None for value in sensitivity.compare(case, base).values()))
        spans = sensitivity.output_spans([case, base])
        self.assertEqual(spans["fcfe"], dict(value=0, valid_results=1))
        self.assertIn("gap", case["checks"][1]["error"])

    def test_unavailable_valuation_preserves_operating_outputs(self):
        with patch.object(sensitivity.model, "value", side_effect=ValueError("Invalid terminal inputs")):
            case = sensitivity.run_case("valuation test fixture")
        self.assertTrue(case["valid"])
        self.assertIsNone(case["outputs"]["per_share"])
        self.assertGreater(case["outputs"]["fcfe"], 0)
        self.assertEqual(case["valuation_limitation"], "Invalid terminal inputs")


if __name__ == "__main__":
    unittest.main()
