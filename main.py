import ccxt
import numpy as np
import pandas as pd
import talib
import datetime
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
stop = 0
# Fetching Data

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


def run_bot_for_ticker(ccxt_ticker, trading_ticker):
    currently_holding = False
    while 1:
        ticker_data = fetch_data(ccxt_ticker)
        if ticker_data is not None:
            trade_rec_type = get_trade_recommendation(ticker_data)
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}  TRADING RECOMMENDATION: {trade_rec_type}')

