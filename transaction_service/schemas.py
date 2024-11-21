from pydantic import BaseModel
from datetime import datetime


class TransactionCreate(BaseModel):
    receiver_email: str
    amount: float


class TransactionOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    amount: float
    timestamp: datetime
    status: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    email: str = None
