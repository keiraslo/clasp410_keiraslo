# Lab 2: Lotka-Volterra Population Dynamics
## Keira Slocum, Climate 410

Today I learned I can add pngs to markdown files 🥳🎊 (yayyyayaya)

### Task 1:
**How does the performance of the Euler method solver compare to the rk45 method for both sets of equations? **


For both examples, I used a=1, b=2, c=1, d=3, and initial populations N_1=0.3, N_2=0.6 for 100 years. The code plots Euler and RK45 trajectories together and prints their final populations and endpoint differences. It also repeats Euler with half the time step to show the effect of step size.

For the competition model, the starting rates are dN_1/dt=-0.15 and dN_2/dt=-0.30. The nonzero equilibrium is N_1=0.2, N_2=0.4, and these initial conditions lie on the line N_2=2N_1. Both methods approach this equilibrium for this particular example. The one-year Euler step is relatively coarse, but it does a good job showing the euler step. On the other hand, the RK45 result appears to be a more accurate reference model.

For the predator-prey model, the equilibrium is prey c/d=1/3 and predator a/b=0.5. From the chosen initial populations, both initial rates are -0.06, so both populations initially decrease. The populations then oscillate around the equilibrium. Euler with a 0.05 step approximates the oscillation, but its error builds up and can distort the cycle. RK45 tracks the oscillation more accurately. Reducing Euler's step to 0.025 years should bring its endpoint closer to RK45, but step count increases and the code takes longer to run.

This comparison depends on the chosen conditions: the competition example follows a special path toward its equilibrium, while the repeating predator-prey cycle makes accumulated time-stepping error easier to see

### Figure 1: Competition Model and timestep
![alt text](attempt3_task1.png)



### Task 2:
For the competition models: How do the initial conditions and coefficient values affect the final result and general behavior of the two species? 

Initial conditions and competition coefficients affect both the populations’ behavior over time and whether they coexist or one approaches extinction. Under strong competition, initial conditions
can determine which species survives: in the figure’s left column, reversing the starting densities reverses which curve approaches 1 and which approaches zero. Under weaker competition, initial conditions affect the early behavior but not the final outcome. Both curves in the middle column approach approximately 0.67, demonstrating coexistence despite different starting populations.Differing competition strengths can also overpower an initial population advantage. In the right column, species 2 strongly suppresses species 1 but experiences weaker competition itself. Its dashed orange curve approaches 1 in both rows, even when it starts smaller, while the blue curve approaches zero. 

Figure 2 also shows that initial conditions influence the populations’ behavior before equilibrium. In the middle subplots, the initiallylarger population briefly overshoots its final density before both species settle near 0.67. Increasing either growth coefficients strengthens that species’ growth relative to competition and can change the coexistence densities or survival
outcome. 

### Figure 2: Initial Population and Competition Stregth
![alt text](comp&starting.png)

Figure 3 shows that variance in growth coefficients affects the final population densities. With both constants equal to 1, both species approach 0.67 as we discovered previously. If we increase species 1's growth coefficient by doubling it (middle Figure 3 subplot) we get a density of about .86, and species 2 which maintains the same growth constant's density decreases to about 0.57. If we instead increase species 2's coefficient (c=2), then the associated densties switch populations. Therefore, a higher growth constant which represents quicker reproduction whem viewed in isolation indicates that the species with faster reproduction affects the one without by supressing the other's growth. 
### Figure 3: Growth Coefficient Impacts
![alt text](.png)

### Task 3: 
**For the Predator-Prey models: How do the initial conditions and coefficient values affect the final result and general behavior of the two species? What new information can we get from the phase diagrams?**



![alt text](axesmoved.png)

### Task 4:
What does this tell us about the feasibility of performing long-term weather forecasts or making long-term predictions about any non-linear system?

