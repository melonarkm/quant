import backtrader as bt

class RsiStrategy(bt.Strategy):
    def __init__(self):
        # Initialize RSI indicator with 14-day period
        self.rsi = bt.indicators.RSI(period=14)

    def next(self):
        # Buy when RSI < 30 (oversold)
        if self.rsi < 30:
            self.buy()
        # Sell when RSI > 70 (overbought)
        elif self.rsi > 70:
            self.sell()

# Backtest setup
data = bt.feeds.YahooFinanceData(dataname='BTC-USD', fromdate=datetime(2021, 1, 1))
cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(RsiStrategy)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())