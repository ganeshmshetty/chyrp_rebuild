from fastapi import APIRouter
from models import User
from db import db

router = APIRouter()

@router.post("/users")
async def create_user(user: User):
    result = await db.users.insert_one(user.dict())
    return {"id": str(result.inserted_id)}

@router.get("/users")
async def list_users():
    users = await db.users.find().to_list(100)
    for u in users:
        u["_id"] = str(u["_id"])
    return users
