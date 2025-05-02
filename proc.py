"""
quant_trading_strategy.py

A sample quantitative trading strategy demonstrating:
- Data fetching
- Technical indicator calculation
- Strategy logic
- Backtesting
- Performance visualization

This implements a Dual Moving Average Crossover strategy.
"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


# Technical Indicator Functions
def SMA(series, window):
    """
    Calculate Simple Moving Average

    Parameters:
    series (pd.Series): Price series to calculate SMA on
    window (int): Rolling window size

    Returns:
    pd.Series: SMA values
    """
    return series.rolling(window).mean()


class MovingAverageCrossover(Strategy):
    """
    Dual Moving Average Crossover Strategy

    Rules:
    1. Buy when short-term MA crosses above long-term MA (golden cross)
    2. Sell when short-term MA crosses below long-term MA (death cross)
    3. All-in, all-out position sizing
    """

    # Strategy parameters (optimizable)
    short_window = 50  # Short-term moving average window
    long_window = 200  # Long-term moving average window

    def init(self):
        """
        Initialize strategy. Called once before backtesting starts.
        Used to precompute indicators.
        """
        close = self.data.Close  # Closing price series

        # Precompute indicators
        self.short_ma = self.I(SMA, close, self.short_window)
        self.long_ma = self.I(SMA, close, self.long_window)

        # For visualization
        self.buy_signals = []
        self.sell_signals = []

    def next(self):
        """
        Main strategy logic. Called for each candle (data point).
        """
        current_position = self.position.size  # Current position size

        # Generate signals
        golden_cross = crossover(self.short_ma, self.long_ma)
        death_cross = crossover(self.long_ma, self.short_ma)

        # Trading logic
        if golden_cross and current_position <= 0:
            # Buy signal: Close any short position and go long
            if current_position < 0:
                self.position.close()
            self.buy()
            self.buy_signals.append(self.data.index[-1])

        elif death_cross and current_position >= 0:
            # Sell signal: Close any long position and go short
            if current_position > 0:
                self.position.close()
            self.sell()
            self.sell_signals.append(self.data.index[-1])


def fetch_data(ticker, start_date, end_date):
    """
    Fetch historical price data from Yahoo Finance

    Parameters:
    ticker (str): Stock symbol (e.g., 'AAPL')
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format

    Returns:
    pd.DataFrame: OHLCV data
    """
    print(f"Downloading data for {ticker}...")
    data = yf.download(ticker, start=start_date, end=end_date)
    data.dropna(inplace=True)
    return data


def analyze_results(bt):
    """
    Analyze and visualize backtest results

    Parameters:
    bt: Backtest results object
    """
    # Print key performance metrics
    print("\nStrategy Performance:")
    print(f"Return: {bt.stats['Return [%]']:.2f}%")
    print(f"Sharpe Ratio: {bt.stats['Sharpe Ratio']:.2f}")
    print(f"Max Drawdown: {bt.stats['Max. Drawdown [%]']:.2f}%")

    # Plot equity curve
    bt.plot()


if __name__ == "__main__":
    # Configuration
    TICKER = "AAPL"  # Stock to trade
    START_DATE = "2020-01-01"  # Backtest start date
    END_DATE = "2023-01-01"  # Backtest end date
    COMMISSION = 0.001  # Broker commission (0.1%)

    # Step 1: Fetch historical data
    price_data = fetch_data(TICKER, START_DATE, END_DATE)

    # Step 2: Initialize and run backtest
    bt = Backtest(
        price_data,
        MovingAverageCrossover,
        commission=COMMISSION,
        exclusive_orders=True
    )

    # Step 3: Run backtest
    results = bt.run()

    # Step 4: Analyze results
    analyze_results(results)

    # Optional: Parameter optimization
    # print("\nRunning optimization...")
    # opt_results = bt.optimize(
    #     short_window=range(10, 60, 5),
    #     long_window=range(50, 250, 20),
    #     maximize='Sharpe Ratio'
    # )