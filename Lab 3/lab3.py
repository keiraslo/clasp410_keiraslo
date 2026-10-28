#Importing Libraries
import numpy as np
import matplotlib.pyplot as plt

# Defining Inputs
nlayers = 2
emissivity = 1
albedo = 0.33       # Earth value used in the lecture
S0 = 1350          # Solar irradiance, W/m^2

# Validate inputs (Fixing broken code from working in class)
if not isinstance(nlayers, (int, np.integer)) or nlayers < 0:
    raise ValueError("nlayers must be a nonnegative integer.")
if not 0 < emissivity <= 1:
    raise ValueError("emissivity must be greater than 0 and at most 1.")
if not 0 <= albedo <= 1:
    raise ValueError("albedo must be between 0 and 1.")
if S0 <= 0:
    raise ValueError("S0 must be positive.")

# Fraction of infrared radiation transmitted through one layer
t = 1 - emissivity

# Average absorbed sunlight
S = (1 - albedo) * S0 / 4
#From Board: F_g = ((1-a)*S)/4(1-e/2))
#F_a = (((1-a)*S)/4*(1-e/2))/2
# Unknowns are F0, F1, ..., FN
# F0 is surface emission; Fj is emission in each direction by layer j
A = np.zeros((nlayers + 1, nlayers + 1))
b = np.zeros(nlayers + 1)

for k in range(nlayers + 1):

    # Net upward radiation equals absorbed sunlight at every boundary
    b[k] = S

    # Surface radiation travels upward through k layers
    A[k, 0] = t ** k

    for j in range(1, nlayers + 1):

        if j <= k:
            # Layer j is below this boundary
            # Its upward radiation crosses k - j layers
            A[k, j] = t ** (k - j)

        else:
            # Layer j is above this boundary
            # Its downward radiation crosses j - k - 1 layers
            # Downward flux gets a negative sign
            A[k, j] = -t ** (j - k - 1)

print("A:")
print(A)

print("b:")
print(b)

# Solve the system without explicitly inverting A.
fluxes = np.linalg.solve(A, b)

print("Fluxes, W/m^2:")
print(fluxes)

# source: https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose.html
# google search AI overview thing led me to this source ^
# Validation: the solution must satisfy every boundary equation.
np.testing.assert_allclose(A @ fluxes, b, rtol=1e-10, atol=1e-10)

# Validation: compare with the analytical surface flux.
expected_surface_flux = S * (
    1 + nlayers * emissivity / (2 - emissivity)
)
np.testing.assert_allclose(
    fluxes[0], expected_surface_flux, rtol=1e-10, atol=1e-10
)

# Validation: perfectly absorbing layers have a known solution.
# F0 = (N + 1)S, F1 = NS, ..., FN = S.
if emissivity == 1:
    expected_fluxes = S * np.arange(nlayers + 1, 0, -1)
    np.testing.assert_allclose(
        fluxes, expected_fluxes, rtol=1e-10, atol=1e-10
    )

# Validation: the two-layer blackbody example from the inputs above.
if nlayers == 2 and emissivity == 1:
    expected_A = np.array([
        [1., -1.,  0.],
        [0.,  1., -1.],
        [0.,  0.,  1.]
    ])
    np.testing.assert_allclose(A, expected_A)

print("All validation checks passed.")

## Task 2:

