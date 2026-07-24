"""
splash_screen.py - Pantalla de arranque de KALMIYA
Pantalla de inicio estilo terminal militar con animacion de boot.
"""

import tkinter as tk
import threading
import time
import sys
import os
from typing import Optional

BG_COLOR      = "#000000"
ACCENT_COLOR  = "#00f2ff"
DIM_COLOR     = "#004d55"
SUCCESS_COLOR = "#00ff88"
WARNING_COLOR = "#ffaa00"
TEXT_COLOR    = "#ccffff"
FONT_MAIN     = ("Consolas", 11)
FONT_LOGO     = ("Consolas", 36, "bold")
FONT_SMALL    = ("Consolas", 9)
FONT_STATUS   = ("Consolas", 10)

BOOT_LINES: list[tuple[str, str, float]] = [
    ("KALMIYA NEURAL CORE v3.5 - INICIALIZANDO", ACCENT_COLOR, 0.15),
    ("", TEXT_COLOR, 0.05),
    ("[SYS]  Verificando integridad del nucleo...", TEXT_COLOR, 0.20),
    ("[SYS]  Nucleo verificado. OK", SUCCESS_COLOR, 0.15),
    ("[MEM]  Cargando modulos de inteligencia...", TEXT_COLOR, 0.25),
    ("[MEM]  Modulos cargados: 12/12", SUCCESS_COLOR, 0.15),
    ("[NET]  Estableciendo conexion segura...", TEXT_COLOR, 0.20),
    ("[NET]  Canal cifrado activo. OK", SUCCESS_COLOR, 0.15),
    ("[VOZ]  Inicializando sintetizador neural...", TEXT_COLOR, 0.20),
    ("[VOZ]  Motor de voz: es-ES-ElviraNeural", SUCCESS_COLOR, 0.15),
    ("[IA]   Conectando con motores de IA...", TEXT_COLOR, 0.25),
    ("[IA]   Gemini 2.5 Flash: DISPONIBLE", SUCCESS_COLOR, 0.15),
    ("[DB]   Cargando memoria persistente...", TEXT_COLOR, 0.20),
    ("[DB]   Base de datos: ONLINE", SUCCESS_COLOR, 0.15),
    ("", TEXT_COLOR, 0.05),
    ("[AUTH] Verificando usuario autorizado...", WARNING_COLOR, 0.30),
    ("[AUTH] SARA KERRIGAN - ACCESO CONCEDIDO", SUCCESS_COLOR, 0.20),
    ("", TEXT_COLOR, 0.05),
    ("Todos los sistemas operativos al 100%.", ACCENT_COLOR, 0.10),
    ("Bienvenida, Sara.", ACCENT_COLOR, 0.15),
]


