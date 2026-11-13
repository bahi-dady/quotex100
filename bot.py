import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# السماح للمتصفح بالاتصال بدون مشاكل الحماية (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# قائمة نخبو فيها قاع لي راهم مكونيكتيين (السيت + الإضافات تاع كروم)
active_connections = []

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"✅ Nouvelle connexion établie ! (Clients connectés: {len(active_connections)})")
    
    try:
        while True:
            # نستقبلو الإشارة (Signal) من السيت (index.html)
            data = await websocket.receive_text()
            print(f"📩 Signal reçu du Dashboard: {data}")
            
            # نبعثو هاد الإشارة للإضافات تاع كروم باش يكليكو
            for connection in active_connections:
                if connection != websocket: # نبعثو للكل ما عدا المرسل
                    try:
                        await connection.send_text(data)
                    except:
                        pass
            print(f"🚀 Signal relayé aux extensions !")
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"❌ Connexion fermée. (Clients connectés: {len(active_connections)})")

if __name__ == "__main__":
    print("="*50)
    print("🌟 QUANTUM NEXUS - CORE SERVER 🌟")
    print("="*50)
    print("🟢 En attente de connexions sur ws://localhost:8765")
    # تشغيل السيرفر على البورت 8765
    uvicorn.run(app, host="0.0.0.0", port=8765)