class VolatilityBreakout(bt.Strategy):
    params = (
        ('atr_period', 14),  # ATR lookback
        ('multiplier', 1.5),  # ATR multiplier
        ('time_exit', 18)  # Exit at 6pm UTC (crypto)
    )

    def __init__(self):
        self.atr = bt.indicators.ATR(period=self.p.atr_period)
        self.range_high = self.data.high[-1] + self.atr[0] * self.p.multiplier
        self.range_low = self.data.low[-1] - self.atr[0] * self.p.multiplier

    def next(self):
        # Entry logic
        if not self.position:
            if self.data.close[0] > self.range_high:
                self.buy()
            elif self.data.close[0] < self.range_low:
                self.sell()

        # Daily exit
        if self.data.datetime.time().hour >= self.p.time_exit:
            self.close()