from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import algorithm, secret_key
from datetime import timedelta
import os

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if pwd_context.hash(plain_password) == hashed_password:
        return True
    return False

def create_access_token(data: dict) -> str:
    token = jwt.encode(data, secret_key, algorithm=algorithm, exp=timedelta(days=7))
    return token

def decode_access_token(token: string) -> string:
    try:
        decoded_token = jwt.decode(token)
        return decoded_token["sub"]
    except JWTError:
        return None