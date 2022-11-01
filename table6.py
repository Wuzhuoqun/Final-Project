import pyfeng as pf
import timer

n_path = 200000
dt = 1 / 250

sigma, mr, spot, theta, intr = 0.087, 2, 100, 0.09, 0.015
vol_budget = 0.087  # Li M, Mercurio F (2015). Budget level is constant = 0.087
for vov in [0.125, 0.25, 0.375]:
    for texp in [0.5, 1.0, 1.5,]:
        for rho in [-0.5, 0.5]:
            for strike in [90, 100, 110]:
                m = pf.HestonMcAndersen2008(sigma, vov=vov, mr=mr, rho=rho, theta=theta, intr=intr)
                m.set_num_params(n_path=n_path, dt=dt, rn_seed=123456)

                cp = -1  # Timer option--put option
                print("vov(η)=", vov, "texp(T)=", texp, "rho(ρ)=", rho, "strike(K)=", strike, ": ", \
                      timer.timeroption(vol_budget, model=m).price(spot=spot, strike=strike, texp=texp, cp=cp))
