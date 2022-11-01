import pyfeng as pf
import numpy as np
import timer

n_path = 200000
dt = 1 / 100

sigma, mr, spot, theta, intr = 0.09, 2, 100, 0.09, 0.015
vol_budget = 0.087
vov = 0.125
rho = 0
strike = 100
for texp in np.linspace(1, 6, 5):
    m = pf.HestonMcAndersen2008(sigma, vov=vov, mr=mr, rho=rho, theta=theta, intr=intr)
    m.set_num_params(n_path=n_path, dt=dt, rn_seed=123456)

    cp = 1  # Timer optio   n--call option
    print("vov(η)=", vov, "texp(T)=", texp, "rho(ρ)=", rho, "strike(K)=", strike, ": ", \
          timer.timeroption(vol_budget, model=m).price(spot=spot, strike=strike, texp=texp, cp=cp))

    m2 = pf.Bsm(sigma=np.sqrt(vol_budget/texp), intr=intr)
    price_bsm = m2.price(strike=strike, spot=spot, texp=texp)
    print(price_bsm)