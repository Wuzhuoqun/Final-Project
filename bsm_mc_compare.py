import pyfeng as pf
import numpy as np
import timer

n_path = 200000
dt = 1 / 100

sigma, mr, spot, theta, intr = 0.09, 2, 100, 0.09, 0.00
vol_budget = 0.09
vov = 0.125
rho = 0
strike = 100
# for texp in np.linspace(0.1, 5, 30):
texp = 4