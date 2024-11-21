from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Transaction
from schemas import TransactionCreate, TransactionOut
from auth import get_current_user
from crud import create_transaction, get_transactions
from datetime import datetime
import requests

router = APIRouter()

AUTH_SERVICE_URL = "http://auth_service:8000/auth"


def get_user_by_email(email: str):
    response = requests.get(f"{AUTH_SERVICE_URL}/users/{email}")
    if response.status_code == 200:
        return response.json()
    return None


@router.post("/transfer", response_model=TransactionOut)
def transfer_funds(transaction: TransactionCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    sender = current_user
    receiver = get_user_by_email(transaction.receiver_email)

    print(sender, receiver, transaction.amount)

    if not receiver:
        raise HTTPException(status_code=400, detail="Receiver not found")
    if sender["balance"] < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    sender_update_response = requests.patch(
        f"{AUTH_SERVICE_URL}/users/{sender['id']}/balance?amount={-transaction.amount}",
    )
    if sender_update_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to update sender balance")

    receiver_update_response = requests.patch(
        f"{AUTH_SERVICE_URL}/users/{receiver['id']}/balance?amount={transaction.amount}",
    )
    if receiver_update_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to update receiver balance")

    new_transaction = create_transaction(db, transaction, sender["id"], receiver["id"])
    return new_transaction


@router.get("/transactions", response_model=list[TransactionOut])
def get_transactions_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    transactions = get_transactions(db, sender_id=current_user["id"], skip=skip, limit=limit)
    return transactions
