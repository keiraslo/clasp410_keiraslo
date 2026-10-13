#Notes from class: convergence test w/ time step size, check steady state (4), check doesnt diverge to infinity
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode

# Task 1
#Implement Euler and RK45 solvers using a=1, b=2, c=1, d=3
#Integrate for 100 years with initial conditions N1=0.3 N2=0.6
#for the competition model: use a step size of 1 year
#for the predator-prey model: use a step size of 0.05 years
def competition(t, N, a, b, c, d):
    """Calculate the competition model rates.

    Args:
        t: Current time, required by the ODE solver.
        N: Current populations [N1, N2].
        a: Growth rate of population 1.
        b: Effect of population 2 on population 1.
        c: Growth rate of population 2.
        d: Effect of population 1 on population 2.

    Returns:
        The rates of change [dN1/dt, dN2/dt].
    """
    N1, N2 = N
    return np.array([
        a * N1 * (1 - N1) - b * N1 * N2,
        c * N2 * (1 - N2) - d * N1 * N2,
    ])


def predator_prey(t, N, a, b, c, d):
    """Calculate the predator-prey model rates.

    Args:
        t: Current time, required by the ODE solver.
        N: Current prey and predator populations [prey, predator].
        a: Prey growth rate.
        b: Effect of predators on prey.
        c: Predator death rate.
        d: Effect of prey on predator growth.

    Returns:
        The rates of change [dprey/dt, dpredator/dt].
    """
    prey, predator = N
    return np.array([
        a * prey - b * prey * predator,
        -c * predator + d * prey * predator,
    ])


def euler(model, initial, dt, years, parameters):
    """Integrate a two-population model with the Euler method.

    Args:
        model: Function that calculates both populations' rates.
        initial: Starting populations [N1, N2].
        dt: Euler time step in years.
        years: Total integration time in years.
        parameters: Model coefficients [a, b, c, d].

    Returns:
        Arrays of output times and populations at those times.
    """
    time = [0]
    populations = [np.array(initial, dtype=float)]

    for i in range(int(years / dt)):
        rates = model(time[-1], populations[-1], *parameters)
        next_populations = populations[-1] + dt * rates
        populations.append(next_populations)
        time.append((i + 1) * dt)

    return np.array(time), np.array(populations)


def rk45(model, initial, dt, years, parameters):
    """Integrate a two-population model with SciPy's RK45 solver.

    Args:
        model: Function that calculates both populations' rates.
        initial: Starting populations [N1, N2].
        dt: Time between returned output values in years.
        years: Total integration time in years.
        parameters: Model coefficients [a, b, c, d].

    Returns:
        Arrays of output times and populations at those times.
    """
    solver = ode(model).set_integrator("dopri5")
    solver.set_initial_value(initial, 0)
    solver.set_f_params(*parameters)

    time = [0]
    populations = [np.array(initial, dtype=float)]
    for i in range(int(years / dt)):
        next_populations = solver.integrate((i + 1) * dt)
        time.append(solver.t)
        populations.append(next_populations.copy())

    return np.array(time), np.array(populations)

initial = [0.3, 0.6]
years = 100
parameters = (1, 2, 1, 3)
#set timestep to smallest that can run fast (aka dont kill the loaner laptop)
models = [("Competition", competition, 1), ("Predator-prey", predator_prey, 0.001)]

fig, axes = plt.subplots(2, 1, figsize=(9, 7))
for axis, (name, model, dt) in zip(axes, models):
    time, euler_values = euler(model, initial, dt, years, parameters)
    rk_time, rk_values = rk45(model, initial, dt, years, parameters)
    _, euler_half_values = euler(model, initial, dt / 2, years, parameters)

    print(name)
    print("  Euler final:", euler_values[-1])
    print("  RK45 final:", rk_values[-1])
    print("  Euler error vs RK45:", np.linalg.norm(euler_values[-1] - rk_values[-1]))
    print("  Half-step Euler error:", np.linalg.norm(euler_half_values[-1] - rk_values[-1]))

    axis.plot(time, euler_values[:, 0], "--", label="Euler population 1")
    axis.plot(time, euler_values[:, 1], ":", label="Euler population 2")
    axis.plot(rk_time, rk_values[:, 0], label="RK45 population 1")
    axis.plot(rk_time, rk_values[:, 1], label="RK45 population 2")
    axis.set_title(f"{name} model (dt = {dt} years)")
    axis.set_ylabel("Population density")
    axis.legend()

axes[-1].set_xlabel("Time (years)")
fig.tight_layout()
plt.show()





# VALIDATION!!!!!!!
# These tests check equilibrium behavior, numerical breakdown,
# and whether smaller Euler steps improve accuracy
#Aka what jeremy said to do in class :)

test_parameters = (1, 2, 1, 3)


# TEST 1: Known Equilibrium Points
# At equilibrium, both rates should be zero.
# Starting exactly there should also leave the populations unchanged.
equilibrium_tests = [
    ("Competition", competition, [0.2, 0.4]),
    ("Predator-prey", predator_prey, [1 / 3, 0.5])
]

