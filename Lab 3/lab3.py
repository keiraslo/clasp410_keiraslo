#Importing Libraries
import numpy as np

# Defining Inputs
nlayers = 2
emissivity = 1
albedo = 0.33       # Earth value used in the lecture
S0 = 1350          # Solar irradiance, W/m^2

# Fraction of infrared radiation transmitted through one layer
t = 1 - emissivity

# Average absorbed sunlight
S = (1 - albedo) * S0 / 4

# Unknowns are F0, F1, ..., FN.
# We need one equation for each boundary.
A = np.zeros((nlayers + 1, nlayers + 1))
b = np.zeros(nlayers + 1)

for k in range(nlayers + 1):

    # Net upward radiation equals absorbed sunlight at every boundary.
    b[k] = S

    # Surface radiation travels upward through k layers.
    A[k, 0] = t ** k

    for j in range(1, nlayers + 1):

        if j <= k:
            # Layer j is below this boundary.
            # Its upward radiation crosses k - j layers.
            A[k, j] = t ** (k - j)

        else:
            # Layer j is above this boundary.
            # Its downward radiation crosses j - k - 1 layers.
            # Downward flux gets a negative sign.
            A[k, j] = -t ** (j - k - 1)

print("A:")
print(A)

print("b:")
print(b)

## Task 2:

