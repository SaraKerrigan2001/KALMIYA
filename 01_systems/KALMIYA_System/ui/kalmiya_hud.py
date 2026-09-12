"""
kalmiya_hud.py - HUD Rediseñado v3.7 (Cyber Pink Ultra)
Basado en la referencia visual del usuario.
"""

import customtkinter as ctk
import tkinter as tk
import threading
import time
import sys
import os
from datetime import datetime

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False

try:
    import requests as _req
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from brain import ask_kalmiya, get_engine_status  # type: ignore
    BRAIN_OK = True
except Exception:
    BRAIN_OK = False
    def ask_kalmiya(q: str, **kwargs) -> str: return "[brain.py no disponible]"
    def get_engine_status() -> dict: return {}

try:
    from voz import speak  # type: ignore
    VOZ_OK = True
except Exception:
    VOZ_OK = False
    def speak(text: str):
        print(f"[KALMIYA - MUDO]: {text}")

# ── Configuración Visual (Cyber Pink) ──────────────────────────────────────────
ctk.set_appearance_mode("dark")

BG_APP       = "#160a22"  # Fondo principal ultra oscuro
BG_CARD      = "#281b3c"  # Fondo de tarjetas
BG_BUBBLE_U  = "#ff66b2"  # Burbuja Usuario (Rosa)
BG_BUBBLE_K  = "#3d266b"  # Burbuja Kalmiya (Morado)
ACCENT_PINK  = "#ff66b2"  # Rosa neón
ACCENT_DIM   = "#4a2d75"  # Morado oscuro (para botones sutiles)
TEXT_WHITE   = "#ffffff"
TEXT_DIM     = "#a89eb8"
SUCCESS      = "#ff66b2"  # Online status in pink

HUD_W = 480
HUD_H = 800

def _check_network() -> bool:
    if not REQUESTS_OK: return False
    try:
        _req.get("https://www.google.com", timeout=3)
        return True
    except Exception: return False

