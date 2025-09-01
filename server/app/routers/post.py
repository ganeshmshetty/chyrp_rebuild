from fastapi import APIRouter, Depends, HTTPException
from ..db import db
from ..models.pydantic_models import PostCreate, PostOut
from ..utils.security import get_current_user
from datetime import datetime
import bson


router = APIRouter()


@router.post("/", response_model=PostOut)
async def create_post(payload: PostCreate, current=Depends(get_current_user)):
author_id = current.get("_id")
doc = payload.dict()
doc.update({"author_id": bson.ObjectId(author_id), "created_at": datetime.utcnow()})
res = await db.posts.insert_one(doc)
inserted = await db.posts.find_one({"_id": res.inserted_id})
inserted["id"] = str(inserted.get("_id"))
# convert author_id to str
inserted["author_id"] = str(inserted.get("author_id"))
return inserted


@router.get("/", response_model=list[PostOut])
async def list_posts():
docs = await db.posts.find({}).sort("created_at", -1).to_list(100)
out = []
for d in docs:
d["id"] = str(d.get("_id"))
d["author_id"] = str(d.get("author_id")) if d.get("author_id") else ""
out.append(d)
return out


@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: str):
try:
oid = bson.ObjectId(post_id)
except Exception:
raise HTTPException(status_code=404, detail="Not found")
doc = await db.posts.find_one({"_id": oid})
if not doc:
raise HTTPException(status_code=404, detail="Not found")
doc["id"] = str(doc.get("_id"))
return doc