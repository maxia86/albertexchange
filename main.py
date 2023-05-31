from alpaca.data.timeframe import TimeFrame
from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

import datetime

import brokers.alpaca as broker
from database import SessionLocal, engine
import schemas
import crud
import models

#para arrancar uvicorn con play
import uvicorn


#crear API
app = FastAPI()

#crear tablas en la DB en base a models
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#precios open/close del ticker por dia
@app.get("/prices/{ticker}", response_model=list[schemas.OpenClose])
def get_prices(ticker: str, days: int = 7) :
    """Gets Open/Close prices for the selected ticker and amount of days
    """
    prices = broker.get_bars_oc(ticker+"/USD",TimeFrame.Day,datetime.datetime.today() + datetime.timedelta(days= -days),datetime.datetime.today())
    result = prices.to_dict('records')

    return result

#compra del ticker por cantidad a precio actual
@app.post("/trades/", response_model=schemas.Trade)
def create_trade(trade: schemas.TradeBase, db: Session = Depends(get_db)) :
    """Performs a BUY trade for the specified ticker and amount at the current price
    """
    if (trade.amount > 0 ) :
       trade_timestamp = datetime.datetime.today()
       trade_operation = 'buy'
       trade_price = broker.get_current_c(trade.ticker, TimeFrame.Day)
       create_trade = schemas.TradeCreate(**trade.dict(), operation=trade_operation, timestamp=trade_timestamp, price=trade_price)
       result = crud.create_trade_buy(db=db, trade=create_trade)
    else :
        raise HTTPException(status_code=400, detail="Invalid Operation")
        
    return result


@app.get("/trades/", response_model=list[schemas.Trade])
def read_trades(skip: int = 0, 
               limit: int = 100, 
               db: Session = Depends(get_db)
               ):
    """Gets all the trades
    """
    trades = crud.get_trades(db, skip=skip, limit=limit)

    return trades

@app.get("/balance/", response_model=list[schemas.Balance])
def read_balance(db: Session = Depends(get_db)):
    """Gets current balance
    """
    balance = crud.get_balance(db)
    print(balance)
    return balance



##################
#para arrancar uvicorn con play en vez de linea de comando $ uvicorn main:app --reload --port 8000
if __name__ == "__main__" :
    uvicorn.run(
        "main:app",
        host= "127.0.0.1",
        port= 8000,
        log_level= "info",
        reload= True
    )
