import datetime
from alpaca.data.timeframe import TimeFrame
import brokers.alpaca as alp


asd=alp.get_bars_oc("BTC/USD",TimeFrame.Day,datetime.datetime.today() + datetime.timedelta(days= -7),datetime.datetime.today())

print(asd)

asd2=alp.get_current_c("BTC/USD",TimeFrame.Day)
print(asd2)