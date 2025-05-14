from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from model.models import User, FriendRequest
from fastapi import Request, HTTPException
from utils.context_utils import get_access_token, validate_access_token
from sqlalchemy.exc import IntegrityError


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
    

# async def get_current_user_id(request: Request) -> int:
#     try:
#         access_token = await get_access_token(request)
#     except Exception:
#         raise HTTPException(status_code=401, detail="Access token missing on invalid")
    
#     try:
#         user_id_str = await validate_access_token(access_token)
#         user_id = int(user_id_str)
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid user_id format in token")
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid Token")
    
#     return user_id