from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import algorithm, secret_key
import os

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    token = jwt.encode(data, secret_key, algorithm=algorithm)
    return token

def decode_access_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[algorithm])
        return decoded_token["sub"]
    except JWTError:
        return None