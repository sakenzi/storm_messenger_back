from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from model.models import User
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def search_user(db: AsyncSession, search_query: str | None = None):
    stmt = select(User).where(User.username.like(f"%{search_query}%"))
    result = await db.execute(stmt)
    return result.scalars().all()
