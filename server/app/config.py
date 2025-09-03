import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
DB_NAME = os.getenv("DB_NAME", "chryp-rebuild")
