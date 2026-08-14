"""
kalmiya_launcher.py — Lanzador principal de KALMIYA
=====================================================
Orquesta el arranque completo del sistema KALMIYA:
  1. Muestra la pantalla de splash
  2. Lanza el HUD flotante en hilo separado
  3. Actualiza el fondo de pantalla
  4. Inicia el núcleo de voz (kalmiya_core.py)
  5. Mantiene el proceso vivo con manejo limpio de señales

Uso:
    python kalmiya_launcher.py
"""

import os
import sys
import time
import signal
import threading
import subprocess
import ctypes
from pathlib import Path
from datetime import datetime
from typing import Optional
from decouple import config


def _ensure_admin():
    """
    Verifica si KALMIYA tiene permisos de administrador.
    Si no los tiene, se relanza automaticamente como administrador.
    """
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False

    if not is_admin:
        # Relanzar como administrador
        try:
            script = str(Path(__file__).resolve())
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas",
                sys.executable,
                f'"{script}"',
                str(Path(__file__).parent),
                1  # SW_SHOWNORMAL
            )
            sys.exit(0)  # Cerrar proceso sin permisos
        except Exception as e:
            print(f"[ADMIN] No se pudieron obtener permisos de administrador: {e}")
            print("[ADMIN] Continuando sin permisos elevados...")


# ── Directorio base ────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

