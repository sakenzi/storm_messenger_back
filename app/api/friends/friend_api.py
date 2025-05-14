from app.api.friends.commands.friend_crud import (send_friend_request, get_sent_friend_requests, 
                                                  get_friend_requests, get_friends, accept_friend_request)
from app.api.friends.schemas.update import FriendAcceptResponse
from fastapi import Depends, APIRouter, Request, HTTPException,  Form
from sqlalchemy.ext.asyncio import AsyncSession
from utils.context_utils import get_access_token, validate_access_token
from database.db import get_db
from app.api.friends.schemas.response import UserResponse
from typing import List


router = APIRouter()


@router.post(
    "/send_friend_request",
    summary="Отправить заявку",
    response_model=dict
)
async def send_friend(request: Request, to_user_id: int = Form(...), db: AsyncSession = Depends(get_db)):
    try:
        access_token = await get_access_token(request)
        user_id_str = await validate_access_token(access_token)

        try:
            from_user_id = int(user_id_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user_id format in token")
        
        request_obj = await send_friend_request(
            db=db,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
        )

        return {
            "request_id": request_obj.id,
            "from_user_id": from_user_id,
            "to_user_id": to_user_id,
            "message": "Заявка успешно отправлено"
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get(
    "/user/friend-requests",
    summary="Получить все отправленные заявки в друзья" ,
    response_model=List[UserResponse]
)
async def get_sent_requests(request: Request, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    user_id = int(await validate_access_token(access_token))

    friend_requests = await get_sent_friend_requests(user_id, db)
    return [req.to_user for req in friend_requests]

@router.get(
    "/user/my-friend-requests",
    summary="Получить все мои заявки которое незнакомые люди отправляли мне",
    response_model=List[UserResponse]
)
async def get_requests(request: Request, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    user_id = int(await validate_access_token(access_token))

    friend_requests = await get_friend_requests(user_id, db)
    return [req.from_user for req in friend_requests]

@router.get(
    "/my-friends",
    summary="Получить всех друзей",
    response_model=List[UserResponse]
)
async def get_user_friends(request: Request, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    user_id = int(await validate_access_token(access_token))

    friends = await get_friends(user_id, db)
    return friends

@router.post(
    "/accept",
    summary="Одобрит заявкув друзья",
    response_model=FriendAcceptResponse
)
async def accept_request(from_user_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    to_user_id = int(await validate_access_token(access_token))

    await accept_friend_request(from_user_id, to_user_id, db)
    return {"message": "Запрос в друзья принят"}