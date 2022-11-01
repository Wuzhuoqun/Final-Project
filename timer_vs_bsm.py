import pyfeng as pf
import numpy as np
import timer_mc

n_path = 200000
dt = 1 / 250

sigma, mr, spot, theta, intr = 0.09, 2, 100, 0.09, 0.00
vol_budget = 0.09
vov = 0.125
rho = 0
strike = 100
# for texp in np.linspace(0.1, 5, 30):
texp = 1

m = pf.HestonMcAndersen2008(sigma, vov=vov, mr=mr, rho=rho, theta=theta, intr=intr)
m.set_num_params(n_path=n_path, dt=dt, rn_seed=123456)

cp = 1  # Timer option--call option
m2 = pf.Bsm(sigma=np.sqrt(vol_budget/texp), intr=intr)
price_bsm = m2.price(strike=strike, spot=spot, texp=texp, cp=cp)
print("BSM_price =", price_bsm)

if cp == 1:
    call_or_put = "Call"
else:
    call_or_put = "Put"

condmc = 0  # 0/1 for Simple MC/Conditional MC
for i in range(10):
    print("vov(η)=", vov, "texp(T)=", texp, "rho(ρ)=", rho, "strike(K)=", strike, ": ", " Timer", call_or_put, "Option =",\
          timer_mc.timeroption(vol_budget, model=m).price(spot=spot, strike=strike, texp=texp, cp=cp, condmc=condmc))

condmc = 1  # 0/1 for Simple MC/Conditional MC
for i in range(10):
    print("vov(η)=", vov, "texp(T)=", texp, "rho(ρ)=", rho, "strike(K)=", strike, ": ", " Timer", call_or_put, "Option =",\
          timer_mc.timeroption(vol_budget, model=m).price(spot=spot, strike=strike, texp=texp, cp=cp, condmc=condmc))