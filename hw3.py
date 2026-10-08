#My RAM failed on my computer so the homework I did in class is
#stuck on that device which is now being repaired.

import matplotlib.pyplot as plt
import numpy as np

# Set the starting temperature
T_i = 90

# Set the surrounding temperature
T_env = 20

# Set the cooling constant
k = 0.1

# Set different time step sizes
time_steps = [0.1, 0.5, 1, 5, 10]

# Create a figure
plt.figure()

# Repeat for each time step size
for dt in time_steps:

    # Create times from zero to sixty minutes
    time = np.arange(0, 60 + dt, dt)

    # Create an array to store temperatures
    T = np.zeros(len(time))

    # Set the first temperature
    T[0] = T_i

    # Calculate each new temperature
    for i in range(len(time) - 1):

        # Calculate the cooling rate
        dT_dt = -k * (T[i] - T_env)

        # Update the temperature
        T[i + 1] = T[i] + dT_dt * dt

    # Plot temperatures for this time step
    plt.plot(time, T, label=str(dt))

# Label the graph
plt.xlabel("Time")
plt.ylabel("Temperature in Celsius")
plt.title("Effect of time step size")

# Show the legend and graph
plt.legend()
plt.show()