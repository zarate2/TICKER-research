import sys

starting_fcff = 100.0
growth_rates = [0.08, 0.06, 0.05, 0.04, 0.03]
wacc = 0.10
terminal_growth = 0.03
cash = 50.0
debt = 300.0
shares = 50.0

if terminal_growth >= wacc:
    sys.exit("Error: Terminal growth rate must be less than WACC.")

fcff_years = []
current_fcff = starting_fcff
for g in growth_rates:
    current_fcff *= (1 + g)
    fcff_years.append(current_fcff)

pv_fcff_years = [fcff / ((1 + wacc) ** i) for i, fcff in enumerate(fcff_years, 1)]

terminal_value = (fcff_years[-1] * (1 + terminal_growth)) / (wacc - terminal_growth)
pv_terminal_value = terminal_value / ((1 + wacc) ** 5)

for i, fcff in enumerate(fcff_years, 1):
    print(f"FCFF Year {i}: {fcff:.4f}")

for i, pv in enumerate(pv_fcff_years, 1):
    print(f"PV of FCFF Year {i}: {pv:.4f}")

print(f"Terminal Value at Year 5: {terminal_value:.4f}")
print(f"PV of Terminal Value: {pv_terminal_value:.4f}")
