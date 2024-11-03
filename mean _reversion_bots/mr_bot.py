order_usd_size = 10

leverage = 3
timeframe = '4h'

symbols = ['WIF', 'SOL']
symbols_data = {
    'WIF': {
        'sma_period' : 14,
        'buy_range' : (14, 15),
        'sell_range' : (14, 22)
    },
    'SOL': {
        'sma_period' : 14,  #i will be
        'buy_range' : (10, 15),
        'sell_range' : (19, 23)
    }
}

def get_range(symbol):
    return symbols_data.get(symbol, {'buy_range' : (0, 0), 'sell_range' : (0, 0)})


import sys
import os
from datetime import datetime, timedelta
import nice_funcs as n
from eth_account.signers.local import LocalAccount
import eth_account
import json
import time, random
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
import ccxt
import pandas as pd
import schedule
import requests
# from dotshareconfig import secret
from hyperliquid.utils import constants
import numpy as np
import donshare as d

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Fetch symbols from the API
def get_symbols():
    url = 'https://api.hyperliquid.xyz/info'
    headers = {'Content-Type': 'application/json'}
    data = {'type': 'meta'}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print('Error:', response.status_code)
        return []

    data = response.json()
    symbols = [symbol['name'] for symbol in data['universe']]
    print("Fetched Symbols:", symbols)
    return symbols

def calculate_sma(data, period):
    return data['close'].rolling(window=period).mean()

# Mean reversion strategy function
def mean_reversion_strategy(symbol, data, sma_period, buy_range, sell_range):
    # Calculate SMA
    data['SMA'] = calculate_sma(data, sma_period)
    print(data)  # For debugging; you may remove this later

    # Ensure there are enough data points after calculating SMA
    if len(data) < sma_period:
        print(f"Not enough data to calculate SMA for period {sma_period}")
        return "HOLD", None, None, None

    # Get the last valid SMA value (non-NaN)
    last_valid_sma = data['SMA'].dropna().iloc[-1]

    # Calculate buying and selling thresholds
    buy_threshold = last_valid_sma * (1 - np.random.uniform(buy_range[0], buy_range[1]) / 100)
    sell_threshold = last_valid_sma * (1 + np.random.uniform(sell_range[0], sell_range[1]) / 100)

    # Get the latest closing price
    current_price = data['close'].iloc[-1]

    # Convert numpy numbers of current_price, buy_threshold, and sell_threshold to float
    current_price = float(current_price)
    buy_threshold = float(buy_threshold)
    sell_threshold = float(sell_threshold)

    # Strategy: Buy if current price is below the buy threshold; Sell if current price is above the sell threshold
    if current_price < buy_threshold:
        action = "BUY"
    elif current_price > sell_threshold:
        action = "SELL"
    else:
        action = "HOLD"

    return action, buy_threshold, sell_threshold, current_price

def main():
    # GET BALANCES FROM ACCT 1, SIZE, POSITION, ENTRY PRICE, PNL, LONG/SHORT
    account1 = LocalAccount = eth_account.Account.from_key(d.private_key)

    for symbol in symbols:
        # Fetch the OHLCV data
        snapshot_data = n.get_ohlcv2(symbol, timeframe, 20)
        hourly_snapshots = n.process_data_to_df(snapshot_data)

        if not hourly_snapshots.empty:
            # Fetch symbol-specific settings
            sma_period = symbols_data[symbol]['sma_period']
            buy_range = symbols_data[symbol]['buy_range']
            sell_range = symbols_data[symbol]['sell_range']

            # Run the mean reversion strategy
            action, buy_threshold, sell_threshold, current_price = mean_reversion_strategy(
                symbol, hourly_snapshots, sma_period, buy_range, sell_range
            )

            print(f"{symbol} - Action: {action}, Buy Threshold: {buy_threshold}, Sell Threshold: {sell_threshold}, Current Price: {current_price}")

            if action == "BUY":
                print(f"Executing BUY order for {symbol}")
                print(f"passing {symbol} to adjust leverage and open order...")
                lev, size = n.adjust_leverage_usd_size(symbol, order_usd_size, leverage, account1)

                # Check if we have a position of that symbol
                positions, im_in_pos, pos_size, pos_sym, entry_px, pnl_perc, long = n.get_position(symbol, account1)

                if not im_in_pos:
                    print(f"not in position for {symbol}")
                    entry_price = current_price  # Set entry price as the current price
                    entry_price = round(entry_price, 3)
                    entry_price = float(entry_price)

                    # same for buy threshold and sell threshold
                    buy_threshold = round(buy_threshold, 3)
                    buy_threshold = float(buy_threshold)

                    sell_threshold = round(sell_threshold, 3)
                    sell_threshold = float(sell_threshold)

                    # Create a dictionary to hold the symbol information before sending the order
                    symbol_info = {
                        "Symbol": symbol,
                        "Entry Price": buy_threshold,
                        "Stop Loss": buy_threshold*0.3,  # Assuming buy threshold is the stop loss for simplicity
                        "Take Profit": sell_threshold  # Similarly, assuming sell threshold for take profit
                    }

                    n.open_order_deluxe(symbol_info, size, account1)
                    print(f"Order opened for {symbol}")
                else:
                    print(f"Already in a position for {symbol}")

            elif action == "SELL":
                print(f"Flashing SELL for {symbol} but we should already have the orders in place")
                # Place your sell order logic here
            else:
                print(f"We aint doin nothing but holding king")

print("running algo...")
main()
schedule.every(1).minutes.do(main)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(f"Encountered an error: {e}")
        time.sleep(10)