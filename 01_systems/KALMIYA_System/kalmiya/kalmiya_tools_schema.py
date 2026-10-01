"""
kalmiya_tools_schema.py — Definición de Tools para LLM (Function Calling)
===========================================================================
Contiene los esquemas en formato JSON compatibles con Gemini y OpenAI/Groq
para habilitar el uso nativo de herramientas.
"""

# ══════════════════════════════════════════════════════════════════════════════
#  GEMINI TOOLS SCHEMA
# ══════════════════════════════════════════════════════════════════════════════

GEMINI_TOOLS = [
    {
        "functionDeclarations": [
            {
                "name": "get_system_info",
                "description": "Obtiene información completa del sistema operativo, CPU, RAM y disco."
            },
            {
                "name": "analyze_network_security",
                "description": "Analiza la red local para protección contra malware y detección de amenazas."
            },
            {
                "name": "execute_kalmiya_function",
                "description": "Ejecuta una función extendida de KALMIYA (Módulos).",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "function_name": {
                            "type": "STRING",
                            "description": "El nombre de la función a ejecutar (ej: 'get_weather', 'add_todo', 'create_trip')."
                        },
                        "args_json": {
                            "type": "STRING",
                            "description": "Argumentos extra opcionales en formato JSON string."
                        }
                    },
                    "required": ["function_name"]
                }
            },
            {
                "name": "execute_in_sandbox",
                "description": "Ejecuta código o un comando riesgoso en un contenedor Docker aislado para seguridad.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "command": {
                            "type": "STRING",
                            "description": "El comando de terminal o script a ejecutar en el sandbox."
                        }
                    },
                    "required": ["command"]
                }
            }
        ]
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Busca informacion en internet en tiempo real usando DuckDuckGo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": { "type": "string", "description": "La consulta de busqueda" }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": "Ejecuta codigo Python localmente y devuelve la salida (stdout). Util para calculos complejos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": { "type": "string", "description": "Codigo fuente python" }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "spotify_control",
            "description": "Controla la reproduccion local de musica o multimedia.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": { "type": "string", "enum": ["play", "pause", "next", "prev"] }
                },
                "required": ["action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_local_file",
            "description": "Lee el contenido de un archivo local en texto plano.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": { "type": "string", "description": "Ruta absoluta o relativa del archivo" }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calendar_ops",
            "description": "Agrega o consulta tareas temporales o recordatorios.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": { "type": "string", "enum": ["add", "list"] },
                    "details": { "type": "string", "description": "Detalles del recordatorio a guardar (solo si add)" }
                },
                "required": ["action"]
            }
        }
    }
]

# ══════════════════════════════════════════════════════════════════════════════
#  OPENAI / GROQ TOOLS SCHEMA
# ══════════════════════════════════════════════════════════════════════════════

OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_system_info",
            "description": "Obtiene información completa del sistema operativo, CPU, RAM y disco."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_network_security",
            "description": "Analiza la red local para protección contra malware y detección de amenazas."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_kalmiya_function",
            "description": "Ejecuta una función extendida de KALMIYA (Módulos).",
            "parameters": {
                "type": "object",
                "properties": {
                    "function_name": {
                        "type": "string",
                        "description": "El nombre de la función a ejecutar (ej: 'get_weather', 'add_todo')."
                    },
                    "args_json": {
                        "type": "string",
                        "description": "Argumentos extra opcionales en formato JSON string."
                    }
                },
                "required": ["function_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_in_sandbox",
            "description": "Ejecuta código o un comando riesgoso en un contenedor Docker aislado para seguridad.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "El comando de terminal o script a ejecutar en el sandbox."
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Busca informacion en internet en tiempo real usando DuckDuckGo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": { "type": "string", "description": "La consulta de busqueda" }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": "Ejecuta codigo Python localmente y devuelve la salida (stdout). Util para calculos complejos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": { "type": "string", "description": "Codigo fuente python" }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "spotify_control",
            "description": "Controla la reproduccion local de musica o multimedia.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": { "type": "string", "enum": ["play", "pause", "next", "prev"] }
                },
                "required": ["action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_local_file",
            "description": "Lee el contenido de un archivo local en texto plano.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": { "type": "string", "description": "Ruta absoluta o relativa del archivo" }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calendar_ops",
            "description": "Agrega o consulta tareas temporales o recordatorios.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": { "type": "string", "enum": ["add", "list"] },
                    "details": { "type": "string", "description": "Detalles del recordatorio a guardar (solo si add)" }
                },
                "required": ["action"]
            }
        }
    }
]