print("\nTEST 1: Equilibrium checks")

for name, model, equilibrium in equilibrium_tests:
    rates = model(0, equilibrium, *test_parameters)

    # Allow tiny differences from zero because computers round decimals.
    rates_pass = np.allclose(rates, [0, 0], rtol=0, atol=1e-12)

    _, equilibrium_values = euler(
        model, equilibrium, 0.01, 10, test_parameters
    )

    # Check the entire simulation, not just the final populations.
    steady_pass = np.allclose(
        equilibrium_values, equilibrium, rtol=0, atol=1e-10
    )

    print(name)
    print("  Rates are approximately zero:", rates_pass)
    print("  Populations remain at equilibrium:", steady_pass)


# TEST 2: Numerical
# Infinite or undefined values indicate that the numerical calculation
# has broken down. Negative populations are also invalid for these models.
# Passing these checks does not prove accuracy, only basic validity.
print("\nTEST 2: Finite and nonnegative populations")

validation_models = [
    ("Competition", competition, 1),
    ("Predator-prey", predator_prey, 0.05)
]

for name, model, step in validation_models:
    for solver_name, solver_function in [("Euler", euler), ("RK45", rk45)]:
        check_time, check_values = solver_function(
            model, [0.3, 0.6], step, 100, test_parameters
        )

        finite_pass = np.all(np.isfinite(check_values))
        positive_pass = np.all(check_values >= 0)

        # Also check that the returned times reached the requested endpoint.
        finished_pass = np.isclose(check_time[-1], 100)

        print(name, solver_name)
        print("  All populations are finite:", finite_pass)
        print("  All populations are nonnegative:", positive_pass)
        print("  Reached 100 years:", finished_pass)


# TEST 3: Eulerian Convergence
# These particular competition inputs have a known exact solution:
# N2 stays equal to 2*N1, and N1 follows a logistic equation.
# This gives us an independent reference instead of assuming RK45 is exact.
#
# Use a shorter interval because numerical disturbances near this
# unstable equilibrium can grow during a long simulation.
print("\nTEST 3: Euler convergence against an exact solution")

previous_error = None

for step in [0.1, 0.05, 0.025]:
    check_time, check_values = euler(
        competition, [0.3, 0.6], step, 10, test_parameters
    )

    # Exact solution for these coefficients and starting populations.
    exact_N1 = 0.2 / (1 + (0.2 / 0.3 - 1) * np.exp(-check_time))
    exact_N2 = 2 * exact_N1

    # Measure the largest error across both species and all saved times.
    # This catches errors that a final-value comparison could miss.
    error_N1 = np.max(np.abs(check_values[:, 0] - exact_N1))
    error_N2 = np.max(np.abs(check_values[:, 1] - exact_N2))
    largest_error = max(error_N1, error_N2)

    print("  dt =", step, " Maximum error =", largest_error)

    if previous_error is not None:
        # Euler is first-order: halving a sufficiently small step should
        # approximately halve the error, giving a ratio near 2.
        print("    Error decreased:", largest_error < previous_error)
        print("    Previous error / current error:",
              previous_error / largest_error)

    previous_error = largest_error




#Task 2: For the competition models: 
# How do the initial conditions and coefficient values affect the final 
# result and general behavior of the two species?


# Swap the starting populations to see whether an initial advantage
# changes which species survives.
starting_populations = [[0.2, 0.6], [0.6, 0.2]]

# Keep growth rates a and c fixed while changing competition strengths.
# Each set contains (a, b, c, d).
coefficient_sets = [
    (1, 2, 1, 3),
    (1, 0.5, 1, 0.5),
    (1, 2, 1, 0.5)
]

case_names = [
    "Strong competition",
    "Weaker competition",
    "Species 2 advantage"
]

# Use the same simulation length for every experiment.
# dt controls saved output times; RK45 chooses its own internal steps.
task2_years = 100
task2_dt = 0.1

# Columns compare coefficients, and rows compare starting populations.
# Matching axis scales make the outcomes easier to compare.
fig, axes = plt.subplots(
    2, 3, figsize=(14, 8), sharex=True, sharey=True
)

for row in range(2):
    for column in range(3):
        start = starting_populations[row]
        coefficients = coefficient_sets[column]

        # Start each experiment fresh so only the chosen inputs change.
        time2, populations2 = rk45(
            competition, start, task2_dt, task2_years, coefficients
        )

        # Use the same colors and line styles throughout the figure.
        axis = axes[row, column]

        axis.plot(
            time2, populations2[:, 0],
            color="#0072B2", label="Species 1"
        )

        axis.plot(
            time2, populations2[:, 1],
            "--", color="#D55E00", label="Species 2"
        )

        axis.set_title(
            case_names[column]
            + "\n(a,b,c,d) = " + str(coefficients)
            + "\nStart = " + str(start),
            fontsize=10
        )

        axis.set_xlabel("Time (years)")
        axis.set_ylabel("Population density")
        axis.set_ylim(-0.02, 1.05)
        axis.grid(True, alpha=0.25)
        axis.legend(fontsize=9)

        # Print final values to support our interpretation of the curves.
        print(
            case_names[column],
            "Start:", start,
            "Final:", np.round(populations2[-1], 4)
        )

