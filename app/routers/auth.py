from app.config import app
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.user import UserCreate
from app.database import get_db
from app.database import Todo, User
from utils.security import hash_password

@app.post("/register")
async def reg_new_user(user: UserCreate, db: Session = Depends(get_db)):
    user_email_check = db.query(User).filter(User.email == user.email).first()
    user_username_check = db.query(User).filter(User.username == user.username).first()
    
    if user_email_check:
        raise HTTPException(status_code=400, detail="Email already registered")

    if user_username_check:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    new_user = User(user.model_dump())
    db.add(new_user)
    db.commit()



