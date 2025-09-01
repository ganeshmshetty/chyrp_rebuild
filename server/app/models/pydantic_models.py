from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: str

class PostCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []
    is_published: bool = False

class PostOut(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    tags: List[str] = []
    created_at: datetime
    is_published: bool
