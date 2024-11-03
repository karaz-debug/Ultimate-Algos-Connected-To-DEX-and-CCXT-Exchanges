import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, crossunder
import matplotlib.pyplot as plt

# Define file paths for ETH and altcoins
eth_file = 'ETH-USD.csv'
alt_files = {
    'ADAUSD': 'ADAUSD.csv',
    'DOTUSD': 'DOTUSD.csv',
    'MANAUSD': 'MANAUSD.csv',
    'XRPUSD': 'XRPUSD.csv',
    'UNIUSD': 'UNIUSD.csv',
    'SOLUSD': 'SOLUSD.csv'
}

# Load ETH data
eth_df = pd.read_csv(eth_file, parse_dates=['timestamp'])
eth_df.set_index('timestamp', inplace=True)
eth_df = eth_df.sort_index()

# Rename ETH columns to include prefix
eth_df.rename(columns=lambda x: f'ETH_{x}', inplace=True)

# Initialize merged DataFrame with ETH data
merged_df = eth_df.copy()

# Load and merge altcoin data
for coin, file in alt_files.items():
    df = pd.read_csv(file, parse_dates=['timestamp'])
    df.set_index('timestamp', inplace=True)
    df = df.sort_index()
    # Keep only the 'close' price for simplicity
    df = df[['close']].rename(columns={'close': f'{coin}_Close'})
    # Merge with the main DataFrame
    merged_df = merged_df.join(df, how='inner')  # Use inner join to ensure synchronized timestamps

# Drop any rows with missing values
merged_df.dropna(inplace=True)

# Define strategy parameters
timeframe = '15T'  # 15-minute intervals
dataRange = 20  # Number of candles to consider for indicators
sl_percent = 0.2  # Stop loss percentage
tp_percent = 0.25  # Take profit percentage
size = 1  # Trade size (adjust as needed)

# Calculate True Range (TR) and Average True Range (ATR) for ETH
eth_high = merged_df['ETH_high']
eth_low = merged_df['ETH_low']
eth_close = merged_df['ETH_close']

# Calculate True Range
tr1 = eth_high - eth_low
tr2 = (eth_high - eth_close.shift(1)).abs()
tr3 = (eth_low - eth_close.shift(1)).abs()
tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

# Calculate ATR
merged_df['ETH_ATR'] = tr.rolling(window=dataRange).mean()

# Calculate Support and Resistance
merged_df['ETH_Support'] = eth_low.rolling(window=dataRange).min()
merged_df['ETH_Resistance'] = eth_high.rolling(window=dataRange).max()

# Calculate percentage change for each altcoin over the last 'dataRange' candles
for coin in alt_files.keys():
    merged_df[f'{coin}_Change'] = merged_df[f'{coin}_Close'].pct_change(periods=dataRange) * 100

# Reset index to have 'timestamp' as a column
merged_df.reset_index(inplace=True)

# Set 'timestamp' as the index again (required by backtesting.py)
merged_df.set_index('timestamp', inplace=True)

# Ensure data is sorted
merged_df.sort_index(inplace=True)

class CorrelationAltcoinStrategy(Strategy):
    def init(self):
        # Initialize indicators
        self.atr = self.data.ETH_ATR
        self.support = self.data.ETH_Support
        self.resistance = self.data.ETH_Resistance

        # Initialize a variable to track the currently open altcoin position
        self.open_position = None

    def next(self):
        # Skip if ATR or support/resistance is not available
        if pd.isna(self.atr[-1]) or pd.isna(self.support[-1]) or pd.isna(self.resistance[-1]):
            return

        # Current ETH price
        current_eth_price = self.data.ETH_close[-1]

        # Conditions for Buy and Sell
        trigger_buy = current_eth_price > (self.data.ETH_close[-2] + self.atr[-1]) or current_eth_price > self.resistance[-1]
        trigger_sell = current_eth_price < (self.data.ETH_close[-2] - self.atr[-1]) or current_eth_price < self.support[-1]

        # If no open position, evaluate to open a new one
        if not self.position:
            if trigger_buy or trigger_sell:
                # Identify the most lagging altcoin
                alt_coins = ['ADAUSD', 'DOTUSD', 'MANAUSD', 'XRPUSD', 'UNIUSD', 'SOLUSD']
                changes = {coin: self.data[f'{coin}_Change'][-1] for coin in alt_coins}
                # Replace NaN with a large number to exclude from min selection
                changes = {k: (v if not pd.isna(v) else np.inf) for k, v in changes.items()}
                most_lagging = min(changes, key=changes.get)

                # Current price of the selected altcoin
                alt_price = self.data[f'{most_lagging}_Close'][-1]

                # Define stop loss and take profit
                if trigger_buy:
                    sl_price = alt_price * (1 - sl_percent / 100)
                    tp_price = alt_price * (1 + tp_percent / 100)
                    # Place a buy order with SL and TP
                    self.buy(
                        size=size,
                        price=alt_price,
                        sl=sl_price,
                        tp=tp_price,
                        name=most_lagging  # Use 'name' to track which altcoin is being traded
                    )
                    self.open_position = most_lagging
                    print(f"BUY {most_lagging} at {alt_price:.2f}, SL: {sl_price:.2f}, TP: {tp_price:.2f}")
                elif trigger_sell:
                    sl_price = alt_price * (1 + sl_percent / 100)
                    tp_price = alt_price * (1 - tp_percent / 100)
                    # Place a sell order with SL and TP
                    self.sell(
                        size=size,
                        price=alt_price,
                        sl=sl_price,
                        tp=tp_price,
                        name=most_lagging
                    )
                    self.open_position = most_lagging
                    print(f"SELL {most_lagging} at {alt_price:.2f}, SL: {sl_price:.2f}, TP: {tp_price:.2f}")
        else:
            # If there's an open position, check if it's been closed
            # This is handled automatically by backtesting.py based on SL and TP
            if not self.position:
                self.open_position = None

# Initialize the Backtest
bt = Backtest(
    merged_df,
    CorrelationAltcoinStrategy,
    cash=10000,  # Starting with $10,000
    commission=0.002,  # 0.2% commission per trade (adjust as needed)
    exclusive_orders=True  # Ensures that new orders are not placed before existing ones are closed
)

# Run the backtest
stats = bt.run()
print(stats)

# Plot the backtest results
bt.plot()
