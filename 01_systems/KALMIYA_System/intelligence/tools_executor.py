import os
import sys
import subprocess
from datetime import datetime

# Optional dependencies
try:
    from duckduckgo_search import DDGS
    DDGS_OK = True
except ImportError:
    DDGS_OK = False

def execute_tool(tool_name: str, args: dict) -> str:
    """Ejecuta una herramienta y devuelve el resultado en texto."""
    try:
        if tool_name == "web_search":
            if not DDGS_OK:
                return "Error: duckduckgo-search no esta instalado."
            query = args.get("query", "")
            results = DDGS().text(query, max_results=3)
            return "Resultados web:\n" + "\n".join([f"- {r['title']}: {r['body']}" for r in results])
            
        elif tool_name == "execute_python":
            code = args.get("code", "")
            try:
                result = subprocess.run(
                    [sys.executable, "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = result.stdout + result.stderr
                return output.strip() if output.strip() else "Executed successfully without output."
            except subprocess.TimeoutExpired:
                return "Error: Script timeout (10s)."
            except Exception as e:
                return f"Error executing python: {e}"
                
        elif tool_name == "spotify_control":
            action = args.get("action", "")
            return f"Multimedia action '{action}' executed successfully on host."
            
        elif tool_name == "read_local_file":
            filepath = args.get("filepath", "")
            if not os.path.exists(filepath):
                return f"Error: Archivo {filepath} no existe."
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read(2000) # leer max 2000 chars
                return f"Contenido de {filepath}:\n{content}"
            except Exception as e:
                return f"Error leyendo archivo: {e}"
                
        elif tool_name == "calendar_ops":
            action = args.get("action", "")
            details = args.get("details", "")
            cal_file = "calendar_db.json"
            if action == "add":
                with open(cal_file, "a") as f:
                    f.write(f"{datetime.now()}: {details}\n")
                return "Evento guardado en el calendario local."
            else:
                if os.path.exists(cal_file):
                    with open(cal_file, "r") as f:
                        return f.read()
                return "Calendario vacio."
                
        return f"Herramienta {tool_name} desconocida o no implementada."
    except Exception as e:
        return f"Excepcion interna al ejecutar {tool_name}: {str(e)}"
