from pydantic import BaseModel
import datetime


class OpenClose(BaseModel):
    timestamp: datetime.datetime
    open: float
    close: float


class TradeBase(BaseModel):
    ticker: str
    amount: int


class TradeCreate(TradeBase):
    operation: str
    price: float
    timestamp: datetime.datetime


class Trade(TradeCreate):
    id: int

    class Config:
        orm_mode = True


class PositionCreate(BaseModel):
    ticker: str
    amount: int


class Position(PositionCreate):
    id: int
    vwap: float
    class Config:
        orm_mode = True


class Profit(BaseModel):
    ticker: str
    amount: int
    profit: float