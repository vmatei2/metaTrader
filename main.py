import time

import ccxt
import numpy as np
import pandas as pd
import talib
from datetime import datetime
import config

CANDLE_DURATION_IN_MIN = 5

RSI_PERIOD = 15
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

CCXT_TICKER_NAME = 'BTC/USDT'
TRADING_TICKER_NAME = 'btcusdt'

INVESTMENT_AMOUNT_DOLLARS = 1
HOLDING_QUANTITY = 0

kraken = ccxt.kraken({
    'apiKey': config.apiKey,
    'secret': config.secret
})
kraken.enableRateLimit = True  # stay under rate limit to avoid ban on exchange


def fetch_data(ticker):
    global kraken
    bars, ticker_df = None, None
    try:
        bars = kraken.fetch_ohlcv(ticker, timeframe=f"{CANDLE_DURATION_IN_MIN}m", limit=100)
    except:
        print(f"Erorr in fetching data from the exchange:{ticker}")

    if bars is not None:
        ticker_df = pd.DataFrame(bars[:-1], columns=['at', 'open', 'high', 'low', 'close', 'vol'])
        ticker_df['Date'] = pd.to_datetime(ticker_df['at'], unit='ms')
        ticker_df['symbol'] = ticker

    return ticker_df


# trading decision
def get_trade_recommendation(ticker_df):
    macd_result, final_result = 'WAIT', 'WAIT'

    # BUY or SELL based on MACD crossover points and the RSI value at that point
    macd, signal, hist = talib.MACD(ticker_df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    last_hist = hist.iloc[-1]
    prev_hist = hist.iloc[-2]
    if not np.isnan(prev_hist) and not np.isnan(last_hist):
        # if hist value has changed from negative to positive or vice versa, it indicates a crossover
        macd_crossover = (abs(last_hist + prev_hist)) != (abs(last_hist) + abs(prev_hist))
        if macd_crossover:
            macd_result = 'BUY' if last_hist > 0 else 'SELL'

        if macd_result != 'WAIT':
            rsi = talib.RSI(ticker_df['close'], timeperiod=14)
            # Consider the last 3 RSI values
            last_rsi_values = rsi.iloc[-3:]

            if (last_rsi_values.min() <= RSI_OVERSOLD):
                final_result = 'BUY'
            elif (last_rsi_values.max() >= RSI_OVERBOUGHT):
                final_result = 'SELL'

    return final_result


def execute_trade(trade_rec_type, trading_ticker):
    # have a look here for global variables - https://stackoverflow.com/questions/423379/using-global-variables-in-a
    # -function
    global kraken, HOLDING_QUANTITY
    order_placed = False
    side_value = 'buy' if (trade_rec_type == "BUY") else "sell"
    try:
        ticker_price_response = kraken.fetch_trades(trading_ticker)[-1]  # -1 for getting latest trade executed
        latest_price = ticker_price_response['price']  # to check the validity of this data, manually go on Kraken -
        # open a new buy order for the trading ticker provided and see how the "est. price" field updates
        # ticker price response object has info list where the entries are: 1. price, 2. volume, 3.time, 4.buy/sell, 5.market/limit, 6.miscellanous
        script_quantity = round(INVESTMENT_AMOUNT_DOLLARS/latest_price, 5) if trade_rec_type == "BUY" else HOLDING_QUANTITY
        print(f"PLACING ORDER {datetime.now().strftime('%d/%m/%y %H:%M:%S')}: {trading_ticker}, {side_value}, {latest_price}, {script_quantity}, {int(time.time() * 1000)}")
        order_response = kraken.create_order(symbol=trading_ticker, side=side_value, price=latest_price, amount=script_quantity, type="limit")
        print(f"ORDER PLACED")
        HOLDING_QUANTITY = script_quantity if trade_rec_type == "BUY" else HOLDING_QUANTITY
        order_placed = True
        test = 0
    except Exception as e:
        print(e)

    return order_placed


def run_bot_for_ticker(ccxt_ticker, trading_ticker):
    currently_holding = False
    while 1:
        ticker_data = fetch_data(ccxt_ticker)
        if ticker_data is not None:
            # STEP 2: Compute the technical indicators and apply the trading strategy
            trade_rec_type = get_trade_recommendation(ticker_data)
            print(f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}  TRADING RECOMMENDATION: {trade_rec_type}')

            # STEP 3:  Exeute the trade
            if trade_rec_type == 'BUY' and not currently_holding or trade_rec_type == "SELL" and currently_holding:
                trade_succesful = execute_trade(trade_rec_type, trading_ticker)
                currently_holding = not currently_holding if trade_succesful else currently_holding
            time.sleep(CANDLE_DURATION_IN_MIN * 60)
        else:
            print("Unable to fetch ticker data for ", ccxt_ticker)
            print()
            print("Retrying")
            time.sleep(5)

execute_trade(trade_rec_type="BUY", trading_ticker=CCXT_TICKER_NAME)
# run_bot_for_ticker(ccxt_ticker=CCXT_TICKER_NAME, trading_ticker=TRADING_TICKER_NAME)