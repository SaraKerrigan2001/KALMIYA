"""
kalmiya_skills.py — Sistema de Skills Modulares para KALMIYA
=============================================================
Skills = funciones especializadas que KALMIYA puede encadenar
automáticamente para resolver tareas complejas.

Diferencia con funciones normales:
  - Se auto-descubren y registran sin tocar el código principal
  - Se pueden encadenar: salida de una skill → entrada de otra
  - Tienen metadatos: nombre, descripción, categoría, ejemplos
  - Se invocan desde CLI, MCP, chat y voz con la misma interfaz

Categorías:
  - productividad: notas, resúmenes, tareas
  - codigo:        generar, explicar, corregir, traducir código
  - info:          clima, noticias, búsqueda web
  - sistema:       archivos, procesos, disco
  - idiomas:       traducir, detectar idioma
  - creatividad:   generar texto, ideas, dibujos ASCII
"""

import os, sys, inspect, json
from pathlib import Path
from datetime import datetime
from typing import Any, Callable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _logging import get_logger
from database import log_command

logger = get_logger(__name__)

# ── Registro de skills ─────────────────────────────────────────────────────────
_registro: dict[str, dict] = {}


def skill(nombre: str, descripcion: str, categoria: str = "general",
          ejemplos: list = None, aliases: list = None):
    """
    Decorador para registrar una función como skill de KALMIYA.

    Uso:
        @skill("traducir", "Traduce texto", categoria="idiomas",
               ejemplos=["traducir 'hola' al inglés"])
        def skill_traducir(texto: str, destino: str = "en") -> str:
            ...
    """
    def decorador(func: Callable) -> Callable:
        _registro[nombre] = {
            "nombre":      nombre,
            "descripcion": descripcion,
            "categoria":   categoria,
            "ejemplos":    ejemplos or [],
            "aliases":     aliases or [],
            "funcion":     func,
            "parametros":  list(inspect.signature(func).parameters.keys()),
        }
        for alias in (aliases or []):
            _registro[alias] = _registro[nombre]
        logger.debug(f"[SKILLS] Registrada: {nombre}")
        return func
    return decorador


# ══════════════════════════════════════════════════════════════════════════════
# SKILLS IMPLEMENTADAS
# ══════════════════════════════════════════════════════════════════════════════

# ── Idiomas ────────────────────────────────────────────────────────────────────

@skill("traducir", "Traduce texto a cualquier idioma",
       categoria="idiomas",
       aliases=["translate", "trans"],
       ejemplos=["traducir 'hola mundo' al inglés",
                 "translate 'good morning' to Spanish"])
def skill_traducir(texto: str, destino: str = "en") -> str:
    from kalmiya_nuevas_funciones import traducir
    return traducir(texto, destino)


@skill("detectar_idioma", "Detecta el idioma de un texto",
       categoria="idiomas",
       aliases=["detect_lang"],
       ejemplos=["detectar_idioma 'Bonjour le monde'"])
def skill_detectar_idioma(texto: str) -> str:
    try:
        from brain import ask_kalmiya
        resp = ask_kalmiya(
            f"¿En qué idioma está escrito este texto? "
            f"Responde SOLO con el nombre del idioma en español.\n\nTexto: {texto}",
            force_engine="gemini"
        )
        return resp.strip()
    except Exception as e:
        return f"Error: {e}"


# ── Código ────────────────────────────────────────────────────────────────────

@skill("generar_codigo", "Genera un snippet de código funcional",
       categoria="codigo",
       aliases=["codigo", "code", "snippet"],
       ejemplos=["generar_codigo 'función que ordena una lista' Python",
                 "snippet 'conectar a MySQL' Python"])
def skill_generar_codigo(descripcion: str, lenguaje: str = "Python") -> str:
    from kalmiya_nuevas_funciones import generar_snippet
    return generar_snippet(descripcion, lenguaje)


@skill("explicar_codigo", "Explica qué hace un fragmento de código",
       categoria="codigo",
       aliases=["explicar", "explain"],
       ejemplos=["explicar_codigo 'for i in range(10): print(i)' Python"])
def skill_explicar_codigo(codigo: str, lenguaje: str = "Python") -> str:
    from kalmiya_nuevas_funciones import explicar_codigo
    return explicar_codigo(codigo, lenguaje)


@skill("corregir_error", "Analiza un error y propone la solución",
       categoria="codigo",
       aliases=["debug", "fix", "arreglar"],
       ejemplos=["corregir_error 'NameError: name x is not defined'"])
def skill_corregir_error(error: str, contexto: str = "") -> str:
    from kalmiya_nuevas_funciones import buscar_solucion_error
    return buscar_solucion_error(error, contexto)


