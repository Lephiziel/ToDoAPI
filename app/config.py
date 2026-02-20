from dotenv import load_dotenv
import os

#database
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

#for JWT
algorithm = os.getenv("ALGORITHM")
secret_key = os.getenv("SECRET_KEY")
