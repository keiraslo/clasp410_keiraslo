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