# Define a function so we can run the model with different inputs
def atmosphere_model(nlayers, S0, emissivity, albedo):

    # Stefan-Boltzmann constant
    sigma = 5.6703e-8

    # Fraction of infrared radiation transmitted through one layer (again in case)
    t = 1 - emissivity

    # Average absorbed sunlight
    S = (1 - albedo) * S0 / 4

    # Unknowns are F0 through FN
    # Index 0 is the surface; indices 1 through N are atmospheric layers
    # We need one equation for each boundary
    A = np.zeros((nlayers + 1, nlayers + 1))
    b = np.zeros(nlayers + 1)

    # Visit each boundary, starting just above the surface
    for k in range(nlayers + 1):

        # Net upward radiation equals absorbed sunlight at every boundary
        b[k] = S

        # Surface radiation travels upward through k layers
        A[k, 0] = t ** k

        # Add the radiation contribution from each atmospheric layer
        for j in range(1, nlayers + 1):

            if j <= k:
                # Layer j is below this boundary
                # Its upward radiation crosses k - j layers
                A[k, j] = t ** (k - j)

            else:
                # Layer j is above this boundary
                # Its downward radiation crosses j - k - 1 layers
                # Downward flux gets a negative sign
                A[k, j] = -t ** (j - k - 1)

    # Solve the equations to find the emitted fluxes
    fluxes = np.linalg.solve(A, b)

    # Create an array to hold the temperature of the surface and each layer
    temperatures = np.zeros(nlayers + 1)

    # Convert surface flux to temperature using surface emissivity = 1
    temperatures[0] = (fluxes[0] / sigma) ** 0.25

    # Convert each atmospheric layer's emitted flux to temperature
    for j in range(1, nlayers + 1):
        temperatures[j] = (fluxes[j] / (emissivity * sigma)) ** 0.25

    # Return temperatures in order from the surface to the highest layer
    return temperatures


# Run the function using the inputs defined in Task 1
temperatures = atmosphere_model(nlayers, S0, emissivity, albedo)

# Display the calculated temperatures
print("Temperatures in K, starting at the surface:")
print(temperatures)


# Validation: test two perfectly absorbing atmospheric layers
# I got "Access to singh.sci.monash.edu was denied" and I didnt write down the in-class values
test_temperatures = atmosphere_model(2, 1350, 1, 0.33)

# Calculate the absorbed sunlight for this test
test_S = (1 - 0.33) * 1350 / 4

# Stefan-Boltzmann constant
sigma = 5.6703e-8

# For two blackbody layers, the expected fluxes are 3S, 2S, and S
expected_temperatures = np.zeros(3)
expected_temperatures[0] = (3 * test_S / sigma) ** 0.25
expected_temperatures[1] = (2 * test_S / sigma) ** 0.25
expected_temperatures[2] = (test_S / sigma) ** 0.25

# Check whether the calculated and expected temperatures agree
# The allclose function allows for small rounding differences
if np.allclose(test_temperatures, expected_temperatures):
    print("Validation passed.")
else:
    print("Validation failed.")
    print("Model temperatures:", test_temperatures)
    print("Expected temperatures:", expected_temperatures)


#Task 3
# Experiment 1: vary emissivity with one atmospheric layer

# Create 100 emissivity values between nearly zero and one
# Avoid zero because the function divides by emissivity
emissivities = np.linspace(0.001, 1, 100)

# Create an array to store the surface temperatures
surface_temperatures = np.zeros(len(emissivities))

# Run the model once for each emissivity
for i in range(len(emissivities)):

    # Calculate temperatures for a single atmospheric layer
    temperatures = atmosphere_model(1, S0, emissivities[i], albedo)

    # Save the surface temperature from the first array entry
    surface_temperatures[i] = temperatures[0]

# Calculate the emissivity needed to produce a surface temperature of 288 K
# For one layer, sigma * T_surface^4 = S / (1 - emissivity / 2)
S = (1 - albedo) * S0 / 4
target_temperature = 288
required_emissivity = 2 * (1 - S / (sigma * target_temperature ** 4))

# Check the calculated emissivity using our model
check_temperatures = atmosphere_model(
    1, S0, required_emissivity, albedo
)

print("Emissivity needed for 288 K:", required_emissivity)
print("Surface temperature check:", check_temperatures[0], "K")

# Plot surface temperature against emissivity
plt.figure()
plt.plot(emissivities, surface_temperatures)
plt.axhline(288, color="gray", linestyle="--", label="288 K")
plt.plot(
    required_emissivity, 288, "ro",
    label="Required emissivity"
)
plt.xlabel("Atmospheric emissivity")
plt.ylabel("Surface temperature (K)")
plt.title("Surface temperature with one atmospheric layer")
plt.legend()
plt.grid(True)
plt.show()


