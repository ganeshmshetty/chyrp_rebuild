import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "my_blog")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
