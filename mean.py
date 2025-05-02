import backtrader as bt

class MeanReversion(bt.Strategy):
    def __init__(self):
        # Bollinger Bands with 20-period SMA and 2 standard deviations
        self.boll = bt.indicators.BollingerBands(period=20, devfactor=2)

    def next(self):
        # Buy when price crosses below lower band
        if self.data.close[0] < self.boll.lines.bot[0]:
            self.buy()
        # Sell when price crosses above upper band
        elif self.data.close[0] > self.boll.lines.top[0]:
            self.sell()

# Example usage with CSV data
data = bt.feeds.GenericCSVData(dataname='stock_data.csv')
cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(MeanReversion)
cerebro.run()