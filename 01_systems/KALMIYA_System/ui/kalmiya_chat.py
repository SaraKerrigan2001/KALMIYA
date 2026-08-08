"""
kalmiya_chat.py — Panel de Chat KALMIYA
========================================
Interfaz de chat premium para hablar con KALMIYA.
Se lanza al hacer clic en el icono del escritorio.
Chat de texto con IA (sin eco de voz).
"""

import customtkinter as ctk
import tkinter as tk
import threading
import time
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False

try:
    from brain import ask_kalmiya, get_engine_status, is_gemini_configured, is_ollama_running
    BRAIN_OK = True
except Exception as e:
    BRAIN_OK = False
    def ask_kalmiya(q: str, **kwargs) -> str: return "[brain.py no disponible]"
    def get_engine_status() -> dict: return {}
    def is_gemini_configured() -> bool: return False
    def is_ollama_running() -> bool: return False

from decouple import config
USERNAME = config('USER', default='Sara')
BOTNAME = config('BOTNAME', default='KALMIYA')

# ── Configuración Visual ───────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")

# Paleta de colores premium
BG_MAIN       = "#06080f"
BG_PANEL      = "#0c1019"
BG_CHAT       = "#080c14"
BG_INPUT      = "#0e1420"
BG_MSG_USER   = "#0f1e35"
BG_MSG_BOT    = "#0a1822"
ACCENT        = "#00e5ff"
ACCENT_DIM    = "#005566"
ACCENT_GLOW   = "#00b8d4"
TEXT_WHITE    = "#e8f0f2"
TEXT_DIM      = "#5a7080"
TEXT_BOT      = "#b0e0ec"
SUCCESS       = "#00e676"
WARNING       = "#ffab40"
DANGER        = "#ff5252"
BORDER_COLOR  = "#152535"

CHAT_W = 440
CHAT_H = 600


