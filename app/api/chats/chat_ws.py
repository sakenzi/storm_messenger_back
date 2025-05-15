from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
from database.db import get_db
from utils.context_utils import validate_access_token
from app.api.chats.commands.chat_ws import manager
from app.api.chats.commands.chat_crud import create_message, get_or_create_chat


router = APIRouter()
active_connections: Dict[int, WebSocket] = {}


@router.websocket(
    "/ws/message"
)
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),  
    db: AsyncSession = Depends(get_db)
):
    try:
        user_id = int(await validate_access_token(token))
    except Exception as e:
        await websocket.close(code=1008)  
        return

    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            recipient_id = int(data.get("recipient_id"))
            text = data.get("text")

            if not recipient_id or not text:
                await websocket.send_json({"error": "recipient_id and text are required"})
                continue

            chat = await get_or_create_chat(user_id, recipient_id, db)

            message = await create_message(chat.id, user_id, text, db)

            message_data = {
                "sender_id": user_id,
                "recipient_id": recipient_id,
                "text": text,
                "created_at": message.created_at.isoformat()
            }

            await manager.send_message(message_data)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        manager.disconnect(user_id)
        await websocket.close(code=1011)