import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# السماح بالاتصالات من أي مكان (باش السيت والإضافة يقدرو يتصلو بلا مشاكل)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# قائمة باش نشدو فيها ڨاع الإضافات لي راهم مكونيكتيين
active_connections = []

# هذي زدتهالك باش كي تدخل للرابط تاع Render يكتبلك بلي راه خدام
@app.get("/")
def read_root():
    return {"status": "Quantum Nexus Server is LIVE and Running!", "websocket_url": "wss://quotex100.onrender.com/ws"}

# مسار الـ WebSocket لي تتصل بيه الإضافة والسيت
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print("✅ Nouvelle connexion Web ou Extension !")
    try:
        while True:
            # استقبال السيغنال من السيت
            data = await websocket.receive_text()
            print(f"Message reçu: {data}")
            
            # إرسال السيغنال لجميع الإضافات المتصلة باش ينفذو الصفقة
            for connection in active_connections:
                if connection != websocket:
                    await connection.send_text(data)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("❌ Connexion perdue.")

if __name__ == "__main__":
    print("🚀 Serveur démarré !")
    uvicorn.run(app, host="0.0.0.0", port=8000)
