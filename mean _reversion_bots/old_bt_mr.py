import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import yfinance as yf  # Ensure yfinance is installed: pip install yfinance

# Custom function to calculate rolling standard deviation
def STD(values, n):
    """
    Calculates the rolling standard deviation.

    Parameters:
    - values (np.array): Array of price values.
    - n (int): Window size for rolling calculation.

    Returns:
    - np.array: Rolling standard deviation.
    """
    return pd.Series(values).rolling(n).std().values
def SMA(values, n):
    """
    Calculates the Simple Moving Average (SMA).

    Parameters:
    - values (np.array): Array of price values.
    - n (int): Window size for the moving average.

    Returns:
    - np.array: Simple Moving Average.
    """
    return pd.Series(values).rolling(n).mean().values

class MeanReversionStrategy(Strategy):
    # Strategy parameters
    ma_window = 22            # Window for moving average
    std_dev_multiplier = 2    # Multiplier for standard deviation bands
    trend_ma_window = 50      # Window for trend moving average

    def init(self):
        """
        Initialize the indicators used in the strategy.
        This method is called once at the start of the backtest.
        """
        # Calculate the Simple Moving Average (SMA)
        self.ma = self.I(SMA, self.data.Close, self.ma_window)
        
        # Calculate the rolling Standard Deviation (STD)
        self.std = self.I(STD, self.data.Close, self.ma_window)
        
        # Calculate the upper and lower standard deviation bands
        self.upper_band = self.ma + self.std * self.std_dev_multiplier
        self.lower_band = self.ma - self.std * self.std_dev_multiplier
        
        # Calculate the trend moving average (for trend confirmation)
        self.trend_ma = self.I(SMA, self.data.Close, self.trend_ma_window)

    def next(self):
        """
        Defines the trading logic executed at each step of the backtest.
        """
        # Current price
        price = self.data.Close[-1]
        
        # Current indicator values
        ma = self.ma[-1]
        upper_band = self.upper_band[-1]
        lower_band = self.lower_band[-1]
        trend_ma = self.trend_ma[-1]

        # If no open position, check for entry signals
        if not self.position:
            # Long Entry Condition:
            # - Price is below the lower band (oversold)
            # - Price is above the trend moving average (uptrend)
            if price < lower_band and price > trend_ma:
                self.buy()
            
            # Short Entry Condition:
            # - Price is above the upper band (overbought)
            # - Price is below the trend moving average (downtrend)
            elif price > upper_band and price < trend_ma:
                self.sell()
        
        else:
            # If in a long position, check for exit condition
            if self.position.is_long and price >= ma:
                self.position.close()
            
            # If in a short position, check for exit condition
            elif self.position.is_short and price <= ma:
                self.position.close()



# Function to load your data with the desired timeframe
# C:\Users\IQRA\Desktop\Mean_Reversion.BTCUSDT_15m.csv
# data_path = 'C:/Users/IQRA/Desktop/Mean_Reversion/BTCUSDT.csv' - failed 15min also failed
# C:\Users\IQRA\Desktop\Mean_Reversion\EURUSD_X_hourly.csv
# C:\Users\IQRA\Desktop\Mean_Reversion\GBPUSD_X_hourly.csv
data_path = 'C:/Users/IQRA/Desktop/Mean_Reversion/GBPUSD_X_hourly.csv' 
# data_path = 'C:/Users/IQRA/Desktop/Mean_Reversion/WIFUSDT_4h.csv' - #failed
# data_path = 'C:/Users/IQRA/Desktop/Mean_Reversion/SOLUSDT.csv' - failed
data = pd.read_csv(data_path, index_col=0, parse_dates=True)

#Rename the columns
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

## Sort the data
data = data.sort_index()

bt = Backtest(data, MeanReversionStrategy, cash=10000, commission=.002)
stats = bt.run()
print(stats)
bt.plot()

# List of timeframes to test
# timeframes = ['15m', '30m', '60m', '4h']

# for tf in timeframes:
#     print(f"\nBacktesting for timeframe: {tf}")
#     data = load_data(timeframe=tf)
#     bt = Backtest(data, MeanReversionStrategy, cash=10000, commission=.002)
#     stats = bt.run()
#     print(stats)
#     bt.plot()


#EUR USD TERABLY FAILING TOO
# Start                     2022-09-29 15:00:00
# End                       2024-09-27 22:00:00
# Duration                    729 days 07:00:00
# Exposure Time [%]                    9.395484
# Equity Final [$]                  8219.934423
# Equity Peak [$]                       10000.0
# Return [%]                         -17.800656
# Buy & Hold Return [%]               14.317616
# Return (Ann.) [%]                   -9.029211
# Volatility (Ann.) [%]                2.504918
# Sharpe Ratio                              0.0
# Sortino Ratio                             0.0
# Calmar Ratio                              0.0
# Max. Drawdown [%]                  -17.966173
# Avg. Drawdown [%]                  -17.966173
# Max. Drawdown Duration      723 days 11:00:00
# Avg. Drawdown Duration      723 days 11:00:00
# # Trades                                   61
# Win Rate [%]                        14.754098
# Best Trade [%]                       0.314834
# Worst Trade [%]                      -2.38542
# Avg. Trade [%]                      -0.320851
# Max. Trade Duration           4 days 01:00:00
# Avg. Trade Duration           1 days 07:00:00
# Profit Factor                        0.054866
# Expectancy [%]                      -0.319786
# SQN                                 -5.203414
# _strategy                 MeanReversionStr...
# _equity_curve                             ...
# _trades                        Size  Entry...
# dtype: object

#GBPUSD TO ALSO FAILING BADLY
# Start                     2022-09-29 15:00:00
# End                       2024-09-27 22:00:00
# Duration                    729 days 07:00:00
# Exposure Time [%]                    8.699523
# Equity Final [$]                  8488.448884
# Equity Peak [$]                  10013.020846
# Return [%]                         -15.115511
# Buy & Hold Return [%]               21.233602
# Return (Ann.) [%]                   -7.606532
# Volatility (Ann.) [%]                2.467812
# Sharpe Ratio                              0.0
# Sortino Ratio                             0.0
# Calmar Ratio                              0.0
# Max. Drawdown [%]                  -15.392088
# Avg. Drawdown [%]                   -3.460961
# Max. Drawdown Duration      700 days 20:00:00
# Avg. Drawdown Duration      141 days 20:00:00
# # Trades                                   56
# Win Rate [%]                        23.214286
# Best Trade [%]                       0.628166
# Worst Trade [%]                     -2.283636
# Avg. Trade [%]                      -0.292232
# Max. Trade Duration           4 days 14:00:00
# Avg. Trade Duration           1 days 03:00:00
# Profit Factor                        0.112054
# Expectancy [%]                      -0.291019
# SQN                                 -4.238189
# _strategy                 MeanReversionStr...
# _equity_curve                             ...
# _trades                       Size  EntryB...
# dtype: object