class KalmiyaChat:
    def __init__(self):
        self._drag_x = 0
        self._drag_y = 0
        self._thinking = False
        self._pulse_state = True
        self._running = True
        self._anim_dots = 0
        self._build_window()

    def _build_window(self):
        self.root = ctk.CTk()
        self.root.title("KALMIYA — Chat")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.96)
        # Quitar el borde exterior y dejar el color de fondo oscuro original
        self.root.configure(fg_color=BG_MAIN)

        # Posicionar a la derecha de la pantalla
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = sw - CHAT_W - 20
        y = (sh - CHAT_H) // 2
        self.root.geometry(f"{CHAT_W}x{CHAT_H}+{x}+{y}")

        # Usar grid directamente sobre el root (sin main_frame para evitar el borde gris)
        self.root.grid_columnconfigure(0, weight=1)
        # Fila 0: header (fijo)
        self.root.grid_rowconfigure(0, weight=0, minsize=44)
        # Fila 1: status bar (fijo)
        self.root.grid_rowconfigure(1, weight=0, minsize=24)
        # Fila 2: area de chat (expansible)
        self.root.grid_rowconfigure(2, weight=1)
        # Fila 3: thinking label (fijo)
        self.root.grid_rowconfigure(3, weight=0, minsize=16)
        # Fila 4: input area (fijo)
        self.root.grid_rowconfigure(4, weight=0, minsize=52)

        self._build_header()
        self._build_status_bar()
        self._build_chat_area()
        self._build_thinking_bar()
        self._build_input_area()
        self._draw_decorations()

        self._make_draggable()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.after(300, self._show_welcome)

    # ── DECORACIONES ──────────────────────────────────────────────────────────

    def _draw_decorations(self):
        """Dibuja esquinas HUD que cuadran perfectamente con el borde exterior de la ventana dinámicamente."""
        self.c_size = 16

        # Guardar referencias de los canvases como atributos
        self.tl_canvas = tk.Canvas(self.root, width=self.c_size, height=self.c_size, bg=BG_MAIN, highlightthickness=0)
        self.tl_canvas.create_line(1, 1, self.c_size, 1, fill=ACCENT, width=2)
        self.tl_canvas.create_line(1, 1, 1, self.c_size, fill=ACCENT, width=2)

        self.tr_canvas = tk.Canvas(self.root, width=self.c_size, height=self.c_size, bg=BG_MAIN, highlightthickness=0)
        self.tr_canvas.create_line(self.c_size-1, 1, 0, 1, fill=ACCENT, width=2)
        self.tr_canvas.create_line(self.c_size-1, 1, self.c_size-1, self.c_size, fill=ACCENT, width=2)

        self.bl_canvas = tk.Canvas(self.root, width=self.c_size, height=self.c_size, bg=BG_PANEL, highlightthickness=0)
        self.bl_canvas.create_line(1, self.c_size-1, self.c_size, self.c_size-1, fill=ACCENT_DIM, width=2)
        self.bl_canvas.create_line(1, 0, 1, self.c_size-1, fill=ACCENT_DIM, width=2)

        self.br_canvas = tk.Canvas(self.root, width=self.c_size, height=self.c_size, bg=BG_PANEL, highlightthickness=0)
        self.br_canvas.create_line(0, self.c_size-1, self.c_size-1, self.c_size-1, fill=ACCENT_DIM, width=2)
        self.br_canvas.create_line(self.c_size-1, 0, self.c_size-1, self.c_size-1, fill=ACCENT_DIM, width=2)

        # Enlazar la actualización de posición al evento de configuración de ventana
        self.root.bind("<Configure>", self._on_window_configure)

    def _on_window_configure(self, event):
        """Reposiciona las esquineras dinámicamente al tamaño real y actual de la ventana."""
        if event.widget == self.root:
            w = event.width
            h = event.height
            
            # Colocar en las 4 esquinas absolutas de la ventana
            self.tl_canvas.place(x=0, y=0)
            self.tr_canvas.place(x=w - self.c_size, y=0)
            self.bl_canvas.place(x=0, y=h - self.c_size)
            self.br_canvas.place(x=w - self.c_size, y=h - self.c_size)

    # ── HEADER ────────────────────────────────────────────────────────────────

    def _build_header(self):
        """Cabecera con nombre y botones."""
        header = tk.Frame(self.root, bg=BG_MAIN, height=44)
        header.grid(row=0, column=0, sticky="ew", padx=6, pady=(4, 0))
        header.grid_columnconfigure(1, weight=1)

        # Punto de estado
        self.status_dot = tk.Canvas(header, width=10, height=10,
                                     bg=BG_MAIN, highlightthickness=0)
        self.status_dot.grid(row=0, column=0, padx=(8, 6), pady=14)
        self._draw_status_dot(SUCCESS)

        # Nombre
        name_frame = tk.Frame(header, bg=BG_MAIN)
        name_frame.grid(row=0, column=1, sticky="w", pady=10)
        tk.Label(name_frame, text="KALMIYA", font=("Consolas", 15, "bold"),
                 fg=ACCENT, bg=BG_MAIN).pack(side="left")
        tk.Label(name_frame, text="  CHAT", font=("Consolas", 9),
                 fg=TEXT_DIM, bg=BG_MAIN).pack(side="left", pady=(3, 0))

        # Botones minimizar/cerrar
        btn_f = tk.Frame(header, bg=BG_MAIN)
        btn_f.grid(row=0, column=2, padx=4, pady=10)

        min_btn = tk.Label(btn_f, text="—", font=("Consolas", 12),
                           fg=TEXT_DIM, bg=BG_MAIN, cursor="hand2", padx=6)
        min_btn.pack(side="left")
        min_btn.bind("<Button-1>", lambda e: self._minimize())
        min_btn.bind("<Enter>", lambda e: min_btn.config(fg=ACCENT))
        min_btn.bind("<Leave>", lambda e: min_btn.config(fg=TEXT_DIM))

        close_btn = tk.Label(btn_f, text="✕", font=("Consolas", 11),
                             fg=TEXT_DIM, bg=BG_MAIN, cursor="hand2", padx=6)
        close_btn.pack(side="left")
        close_btn.bind("<Button-1>", lambda e: self._on_close())
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg=DANGER))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg=TEXT_DIM))

        # Separador
        sep = tk.Canvas(self.root, height=1, bg=BORDER_COLOR, highlightthickness=0)
        sep.grid(row=0, column=0, sticky="sew", padx=10)

    # ── BARRA DE ESTADO ───────────────────────────────────────────────────────

    def _build_status_bar(self):
        """Barra con motor de IA y reloj."""
        bar = tk.Frame(self.root, bg=BG_PANEL, height=24)
        bar.grid(row=1, column=0, sticky="ew")

        self.engine_label = tk.Label(bar, text="  ◆ CONECTANDO...",
                                      font=("Consolas", 8), fg=TEXT_DIM, bg=BG_PANEL)
        self.engine_label.pack(side="left", padx=8, pady=3)

        self.time_label = tk.Label(bar, text="00:00:00",
                                    font=("Consolas", 8), fg=TEXT_DIM, bg=BG_PANEL)
        self.time_label.pack(side="right", padx=8, pady=3)

        threading.Thread(target=self._check_ai_status, daemon=True).start()
        if config('KALMIYA_ENABLE_WALLPAPER', default='true', cast=str).lower() in ('1', 'true'):
            threading.Thread(target=self._background_wallpaper_updater, daemon=True, name="chat-wallpaper-updater").start()

    # ── AREA DE CHAT ──────────────────────────────────────────────────────────

    def _build_chat_area(self):
        """Area principal con mensajes."""
        # Contenedor del chat
        chat_host = tk.Frame(self.root, bg=BG_CHAT)
        chat_host.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        chat_host.grid_columnconfigure(0, weight=1)
        chat_host.grid_rowconfigure(0, weight=1)

        # Marca de agua sutil (canvas de fondo)
        self.watermark = tk.Canvas(chat_host, bg=BG_CHAT, highlightthickness=0)
        self.watermark.place(x=0, y=0, relwidth=1, relheight=1)
        self.watermark.create_text(CHAT_W//2, 200,
                                    text="KALMIYA", font=("Consolas", 42, "bold"),
                                    fill="#0b1420")

        # Canvas de scroll manual (sin CTkScrollableFrame para tener control total)
        self.chat_canvas = tk.Canvas(chat_host, bg=BG_CHAT, highlightthickness=0,
                                      bd=0)
        # Scrollbar delgada y sutil
        self.scrollbar = tk.Scrollbar(chat_host, orient="vertical",
                                       command=self.chat_canvas.yview,
                                       width=6, troughcolor=BG_CHAT,
                                       bg=ACCENT_DIM, activebackground=ACCENT,
                                       relief="flat", bd=0)

        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=0, column=1, sticky="ns", pady=6)
        self.chat_canvas.grid(row=0, column=0, sticky="nsew", padx=(10, 2), pady=6)

        # Frame interior para los mensajes
        self.msg_frame = tk.Frame(self.chat_canvas, bg=BG_CHAT)
        self.canvas_window = self.chat_canvas.create_window(
            (0, 0), window=self.msg_frame, anchor="nw"
        )

        # Ajustar tamaño del frame interior cuando cambie
        self.msg_frame.bind("<Configure>", self._on_msg_frame_configure)
        self.chat_canvas.bind("<Configure>", self._on_canvas_configure)

        # Scroll con rueda del mouse
        self.chat_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_msg_frame_configure(self, event):
        """Actualiza la region de scroll cuando se agregan mensajes."""
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Ajusta el ancho del frame interior al ancho del canvas."""
        self.chat_canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        """Scroll con la rueda del mouse."""
        self.chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── BARRA DE PENSANDO ─────────────────────────────────────────────────────

    def _build_thinking_bar(self):
        """Label que muestra 'KALMIYA pensando...'"""
        think_f = tk.Frame(self.root, bg=BG_MAIN, height=16)
        think_f.grid(row=3, column=0, sticky="ew")
        self.thinking_label = tk.Label(think_f, text="", font=("Consolas", 8),
                                        fg=ACCENT_DIM, bg=BG_MAIN, anchor="w")
        self.thinking_label.pack(side="left", padx=14)

    # ── AREA DE ENTRADA ───────────────────────────────────────────────────────

    def _build_input_area(self):
        """Campo de texto + boton enviar + opciones."""
        # Separador sutil
        sep = tk.Canvas(self.root, height=1, bg=BORDER_COLOR, highlightthickness=0)
        sep.grid(row=3, column=0, sticky="sew", padx=12)

        input_f = tk.Frame(self.root, bg=BG_PANEL, height=76)
        input_f.grid(row=4, column=0, sticky="ew")
        input_f.grid_columnconfigure(0, weight=1)

        # Opciones extra arriba del input
        opt_f = tk.Frame(input_f, bg=BG_PANEL)
        opt_f.grid(row=0, column=0, columnspan=2, sticky="ew", padx=14, pady=(6, 0))
        
        self.use_rag_var = ctk.BooleanVar(value=True)
        self.rag_cb = ctk.CTkCheckBox(
            opt_f, text="📚 Usar RAG (Buscar en mis documentos)", 
            variable=self.use_rag_var,
            font=("Consolas", 10),
            fg_color=ACCENT, hover_color=ACCENT_DIM,
            width=120, height=18, checkbox_width=16, checkbox_height=16
        )
        self.rag_cb.pack(side="left")

        # Entry
        self.input_var = tk.StringVar()
        self.entry = tk.Entry(
            input_f,
            textvariable=self.input_var,
            font=("Consolas", 11),
            bg=BG_INPUT, fg=TEXT_WHITE,
            insertbackground=ACCENT,
            relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
            highlightcolor=ACCENT_DIM
        )
        self.entry.grid(row=1, column=0, sticky="ew", padx=(14, 6), pady=(4, 10), ipady=8)
        self.entry.bind("<Return>", self._on_send)

        # Boton enviar
        self.send_btn = tk.Label(
            input_f, text=" ➤ ", font=("Consolas", 14, "bold"),
            fg=BG_MAIN, bg=ACCENT_DIM, cursor="hand2",
            padx=8, pady=4
        )
        self.send_btn.grid(row=1, column=1, padx=(0, 14), pady=(4, 10))
        self.send_btn.bind("<Button-1>", self._on_send)
        self.send_btn.bind("<Enter>", lambda e: self.send_btn.config(bg=ACCENT))
        self.send_btn.bind("<Leave>", lambda e: self.send_btn.config(
            bg=ACCENT_DIM if not self._thinking else "#1a2030"))

    # ══════════════════════════════════════════════════════════════════════════
    #  MENSAJES DEL CHAT
    # ══════════════════════════════════════════════════════════════════════════

    def _add_message(self, role: str, text: str):
        """Agrega un mensaje al chat con burbuja."""
        is_bot = role.upper() == "KALMIYA"
        is_system = role.upper() == "SISTEMA"

        # Color de la burbuja
        if is_bot:
            bubble_bg = BG_MSG_BOT
            pad_l, pad_r = 6, 40
        elif is_system:
            bubble_bg = BG_CHAT
            pad_l, pad_r = 20, 20
        else:
            bubble_bg = BG_MSG_USER
            pad_l, pad_r = 40, 6

        # Wrapper con padding
        wrapper = tk.Frame(self.msg_frame, bg=BG_CHAT)
        wrapper.pack(fill="x", padx=(pad_l, pad_r), pady=3)

        # Burbuja
        bubble = tk.Frame(wrapper, bg=bubble_bg, bd=0,
                           highlightthickness=1,
                           highlightbackground="#1a2a3a" if not is_system else BG_CHAT)
        bubble.pack(fill="x", anchor="w" if is_bot else "e")

        # Header (nombre + hora)
        head = tk.Frame(bubble, bg=bubble_bg)
        head.pack(fill="x", padx=10, pady=(6, 0))

        name_color = ACCENT if is_bot else (TEXT_DIM if is_system else WARNING)
        tk.Label(head, text=role.upper(), font=("Consolas", 8, "bold"),
                 fg=name_color, bg=bubble_bg).pack(side="left")

        hora = datetime.now().strftime("%H:%M")
        tk.Label(head, text=hora, font=("Consolas", 7),
                 fg="#2a3a4a", bg=bubble_bg).pack(side="right")

        # Texto del mensaje
        txt_color = TEXT_BOT if is_bot else (TEXT_DIM if is_system else TEXT_WHITE)
        txt_font = ("Segoe UI", 10) if not is_system else ("Consolas", 8)
        msg_lbl = tk.Label(bubble, text=text, font=txt_font,
                            fg=txt_color, bg=bubble_bg,
                            wraplength=CHAT_W - pad_l - pad_r - 40,
                            justify="left", anchor="w")
        msg_lbl.pack(fill="x", padx=10, pady=(2, 8))

        # Auto-scroll al final
        self.root.after(50, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        """Hace scroll al último mensaje."""
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def _show_welcome(self):
        """Muestra el mensaje de bienvenida."""
        hora = datetime.now().hour
        if 6 <= hora < 12:
            saludo = "Buenos días"
        elif 12 <= hora < 19:
            saludo = "Buenas tardes"
        else:
            saludo = "Buenas noches"

        msg = f"{saludo}, {USERNAME}. Estoy lista para hablar contigo. Escribe lo que necesites."
        self._add_message("KALMIYA", msg)
        self.entry.focus_set()
        
        # Hablar el mensaje de bienvenida si el sistema lo permite
        try:
            from voz import speak
            threading.Thread(target=speak, args=(msg,), daemon=True).start()
        except Exception as e:
            pass

    # ══════════════════════════════════════════════════════════════════════════
    #  ENVÍO Y PROCESAMIENTO
    # ══════════════════════════════════════════════════════════════════════════

    def _on_send(self, event=None):
        text = self.input_var.get().strip()
        if not text or self._thinking:
            return
        self.input_var.set("")
        self._add_message(USERNAME, text)
        self._set_thinking(True)
        threading.Thread(target=self._process_message, args=(text,), daemon=True).start()

    def _process_message(self, text: str):
        # ── Interceptar comandos de Obsidian primero ──────────────────────────
        try:
            from obsidian_bridge import process_obsidian_command
            obs_response = process_obsidian_command(text)
            if obs_response is not None:
                self.root.after(0, self._on_response, obs_response)
                return
        except Exception:
            pass

        # ── Interceptar comandos de PC (Discos y Carpetas) ────────────────────
        try:
            from pc_bridge import process_pc_command
            pc_response = process_pc_command(text)
            if pc_response is not None:
                self.root.after(0, self._on_response, pc_response)
                return
        except Exception:
            pass

        # ── Respuesta de IA con/sin RAG ───────────────────────────────────────
        try:
            if getattr(self, "use_rag_var", None) and self.use_rag_var.get():
                try:
                    from kalmiya_rag import responder_con_rag
                    rag_res = responder_con_rag(text)
                    if isinstance(rag_res, dict):
                        response = rag_res.get("response", str(rag_res))
                        # Opcional: mostrar fuentes en la UI
                        fuentes = rag_res.get("rag_sources", [])
                        if fuentes:
                            response += f"\n\n[📚 RAG usó {len(fuentes)} fuentes]"
                    else:
                        response = str(rag_res)
                except Exception as e:
                    # Fallback si falla RAG
                    response = ask_kalmiya(text)
            else:
                response = ask_kalmiya(text)
        except Exception as e:
            response = f"Error de enlace con la IA: {e}"
        
        self.root.after(0, self._on_response, response)

    def _on_response(self, response: str):
        """Muestra la respuesta de KALMIYA."""
        self._set_thinking(False)
        self._add_message("KALMIYA", response)
        
        # Opcional: También hablar las respuestas del chat si se desea
        # Descomentar si el usuario quiere que KALMIYA hable todas las respuestas
        # try:
        #     from voz import speak
        #     clean_text = re.sub(r'\[.*?\]', '', response).strip() # Quitar tags de RAG
        #     threading.Thread(target=speak, args=(clean_text,), daemon=True).start()
        # except Exception:
        #     pass

    def _set_thinking(self, active: bool):
        self._thinking = active
        self.entry.configure(state="disabled" if active else "normal")
        btn_bg = "#1a2030" if active else ACCENT_DIM
        btn_fg = TEXT_DIM if active else BG_MAIN
        self.send_btn.configure(bg=btn_bg, fg=btn_fg)
        if active:
            self._anim_dots = 0
            self._animate_thinking()
        else:
            self.thinking_label.configure(text="")
            self.entry.configure(state="normal")
            self.entry.focus_set()

    def _animate_thinking(self):
        if not self._thinking:
            return
        dots = "·" * (self._anim_dots % 4)
        self.thinking_label.configure(text=f"  ◆ KALMIYA pensando{dots}")
        self._anim_dots += 1
        self.root.after(400, self._animate_thinking)

    # ══════════════════════════════════════════════════════════════════════════
    #  ESTADO Y UTILIDADES
    # ══════════════════════════════════════════════════════════════════════════

    def _check_ai_status(self):
        try:
            gemini = is_gemini_configured()
            ollama = is_ollama_running()

            if gemini and ollama:
                label, color = "◆ GEMINI + OLLAMA", SUCCESS
            elif gemini:
                label, color = "◆ GEMINI ACTIVO", SUCCESS
            elif ollama:
                label, color = "◆ OLLAMA LOCAL", ACCENT
            else:
                label, color = "◆ SIN MOTOR IA", DANGER

            self.root.after(0, lambda: self.engine_label.configure(
                text=f"  {label}", fg=color))
        except Exception:
            pass
        self._update_loop()

    def _update_loop(self):
        while self._running:
            try:
                now = datetime.now().strftime("%H:%M:%S")
                self.root.after(0, lambda t=now: self.time_label.configure(text=t))
                self._pulse_state = not self._pulse_state
                color = SUCCESS if self._pulse_state else "#004422"
                self.root.after(0, lambda c=color: self._draw_status_dot(c))
            except Exception:
                break
            time.sleep(1)

    def _draw_status_dot(self, color):
        self.status_dot.delete("all")
        self.status_dot.create_oval(1, 1, 9, 9, fill=color, outline="")

    # ══════════════════════════════════════════════════════════════════════════
    #  DRAGGING Y CONTROL DE VENTANA
    # ══════════════════════════════════════════════════════════════════════════

    def _make_draggable(self):
        # Arrastrar desde la cabecera (header) y desde el fondo del root para mover
        self.root.bind("<ButtonPress-1>", self._drag_start)
        self.root.bind("<B1-Motion>", self._drag_move)

    def _drag_start(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _drag_move(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")

    def _minimize(self):
        self.root.overrideredirect(False)
        self.root.iconify()
        self.root.after(500, lambda: self.root.overrideredirect(True))

    def _background_wallpaper_updater(self):
        """Mantiene el fondo de pantalla sincronizado con la hora exacta si el launcher no está corriendo."""
        def is_launcher_running():
            if not PSUTIL_OK:
                return False
            for p in psutil.process_iter(['cmdline']):
                try:
                    cmd = p.info.get('cmdline') or []
                    if any('kalmiya_launcher.py' in part for part in cmd):
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return False

        # Primera actualización al iniciar el chat (para asegurar que coincide al instante con la hora exacta)
        if not is_launcher_running():
            try:
                from wallpaper_engine import update_wallpaper
                update_wallpaper()
            except Exception:
                pass

        while self._running:
            # Esperar 60 segundos
            for _ in range(60):
                if not self._running:
                    break
                time.sleep(1)

            if not self._running:
                break

            if not is_launcher_running():
                try:
                    from wallpaper_engine import update_wallpaper
                    update_wallpaper()
                except Exception:
                    pass

    def _on_close(self):
        self._running = False
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    KalmiyaChat().run()
