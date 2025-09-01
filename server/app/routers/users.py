from fastapi import APIRouter, Depends
from ..db import db
from ..models.pydantic_models import UserOut
from ..utils.security import get_current_user


router = APIRouter()


@router.get("/me", response_model=dict)
async def me(current=Depends(get_current_user)):
uid = current.get("_id")
user = await db.users.find_one({"_id": __import__('bson').ObjectId(uid)})
if not user:
return {}
user_out = {"id": str(user.get("_id")), "username": user.get("username"), "email": user.get("email")}
return user_out