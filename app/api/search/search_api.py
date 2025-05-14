from fastapi import Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.search.schemas.response import UsersResponse
from app.api.search.commands.search_crud import search_user
from database.db import get_db
from typing import List


router = APIRouter()


@router.get(
    "/search/users",
    summary="Поиск пользователей",
    response_model=List[UsersResponse]
)
async def search_users(username: str = Query, db: AsyncSession = Depends(get_db)):
    return await search_user(db, username)