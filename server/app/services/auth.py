from fastapi import APIRouter, HTTPException, status
from ..models.pydantic_models import UserCreate, Token
from ..services.auth_service import register_user, authenticate_user


router = APIRouter()


@router.post("/register", summary="Register new user", response_model=dict)
async def register(payload: UserCreate):
uid = await register_user(payload.username, payload.email, payload.password)
if not uid:
raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
return {"id": uid}


@router.post("/login", summary="Login", response_model=Token)
async def login(payload: UserCreate):
token = await authenticate_user(payload.email, payload.password)
if not token:
raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
return {"access_token": token}