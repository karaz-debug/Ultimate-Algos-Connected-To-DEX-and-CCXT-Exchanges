

import ccxt, time, schedule 
import nice_funcs as nf




#connect to the phemex exchange
phemex = ccxt.phemex({
    'enableRateLimit': True, 
    # 'apiKey': config.phemex_key,
    # 'secret': config.phemex_secret
})


#config settings for bot
timeframe = '5m' #use m for minutes and h for hours, EX. 1m (1 minute) or 4h (4 hour)
limit = 20 #amount of candles to check
symbol = 'ETHUSD'
size = 1
tp_percent = .3 #set percent of take profit
sl_percent = .25 #set percent of take loss
params = {'timeInForce': 'PostOnly','takeProfit':0,'stopLoss':0} #set default tp and sl, will be changed when an order is about to be placed


# used to only trade in times of little movement. 
# This value is the percent deviance from price of the true range,
# meaning that if the true range is within x percent away 
# from the price it is considered consolidation
consolidation_percent = .7 # if tr is .7% of the price its considered consolidation




def bot():


    position_info,in_position,long = nf.get_position(phemex,symbol) #get your current position in the market
    candles = nf.get_candle_df(phemex,symbol,timeframe,limit) #get the last 55 candle data for the timeframe
    tr = nf.calc_tr(candles) #get the true range


    # calc the deviance % from tr of lcose
    tr_deviance = (tr/candles.close.iloc[-1])*100 #get the percent deviation of the true range from the price


    #only look to create an order if we are not in a position already
    if not in_position:
        
        # if the tr_dev is smaller than our wanted one then we do the bot
        if tr_deviance < consolidation_percent:
            price = phemex.fetch_ticker(symbol)['bid'] #get the current bid
            low,high = nf.get_extreme_of_consolidation(candles,consolidation_percent) #get the lowest and highest prices in the current consolidation


            #buy if price is in the lower 1/3 of the consolidation range
            if price <= ((high-low)/3)+low:
                params['stopLoss'] = price * (1-(sl_percent/100)) #set stop loss price
                params['takeProfit'] = price * (1+(tp_percent/100)) #set take profit price
                order = phemex.create_limit_buy_order(symbol, size, price=price, params=params)


            #sell if price is in the upper 1/3 of the consolidation range
            if price >= high-((high-low)/3):
                params['stopLoss'] = price * (1+(sl_percent/100)) #set stop loss price
                params['takeProfit'] = price * (1-(tp_percent/100)) #set take profit price
                order = phemex.create_limit_sell_order(symbol, size, price=price, params=params)




#run the bot every 20 seconds
schedule.every(20).seconds.do(bot)


while True:
    try:
        schedule.run_pending()
    except:
        print('+++++ ERROR RUNNING BOT, SLEEPING FOR 30 SECONDS BEFORE RETRY')
        time.sleep(30)
        
        
# Operational Workflow
# Initialize Bot:

# Connect to Phemex exchange using ccxt.
# Define strategy parameters (timeframe, limit, symbol, trade size, TP and SL percentages, consolidation threshold).
# Execute Bot Periodically:

# Frequency: Every 20 seconds.
# Bot Execution Steps:

# Check Current Position:
# Determine if there is an existing open position in ETHUSD.
# Fetch Candle Data:
# Retrieve the latest 20 candles for ETHUSD in 5-minute intervals.
# Calculate True Range (TR):
# Compute the True Range for the latest candle.
# Calculate Deviation Percentage (tr_deviance):
# Determine how much the TR deviates from the closing price as a percentage.
# Identify Consolidation:
# If tr_deviance is below 0.7%, consider the market in consolidation.
# Determine Trade Signals:
# Buy Signal: If the current price is in the lower third of the consolidation range.
# Sell Signal: If the current price is in the upper third of the consolidation range.
# Place Orders:
# Execute a limit buy or sell order based on the identified signal.
# Set stop loss and take profit parameters accordingly.
# Handle Exceptions:

# If any error occurs during bot execution, log the error and pause the bot for 30 seconds before retrying.
