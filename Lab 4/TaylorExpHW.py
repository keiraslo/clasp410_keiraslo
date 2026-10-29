'''
Review  the definition for Taylor series expansions.

Find the first four terms of the Maclaurin series (Taylor series expansions about 
(x=0) for the following expressions 

1) f(x) = e^x (sinx)
2) f(x) = (e^x)/1-x
3) f(x) = e^sinx
'''

# First four nonzero terms of each Maclaurin series:
# 1) e^x sin(x) = x + x^2 + x^3/3 - x^5/30 + ...
# 2) e^x/(1 - x) = 1 + 2x + 5x^2/2 + 8x^3/3 + ...
# 3) e^sin(x) = 1 + x + x^2/2 - x^4/8 + ...

import sympy as sp

x = sp.symbols("x")
functions = [
	sp.exp(x) * sp.sin(x),
	sp.exp(x) / (1 - x),
	sp.exp(sp.sin(x)),
]

# Expand far enough to include the first four nonzero terms of each series.
orders = [6, 4, 5]
for number, (function, order) in enumerate(zip(functions, orders), start=1):
	print(f"{number}) {sp.series(function, x, 0, order)}")

