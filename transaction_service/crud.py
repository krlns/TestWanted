from sqlalchemy.orm import Session
from models import Transaction
from schemas import TransactionCreate


def create_transaction(db: Session, transaction: TransactionCreate, sender_id: int, receiver_id: int):
    db_transaction = Transaction(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=transaction.amount,
        status="completed"
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(db: Session, sender_id: int, skip: int = 0, limit: int = 10):
    return db.query(Transaction).filter(Transaction.sender_id == sender_id).offset(skip).limit(limit).all()