@skill("convertir_codigo", "Convierte código de un lenguaje a otro",
       categoria="codigo",
       aliases=["convertir", "portar"],
       ejemplos=["convertir_codigo 'print(x)' de Python a JavaScript"])
def skill_convertir_codigo(codigo: str, de_lang: str = "Python",
                            a_lang: str = "JavaScript") -> str:
    from brain import ask_kalmiya
    return ask_kalmiya(
        f"Convierte este código de {de_lang} a {a_lang}. "
        f"Solo devuelve el código convertido sin explicaciones:\n\n{codigo}",
        force_engine="gemini"
    )


# ── Productividad ─────────────────────────────────────────────────────────────

@skill("resumir", "Resume un texto largo en puntos clave",
       categoria="productividad",
       aliases=["resumen", "summary"],
       ejemplos=["resumir 'texto largo aquí...'",
                 "resumen 'artículo de noticias'"])
def skill_resumir(texto: str, max_puntos: int = 5) -> str:
    from brain import ask_kalmiya
    return ask_kalmiya(
        f"Resume este texto en máximo {max_puntos} puntos clave en español. "
        f"Formato: lista con viñetas.\n\n{texto[:4000]}",
        force_engine="gemini"
    )


@skill("crear_nota_rapida", "Crea una nota rápida en Obsidian",
       categoria="productividad",
       aliases=["nota", "note", "anotar"],
       ejemplos=["nota 'Recordar estudiar triggers SQL'",
                 "crear_nota_rapida 'Ideas proyecto ADSO'"])
def skill_crear_nota_rapida(contenido: str, titulo: str = "") -> str:
    from obsidian_bridge import create_note
    if not titulo:
        titulo = f"Nota {datetime.now().strftime('%Y-%m-%d %H-%M')}"
    path = create_note(titulo, contenido, tags=["rapida", "kalmiya"])
    return f"Nota creada: {path.name}"


@skill("buscar_notas", "Busca en las notas de Obsidian",
       categoria="productividad",
       aliases=["buscar", "search"],
       ejemplos=["buscar_notas 'Python clases herencia'",
                 "search 'ADSO módulo 3'"])
def skill_buscar_notas(query: str, top_k: int = 5) -> list:
    from kalmiya_rag import buscar_rag, _init_rag
    _init_rag()
    resultados = buscar_rag(query, top_k=top_k, filtro_tipo=".md")
    return [{"fuente": r["fuente"], "similitud": r["similitud"],
             "preview": r["texto"][:150]} for r in resultados]


@skill("generar_tareas", "Descompone un objetivo en tareas accionables",
       categoria="productividad",
       aliases=["tareas", "tasks", "planear"],
       ejemplos=["generar_tareas 'Aprender Django para el proyecto ADSO'"])
def skill_generar_tareas(objetivo: str, n_tareas: int = 5) -> str:
    from brain import ask_kalmiya
    return ask_kalmiya(
        f"Descompón este objetivo en {n_tareas} tareas específicas y accionables. "
        f"Formato: lista numerada con pasos concretos.\n\nObjetivo: {objetivo}",
        force_engine="gemini"
    )


# ── Información ───────────────────────────────────────────────────────────────

@skill("clima", "Obtiene el clima actual y pronóstico de 7 días",
       categoria="info",
       aliases=["weather", "tiempo"],
       ejemplos=["clima Cúcuta", "weather Bogotá"])
def skill_clima(ciudad: str = "Cúcuta") -> dict:
    from kalmiya_nuevas_funciones import get_real_weather
    return get_real_weather(ciudad)


@skill("wikipedia", "Busca información en Wikipedia",
       categoria="info",
       aliases=["wiki", "buscar_web"],
       ejemplos=["wikipedia 'Python programming language'",
                 "wiki 'SENA Colombia'"])
def skill_wikipedia(query: str, oraciones: int = 3) -> str:
    from online_ops import search_on_wikipedia
    resultado = search_on_wikipedia(query)
    return resultado or "No encontré información sobre ese tema."


@skill("calcular", "Evalúa expresiones matemáticas de forma segura",
       categoria="info",
       aliases=["calc", "math"],
       ejemplos=["calcular '2 ** 10'", "calc 'sqrt(144)'"])
def skill_calcular(expresion: str) -> str:
    import math as _math
    try:
        # Solo permitir operaciones matemáticas seguras
        permitidos = {k: getattr(_math, k) for k in dir(_math) if not k.startswith("_")}
        permitidos.update({"abs": abs, "round": round, "min": min, "max": max, "sum": sum})
        resultado = eval(expresion, {"__builtins__": {}}, permitidos)
        return str(resultado)
    except Exception as e:
        return f"Error: {e}"


