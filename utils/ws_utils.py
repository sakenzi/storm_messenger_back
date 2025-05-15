from fastapi import WebSocket


async def get_token_from_ws(websocket: WebSocket):
    auth = websocket.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        await websocket.close(code=1008)
        raise Exception("Invalid token")
    return auth.split("Bearer ")[-1]