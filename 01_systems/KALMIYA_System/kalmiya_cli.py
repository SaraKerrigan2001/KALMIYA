"""
kalmiya_cli.py — Interfaz de Línea de Comandos de KALMIYA
==========================================================
Permite usar KALMIYA desde cualquier terminal con comandos rápidos:

  python kalmiya_cli.py "¿cuál es el clima en Cúcuta?"
  python kalmiya_cli.py --rag "explica qué es ADSO"
  python kalmiya_cli.py --skill traducir "hello world" --a es
  python kalmiya_cli.py --sistema
  python kalmiya_cli.py --indexar
  python kalmiya_cli.py --chat   (modo interactivo)

Uso:
  kalmiya "pregunta"              → respuesta directa con IA
  kalmiya --rag "pregunta"        → respuesta con contexto de tus documentos
  kalmiya --skill NOMBRE args     → ejecutar una skill específica
  kalmiya --sistema               → info del sistema
  kalmiya --indexar               → indexar documentos para RAG
  kalmiya --chat                  → modo conversación interactiva
  kalmiya --estado                → estado de todos los módulos
  kalmiya --version               → versión del sistema
"""

import sys
import os
import argparse
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Colores ANSI ──────────────────────────────────────────────────────────────
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"
PURPLE = "\033[95m"

