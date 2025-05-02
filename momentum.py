class MomentumStrategy(bt.Strategy):
    params = (
        ('fast_ma', 10),  # Fast moving average period
        ('slow_ma', 30),  # Slow moving average period
        ('volume_threshold', 1.5)  # 150% of average volume
    )

    def __init__(self):
        # Trend indicators
        self.fast_ma = bt.indicators.SMA(period=self.p.fast_ma)
        self.slow_ma = bt.indicators.SMA(period=self.p.slow_ma)

        # Volume filter
        self.vol_avg = bt.indicators.SMA(
            self.data.volume, period=20
        )

    def next(self):
        # Buy signal: Fast MA above Slow MA + high volume
        if (self.fast_ma[0] > self.slow_ma[0] and
                self.data.volume[0] > self.vol_avg[0] * self.p.volume_threshold):
            self.buy()

        # Sell signal: Fast MA crosses below Slow MA
        elif self.fast_ma[0] < self.slow_ma[0]:
            self.sell()