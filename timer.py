import numpy as np

class timeroption:
    """
    Timer Option model for option pricing.
    Underlying variance is assumed to follow Heston model.
    """
    def __init__(self, vol_budget, model, n_path=200000, dt=1/250):
        self.vol_budget = vol_budget
        self.model = model
        self.n_path = n_path
        self.dt = dt

    def price(self, spot, strike, texp, cp=1):
        """
        Heston model timer option Price

        Args:
            strike: strike price
            spot: spot (or forward)
            sigma: model volatility
            texp: time to expiry
            cp: 1/-1 for call/put option
            sigma: model volatility
            intr: interest rate (domestic interest rate)
            divr: dividend/convenience yield (foreign interest rate)
        Returns:
            Timer option price
        """
        n_dt = int(texp/self.dt)
        dt = texp / n_dt

        var_t1 = np.full(self.n_path, self.model.sigma)
        intvar = np.zeros_like(var_t1)
        s_t = np.ones(self.n_path) * spot
        payout = np.zeros(self.n_path)

        for i in range(n_dt-1):
            var_t2, avgvar_inc, *_ = self.model.cond_states_step(dt, var_t1)
            log_rt = self.model.draw_log_return(dt, var_t1, var_t2, avgvar_inc)
            s_t *= np.exp(log_rt)
            var_t1 = var_t2

            intvar += avgvar_inc * dt
            # Check if intvar exceeds the budget.
            # If exceeds, fix the payout.
            payout = np.exp(-self.model.intr * dt * (i+1)) * np.maximum(cp*(s_t-strike) * (intvar > self.vol_budget), 0) * (payout == 0) + 123456 * (cp*(s_t - strike) < 0) * (intvar > self.vol_budget) * (payout == 0) + payout
        
        var_t2, avgvar_inc, *_ = self.model.cond_states_step(dt, var_t1)
        log_rt = self.model.draw_log_return(dt, var_t1, var_t2, avgvar_inc)
        s_t *= np.exp(log_rt)
        payout = np.exp(-self.model.intr * dt * n_dt) * np.maximum(cp*(s_t - strike), 0) * (payout == 0) + 123456 * (cp*(s_t - strike) < 0) * (intvar > self.vol_budget) * (payout == 0) + payout

        payout = payout * (payout != 123456)
        price = np.mean(payout)

        return price