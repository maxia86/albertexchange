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
@app.get("/prices/{ticker}/USD", response_model=list[schemas.OpenClose])
def get_prices(ticker: str, days: int = 7) :
    """Gets Open/Close prices for the selected ticker and amount of days
    """
    prices = broker.get_bars_oc(ticker+"/USD",TimeFrame.Day,datetime.datetime.today() + datetime.timedelta(days= -days),datetime.datetime.today())
    result = prices.to_dict('records')

    return result

#compra del ticker por cantidad a precio actual
@app.post("/trades/", response_model=schemas.Position)
def create_trade_buy(trade: schemas.TradeBase, db: Session = Depends(get_db)) :
    """Performs a BUY trade for the specified ticker and amount at the current price
    """
    if (trade.amount > 0 ) :
       trade_timestamp = datetime.datetime.today()
       trade_operation = 'buy'
       trade_price = broker.get_current_c(trade.ticker, TimeFrame.Day)
       create_trade = schemas.TradeCreate(**trade.dict(), operation=trade_operation, timestamp=trade_timestamp, price=trade_price)
       crud.create_trade(db=db, trade=create_trade)
       create_position=schemas.PositionCreate(ticker=trade.ticker,amount=trade.amount)
       result = crud.increase_position(db=db, position=create_position, price=trade_price)
    else :
        raise HTTPException(status_code=400, detail="Invalid Operation")
        
    return result

#todos los trades
@app.get("/trades/", response_model=list[schemas.Trade])
def read_trades(skip: int = 0, 
               limit: int = 100, 
               db: Session = Depends(get_db)
               ):
    """Gets all the trades
    """
    trades = crud.get_trades(db, skip=skip, limit=limit)

    return trades


#venta del ticker por cantidad al precio actual
@app.put("/trades/", response_model=schemas.Profit)
def create_trade_sell(trade: schemas.TradeBase, db: Session = Depends(get_db)):
    """Performs a SELL trade for the specified ticker and amount at the current price
    """
    if (trade.amount > 0 and trade.amount <= crud.get_amount(db=db, ticker=trade.ticker)) :
       trade_timestamp = datetime.datetime.today()
       trade_operation = 'sell'
       trade_price = broker.get_current_c(trade.ticker, TimeFrame.Day)
       create_trade = schemas.TradeCreate(**trade.dict(), operation=trade_operation, timestamp=trade_timestamp, price=trade_price)
       crud.create_trade(db=db, trade=create_trade)
       create_position = schemas.PositionCreate(ticker=trade.ticker,amount=trade.amount)
       result = crud.decrease_position(db=db, position=create_position, price=trade_price)
    else :
        raise HTTPException(status_code=409, detail="Invalid Operation")
     
    return result


#posicion actual total
@app.get("/positions/", response_model=list[schemas.Position])
def read_positions(db: Session = Depends(get_db)):
    """Gets current positions
    """
    positions = crud.get_positions(db)

    return positions


#posicion actual ticker
@app.get("/positions/{ticker}/USD", response_model=schemas.Position)
def read_position(ticker:str, db: Session = Depends(get_db)):
    """Gets current positions for ticker
    """
    position = crud.get_position(db=db, ticker=ticker+"/USD")

    return position


#a borrar
@app.get("/amount/{ticker}")
def lala(ticker: str, db: Session = Depends(get_db)):
    return crud.get_amount(db=db, ticker=ticker+"/USD")

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
