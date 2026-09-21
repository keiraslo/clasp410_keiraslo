#Import libraries
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

#Global constants
k = 0.1 #cooling coeff
T_final = 60 # desired temp in degrees Celsius
T_initial = 90 # initial temp in degrees Celsius
T_creamer = 5 # temperature of creamer in degrees Celsius

#Case 1 (no creamer)
def NoCreamer(T_initial, T_final, T_env):
    '''
    Parameters
    -------
    T_initial - initial temperature of coffee
    T_final - final temperature of coffee
    Returns
    -------
    -------
    t- time taken for coffee to reach T_final
    Example
    -------
    >>>> Cooltime = NoCreamer(90, 60, 60)

    '''
    CoolingTime = (1/k) * np.log((T_initial - T_final)/(T_initial - T_env))
    return CoolingTime

Time = NoCreamer(90, 60, 60)
#Case 2 (creamer added immediately)
#Case 3 (creamer added when coffee reaches 60 degrees Celsius)