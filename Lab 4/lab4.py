import numpy as np


def EnergyBalance(e, N, S, sigma, a):
	A = np.zeros((N + 1, N + 1))
	B = np.zeros((N + 1, 1))
	B[0] = S * (1 - a) / 4

	for i in range(N + 1):
		for j in range(N + 1):
			if i == 0:
				if j == 0:
					A[i][j] = 1
				elif j == 1:
					A[i][j] = -e
				else:
					A[i][j] = 0
			elif i == N:
				if j == N - 1:
					A[i][j] = -1
				elif j == N:
					A[i][j] = 2
				else:
					A[i][j] = 0
			else:
				if j == i - 1:
					A[i][j] = -1
				elif j == i:
					A[i][j] = 2
				elif j == i + 1:
					A[i][j] = -1
				else:
					A[i][j] = 0

	fluxes = np.linalg.solve(A, B)
	temperatures = (fluxes / sigma) ** (1 / 4)
	return temperatures


if __name__ == "__main__":
	emissivity = 1
	layer_count = 1
	solar_flux = 1350
	stefan_boltzmann = 5.6703e-8
	albedo = 0.3

	print(EnergyBalance(emissivity, layer_count, solar_flux, stefan_boltzmann, albedo))
