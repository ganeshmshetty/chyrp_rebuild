from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ..models.pydantic_models import Token
from ..services.auth_service import register_user, authenticate_user


router = APIRouter()


class AuthPayload(BaseModel):
    username: str
    password: str


@router.post("/register", summary="Register new user", response_model=dict)
async def register(payload: AuthPayload):
    uid = await register_user(payload.username, payload.password)
    if not uid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already in use")
    return {"id": uid}


@router.post("/login", summary="Login", response_model=Token)
async def login(payload: AuthPayload):
    token = await authenticate_user(payload.username, payload.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token}