fig.suptitle(
    "Task 2: How competition and starting populations affect survival"
)
fig.tight_layout()


#From AI Overview on google bc for some reason my file is listed as read only so I got an error
from pathlib import Path

# Save to your local Downloads folder instead of the read-only folder.
save_path = Path.home() / "Downloads" / "task2_competition.png"
fig.savefig(save_path, dpi=180)

print("Figure saved to:", save_path)
plt.show()



# TASK 3: Predator-prey experiments

# First change the initial populations while keeping coefficients fixed.
# Then change each coefficient separately to isolate its effect.
experiments = [
    ("Baseline",                 [0.3, 0.6], (1, 2, 1, 3)),
    ("Different starting values", [0.6, 0.3], (1, 2, 1, 3)),
    ("Higher prey growth: a",     [0.3, 0.6], (2, 2, 1, 3)),
    ("Stronger predation: b",     [0.3, 0.6], (1, 3, 1, 3)),
    ("Higher predator death: c",  [0.3, 0.6], (1, 2, 2, 3)),
    ("Higher predator growth: d", [0.3, 0.6], (1, 2, 1, 4))
]

# A shorter time window makes individual population cycles easier to see.
task3_years = 30
task3_dt = 0.02

#Source for guidance (from google yay):
#https://scipy-cookbook.readthedocs.io/items/LoktaVolterraTutorial.html
#https://scientific-python.readthedocs.io/en/latest/notebooks_rst/3_Ordinary_Differential_Equations/02_Examples/Lotka_Volterra_model.html
fig, axes = plt.subplots(6, 2, figsize=(12, 20))

for row in range(len(experiments)):
    name, start, coefficients = experiments[row]

    # Use RK45 to reduce the artificial growth of oscillations that
    # Euler can produce in this model.
    time3, populations3 = rk45(
        predator_prey, start, task3_dt, task3_years, coefficients
    )

    prey = populations3[:, 0]
    predators = populations3[:, 1]

    # Plot both populations against time to compare peak heights,
    # cycle lengths, and the delay between prey and predator peaks.
    axes[row, 0].plot(
        time3, prey, color="#0072B2", label="Prey"
    )
    axes[row, 0].plot(
        time3, predators, "--", color="#D55E00", label="Predators"
    )

    axes[row, 0].set_title(
        name + "\nStart = " + str(start)
        + ", (a,b,c,d) = " + str(coefficients),
        fontsize=10
    )
    axes[row, 0].set_xlabel("Time (years)")
    axes[row, 0].set_ylabel("Population density")
    axes[row, 0].legend(loc="upper right", fontsize=9)
    axes[row, 0].grid(True, alpha=0.25)

    # A phase diagram compares predator and prey populations directly.
    # Each point pairs their populations at the same moment in time.
    axes[row, 1].plot(
        prey, predators, color="#0072B2", label="Trajectory"
    )

    # Mark the starting point to show where the experiment begins.
    axes[row, 1].plot(
        prey[0], predators[0], "o", color="#D55E00", label="Start"
    )

    # Setting both rates to zero gives the coexistence equilibrium:
    # prey = c/d and predators = a/b.
    # Mark it to see how each trajectory moves around equilibrium.
    a, b, c, d = coefficients
    equilibrium_prey = c / d
    equilibrium_predators = a / b

    axes[row, 1].plot(
        equilibrium_prey, equilibrium_predators,
        "kx", markersize=9, label="Equilibrium"
    )

    #Making the axes bigger so legend doesnt overlap
    axes[row, 1].set_xlim(0.0, 1.5)
    axes[row, 1].set_ylim(0.0, 1.7)

    axes[row, 1].set_title(name + ": phase diagram", fontsize=10)
    axes[row, 1].set_xlabel("Prey population density")
    axes[row, 1].set_ylabel("Predator population density")
    axes[row, 1].legend(loc="upper right")
    axes[row, 1].grid(True, alpha=0.25)

    # Ranges describe oscillating populations better than final values,
    # which depend on where the simulation stops within a cycle.
    print("\n" + name)
    print("  Prey range:", round(min(prey), 3), "to", round(max(prey), 3))
    print(
        "  Predator range:",
        round(min(predators), 3), "to", round(max(predators), 3)
    )
    print(
        "  Equilibrium:",
        round(equilibrium_prey, 3),
        round(equilibrium_predators, 3)
    )

fig.suptitle("Task 3: Predator-prey cycles and phase diagrams", fontsize=14)
fig.tight_layout(rect=[0, 0, 1, 0.98])

plt.show()