class SplashScreen:
    def __init__(self, on_complete_callback: Optional[callable] = None):
        self.on_complete = on_complete_callback
        self._pulse_running = False
        self._progress = 0.0
        self._text_widgets: list[tk.Label] = []
        self._build_window()

    def _build_window(self):
        self.root = tk.Tk()
        self.root.title("KALMIYA")
        self.root.configure(bg=BG_COLOR)
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self._build_canvas_bg()
        self._build_logo()
        self._build_terminal_area()
        self._build_progress_bar()
        self._build_footer()
        self.root.bind("<Escape>", lambda e: self._finish())

    def _build_canvas_bg(self):
        self.canvas = tk.Canvas(self.root, width=self.screen_w, height=self.screen_h,
                                bg=BG_COLOR, highlightthickness=0)
        self.canvas.place(x=0, y=0)
        grid_color = "#050510"
        for x in range(0, self.screen_w, 60):
            self.canvas.create_line(x, 0, x, self.screen_h, fill=grid_color, width=1)
        for y in range(0, self.screen_h, 60):
            self.canvas.create_line(0, y, self.screen_w, y, fill=grid_color, width=1)
        self.canvas.create_line(40, 80, self.screen_w - 40, 80, fill=DIM_COLOR, width=1, dash=(4, 8))
        self.canvas.create_line(40, self.screen_h - 80, self.screen_w - 40, self.screen_h - 80,
                                fill=DIM_COLOR, width=1, dash=(4, 8))
        c = 30
        for (x1, y1, x2, y2, x3, y3) in [
            (40, 40, 40 + c, 40, 40, 40 + c),
            (self.screen_w - 40, 40, self.screen_w - 40 - c, 40, self.screen_w - 40, 40 + c),
            (40, self.screen_h - 40, 40 + c, self.screen_h - 40, 40, self.screen_h - 40 - c),
            (self.screen_w - 40, self.screen_h - 40, self.screen_w - 40 - c, self.screen_h - 40,
             self.screen_w - 40, self.screen_h - 40 - c),
        ]:
            self.canvas.create_line(x1, y1, x2, y2, fill=ACCENT_COLOR, width=2)
            self.canvas.create_line(x1, y1, x3, y3, fill=ACCENT_COLOR, width=2)

    def _build_logo(self):
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.place(relx=0.5, rely=0.18, anchor="center")
        self.logo_label = tk.Label(frame, text="K A L M I Y A", font=FONT_LOGO,
                                   fg=ACCENT_COLOR, bg=BG_COLOR)
        self.logo_label.pack()
        tk.Label(frame, text="NEURAL INTELLIGENCE SYSTEM  v3.5", font=("Consolas", 12),
                 fg=DIM_COLOR, bg=BG_COLOR).pack(pady=(4, 0))
        sep = tk.Canvas(frame, width=500, height=2, bg=BG_COLOR, highlightthickness=0)
        sep.pack(pady=(12, 0))
        sep.create_line(0, 1, 500, 1, fill=ACCENT_COLOR, width=1)

    def _build_terminal_area(self):
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.place(relx=0.5, rely=0.52, anchor="center",
                    width=min(900, self.screen_w - 120), height=320)
        border = tk.Canvas(frame, bg=BG_COLOR, highlightthickness=1, highlightbackground=DIM_COLOR)
        border.pack(fill="both", expand=True)
        tk.Label(border, text="  KALMIYA BOOT SEQUENCE - SECURE CHANNEL",
                 font=FONT_SMALL, fg=DIM_COLOR, bg="#020208", anchor="w", pady=4).pack(fill="x")
        self.terminal_inner = tk.Frame(border, bg=BG_COLOR)
        self.terminal_inner.pack(fill="both", expand=True, padx=12, pady=8)

    def _build_progress_bar(self):
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.place(relx=0.5, rely=0.80, anchor="center", width=min(900, self.screen_w - 120))
        self.status_label = tk.Label(frame, text="Iniciando...", font=FONT_STATUS,
                                     fg=DIM_COLOR, bg=BG_COLOR, anchor="w")
        self.status_label.pack(fill="x", pady=(0, 6))
        self.progress_canvas = tk.Canvas(frame, height=18, bg="#020208",
                                         highlightthickness=1, highlightbackground=DIM_COLOR)
        self.progress_canvas.pack(fill="x")
        self._draw_progress(0.0)
        self.percent_label = tk.Label(frame, text="0%", font=FONT_SMALL,
                                      fg=ACCENT_COLOR, bg=BG_COLOR, anchor="e")
        self.percent_label.pack(fill="x", pady=(4, 0))

    def _build_footer(self):
        tk.Label(self.root, text="SARA KERRIGAN - USUARIO AUTORIZADO  SISTEMA CLASIFICADO",
                 font=FONT_SMALL, fg=DIM_COLOR, bg=BG_COLOR).place(relx=0.5, rely=0.96, anchor="center")

    def _draw_progress(self, fraction: float):
        self.progress_canvas.update_idletasks()
        w = self.progress_canvas.winfo_width()
        h = self.progress_canvas.winfo_height()
        if w < 2:
            w = 860
        fill_w = int(w * fraction)
        self.progress_canvas.delete("all")
        self.progress_canvas.create_rectangle(0, 0, w, h, fill="#020208", outline="")
        if fill_w > 0:
            self.progress_canvas.create_rectangle(0, 0, fill_w, h, fill=ACCENT_COLOR, outline="")
            glow_x = max(0, fill_w - 4)
            self.progress_canvas.create_rectangle(glow_x, 0, fill_w, h, fill="#80f8ff", outline="")

    def _animate_progress(self, target: float, steps: int = 20, delay: float = 0.02):
        current = self._progress
        delta = (target - current) / max(steps, 1)
        def step(i: int):
            if i >= steps:
                self._progress = target
                self._draw_progress(target)
                self.percent_label.config(text=f"{int(target * 100)}%")
                return
            self._progress += delta
            self._draw_progress(self._progress)
            self.percent_label.config(text=f"{int(self._progress * 100)}%")
            self.root.after(int(delay * 1000), lambda: step(i + 1))
        step(0)

    def _start_logo_pulse(self):
        self._pulse_running = True
        self._pulse_colors = self._generate_pulse_colors()
        self._pulse_index = 0
        self._do_pulse()

    def _generate_pulse_colors(self) -> list[str]:
        colors = []
        steps = 30
        for i in range(steps):
            t = i / steps
            g = int(80 + t * (242 - 80))
            b = int(100 + t * (255 - 100))
            colors.append(f"#00{g:02x}{b:02x}")
        for i in range(steps):
            t = i / steps
            g = int(242 - t * (242 - 80))
            b = int(255 - t * (255 - 100))
            colors.append(f"#00{g:02x}{b:02x}")
        return colors

    def _do_pulse(self):
        if not self._pulse_running:
            return
        try:
            color = self._pulse_colors[self._pulse_index]
            self.logo_label.config(fg=color)
            self._pulse_index = (self._pulse_index + 1) % len(self._pulse_colors)
            self.root.after(40, self._do_pulse)
        except Exception:
            pass

    def _add_boot_line(self, text: str, color: str):
        label = tk.Label(self.terminal_inner, text=text if text else " ",
                         font=FONT_MAIN, fg=color, bg=BG_COLOR, anchor="w", justify="left")
        label.pack(fill="x", pady=1)
        self._text_widgets.append(label)
        if len(self._text_widgets) > 14:
            old = self._text_widgets.pop(0)
            old.destroy()

    def _run_boot_sequence(self):
        total = len(BOOT_LINES)
        for i, (text, color, pause) in enumerate(BOOT_LINES):
            self.root.after(0, self._add_boot_line, text, color)
            self.root.after(0, self._animate_progress, (i + 1) / total)
            if text.strip():
                self.root.after(0, self.status_label.config, {"text": text[:60]})
            time.sleep(pause)
        time.sleep(0.5)
        self.root.after(0, self._on_boot_complete)

    def _on_boot_complete(self):
        self.status_label.config(text="Sistema listo.", fg=SUCCESS_COLOR)
        self._animate_progress(1.0)
        self.root.after(800, self._finish)

    def _finish(self):
        self._pulse_running = False
        try:
            self.root.destroy()
        except Exception:
            pass
        if self.on_complete:
            try:
                self.on_complete()
            except Exception as e:
                print(f"[SPLASH] Error en callback: {e}")

    def run(self):
        self._start_logo_pulse()
        threading.Thread(target=self._run_boot_sequence, daemon=True).start()
        self.root.mainloop()


if __name__ == "__main__":
    splash = SplashScreen()
    splash.run()
