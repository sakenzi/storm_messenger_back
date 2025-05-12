import re

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.scheme.create import UserBase, CreateClient
from app.api.auth.scheme.response import TokenResponse, MessageResponse
from app.api.auth.crud.auth import dal_admin_login
from utils.service_utils import verify_password, create_access_token


async def validate_password(password: str):
    if len(password) < 8:
        raise ValueError("Пароль должен содержать минимум 8 символов.")
    if not re.search(r"[A-Za-z]", password):
        raise ValueError("Пароль должен содержать хотя бы одну букву.")
    if not re.search(r"\d", password):
        raise ValueError("Пароль должен содержать хотя бы одну цифру.")


async def bll_admin_login(user: UserBase, db: AsyncSession):
    try: 
        await validate_password(user.password)
        db_user = await dal_admin_login(user=user, db=db)

        if not db_user or not await verify_password(plain_password=user.password, hashed_password=db_user.password):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        access_token, expire_time = await create_access_token(data={"sub": db_user.id, "admin": True})

        return TokenResponse(
            access_token=access_token,
            access_token_expire_time=expire_time
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occured durning login: {e}"
        )


async def bll_client_login(client: CreateClient, db: AsyncSession):
    try:
        client_data: dict[str]= await dal_client_login(client=client, db=db)

        if client_data.get('message') != "Client joined successfully":
            raise HTTPException(
                status_code=401,
                detail=client_data.get('message')
            )

        access_token, expire_time = await create_access_token(data={"sub": client.ip_address, "admin": False})

        room_id = client_data.get('room_data')

        return TokenResponse(
            access_token=access_token,
            access_token_expire_time=expire_time,
            room_id=room_id,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Exception: {e}"
        )