class KalmiyaHUD:
    def __init__(self):
        self._drag_x = 0
        self._drag_y = 0
        self._chat_history = []
        self._stats_running = False
        self._thinking = False
        self._network_ok = False
        self._net_check_counter = 0
        self._voice_active = False
        self._current_theme_idx = 0
        self._themes = ["pink", "cyan", "green"]
        self._build_window()

    def _build_window(self):
        self.root = ctk.CTk()
        self.root.title("KALMIYA V4")
        self.root.geometry(f"{HUD_W}x{HUD_H}")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(fg_color=BG_APP)
        
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{HUD_W}x{HUD_H}+{sw - HUD_W - 30}+{(sh - HUD_H)//2}")

        self._build_header()
        self._build_profile_card()
        self._build_chat_section()
        self._build_input_section()
        self._build_footer()
        
        self._make_draggable()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_header(self):
        header = ctk.CTkFrame(self.root, fg_color="transparent", height=40)
        header.pack(fill="x", padx=15, pady=10)
        
        # Logo y Título
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        ctk.CTkLabel(title_frame, text="✦ ", font=ctk.CTkFont("Segoe UI", 16), text_color=ACCENT_PINK).pack(side="left")
        ctk.CTkLabel(title_frame, text="KALMIYA", font=ctk.CTkFont("Segoe UI", 15, "bold"), text_color=TEXT_WHITE).pack(side="left")
        ctk.CTkLabel(title_frame, text=" V4 ", font=ctk.CTkFont("Segoe UI", 10), text_color=TEXT_DIM).pack(side="left", padx=5)
        ctk.CTkLabel(title_frame, text="✦", font=ctk.CTkFont("Segoe UI", 16), text_color=ACCENT_PINK).pack(side="left")

        # Controles derecha
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        # Minimizar y cerrar
        ctk.CTkButton(btn_frame, text="X", width=30, height=30, fg_color="transparent", 
                      hover_color="#500", font=ctk.CTkFont("Arial", 14), command=self._on_close).pack(side="right", padx=(5,0))
        ctk.CTkButton(btn_frame, text="—", width=30, height=30, fg_color="transparent", 
                      hover_color=ACCENT_DIM, font=ctk.CTkFont("Arial", 14), command=self._minimize).pack(side="right")
        
        # Opciones
        ctk.CTkButton(btn_frame, text="? Ayuda", width=60, height=26, fg_color=BG_CARD, 
                      hover_color=ACCENT_DIM, corner_radius=5, font=ctk.CTkFont("Segoe UI", 11)).pack(side="right", padx=5)
        self.btn_tema = ctk.CTkButton(btn_frame, text="⚙ Tema", width=60, height=26, fg_color=BG_CARD, 
                      hover_color=ACCENT_DIM, corner_radius=5, font=ctk.CTkFont("Segoe UI", 11), command=self._toggle_theme)
        self.btn_tema.pack(side="right", padx=5)
        
        # Status
        self.net_label = ctk.CTkLabel(btn_frame, text="● ONLINE", font=ctk.CTkFont("Segoe UI", 10, "bold"), text_color=ACCENT_PINK)
        self.net_label.pack(side="right", padx=10)

    def _build_profile_card(self):
        self.profile = ctk.CTkFrame(self.root, fg_color=BG_CARD, corner_radius=15)
        self.profile.pack(fill="x", padx=15, pady=(0, 10), ipady=10)
        
        # Contenedor superior (Avatar + Textos)
        top_frame = ctk.CTkFrame(self.profile, fg_color="transparent")
        top_frame.pack(fill="x", padx=15, pady=10)
        
        # Avatar (Emoji como placeholder si no hay imagen)
        self.avatar_lbl = ctk.CTkLabel(top_frame, text="🤖", font=ctk.CTkFont("Segoe UI", 60))
        self.avatar_lbl.pack(side="left", padx=(10, 20))
        
        info_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        self.greeting_lbl = ctk.CTkLabel(info_frame, text="¡Buenas noches!, Sara Kerigan!", 
                                         font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=TEXT_WHITE)
        self.greeting_lbl.pack(anchor="w")
        
        ctk.CTkLabel(info_frame, text="🚀 ¿Qué aventura tenemos hoy?", 
                     font=ctk.CTkFont("Segoe UI", 12), text_color=TEXT_DIM).pack(anchor="w", pady=(0, 10))
        
        btn_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        btn_row.pack(anchor="w")
        
        self.btn_voz = ctk.CTkButton(btn_row, text="🎙️ Voz", width=80, height=28, fg_color=ACCENT_PINK, 
                      hover_color="#e555a0", text_color="#111", corner_radius=8, font=ctk.CTkFont("Segoe UI", 12), command=self._toggle_voz)
        self.btn_voz.pack(side="left", padx=(0, 10))
        self.btn_rapido = ctk.CTkButton(btn_row, text="⚡ Rápido", width=80, height=28, fg_color=ACCENT_DIM, 
                      hover_color=BG_BUBBLE_K, corner_radius=8, font=ctk.CTkFont("Segoe UI", 12), command=self._on_nexus_boost)
        self.btn_rapido.pack(side="left")
        
        # Discos
        ctk.CTkButton(btn_row, text="C:", width=35, height=28, fg_color=BG_APP, 
                      hover_color=ACCENT_DIM, corner_radius=5, font=ctk.CTkFont("Segoe UI", 11, "bold"), 
                      command=lambda: os.startfile("C:\\") if os.path.exists("C:\\") else None).pack(side="left", padx=(15, 5))
        ctk.CTkButton(btn_row, text="D:", width=35, height=28, fg_color=BG_APP, 
                      hover_color=ACCENT_DIM, corner_radius=5, font=ctk.CTkFont("Segoe UI", 11, "bold"), 
                      command=lambda: os.startfile("D:\\") if os.path.exists("D:\\") else None).pack(side="left")
        
        # Stats inferiores
        self.stats_lbl = ctk.CTkLabel(self.profile, text="CPU: 0% | RAM: 0% | Disco: 0%", 
                                      font=ctk.CTkFont("Segoe UI", 10), text_color=TEXT_DIM)
        self.stats_lbl.pack(anchor="w", padx=30)

    def _build_chat_section(self):
        # Contenedor principal de chat
        self.chat_wrapper = ctk.CTkFrame(self.root, fg_color=BG_CARD, corner_radius=15)
        self.chat_wrapper.pack(fill="both", expand=True, padx=15, pady=(5, 5))
        
        # Header del chat
        chat_header = ctk.CTkFrame(self.chat_wrapper, fg_color="transparent", height=40)
        chat_header.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(chat_header, text="💬 Conversación", font=ctk.CTkFont("Segoe UI", 13, "bold"), text_color=TEXT_WHITE).pack(side="left")
        
        ctk.CTkButton(chat_header, text="🗑", width=28, height=28, fg_color="transparent", hover_color=ACCENT_DIM, font=ctk.CTkFont("Segoe UI", 14), command=self._clear_chat).pack(side="right")
        ctk.CTkButton(chat_header, text="📄", width=28, height=28, fg_color="transparent", hover_color=ACCENT_DIM, font=ctk.CTkFont("Segoe UI", 14)).pack(side="right", padx=5)

        # Separador
        sep = ctk.CTkFrame(self.chat_wrapper, fg_color=BG_APP, height=2)
        sep.pack(fill="x", padx=15, pady=0)

        # Área de scroll (ScrollableFrame)
        self.chat_frame = ctk.CTkScrollableFrame(self.chat_wrapper, fg_color="transparent", scrollbar_button_color=ACCENT_DIM)
        self.chat_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Mensaje inicial de bienvenida
        self._add_bubble("KALMIYA", "Bienvenida Sara Kerrigan como estas, en que puedo ayudarte en el día de hoy.")

    def _add_bubble(self, role, text):
        is_user = role.upper() == "SARA"
        bg_color = BG_BUBBLE_U if is_user else BG_BUBBLE_K
        txt_color = "#111111" if is_user else TEXT_WHITE
        
        # Fila contenedora para alinear a izq/der
        row_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=5, padx=10)
        
        # Marco de la burbuja
        bubble = ctk.CTkFrame(row_frame, fg_color=bg_color, corner_radius=15)
        bubble.pack(side="right" if is_user else "left")
        
        if not is_user:
            # Header de la burbuja (Solo para KALMIYA)
            header_f = ctk.CTkFrame(bubble, fg_color="transparent")
            header_f.pack(fill="x", padx=10, pady=(5, 0))
            now_str = datetime.now().strftime("%H:%M")
            ctk.CTkLabel(header_f, text="🤖 KALMIYA", font=ctk.CTkFont("Segoe UI", 9, "bold"), text_color=ACCENT_PINK).pack(side="left")
            ctk.CTkLabel(header_f, text=now_str, font=ctk.CTkFont("Segoe UI", 8), text_color=TEXT_DIM).pack(side="right")
            
        # Contenido
        w_len = 280 if len(text) > 35 else 0
        msg = ctk.CTkLabel(bubble, text=text, font=ctk.CTkFont("Segoe UI", 12), text_color=txt_color,
                           wraplength=w_len, justify="left" if not is_user else "right")
        msg.pack(anchor="w" if not is_user else "e", padx=15, pady=(2 if not is_user else 10, 10))
        
        self.root.after(100, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    def _clear_chat(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()

    def _build_input_section(self):
        self.input_wrapper = ctk.CTkFrame(self.root, fg_color=BG_CARD, corner_radius=20, height=60, border_width=1, border_color=ACCENT_DIM)
        self.input_wrapper.pack(fill="x", padx=15, pady=(10, 5), ipady=5)
        self.input_wrapper.pack_propagate(False)
        
        self.input_var = tk.StringVar()
        self.entry = ctk.CTkEntry(self.input_wrapper, textvariable=self.input_var, placeholder_text="Escribe aquí...",
                                  font=ctk.CTkFont("Segoe UI", 12), fg_color="transparent", border_width=0, text_color=TEXT_WHITE)
        self.entry.pack(side="left", fill="both", expand=True, padx=20)
        self.entry.bind("<Return>", self._on_send)
        
        self.send_btn = ctk.CTkButton(self.input_wrapper, text="...", width=45, height=40, fg_color=BG_APP,
                                      hover_color=ACCENT_DIM, corner_radius=20, command=self._on_send)
        self.send_btn.pack(side="right", padx=10)

    def _build_footer(self):
        footer = ctk.CTkFrame(self.root, fg_color="transparent", height=20)
        footer.pack(fill="x", padx=20, pady=(5, 10))
        
        ctk.CTkLabel(footer, text="⚙ LOCAL • V4", font=ctk.CTkFont("Segoe UI", 10), text_color=TEXT_DIM).pack(side="left")
        
        self.clock_lbl = ctk.CTkLabel(footer, text="🎨 Cyber Pink ♡ 00:00", font=ctk.CTkFont("Segoe UI", 10), text_color=TEXT_DIM)
        self.clock_lbl.pack(side="right")

    def _on_send(self, e=None):
        txt = self.input_var.get().strip()
        if not txt or self._thinking: return
        self.input_var.set("")
        self._add_bubble("SARA", txt)
        self._set_thinking(True)
        threading.Thread(target=self._proc, args=(txt,), daemon=True).start()

    def _proc(self, txt):
        try:
            res = ask_kalmiya(txt)
        except Exception as e:
            import traceback
            print(f"[HUD] Error en ask_kalmiya: {e}\n{traceback.format_exc()}")
            res = f"Error de enlace: {e}"
        self.root.after(0, self._on_res, res)

    def _on_res(self, res):
        self._set_thinking(False)
        self._add_bubble("KALMIYA", res)

    def _set_thinking(self, b):
        self._thinking = b
        self.entry.configure(state="disabled" if b else "normal")

    def _on_nexus_boost(self):
        self._add_bubble("SARA", "[Ejecutando Boost]")
        self._set_thinking(True)
        threading.Thread(target=self._run_boost, daemon=True).start()

    def _run_boost(self):
        try:
            from kalmiya_v4_features import smart_performance_boost
            # Ejecutamos la limpieza en consola sin enviar todo el string a la UI
            smart_performance_boost()
            self.root.after(0, self._on_res, "⚡ Optimización completada. El sistema está ahora a su máximo rendimiento.")
        except: self.root.after(0, self._on_res, "Boost fallido.")

    def _start_stats(self):
        self._stats_running = True
        threading.Thread(target=self._stats_loop, daemon=True).start()

    def _stats_loop(self):
        while self._stats_running:
            if PSUTIL_OK:
                c = psutil.cpu_percent(interval=1)
                r = psutil.virtual_memory().percent
                d = psutil.disk_usage('C:\\').percent if sys.platform == "win32" else psutil.disk_usage('/').percent
            else:
                c = r = d = 0
                time.sleep(1)
                
            self._net_check_counter += 1
            if self._net_check_counter >= 5:
                self._network_ok = _check_network()
                self._net_check_counter = 0
            
            self.root.after(0, self._upd_ui, c, r, d)

    def _upd_ui(self, c, r, d):
        self.stats_lbl.configure(text=f"CPU: {c}% | RAM: {r}% | Disco: {d}%")
        
        now = datetime.now()
        greeting = "¡Buenas noches!" if now.hour >= 18 else "¡Buenos días!" if now.hour < 12 else "¡Buenas tardes!"
        self.greeting_lbl.configure(text=f"{greeting}, Sara Kerigan!")
        self.clock_lbl.configure(text=f"🎨 Cyber Pink ♡ {now.strftime('%H:%M')}")
        self.net_label.configure(text="● ONLINE" if self._network_ok else "○ OFFLINE", 
                                 text_color=SUCCESS if self._network_ok else TEXT_DIM)

    def _toggle_theme(self):
        global BG_APP, BG_CARD, ACCENT_PINK, ACCENT_DIM, BG_BUBBLE_U, BG_BUBBLE_K, SUCCESS
        self._current_theme_idx = (self._current_theme_idx + 1) % len(self._themes)
        theme = self._themes[self._current_theme_idx]
        
        if theme == "cyan":
            BG_APP = "#050510"
            BG_CARD = "#020a15"
            ACCENT_PINK = "#00f2ff"
            ACCENT_DIM = "#004d55"
            BG_BUBBLE_U = "#00f2ff"
            BG_BUBBLE_K = "#004d55"
            SUCCESS = "#00f2ff"
            self.clock_lbl.configure(text=f"🎨 Cyber Cyan ♡ {datetime.now().strftime('%H:%M')}")
        elif theme == "green":
            BG_APP = "#010a01"
            BG_CARD = "#021a02"
            ACCENT_PINK = "#00ff00"
            ACCENT_DIM = "#005500"
            BG_BUBBLE_U = "#00ff00"
            BG_BUBBLE_K = "#005500"
            SUCCESS = "#00ff00"
            self.clock_lbl.configure(text=f"🎨 Matrix Green ♡ {datetime.now().strftime('%H:%M')}")
        else: # pink
            BG_APP = "#160a22"
            BG_CARD = "#281b3c"
            ACCENT_PINK = "#ff66b2"
            ACCENT_DIM = "#4a2d75"
            BG_BUBBLE_U = "#ff66b2"
            BG_BUBBLE_K = "#3d266b"
            SUCCESS = "#ff66b2"
            self.clock_lbl.configure(text=f"🎨 Cyber Pink ♡ {datetime.now().strftime('%H:%M')}")

        self.root.configure(fg_color=BG_APP)
        self.profile.configure(fg_color=BG_CARD)
        self.chat_wrapper.configure(fg_color=BG_CARD)
        self.input_wrapper.configure(fg_color=BG_CARD, border_color=ACCENT_DIM)
        self.btn_tema.configure(fg_color=BG_CARD, hover_color=ACCENT_DIM)
        self.btn_voz.configure(fg_color=SUCCESS if self._voice_active else ACCENT_PINK)
        self.btn_rapido.configure(fg_color=ACCENT_DIM, hover_color=BG_BUBBLE_K)
        self.send_btn.configure(fg_color=BG_APP, hover_color=ACCENT_DIM)
        self.net_label.configure(text_color=SUCCESS if self._network_ok else TEXT_DIM)
        
        # Opcional: Actualizar color de textos y bordes si es necesario
        for widget in self.chat_frame.winfo_children():
            # Actualizar colores en burbujas existentes es complejo sin referencias, 
            # pero los nuevos mensajes usarán el nuevo color.
            pass

    def _toggle_voz(self):
        self._voice_active = not self._voice_active
        if self._voice_active:
            self.btn_voz.configure(text="🎙️ Voz (ON)", fg_color=SUCCESS)
            self._add_bubble("KALMIYA", "Módulo de voz activado.")
        else:
            self.btn_voz.configure(text="🎙️ Voz", fg_color=ACCENT_PINK)
            self._add_bubble("KALMIYA", "Módulo de voz desactivado.")

    def _make_draggable(self):
        self.root.bind("<ButtonPress-1>", self._drag_start)
        self.root.bind("<B1-Motion>", self._drag_move)
    def _drag_start(self, e):
        self._drag_x, self._drag_y = e.x, e.y
    def _drag_move(self, e):
        x = self.root.winfo_x() + (e.x - self._drag_x)
        y = self.root.winfo_y() + (e.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")

    def _minimize(self):
        self.root.overrideredirect(False)
        self.root.iconify()
        self.root.after(500, lambda: self.root.overrideredirect(True))

    def _on_close(self):
        self._stats_running = False
        self.root.destroy()

    def run(self):
        self._start_stats()
        self.root.mainloop()


def main():
    hud = KalmiyaHUD()
    hud.run()

if __name__ == "__main__":
    main()
