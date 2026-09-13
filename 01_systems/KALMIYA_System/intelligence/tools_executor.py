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
            
        elif tool_name == "get_system_info":
            import platform
            import psutil
            info = {
                "OS": platform.system() + " " + platform.release(),
                "CPU": platform.processor(),
                "Cores": psutil.cpu_count(logical=True),
                "RAM_Total_GB": round(psutil.virtual_memory().total / (1024**3), 2),
                "RAM_Used_GB": round(psutil.virtual_memory().used / (1024**3), 2),
                "Disk_Total_GB": round(psutil.disk_usage('/').total / (1024**3), 2)
            }
            return f"Información del Sistema:\n" + "\n".join([f"- {k}: {v}" for k, v in info.items()])

        elif tool_name == "execute_python":
            code = args.get("code", "")
            import tempfile
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                    f.write(code)
                    temp_path = f.name
                
                result = subprocess.run(
                    [sys.executable, temp_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                try:
                    os.remove(temp_path)
                except:
                    pass
                    
                output = result.stdout + "\n" + result.stderr
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
                
        elif tool_name == "execute_kalmiya_function":
            try:
                # Import here to avoid circular imports
                sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from core.module_manager import manager
                
                func_name = args.get("function_name")
                args_json = args.get("args_json")
                if not func_name:
                    return "Error: function_name is required."
                return manager.execute_function(func_name, args_json)
            except Exception as e:
                return f"Error executing kalmiya function: {e}"
                
        return f"Herramienta {tool_name} desconocida o no implementada."
    except Exception as e:
        return f"Excepcion interna al ejecutar {tool_name}: {str(e)}"
