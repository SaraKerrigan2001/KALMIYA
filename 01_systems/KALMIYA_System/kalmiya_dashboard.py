"""
kalmiya_dashboard.py — Dashboard automático en Obsidian
=========================================================
Genera y actualiza KALMIYA_DASHBOARD.md en el vault con:
  - Estado del sistema en tiempo real
  - Motores de IA activos
  - Últimas conversaciones
  - Memoria de Sara
  - Tareas pendientes
  - Actividad reciente
"""

import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _logging import get_logger
from obsidian_bridge import get_vault

logger = get_logger(__name__)

DASHBOARD_FILE = "KALMIYA_DASHBOARD.md"


def _get_system_stats() -> dict:
    """Recopila estadísticas del sistema."""
    stats = {}
    try:
        import psutil
        cpu   = psutil.cpu_percent(interval=0.5)
        mem   = psutil.virtual_memory()
        disk  = psutil.disk_usage("C:\\")
        stats = {
            "cpu_pct":  cpu,
            "ram_used": round(mem.used  / (1024**3), 1),
            "ram_total":round(mem.total / (1024**3), 1),
            "ram_pct":  mem.percent,
            "disk_free":round(disk.free / (1024**3), 1),
            "disk_pct": disk.percent,
        }
    except Exception:
        pass
    return stats


def _get_brain_status() -> dict:
    """Obtiene el estado de los motores de IA."""
    try:
        from brain import get_engine_status
        return get_engine_status()
    except Exception:
        return {}


def _get_db_stats() -> dict:
    """Obtiene estadísticas de la BD."""
    try:
        from database import get_db_stats
        return get_db_stats()
    except Exception:
        return {}


def _get_recent_history(limit: int = 5) -> list:
    """Obtiene las últimas conversaciones."""
    try:
        from database import get_recent_history
        return get_recent_history(limit)
    except Exception:
        return []


def _get_memory_summary() -> dict:
    """Obtiene la memoria de Sara."""
    try:
        from database import get_memory
        keys = ["nombre_real", "ubicacion", "trabajo", "cumpleanos",
                "color_favorito", "gustos", "ai_mode_override"]
        return {k: get_memory(k) or "" for k in keys}
    except Exception:
        return {}


def _get_pending_tasks() -> list:
    """Obtiene tareas pendientes del módulo TODO."""
    try:
        from modules.todo_manager import TODOManager
        manager = TODOManager()
        return manager.get_daily_summary()
    except Exception:
        return []


def _bar(pct: float, width: int = 20) -> str:
    """Genera una barra de progreso ASCII."""
    filled = int(pct / 100 * width)
    return f"{'█' * filled}{'░' * (width - filled)} {pct:.0f}%"


