from alpaca.data.timeframe import TimeFrame
from fastapi import Depends, FastAPI, HTTPException, Response

import datetime

import brokers.alpaca as broker
import schemas

#para arrancar uvicorn con play
import uvicorn


#crear API
app = FastAPI()


@app.get("/prices/{ticker}", response_model=list[schemas.OpenClose])
def get_prices(ticker: str, days: int = 7) :
    prices = broker.get_bars_oc(ticker+"/USD",TimeFrame.Day,datetime.datetime.today() + datetime.timedelta(days= -days),datetime.datetime.today())
    result = prices.to_dict('records')
# json_result= prices.to_json(orient='records', date_format='iso')
# return Response(content=json_result, media_type= "application/json")
    return result









#para arrancar uvicorn con play en vez de linea de comando $ uvicorn main:app --reload --port 8000
if __name__ == "__main2__" :
    uvicorn.run(
        "main:app",
        host= "127.0.0.1",
        port= 8000,
        log_level= "info",
        reload= True
    )

#asd=alp.get_bars_oc("BTC/USD",TimeFrame.Day,datetime.datetime.today() + datetime.timedelta(days= -7),datetime.datetime.today())
#print(asd)
#asd2=alp.get_current_c("BTC/USD",TimeFrame.Day)
