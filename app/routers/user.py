from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.repo import SessionLocal
from app.database.models import User
from app.models.schemas import UserCreate, UserLogin
from app.auth.auth import authenticate_user, create_access_token, get_password_hash

router = APIRouter()

@router.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(SessionLocal)):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return create_access_token(data={"sub": user.email})

@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(SessionLocal)):
    db_user = authenticate_user(user.email, user.password, db)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return create_access_token(data={"sub": user.email})