@skill("graphify", "Explica qué es Graphify y cómo usarlo con KALMIYA",
       categoria="info",
       aliases=["knowledge_graph", "grafo_conocimiento"],
       ejemplos=["graphify", "knowledge_graph 'cómo usarlo'"])
def skill_graphify(consulta: str = "") -> dict:
    from kalmiya_nuevas_funciones import obtener_informacion_graphify
    info = obtener_informacion_graphify()
    if consulta.strip().lower().startswith("instal"):
        info["respuesta"] = "Para instalarlo usa uv tool install graphifyy y luego graphify install."
    elif consulta.strip().lower().startswith("mcp"):
        info["respuesta"] = f"Para exponer el grafo como MCP usa: {info['mcp']}"
    else:
        info["respuesta"] = (
            f"{info['titulo']} convierte tu proyecto en un grafo de conocimiento consultable. "
            f"Sirve para responder preguntas sobre arquitectura, relaciones y contexto, "
            f"y puede integrarse con asistentes como KALMIYA."
        )
    return info


# ── Sistema ───────────────────────────────────────────────────────────────────

@skill("info_sistema", "Muestra el estado del sistema (CPU, RAM, disco)",
       categoria="sistema",
       aliases=["sistema", "system"],
       ejemplos=["info_sistema", "sistema"])
def skill_info_sistema() -> dict:
    from kalmiya_system_info import resumen_sistema_completo
    data = resumen_sistema_completo()
    return {
        "cpu_uso":   data["cpu"].get("uso_total_pct"),
        "ram_uso":   data["ram"].get("uso_pct"),
        "ram_gb":    data["ram"].get("total_gb"),
        "gpus":      [g["nombre"] for g in data.get("gpus", [])],
    }


@skill("listar_archivos", "Lista archivos de una carpeta",
       categoria="sistema",
       aliases=["ls", "dir", "archivos"],
       ejemplos=["listar_archivos 'D:/Steam'",
                 "ls 'c:/Users/maria/Documents'"])
def skill_listar_archivos(carpeta: str = ".", extension: str = "") -> list:
    ruta = Path(carpeta).expanduser()
    if not ruta.exists():
        return [f"Carpeta no encontrada: {carpeta}"]
    patron = f"*{extension}" if extension else "*"
    return [str(p.name) for p in sorted(ruta.glob(patron))[:50]]


# ── Creatividad ───────────────────────────────────────────────────────────────

@skill("ideas", "Genera ideas creativas sobre un tema",
       categoria="creatividad",
       aliases=["brainstorm", "ideas_para"],
       ejemplos=["ideas 'proyecto final ADSO'",
                 "brainstorm 'app para el SENA'"])
def skill_ideas(tema: str, n_ideas: int = 5) -> str:
    from brain import ask_kalmiya
    return ask_kalmiya(
        f"Genera {n_ideas} ideas creativas y originales sobre: {tema}. "
        f"Formato: lista numerada. Sé específico y práctico.",
        force_engine="gemini"
    )


@skill("contraseña", "Genera contraseñas seguras",
       categoria="sistema",
       aliases=["password", "pwd"],
       ejemplos=["contraseña", "password 20", "pwd 16 3"])
def skill_contrasena(longitud: int = 16, cantidad: int = 1) -> list:
    from kalmiya_nuevas_funciones import generar_password
    return generar_password(longitud, True, cantidad)


# ══════════════════════════════════════════════════════════════════════════════
# MOTOR DE EJECUCIÓN Y ENCADENAMIENTO
# ══════════════════════════════════════════════════════════════════════════════

def ejecutar_skill(nombre: str, args: list = None,
                   kwargs: dict = None) -> Any:
    """
    Ejecuta una skill por nombre con sus argumentos.

    Args:
        nombre: Nombre o alias de la skill.
        args:   Argumentos posicionales.
        kwargs: Argumentos por nombre.

    Returns:
        Resultado de la skill o mensaje de error.
    """
    skill_info = _registro.get(nombre.lower())
    if not skill_info:
        # Intentar coincidencia parcial
        for k in _registro:
            if nombre.lower() in k.lower():
                skill_info = _registro[k]
                break

    if not skill_info:
        return f"Skill '{nombre}' no encontrada. " \
               f"Skills disponibles: {', '.join(listar_nombres())}"

    try:
        funcion = skill_info["funcion"]
        params  = inspect.signature(funcion).parameters
        args    = args   or []
        kwargs  = kwargs or {}

        # Convertir args posicionales a kwargs
        param_names = list(params.keys())
        for i, val in enumerate(args):
            if i < len(param_names):
                kwargs[param_names[i]] = _convertir_tipo(
                    val, params[param_names[i]])

        resultado = funcion(**kwargs)
        log_command(f"[SKILL] {nombre}", str(args)[:100], source="modules")
        return resultado

    except TypeError as e:
        return f"Error de parámetros en '{nombre}': {e}"
    except Exception as e:
        logger.error(f"[SKILLS] Error en '{nombre}': {e}")
        return f"Error ejecutando '{nombre}': {e}"


