"""
kalmiya_mcp.py — Servidor MCP (Model Context Protocol) para KALMIYA
====================================================================
Expone las capacidades de KALMIYA como herramientas MCP estándar.
Compatible con Claude Desktop, Cursor, Kiro y cualquier cliente MCP.

Herramientas expuestas:
  - preguntar_kalmiya     → pregunta a la IA
  - buscar_documentos     → RAG en el vault de Obsidian
  - leer_nota             → leer una nota del vault
  - crear_nota            → crear nueva nota en Obsidian
  - listar_notas          → listar notas del vault
  - estado_sistema        → CPU, RAM, disco
  - ejecutar_skill        → ejecutar una skill de KALMIYA
  - clima                 → clima actual de cualquier ciudad
  - traducir              → traducir texto
  - generar_codigo        → generar snippet de código

Transporte: stdio (estándar MCP) o HTTP (puerto 8765)
"""

import os, sys, json, threading, time
from pathlib import Path
from datetime import datetime
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import log_command
from _logging import get_logger

logger = get_logger(__name__)

# ── Dependencias opcionales ────────────────────────────────────────────────────
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp import types as mcp_types
    MCP_OK = True
except ImportError:
    MCP_OK = False
    logger.warning("[MCP] mcp no disponible — instala: pip install mcp")

# ── Estado del servidor ────────────────────────────────────────────────────────
_servidor_activo = False
_puerto          = 8765
_n_llamadas      = 0

# ══════════════════════════════════════════════════════════════════════════════
# REGISTRO DE HERRAMIENTAS MCP
# ══════════════════════════════════════════════════════════════════════════════

