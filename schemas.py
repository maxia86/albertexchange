from pydantic import BaseModel
import datetime


class OpenClose(BaseModel):
    timestamp: datetime.datetime
    open: float
    close: float