# ── Colores ANSI para consola ──────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    CYAN    = "\033[96m"
    BLUE    = "\033[94m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    DIM     = "\033[2m"
    BOLD    = "\033[1m"

def _c(color: str, text: str) -> str:
    return f"{color}{text}{C.RESET}"


# ── Banner de consola ──────────────────────────────────────────────────────────
BANNER = f"""
{C.CYAN}
  ██╗  ██╗ █████╗ ██╗     ███╗   ███╗██╗██╗   ██╗ █████╗
  ██║ ██╔╝██╔══██╗██║     ████╗ ████║██║╚██╗ ██╔╝██╔══██╗
  █████╔╝ ███████║██║     ██╔████╔██║██║ ╚████╔╝ ███████║
  ██╔═██╗ ██╔══██║██║     ██║╚██╔╝██║██║  ╚██╔╝  ██╔══██║
  ██║  ██╗██║  ██║███████╗██║ ╚═╝ ██║██║   ██║   ██║  ██║
  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝
{C.RESET}
{C.DIM}  NEURAL INTELLIGENCE SYSTEM  ·  v3.5  ·  SARA KERRIGAN{C.RESET}
  {C.CYAN}{'─' * 56}{C.RESET}
"""


# ── Estado global del lanzador ─────────────────────────────────────────────────
_running = True
_processes: dict[str, subprocess.Popen] = {}
_threads: dict[str, threading.Thread] = {}


def _log(tag: str, msg: str, level: str = "info"):
    """Imprime un mensaje de log con formato."""
    now = datetime.now().strftime("%H:%M:%S")
    colors = {
        "info":    C.CYAN,
        "ok":      C.GREEN,
        "warn":    C.YELLOW,
        "error":   C.RED,
        "dim":     C.DIM,
    }
    color = colors.get(level, C.RESET)
    tag_str = f"[{tag}]".ljust(12)
    print(f"  {C.DIM}{now}{C.RESET}  {color}{tag_str}{C.RESET}  {msg}")


# ── Paso 1: Pantalla de splash ─────────────────────────────────────────────────

def _run_splash() -> bool:
    """
    Muestra la pantalla de splash y espera a que termine.
    Retorna True si completó correctamente.
    """
    splash_path = BASE_DIR / "splash_screen.py"
    if not splash_path.exists():
        _log("SPLASH", "splash_screen.py no encontrado, omitiendo.", "warn")
        return False

    _log("SPLASH", "Iniciando pantalla de arranque...", "info")
    try:
        # Ejecutar splash en proceso separado y esperar
        proc = subprocess.run(
            [sys.executable, str(splash_path)],
            timeout=30
        )
        _log("SPLASH", "Pantalla de arranque completada.", "ok")
        return True
    except subprocess.TimeoutExpired:
        _log("SPLASH", "Timeout en splash, continuando.", "warn")
        return True
    except Exception as e:
        _log("SPLASH", f"Error en splash: {e}", "error")
        return False


def _run_biometric_authentication() -> bool:
    """Inicia el flujo de verificación biométrica al arrancar el lanzador."""
    try:
        require_bio = config('KALMIYA_REQUIRE_BIOMETRIC', default='true', cast=str).lower() in ('1', 'true')
    except Exception:
        require_bio = True

    if not require_bio:
        _log("AUTH", "Autenticación biométrica desactivada por configuración.", "dim")
        return True

    try:
        from kalmiya_biometrics import verificacion_biometrica_completa, estado_biometrico
    except Exception as e:
        _log("AUTH", f"Módulo biométrico no disponible: {e}", "warn")
        _log("AUTH", "Continuando sin autenticación biométrica.", "warn")
        return True

    _log("AUTH", "Iniciando verificación biométrica de inicio.", "info")
    resultado = verificacion_biometrica_completa(usar_cara=True, usar_voz=True, usar_pin=True, modo_silencioso=False)
    if resultado:
        estado = estado_biometrico()
        _log("AUTH", f"Usuario autenticado: {resultado.get('nombre')} — Nivel {resultado.get('nivel_acceso')}", "ok")
        _log("AUTH", f"Estado biométrico: {estado}", "dim")
        return True

    _log("AUTH", "Autenticación biométrica fallida. Apagando lanzador por seguridad.", "error")
    return False


# ── Paso 2: HUD flotante ───────────────────────────────────────────────────────

def _launch_hud():
    """Lanza el HUD en un proceso separado."""
    hud_path = BASE_DIR / "kalmiya_hud.py"
    if not hud_path.exists():
        _log("HUD", "kalmiya_hud.py no encontrado.", "error")
        return

    _log("HUD", "Lanzando HUD flotante...", "info")
    try:
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        proc = subprocess.Popen(
            [sys.executable, str(hud_path)],
            creationflags=flags
        )
        _processes["hud"] = proc
        _log("HUD", f"HUD activo (PID: {proc.pid})", "ok")
    except Exception as e:
        _log("HUD", f"Error lanzando HUD: {e}", "error")


def _launch_hud_thread():
    """Lanza el HUD en un hilo separado."""
    t = threading.Thread(target=_launch_hud, daemon=True, name="hud-launcher")
    t.start()
    _threads["hud"] = t
    t.join(timeout=5)  # Esperar a que el proceso arranque


# ── Paso 3: Fondo de pantalla ──────────────────────────────────────────────────

def _start_dashboard_autoupdate():
    """Inicia la actualización automática del dashboard de Obsidian cada 1 min."""
    try:
        from kalmiya_dashboard import start_auto_update
        start_auto_update(interval_minutes=1)
        _log("DASHBOARD", "Auto-update iniciado (cada 1 min)", "ok")
    except Exception as e:
        _log("DASHBOARD", f"No disponible: {e}", "warn")


def _start_audio_system():
    """Inicializa el sistema de audio y aplica perfil automático por hora."""
    try:
        from kalmiya_audio import (cargar_estado_guardado, perfil_automatico_por_hora,
                                   sonido_kalmiya_arranque)
        cargar_estado_guardado()
        perfil = perfil_automatico_por_hora()
        _log("AUDIO", f"Sistema de audio listo — perfil: {perfil}", "ok")
        sonido_kalmiya_arranque()
    except Exception as e:
        _log("AUDIO", f"No disponible: {e}", "warn")


def _start_mcp_server():
    """Inicia el servidor MCP HTTP en background."""
    try:
        from kalmiya_mcp import iniciar_mcp_background
        iniciar_mcp_background(puerto=8765)
        _log("MCP", "Servidor iniciado en http://127.0.0.1:8765", "ok")
    except Exception as e:
        _log("MCP", f"No disponible: {e}", "warn")


def _start_rag_indexer():
    """Indexa los documentos del vault en background para RAG."""
    import threading

    def _indexar():
        try:
            from kalmiya_rag import indexar_vault, get_rag_stats, VAULT_PATH
            stats = get_rag_stats()
            # Solo indexar si hay cambios o es la primera vez
            if stats.get("chunks_en_db", 0) == 0:
                _log("RAG", "Indexando documentos por primera vez...", "info")
                resultado = indexar_vault(VAULT_PATH, mostrar_progreso=False)
                _log("RAG", f"Indexado: {resultado.get('chunks',0)} chunks de {resultado.get('archivos',0)} archivos", "ok")
            else:
                # Indexado incremental rápido (solo archivos nuevos/modificados)
                resultado = indexar_vault(VAULT_PATH, mostrar_progreso=False)
                if resultado.get("chunks", 0) > 0:
                    _log("RAG", f"RAG actualizado: +{resultado.get('chunks',0)} chunks", "ok")
                else:
                    _log("RAG", f"RAG al día — {stats.get('chunks_en_db',0)} chunks", "ok")
        except Exception as e:
            _log("RAG", f"No disponible: {e}", "warn")

    t = threading.Thread(target=_indexar, daemon=True, name="rag-indexer")
    t.start()

def _start_multitasking_engine():
    """Inicia el motor de multitarea para procesos en segundo plano y auto-crecimiento."""
    try:
        from multitasking_engine import engine
        _log("ENGINE", "Motor de multitarea y auto-crecimiento inicializado.", "ok")
        # Podemos iniciar un self-learning loop inicial
        engine.start_self_learning_loop()
    except Exception as e:
        _log("ENGINE", f"No disponible: {e}", "warn")

def _start_telegram_bot():
    """Inicia el bot de Telegram si está configurado."""
    try:
        from modules.telegram_bot import start_telegram_bot
        started = start_telegram_bot()
        if started:
            _log("TELEGRAM", "Bot de Telegram activo y escuchando en segundo plano.", "ok")
        else:
            _log("TELEGRAM", "Bot inactivo (Falta configurar el Token).", "dim")
    except ImportError as e:
        _log("TELEGRAM", f"No disponible (Falta instalar librerías): {e}", "warn")
    except Exception as e:
        _log("TELEGRAM", f"Error al iniciar el bot: {e}", "error")

def _update_wallpaper_thread():
    """Actualiza el fondo de pantalla en un hilo separado de forma periódica (tiempo real)."""
    def _worker():
        first_run = True
        while _running:
            try:
                from wallpaper_engine import update_wallpaper
                if first_run:
                    _log("WALLPAPER", "Generando fondo de pantalla inicial...", "info")
                    success = update_wallpaper()
                    if success:
                        _log("WALLPAPER", "Fondo de pantalla aplicado correctamente.", "ok")
                    else:
                        _log("WALLPAPER", "No se pudo aplicar el fondo inicial.", "warn")
                    first_run = False
                else:
                    # Actualizaciones silenciosas en segundo plano
                    update_wallpaper()
            except Exception as e:
                _log("WALLPAPER", f"Error en ciclo de actualización: {e}", "error")
            
            # Esperar 60 segundos antes de la siguiente actualización de tiempo real
            for _ in range(60):
                if not _running:
                    break
                time.sleep(1)

    t = threading.Thread(target=_worker, daemon=True, name="wallpaper")
    t.start()
    _threads["wallpaper"] = t


# ── Paso 3.5: Asegurar Ollama ──────────────────────────────────────────────────

def _ensure_ollama():
    """Verifica si Ollama esta corriendo y lo lanza si no."""
    _log("OLLAMA", "Verificando servicio local...", "info")
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        if r.status_code == 200:
            _log("OLLAMA", "Servicio activo y respondiendo.", "ok")
            return
    except Exception:
        pass

    _log("OLLAMA", "Servicio no detectado. Intentando iniciar...", "warn")
    try:
        # Intentar lanzar ollama serve en segundo plano
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        proc = subprocess.Popen(
            ["ollama", "serve"],
            creationflags=flags,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        _processes["ollama"] = proc
        _log("OLLAMA", "Comando 'ollama serve' enviado.", "ok")
        time.sleep(2) # Esperar a que inicialice
    except Exception as e:
        _log("OLLAMA", f"No se pudo iniciar Ollama: {e}", "error")
        _log("OLLAMA", "Asegurate de tener Ollama instalado: https://ollama.com", "dim")


# ── Paso 4: Núcleo de voz ──────────────────────────────────────────────────────

def _launch_core():
    """Lanza kalmiya_core.py en un proceso separado."""
    core_path = BASE_DIR / "kalmiya_core.py"
    if not core_path.exists():
        _log("CORE", "kalmiya_core.py no encontrado.", "error")
        return

    _log("CORE", "Iniciando núcleo de voz...", "info")
    try:
        # El core arranca oculto para no mostrar la terminal de Python
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        proc = subprocess.Popen(
            [sys.executable, str(core_path)],
            creationflags=flags
        )
        _processes["core"] = proc
        _log("CORE", f"Núcleo de voz activo (PID: {proc.pid})", "ok")
    except Exception as e:
        _log("CORE", f"Error lanzando núcleo: {e}", "error")


def _launch_core_thread():
    """Lanza el núcleo en un hilo separado."""
    t = threading.Thread(target=_launch_core, daemon=True, name="core-launcher")
    t.start()
    _threads["core"] = t
    t.join(timeout=5)


# ── Paso 5: Icono de bandeja del sistema ──────────────────────────────────────

def _create_tray_icon():
    """
    Crea un icono de bandeja del sistema usando tkinter.
    Muestra el estado de KALMIYA y permite salir.
    """
    import tkinter as tk

    def _show_status():
        """Muestra una ventana de estado."""
        status_win = tk.Toplevel()
        status_win.title("KALMIYA — Estado")
        status_win.geometry("400x300")
        status_win.configure(bg="#0a0a1a")
        status_win.attributes("-topmost", True)

        tk.Label(
            status_win,
            text="⬡ KALMIYA NEURAL CORE",
            font=("Consolas", 14, "bold"),
            fg="#00f2ff", bg="#0a0a1a"
        ).pack(pady=(20, 10))

        # Estado de procesos
        for name, proc in _processes.items():
            alive = proc.poll() is None
            status = "ACTIVO ●" if alive else "DETENIDO ●"
            color = "#00ff88" if alive else "#ff4444"
            tk.Label(
                status_win,
                text=f"  {name.upper()}: {status}",
                font=("Consolas", 10),
                fg=color, bg="#0a0a1a",
                anchor="w"
            ).pack(fill="x", padx=20)

        tk.Button(
            status_win,
            text="Cerrar",
            font=("Consolas", 10),
            fg="#00f2ff", bg="#001a2e",
            relief="flat",
            command=status_win.destroy
        ).pack(pady=20)

    def _quit_all():
        """Cierra todos los procesos y sale."""
        _log("LAUNCHER", "Apagando todos los sistemas...", "warn")
        _shutdown()
        root.destroy()

    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal

    # Menú contextual del icono de bandeja
    menu = tk.Menu(root, tearoff=0, bg="#0a0a1a", fg="#00f2ff",
                   activebackground="#001a2e", activeforeground="#00f2ff",
                   font=("Consolas", 10))
    menu.add_command(label="⬡ KALMIYA — Estado", command=_show_status)
    menu.add_separator()
    menu.add_command(label="Apagar KALMIYA", command=_quit_all)

    def _show_menu(event=None):
        try:
            menu.tk_popup(root.winfo_pointerx(), root.winfo_pointery())
        finally:
            menu.grab_release()

    # Crear ventana mínima en la barra de tareas
    root.title("KALMIYA")
    root.geometry("1x1+0+0")
    root.overrideredirect(False)
    root.attributes("-alpha", 0.01)  # Casi invisible

    _log("TRAY", "Icono de bandeja activo. Clic derecho para opciones.", "ok")

    try:
        root.mainloop()
    except Exception:
        pass


# ── Manejo de señales y apagado ────────────────────────────────────────────────

def _shutdown():
    """Apaga todos los procesos de KALMIYA."""
    global _running
    _running = False

    _log("LAUNCHER", "Iniciando apagado limpio...", "warn")

    for name, proc in _processes.items():
        try:
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=5)
                _log("LAUNCHER", f"{name} detenido.", "dim")
        except Exception as e:
            _log("LAUNCHER", f"Error deteniendo {name}: {e}", "error")
            try:
                proc.kill()
            except Exception:
                pass

    _log("LAUNCHER", "Todos los sistemas apagados. Hasta pronto, Sara.", "ok")


def _signal_handler(sig, frame):
    """Maneja Ctrl+C y señales de terminación."""
    print()
    _log("LAUNCHER", "Señal de interrupción recibida.", "warn")
    _shutdown()
    sys.exit(0)


# ── Monitor de procesos ────────────────────────────────────────────────────────

def _monitor_processes():
    """Monitorea los procesos y los reinicia si se caen (opcional)."""
    while _running:
        time.sleep(30)
        for name, proc in list(_processes.items()):
            if proc.poll() is not None:
                _log("MONITOR", f"{name} se detuvo (código: {proc.returncode})", "warn")
                del _processes[name]


# ── Función principal ──────────────────────────────────────────────────────────

def main():
    """Punto de entrada principal del lanzador."""
    # Habilitar colores ANSI en Windows y forzar UTF-8
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        os.system("color")
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7
            )
        except Exception:
            pass

    # Solicitar permisos de administrador al inicio
    _ensure_admin()

    # Registrar manejadores de señales
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    # Imprimir banner
    print(BANNER)
    _log("LAUNCHER", f"Iniciando KALMIYA — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", "info")
    _log("LAUNCHER", f"Directorio base: {BASE_DIR}", "dim")
    print()

    # ── Secuencia de arranque ──────────────────────────────────────────────────

    # 1. Splash screen (bloqueante)
    _log("PASO 1/4", "Pantalla de arranque", "info")
    _run_splash()
    print()

    # 1.5 Autenticación biométrica de inicio
    _log("PASO 1.5/4", "Autenticación biométrica", "info")
    if not _run_biometric_authentication():
        _log("LAUNCHER", "No se pudo autenticar. Finalizando el proceso.", "error")
        return
    print()

    # 2. HUD flotante (no bloqueante)
    _log("PASO 2/4", "HUD flotante", "info")
    _launch_hud_thread()
    time.sleep(1)
    print()

    # Paso 2.6: Dashboard auto-update
    _start_dashboard_autoupdate()

    # Paso 2.7: Sistema de audio
    _start_audio_system()

    # Paso 2.75: Bienvenida y Rutina Diaria por voz al encender el PC
    _log("SALUDO", "Preparando bienvenida y rutina diaria...", "info")
    try:
        from bienvenida import greet_user, daily_routine
        greet_user()
        daily_routine()
        _log("SALUDO", "Bienvenida y rutina diaria completadas.", "ok")
    except Exception as e:
        _log("SALUDO", f"No se pudo completar el saludo o rutina: {e}", "warn")
    print()

    # Paso 2.8: Servidor MCP en background
    _start_mcp_server()

    # Paso 2.9: Indexado RAG inicial
    _start_rag_indexer()

    # Paso 2.10: Motor de multitarea (Crecimiento e independencia)
    _start_multitasking_engine()

    # Paso 2.11: Bot de Telegram Privado
    _start_telegram_bot()

    # 3. Fondo de pantalla (no bloqueante)
    if config('KALMIYA_ENABLE_WALLPAPER', default='true', cast=str).lower() in ('1', 'true'):
        _log("PASO 3/4", "Motor de fondo de pantalla", "info")
        _update_wallpaper_thread()
    else:
        _log("PASO 3/4", "Motor de fondo de pantalla desactivado por configuración", "info")
    print()

    # 3.5 Asegurar Ollama (bloqueante ligero)
    _ensure_ollama()
    print()

    # 4. Núcleo de voz (no bloqueante)
    _log("PASO 4/4", "Núcleo de voz autonomo", "info")
    _launch_core_thread()
    print()

    # ── Servidor HTTP opcional ──────────────────────────────────────────────────────
    # (Servidor web eliminado a favor de una arquitectura pura de escritorio)

    # ── Sistema activo ─────────────────────────────────────────────────────────
    _log("LAUNCHER", "=" * 50, "dim")
    _log("LAUNCHER", _c(C.GREEN + C.BOLD, "KALMIYA COMPLETAMENTE OPERATIVA"), "ok")
    _log("LAUNCHER", "Presiona Ctrl+C para apagar todos los sistemas.", "dim")
    _log("LAUNCHER", "=" * 50, "dim")
    print()

    # Iniciar monitor en hilo separado
    monitor_t = threading.Thread(target=_monitor_processes, daemon=True, name="monitor")
    monitor_t.start()

    # Lanzar icono de bandeja (bloqueante — mantiene el proceso vivo)
    try:
        _create_tray_icon()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        _log("TRAY", f"Error en bandeja: {e}", "error")
        # Si la bandeja falla, mantener el proceso vivo de otra forma
        _log("LAUNCHER", "Modo sin bandeja. Presiona Ctrl+C para salir.", "warn")
        try:
            while _running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    _shutdown()


# ── Ejecución standalone ───────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
