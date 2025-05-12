import hashlib
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from model.models import User
from core.config import settings
from sqlalchemy.orm import selectinload


def hash_password(plain_password: str) -> str:
    return hashlib.sha256(plain_password.encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> str:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> tuple:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(settings.TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    return encoded_jwt, expire.isoformat()

async def get_access_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    
    return parts[1]

async def validate_access_token(access_token: str) -> str:
    payload = jwt.decode(
            access_token,
            settings.TOKEN_SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM]
        )
        
    tg_username = payload.get("sub") 
    if tg_username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    exp = payload.get("exp")
    if exp and exp < datetime.utcnow().timestamp():
        raise HTTPException(status_code=401, detail="Token has expired")
    
    return tg_username

async def get_user_by_username(username: str, db: AsyncSession) -> User:
    user = await db.execute(
        select(User)
        .filter(User.username==username)
    )
    return user.scalar_one_or_none()

async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
    user = await db.execute(
        select(User)
        .options(selectinload(User.role))
        .filter(User.id == user_id)
    )
    return user.scalars().first()
