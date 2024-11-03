import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from backtesting import Backtest, Strategy
from backtesting.test import SMA


class SMABuySellStrategy(Strategy):
    sma_period = 14  #Defaul SMA period will be optimized
    buy_pct = 1.0    # Default buy percentage below SMA will  be optimized
    sell_pct = 1.0   # Default sell percentage above SMA will be optimized  

    def init(self):
        #Caluclate the moving average
        self.sma = self.I(SMA, self.data.Close, self.sma_period)

    def next(self):
        #Calculate the buy and sell thresholds
        buy_threshold = self.sma[-1] * (1 - self.buy_pct / 100)
        sell_threshold = self.sma[-1] * (1 + self.sell_pct / 100)

        #Buy if the price is below the buy threshold
        if len(self.data.Close) > 0 and self.data.Close[-1] < buy_threshold:
            self.buy()
        # if close price is above the sell threshold, sell
        elif len(self.data.Close) > 0 and self.data.Close[-1] > sell_threshold:
            self.position.close()

#Load the data
data_path = 'C:/Users/IQRA/Desktop/Mean_Reversion/WIFUSDT_4h.csv'
data = pd.read_csv(data_path, index_col=0, parse_dates=True)
print("Columns in the DataFrame:", data.columns)

# Correct the column names by selecting the right columns with correct capitalization
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]


#Sort the data index in ascending order
# data = data.sort_values(by='timestamp')
data = data.sort_index()


#Create the backtest
bt = Backtest(data, SMABuySellStrategy, cash=1000000, commission=0.002)

#Optimize the strategy
opt_stats, heatmap = bt.optimize(
    sma_period=range(10, 30),             # Test between 10 and 50
    buy_pct=range(10, 25),                # Test between 1% and 10%
    sell_pct=range(10, 25),  
    maximize= 'Equity Final [$]',         # Test between 1% and 10%
    constraint= lambda param: param.sma_period > 0 and param.buy_pct > 0 and param.sell_pct > 0,
    return_heatmap=True
)

#print the optimization results
print(f'here the optimized stat {opt_stats}')

#Convert the heatmap to a DataFrame 
heatmap_df = heatmap.unstack(level = 'buy_pct').T

#Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_df, annot=True, fmt='.2f', cmap='viridis')
plt.title('Optimization Heatmap')
plt.xlabel('Sell Percentage (%)')
plt.ylabel('Buy Percentage (%)')
plt.show()

#Run the backtest with the optimized parameters
results = bt.run(sma_period=opt_stats.sma_period, buy_pct=opt_stats.buy_pct, sell_pct=opt_stats.sell_pct)
print(f'here the optimized results {results}')
print(f'here are the best paramters SMA: {opt_stats.opt_stats.sma_period} BUY PT: {opt_stats.opt_stats.buy_pct} SELL PT: {opt_stats.opt_stats.sell_pct}')

#Plot the backtest results
bt.plot()

## SOLANA 
# End                       2024-09-23 16:00:00
# Duration                    388 days 16:00:00
# Exposure Time [%]                   77.796828
# Equity Final [$]                3241478.29378
# Equity Peak [$]                 4677436.81378
# Return [%]                         224.147829
# Buy & Hold Return [%]              622.875817
# Return (Ann.) [%]                  201.461582
# Volatility (Ann.) [%]              276.751857
# Sharpe Ratio                          0.72795
# Sortino Ratio                        4.189444
# Calmar Ratio                         4.550606
# Max. Drawdown [%]                  -44.271373
# Avg. Drawdown [%]                   -6.080646
# Max. Drawdown Duration      189 days 08:00:00
# Avg. Drawdown Duration        7 days 18:00:00
# # Trades                                    3
# Win Rate [%]                            100.0
# Best Trade [%]                      124.56539
# Worst Trade [%]                     44.345211
# Avg. Trade [%]                      79.833836
# Max. Trade Duration         270 days 00:00:00
# Avg. Trade Duration         182 days 03:00:00
# Profit Factor                             NaN
# Expectancy [%]                      82.776615
# SQN                                  1.963902
# _strategy                 SMABuySellStrate...
# _equity_curve                             ...
# _trades                       Size  EntryB...
# dtype: object


#WIF 
# End                       2024-09-23 16:00:00
# Duration                    202 days 04:00:00
# Exposure Time [%]                   32.701812
# Equity Final [$]               5525378.462789
# Equity Peak [$]                5525378.462789
# Return [%]                         452.537846
# Buy & Hold Return [%]               30.868457
# Return (Ann.) [%]                 2061.667398
# Volatility (Ann.) [%]             3970.057754
# Sharpe Ratio                         0.519304
# Sortino Ratio                       39.285242
# Calmar Ratio                        59.328513
# Max. Drawdown [%]                  -34.750026
# Avg. Drawdown [%]                  -10.420345
# Max. Drawdown Duration       34 days 00:00:00
# Avg. Drawdown Duration        4 days 21:00:00
# # Trades                                    6
# Win Rate [%]                            100.0
# Best Trade [%]                      75.521292
# Worst Trade [%]                     33.067199
# Avg. Trade [%]                      46.032212
# Max. Trade Duration          46 days 08:00:00
# Avg. Trade Duration          18 days 11:00:00
# Profit Factor                             NaN
# Expectancy [%]                       46.68949
# SQN                                    3.5813
# _strategy                 SMABuySellStrate...
# _equity_curve                             ...
# _trades                         Size  Entr...
# dtype: object



