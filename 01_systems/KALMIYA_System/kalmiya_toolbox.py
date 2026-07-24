"""
kalmiya_toolbox.py — Panel de Herramientas KALMIYA v1.0
========================================================
Ventana flotante con accesos rápidos a todas las funciones:
  - Estado del sistema en tiempo real
  - Botones de herramientas organizados por categoría
  - Acceso directo a Obsidian y notas
  - Control de motores de IA
  - Búsqueda rápida en notas
"""

import sys
import os
import threading
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import customtkinter as ctk
    import tkinter as tk
    from tkinter import messagebox, simpledialog
    CTK_OK = True
except ImportError:
    CTK_OK = False

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False

# ── Colores ────────────────────────────────────────────────────────────────────
BG_MAIN   = "#050510"
BG_CARD   = "#0a0a1a"
BG_BTN    = "#020a15"
ACCENT    = "#00f2ff"
ACCENT2   = "#7b00ff"
TEXT_W    = "#ffffff"
TEXT_DIM  = "#888888"
SUCCESS   = "#00ff88"
WARNING   = "#ffaa00"
DANGER    = "#ff4444"
PURPLE    = "#b044ff"

BOX_W = 480
BOX_H = 680


class KalmiyaToolbox:
    """Panel flotante de herramientas de KALMIYA."""

    def __init__(self):
        if not CTK_OK:
            raise ImportError("customtkinter no está instalado.")
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.title("🧰 KALMIYA Toolbox")
        self.root.geometry(f"{BOX_W}x{BOX_H}+50+50")
        self.root.configure(fg_color=BG_MAIN)
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self._build_ui()
        self._start_monitor()

    # ── UI ─────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self.root, fg_color=BG_CARD, corner_radius=10, height=60)
        header.pack(fill="x", padx=10, pady=(10,5))
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="🧰  KALMIYA TOOLBOX",
                     font=("Courier New", 16, "bold"), text_color=ACCENT).pack(side="left", padx=15)
        self.lbl_time = ctk.CTkLabel(header, text="", font=("Courier New", 11), text_color=TEXT_DIM)
        self.lbl_time.pack(side="right", padx=15)

        # Stats strip
        stats = ctk.CTkFrame(self.root, fg_color=BG_CARD, corner_radius=8, height=36)
        stats.pack(fill="x", padx=10, pady=2)
        stats.pack_propagate(False)
        self.lbl_cpu  = ctk.CTkLabel(stats, text="CPU: --",  font=("Courier New",10), text_color=SUCCESS)
        self.lbl_ram  = ctk.CTkLabel(stats, text="RAM: --",  font=("Courier New",10), text_color=ACCENT)
        self.lbl_disk = ctk.CTkLabel(stats, text="DISK: --", font=("Courier New",10), text_color=WARNING)
        self.lbl_motor = ctk.CTkLabel(stats, text="IA: --",  font=("Courier New",10), text_color=PURPLE)
        for w in (self.lbl_cpu, self.lbl_ram, self.lbl_disk, self.lbl_motor):
            w.pack(side="left", padx=10)

        # Tabs
        self.tabs = ctk.CTkTabview(self.root, fg_color=BG_CARD, segmented_button_fg_color=BG_BTN,
                                    segmented_button_selected_color=ACCENT,
                                    segmented_button_selected_hover_color="#00c0cc",
                                    text_color=TEXT_W, height=520)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabs.add("🔧 Sistema")
        self.tabs.add("📝 Notas")
        self.tabs.add("🧠 IA")
        self.tabs.add("🛡️ Seguridad")

        self._build_tab_sistema(self.tabs.tab("🔧 Sistema"))
        self._build_tab_notas(self.tabs.tab("📝 Notas"))
        self._build_tab_ia(self.tabs.tab("🧠 IA"))
        self._build_tab_seguridad(self.tabs.tab("🛡️ Seguridad"))

        # Status bar
        self.lbl_status = ctk.CTkLabel(self.root, text="Listo.", font=("Courier New",10), text_color=TEXT_DIM)
        self.lbl_status.pack(pady=(0,8))


    # ── Tab Sistema ────────────────────────────────────────────────────────────
    def _build_tab_sistema(self, tab):
        btns = [
            ("🖥️  Info completa del sistema",  SUCCESS,  self._btn_sysinfo),
            ("🎤  Estado del micrófono",        ACCENT,   self._btn_mic_status),
            ("🔧  Restaurar micrófono",         WARNING,  self._btn_mic_restore),
            ("💾  Backup rápido de BD",         ACCENT2,  self._btn_backup),
            ("📊  Dashboard Obsidian",          PURPLE,   self._btn_dashboard),
            ("🗂️  Abrir Obsidian",              ACCENT,   self._btn_obsidian),
            ("💬  Abrir Chat KALMIYA",          SUCCESS,  self._btn_chat),
        ]
        for txt, color, cmd in btns:
            ctk.CTkButton(tab, text=txt, fg_color=BG_BTN, hover_color=color,
                          text_color=TEXT_W, font=("Courier New", 12),
                          height=38, corner_radius=8, command=cmd).pack(
                          fill="x", padx=12, pady=4)

    # ── Tab Notas ──────────────────────────────────────────────────────────────
    def _build_tab_notas(self, tab):
        # Búsqueda
        search_frame = ctk.CTkFrame(tab, fg_color=BG_BTN, corner_radius=8)
        search_frame.pack(fill="x", padx=12, pady=(10,4))
        self.entry_search = ctk.CTkEntry(search_frame, placeholder_text="Buscar en notas...",
                                          fg_color=BG_MAIN, text_color=TEXT_W,
                                          border_color=ACCENT, font=("Courier New",11))
        self.entry_search.pack(side="left", fill="x", expand=True, padx=8, pady=6)
        ctk.CTkButton(search_frame, text="🔍", width=40, fg_color=ACCENT,
                       hover_color="#00c0cc", text_color=BG_MAIN,
                       command=self._btn_search).pack(side="right", padx=4, pady=4)

        # Crear nota rápida
        ctk.CTkLabel(tab, text="Crear nota rápida:", font=("Courier New",11),
                     text_color=TEXT_DIM).pack(anchor="w", padx=14, pady=(8,2))
        self.entry_note_title = ctk.CTkEntry(tab, placeholder_text="Título de la nota...",
                                              fg_color=BG_BTN, text_color=TEXT_W,
                                              border_color=ACCENT2, font=("Courier New",11))
        self.entry_note_title.pack(fill="x", padx=12, pady=2)
        self.txt_note = ctk.CTkTextbox(tab, height=120, fg_color=BG_BTN,
                                        text_color=TEXT_W, font=("Courier New",11))
        self.txt_note.pack(fill="x", padx=12, pady=2)

        nota_btns = ctk.CTkFrame(tab, fg_color="transparent")
        nota_btns.pack(fill="x", padx=12, pady=4)
        ctk.CTkButton(nota_btns, text="💾 Guardar nota", fg_color=ACCENT2,
                       hover_color=PURPLE, text_color=TEXT_W, font=("Courier New",11),
                       command=self._btn_save_note).pack(side="left", padx=4)
        ctk.CTkButton(nota_btns, text="📋 Listar notas", fg_color=BG_BTN,
                       hover_color=ACCENT, text_color=TEXT_W, font=("Courier New",11),
                       command=self._btn_list_notes).pack(side="left", padx=4)
        ctk.CTkButton(nota_btns, text="💬 Guardar chat", fg_color=BG_BTN,
                       hover_color=SUCCESS, text_color=TEXT_W, font=("Courier New",11),
                       command=self._btn_save_chat).pack(side="left", padx=4)

        # Resultado
        self.txt_notes_result = ctk.CTkTextbox(tab, height=100, fg_color=BG_BTN,
                                                text_color=ACCENT, font=("Courier New",10),
                                                state="disabled")
        self.txt_notes_result.pack(fill="x", padx=12, pady=4)


    # ── Tab IA ─────────────────────────────────────────────────────────────────
    def _build_tab_ia(self, tab):
        ctk.CTkLabel(tab, text="Motor activo:", font=("Courier New",11),
                     text_color=TEXT_DIM).pack(anchor="w", padx=14, pady=(10,2))
        self.lbl_ia_status = ctk.CTkLabel(tab, text="Cargando...",
                                           font=("Courier New",12,"bold"), text_color=PURPLE)
        self.lbl_ia_status.pack(anchor="w", padx=14, pady=(0,8))

        modos = [("🤖 Auto (cascada)",  "auto",       SUCCESS),
                 ("🦙 Ollama local",    "ollama",     ACCENT),
                 ("✨ Gemini",          "gemini",     WARNING),
                 ("⚡ Groq (gratis)",   "groq",       PURPLE),
                 ("🌐 OpenRouter",      "openrouter", ACCENT2),
                 ("🔷 Cohere",          "cohere",     "#00aaff"),
                 ("🧬 Claude",          "claude",     DANGER)]
        for label, modo, color in modos:
            ctk.CTkButton(tab, text=label, fg_color=BG_BTN, hover_color=color,
                          text_color=TEXT_W, font=("Courier New",11), height=34,
                          command=lambda m=modo: self._set_mode(m)).pack(
                          fill="x", padx=12, pady=2)

        ctk.CTkButton(tab, text="📊 Ver estado completo de motores",
                       fg_color=BG_BTN, hover_color=ACCENT, text_color=TEXT_W,
                       font=("Courier New",11), height=34,
                       command=self._btn_engine_status).pack(fill="x", padx=12, pady=(8,2))

    # ── Tab Seguridad ──────────────────────────────────────────────────────────
    def _build_tab_seguridad(self, tab):
        btns = [
            ("🔍  Escanear red local",          ACCENT,   self._btn_scan_net),
            ("🛡️  Activar escudo cibernético",  SUCCESS,  self._btn_shield),
            ("🔐  Analizar contraseña",          ACCENT2,  self._btn_password),
            ("📡  Ver dispositivos en red",      WARNING,  self._btn_devices),
            ("🏥  Chequeo de salud del sistema", SUCCESS,  self._btn_health),
        ]
        for txt, color, cmd in btns:
            ctk.CTkButton(tab, text=txt, fg_color=BG_BTN, hover_color=color,
                          text_color=TEXT_W, font=("Courier New",12),
                          height=38, corner_radius=8, command=cmd).pack(
                          fill="x", padx=12, pady=4)

        self.txt_sec_result = ctk.CTkTextbox(tab, height=180, fg_color=BG_BTN,
                                              text_color=SUCCESS, font=("Courier New",10),
                                              state="disabled")
        self.txt_sec_result.pack(fill="x", padx=12, pady=8)


    # ── Monitor de sistema (hilo) ──────────────────────────────────────────────
    def _start_monitor(self):
        threading.Thread(target=self._monitor_loop, daemon=True).start()

    def _monitor_loop(self):
        while True:
            try:
                now = datetime.now().strftime("%H:%M:%S")
                self.root.after(0, self.lbl_time.configure, {"text": now})
                if PSUTIL_OK:
                    cpu  = psutil.cpu_percent(interval=0.5)
                    mem  = psutil.virtual_memory().percent
                    disk = psutil.disk_usage("C:\\").percent
                    cpu_col  = SUCCESS if cpu  < 70 else DANGER
                    ram_col  = SUCCESS if mem  < 70 else DANGER
                    disk_col = SUCCESS if disk < 80 else DANGER
                    self.root.after(0, self.lbl_cpu.configure,  {"text": f"CPU: {cpu:.0f}%",  "text_color": cpu_col})
                    self.root.after(0, self.lbl_ram.configure,  {"text": f"RAM: {mem:.0f}%",  "text_color": ram_col})
                    self.root.after(0, self.lbl_disk.configure, {"text": f"DISK: {disk:.0f}%","text_color": disk_col})
                try:
                    from brain import get_engine_status
                    est = get_engine_status()
                    motor = est.get("motor_usado","--")
                    self.root.after(0, self.lbl_motor.configure, {"text": f"IA: {motor[:18]}"})
                    self.root.after(0, self.lbl_ia_status.configure, {"text": f"{motor} | modo: {est.get('modo_actual','auto')}"})
                except Exception:
                    pass
            except Exception:
                pass
            time.sleep(3)

    def _set_status(self, msg: str):
        self.root.after(0, self.lbl_status.configure, {"text": msg})

    def _show_notes_result(self, text: str):
        self.txt_notes_result.configure(state="normal")
        self.txt_notes_result.delete("1.0", "end")
        self.txt_notes_result.insert("1.0", text)
        self.txt_notes_result.configure(state="disabled")

    def _show_sec_result(self, text: str):
        self.txt_sec_result.configure(state="normal")
        self.txt_sec_result.delete("1.0", "end")
        self.txt_sec_result.insert("1.0", text)
        self.txt_sec_result.configure(state="disabled")


    # ══════════════════════════════════════════════════════════════════════════
    # HANDLERS — Tab Sistema
    # ══════════════════════════════════════════════════════════════════════════

    def _btn_sysinfo(self):
        self._set_status("Obteniendo información del sistema...")
        def _run():
            try:
                from os_ops import print_full_system_info
                result = print_full_system_info()
                self._set_status("✅ Info del sistema obtenida.")
            except Exception as e:
                self._set_status(f"❌ Error: {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_mic_status(self):
        self._set_status("Consultando micrófonos...")
        def _run():
            try:
                from os_ops import get_microphone_status
                est = get_microphone_status()
                micros = est.get("micros", [])
                if micros:
                    lines = [f"Micrófonos ({len(micros)}):"]
                    for m in micros:
                        ico = "✅" if m["estado"] == "OK" else "❌" if m["estado"] == "Error" else "⚠️"
                        lines.append(f"{ico} {m['nombre']} — {m['estado']}")
                    self._set_status(" | ".join(lines[:3]))
                else:
                    self._set_status("⚠️ No se encontraron micrófonos.")
            except Exception as e:
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_mic_restore(self):
        self._set_status("Restaurando micrófono...")
        def _run():
            try:
                from os_ops import restore_microphone
                res = restore_microphone()
                ok  = res.get("micros_ok", 0)
                self._set_status(f"{'✅' if res['exito'] else '⚠️'} Restauración: {ok} mic(s) OK")
            except Exception as e:
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_backup(self):
        self._set_status("Haciendo backup...")
        def _run():
            try:
                import shutil
                from datetime import datetime
                src = Path(__file__).parent / "kalmiya.db"
                dst = Path(__file__).parent.parent.parent / "_BACKUPS" / \
                      f"kalmiya_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                dst.parent.mkdir(exist_ok=True)
                shutil.copy2(src, dst)
                self._set_status(f"✅ Backup: {dst.name}")
            except Exception as e:
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_dashboard(self):
        self._set_status("Actualizando dashboard en Obsidian...")
        def _run():
            try:
                from kalmiya_dashboard import update_dashboard
                ok = update_dashboard()
                self._set_status("✅ KALMIYA_DASHBOARD.md actualizado." if ok else "❌ Error al actualizar.")
            except Exception as e:
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_obsidian(self):
        def _run():
            try:
                from os_ops import open_obsidian_vault, load_obsidian_vault_path
                open_obsidian_vault(load_obsidian_vault_path())
                self._set_status("✅ Obsidian abierto.")
            except Exception as e:
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_chat(self):
        def _run():
            try:
                from open_chat import open_kalmiya_chat
                open_kalmiya_chat()
                self._set_status("✅ Chat abierto.")
            except Exception as e:
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()


    # ══════════════════════════════════════════════════════════════════════════
    # HANDLERS — Tab Notas
    # ══════════════════════════════════════════════════════════════════════════

    def _btn_search(self):
        query = self.entry_search.get().strip()
        if not query:
            self._show_notes_result("Escribe algo para buscar.")
            return
        self._set_status(f"Buscando '{query}'...")
        def _run():
            try:
                from obsidian_bridge import search_notes
                results = search_notes(query)
                if not results:
                    self._show_notes_result(f"Sin resultados para '{query}'.")
                    self._set_status("🔍 Sin resultados.")
                    return
                lines = [f"Resultados para '{query}' ({len(results)}):"]
                for r in results:
                    lines.append(f"\n📄 {r['file']} ({r['score']} coincidencias)")
                    for s in r["snippets"][:2]:
                        lines.append(f"   › {s['text']}")
                self._show_notes_result("\n".join(lines))
                self._set_status(f"✅ {len(results)} nota(s) encontrada(s).")
            except Exception as e:
                self._show_notes_result(f"Error: {e}")
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_save_note(self):
        title   = self.entry_note_title.get().strip()
        content = self.txt_note.get("1.0", "end").strip()
        if not title:
            self._show_notes_result("❌ El título no puede estar vacío.")
            return
        if not content:
            self._show_notes_result("❌ El contenido no puede estar vacío.")
            return
        def _run():
            try:
                from obsidian_bridge import create_note
                path = create_note(title, content)
                self._show_notes_result(f"✅ Nota creada:\n{path.name}")
                self._set_status(f"✅ Nota '{title}' guardada.")
                self.root.after(0, self.entry_note_title.delete, 0, "end")
                self.root.after(0, self.txt_note.delete, "1.0", "end")
            except Exception as e:
                self._show_notes_result(f"❌ Error: {e}")
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_list_notes(self):
        def _run():
            try:
                from obsidian_bridge import list_notes
                notes = list_notes()
                if not notes:
                    self._show_notes_result("No hay notas en KALMIYA_Notes todavía.")
                else:
                    self._show_notes_result(f"Notas ({len(notes)}):\n" + "\n".join(f"  • {n}" for n in notes))
                self._set_status(f"📂 {len(notes)} nota(s) encontrada(s).")
            except Exception as e:
                self._show_notes_result(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_save_chat(self):
        def _run():
            try:
                from brain import _conversation_history
                from obsidian_bridge import save_conversation_to_obsidian
                from obsidian_bridge import get_vault
                if not _conversation_history:
                    self._show_notes_result("⚠️ No hay conversación activa para guardar.")
                    return
                path = save_conversation_to_obsidian(_conversation_history)
                self._show_notes_result(f"✅ Chat guardado:\n{path.relative_to(get_vault())}")
                self._set_status("✅ Conversación guardada en Obsidian.")
            except Exception as e:
                self._show_notes_result(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()


    # ══════════════════════════════════════════════════════════════════════════
    # HANDLERS — Tab IA
    # ══════════════════════════════════════════════════════════════════════════

    def _set_mode(self, modo: str):
        def _run():
            try:
                from brain import set_ai_mode
                set_ai_mode(modo)
                self._set_status(f"✅ Modo cambiado a: {modo}")
            except Exception as e:
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_engine_status(self):
        def _run():
            try:
                from brain import get_engine_status
                est = get_engine_status()
                lines = [
                    f"Modo actual  : {est.get('modo_actual','auto')}",
                    f"Motor usado  : {est.get('motor_usado','--')}",
                    f"Historial    : {est.get('historial_turnos',0)} turnos",
                    f"Ollama       : {'✅' if est.get('ollama_activo') else '❌'} {est.get('ollama_modelos',[])}",
                    f"Gemini       : {'✅' if est.get('gemini_activo') else '❌'}",
                    f"Claude       : {'✅' if est.get('claude_activo') else '❌ sin créditos'}",
                    f"Groq         : {'✅' if est.get('groq_activo') else '❌ sin key'}",
                    f"OpenRouter   : {'✅' if est.get('openrouter_activo') else '❌ sin key'}",
                    f"Cohere       : {'✅' if est.get('cohere_activo') else '❌ sin key'}",
                ]
                self._show_sec_result("\n".join(lines))
                self._set_status("✅ Estado de motores actualizado.")
            except Exception as e:
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    # ══════════════════════════════════════════════════════════════════════════
    # HANDLERS — Tab Seguridad
    # ══════════════════════════════════════════════════════════════════════════

    def _btn_scan_net(self):
        self._set_status("Escaneando red...")
        def _run():
            try:
                from security_ops import scan_network
                result = scan_network()
                self._show_sec_result(str(result)[:600])
                self._set_status("✅ Escaneo de red completado.")
            except Exception as e:
                self._show_sec_result(f"Error: {e}")
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_shield(self):
        self._set_status("Activando escudo cibernético...")
        def _run():
            try:
                from kalmiya_v35_features import activate_nexus_shield
                activate_nexus_shield()
                self._show_sec_result("✅ Escudo Nexus activado.")
                self._set_status("✅ Escudo activo.")
            except Exception as e:
                self._show_sec_result(f"Error: {e}")
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_password(self):
        pwd = simpledialog.askstring("Analizar contraseña",
                                      "Ingresa la contraseña a analizar:",
                                      parent=self.root)
        if not pwd:
            return
        def _run():
            try:
                from security_ops import analyze_password_strength
                result = analyze_password_strength(pwd)
                self._show_sec_result(str(result))
                self._set_status("✅ Análisis completado.")
            except Exception as e:
                self._show_sec_result(f"Error: {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_devices(self):
        self._set_status("Detectando dispositivos en red...")
        def _run():
            try:
                from security_ops import scan_network
                devices = scan_network()
                self._show_sec_result(str(devices)[:600])
                self._set_status("✅ Dispositivos detectados.")
            except Exception as e:
                self._show_sec_result(f"Error: {e}")
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    def _btn_health(self):
        self._set_status("Revisando salud del sistema...")
        def _run():
            try:
                if PSUTIL_OK:
                    cpu  = psutil.cpu_percent(interval=1)
                    mem  = psutil.virtual_memory()
                    disk = psutil.disk_usage("C:\\")
                    lines = [
                        f"CPU         : {cpu:.1f}% {'✅' if cpu < 70 else '⚠️'}",
                        f"RAM         : {mem.percent:.1f}% ({mem.used//1024**3}GB/{mem.total//1024**3}GB) {'✅' if mem.percent < 80 else '⚠️'}",
                        f"Disco C     : {disk.percent:.1f}% libre: {disk.free//1024**3}GB {'✅' if disk.percent < 85 else '⚠️'}",
                    ]
                    from database import get_db_stats
                    db = get_db_stats()
                    lines += [
                        f"BD tamaño   : {db.get('size_kb',0)} KB",
                        f"Historial   : {db.get('command_history',0)} entradas",
                        f"Pensamientos: {db.get('neural_thoughts',0)} guardados",
                    ]
                    self._show_sec_result("\n".join(lines))
                    self._set_status("✅ Salud del sistema revisada.")
            except Exception as e:
                self._show_sec_result(f"Error: {e}")
                self._set_status(f"❌ {e}")
        threading.Thread(target=_run, daemon=True).start()

    # ── Arranque ───────────────────────────────────────────────────────────────
    def run(self):
        self.root.mainloop()


# ══════════════════════════════════════════════════════════════════════════════
# Función de apertura (llamada desde kalmiya_launcher o el menú)
# ══════════════════════════════════════════════════════════════════════════════

def open_toolbox():
    """Abre la caja de herramientas en un proceso separado."""
    import subprocess
    import sys
    script = str(Path(__file__).parent / "kalmiya_toolbox.py")
    subprocess.Popen([sys.executable, script],
                     creationflags=subprocess.CREATE_NO_WINDOW
                     if sys.platform == "win32" else 0)


if __name__ == "__main__":
    tb = KalmiyaToolbox()
    tb.run()
