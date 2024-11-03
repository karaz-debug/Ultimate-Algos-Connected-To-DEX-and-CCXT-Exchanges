import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, crossunder
import matplotlib.pyplot as plt

class MeanReversionStrategy(Strategy):
    # Define strategy parameters
    timeframe = '5m'
    limit = 20
    consolidation_percent = 0.7
    sl_percent = 0.25
    tp_percent = 0.3
    size = 1  # Trade size per order

    def init(self):
        # Initialize indicators
        high = self.data.High
        low = self.data.Low
        close = self.data.Close

        # Calculate True Range (TR)
        tr1 = high - low
        tr2 = (high - close.shift(1)).abs()
        tr3 = (low - close.shift(1)).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        self.tr = tr.rolling(window=self.limit).mean()

        # Calculate deviation percentage
        self.tr_deviance = (self.tr / close) * 100

    def next(self):
        # Ensure that TR deviation is calculated
        if pd.isna(self.tr_deviance[-1]):
            return

        # Current price
        price = self.data.Close[-1]

        # Check for consolidation
        if self.tr_deviance[-1] < self.consolidation_percent:
            # Define consolidation range: last 'limit' candles
            recent_low = self.data.Low[-self.limit:].min()
            recent_high = self.data.High[-self.limit:].max()

            # Calculate lower and upper thirds
            lower_third = recent_low + ((recent_high - recent_low) / 3)
            upper_third = recent_high - ((recent_high - recent_low) / 3)

            # Buy condition: price in lower third
            if price <= lower_third:
                sl_price = price * (1 - (self.sl_percent / 100))
                tp_price = price * (1 + (self.tp_percent / 100))
                self.buy(
                    size=self.size,
                    sl=sl_price,
                    tp=tp_price
                )
                print(f"BUY Order: Price={price:.2f}, SL={sl_price:.2f}, TP={tp_price:.2f}")

            # Sell condition: price in upper third
            elif price >= upper_third:
                sl_price = price * (1 + (self.sl_percent / 100))
                tp_price = price * (1 - (self.tp_percent / 100))
                self.sell(
                    size=self.size,
                    sl=sl_price,
                    tp=tp_price
                )
                print(f"SELL Order: Price={price:.2f}, SL={sl_price:.2f}, TP={tp_price:.2f}")

# Load and prepare data
data_path = 'C:/Users/IQRA/Desktop/Mean_Reversion/ETHUSD_5m.csv'  # Update the path as necessary
data = pd.read_csv(data_path, index_col='timestamp', parse_dates=True)
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
data = data.sort_index()

# Initialize the Backtest
bt = Backtest(
    data,
    MeanReversionStrategy,
    cash=10000,  # Starting with $10,000
    commission=0.002,  # 0.2% commission per trade
    exclusive_orders=True  # Ensures that new orders are not placed before existing ones are closed
)

# Run the backtest
stats = bt.run()
print(stats)

# Plot the backtest results
bt.plot()
