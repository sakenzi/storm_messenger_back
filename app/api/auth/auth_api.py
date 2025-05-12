from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.commands.auth import bll_admin_login
from app.api.auth.scheme.create import UserBase
from app.api.auth.scheme.response import TokenResponse
from database.db import get_db


router = APIRouter()

@router.post(
    '/user/login',
    summary="Admin login",
    response_model=TokenResponse
)
async def login(user: UserBase, db: AsyncSession = Depends(get_db)):
    return await bll_admin_login(user=user, db=db)
