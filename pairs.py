import statsmodels.api as sm


class PairsTradingStrategy(bt.Strategy):
    params = (
        ('lookback', 30),  # Cointegration test period
        ('z_entry', 2.0),  # Entry Z-score threshold
        ('z_exit', 0.5)  # Exit Z-score threshold
    )

    def __init__(self):
        self.spread = self.data0.close - self.data1.close  # Asset A - Asset B
        self.zscore = bt.indicators.StdDev(self.spread) / self.spread.mean()

    def next(self):
        # Long spread (buy A/sell B) when zscore < -entry threshold
        if self.zscore < -self.p.z_entry:
            self.order_target_percent(data=self.data0, target=0.5)  # 50% in A
            self.order_target_percent(data=self.data1, target=-0.5)  # -50% in B

        # Close positions when zscore reverts
        elif abs(self.zscore) < self.p.z_exit:
            self.close(self.data0)
            self.close(self.data1)