"""Lab 14: Meridian portfolio baselines. Run: python3 portfolio.py

Standard library only. Returns, volatilities and weights are decimal fractions.
All inputs below are course training values, not market estimates.
"""

SLEEVES = [
    {"name": "Treasury bills", "return": .035, "volatility": .005, "reserve": True},
    {"name": "Treasury 10-year note", "return": .043, "volatility": .070, "reserve": True},
    {"name": "Investment-grade bond fund", "return": .050, "volatility": .060, "reserve": False},
    {"name": "Global equity index fund", "return": .080, "volatility": .160, "reserve": False},
]
CORRELATIONS = [
    [1.00, .10, .05, .00],
    [.10, 1.00, .80, -.10],
    [.05, .80, 1.00, .25],
    [.00, -.10, .25, 1.00],
]
CPI_ESTIMATE = .025  # Labelled course estimate, not an observed inflation rate.
REAL_RETURN_TARGET = .040
OBJECTIVE_RETURN = CPI_ESTIMATE + REAL_RETURN_TARGET  # Course additive convention.
BENCHMARK_WEIGHTS = [0.0, 0.0, .40, .60]

from math import fsum, isclose, isfinite, sqrt
import sys


def validate_inputs(sleeves, correlations):
    """Reject malformed, nonfinite, out-of-range or asymmetric inputs."""
    n = len(sleeves)
    if not n or len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table must be square with one row per sleeve.")
    for sleeve in sleeves:
        if not isfinite(sleeve["return"]):
            raise ValueError("Expected returns must be finite.")
        if not isfinite(sleeve["volatility"]) or sleeve["volatility"] <= 0:
            raise ValueError("Volatilities must be finite and positive for inverse volatility.")
    for i in range(n):
        for j in range(n):
            rho = correlations[i][j]
            if not isfinite(rho) or not -1 <= rho <= 1:
                raise ValueError(f"Correlation [{i}][{j}] = {rho} is outside -1 to 1 or nonfinite.")
            if not isclose(rho, correlations[j][i], rel_tol=0, abs_tol=1e-12):
                raise ValueError(f"Correlation table is not symmetric at [{i}][{j}] and [{j}][{i}].")
        if not isclose(correlations[i][i], 1, rel_tol=0, abs_tol=1e-12):
            raise ValueError("Every diagonal correlation must equal 1.")


def covariance_matrix(sleeves, correlations):
    validate_inputs(sleeves, correlations)
    return [[correlations[i][j] * a["volatility"] * b["volatility"]
             for j, b in enumerate(sleeves)] for i, a in enumerate(sleeves)]


def validate_weights(weights, count):
    if len(weights) != count or not all(isfinite(w) and w >= 0 for w in weights):
        raise ValueError("Provide one finite, nonnegative weight per sleeve.")
    if not isclose(fsum(weights), 1, rel_tol=0, abs_tol=1e-12):
        raise ValueError("Portfolio weights must sum to 1 (100%).")


def equal_weights(sleeves):
    if not sleeves:
        raise ValueError("At least one sleeve is required.")
    return [1 / len(sleeves)] * len(sleeves)


def inverse_volatility_weights(sleeves):
    if not sleeves or any(not isfinite(s["volatility"]) or s["volatility"] <= 0 for s in sleeves):
        raise ValueError("Inverse volatility requires positive, finite volatilities.")
    inverse = [1 / sleeve["volatility"] for sleeve in sleeves]
    total = fsum(inverse)
    return [value / total for value in inverse]


def expected_return(weights, sleeves):
    validate_weights(weights, len(sleeves))
    return fsum(w * sleeve["return"] for w, sleeve in zip(weights, sleeves))


def portfolio_variance(weights, covariance):
    validate_weights(weights, len(covariance))
    n = len(weights)
    if any(len(row) != n for row in covariance):
        raise ValueError("Covariance matrix must be square.")
    # All i,j pairs include the two symmetric cross terms for each asset pair.
    variance = fsum(weights[i] * weights[j] * covariance[i][j]
                    for i in range(n) for j in range(n))
    if not isfinite(variance) or variance < -1e-12:
        raise ValueError("Portfolio variance is invalid; check the covariance inputs.")
    return max(0.0, variance)  # Only absorbs tiny floating-point roundoff.


def portfolio_volatility(weights, covariance):
    return sqrt(portfolio_variance(weights, covariance))


def reserve_weight(weights, sleeves):
    validate_weights(weights, len(sleeves))
    return fsum(w for w, sleeve in zip(weights, sleeves) if sleeve["reserve"])


def meets_objective(value, objective):
    if not isfinite(objective):
        raise ValueError("Objective return must be finite.")
    return value >= objective


def baseline_weights(sleeves):
    return {"Benchmark": list(BENCHMARK_WEIGHTS), "Equal weight": equal_weights(sleeves),
            "Inverse volatility": inverse_volatility_weights(sleeves)}


def evaluate(weights, sleeves, covariance, objective):
    result = expected_return(weights, sleeves)
    return {"weights": list(weights), "return": result,
            "volatility": portfolio_volatility(weights, covariance),
            "reserve": reserve_weight(weights, sleeves),
            "meets_objective": meets_objective(result, objective)}


def calculate_baselines(sleeves=None, correlations=None, objective=None):
    sleeves = SLEEVES if sleeves is None else sleeves
    correlations = CORRELATIONS if correlations is None else correlations
    objective = OBJECTIVE_RETURN if objective is None else objective
    covariance = covariance_matrix(sleeves, correlations)
    return {name: evaluate(weights, sleeves, covariance, objective)
            for name, weights in baseline_weights(sleeves).items()}


def main():
    results = calculate_baselines()
    print("Meridian baselines — course training inputs; annual return and volatility")
    print(f"Objective: {OBJECTIVE_RETURN:.2%}; CPI estimate: {CPI_ESTIMATE:.1%}")
    print("Weight order: " + " / ".join(s["name"] for s in SLEEVES))
    for name, row in results.items():
        print(f"\n{name}")
        print("  Weights: " + " / ".join(f"{w:.1%}" for w in row["weights"]))
        print(f"  Expected return: {row['return']:.2%}")
        print(f"  Volatility: {row['volatility']:.2%}")
        print(f"  Reserve-eligible: {row['reserve']:.1%}")
        print(f"  Meets {OBJECTIVE_RETURN:.1%} objective: {'yes' if row['meets_objective'] else 'no'}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
