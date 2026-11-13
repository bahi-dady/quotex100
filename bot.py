import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# هادا هو الحل الجذري: allow_origin_regex=".*" يقبل إضافات ڨوڨل كروم ديريكت
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=".*",  # <--- السطر السحري 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_connections = []

@app.get("/")
def read_root():
    return {"status": "Quantum Nexus Server is LIVE!", "websocket_url": "wss://quotex100.onrender.com/ws"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print("✅ Nouvelle connexion Web ou Extension !")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message reçu: {data}")
            for connection in active_connections:
                if connection != websocket:
                    await connection.send_text(data)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("❌ Connexion perdue.")
