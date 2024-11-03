Overview
The Mean Reversion Trading Strategy aims to capitalize on periods of market consolidation where the price of an asset (in this case, Ethereum USD - ETHUSD) remains within a narrow range. By identifying these consolidation periods and executing trades when the price moves towards the lower or upper thirds of this range, the strategy seeks to profit from the anticipated reversal back towards the mean (average) price.

Objectives
Primary Goal: To identify and trade ETHUSD during consolidation periods, entering long (buy) positions when the price is in the lower third of the consolidation range and short (sell) positions when the price is in the upper third.

Secondary Goals:

Implement robust risk management through predefined stop loss and take profit levels.
Automate trade execution based on real-time price movements.
Optimize strategy parameters for enhanced performance.
Strategy Components
Primary Asset
Ethereum USD (ETHUSD):
Exchange: Phemex
Market Type: Spot trading
Timeframe: 5-minute (5m) candlesticks
Indicators and Calculations
True Range (TR)
Definition: The True Range (TR) measures the range of price movement over a specified period, accounting for gaps and limit moves.

Calculation:

𝑇
𝑅
=
max
⁡
(
𝐻
𝑖
𝑔
ℎ
−
𝐿
𝑜
𝑤
,
∣
𝐻
𝑖
𝑔
ℎ
−
𝑃
𝑟
𝑒
𝑣
𝑖
𝑜
𝑢
𝑠
 
𝐶
𝑙
𝑜
𝑠
𝑒
∣
,
∣
𝐿
𝑜
𝑤
−
𝑃
𝑟
𝑒
𝑣
𝑖
𝑜
𝑢
𝑠
 
𝐶
𝑙
𝑜
𝑠
𝑒
∣
)
TR=max(High−Low,∣High−Previous Close∣,∣Low−Previous Close∣)
Where:

High: Highest price in the current candle
Low: Lowest price in the current candle
Previous Close: Closing price of the previous candle
Deviation Percentage
Definition: The deviation percentage (tr_deviance) quantifies how much the True Range deviates from the current closing price, expressed as a percentage.

Calculation:

𝑡
𝑟
_
𝑑
𝑒
𝑣
𝑖
𝑎
𝑛
𝑐
𝑒
=
(
𝑇
𝑅
𝐶
𝑙
𝑜
𝑠
𝑒
)
×
100
tr_deviance=( 
Close
TR
​
 )×100
Where:

TR: True Range
Close: Closing price of the current candle
Consolidation Range
Definition: A period where the price remains within a narrow range, characterized by low volatility.

Identification Criterion: The strategy considers the market to be in consolidation if tr_deviance is below a predefined threshold (consolidation_percent).

Calculation:

Lower Third:

𝐿
𝑜
𝑤
𝑒
𝑟
 
𝑇
ℎ
𝑖
𝑟
𝑑
=
𝐿
𝑜
𝑤
+
(
𝐻
𝑖
𝑔
ℎ
−
𝐿
𝑜
𝑤
)
3
Lower Third=Low+ 
3
(High−Low)
​
 
Upper Third:

𝑈
𝑝
𝑝
𝑒
𝑟
 
𝑇
ℎ
𝑖
𝑟
𝑑
=
𝐻
𝑖
𝑔
ℎ
−
(
𝐻
𝑖
𝑔
ℎ
−
𝐿
𝑜
𝑤
)
3
Upper Third=High− 
3
(High−Low)
​
 
Where:

Low: Lowest price in the consolidation range
High: Highest price in the consolidation range
Trade Execution
Entry Conditions
Consolidation Identification:

Condition: tr_deviance < consolidation_percent (e.g., 0.7%)
Action: Proceed to evaluate trade signals.
Buy Signal (Long Position):

Trigger: Current price (price) is in the lower third of the consolidation range.
𝑝
𝑟
𝑖
𝑐
𝑒
≤
(
𝐻
𝑖
𝑔
ℎ
−
𝐿
𝑜
𝑤
3
)
+
𝐿
𝑜
𝑤
price≤( 
3
High−Low
​
 )+Low
Sell Signal (Short Position):

Trigger: Current price (price) is in the upper third of the consolidation range.
𝑝
𝑟
𝑖
𝑐
𝑒
≥
𝐻
𝑖
𝑔
ℎ
−
(
𝐻
𝑖
𝑔
ℎ
−
𝐿
𝑜
𝑤
3
)
price≥High−( 
3
High−Low
​
 )
Order Placement
Buy Order:
Type: Limit Buy Order
Price: Current bid price (price)
Parameters:
Stop Loss (SL): price * (1 - (sl_percent / 100))
Take Profit (TP): price * (1 + (tp_percent / 100))
Sell Order:
Type: Limit Sell Order
Price: Current bid price (price)
Parameters:
Stop Loss (SL): price * (1 + (sl_percent / 100))
Take Profit (TP): price * (1 - (tp_percent / 100))
Risk Management
Stop Loss (SL)
Purpose: To limit potential losses by automatically exiting a trade if the price moves against the anticipated direction beyond a certain percentage.

Configuration:

Buy Order SL: 0.25% below the entry price.
Sell Order SL: 0.25% above the entry price.
Take Profit (TP)
Purpose: To secure profits by automatically exiting a trade once the price reaches a certain favorable percentage above (for buys) or below (for sells) the entry price.

Configuration:

Buy Order TP: 0.3% above the entry price.
Sell Order TP: 0.3% below the entry price.