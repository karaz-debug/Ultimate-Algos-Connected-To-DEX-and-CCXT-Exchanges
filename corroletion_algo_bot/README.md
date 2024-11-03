##        Correlation-Based Altcoin Trading Strategy Documentation

'''
correlation algo 


we will use coinbase pro api to pull in prices for ethereum on the X minute chart 
(1m, 3 min, 5min, 15m) we will use coinbase cause their prices are quicker to update, 
there is a bit of lag when phemex OHLC data but the bid and ask data is fine


when ethereum makes a move outside of the True range in the past Y bars (20 to start) 
or outside of support and resistance of that time.. then we will quickly look for 
the below alt coins to follow and trade them in the direction ethereum went. 


altcoins - ADAUSD, DOTUSD, MANAUSD, XRPUSD, UNIUSD, SOLUSD


look to see which one is lagging behind ethereum the most and make the trade on that one. 


we will have a stop loss (.2%) and take profit close (.25%) as variables so we can tweak


example - ethereum makes an up move breaking past the ATR.. or breaking through 
resistance… we look at the above altcoins to see which one is lagging the most and 
hasnt made the full move ETH has.. then we buy at the current bid. and sell with the 
conditions above. 
'''



Overview
The Correlation-Based Altcoin Trading Strategy is designed to capitalize on the price movements of Ethereum (ETH) by identifying and trading altcoins that lag behind ETH's performance. By monitoring ETH's breakouts beyond its True Range or support/resistance levels, the strategy seeks to enter trades in the altcoins that are the slowest to follow ETH's trend, aiming to benefit from the subsequent price alignment.

Objectives
Primary Goal: To exploit the momentum and trend-following behavior of the cryptocurrency market by trading altcoins that exhibit delayed reactions to ETH's significant price movements.
Secondary Goals:
Enhance trade entry precision by identifying the most lagging altcoin.
Implement robust risk management through predefined stop loss and take profit levels.
Optimize trade execution timing using multiple timeframe analyses.
Strategy Components
Primary Asset
Ethereum (ETH-USD):
Acts as the leading indicator.
Monitored for significant price movements beyond its True Range or support/resistance levels.
Altcoins Selection
Target Altcoins:
ADAUSD (Cardano)
DOTUSD (Polkadot)
MANAUSD (Decentraland)
XRPUSD (Ripple)
UNIUSD (Uniswap)
SOLUSD (Solana)
These altcoins are selected based on their market capitalization, liquidity, and historical correlation with ETH, making them suitable candidates for trend-following strategies.

Indicators and Calculations
True Range (ATR)
Definition: The True Range (ATR) measures market volatility by calculating the range of price movement over a specified period.
Calculation:
True Range (TR): The maximum of the following:
Current High - Current Low
|Current High - Previous Close|
|Current Low - Previous Close|
ATR: The rolling average of TR over the past n periods (e.g., 14).
Support and Resistance
Support: The lowest price point over a specified period (n candles), indicating a potential price floor.
Resistance: The highest price point over the same period, indicating a potential price ceiling.
Calculation:
Support: Rolling minimum of the low prices over n candles.
Resistance: Rolling maximum of the high prices over n candles.
Correlation and Lag Identification
Objective: Identify the altcoin that is most lagging behind ETH's recent price movement.
Methodology:
ETH's Movement Calculation:
Determine the percentage change in ETH's price over the last n candles.
Altcoins' Movement Calculation:
For each altcoin, calculate the percentage change over the same period.
Lag Assessment:
Compute the absolute difference between ETH's movement and each altcoin's movement.
The altcoin with the smallest lag (i.e., smallest difference) is identified as the most lagging.
Trade Execution
Entry Conditions
Buy Signal (Long Position):
Trigger: ETH's current price exceeds either:
ETH's last closing price plus its ATR.
ETH's resistance level.
Sell Signal (Short Position):
Trigger: ETH's current price falls below either:
ETH's last closing price minus its ATR.
ETH's support level.
Upon triggering, the strategy identifies the most lagging altcoin and initiates a trade in the direction of ETH's movement.

Order Placement
Identification of Altcoin:
After a trigger condition is met, calculate the lag for each altcoin.
Select the altcoin with the smallest lag.
Price Retrieval:
Fetch the current bid price of the selected altcoin from Phemex.
Order Parameters:
Limit Order: Place a limit buy or sell order at the current bid price.
Stop Loss (SL): Set at a predefined percentage below (for buys) or above (for sells) the entry price.
Take Profit (TP): Set at a predefined percentage above (for buys) or below (for sells) the entry price.
Execution:
Buy Order: If ETH moves up, place a buy order on the altcoin.
Sell Order: If ETH moves down, place a sell order on the altcoin.
Risk Management
Stop Loss (SL)
Purpose: To limit potential losses if the trade moves against the anticipated direction.
Configuration: Set as a percentage of the entry price (e.g., 0.2% below for buys, 0.2% above for sells).
Take Profit (TP)
Purpose: To secure profits when the trade moves favorably.
Configuration: Set as a percentage of the entry price (e.g., 0.25% above for buys, 0.25% below for sells).
Note: Both SL and TP are configurable parameters, allowing for optimization based on market conditions and risk tolerance.

Parameters and Configuration
Timeframe (timeframe): Duration of each candlestick in seconds (e.g., 900 seconds for a 15-minute chart).
Data Range (dataRange): Number of past candles used for calculations (e.g., 20 candles).
Stop Loss Percentage (sl_percent): Percentage at which to exit a trade to prevent excessive loss (e.g., 0.2%).
Take Profit Percentage (tp_percent): Percentage at which to exit a trade to secure profits (e.g., 0.25%).
Trade Size (size): Quantity of the altcoin to trade per order (e.g., 1 unit).
Altcoins List (alt_coins): List of altcoins to monitor and trade (e.g., ['ADAUSD', 'DOTUSD', 'MANAUSD', 'XRPUSD', 'UNIUSD', 'SOLUSD']).
Operational Workflow
Data Retrieval:

Fetch current bid price and historical candle data for ETH from Coinbase Pro.
Fetch current bid prices and historical candle data for each altcoin from Phemex.
Indicator Calculation:

Calculate ETH's True Range (ATR) and support/resistance levels.
Determine ETH's percentage price movement over the specified data range.
Calculate each altcoin's percentage price movement over the same data range.
Signal Detection:

Check if ETH's current price breaches its ATR or support/resistance levels to trigger a trade.
Altcoin Selection:

Identify the altcoin with the smallest lag relative to ETH's movement.
Order Placement:

Place a limit buy or sell order on the selected altcoin at its current bid price.
Set stop loss and take profit levels based on the configured percentages.
Order Management:

Monitor orders for execution.
Automatically manage exit points via stop loss and take profit orders.
Scheduling:

Execute the above steps at regular intervals (e.g., every 20 seconds) to ensure timely trade execution.