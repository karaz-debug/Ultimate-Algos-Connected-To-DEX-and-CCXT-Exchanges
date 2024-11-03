from os import openpty
import ccxt, turle_trading.donshare as donshare, time, schedule 
import nice_funcs as n


#connect to the phemex exchange
phemex = ccxt.phemex({
    'enableRateLimit': True, 
    'apiKey': donshare.phemex_key,
    'secret': donshare.phemex_secret
})


#config settings for bot
timeframe = '1m' #use m for minutes and h for hours, EX. 1m (1 minute) or 4h (4 hour)
symbol = 'ETHUSD'
size = 1
params = {'timeInForce': 'PostOnly'}
take_profit_percent = .2 # take profit % dev from entry price .2% 


# main bot function
def bot():


    # if the time is between 9-4p et m-f
    if n.in_timeframe():


        # gets position information, then 2 bools
        position_info,in_position,long = n.get_position(phemex,symbol) #get your current position in the market
        # this gets a candle data frame
        candles = n.get_candle_df(phemex,symbol,timeframe) #get the last 55 candle data for the timeframe
        # get ticker data to get bid/ask
        ticker = phemex.fetch_ticker(symbol) #get ticker data
        bid = ticker['bid']
        openPrice = ticker['open']




        if not in_position:


            #get the min and max prices over the 55 candle period
            minPrice = candles['low'].min()
            maxPrice = candles['high'].max()




            #if the 55 candle low is crossed under
            if bid <= minPrice and openPrice > minPrice:
                order = phemex.create_limit_sell_order(symbol, size, price=bid, params=params)


            #if the 55 candle high is crossed over
            elif bid >= maxPrice and openPrice < maxPrice:
                order = phemex.create_limit_buy_order(symbol, size, price=bid, params=params)




        # if we are already in the position
        elif in_position:


            #add the ATR to the candles dataframe (column named ATR)
            n.calc_atr(candles)
            
                
            #CALCULATE PRICES TO TAKE PROFIT AND LOSS AT
                #take profit formula: entry price * ( 1 + take_profit_percent(in decimal form) )  (would be - instead of + for a short)
                #stop loss formula: entry price - (ATR*2)  (would be + instead of - for a short)
            take_profit_price = float(position_info['avgEntryPrice']) * (1+(take_profit_percent/100))   if long else   float(position_info['avgEntryPrice']) * (1-(take_profit_percent/100))
            stop_loss_price = float(position_info['avgEntryPrice']) - (candles['ATR'].iloc[-1]*2)   if long else   float(position_info['avgEntryPrice']) + (candles['ATR'].iloc[-1]*2)
                
            #if the take profit or stop loss is reached close the position
            # this sends to the function file to send back a t/f
            if n.hit_target(bid,take_profit_price,stop_loss_price,long):
                n.close_position(phemex,symbol)






    #if past 4pm est on a friday close all positions
    # this is because we only trade til friday 4pm et
    elif n.end_of_trading_week():
        n.close_position(phemex,symbol)




#run the bot every 60 seconds
schedule.every(60).seconds.do(bot)


while True:
    try:
        schedule.run_pending()
    except:
        print('+++++ ERROR RUNNING BOT, SLEEPING FOR 30 SECONDS BEFORE RETRY')
        time.sleep(30)
