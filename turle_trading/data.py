import pandas as pd
import requests
import time
from datetime import datetime, timedelta
import os

# Function to fetch historical klines data from Binance API
def get_binance_klines(symbol, interval, start_str, end_str=None):
    url = 'https://api.binance.com/api/v3/klines'
    limit = 1000  # Max limit per request
    df_list = []
    start_ts = int(datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    if end_str:
        end_ts = int(datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    else:
        end_ts = int(datetime.now().timestamp() * 1000)
    
    while True:
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_ts,
            'endTime': end_ts,
            'limit': limit
        }
        response = requests.get(url, params=params)
        data = response.json()
        if not data or 'code' in data:
            break
        df = pd.DataFrame(data, columns=[
            'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close time', 'Quote asset volume', 'Number of trades',
            'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
        ])
        df_list.append(df)
        start_ts = int(data[-1][0]) + 1  # Increment start_ts to last returned timestamp + 1 ms
        if start_ts >= end_ts:
            break
        time.sleep(0.5)  # Sleep to respect API rate limits
    if df_list:
        result_df = pd.concat(df_list, ignore_index=True)
        return result_df
    else:
        return pd.DataFrame()

# Function to process and save the data
def fetch_and_save_data(symbol, interval, start_str, end_str, filename):
    print(f"Fetching {interval} data for {symbol} from {start_str} to {end_str}")
    df = get_binance_klines(symbol, interval, start_str, end_str)
    if not df.empty:
        # Convert timestamp to datetime
        df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
        df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
        # Select and rename columns
        df = df[['Open time', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df.rename(columns={'Open time': 'timestamp'}, inplace=True)
        
        # Convert prices to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col])
        
        # Calculate support and resistance levels
        # if len(df) > 2:
        #     df['support'] = df['Close'].rolling(window=len(df)-2, min_periods=1).min()
        #     df['resistance'] = df['Close'].rolling(window=len(df)-2, min_periods=1).max()
        # else:
        #     df['support'] = df['Close'].min()
        #     df['resistance'] = df['Close'].max()
        
        # Save to CSV
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        
        # Code to download the file if running in an online environment
        # For Google Colab:
        # from google.colab import files
        # files.download(filename)
        
        # For Jupyter Notebook:
        # from IPython.display import FileLink
        # display(FileLink(filename))
        
    else:
        print(f"No data fetched for {symbol} at interval {interval}")

# Set the symbol and date range
symbol = 'SOLUSDT'  # Bitcoin to Tether on Binance
start_date = '2023-09-01 00:00:00'  # Start date (adjust as needed)
end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # End date is now

# Fetch and save data for different intervals
# 1-minute interval
# fetch_and_save_data(symbol, '4h', start_date, end_date, 'BTCUSDT.csv')

# 15-minute interval
fetch_and_save_data(symbol, '1m', start_date, end_date, 'SOLUSDT_1m.csv')

# 1-hour interval
# fetch_and_save_data(symbol, '1h', start_date, end_date, 'BTCUSDT_1h.csv')

# Uncomment the following lines if you want to fetch daily data
# # 1-day interval
# fetch_and_save_data(symbol, '1d', start_date, end_date, 'BTCUSDT_1d.csv')
