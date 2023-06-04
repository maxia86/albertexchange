from sqlalchemy.orm import Session
from sqlalchemy import func

import brokers.alpaca as broker
import models
import schemas

def create_trade(db: Session, trade: schemas.TradeCreate):
    db_trade = models.Trades(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def get_trades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trades).offset(skip).limit(limit).all()


def increase_position(db: Session, position:schemas.PositionCreate, price: float):
    db_position = get_position(db, position.ticker)
    if db_position:
        db_position.vwap = ((models.Positions.vwap * models.Positions.amount)+(position.amount * price))/(models.Positions.amount + position.amount)
        db_position.amount = models.Positions.amount + position.amount
        db.commit()
        db.refresh(db_position)
    else: 
        db_position = models.Positions(**position.dict())
        db_position.vwap = price
        db.add(db_position)
        db.commit()
        db.refresh(db_position)
    return db_position


def decrease_position(db: Session, position:schemas.PositionCreate, price: float):
    db_position = get_position(db, position.ticker)
    profit = schemas.Profit(ticker=position.ticker, amount=position.amount, profit=((price - float(db_position.vwap)) * position.amount))
    if db_position.amount > position.amount:
        db_position.amount = models.Positions.amount - position.amount
        db.commit()
#        db.refresh(db_position)
    else:
        db.delete(db_position)
        db.commit()
        
    return profit
    

def get_positions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Positions).offset(skip).limit(limit).all()


def get_position(db: Session, ticker: str):
    return db.query(models.Positions).filter(models.Positions.ticker==ticker).first()


def get_amount(db: Session, ticker: str):
    position = db.query(models.Positions).filter(models.Positions.ticker==ticker).first()
    if not position:
        result = 0
    else:
        result = position.amount
    return result

def get_vwap(db: Session, ticker: str):
    position = db.query(models.Positions).filter(models.Positions.ticker==ticker).first()
    if not position:
        result = 0
    else:
        result = position.vwap
    return result