def _convertir_tipo(valor: str, parametro) -> Any:
    """Convierte un string al tipo esperado por el parámetro."""
    try:
        anotacion = parametro.annotation
        if anotacion == int or (hasattr(parametro, "default") and
                                 isinstance(parametro.default, int)):
            return int(valor)
        if anotacion == float:
            return float(valor)
        if anotacion == bool:
            return valor.lower() in ("true", "1", "si", "yes")
    except Exception:
        pass
    return valor


def encadenar_skills(pipeline: list[dict]) -> list[Any]:
    """
    Ejecuta una cadena de skills donde la salida de una
    puede ser entrada de la siguiente.

    Args:
        pipeline: Lista de dicts con 'skill', 'args', 'kwargs', 'usar_resultado_anterior'

    Ejemplo:
        encadenar_skills([
            {"skill": "wikipedia", "args": ["Python"]},
            {"skill": "resumir",   "usar_resultado_anterior": True},
            {"skill": "traducir",  "kwargs": {"destino": "en"},
             "usar_resultado_anterior": True}
        ])

    Returns:
        Lista con los resultados de cada skill.
    """
    resultados = []
    ultimo_resultado = None

    for paso in pipeline:
        nombre   = paso.get("skill", "")
        args     = list(paso.get("args", []))
        kwargs   = dict(paso.get("kwargs", {}))
        usar_ant = paso.get("usar_resultado_anterior", False)

        if usar_ant and ultimo_resultado is not None:
            if isinstance(ultimo_resultado, str):
                if args:
                    args[0] = ultimo_resultado
                else:
                    args = [ultimo_resultado]

        resultado = ejecutar_skill(nombre, args, kwargs)
        resultados.append({"skill": nombre, "resultado": resultado})
        ultimo_resultado = resultado

    return resultados


def listar_skills() -> list[dict]:
    """Lista todas las skills registradas sin duplicados por alias."""
    vistos = set()
    result = []
    for uid, s in _registro.items():
        if s["nombre"] not in vistos:
            vistos.add(s["nombre"])
            result.append({
                "nombre":      s["nombre"],
                "descripcion": s["descripcion"],
                "categoria":   s["categoria"],
                "aliases":     s["aliases"],
                "parametros":  s["parametros"],
                "ejemplos":    s["ejemplos"],
            })
    return sorted(result, key=lambda x: (x["categoria"], x["nombre"]))


def listar_nombres() -> list[str]:
    """Lista solo los nombres de skills (sin aliases)."""
    vistos = set()
    return [s["nombre"] for s in listar_skills()
            if s["nombre"] not in vistos and not vistos.add(s["nombre"])]


def buscar_skill_por_intencion(texto: str) -> Optional_skill:
    """Detecta qué skill usar basándose en el texto del usuario."""
    texto_lower = texto.lower()
    mejores = []

    for nombre, s in _registro.items():
        if s["nombre"] != nombre:  # Skip aliases
            continue
        score = 0
        # Coincidencia directa con nombre
        if nombre in texto_lower:
            score += 10
        # Coincidencia con aliases
        for alias in s["aliases"]:
            if alias in texto_lower:
                score += 8
        # Coincidencia con palabras clave de descripción
        for palabra in s["descripcion"].lower().split():
            if len(palabra) > 3 and palabra in texto_lower:
                score += 2
        if score > 0:
            mejores.append((score, nombre))

    if mejores:
        mejores.sort(reverse=True)
        return mejores[0][1]
    return None


# Tipo para la función anterior
from typing import Optional as Optional_skill


def imprimir_skills():
    """Imprime todas las skills disponibles."""
    skills = listar_skills()
    categorias: dict[str, list] = {}
    for s in skills:
        categorias.setdefault(s["categoria"], []).append(s)

    print("\n╔" + "═"*60 + "╗")
    print("║" + "  ⚡  KALMIYA SKILLS — Funciones disponibles".center(60) + "║")
    print("╚" + "═"*60 + "╝")
    for cat, lista in sorted(categorias.items()):
        print(f"\n  [{cat.upper()}]")
        for s in lista:
            aliases = f"  (alias: {', '.join(s['aliases'])})" if s["aliases"] else ""
            print(f"  • {s['nombre']:<22} {s['descripcion']}{aliases}")
    print()
