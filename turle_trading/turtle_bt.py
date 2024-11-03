import pandas as pd
import numpy as np
import pytz
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import logging
import warnings

# Suppress specific warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="backtesting")

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("backtest_debug.log"),
        logging.StreamHandler()
    ]
)

# Define crossunder function
def crossunder(series1, series2):
    """
    Returns True if series1 crosses below series2 between the last two data points.
    """
    return (series1[-2] > series2[-2]) and (series1[-1] < series2[-1])

# Indicator functions with validation
def rolling_max(arr, n):
    series = pd.Series(arr)
    rolling_max = series.rolling(n).max()
    if rolling_max.isnull().any():
        logging.warning("NaN values detected in rolling_max calculation.")
    return rolling_max.to_numpy()

def rolling_min(arr, n):
    series = pd.Series(arr)
    rolling_min = series.rolling(n).min()
    if rolling_min.isnull().any():
        logging.warning("NaN values detected in rolling_min calculation.")
    return rolling_min.to_numpy()

def ATR(high, low, close, n):
    high = pd.Series(high)
    low = pd.Series(low)
    close = pd.Series(close)
    tr = pd.concat([
        high - low,
        (high - close.shift(1)).abs(),
        (low - close.shift(1)).abs()
    ], axis=1).max(axis=1)
    atr = tr.rolling(n).mean()
    if atr.isnull().any():
        logging.warning("NaN values detected in ATR calculation.")
    return atr.to_numpy()

def get_current_time(timestamp):
    """
    Converts the given timestamp to US/Eastern timezone.
    If the timestamp is timezone-naive, localize it to UTC first.
    """
    if timestamp.tzinfo is None:
        # Assume the timestamp is in UTC if timezone-naive
        timestamp = timestamp.tz_localize('UTC')
    return timestamp.tz_convert('US/Eastern')

# Strategy class
class TurtleStrategy(Strategy):
    n = 20  # Adjusted number of bars for high/low calculation
    atr_period = 14  # Period for ATR calculation
    take_profit_percent = 0.5  # Increased take profit percentage
    stop_loss_atr_multiplier = 2  # 2 * ATR for stop loss

    def init(self):
        # Initialize indicators
        self.high_n = self.I(rolling_max, self.data.High, self.n)
        self.low_n = self.I(rolling_min, self.data.Low, self.n)
        self.atr = self.I(ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)
        logging.debug("Initialized indicators: high_n, low_n, ATR")

    def next(self):
        # Get the current timestamp
        current_timestamp = self.data.index[-1]
        try:
            current_time = get_current_time(current_timestamp)
        except Exception as e:
            logging.error(f"Timestamp conversion error at {current_timestamp}: {e}")
            return

        # Only trade between 9:30 AM and 4:00 PM EST, Monday to Friday
        if current_time.weekday() >= 5:
            return  # Skip weekends

        if not ((current_time.hour == 9 and current_time.minute >= 30) or (10 <= current_time.hour < 16)):
            return  # Skip outside trading hours

        # Close positions before 4:00 PM on Fridays
        if current_time.weekday() == 4 and current_time.hour == 16 and current_time.minute == 0:
            if self.position:
                logging.info(f"Closing position at {current_timestamp} due to end of trading week.")
                self.position.close()
            return

        # Ensure indicators are valid (not NaN)
        if np.isnan(self.high_n[-1]) or np.isnan(self.low_n[-1]) or np.isnan(self.atr[-1]):
            logging.debug(f"Skipping candle {len(self.data)} due to NaN indicators.")
            return

        # Logging indicator values for every candle (can be adjusted for verbosity)
        logging.debug(f"Candle {len(self.data)}: Time={current_time}, Close={self.data.Close[-1]:.2f}, "
                      f"High_n={self.high_n[-1]:.2f}, Low_n={self.low_n[-1]:.2f}, ATR={self.atr[-1]:.2f}")

        # Check for potential crossovers
        if crossover(self.data.Close, self.high_n):
            logging.debug(f"Potential BUY signal detected at {current_timestamp}: Close={self.data.Close[-1]:.2f} crossing above High_n={self.high_n[-1]:.2f}")

        if crossunder(self.data.Close, self.low_n):
            logging.debug(f"Potential SELL signal detected at {current_timestamp}: Close={self.data.Close[-1]:.2f} crossing below Low_n={self.low_n[-1]:.2f}")

        if not self.position:
            # Long entry
            if crossover(self.data.Close, self.high_n):
                # Removed the Open price condition for testing
                entry_price = self.data.Close[-1]
                sl = entry_price - self.atr[-1] * self.stop_loss_atr_multiplier
                tp = entry_price * (1 + self.take_profit_percent / 100)
                self.buy(sl=sl, tp=tp)
                logging.info(f"BUY signal executed at {current_timestamp}: Close={entry_price:.2f}, High_n={self.high_n[-1]:.2f}, "
                             f"SL={sl:.2f}, TP={tp:.2f}")

            # Short entry
            elif crossunder(self.data.Close, self.low_n):
                # Removed the Open price condition for testing
                entry_price = self.data.Close[-1]
                sl = entry_price + self.atr[-1] * self.stop_loss_atr_multiplier
                tp = entry_price * (1 - self.take_profit_percent / 100)
                self.sell(sl=sl, tp=tp)
                logging.info(f"SELL signal executed at {current_timestamp}: Close={entry_price:.2f}, Low_n={self.low_n[-1]:.2f}, "
                             f"SL={sl:.2f}, TP={tp:.2f}")
        else:
            # Position exit is handled by stop loss and take profit parameters
            pass

# Load your data
data_path = 'C:/Users/IQRA/Desktop/Mean_Reversion/turle_trading/SOLUSDT_1m.csv'
data = pd.read_csv(data_path, index_col='timestamp', parse_dates=True)

# Ensure the data has the correct columns
required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"Data must contain the following columns: {required_columns}")

data = data[required_columns]

# Sort the data by index (timestamp)
data = data.sort_index()

# Remove duplicate timestamps
if data.index.duplicated().any():
    logging.warning("Duplicate timestamps detected. Removing duplicates.")
    data = data[~data.index.duplicated()]

# Check for missing data
missing_before = len(data)
data = data.dropna()
missing_after = len(data)
if missing_before != missing_after:
    logging.warning(f"Dropped {missing_before - missing_after} rows due to NaN values.")

# Handle timezone
if data.index.tz is None:
    # Assume timestamps are in UTC if timezone-naive
    data.index = data.index.tz_localize('UTC')
    logging.info("Timestamps were timezone-naive. Localized to UTC.")
else:
    # Convert to UTC if already timezone-aware
    data.index = data.index.tz_convert('UTC')
    logging.info("Converted timestamps to UTC.")

# Log data loading completion
logging.info(f"Data loaded successfully with {len(data)} records from {data.index[0]} to {data.index[-1]}.")

# Run the backtest
bt = Backtest(
    data,
    TurtleStrategy,
    cash=10000,
    commission=.002,
    exclusive_orders=True,  # Ensures that orders are exclusive (e.g., no overlapping positions)
    trade_on_close=False  # Trades are executed on the next candle's open
)

# Execute the backtest
try:
    stats = bt.run()
    logging.info("Backtest completed successfully.")
    print(stats)
    # Plot the results
    bt.plot()
except Exception as e:
    logging.error(f"An error occurred during backtesting: {e}")
