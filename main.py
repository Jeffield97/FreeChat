import os
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect

app = FastAPI()
websockets= set()
@app.get('/')
def hello():
    return {'Hello world'}

# WebScket endpoint
@app.websocket ('/ws')
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    websockets.add(websocket)
    for ws in websockets:
        await ws.send_text(f'New user {websocket.client.host} connected')
    print(f'{websocket.client.host} connected')
    while True:
        try:
            data = await websocket.receive_text()
            for ws in websockets:
                if ws!=websocket :
                    await ws.send_text(data)
        except WebSocketDisconnect:
            websockets.remove(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=5000), log_level="info")