# Experiment 2: vary the number of layers with emissivity fixed at 0.255
emissivity = 0.255

# Test models with zero through four atmospheric layers
layer_numbers = np.arange(6)

# Create an array to store the surface temperature for each model
layer_surface_temperatures = np.zeros(len(layer_numbers))

# Run the model for each number of layers
for i in range(len(layer_numbers)):

    # Calculate temperatures for the current number of layers
    temperatures = atmosphere_model(
        layer_numbers[i], S0, emissivity, albedo
    )

    # Save and display the surface temperature
    layer_surface_temperatures[i] = temperatures[0]
    print(
        "Layers:", layer_numbers[i],
        "Surface temperature:", round(temperatures[0], 2), "K"
    )

# Plot how surface temperature changes with the number of layers
plt.figure()
plt.plot(layer_numbers, layer_surface_temperatures, "o-")
plt.axhline(288, color="gray", linestyle="--", label="288 K")
plt.xlabel("Number of atmospheric layers")
plt.ylabel("Surface temperature (K)")
plt.xticks(layer_numbers)
plt.title("Surface temperature with emissivity = 0.255")
plt.legend()
plt.grid(True)
plt.show()

# Plot temperature profiles for the one through four layer models
plt.figure()

for n in range(1, 6):

    # Calculate the surface and atmospheric temperatures
    temperatures = atmosphere_model(n, S0, emissivity, albedo)

    # Use layer number as height because physical altitudes are not specified
    # Layer 0 represents the surface
    altitude = np.arange(n + 1)

    # Plot temperature horizontally and layer number vertically
    plt.plot(temperatures, altitude, "o-", label=str(n) + " layers")

plt.xlabel("Temperature (K)")
plt.ylabel("Model layer above surface")
plt.yticks(np.arange(6))
plt.title("Temperature profiles with emissivity = 0.255")
plt.legend()
plt.grid(True)
plt.show()

## Task 4:
# Set the solar irradiance for Venus
S0_venus = 2600

# Albedo from https://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html
albedo_venus = 0.75

# Each atmospheric layer absorbs all incident infrared radiation
emissivity_venus = 1

# Set the target surface temperature
target_temperature = 700

# Store the Stefan-Boltzmann constant
sigma = 5.6703e-8

# Calculate the average sunlight absorbed by Venus
S_venus = (1 - albedo_venus) * S0_venus / 4

# Solve the blackbody surface temperature equation for the number of layers
estimated_layers = (
    sigma * target_temperature ** 4 / S_venus
) - 1

# Test the two whole numbers surrounding the estimated number of layers
lower_layers = int(np.floor(estimated_layers))
upper_layers = lower_layers + 1

# Calculate temperatures for each of these models
lower_temperatures = atmosphere_model(
    lower_layers, S0_venus, emissivity_venus, albedo_venus
)
upper_temperatures = atmosphere_model(
    upper_layers, S0_venus, emissivity_venus, albedo_venus
)

# Calculate how far each surface temperature is from 700 K
lower_difference = abs(lower_temperatures[0] - target_temperature)
upper_difference = abs(upper_temperatures[0] - target_temperature)

# Select the number of layers that gives the closest surface temperature
if lower_difference < upper_difference:
    best_layers = lower_layers
    best_temperature = lower_temperatures[0]
else:
    best_layers = upper_layers
    best_temperature = upper_temperatures[0]

# Display the result
print("Estimated number of layers:", estimated_layers)
print("Closest whole number of layers:", best_layers)
print("Surface temperature:", best_temperature, "K")

# Validate the model against the analytical blackbody solution
expected_temperature = (
    (best_layers + 1) * S_venus / sigma
) ** 0.25

# Allow for small rounding differences between the two calculations
if np.isclose(best_temperature, expected_temperature):
    print("Validation passed")
else:
    print("Validation failed")


