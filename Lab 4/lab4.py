# CLaSP 410 - Lab 4 Code 
# Keira Slocum

## Boundary conditions to consider
# Edge - no heat flux at poles
# - q = -D partial T/ partial y = 0 at upper boundary...

#Import libraries
import numpy as np
import matplotlib.pyplot as plt

#Task 1
print('---------Task 1---------')

#equation 4: f (T, Axz )j = λ∆tB T_bar j B A_bar_xz
# begin w/ equation 2:  T_bar_j+1 = L^-1 T_bar_j
#  -> w/ L identity matrix = I - λ∆tK where K is the tridiagonal matrix
# use table 1 values
# S0 = 1370, C_seawater = 4.2 x 10^6, rho_seawater=1020,
#       Gamma (thermal diffusivity) = 100 m^2/s, dz (mixed layer ocean depth) = 50m
#       emissivity = 1.0, albedo = water/ground:0.3 and ice/snow: 0.6
# for task one use albedo of 0.3

# Code equation 4 starting with equation 2 using table 1 values

def diffusion_matrix(n, gamma, dt, dz):
    """Build the tridiagonal diffusion matrix K for a 1D no-flux system.

    The discrete operator is based on the second derivative, with no-flux
    boundaries approximated by a Neumann condition at the ends.
    """
    k = gamma * dt / dz**2
    K = np.zeros((n, n), dtype=float)

    for i in range(n):
        for j in range(n):
            if i == j:
                K[i, j] = 2.0 * k
            elif abs(i - j) == 1:
                K[i, j] = -1.0 * k

    # Apply no-flux boundary condition by modifying the first and last rows.
    K[0, 0] = k
    K[-1, -1] = k
    if n > 1:
        K[0, 1] = -k
        K[-1, -2] = -k

    return K


def equation_2_step(T, gamma, dt, dz, lambda_coeff):
    """Advance the temperature vector using equation 2: T_{j+1} = L^{-1} T_j."""
    n = len(T)
    K = diffusion_matrix(n, gamma, dt, dz)
    L = np.eye(n) - lambda_coeff * dt * K
    return np.linalg.solve(L, T)


def equation_4_step(T, gamma, dt, dz, lambda_coeff, albedo, s0):
    """Apply the forcing term from equation 4 and update the state.

    Equation 4 is represented as a linear forcing of the form
    f(T, A_xz) = lambda * dt * B * T + B * A_bar_xz,
    with the absorbed solar forcing B*A_bar_xz determined by the albedo.
    """
    n = len(T)
    K = diffusion_matrix(n, gamma, dt, dz)
    L = np.eye(n) - lambda_coeff * dt * K

    # Effective absorbed shortwave forcing per unit temperature, using a
    # simple linearized surface balance.
    absorbed = (1.0 - albedo) * s0 / 4.0
    B = absorbed / (1.0 + np.max(np.abs(T)))
    forcing = B * np.ones(n)

    rhs = T + lambda_coeff * dt * forcing
    return np.linalg.solve(L, rhs)


def task_1_solution():
    """Solve the lab's Task 1 setup using the constants listed in the notes."""
    s0 = 1370.0
    c_seawater = 4.2e6
    rho_seawater = 1020.0
    gamma = 100.0  # m^2 / s
    dz = 50.0
    emissivity = 1.0
    albedo = 0.3
    dt = 86400.0  # 1 day in seconds
    lambda_coeff = (1.0 - emissivity) / (rho_seawater * c_seawater * dz)

    # Simple 1D temperature profile with an initial cold state.
    grid_size = 6
    T = np.linspace(260.0, 290.0, grid_size)


    print('Initial profile (K):')
    print(np.round(T, 2))

    T_1 = equation_2_step(T, gamma, dt, dz, lambda_coeff)
    T_2 = equation_4_step(T, gamma, dt, dz, lambda_coeff, albedo, s0)

    print('\nAfter equation 2 update:')
    print(np.round(T_1, 2))
    print('\nAfter equation 4 update:')
    print(np.round(T_2, 2))

    return T_2


def latitude_diffusion_matrix(n, dy):
    """Build the second-derivative matrix with no-flux boundary conditions."""
    scale = 1.0 / dy**2
    matrix = np.zeros((n, n), dtype=float)

    for i in range(1, n - 1):
        matrix[i, i - 1] = scale
        matrix[i, i] = -2.0 * scale
        matrix[i, i + 1] = scale

    if n > 1:
        matrix[0, 0] = -scale
        matrix[0, 1] = scale
        matrix[-1, -2] = scale
        matrix[-1, -1] = -scale

    return matrix


def spherical_diffusion_step(T, latitudes, diffusivity, dt, dy, earth_radius):
    """Apply one implicit diffusion step with the spherical correction term."""
    n = len(T)
    second_derivative = latitude_diffusion_matrix(n, dy)
    operator = np.eye(n) - diffusivity * dt * second_derivative

    dtemp_dy = np.gradient(T, dy)
    dtemp_dy[[0, -1]] = 0.0
    latitudes_rad = np.deg2rad(latitudes)
    dln_area_dy = -np.tan(latitudes_rad) / earth_radius
    correction = diffusivity * dt * dtemp_dy * dln_area_dy

    return np.linalg.solve(operator, T + correction)


def plot_latitude_temperature():
    """Plot the Cartesian and spherical diffusion profiles by latitude."""
    npoints = 90
    dlat = 180.0 / npoints
    latitudes = np.linspace(-90.0 + dlat / 2.0, 90.0 - dlat / 2.0, npoints)
    earth_radius = 6.378e6
    dy = earth_radius * np.deg2rad(dlat)
    diffusivity = 100.0  # m^2 / s
    dt = 365.25 * 24.0 * 60.0 * 60.0  # one year in seconds
    temperature = np.linspace(260.0, 290.0, npoints)

    operator = np.eye(npoints) - diffusivity * dt * latitude_diffusion_matrix(
        npoints, dy
    )
    cartesian = np.linalg.solve(operator, temperature)
    spherical = spherical_diffusion_step(
        temperature, latitudes, diffusivity, dt, dy, earth_radius
    )

    plt.plot(latitudes, cartesian, label='Cartesian diffusion')
    plt.plot(latitudes, spherical, label='With spherical correction')
    plt.xlabel('Latitude (degrees)')
    plt.ylabel('Temperature (K)')
    plt.title('Temperature versus latitude after one year')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    task_1_solution()
    plot_latitude_temperature()

# then, add in the spherical correction term (eq 3)

# eq 3: T_bar = L_bold^-1 [T_bar_j + f(T,A_xx)_j]

# Create figure with latitude and temperature



