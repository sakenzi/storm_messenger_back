from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.commands.auth_crud import user_register, user_login
from app.api.auth.scheme.response import TokenResponse
from app.api.auth.scheme.create import UserRegister, UserLogin
from database.db import get_db


router = APIRouter()


@router.post(
    "/user/register",
    summary="Регистрация пользователя"
)
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    return await user_register(user=user, db=db)

@router.post(
    "user/login",
    summary="Логин пользователя",
    response_model=TokenResponse
)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await user_login(username=login_data.username, password=login_data.password, db=db)