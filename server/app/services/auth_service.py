from ..db import db
from ..utils.security import get_password_hash, verify_password, create_access_token
from bson import ObjectId




async def register_user(username: str, email: str, password: str):
existing = await db.users.find_one({"email": email})
if existing:
return None
hashed = get_password_hash(password)
doc = {"username": username, "email": email, "password": hashed, "created_at": None}
res = await db.users.insert_one(doc)
return str(res.inserted_id)




async def authenticate_user(email: str, password: str):
user = await db.users.find_one({"email": email})
if not user:
return None
if not verify_password(password, user.get("password")):
return None
# create token
token = create_access_token({"sub": str(user.get("_id")), "email": user.get("email")})
return token