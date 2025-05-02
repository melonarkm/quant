class VWAPStrategy(bt.Strategy):
    params = (
        ('vwap_dev', 0.01),  # 1% deviation threshold
        ('trail_dist', 0.005)  # 0.5% trailing stop
    )

    def __init__(self):
        self.vwap = bt.indicators.VWAP(self.data)
        self.trailing_stop = 0

    def next(self):
        price = self.data.close[0]

        # Long entry: Price > VWAP + threshold
        if price > self.vwap[0] * (1 + self.p.vwap_dev):
            self.buy()
            self.trailing_stop = price * (1 - self.p.trail_dist)

        # Update trailing stop
        if self.position:
            self.trailing_stop = max(
                self.trailing_stop,
                price * (1 - self.p.trail_dist)
            )

            # Exit if price hits trailing stop
            if price <= self.trailing_stop:
                self.close()