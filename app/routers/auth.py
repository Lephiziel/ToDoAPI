from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from app.models.user import UserCreate, UserResponse, UserLogin, Token
from app.database import get_db
from app.schemas.user import User
from app.utils.security import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/register",
          status_code=status.HTTP_201_CREATED,
          response_model=UserResponse)
async def reg_new_user(user: UserCreate,
                       db: Session = Depends(get_db)):
    user_email_check = db.query(User).filter(User.email == user.email).first()
    user_username_check = db.query(User).filter(User.username == user.username).first()
    
    if user_email_check:
        raise HTTPException(status_code=400,
                            detail="Email already registered")

    if user_username_check:
        raise HTTPException(status_code=400,
                            detail="Username already taken")
    
    new_user_to_db = User(
        email=user.email,
        username=user.username,
        hashed_password = hash_password(user.password)
    )
    db.add(new_user_to_db)
    db.commit()

    user_response = db.query(User).filter(User.email == new_user_to_db.email).first()
    return user_response

@router.post("/login", response_model=Token,
                    status_code=status.HTTP_200_OK)
async def user_login(user: UserLogin,
                     db: Session = Depends(get_db)):
    user_check = db.query(User).filter(User.username == user.username).first()
    if user_check is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, user_check.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user_check.id), "exp": datetime.utcnow() + timedelta(days=7)})

    return Token(access_token=token, token_type="bearer")

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


