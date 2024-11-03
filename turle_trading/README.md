## Turtle Trading Strategy Documentation
Overview
This strategy is an adaptation of the classic Turtle Trading system, designed to work on multiple timeframes (1 minute, 5 minutes, 15 minutes, 1 hour, and 4 hours) for cryptocurrency trading on the Phemex exchange.
Key Components

## Entry Conditions:

Long Entry: When price breaks above the 55-bar high and is moving up
Short Entry: When price breaks below the 55-bar low and is moving down


## Exit Conditions:

Take Profit: When profit reaches 0.2% (configurable)
Stop Loss: When price moves against the position by 2 times the Average True Range (2N)


# Trading Hours:

Only trades between 9:30 AM and 4:00 PM EST, Monday to Friday
Closes all positions before 4:00 PM on Fridays



##### Detailed Workflow

### Market Analysis:

Fetches the last 55 candles for the specified timeframe
Calculates the highest high and lowest low of these 55 candles


Entry Logic:

## For a long entry:

Current bid price >= 55-bar high
Opening price of the current candle < 55-bar high


## For a short entry:

Current bid price <= 55-bar low
Opening price of the current candle > 55-bar low




####  Position Management:

If not in a position, checks for entry conditions
If in a position, monitors for exit conditions


## Exit Logic:

Take Profit:

Long: Current price >= Entry price * (1 + take_profit_percent)
Short: Current price <= Entry price * (1 - take_profit_percent)


Stop Loss:

Long: Current price <= Entry price - (2 * ATR)
Short: Current price >= Entry price + (2 * ATR)




## Risk Management:

Uses a fixed position size (configurable)
Implements a stop loss based on ATR to adapt to market volatility



Average True Range (ATR) Calculation
The strategy uses the Average True Range (ATR) for setting stop losses. Here's how it's calculated:

True Range (TR) is the greatest of:

Current High - Current Low
|Current High - Previous Close|
|Current Low - Previous Close|


ATR is then calculated as the simple moving average of TR over the last 14 periods.

In the code, this is implemented in the calc_atr function (not shown in the provided snippet).
Trade Execution

Entry:

Uses limit orders at the current bid price
Sets orders as 'Post Only' to ensure they're always limit orders


Exit:

Monitors current price against take profit and stop loss levels
Closes the entire position when either level is hit


## Timeframe Management:

Runs every 60 seconds to check conditions
Only operates during specified trading hours



## Important Considerations

The strategy assumes sufficient liquidity for limit orders to be filled
It doesn't account for slippage or partial fills
The effectiveness may vary across different market conditions and assets##