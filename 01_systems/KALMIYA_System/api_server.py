import asyncio
import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI(title="KALMIYA API Server & Neural Interface")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                pass

manager = ConnectionManager()

# Variables globales para control de estado
kalmiya_state = {
    "status": "idle",
    "last_tool": None
}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send initial state
        await websocket.send_text(json.dumps({"type": "state_change", "state": kalmiya_state}))
        
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data) if data.startswith("{") else {"text": data}
            user_msg = payload.get("text", "")
            
            if not user_msg:
                continue

            # Emitir estado 'thinking'
            await broadcast_state("thinking")
            
            try:
                # Importar sys.path para que encuentre los módulos de KALMIYA
                import sys
                kalmiya_dir = os.path.dirname(__file__)
                if kalmiya_dir not in sys.path:
                    sys.path.insert(0, kalmiya_dir)
                
                try:
                    from intelligence.brain_v4 import ask_kalmiya
                except ImportError:
                    from intelligence.brain import ask_kalmiya
                loop = asyncio.get_event_loop()
                
                # Ejecutar con timeout de 60 segundos
                response = await asyncio.wait_for(
                    loop.run_in_executor(None, ask_kalmiya, user_msg),
                    timeout=60.0
                )
            except asyncio.TimeoutError:
                response = "⏱️ La solicitud tardó demasiado (timeout 60s). Es posible que ningún motor de IA esté disponible. Verifica tu conexión o las API keys en el archivo .env"
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                print(f"[ERROR EN BRAIN] {error_detail}")
                response = f"⚠️ Error al procesar: {str(e)}"
            
            # Emitir respuesta
            await broadcast_state("idle")
            await manager.broadcast({
                "type": "response",
                "user": user_msg,
                "text": response
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)

async def broadcast_state(status: str, tool_name: str = None):
    kalmiya_state["status"] = status
    if tool_name:
        kalmiya_state["last_tool"] = tool_name
    await manager.broadcast({"type": "state_change", "state": kalmiya_state})

# Función sincrona para que brain.py u otros módulos emitan eventos
def emit_sync_event(event_type: str, data: dict):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.run_coroutine_threadsafe(
                manager.broadcast({"type": event_type, **data}),
                loop
            )
    except Exception:
        pass

# Montar archivos estáticos para la interfaz Web Reactiva
static_dir = os.path.join(os.path.dirname(__file__), "web_ui")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def get_index():
    index_file = os.path.join(os.path.dirname(__file__), "web_ui", "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "online", "message": "KALMIYA Neural Core API Active. Interface files not found."}

@app.get("/api/system/status")
async def get_system_status():
    from intelligence.intelligence import KALMIYAIntelligence
    intel = KALMIYAIntelligence()
    return {
        "system": intel.get_system_info(),
        "state": kalmiya_state
    }

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
