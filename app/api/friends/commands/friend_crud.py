from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from model.models import User, FriendRequest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload


async def send_friend_request(db: AsyncSession, from_user_id: int, to_user_id: int):
    if from_user_id == to_user_id:
        raise ValueError("Нельзя отправить заявку самому себе")
    
    stmt = select(FriendRequest).where(
        FriendRequest.from_user_id == from_user_id,
        FriendRequest.to_user_id == to_user_id,
    )
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    if existing:
        raise ValueError("Заявка уже отправлено")
    
    new_request = FriendRequest(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
    )
    db.add(new_request)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("Заяка уже существует")
    return new_request
    

async def get_sent_friend_requests(user_id: int, db: AsyncSession):
    stmt = (
        select(FriendRequest)
        .where(FriendRequest.from_user_id == user_id, FriendRequest.accepted == False)
        .options(selectinload(FriendRequest.to_user))
    )
    result = await db.execute(stmt)
    return result.scalars().all()