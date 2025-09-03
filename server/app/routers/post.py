from fastapi import APIRouter, Depends, HTTPException, status
from ..db import db
from ..models.pydantic_models import PostCreate, PostOut
from ..utils.security import get_current_user
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from typing import List


router = APIRouter()


def format_post(doc: dict) -> dict:
    """Helper function to format post document"""
    if doc:
        doc["id"] = str(doc.get("_id"))
        if doc.get("author_id"):
            doc["author_id"] = str(doc["author_id"])
        doc.pop("_id", None)
    return doc


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(payload: PostCreate, current_user=Depends(get_current_user)):
    """Create a new post"""
    author_id = current_user.get("_id")
    doc = payload.dict()
    doc.update({
        "author_id": ObjectId(author_id), 
        "created_at": datetime.utcnow()
    })
    
    result = await db.posts.insert_one(doc)
    created_post = await db.posts.find_one({"_id": result.inserted_id})
    
    return format_post(created_post)


@router.get("/", response_model=List[PostOut])
async def list_posts():
    """List all posts sorted by creation date (newest first)"""
    cursor = db.posts.find({}).sort("created_at", -1).limit(100)
    docs = await cursor.to_list(length=100)
    
    return [format_post(doc) for doc in docs]


@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: str):
    """Get a specific post by ID"""
    try:
        object_id = ObjectId(post_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Invalid post ID"
        )
    
    doc = await db.posts.find_one({"_id": object_id})
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post not found"
        )
    
    return format_post(doc)