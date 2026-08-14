"""
kalmiya_chat_optimized.py — Chat KALMIYA Optimizado
====================================================
Versión ligera del diseño futurista con avatar robótico.
Tamaño: 500x700 px (más pequeño que v2 pero más grande que v1)
RAM: ~120 MB (optimizado)

Balance perfecto entre diseño y rendimiento.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas
import threading
import time
import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False

try:
    from brain import ask_kalmiya, get_engine_status
    BRAIN_OK = True
except Exception:
    BRAIN_OK = False
    def ask_kalmiya(q: str, **kwargs) -> str: return "[brain.py no disponible]"
    def get_engine_status() -> dict: return {}

from decouple import config
USERNAME = config('USER', default='Sara')
BOTNAME = config('BOTNAME', default='KALMIYA')

# ── Configuración Visual Optimizada ────────────────────────────────────────────
ctk.set_appearance_mode("dark")

# Paleta optimizada (menos colores = mejor rendimiento)
BG_DARK        = "#0a0e1a"
BG_CARD        = "#0f1624"
BG_INPUT       = "#131b2e"
ACCENT_CYAN    = "#00d9ff"
ACCENT_PINK    = "#ff6ec7"
TEXT_WHITE     = "#ffffff"
TEXT_GRAY      = "#8b9ab5"
SUCCESS        = "#00ff88"

# Colores del avatar (simplificados)
ROBOT_WHITE    = "#f5f5f5"
ROBOT_PINK     = "#ffb6d9"
ROBOT_CYAN     = "#00d9ff"
ROBOT_DARK     = "#2a2a2a"

# Tamaño optimizado (más pequeño que v2)
CHAT_W = 500
CHAT_H = 700


class KalmiyaChatOptimized:
    """Chat KALMIYA optimizado - Balance diseño/rendimiento"""
    
    def __init__(self):
        self._drag_x = 0
        self._drag_y = 0
        self._thinking = False
        self._running = True
        self._build_window()
    
    def _build_window(self):
        self.root = ctk.CTk()
        self.root.title(f"{BOTNAME} AI")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.97)
        self.root.configure(fg_color=BG_DARK)
        
        # Posicionar a la derecha (como v1)
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = sw - CHAT_W - 20
        y = (sh - CHAT_H) // 2
        self.root.geometry(f"{CHAT_W}x{CHAT_H}+{x}+{y}")
        
        # Layout
        self._build_header()
        self._build_avatar_compact()
        self._build_chat_section()
        self._build_input_section()
        self._build_footer()
        
        self._make_draggable()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _build_header(self):
        """Header compacto"""
        header = ctk.CTkFrame(self.root, fg_color="transparent", height=50)
        header.pack(fill="x", padx=15, pady=(10, 0))
        
        # Título
        ctk.CTkLabel(
            header,
            text=f"🤖 {BOTNAME}",
            font=ctk.CTkFont("Segoe UI", 18, "bold"),
            text_color=ACCENT_CYAN
        ).pack(side="left")
        
        # Status
        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.pack(side="right")
        
        self.status_canvas = Canvas(
            status_frame,
            width=10,
            height=10,
            bg=BG_DARK,
            highlightthickness=0
        )
        self.status_canvas.pack(side="left", padx=3)
        self.status_canvas.create_oval(1, 1, 9, 9, fill=SUCCESS, outline="")
        
        ctk.CTkLabel(
            status_frame,
            text="ONLINE",
            font=ctk.CTkFont("Segoe UI", 9),
            text_color=SUCCESS
        ).pack(side="left", padx=3)
        
        # Botones
        ctk.CTkButton(
            status_frame,
            text="─",
            width=25,
            height=25,
            fg_color=BG_CARD,
            hover_color=BG_INPUT,
            command=self._minimize
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            status_frame,
            text="✕",
            width=25,
            height=25,
            fg_color=BG_CARD,
            hover_color="#ff3333",
            command=self._on_close
        ).pack(side="left", padx=1)
    
    def _build_avatar_compact(self):
        """Avatar compacto con saludo"""
        container = ctk.CTkFrame(
            self.root,
            fg_color=BG_CARD,
            corner_radius=15,
            height=150
        )
        container.pack(fill="x", padx=15, pady=10)
        container.pack_propagate(False)
        
        # Avatar pequeño con tamaño correcto para el diseño
        self.avatar_canvas = Canvas(
            container,
            width=80,
            height=110,
            bg=BG_CARD,
            highlightthickness=0
        )
        self.avatar_canvas.pack(side="left", padx=15, pady=20)
        self._draw_mini_avatar()
        
        # Info
        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=10, pady=20)
        
        greeting = self._get_greeting()
        
        # Título con emoji animado
        title_text = f"👋 {greeting}, {USERNAME}!"
        ctk.CTkLabel(
            info,
            text=title_text,
            font=ctk.CTkFont("Segoe UI", 16, "bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        ).pack(anchor="w", pady=(0, 3))
        
        # Mensaje amigable aleatorio
        friendly_messages = [
            "🌟 ¡Estoy aquí para ayudarte!",
            "✨ ¿En qué puedo asistirte hoy?",
            "💜 ¡Lista para ayudarte!",
            "🚀 ¿Qué vamos a hacer hoy?",
            "😊 ¡Cuéntame, en qué te ayudo!"
        ]
        import random
        friendly_msg = random.choice(friendly_messages)
        
        ctk.CTkLabel(
            info,
            text=friendly_msg,
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_GRAY,
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        # Stats mini (opcional, solo si psutil existe)
        if PSUTIL_OK:
            stats_line = ctk.CTkLabel(
                info,
                text="CPU: ... | RAM: ... | Disco: ...",
                font=ctk.CTkFont("Segoe UI", 9),
                text_color=TEXT_GRAY,
                anchor="w"
            )
            stats_line.pack(anchor="w")
            self.stats_label = stats_line
            threading.Thread(target=self._update_stats_mini, daemon=True).start()
    
    def _draw_mini_avatar(self):
        """Avatar robótico kawaii estilo tercera imagen - Saludando animadamente"""
        c = self.avatar_canvas
        
        # ===== OREJAS LARGAS TIPO CONEJO (como la imagen) =====
        # Oreja izquierda larga y vertical
        c.create_oval(8, 0, 20, 32, fill=ROBOT_WHITE, outline=ROBOT_DARK, width=2)
        c.create_oval(10, 8, 18, 28, fill=ROBOT_PINK, outline="")
        
        # Oreja derecha larga y vertical
        c.create_oval(60, 0, 72, 32, fill=ROBOT_WHITE, outline=ROBOT_DARK, width=2)
        c.create_oval(62, 8, 70, 28, fill=ROBOT_PINK, outline="")
        
        # ===== CABEZA GRANDE Y EXPRESIVA =====
        c.create_oval(18, 22, 62, 58, fill=ROBOT_WHITE, outline=ROBOT_DARK, width=2)
        
        # Detalles faciales decorativos rosas (líneas en la frente)
        c.create_line(26, 28, 32, 32, fill=ROBOT_PINK, width=2, smooth=True)
        c.create_line(48, 32, 54, 28, fill=ROBOT_PINK, width=2, smooth=True)
        
        # ===== OJOS MUY GRANDES ESTILO ANIME =====
        # Ojo izquierdo - mucho más grande
        c.create_oval(24, 32, 40, 48, fill=ROBOT_CYAN, outline="")
        # Brillos múltiples (más kawaii)
        c.create_oval(27, 34, 37, 44, fill="#80e0ff", outline="")
        c.create_oval(29, 36, 35, 42, fill="#ffffff", outline="")
        c.create_oval(31, 37, 33, 40, fill="#ffffff", outline="")
        
        # Ojo derecho - mucho más grande
        c.create_oval(40, 32, 56, 48, fill=ROBOT_CYAN, outline="")
        # Brillos múltiples
        c.create_oval(43, 34, 53, 44, fill="#80e0ff", outline="")
        c.create_oval(45, 36, 51, 42, fill="#ffffff", outline="")
        c.create_oval(47, 37, 49, 40, fill="#ffffff", outline="")
        
        # ===== BOCA SONRIENTE Y EXPRESIVA =====
        c.create_arc(28, 42, 52, 56, start=200, extent=140, outline=ROBOT_PINK, width=3, style="arc")
        
        # ===== RUBOR EN MEJILLAS (super kawaii) =====
        c.create_oval(19, 42, 26, 48, fill=ROBOT_PINK, outline="", stipple="gray50")
        c.create_oval(54, 42, 61, 48, fill=ROBOT_PINK, outline="", stipple="gray50")
        
        # ===== CUELLO =====
        c.create_rectangle(34, 56, 46, 62, fill=ROBOT_DARK, outline="")
        
        # ===== TORSO REDONDEADO =====
        c.create_oval(22, 58, 58, 82, fill=ROBOT_WHITE, outline=ROBOT_DARK, width=2)
        
        # Detalles rosas en hombros (articulaciones)
        c.create_oval(20, 62, 28, 70, fill=ROBOT_PINK, outline=ROBOT_DARK, width=1)
        c.create_oval(52, 62, 60, 70, fill=ROBOT_PINK, outline=ROBOT_DARK, width=1)
        
        # ===== CORE CENTRAL CON GLOW =====
        c.create_oval(32, 66, 48, 78, fill=ROBOT_DARK, outline=ROBOT_CYAN, width=2)
        c.create_oval(35, 69, 45, 75, fill=ROBOT_CYAN, outline="")
        c.create_oval(37, 70, 42, 74, fill="#ffffff", outline="")
        
        # ===== CORAZÓN ROSA GRANDE (muy visible) =====
        # Corazón compuesto
        c.create_oval(36, 76, 44, 84, fill=ROBOT_PINK, outline="")
        c.create_polygon(36, 80, 40, 86, 44, 80, fill=ROBOT_PINK, outline="", smooth=True)
        
        # ===== BRAZOS LEVANTADOS SALUDANDO (como en la imagen) =====
        # Brazo izquierdo levantado y curvo
        c.create_line(24, 64, 14, 56, 10, 50, fill=ROBOT_WHITE, width=7, capstyle="round", smooth=True)
        # Mano/articulación
        c.create_oval(7, 47, 13, 53, fill=ROBOT_WHITE, outline=ROBOT_DARK, width=2)
        c.create_oval(8, 48, 12, 52, fill=ROBOT_PINK, outline="")
        
        # Brazo derecho levantado y curvo
        c.create_line(56, 64, 66, 56, 70, 50, fill=ROBOT_WHITE, width=7, capstyle="round", smooth=True)
        # Mano/articulación
        c.create_oval(67, 47, 73, 53, fill=ROBOT_WHITE, outline=ROBOT_DARK, width=2)
        c.create_oval(68, 48, 72, 52, fill=ROBOT_PINK, outline="")
        
        # ===== PIERNAS REDONDEADAS =====
        c.create_rectangle(26, 80, 35, 92, fill=ROBOT_WHITE, outline=ROBOT_DARK, width=1)
        c.create_rectangle(45, 80, 54, 92, fill=ROBOT_WHITE, outline=ROBOT_DARK, width=1)
        
        # Articulaciones rosas en rodillas
        c.create_oval(28, 84, 33, 89, fill=ROBOT_PINK, outline="")
        c.create_oval(47, 84, 52, 89, fill=ROBOT_PINK, outline="")
        
        # ===== PIES/ZAPATOS ROSAS GRANDES (como la imagen) =====
        c.create_oval(22, 88, 38, 98, fill=ROBOT_PINK, outline=ROBOT_DARK, width=2)
        c.create_oval(42, 88, 58, 98, fill=ROBOT_PINK, outline=ROBOT_DARK, width=2)
        
        # Brillos en los zapatos
        c.create_oval(26, 90, 31, 94, fill="#ffffff", outline="", stipple="gray50")
        c.create_oval(46, 90, 51, 94, fill="#ffffff", outline="", stipple="gray50")
    
    def _build_chat_section(self):
        """Sección de chat optimizada"""
        # Header simple
        chat_header = ctk.CTkFrame(self.root, fg_color="transparent", height=35)
        chat_header.pack(fill="x", padx=15, pady=(5, 5))
        
        ctk.CTkLabel(
            chat_header,
            text="💬 Chat",
            font=ctk.CTkFont("Segoe UI", 12, "bold"),
            text_color=TEXT_WHITE
        ).pack(side="left")
        
        ctk.CTkButton(
            chat_header,
            text="🗑️",
            width=30,
            height=25,
            fg_color=BG_CARD,
            hover_color=BG_INPUT,
            command=self._clear_chat
        ).pack(side="right")
        
        # Container
        self.chat_container = ctk.CTkFrame(
            self.root,
            fg_color=BG_CARD,
            corner_radius=15
        )
        self.chat_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        # Scrollable frame
        self.chat_frame = ctk.CTkScrollableFrame(
            self.chat_container,
            fg_color="transparent",
            scrollbar_button_color=ACCENT_CYAN
        )
        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mensaje inicial animado y expresivo
        welcome_messages = [
            f"¡Hola {USERNAME}! 👋 Soy {BOTNAME}, tu asistente personal. Estoy aquí para ayudarte en lo que necesites. ¿Qué te gustaría hacer hoy? 😊",
            f"¡Bienvenida {USERNAME}! 🌟 Soy {BOTNAME} y estoy lista para asistirte. Pregúntame lo que quieras, ¡estoy aquí para ti! 💜",
            f"¡Hey {USERNAME}! 🚀 {BOTNAME} a tu servicio. ¿En qué aventura te puedo ayudar hoy? ¡Conversemos! ✨"
        ]
        import random
        welcome = random.choice(welcome_messages)
        self._add_message(BOTNAME, welcome, is_bot=True)
    
    def _build_input_section(self):
        """Input optimizado"""
        input_container = ctk.CTkFrame(
            self.root,
            fg_color=BG_INPUT,
            corner_radius=20,
            height=60
        )
        input_container.pack(fill="x", padx=15, pady=(0, 10))
        input_container.pack_propagate(False)
        
        self.input_var = tk.StringVar()
        self.entry = ctk.CTkEntry(
            input_container,
            textvariable=self.input_var,
            placeholder_text="Escribe aquí...",
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color="transparent",
            border_width=0
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        self.entry.bind("<Return>", lambda e: self._send_message())
        
        self.send_btn = ctk.CTkButton(
            input_container,
            text="➤",
            width=40,
            height=40,
            fg_color=ACCENT_CYAN,
            hover_color=ACCENT_PINK,
            font=ctk.CTkFont("Segoe UI", 16, "bold"),
            corner_radius=20,
            command=self._send_message
        )
        self.send_btn.pack(side="right", padx=10, pady=10)
    
    def _build_footer(self):
        """Footer simple"""
        footer = ctk.CTkFrame(self.root, fg_color="transparent", height=25)
        footer.pack(fill="x", padx=15, pady=(0, 10))
        
        status = get_engine_status() if BRAIN_OK else {}
        engine = status.get('engine', 'local')
        
        ctk.CTkLabel(
            footer,
            text=f"Motor: {engine.upper()} • v3.6",
            font=ctk.CTkFont("Segoe UI", 9),
            text_color=TEXT_GRAY
        ).pack(side="left")
        
        ctk.CTkLabel(
            footer,
            text=datetime.now().strftime("%H:%M"),
            font=ctk.CTkFont("Segoe UI", 9),
            text_color=TEXT_GRAY
        ).pack(side="right")
    
    def _add_message(self, sender, text, is_bot=False):
        """Agrega mensaje optimizado (sin avatar pesado)"""
        msg_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_frame.pack(fill="x", pady=5, anchor="w" if is_bot else "e")
        
        # Bubble
        bubble_color = BG_INPUT if is_bot else ACCENT_CYAN
        text_color = TEXT_WHITE
        
        bubble = ctk.CTkFrame(
            msg_frame,
            fg_color=bubble_color,
            corner_radius=12
        )
        bubble.pack(side="left" if is_bot else "right", fill="x", 
                   expand=True if is_bot else False, padx=(0 if is_bot else 40, 40 if is_bot else 0))
        
        # Emoji pequeño en vez de avatar grande
        if is_bot:
            ctk.CTkLabel(
                bubble,
                text=f"🤖 {sender}",
                font=ctk.CTkFont("Segoe UI", 10, "bold"),
                text_color=ACCENT_CYAN,
                anchor="w"
            ).pack(anchor="w", padx=12, pady=(8, 2))
        
        # Texto
        ctk.CTkLabel(
            bubble,
            text=text,
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=text_color,
            wraplength=350,
            justify="left" if is_bot else "right",
            anchor="w" if is_bot else "e"
        ).pack(anchor="w" if is_bot else "e", padx=12, pady=(2 if is_bot else 8, 8))
        
        # Auto scroll
        self.root.after(50, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))
    
    def _send_message(self):
        """Envía mensaje"""
        text = self.input_var.get().strip()
        if not text or self._thinking:
            return
        
        self.input_var.set("")
        self._add_message(USERNAME, text, is_bot=False)
        self._set_thinking(True)
        threading.Thread(target=self._process_message, args=(text,), daemon=True).start()
    
    def _process_message(self, text):
        """Procesa mensaje"""
        try:
            response = ask_kalmiya(text) if BRAIN_OK else "Sistema IA no disponible"
        except Exception as e:
            response = f"Error: {str(e)}"
        
        self.root.after(0, self._on_response, response)
    
    def _on_response(self, response):
        """Recibe respuesta con reacción amigable"""
        self._set_thinking(False)
        
        # Agregar emoji al inicio según el tipo de respuesta (opcional)
        if len(response) < 50:
            # Respuesta corta - más casual
            response = f"💭 {response}"
        elif "error" in response.lower() or "no disponible" in response.lower():
            response = f"⚠️ {response}"
        
        self._add_message(BOTNAME, response, is_bot=True)
    
    def _set_thinking(self, thinking):
        """Estado de pensando"""
        self._thinking = thinking
        self.entry.configure(state="disabled" if thinking else "normal")
        self.send_btn.configure(
            fg_color=BG_CARD if thinking else ACCENT_CYAN,
            text="..." if thinking else "➤"
        )
    
    def _clear_chat(self):
        """Limpia chat con mensaje expresivo"""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        
        clear_messages = [
            "✨ ¡Chat limpiado! Empecemos de nuevo. ¿En qué te ayudo?",
            "🗑️ ¡Listo! Chat limpio y fresco. ¿Qué hacemos ahora?",
            "💫 Chat reiniciado. ¡Conversemos! ¿Qué necesitas?",
            "🌟 ¡Perfecto! Espacio limpio. ¿Cuál es tu siguiente pregunta?"
        ]
        import random
        msg = random.choice(clear_messages)
        self._add_message(BOTNAME, msg, is_bot=True)
    
    def _update_stats_mini(self):
        """Actualiza stats en línea"""
        while self._running:
            try:
                cpu = psutil.cpu_percent(interval=1)
                ram = psutil.virtual_memory().percent
                disk = psutil.disk_usage('C:\\' if sys.platform == 'win32' else '/').percent
                
                text = f"CPU: {cpu:.0f}% | RAM: {ram:.0f}% | Disco: {disk:.0f}%"
                self.root.after(0, lambda: self.stats_label.configure(text=text))
            except:
                pass
            time.sleep(3)
    
    def _get_greeting(self):
        """Saludo expresivo según hora"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            greetings = ["Buenos días", "¡Buenos días!", "Buen día", "¡Hola! Buenos días"]
        elif 12 <= hour < 19:
            greetings = ["Buenas tardes", "¡Buenas tardes!", "Buena tarde", "¡Hola! Buenas tardes"]
        else:
            greetings = ["Buenas noches", "¡Buenas noches!", "Buena noche", "¡Hola! Buenas noches"]
        
        import random
        return random.choice(greetings)
    
    def _make_draggable(self):
        """Ventana arrastrable"""
        self.root.bind("<ButtonPress-1>", self._drag_start)
        self.root.bind("<B1-Motion>", self._drag_move)
    
    def _drag_start(self, e):
        self._drag_x, self._drag_y = e.x, e.y
    
    def _drag_move(self, e):
        x = self.root.winfo_x() + (e.x - self._drag_x)
        y = self.root.winfo_y() + (e.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")
    
    def _minimize(self):
        """Minimiza"""
        self.root.overrideredirect(False)
        self.root.iconify()
        self.root.after(500, lambda: self.root.overrideredirect(True))
    
    def _on_close(self):
        """Cierra"""
        self._running = False
        self.root.destroy()
    
    def run(self):
        """Inicia"""
        self.root.mainloop()


def main():
    """Función main"""
    chat = KalmiyaChatOptimized()
    chat.run()


if __name__ == "__main__":
    main()