# Lista de herramientas con sus esquemas
HERRAMIENTAS_MCP: list[dict] = [
    {
        "nombre":      "preguntar_kalmiya",
        "descripcion": "Hace una pregunta a KALMIYA y devuelve la respuesta de la IA",
        "parametros": {
            "query":  {"type": "string", "description": "Pregunta o consulta"},
            "engine": {"type": "string", "description": "Motor IA: auto, gemini, ollama, groq", "default": "auto"},
            "rag":    {"type": "boolean","description": "Usar RAG (documentos personales)", "default": False},
        },
        "requeridos": ["query"],
    },
    {
        "nombre":      "buscar_documentos",
        "descripcion": "Busca en los documentos del vault de Obsidian usando RAG semántico",
        "parametros": {
            "query":  {"type": "string",  "description": "Texto a buscar"},
            "top_k":  {"type": "integer", "description": "Número de resultados (1-10)", "default": 5},
            "tipo":   {"type": "string",  "description": "Filtrar por extensión: .md .py .pdf", "default": ""},
        },
        "requeridos": ["query"],
    },
    {
        "nombre":      "leer_nota",
        "descripcion": "Lee el contenido de una nota del vault de Obsidian",
        "parametros": {
            "nombre": {"type": "string", "description": "Nombre de la nota (sin .md)"},
            "carpeta": {"type": "string", "description": "Carpeta opcional", "default": ""},
        },
        "requeridos": ["nombre"],
    },
    {
        "nombre":      "crear_nota",
        "descripcion": "Crea una nueva nota en el vault de Obsidian",
        "parametros": {
            "titulo":   {"type": "string", "description": "Título de la nota"},
            "contenido":{"type": "string", "description": "Contenido en Markdown"},
            "carpeta":  {"type": "string", "description": "Carpeta destino", "default": "KALMIYA_Notes"},
            "tags":     {"type": "array",  "description": "Lista de tags", "default": []},
        },
        "requeridos": ["titulo", "contenido"],
    },
    {
        "nombre":      "listar_notas",
        "descripcion": "Lista las notas de una carpeta del vault",
        "parametros": {
            "carpeta": {"type": "string", "description": "Carpeta a listar", "default": "KALMIYA_Notes"},
        },
        "requeridos": [],
    },
    {
        "nombre":      "estado_sistema",
        "descripcion": "Devuelve el estado actual del sistema: CPU, RAM, disco, motores IA",
        "parametros": {},
        "requeridos": [],
    },
    {
        "nombre":      "ejecutar_skill",
        "descripcion": "Ejecuta una skill de KALMIYA (traducir, clima, código, etc.)",
        "parametros": {
            "skill":     {"type": "string", "description": "Nombre de la skill"},
            "argumentos":{"type": "array",  "description": "Lista de argumentos", "default": []},
        },
        "requeridos": ["skill"],
    },
    {
        "nombre":      "clima",
        "descripcion": "Obtiene el clima actual y pronóstico de 7 días para una ciudad",
        "parametros": {
            "ciudad": {"type": "string", "description": "Nombre de la ciudad", "default": "Cúcuta"},
        },
        "requeridos": [],
    },
    {
        "nombre":      "traducir",
        "descripcion": "Traduce texto a cualquier idioma",
        "parametros": {
            "texto":   {"type": "string", "description": "Texto a traducir"},
            "destino": {"type": "string", "description": "Idioma destino: es, en, fr, pt, de", "default": "en"},
        },
        "requeridos": ["texto"],
    },
    {
        "nombre":      "generar_codigo",
        "descripcion": "Genera un snippet de código en cualquier lenguaje",
        "parametros": {
            "descripcion": {"type": "string", "description": "Qué debe hacer el código"},
            "lenguaje":    {"type": "string", "description": "Lenguaje: Python, JS, Java, etc.", "default": "Python"},
        },
        "requeridos": ["descripcion"],
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# EJECUTORES DE HERRAMIENTAS
# ══════════════════════════════════════════════════════════════════════════════

def _ejecutar_herramienta(nombre: str, params: dict) -> Any:
    """Ejecuta una herramienta MCP y devuelve el resultado."""
    global _n_llamadas
    _n_llamadas += 1
    log_command(f"[MCP] {nombre}", json.dumps(params)[:200], source="system")

    try:
        if nombre == "preguntar_kalmiya":
            query  = params.get("query", "")
            engine = params.get("engine", "")
            usar_rag = params.get("rag", False)
            if usar_rag:
                from kalmiya_rag import responder_con_rag
                return responder_con_rag(query, force_engine=engine)
            else:
                from brain import ask_kalmiya
                return ask_kalmiya(query, force_engine=engine)

        elif nombre == "buscar_documentos":
            from kalmiya_rag import buscar_rag, _init_rag
            _init_rag()
            query  = params.get("query", "")
            top_k  = params.get("top_k", 5)
            tipo   = params.get("tipo", "") or None
            chunks = buscar_rag(query, top_k=top_k, filtro_tipo=tipo)
            return [{"fuente": c["fuente"], "similitud": c["similitud"],
                     "texto": c["texto"][:300]} for c in chunks]

        elif nombre == "leer_nota":
            from obsidian_bridge import read_note
            nombre_nota = params.get("nombre", "")
            carpeta     = params.get("carpeta", "") or None
            return read_note(nombre_nota, carpeta)

        elif nombre == "crear_nota":
            from obsidian_bridge import create_note
            path = create_note(
                title   = params.get("titulo", ""),
                content = params.get("contenido", ""),
                folder  = params.get("carpeta", "KALMIYA_Notes"),
                tags    = params.get("tags", []),
            )
            return {"creada": True, "ruta": str(path)}

        elif nombre == "listar_notas":
            from obsidian_bridge import list_notes
            return list_notes(params.get("carpeta", "KALMIYA_Notes"))

        elif nombre == "estado_sistema":
            from kalmiya_system_info import resumen_sistema_completo, espacio_libre_rapido
            from brain import get_engine_status
            data  = resumen_sistema_completo()
            discos = espacio_libre_rapido()
            motores = get_engine_status()
            return {
                "cpu":     {"uso": data["cpu"].get("uso_total_pct"),
                            "nucleos": data["cpu"].get("nucleos_fisicos")},
                "ram":     {"uso_pct": data["ram"].get("uso_pct"),
                            "total_gb": data["ram"].get("total_gb")},
                "discos":  {k: {"libre_gb": v["libre_gb"], "uso_pct": v["uso_pct"]}
                            for k, v in discos.items()},
                "motores": {"modo": motores.get("modo_actual"),
                            "activo": motores.get("motor_usado")},
            }

        elif nombre == "ejecutar_skill":
            from kalmiya_skills import ejecutar_skill
            return ejecutar_skill(params.get("skill", ""),
                                   params.get("argumentos", []))

        elif nombre == "clima":
            from kalmiya_nuevas_funciones import get_real_weather
            return get_real_weather(params.get("ciudad", "Cúcuta"))

        elif nombre == "traducir":
            from kalmiya_nuevas_funciones import traducir
            return traducir(params.get("texto", ""), params.get("destino", "en"))

        elif nombre == "generar_codigo":
            from kalmiya_nuevas_funciones import generar_snippet
            return generar_snippet(params.get("descripcion", ""),
                                    params.get("lenguaje", "Python"))

        else:
            return {"error": f"Herramienta '{nombre}' no encontrada"}

    except Exception as e:
        logger.error(f"[MCP] Error ejecutando '{nombre}': {e}")
        return {"error": str(e)}


# ══════════════════════════════════════════════════════════════════════════════
# SERVIDOR MCP STDIO (protocolo estándar)
# ══════════════════════════════════════════════════════════════════════════════

def iniciar_servidor_stdio():
    """
    Inicia el servidor MCP en modo stdio.
    Compatible con Claude Desktop, Cursor, Kiro y otros clientes MCP.
    """
    if not MCP_OK:
        logger.error("[MCP] Instala: pip install mcp")
        return

    server = Server("kalmiya")

    @server.list_tools()
    async def list_tools():
        tools = []
        for h in HERRAMIENTAS_MCP:
            props = {}
            for pname, pdef in h["parametros"].items():
                props[pname] = {
                    "type":        pdef.get("type", "string"),
                    "description": pdef.get("description", ""),
                }
                if "default" in pdef:
                    props[pname]["default"] = pdef["default"]
            tools.append(mcp_types.Tool(
                name=h["nombre"],
                description=h["descripcion"],
                inputSchema={
                    "type":       "object",
                    "properties": props,
                    "required":   h.get("requeridos", []),
                }
            ))
        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        resultado = _ejecutar_herramienta(name, arguments or {})
        texto = json.dumps(resultado, ensure_ascii=False, indent=2) \
                if isinstance(resultado, (dict, list)) else str(resultado)
        return [mcp_types.TextContent(type="text", text=texto)]

    import asyncio
    async def _run():
        global _servidor_activo
        _servidor_activo = True
        async with stdio_server() as (read, write):
            await server.run(read, write,
                             server.create_initialization_options())
        _servidor_activo = False

    asyncio.run(_run())


# ══════════════════════════════════════════════════════════════════════════════
# SERVIDOR HTTP LIGERO (alternativa sin librería mcp)
# ══════════════════════════════════════════════════════════════════════════════

def iniciar_servidor_http(puerto: int = 8765, host: str = "127.0.0.1"):
    """
    Inicia un servidor HTTP JSON-RPC compatible con MCP.
    No requiere la librería mcp — usa solo stdlib.
    Endpoints:
      GET  /tools          → lista de herramientas
      POST /call           → ejecutar herramienta
      GET  /status         → estado del servidor
    """
    from http.server import HTTPServer, BaseHTTPRequestHandler

    class MCPHandler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            logger.debug(f"[MCP-HTTP] {fmt % args}")

        def _send_json(self, data: dict, code: int = 200):
            body = json.dumps(data, ensure_ascii=False, indent=2).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        def do_GET(self):
            if self.path == "/tools":
                self._send_json({"tools": HERRAMIENTAS_MCP})
            elif self.path == "/status":
                self._send_json({
                    "activo":     True,
                    "version":    "3.5",
                    "n_tools":    len(HERRAMIENTAS_MCP),
                    "n_llamadas": _n_llamadas,
                    "timestamp":  datetime.now().isoformat(),
                })
            else:
                self._send_json({"error": "Endpoint no encontrado"}, 404)

        def do_POST(self):
            if self.path == "/call":
                try:
                    length  = int(self.headers.get("Content-Length", 0))
                    body    = json.loads(self.rfile.read(length))
                    nombre  = body.get("name", body.get("tool", ""))
                    params  = body.get("arguments", body.get("params", {}))
                    resultado = _ejecutar_herramienta(nombre, params)
                    self._send_json({"result": resultado, "tool": nombre})
                except Exception as e:
                    self._send_json({"error": str(e)}, 500)
            else:
                self._send_json({"error": "Endpoint no encontrado"}, 404)

    global _servidor_activo, _puerto
    _puerto = puerto
    servidor = HTTPServer((host, puerto), MCPHandler)
    _servidor_activo = True
    logger.info(f"[MCP] Servidor HTTP iniciado en http://{host}:{puerto}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        _servidor_activo = False
        servidor.server_close()


def iniciar_mcp_background(puerto: int = 8765) -> threading.Thread:
    """Inicia el servidor MCP HTTP en un hilo de fondo."""
    t = threading.Thread(
        target=iniciar_servidor_http,
        args=(puerto,),
        daemon=True,
        name="mcp-server"
    )
    t.start()
    time.sleep(0.3)
    logger.info(f"[MCP] Servidor en background — http://127.0.0.1:{puerto}")
    return t


def get_mcp_status() -> dict:
    return {
        "activo":    _servidor_activo,
        "puerto":    _puerto,
        "n_tools":   len(HERRAMIENTAS_MCP),
        "n_llamadas":_n_llamadas,
        "mcp_lib_ok":MCP_OK,
    }


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN PARA CLIENTES MCP
# ══════════════════════════════════════════════════════════════════════════════

def generar_config_cliente(cliente: str = "claude_desktop") -> dict:
    """
    Genera la configuración JSON para conectar un cliente MCP a KALMIYA.

    Args:
        cliente: "claude_desktop" | "cursor" | "kiro" | "generic"
    """
    python_exe = sys.executable
    script_path = str(Path(__file__).resolve())

    config = {
        "mcpServers": {
            "kalmiya": {
                "command": python_exe,
                "args":    [script_path, "--stdio"],
                "env": {
                    "PYTHONPATH": str(Path(__file__).parent),
                }
            }
        }
    }
    return config


def imprimir_instrucciones_cliente():
    """Imprime cómo conectar clientes MCP a KALMIYA."""
    cfg = generar_config_cliente()
    cfg_json = json.dumps(cfg, indent=2)

    print("\n╔" + "═"*60 + "╗")
    print("║" + "  🔌  CONECTAR CLIENTES MCP A KALMIYA".center(60) + "║")
    print("╠" + "═"*60 + "╣")
    print("║                                                            ║")
    print("║  1. CLAUDE DESKTOP                                         ║")
    print("║     Agrega esto a claude_desktop_config.json:              ║")
    print("║                                                            ║")
    for linea in cfg_json.splitlines():
        print(f"║  {linea:<58}║")
    print("║                                                            ║")
    print("║  2. SERVIDOR HTTP (cualquier cliente)                      ║")
    print("║     python kalmiya_mcp.py --http                           ║")
    print("║     Endpoint: http://127.0.0.1:8765/call                   ║")
    print("║                                                            ║")
    print("╚" + "═"*60 + "╝\n")


# ── Modo standalone ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="KALMIYA MCP Server")
    parser.add_argument("--stdio", action="store_true", help="Modo stdio (Claude Desktop)")
    parser.add_argument("--http",  action="store_true", help="Modo HTTP")
    parser.add_argument("--puerto",type=int, default=8765)
    parser.add_argument("--config",action="store_true", help="Mostrar config cliente")
    args = parser.parse_args()

    if args.config:
        imprimir_instrucciones_cliente()
    elif args.stdio:
        iniciar_servidor_stdio()
    else:
        print(f"Iniciando servidor MCP HTTP en puerto {args.puerto}...")
        iniciar_servidor_http(puerto=args.puerto)
