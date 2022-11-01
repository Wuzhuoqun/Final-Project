import numpy as np
import pyfeng as pf


class timeroption:
    """
    Timer Option model for option pricing.
    Underlying variance is assumed to follow Heston model.
    Underlying St is assumed to follow BSM model.
    """

    def __init__(self, vol_budget, model, n_path=200000, dt=1 / 250):
        self.vol_budget = vol_budget
        self.model = model
        self.n_path = n_path
        self.dt = dt

    def price(self, spot, strike, texp, cp=1, condmc=0):
        """
        Heston model timer option Price

        Args:
            strike: strike price
            spot: spot (or forward)
            sigma: model volatility
            texp: time to expiry
            cp: 1/-1 for call/put option
            intr: interest rate (domestic interest rate)
            condmc: 1/0 for conditional MC/simple MC
        Returns:
            Timer option price
        """
        n_dt = int(texp / self.dt)
        dt = texp / n_dt

        var_t1 = np.full(self.n_path, self.model.sigma)
        intvar = np.zeros_like(var_t1)
        s_t = np.ones(self.n_path) * spot

        if condmc == 0:
            payout = np.zeros(self.n_path)
            """
            Simple MC
            """
            for i in range(n_dt - 1):
                var_t2, avgvar_inc, *_ = self.model.cond_states_step(dt, var_t1)
                log_rt = self.model.draw_log_return(dt, var_t1, var_t2, avgvar_inc)
                s_t *= np.exp(log_rt)
                var_t1 = var_t2

                intvar += avgvar_inc * dt
                # Check if intvar exceeds the budget.
                # If exceeds, fix the payout.
                # 123456 is used to indicate the condition when intvar exceeds the budget while timer option price is 0
                payout = np.exp(-self.model.intr * dt * (i + 1)) * np.maximum(
                    cp * (s_t - strike) * (intvar > self.vol_budget), 0) * (payout == 0) \
                         + 123456 * (cp * (s_t - strike) < 0) * (intvar > self.vol_budget) * (payout == 0) + payout

            var_t2, avgvar_inc, *_ = self.model.cond_states_step(dt, var_t1)
            log_rt = self.model.draw_log_return(dt, var_t1, var_t2, avgvar_inc)
            s_t *= np.exp(log_rt)
            payout = np.exp(-self.model.intr * dt * n_dt) * np.maximum(cp * (s_t - strike), 0) * (payout == 0) \
                     + 123456 * (cp * (s_t - strike) < 0) * (intvar > self.vol_budget) * (payout == 0) + payout

            payout = payout * (payout != 123456)
            price = np.mean(payout)

        else:
            """
            Conditional MC (St follows BSM)
            """
            # hit_record keeps a record of history hittings.
            # hit_at_dt records a new hit over budget level.
            hit_record = np.full(self.n_path, False)
            hit_at_dt = np.full(self.n_path, False)
            var_0 = np.full(self.n_path, self.model.sigma)
            payout_sum = 0
            for i in range(n_dt - 1):
                var_t2, avgvar_inc, *_ = self.model.cond_states_step(dt, var_t1)
                var_t1 = var_t2

                intvar += avgvar_inc * dt
                # Check if intvar exceeds the budget.
                # If exceeds, extract the payout using Conditional MC.
                hit_at_dt = hit_at_dt * 0
                if (intvar > self.vol_budget).any():
                    hit_at_dt = np.logical_xor(np.logical_or((intvar > self.vol_budget), hit_record), hit_record)
                if hit_at_dt.any():
                    texp_at_dt = dt * (i + 1)
                    var_t_at_dt = var_t2[hit_at_dt]
                    var_0_at_dt = var_0[hit_at_dt]
                    intvar_at_dt = intvar[hit_at_dt]
                    payout = self.price_condmc(spot=spot, strike=strike, texp=texp_at_dt,
                                               var_t=var_t_at_dt, var_0=var_0_at_dt, intvar=intvar_at_dt, cp=cp)
                    payout_sum += np.sum(payout)
                    hit_record = np.logical_or(hit_record, hit_at_dt)

            var_t2, avgvar_inc, *_ = self.model.cond_states_step(dt, var_t1)
            intvar += avgvar_inc * dt

            var_t_at_dt = var_t2[~hit_record]
            var_0_at_dt = var_0[~hit_record]
            intvar_at_dt = intvar[~hit_record]
            payout = self.price_condmc(spot=spot, strike=strike, texp=texp,
                                       var_t=var_t_at_dt, var_0=var_0_at_dt, intvar=intvar_at_dt, cp=cp)
            payout_sum += np.sum(payout)
            price = payout_sum / self.n_path
        return price

    def price_condmc(self, spot, strike, texp, var_t, var_0, intvar, cp):
        spot_cond = spot * np.exp(
            (self.model.rho / self.model.vov * (var_t - var_0 + self.model.mr * (intvar - self.model.theta * texp)) \
             - 1 / 2 * (self.model.rho ** 2) * intvar))
        sigma_cond = np.sqrt((1.0 - self.model.rho ** 2) * intvar / texp)
        m_bsm = pf.Bsm(sigma=sigma_cond, intr=self.model.intr)
        price = m_bsm.price(strike=strike, spot=spot_cond, texp=texp, cp=cp)
        return price
