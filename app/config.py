from dotenv import load_dotenv
from fastapi import FastAPI
import os

#database
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

#for JWT
algorithm = os.getenv("ALGORITHM")
secret_key = os.getenv("SECRET_KEY")

#FastAPI app
app = FastAPI()