from sqlalchemy.orm import Session
from sqlalchemy import func

import brokers.alpaca as broker
import models
import schemas

def create_trade_buy(db: Session, trade: schemas.TradeCreate):
    db_trade = models.Trades(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def get_trades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trades).offset(skip).limit(limit).all()


def get_balance(db: Session):
    return db.query(models.Trades).add_columns(models.Trades.ticker, func.sum(models.Trades.amount).label("amount"), (func.sum(models.Trades.price * models.Trades.amount)/func.sum(models.Trades.amount)).label("vwap")).group_by(models.Trades.ticker).all()
#cuando agregue la venta va a tener que ser modificado?