from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def get_password_hash(password: str):
return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: int = None):
to_encode = data.copy()
if expires_delta is None:
expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
else:
expire = datetime.utcnow() + timedelta(minutes=expires_delta)
to_encode.update({"exp": expire})
encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
return encoded_jwt


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
token = credentials.credentials
try:
payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
user_id = payload.get("sub")
if user_id is None:
raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
return {"_id": user_id}
except jwt.ExpiredSignatureError:
raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
except Exception:
raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")