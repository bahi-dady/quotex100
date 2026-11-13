import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# التصحيح هنا: رديناها False باش ما يبلوكيش الإضافة تاع الكروم
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    # قبول الاتصال ديريكت
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
if __name__ == "__main__":
    print("🚀 Serveur démarré !")
    uvicorn.run(app, host="0.0.0.0", port=8000)
