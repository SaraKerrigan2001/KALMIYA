"""
kalmiya_hud.py - HUD Rediseñado v3.5 (Nexus Aesthetic)
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from brain import ask_kalmiya, get_engine_status
    BRAIN_OK = True
except Exception as e:
    BRAIN_OK = False
    def ask_kalmiya(q: str, **kwargs) -> str: return "[brain.py no disponible]"
    def get_engine_status() -> dict: return {}

try:
    from voz import speak
    VOZ_OK = True
except Exception:
    VOZ_OK = False
    def speak(text: str):
        print(f"[KALMIYA - MUDO]: {text}")

# ── Configuración Visual ───────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")

BG_MAIN      = "#050510"
BG_SECONDARY = "#0a0a1a"
BG_CARD      = "#020a15"
ACCENT       = "#00f2ff"
ACCENT_DIM   = "#004d55"
TEXT_WHITE   = "#ffffff"
TEXT_DIM     = "#888888"
SUCCESS      = "#00ff88"
WARNING      = "#ffaa00"
DANGER       = "#ff4444"

HUD_W = 320
HUD_H = 640

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
        self._pulse_state = True
        self._thinking = False
        self._network_ok = False
        self._net_check_counter = 0
        self._build_window()

    def _build_window(self):
        self.root = ctk.CTk()
        self.root.title("KALMIYA NEXUS HUD")
        self.root.geometry(f"{HUD_W}x{HUD_H}")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.95)
        self.root.configure(fg_color=BG_MAIN)
        
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{HUD_W}x{HUD_H}+{sw - HUD_W - 15}+{(sh - HUD_H)//2}")

        # Bordes decorativos
        self._build_glow_border()
        self._build_header()
        self._build_stats_section()
        self._build_chat_section()
        self._build_input_section()
        
        self._make_draggable()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_glow_border(self):
        self.canvas_bg = tk.Canvas(self.root, width=HUD_W, height=HUD_H, bg=BG_MAIN, highlightthickness=0)
        self.canvas_bg.place(x=0, y=0)
        # Línea superior de acento
        self.canvas_bg.create_line(10, 55, HUD_W-10, 55, fill=ACCENT_DIM, width=1)
        # Esquinas decorativas
        c = 15
        self.canvas_bg.create_line(2, 2, c, 2, fill=ACCENT, width=2)
        self.canvas_bg.create_line(2, 2, 2, c, fill=ACCENT, width=2)
        self.canvas_bg.create_line(HUD_W-2, 2, HUD_W-c, 2, fill=ACCENT, width=2)
        self.canvas_bg.create_line(HUD_W-2, 2, HUD_W-2, c, fill=ACCENT, width=2)

    def _build_header(self):
        header = ctk.CTkFrame(self.root, fg_color="transparent", height=50)
        header.place(x=10, y=5, width=HUD_W-20)
        
        ctk.CTkLabel(header, text="KALMIYA v3.5", font=ctk.CTkFont("Consolas", 15, "bold"),
                     text_color=ACCENT).pack(side="left", pady=10)
        
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right", pady=10)
        
        self.status_dot = tk.Canvas(btn_frame, width=8, height=8, bg=BG_MAIN, highlightthickness=0)
        self.status_dot.pack(side="left", padx=5)
        self._draw_status_dot(SUCCESS)
        
        ctk.CTkLabel(btn_frame, text="ONLINE", font=ctk.CTkFont("Consolas", 9, "bold"),
                     text_color=SUCCESS).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(btn_frame, text="--", width=24, height=24, fg_color="#111", 
                      hover_color=ACCENT_DIM, command=self._minimize).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="X", width=24, height=24, fg_color="#111",
                      hover_color="#500", command=self._on_close).pack(side="left")

    def _draw_status_dot(self, color):
        self.status_dot.delete("all")
        self.status_dot.create_oval(0, 0, 7, 7, fill=color, outline="")

    def _build_stats_section(self):
        section = ctk.CTkFrame(self.root, fg_color="transparent", width=HUD_W-20, height=180)
        section.place(x=10, y=60)
        
        # Etiquetas de la izquierda
        labels_frame = ctk.CTkFrame(section, fg_color="transparent")
        labels_frame.place(x=0, y=30)
        
        for i, lab in enumerate(["CPU:", "RAM:", "DISCO:"]):
            ctk.CTkLabel(labels_frame, text=lab, font=ctk.CTkFont("Consolas", 10),
                         text_color=TEXT_DIM).pack(pady=12, anchor="w")

        # Barras de la derecha
        self.bars_canvas = tk.Canvas(section, width=180, height=120, bg=BG_MAIN, highlightthickness=0)
        self.bars_canvas.place(x=50, y=30)
        self._cpu_val = 0
        self._ram_val = 0
        self._disk_val = 0

        # Clock Grande (derecha)
        self.clock_label = ctk.CTkLabel(section, text="00:00:00", font=ctk.CTkFont("Consolas", 26, "bold"),
                                        text_color=ACCENT)
        self.clock_label.place(x=HUD_W-160, y=100)
        
        self.date_label = ctk.CTkLabel(section, text="SAT 16 MAY 2026", font=ctk.CTkFont("Consolas", 9),
                                        text_color=TEXT_DIM)
        self.date_label.place(x=HUD_W-160, y=135)

        ctk.CTkLabel(section, text="ESTADO DEL SISTEMA", font=ctk.CTkFont("Consolas", 9, "bold"),
                     text_color=ACCENT_DIM).place(x=0, y=5)
        
        # Red
        self.net_label = ctk.CTkLabel(section, text="RED: ONLINE", font=ctk.CTkFont("Consolas", 10, "bold"),
                                      text_color=ACCENT)
        self.net_label.place(x=100, y=170)

        # Botón Boost (Nexus Style)
        self.boost_btn = ctk.CTkButton(self.root, text="NEXUS BOOST", width=100, height=20,
                                       font=ctk.CTkFont("Consolas", 9, "bold"),
                                       fg_color=ACCENT_DIM, hover_color=ACCENT, text_color=BG_MAIN,
                                       command=self._on_nexus_boost)
        self.boost_btn.place(x=10, y=245)

    def _draw_tech_bar(self, canvas, x, y, w, h, percent, color):
        canvas.create_rectangle(x, y, x+w, y+h, fill="#021a25", outline="")
        fill_w = (w * percent) / 100
        if fill_w > 5:
            # Forma trapezoidal al final como en la imagen
            pts = [x, y, x+fill_w-4, y, x+fill_w, y+h/2, x+fill_w-4, y+h, x, y+h]
            canvas.create_polygon(pts, fill=color, outline="")

    def _build_chat_section(self):
        self.chat_container = ctk.CTkFrame(self.root, fg_color=BG_CARD, corner_radius=5, border_width=1, border_color="#002233")
        self.chat_container.place(x=10, y=275, width=HUD_W-20, height=250)
        
        # Marca de agua "KALMIYA"
        self.watermark = tk.Canvas(self.chat_container, bg=BG_CARD, highlightthickness=0)
        self.watermark.place(x=0, y=0, relwidth=1, relheight=1)
        self.watermark.create_text(HUD_W/2-20, 125, text="KALMIYA", font=("Consolas", 40, "bold"), fill="#030f1a")

        self.chat_frame = ctk.CTkScrollableFrame(self.chat_container, fg_color="transparent", 
                                                 scrollbar_button_color=ACCENT_DIM)
        self.chat_frame.place(x=5, y=5, relwidth=0.96, relheight=0.96)
        
        ctk.CTkLabel(self.root, text="CANAL DE COMUNICACION", font=ctk.CTkFont("Consolas", 8, "bold"),
                     text_color=ACCENT_DIM).place(x=15, y=265)

    def _add_chat_message(self, role, text):
        is_k = role.upper() == "KALMIYA"
        p_color = ACCENT if is_k else WARNING
        t_color = TEXT_WHITE if not is_k else ACCENT
        
        f = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        f.pack(fill="x", pady=4)
        ctk.CTkLabel(f, text=f"[{role.upper()}]", font=ctk.CTkFont("Consolas", 8, "bold"),
                     text_color=p_color).pack(anchor="w")
        ctk.CTkLabel(f, text=text, font=ctk.CTkFont("Consolas", 10), text_color=t_color,
                     wraplength=240, justify="left").pack(anchor="w", padx=10)
        self.root.after(100, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    def _build_input_section(self):
        container = ctk.CTkFrame(self.root, fg_color=BG_SECONDARY, height=80, corner_radius=5)
        container.place(x=10, y=540, width=HUD_W-20)
        
        ctk.CTkLabel(container, text="ENTRADA", font=ctk.CTkFont("Consolas", 9, "bold"),
                     text_color=ACCENT_DIM).place(x=10, y=5)
        
        self.input_var = tk.StringVar()
        self.entry = ctk.CTkEntry(container, textvariable=self.input_var, placeholder_text="Sync message...",
                                  font=ctk.CTkFont("Consolas", 11), fg_color=BG_MAIN, border_color=ACCENT_DIM)
        self.entry.place(x=10, y=28, width=HUD_W-80, height=35)
        self.entry.bind("<Return>", self._on_send)
        
        self.send_btn = ctk.CTkButton(container, text=">", width=40, height=35, fg_color=ACCENT_DIM,
                                      hover_color=ACCENT, text_color=BG_MAIN, command=self._on_send)
        self.send_btn.place(x=HUD_W-65, y=28)

    def _on_send(self, e=None):
        txt = self.input_var.get().strip()
        if not txt or self._thinking: return
        self.input_var.set("")
        self._add_chat_message("SARA", txt)
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
        self._add_chat_message("KALMIYA", res)
        # NO llamar a speak() — evita eco con el nucleo de voz

    def _set_thinking(self, b):
        self._thinking = b
        self.entry.configure(state="disabled" if b else "normal")
        self.send_btn.configure(fg_color="#222" if b else ACCENT_DIM)

    def _on_nexus_boost(self):
        self._add_chat_message("SARA", "[Ejecutando Nexus Boost]")
        self._set_thinking(True)
        threading.Thread(target=self._run_boost, daemon=True).start()

    def _run_boost(self):
        try:
            from kalmiya_v35_features import smart_performance_boost
            res = smart_performance_boost()
            self.root.after(0, self._on_res, res)
        except: self.root.after(0, self._on_res, "Boost fallido.")

    def _start_stats(self):
        self._stats_running = True
        threading.Thread(target=self._stats_loop, daemon=True).start()
        self._pulse()

    def _stats_loop(self):
        while self._stats_running:
            if PSUTIL_OK:
                self._cpu_val = psutil.cpu_percent(interval=1)
                self._ram_val = psutil.virtual_memory().percent
                self._disk_val = psutil.disk_usage('C:\\').percent if sys.platform == "win32" else psutil.disk_usage('/').percent
            self._net_check_counter += 1
            if self._net_check_counter >= 5:
                self._network_ok = _check_network()
                self._net_check_counter = 0
            self.root.after(0, self._upd_ui)
            time.sleep(1)

    def _upd_ui(self):
        self.bars_canvas.delete("all")
        self._draw_tech_bar(self.bars_canvas, 10, 15, 140, 10, self._cpu_val, ACCENT)
        self._draw_tech_bar(self.bars_canvas, 10, 50, 140, 10, self._ram_val, ACCENT)
        self._draw_tech_bar(self.bars_canvas, 10, 85, 140, 10, self._disk_val, ACCENT)
        
        now = datetime.now()
        self.clock_label.configure(text=now.strftime("%H:%M:%S"))
        self.date_label.configure(text=now.strftime("%a %d %b %Y").upper())
        self.net_label.configure(text="RED: ONLINE" if self._network_ok else "RED: OFFLINE", 
                                 text_color=SUCCESS if self._network_ok else DANGER)

    def _pulse(self):
        if not self._stats_running: return
        self._draw_status_dot(SUCCESS if self._pulse_state else "#004422")
        self._pulse_state = not self._pulse_state
        self.root.after(1000, self._pulse)

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
    """Función main para importación desde wrapper"""
    hud = KalmiyaHUD()
    hud.run()


if __name__ == "__main__":
    main()
