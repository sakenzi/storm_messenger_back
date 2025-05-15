from fastapi import Depends, APIRouter, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.chats.commands.chat_crud import get_or_create_chat, create_message
from database.db import get_db
from utils.context_utils import get_access_token, validate_access_token
from app.api.chats.schemas.create import MessageCreate
from typing import Dict
from app.api.chats.commands.chat_ws import manager
from model.models import Message


router = APIRouter()
active_connections: Dict[int, WebSocket] = {}


@router.post("/send-message")
async def send_message(data: MessageCreate, request: Request, db: AsyncSession = Depends(get_db)):
    token = await get_access_token(request)
    sender_id = int(await validate_access_token(token))  

    recipient_id = int(data.recipient_id)  

    chat = await get_or_create_chat(sender_id, recipient_id, db)

    message = Message(
        chat_id=chat.id,
        sender_id=sender_id,
        text=data.text
    )
    db.add(message)
    await db.commit()

    message_data = {
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "text": data.text
    }

    await manager.send_message(message_data)
    return {"status": "sent"}