def generate_dashboard() -> str:
    """
    Genera el contenido completo del dashboard en Markdown.
    """
    now    = datetime.now()
    sys_s  = _get_system_stats()
    brain  = _get_brain_status()
    db_s   = _get_db_stats()
    mem    = _get_memory_summary()
    hist   = _get_recent_history(5)
    tasks  = _get_pending_tasks()

    # ── Encabezado ─────────────────────────────────────────────────────────────
    lines = [
        "---",
        'title: "KALMIYA Dashboard"',
        'tags: [kalmiya, dashboard, sistema]',
        f'updated: "{now.strftime("%Y-%m-%d %H:%M:%S")}"',
        "---",
        "",
        "# 🤖 KALMIYA — Dashboard",
        f"> Última actualización: **{now.strftime('%A %d de %B de %Y — %H:%M:%S')}**",
        "",
        "**Navegación del vault:**",
        "[[INDEX]] | [[WELCOME]] | [[MODULOS_IMPLEMENTADOS]] | [[KALMIYA_FUNCIONES]] | [[CHAT_GUIA]] | [[OBSIDIAN_SETUP]] | [[FUNCIONES_IMPLEMENTACION]]",
        "",
        "---",
        "",
    ]

    # ── Estado del sistema ─────────────────────────────────────────────────────
    lines += [
        "## 🖥️ Estado del Sistema",
        "",
        "| Componente | Estado | Uso |",
        "|---|---|---|",
    ]
    if sys_s:
        lines += [
            f"| CPU | {'🟢 Normal' if sys_s.get('cpu_pct',0) < 80 else '🔴 Alto'} | {_bar(sys_s.get('cpu_pct',0), 15)} |",
            f"| RAM | {sys_s.get('ram_used',0)} / {sys_s.get('ram_total',0)} GB | {_bar(sys_s.get('ram_pct',0), 15)} |",
            f"| Disco C | {sys_s.get('disk_free',0)} GB libre | {_bar(sys_s.get('disk_pct',0), 15)} |",
        ]
    else:
        lines.append("| Sistema | ⚠️ No disponible | — |")
    lines.append("")

    # ── Motores de IA ──────────────────────────────────────────────────────────
    lines += ["## 🧠 Motores de IA", ""]
    motor_map = [
        ("Ollama (local)",  brain.get("ollama_activo",    False), brain.get("ollama_modelos", [])),
        ("Gemini",          brain.get("gemini_activo",    False), []),
        ("Claude",          brain.get("claude_activo",    False), []),
        ("Groq",            brain.get("groq_activo",      False), []),
        ("OpenRouter",      brain.get("openrouter_activo",False), []),
        ("Cohere",          brain.get("cohere_activo",    False), []),
    ]
    for nombre, activo, modelos in motor_map:
        icono = "✅" if activo else "⚠️"
        det   = f" `{', '.join(modelos)}`" if modelos else ""
        lines.append(f"- {icono} **{nombre}**{det}")

    modo = brain.get("modo_actual", "auto")
    motor_usado = brain.get("motor_usado", "ninguno")
    lines += ["", f"**Modo:** `{modo}` | **Último motor:** `{motor_usado}`", ""]

    # ── Base de datos ──────────────────────────────────────────────────────────
    lines += ["## 🗄️ Base de Datos", ""]
    if db_s:
        lines += [
            f"- 💬 Historial de comandos: **{db_s.get('command_history', 0)}** entradas",
            f"- 🧠 Pensamientos autónomos: **{db_s.get('neural_thoughts', 0)}** guardados",
            f"- 🔑 Memoria de Sara: **{db_s.get('user_memory', 0)}** claves",
            f"- 📋 Auditoría de memoria: **{db_s.get('memory_audit', 0)}** cambios",
            f"- 💾 Tamaño: **{db_s.get('size_kb', 0)} KB**",
            f"- ⚡ Triggers activos: {len(db_s.get('triggers', []))}",
        ]
    lines.append("")

    # ── Perfil de Sara ─────────────────────────────────────────────────────────
    lines += ["## 👤 Perfil de Sara Kerrigan", ""]
    if mem:
        campo_map = {
            "nombre_real":  "Nombre",
            "ubicacion":    "Ciudad",
            "trabajo":      "Ocupación",
            "cumpleanos":   "Cumpleaños",
            "color_favorito":"Color favorito",
            "gustos":       "Hobbies",
        }
        for k, label in campo_map.items():
            val = mem.get(k, "")
            if val:
                lines.append(f"- **{label}:** {val}")
    lines.append("")

    # ── Tareas pendientes ──────────────────────────────────────────────────────
    lines += ["## ✅ Tareas Pendientes", ""]
    if tasks:
        for task in tasks[:10]:
            prio  = task.get("priority", "normal")
            icono = "🔴" if prio == "high" else "🟡" if prio == "medium" else "🟢"
            desc  = task.get("description", task.get("title", str(task)))
            lines.append(f"- {icono} {desc}")
    else:
        lines.append("*No hay tareas pendientes.*")
    lines.append("")

    # ── Últimas conversaciones ─────────────────────────────────────────────────
    lines += ["## 💬 Últimas Conversaciones", ""]
    if hist:
        for ts, cmd, resp in hist:
            cmd_short  = cmd[:80].replace("\n"," ")  + ("…" if len(cmd)  > 80 else "")
            resp_short = (resp or "")[:80].replace("\n"," ") + ("…" if resp and len(resp) > 80 else "")
            lines += [
                f"**{ts}**",
                f"> 👤 {cmd_short}",
                f"> 🤖 {resp_short}",
                "",
            ]
    else:
        lines.append("*Sin conversaciones recientes.*")

    # ── Notas KALMIYA recientes ────────────────────────────────────────────────
    lines += ["## 📝 Notas Recientes", ""]
    try:
        from obsidian_bridge import list_notes, search_notes
        notas = list_notes("KALMIYA_Notes")
        if notas:
            for n in notas[-5:]:
                lines.append(f"- [[KALMIYA_Notes/{n}|{n}]]")
        else:
            lines.append("*Sin notas todavía. Dile a KALMIYA: 'crea una nota sobre...'*")
    except Exception:
        lines.append("*No se pudo leer la carpeta de notas.*")
    lines.append("")

    # ── Accesos rápidos ────────────────────────────────────────────────────────
    lines += [
        "## ⚡ Accesos Rápidos",
        "",
        "| Acción | Comando en chat |",
        "|---|---|",
        "| Crear nota | `crea una nota sobre [tema]` |",
        "| Buscar notas | `busca en mis notas [término]` |",
        "| Leer nota | `lee la nota [nombre]` |",
        "| Guardar chat | `guarda esta conversación` |",
        "| Listar notas | `lista mis notas` |",
        "| Info sistema | opción `103` en el menú |",
        "| Estado IA | opción `AIS` en el menú |",
        "| Toolbox | opción `TB` en el menú |",
        "",
        "---",
        "",
        "## 🔗 Links del Vault",
        "",
        "| Documento | Descripción |",
        "|---|---|",
        "| [[INDEX]] | Índice principal del proyecto |",
        "| [[WELCOME]] | Bienvenida y guía inicial |",
        "| [[MODULOS_IMPLEMENTADOS]] | Todos los módulos del sistema |",
        "| [[KALMIYA_FUNCIONES]] | Funciones disponibles de KALMIYA |",
        "| [[CHAT_GUIA]] | Guía de comandos del chat |",
        "| [[OBSIDIAN_SETUP]] | Configuración de Obsidian |",
        "| [[FUNCIONES_IMPLEMENTACION]] | Estado de implementación |",
        "| [[OPEN_VAULT]] | Cómo abrir el vault |",
        "",
        "---",
        "",
        "## 📂 Notas del Sistema",
        "",
        "| Nota | Ubicación |",
        "|---|---|",
        "| [[01_systems/KALMIYA_System/README\\|README KALMIYA System]] | Sistema principal |",
        "| [[01_systems/KALMIYA_System/kalmiya_docs\\|Documentación KALMIYA]] | Docs técnicos |",
        "| [[01_systems/KALMIYA_System/standards\\|Estándares de código]] | Guías de desarrollo |",
        "| [[01_systems/KALMIYA/README\\|README KALMIYA]] | Perfil de KALMIYA |",
        "| [[01_systems/KALMIYA/Bienvenido\\|Bienvenido KALMIYA]] | Nota de inicio |",
        "| [[01_systems/KALMIYA/cree un enlace\\|Crear enlace]] | Guía de enlaces |",
        "| [[01_systems/LLM_Wiki/README\\|README LLM Wiki]] | Wiki de modelos LLM |",
        "| [[01_systems/LLM_Wiki/schema/SCHEMA\\|Esquema LLM]] | Esquema de modelos |",
        "| [[01_systems/LLM_Wiki/wiki/index\\|Índice Wiki LLM]] | Índice de la wiki |",
        "| [[01_systems/LLM_Wiki/wiki/log\\|Log LLM]] | Registro de cambios |",
        "| [[01_systems/LLM_Wiki/KALMIYA/Bienvenido\\|Bienvenido LLM Wiki]] | Intro LLM Wiki |",
        "| [[FUNCIONES_IMPLEMENTACION]] | Estado de implementación |",
        "",
        "---",
        f"*Dashboard generado automáticamente por KALMIYA — {now.strftime('%Y-%m-%d %H:%M')}*",
    ]

    return "\n".join(lines)


