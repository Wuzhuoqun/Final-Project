import pyfeng as pf
import timer
import numpy as np

n_path = 200000
dt = 1 / 250

sigma, mr, spot, theta, intr = 0.087, 2, 100, 0.09, 0.015
vol_budget = 0.087  # Li M, Mercurio F (2015). Budget level is constant = 0.087


# for vov in [0.125, 0.25, 0.375]:
#     for texp in [0.5, 1.0, 1.5, 2.0, 10.0]:
#         for rho in [0]:
#             for strike in [90, 100, 110]:
#                 m = pf.HestonMcAndersen2008(sigma, vov=vov, mr=mr, rho=rho, theta=theta, intr=intr)
#                 m.set_num_params(n_path=n_path, dt=dt, rn_seed=123456)
#
#                 cp = 1  # Timer option--call option
#                 print("vov(η)=", vov, "texp(T)=", texp, "rho(ρ)=", rho, "strike(K)=", strike, ": ", \
#                       timer.timeroption(vol_budget, model=m).price(spot=spot, strike=strike, texp=texp, cp=cp))

# rho = 0
# for vov in [0.125, 0.25, 0.375]:
#     for texp in [0.5, 1.0, 1.5, 2.0, 10.0]:
#         for strike in [90, 100, 110]:
#             import pyfeng as pf
#             import timer
#             import numpy as np

n_path = 200000
dt = 1 / 250

sigma, mr, spot, theta, intr = 0.087, 2, 100, 0.09, 0.015
vol_budget = 0.087  # Li M, Mercurio F (2015). Budget level is constant = 0.087

vov = np.array([0.125, 0.25, 0.375])
texp = np.array([0.5, 1.0, 1.5, 2.0, 10.0])
strike = np.array([90, 100, 110])

            # for vov in [0.125, 0.25, 0.375]:
            #     for texp in [0.5, 1.0, 1.5, 2.0, 10.0]:
            #         for rho in [0]:
            #             for strike in [90, 100, 110]:
            #                 m = pf.HestonMcAndersen2008(sigma, vov=vov, mr=mr, rho=rho, theta=theta, intr=intr)
            #                 m.set_num_params(n_path=n_path, dt=dt, rn_seed=123456)
            #
            #                 cp = 1  # Timer option--call option
            #                 print("vov(η)=", vov, "texp(T)=", texp, "rho(ρ)=", rho, "strike(K)=", strike, ": ", \
            #                       timer.timeroption(vol_budget, model=m).price(spot=spot, strike=strike, texp=texp, cp=cp))

rho = 0
cp = 1
x = np.zeros([5,3,3])

for i in range(len(texp)):
    print('T =%s:\n' % texp(i) )
    for j in range(len(strike)):
        for k in range(len(vov)):
            m = pf.HestonMcAndersen2008(sigma, vov=vov[k], mr=mr, rho=rho, theta=theta, intr=intr)
            m.set_num_params(n_path=n_path, dt=dt, rn_seed=123456)
            cp = 1
            x[j][k][i] = timer.timeroption(vol_budget, model=m).price(spot=spot, strike=strike[j], texp=texp[1], cp=cp)
            print(x[i][j][k])

                    # for k in range(len(strike)):
                    #     m = pf.HestonMcAndersen2008(sigma, vov=vov[i], mr=mr, rho=rho, theta=theta, intr=intr)
                    #     m.set_num_params(n_path=n_path, dt=dt, rn_seed=123456)
                    #     cp = 1
                    #     x[0][k][i] = timer.timeroption(vol_budget, model=m).price(spot=spot, strike=strike[k],
                    #                                                               texp=texp[j], cp=cp)