from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.scheme.create import UserBase, CreateClient
from utils.context_utils import get_user_by_username
from app.api.auth.scheme.response import MessageResponse


async def dal_admin_login(user: UserBase, db: AsyncSession):
    db_user = await get_user_by_username(username=user.username, db=db)
    return db_user
