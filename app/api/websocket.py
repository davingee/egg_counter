from fastapi import WebSocket, WebSocketDisconnect  # type: ignore
from app.clients import pubsub_redis, CHANNEL


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pubsub = pubsub_redis.pubsub()
    await pubsub.subscribe(CHANNEL)
    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            data = message["data"]
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            await websocket.send_text(data)
    except WebSocketDisconnect:
        await pubsub.unsubscribe(CHANNEL)
    except:
        await pubsub.unsubscribe(CHANNEL)
