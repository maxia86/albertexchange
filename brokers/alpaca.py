from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
import datetime

# No necesito keys
client = CryptoHistoricalDataClient()

def get_bars(symbol, timeframe, start, end) :
    request_params = CryptoBarsRequest(
                        symbol_or_symbols=[symbol],
                        timeframe=timeframe,
                        start=start,
                        end=end
                        )
    #agregue el 'us' porque sino saltaba-> alpaca.common.exceptions.APIError: {"message":"Invalid location: CryptoFeed.US"}
    bars = client.get_crypto_bars(request_params,'us')
    
    return bars.df

def get_bars_oc(symbol, timeframe, start, end) :
    bars = get_bars(symbol, timeframe, start, end)
    bars.drop(columns=['high', 'low', 'volume', 'trade_count', 'vwap'], inplace=True)
    bars.reset_index(level=['timestamp'], inplace=True)
    
    return bars 

def get_current_c(symbol, timeframe) :
    bars = get_bars(symbol, timeframe, datetime.datetime.today() + datetime.timedelta(days= -1),datetime.datetime.today())
    bars.drop(columns=['open','high', 'low', 'volume', 'trade_count', 'vwap'], inplace=True)
    
    return bars.values[0]
