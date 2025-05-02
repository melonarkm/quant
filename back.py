import backtrader as bt

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        # Short-term (10 periods) and long-term (30 periods) SMA
        sma1 = bt.ind.SMA(period=10)
        sma2 = bt.ind.SMA(period=30)
        # Buy signal when short-term SMA crosses above long-term SMA
        self.signal_add(bt.SIGNAL_LONG, sma1 > sma2)

# Load Apple stock data from Yahoo Finance
data = bt.feeds.YahooFinanceData(dataname='AAPL', fromdate=datetime(2020, 1, 1), todate=datetime(2023, 1, 1))
cerebro = bt.Cerebro()
cerebro.adddata(data)       # Add data feed
cerebro.addstrategy(SmaCross)  # Add strategy
cerebro.run()               # Run backtest
cerebro.plot()              # Visualize results