from fastapi import APIRouter, Depends, HTTPException
from ..db import db
from ..models.pydantic_models import PostCreate, PostOut
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=PostOut)
async def create_post(payload: PostCreate, current_user=Depends(...)):
    doc = payload.dict()
    doc.update({"author_id": str(current_user["_id"]), "created_at": datetime.utcnow()})
    res = await db.posts.insert_one(doc)
    inserted = await db.posts.find_one({"_id": res.inserted_id})
    inserted["id"] = str(inserted["_id"])
    return inserted
