from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.utils.security import decode_access_token
from app.models.user import User
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(db: Session = Depends(get_db),
                           token = Depends(oauth2_scheme)):
    user = decode_access_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user_check = db.query(User).filter(User.id == int(user)).first()

    if user_check is None:
        raise HTTPException(status_code=401, detail="Invalid user id")
    
    return user_check