VERSION = "3.5.0"
BANNER  = f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════╗
║          KALMIYA Neural Core v{VERSION}              ║
║     Asistente IA Personal de Sara Kerrigan        ║
╚══════════════════════════════════════════════════╝{RESET}
"""


def _print_ok(msg):   print(f"{GREEN}✅  {msg}{RESET}")
def _print_warn(msg): print(f"{YELLOW}⚠️   {msg}{RESET}")
def _print_err(msg):  print(f"{RED}❌  {msg}{RESET}")
def _print_info(msg): print(f"{CYAN}ℹ️   {msg}{RESET}")


def _separador():
    print(f"{DIM}{'─' * 55}{RESET}")


# ══════════════════════════════════════════════════════════════════════════════
# COMANDOS
# ══════════════════════════════════════════════════════════════════════════════

def cmd_preguntar(query: str, usar_rag: bool = False,
                  engine: str = "") -> str:
    """Hace una pregunta a KALMIYA con o sin RAG."""
    try:
        if usar_rag:
            from kalmiya_rag import responder_con_rag, buscar_rag
            chunks = buscar_rag(query, top_k=3)
            if chunks:
                _print_info(f"RAG: {len(chunks)} fragmentos encontrados en tus documentos")
                for c in chunks[:2]:
                    print(f"  {DIM}📄 {c['fuente']} (similitud: {c['similitud']}){RESET}")
                _separador()
            respuesta = responder_con_rag(query, force_engine=engine)
        else:
            from brain import ask_kalmiya, get_engine_status
            respuesta = ask_kalmiya(query, force_engine=engine)
            motor     = get_engine_status()["motor_usado"]
            print(f"{DIM}  🧠 Motor: {motor}{RESET}")

        print(f"\n{CYAN}{BOLD}KALMIYA:{RESET} {respuesta}\n")
        return respuesta

    except Exception as e:
        _print_err(f"Error al procesar la pregunta: {e}")
        return ""


def cmd_chat_interactivo(usar_rag: bool = False, engine: str = ""):
    """Modo conversación interactiva en la terminal."""
    print(BANNER)
    print(f"{PURPLE}Modo chat interactivo — escribe 'salir' para terminar{RESET}")
    print(f"{DIM}RAG: {'activado' if usar_rag else 'desactivado'} | "
          f"Motor: {engine or 'auto'}{RESET}\n")
    _separador()

    try:
        from brain import clear_conversation
        clear_conversation()
    except Exception:
        pass

    historial = []

    while True:
        try:
            entrada = input(f"\n{YELLOW}{BOLD}Sara:{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}Chat cerrado. Hasta pronto, Sara.{RESET}")
            break

        if not entrada:
            continue
        if entrada.lower() in ("salir", "exit", "quit", "bye", "adios", "adiós"):
            print(f"\n{CYAN}KALMIYA:{RESET} Hasta pronto, Sara. 👋\n")
            break

        # Comandos especiales dentro del chat
        if entrada.startswith("/"):
            _procesar_comando_chat(entrada, usar_rag)
            continue

        respuesta = cmd_preguntar(entrada, usar_rag=usar_rag, engine=engine)
        historial.append({"usuario": entrada, "kalmiya": respuesta})

    # Ofrecer guardar el chat
    if historial:
        try:
            guardar = input(f"\n{DIM}¿Guardar esta conversación en Obsidian? (s/n): {RESET}").strip().lower()
            if guardar in ("s", "si", "sí", "y", "yes"):
                from obsidian_bridge import save_conversation_to_obsidian, get_vault
                msgs = []
                for h in historial:
                    msgs.append({"role": "user",      "content": h["usuario"]})
                    msgs.append({"role": "assistant",  "content": h["kalmiya"]})
                path = save_conversation_to_obsidian(msgs)
                _print_ok(f"Chat guardado: {path.relative_to(get_vault())}")
        except Exception:
            pass


def _procesar_comando_chat(cmd: str, usar_rag: bool):
    """Procesa comandos especiales dentro del chat (/rag, /estado, etc.)."""
    if cmd == "/rag":
        _print_info("Buscando en tus documentos...")
    elif cmd == "/limpiar":
        try:
            from brain import clear_conversation
            clear_conversation()
            _print_ok("Historial de conversación limpiado.")
        except Exception:
            pass
    elif cmd == "/estado":
        cmd_estado()
    elif cmd == "/indexar":
        cmd_indexar()
    elif cmd.startswith("/skill "):
        partes = cmd.split()
        if len(partes) >= 2:
            cmd_skill(partes[1], partes[2:])
    else:
        print(f"{DIM}Comandos: /rag /limpiar /estado /indexar /skill NOMBRE{RESET}")


def cmd_indexar(carpeta: str = None, forzar: bool = False):
    """Indexa documentos para RAG."""
    from kalmiya_rag import indexar_vault, get_rag_stats, VAULT_PATH
    print(f"\n{CYAN}Indexando documentos para RAG...{RESET}")
    ruta   = Path(carpeta) if carpeta else VAULT_PATH
    stats  = indexar_vault(ruta, mostrar_progreso=True)
    s      = get_rag_stats()
    print(f"\n{GREEN}Total en base vectorial: {s['chunks_en_db']} chunks{RESET}")


def cmd_buscar_rag(query: str, top_k: int = 5):
    """Busca en los documentos indexados y muestra los resultados."""
    from kalmiya_rag import buscar_rag, _init_rag
    _init_rag()
    print(f"\n{CYAN}🔍 Buscando: '{query}'{RESET}\n")
    resultados = buscar_rag(query, top_k=top_k)

    if not resultados:
        _print_warn("No se encontraron resultados. ¿Has indexado tus documentos? (--indexar)")
        return

    for i, r in enumerate(resultados, 1):
        print(f"{BOLD}[{i}] {r['fuente']}{RESET}  {DIM}similitud: {r['similitud']}{RESET}")
        preview = r["texto"][:200].replace("\n", " ")
        print(f"    {preview}...")
        print()


def cmd_skill(nombre: str, args: list):
    """Ejecuta una skill de KALMIYA."""
    try:
        from kalmiya_skills import ejecutar_skill, listar_skills
        if nombre in ("lista", "list", "help"):
            skills = listar_skills()
            print(f"\n{CYAN}Skills disponibles:{RESET}")
            for s in skills:
                print(f"  {GREEN}• {s['nombre']:<20}{RESET} {DIM}{s['descripcion']}{RESET}")
            return
        resultado = ejecutar_skill(nombre, args)
        if resultado:
            print(f"\n{CYAN}Resultado:{RESET}")
            if isinstance(resultado, dict):
                print(json.dumps(resultado, indent=2, ensure_ascii=False))
            else:
                print(resultado)
    except ImportError:
        _print_err("Módulo de skills no disponible")
    except Exception as e:
        _print_err(f"Error ejecutando skill '{nombre}': {e}")


def cmd_sistema():
    """Muestra información del sistema."""
    try:
        from kalmiya_system_info import resumen_sistema_completo, espacio_libre_rapido
        print(f"\n{CYAN}{BOLD}=== SISTEMA ==={RESET}")
        data  = resumen_sistema_completo()
        cpu   = data.get("cpu", {})
        ram   = data.get("ram", {})
        gpus  = data.get("gpus", [])
        print(f"  CPU : {cpu.get('nombre','?')}")
        print(f"  Uso : {cpu.get('uso_total_pct','?')}%  "
              f"Núcleos: {cpu.get('nucleos_fisicos','?')}F/{cpu.get('nucleos_logicos','?')}L")
        print(f"  RAM : {ram.get('usada_gb','?')}/{ram.get('total_gb','?')} GB "
              f"({ram.get('uso_pct','?')}%)")
        for g in gpus:
            print(f"  GPU : {g['nombre']}  {g['vram_gb']} GB VRAM")
        print(f"\n{CYAN}=== DISCOS ==={RESET}")
        esp = espacio_libre_rapido()
        for disco, v in esp.items():
            barra = "█" * int(v["uso_pct"] / 5)
            print(f"  {disco}  {barra:<20} {v['uso_pct']}%  "
                  f"libre: {v['libre_gb']} GB  {v['estado']}")
    except Exception as e:
        _print_err(f"Error: {e}")


def cmd_estado():
    """Muestra el estado de todos los módulos."""
    print(f"\n{CYAN}{BOLD}=== KALMIYA v{VERSION} — Estado de módulos ==={RESET}\n")

    # Motores IA
    try:
        from brain import get_engine_status
        est = get_engine_status()
        print(f"{BOLD}🧠 Motores de IA:{RESET}")
        print(f"  Modo: {est.get('modo_actual','?')} | "
              f"Último: {est.get('motor_usado','ninguno')}")
        for motor, key in [
            ("Ollama",      "ollama_activo"),
            ("Gemini",      "gemini_activo"),
            ("Claude",      "claude_activo"),
            ("Groq",        "groq_activo"),
            ("OpenRouter",  "openrouter_activo"),
            ("Cohere",      "cohere_activo"),
        ]:
            ico = "✅" if est.get(key) else "❌"
            print(f"  {ico} {motor}")
    except Exception as e:
        _print_warn(f"Motores IA: {e}")

    # RAG
    print(f"\n{BOLD}📚 RAG:{RESET}")
    try:
        from kalmiya_rag import get_rag_stats
        s = get_rag_stats()
        ico = "✅" if s["disponible"] else "⚠️ "
        print(f"  {ico} ChromaDB: {'OK' if s['chroma_ok'] else 'No instalado'}")
        print(f"  {'✅' if s['embeddings_ok'] else '⚠️ '} Embeddings: "
              f"{'sentence-transformers' if s['embeddings_ok'] else 'básico'}")
        print(f"  📄 {s['chunks_en_db']} chunks indexados")
        print(f"  🕐 Último indexado: {s['ultimo_indexado'][:19] if s['ultimo_indexado'] != 'Nunca' else 'Nunca'}")
    except Exception as e:
        _print_warn(f"RAG: {e}")

    # MCP
    print(f"\n{BOLD}🔌 MCP:{RESET}")
    try:
        from kalmiya_mcp import get_mcp_status
        mcp = get_mcp_status()
        print(f"  {'✅' if mcp.get('activo') else '❌'} Servidor: "
              f"{'activo en puerto ' + str(mcp.get('puerto','?')) if mcp.get('activo') else 'detenido'}")
        print(f"  🔧 {mcp.get('n_tools', 0)} herramientas registradas")
    except Exception as e:
        _print_warn(f"MCP: {e}")

    # Skills
    print(f"\n{BOLD}⚡ Skills:{RESET}")
    try:
        from kalmiya_skills import listar_skills
        skills = listar_skills()
        print(f"  ✅ {len(skills)} skills disponibles: "
              f"{', '.join(s['nombre'] for s in skills[:5])}")
    except Exception as e:
        _print_warn(f"Skills: {e}")

    # BD
    print(f"\n{BOLD}🗄️  Base de datos:{RESET}")
    try:
        from database import get_db_stats
        db = get_db_stats()
        print(f"  ✅ {db.get('command_history',0)} comandos | "
              f"{db.get('neural_thoughts',0)} pensamientos | "
              f"{db.get('size_kb',0)} KB")
    except Exception as e:
        _print_warn(f"BD: {e}")

    print()


def cmd_version():
    """Muestra la versión del sistema."""
    print(BANNER)
    print(f"  Versión    : {BOLD}{VERSION}{RESET}")
    print(f"  Creadora   : Sara Kerrigan")
    print(f"  Sistema    : Windows 11 Pro (Build 26200)")
    print(f"  Python     : {sys.version.split()[0]}")
    print(f"  Fecha      : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")


# ══════════════════════════════════════════════════════════════════════════════
# PARSER PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        prog="kalmiya",
        description="KALMIYA — Asistente IA personal de Sara Kerrigan",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  kalmiya "¿cuál es el clima en Cúcuta?"
  kalmiya --rag "explica ADSO con mis notas"
  kalmiya --chat
  kalmiya --chat --rag
  kalmiya --indexar
  kalmiya --buscar "Python clases"
  kalmiya --skill traducir "hello" --a es
  kalmiya --sistema
  kalmiya --estado
        """
    )

    parser.add_argument("query",           nargs="?", help="Pregunta o consulta")
    parser.add_argument("--rag",           action="store_true", help="Usar RAG (busca en tus documentos)")
    parser.add_argument("--chat",          action="store_true", help="Modo chat interactivo")
    parser.add_argument("--indexar",       action="store_true", help="Indexar documentos para RAG")
    parser.add_argument("--buscar",        metavar="QUERY",     help="Buscar en documentos indexados")
    parser.add_argument("--skill",         metavar="NOMBRE",    help="Ejecutar una skill")
    parser.add_argument("--args",          nargs="*",           help="Argumentos para la skill")
    parser.add_argument("--sistema",       action="store_true", help="Info del sistema")
    parser.add_argument("--estado",        action="store_true", help="Estado de todos los módulos")
    parser.add_argument("--version","-v",  action="store_true", help="Versión del sistema")
    parser.add_argument("--engine",        default="",          help="Motor de IA: ollama, gemini, groq...")
    parser.add_argument("--top",           type=int, default=5, help="Número de resultados RAG")
    parser.add_argument("--carpeta",       metavar="RUTA",      help="Carpeta a indexar (default: vault)")
    parser.add_argument("--json",          action="store_true", help="Salida en formato JSON")

    args = parser.parse_args()

    # ── Ejecutar comando ───────────────────────────────────────────────────────
    if args.version:
        cmd_version()

    elif args.estado:
        cmd_estado()

    elif args.sistema:
        cmd_sistema()

    elif args.indexar:
        cmd_indexar(carpeta=args.carpeta)

    elif args.buscar:
        cmd_buscar_rag(args.buscar, top_k=args.top)

    elif args.skill:
        skill_args = args.args or []
        if args.query:
            skill_args.insert(0, args.query)
        cmd_skill(args.skill, skill_args)

    elif args.chat:
        cmd_chat_interactivo(usar_rag=args.rag, engine=args.engine)

    elif args.query:
        if args.json:
            from brain import ask_kalmiya
            resp = ask_kalmiya(args.query, force_engine=args.engine)
            print(json.dumps({
                "query":    args.query,
                "respuesta": resp,
                "motor":    args.engine or "auto",
                "rag":      args.rag,
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False, indent=2))
        else:
            cmd_preguntar(args.query, usar_rag=args.rag, engine=args.engine)

    else:
        # Sin argumentos → modo chat interactivo por defecto
        cmd_chat_interactivo(usar_rag=False)


if __name__ == "__main__":
    main()
