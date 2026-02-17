from dotenv import load_dotenv
import os

#database
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")