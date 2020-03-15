#
# Valuation of European call options in Black-Scholes-Merton Model
# incl. Vega function and implied volatility estimation
# -- class-based implementation
# bsm_option_class.py
#

from numpy import log, sqrt, exp, repeat
from scipy import stats

class call_option(object):
    ''' Class for European call options in BSM model.
    
    Attributes
    ==========
    S0 : float
        initial stock/index level
    K : float
        strike price
    T : float
        maturity (in year fractions)
    r : float
        constant risk-free short rate
    sigma : float
        volatility factor in diffusion term
        
    Methods
    =======
    value : float
        return present value of call option
    vega : float
        return Vega of call option
    imp_vol: float
        return implied volatility given option quote
    '''
    
    def __init__(self, S0, K, T, r, sigma):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        
    def value(self):
        ''' Returns option value. '''
        d1 = ((log(self.S0 / self.K)
            + (self.r + 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        d2 = ((log(self.S0 / self.K)
            + (self.r - 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        value = self.S0 * stats.norm.cdf(d1, 0.0, 1.0) - self.K * exp(-self.r * self.T) * stats.norm.cdf(d2, 0.0, 1.0)
        return value
        
    def vega(self):
        ''' Returns Vega of option. '''

        d1 = ((log(self.S0 / self.K)
            + (self.r + 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))

        vega = self.S0 * stats.norm.pdf(d1, 0.0, 1.0) * sqrt(self.T)
        return vega

    def imp_vol(self, C0, sigma_est=0.2, it=30):
        ''' Returns implied volatility given option price. '''
        try:
            option = call_option(self.S0, self.K, self.T, self.r, repeat(sigma_est,len(self.S0)))
        except:
            option = call_option(self.S0, self.K, self.T, self.r, sigma_est)

        for i in range(it):
            vega = option.vega()
            value = option.value()
            option.sigma = option.sigma - (value - C0) / vega
        return option.sigma


class put_option(object):
    ''' Class for European call options in BSM model.
    
    Attributes
    ==========
    S0 : float
        initial stock/index level
    K : float
        strike price
    T : float
        maturity (in year fractions)
    r : float
        constant risk-free short rate
    sigma : float
        volatility factor in diffusion term
        
    Methods
    =======
    value : float
        return present value of call option
    vega : float
        return Vega of call option
    imp_vol: float
        return implied volatility given option quote
    '''
    
    def __init__(self, S0, K, T, r, sigma):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        
    def value(self):
        ''' Returns option value. '''
        d1 = ((log(self.S0 / self.K)
            + (self.r + 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        d2 = ((log(self.S0 / self.K)
            + (self.r - 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        #print("d1: {}, d2: {}".format(d1,d2))
        value = -1*(self.S0 * stats.norm.cdf(-1*d1, 0.0, 1.0)) + self.K * exp(-self.r * self.T) * stats.norm.cdf(-1*d2, 0.0, 1.0)
        #print("item1: {}, item2: {}".format((self.S0 * stats.norm.cdf(-1*d1, 0.0, 1.0)),self.K * exp(-self.r * self.T) * stats.norm.cdf(-1*d2, 0.0, 1.0)))
        return value
        
    def vega(self):
        ''' Returns Vega of option. '''
        d1 = ((log(self.S0 / self.K)
            + (self.r + 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        vega = self.S0 * stats.norm.pdf(d1, 0.0, 1.0) * sqrt(self.T)
        return vega

    def imp_vol(self, C0, sigma_est=0.2, it=30):
        ''' Returns implied volatility given option price. '''
        try:
            option = put_option(self.S0, self.K, self.T, self.r, repeat(sigma_est,len(self.S0)))
        except:
            option = put_option(self.S0, self.K, self.T, self.r, sigma_est)

        for i in range(it):
            vega = option.vega()
            value = option.value()
            # print("sigma: {}, vega: {}, value: {}".format(option.sigma,vega, value))
            option.sigma -= (value - C0) / vega
            # print(vega, option.sigma)

        return option.sigma