#Task 5
# Define a separate function for sunlight absorbed by the top layer
def nuclear_winter_model(nlayers, S0, emissivity, albedo):

    # This scenario requires at least one atmospheric layer
    if nlayers < 1:
        raise ValueError("At least one atmospheric layer is required")

    # Check emissivity because we divide by it later
    if emissivity <= 0 or emissivity > 1:
        raise ValueError("Emissivity must be greater than 0 and at most 1")

    # Fraction of infrared radiation transmitted through one layer
    t = 1 - emissivity

    # Average absorbed sunlight
    S = (1 - albedo) * S0 / 4

    # Create the coefficient matrix and right-hand side array
    A = np.zeros((nlayers + 1, nlayers + 1))
    b = np.zeros(nlayers + 1)

    # Only the boundary above the top layer has net upward flux equal to S
    # All boundaries below the solar heating have zero net upward flux
    b[nlayers] = S

    # Visit each boundary from the surface to the top of the atmosphere
    for k in range(nlayers + 1):

        # Surface radiation travels upward through k layers
        A[k, 0] = t ** k

        # Add the contribution from each atmospheric layer
        for j in range(1, nlayers + 1):

            if j <= k:
                # Layer j is below this boundary
                # Its upward radiation crosses k - j layers
                A[k, j] = t ** (k - j)

            else:
                # Layer j is above this boundary
                # Its downward radiation crosses j - k - 1 layers
                # Downward flux gets a negative sign
                A[k, j] = -t ** (j - k - 1)

    # Solve the equations to find the emitted fluxes
    fluxes = np.linalg.solve(A, b)

    # Check that the fluxes satisfy every boundary equation
    if not np.allclose(A @ fluxes, b):
        raise ValueError("Energy balance validation failed")

    # Create an array for surface and atmospheric temperatures
    temperatures = np.zeros(nlayers + 1)

    # Convert surface flux to temperature using surface emissivity = 1
    temperatures[0] = (fluxes[0] / sigma) ** 0.25

    # Convert atmospheric fluxes to temperatures
    for j in range(1, nlayers + 1):
        temperatures[j] = (fluxes[j] / (emissivity * sigma)) ** 0.25

    # Return the temperatures from the surface to the highest layer
    return temperatures


# Set the inputs requested for the nuclear winter experiment
nlayers = 5
emissivity = 0.5
S0 = 1350

# Keep the albedo used in the earlier Earth experiments
albedo = 0.33

# Calculate the temperatures
winter_temperatures = nuclear_winter_model(
    nlayers, S0, emissivity, albedo
)

# Display the surface and atmospheric temperatures
print("Surface temperature:", winter_temperatures[0], "K")
print("Temperatures from surface to top layer:")
print(winter_temperatures)


# Validation: compare with the analytical solution for top-layer heating
sigma = 5.6703e-8
S = (1 - albedo) * S0 / 4

# The surface and all layers below the top have the same temperature
expected_surface = (S / ((2 - emissivity) * sigma)) ** 0.25

# The top layer is warmer because it absorbs the sunlight
expected_top = (
    S / (emissivity * (2 - emissivity) * sigma)
) ** 0.25

# Fill the expected array with the surface temperature
expected_temperatures = np.zeros(nlayers + 1)
for j in range(nlayers + 1):
    expected_temperatures[j] = expected_surface

# Replace the last entry with the expected top-layer temperature
expected_temperatures[nlayers] = expected_top

# Compare every modeled temperature with its expected value
if np.allclose(winter_temperatures, expected_temperatures):
    print("Temperature validation passed")
else:
    print("Temperature validation failed")
    print("Expected temperatures:", expected_temperatures)


# Use model layer number as height because physical altitudes are unspecified
altitude = np.arange(nlayers + 1)

# Plot temperature horizontally and model layer vertically
plt.figure()
plt.plot(winter_temperatures, altitude, "o-")
plt.xlabel("Temperature (K)")
plt.ylabel("Model layer above surface")
plt.title("Nuclear winter temperature profile")
plt.yticks(altitude)
plt.grid(True)
plt.show()