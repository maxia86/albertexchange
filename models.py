from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship

from database import Base

class Trades(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)
    amount = Column(Integer)
    operation = Column(String)
    price = Column(DECIMAL)
    timestamp = Column(DATETIME)


class Positions(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key= True, index= True)
    ticker = Column(String, unique=True)
    amount = Column(Integer)
    vwap = Column(DECIMAL)
