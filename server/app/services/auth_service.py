from ..db import db
from ..utils.security import get_password_hash, verify_password, create_access_token
import datetime




async def register_user(username: str, password: str):
    existing = await db.users.find_one({"username": username})
    if existing:
        return None
    hashed = get_password_hash(password)
    doc = {
        "username": username,
        "password": hashed,
        "created_at": datetime.datetime.utcnow()
    }
    res = await db.users.insert_one(doc)
    return str(res.inserted_id)

async def authenticate_user(username: str, password: str):
    user = await db.users.find_one({"username": username})
    if not user:
        return None
    if not verify_password(password, user.get("password")):
        return None
    token = create_access_token({"sub": str(user.get("_id")), "username": user.get("username")})
    return token