def update_dashboard() -> bool:
    """
    Escribe o actualiza KALMIYA_DASHBOARD.md en el vault.

    Returns:
        True si se actualizó correctamente.
    """
    try:
        vault     = get_vault()
        dash_path = vault / DASHBOARD_FILE
        content   = generate_dashboard()
        dash_path.write_text(content, encoding="utf-8")
        logger.info(f"[DASHBOARD] Actualizado: {dash_path}")
        return True
    except Exception as e:
        logger.error(f"[DASHBOARD] Error actualizando: {e}")
        return False


def start_auto_update(interval_minutes: int = 5) -> None:
    """
    Inicia la actualización automática del dashboard en un hilo.

    Args:
        interval_minutes: Cada cuántos minutos actualizar (default: 5).
    """
    import threading

    def _loop():
        import time
        while True:
            try:
                update_dashboard()
            except Exception as e:
                logger.warning(f"[DASHBOARD] Error en auto-update: {e}")
            time.sleep(interval_minutes * 60)

    t = threading.Thread(target=_loop, daemon=True, name="dashboard-updater")
    t.start()
    logger.info(f"[DASHBOARD] Auto-actualización iniciada cada {interval_minutes} minutos")


if __name__ == "__main__":
    print("Actualizando dashboard...")
    if update_dashboard():
        print(f"✅ KALMIYA_DASHBOARD.md actualizado en el vault")
    else:
        print("❌ Error al actualizar el dashboard")
