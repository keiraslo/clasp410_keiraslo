import numpy as np
import matplotlib.pyplot as plt

#emissivity
e = 1
#layer count
N = 1
#Solar Flux
S = 1361
#Stefan-Boltzmann constant
sigma = 5.67e-8
#albedo
a = 0.3

#Want to create a matrix of all of the inputs to our system of equations
#A = np.array([1, 1-e, (1-e)^2, (1-e)^N,[])
#From Board: F_g = ((1-a)*S)/4(1-e/2))
#F_a = (((1-a)*S)/4*(1-e/2))/2

def EnergyBalance(e, N, S, sigma, a):
#since we have N layers, we will have N+1 equations, one for each layer and one for the boundary condition at the top and bottom.
#We cant set matrix dimensions to an arbitrary number, so we will create a matrix of zeros and then fill in the values as we go.
    A = np.zeros((N+1, N+1))
    B = np.zeros((N+1, 1))

#solar flux
    B[0] = S*(1-a)

    for i in range(N+1):
        for j in range(N+1):
            #for the first row, we want to set the first element to 1 and the rest to 0, since we are setting the boundary condition at the top of the atmosphere.
            if i == 0:
                if j == 0:
                    A[i][j] = 1
                else:
                    A[i][j] = 0
            #for the last row, we want to set the last element to (1-e)^N and the rest to 0, since we are setting the boundary condition at the bottom of the atmosphere.
            elif i == N:
                if j == N:
                    A[i][j] = (1-e)**N
                else:
                    A[i][j] = 0
            #for the middle rows, we want to set the elements to -e, 1, and -e for the j-1, j, and j+1 elements respectively, and 0 for the rest of the elements.
            else:
                if j == i-1:
                    A[i][j] = -e
                elif j == i:
                    A[i][j] = 1
                elif j == i+1:
                    A[i][j] = -e
                else:
                    A[i][j] = 0

    #Now we can solve the system of equations using numpy's linear algebra solver.
    T = (np.linalg.solve(A, B))
    print(T.shape)

    #account for the Stefan-Boltzmann law to convert from energy flux to temperature
    Temp = (T/sigma)**(1/4)
    return Temp

output = EnergyBalance(e, N, S, sigma, a)
print (output)


