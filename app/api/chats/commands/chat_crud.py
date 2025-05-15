from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from model.models import Chat, Message
from datetime import datetime


async def get_or_create_chat(user1_id: int, user2_id: int, db: AsyncSession):
    user1_id = int(user1_id)
    user2_id = int(user2_id)

    result = await db.execute(
        select(Chat).where(
            ((Chat.user1_id == user1_id) & (Chat.user2_id == user2_id)) |
            ((Chat.user1_id == user2_id) & (Chat.user2_id == user1_id))
        )
    )
    chat = result.scalar_one_or_none()

    if not chat:
        chat = Chat(user1_id=user1_id, user2_id=user2_id)
        db.add(chat)
        await db.flush()  

    return chat

async def create_message(chat_id: int, sender_id: int, text: str, db: AsyncSession) -> Message:
    message = Message(chat_id=chat_id, sender_id=sender_id, text=text)
    db.add(message)
    await db.commit()
    return message