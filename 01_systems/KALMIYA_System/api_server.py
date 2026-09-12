import asyncio
import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from langchain_core.messages import HumanMessage
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
                
                from intelligence.kalmiya_agent_graph import kalmiya_brain_graph
                
                # Ejecutar stream asíncrono
                inputs = {"messages": [HumanMessage(content=user_msg)]}
                
                # Para evitar bloquear el event loop, ejecutamos el stream en un thread si es síncrono.
                # Ya que kalmiya_brain_graph.stream es síncrono, usamos to_thread.
                def run_graph():
                    responses = []
                    for output in kalmiya_brain_graph.stream(inputs):
                        for key, value in output.items():
                            msgs = value.get("messages", [])
                            if msgs:
                                responses.append({
                                    "agent": key,
                                    "text": msgs[-1].content
                                })
                    return responses
                
                loop = asyncio.get_event_loop()
                stream_results = await loop.run_in_executor(None, run_graph)
                
                # Concatenar respuesta final para el chat si el cliente no soporta parsing avanzado
                final_response = ""
                for res in stream_results:
                    final_response += f"[{res['agent'].upper()}]: {res['text']}\n"
                    
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                print(f"[ERROR EN BRAIN] {error_detail}")
                final_response = f"⚠️ Error al procesar en el Grafo: {str(e)}"
            
            # Emitir respuesta
            await broadcast_state("idle")
            await manager.broadcast({
                "type": "response",
                "user": user_msg,
                "text": final_response,
                "agents": stream_results if 'stream_results' in locals() else []
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

# Montar interfaz web nueva (ui_web/dist) si existe
static_dir = os.path.join(os.path.dirname(__file__), "ui_web", "dist")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def get_index():
    index_file = os.path.join(os.path.dirname(__file__), "ui_web", "dist", "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "online", "message": "KALMIYA Neural Core API Active. Mobile Bridge is ready on /ws"}

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
