from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserOut, Token
from jwt import authenticate_user, create_access_token, get_password_hash, get_current_user
from crud import create_user, get_user_by_email, update_user_balance, get_user_by_id
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/change-password")
def change_password(new_password: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(current_user)
    return {"msg": "Password changed successfully"}


@router.get("/users/{email}", response_model=UserOut)
def get_user_by_email_endpoint(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=UserOut)
def update_user_balance_endpoint(user_id: int, new_balance: float, db: Session = Depends(get_db)):
    user = update_user_balance(db, user_id=user_id, new_balance=new_balance)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}/balance", response_model=UserOut)
def update_user_balance_endpoint(user_id: int, amount: float, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id=user_id)
    print(user.id, user.balance)
    print(amount, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.balance += amount
    db.commit()
    db.refresh(user)
    return user
