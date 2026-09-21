# Lab 1: Forest Fire Spread Model

Keira Slocum, Climate 410
Due 9/21 at 5PM
Hi Tyler!

## Overarching Methodology

Not required for this lab

### Task 1 🔥🧯

#### Initial Design & Implementation

I decided to approach creating this model by creating a function full of if statements. First, I want to establish my initial forest before we begin to run the simulation. Then I save it as the old version and create a copy to run the burning model on. Since this model consists of tiles which have fires spreading only to adjacent tiles, I want to create four subsections of if statement loops for up, down, left, and right. Then, if the target cell has spread, we can set its state to barren. We can then run this function for as many iterations as we desire and have it return each state.

To validate this model, I first established the expected results to be printed for each iteration given our test conditions (100% spread, 3x3 grid, start in center). Then, I can print the initial, uncopied grid, run the function and print the result, and then repeat to get as many results as I want to test. 

### Task 2🌲📊

#### Implementation

For tasks 2a and 2b, I decided to create new functions to produce plots which visually supported muy conclusions while providing quantitative evidence for them aswell. For task 2a, I first defined what variables could be helpful to be observed and then investigated to support my investigation. Then, I wrote a function to plot the probabilities of spread and density against the percent of the forest burned in the simulation. For task 2b, I wrote a seperate section which hardcoded in a line of barren cells across the grid to see how the fire spread would respond to a controlled burn transecting the forest.

#### Task 2a

**For each case, -qualitatively- explore the impact on wildfire evolution. What observables will you need to explore? How will you quantify and visualize the results?**

We need to investigate the following variables: the percentage of cells bare, percent burning, and percent healthy. We should also examine the number of iterations the model takes for the fire to burn out. To quantify the results, for each simulation we can calculate the percentage of each state as a fraction over the total number of grid cells (15). Then, we can create figures to visually represent the change in each.

**How does the spread of wildfire depend on the probability of spread of fire and initial forest density?**
In the second figure our code produces titled: "Effects of P_spread and P_bare", we can see the relationship between the increase in the percentage of the forest burned dependent on the probability of spread and the probability of a cell to be bare. Cells being bare is significant as the fewer forested cells the model has, the less dense it is initially. In the figure, we see that P_spread, represented as a blue line, is dominant when it comes to determining the amount of forest burned with a steep increase starting at about 0.5 capping off at 100% burned once reaching approximately 0.75. The initial forest density appears to have a similar relationship but to a lesser extent. P_bare, a value inversley proportional to the forest density, appears to dominate the percent burned prior to the Probability = 0.4 threshold. This orange line peaks at a probability of 0.2 with 40 percent of the forest burned. This leads me to believe that while wildfire spread is lightly mitigated by a lower forest density, the probability of spread is much more significant to the total amount of forest burned.

#### Task 2b

**Explain how controlled burns could be used to control the spread of wildfires. Would controlled burns reduce the likelihood of fires, severity of fires or both? Explain using figures and words.**

In our simulated model, fires cannot spread to already barren ground. If a controlled burn is planned, cells can be selected in a manner which limits the number of cells that can burn. Seeing as in our model, fire can only spread to neighboring cells, a controlled burn and its area can act as a buffer between forested zones and limit the total damage. In the "Controlled Burn Forest After One Iteration" and "Controlled Burn Forest After Two Iterations" printed returns, we can see that the artifically set buffer line of burnt cells prevent the ignited spots from spreading fire across this barrier. 

### Task 3 🧟🤮

#### Initial Design

Since this model is supposed to demonstrate spread similar to the forest fire model, we can copy the overall structure of our function. However, since we have all of the initial conditions (either set values or randomized), we can create a function to create our initial grid to run before the function determines spread.

**How does disease mortality rate P_survive and early vaccine rates affectdisease spread? What does our simple model tell us about the roles of vaccines in presenting large-scale spread of disease?**

As P_survive increases, fewer people die from the infection and instead develop immunity. This behaves similarly to the effects of a controlled burn. However, in the case of a controlled burn, we can strategically place burnt areas to prevent spread to certain regions. In this model, it is unrealistic to be able to control which cells are set to an immune state. Therefore, P_survive's increase results in fewer cells/people available for infection to spread to and then to their surroundings. While we can't directly control survival like we can a controlled burn, by strategically using vaccines (if quantities are limited) and making sure vaccines are distributed to as many regions of the grid as possible, we can limit the total spread. When looking at the last figure our code produces with the two axes, when P_survive is higher, the aqua immune line rises high above the pink and black infected and dead populations.