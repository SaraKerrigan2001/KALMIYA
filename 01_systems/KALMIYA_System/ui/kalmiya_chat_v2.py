"""
kalmiya_chat_v2.py — Chat KALMIYA Rediseñado v3.6
===================================================
Diseño futurista tipo AI Assistant con avatar robótico.
Inspirado en interfaces modernas con glassmorphism y neón.
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
import math

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

# ── Configuración Visual Futurista ─────────────────────────────────────────────
ctk.set_appearance_mode("dark")

# Paleta inspirada en la imagen del AI Assistant
BG_DARK        = "#0a0e1a"      # Fondo principal oscuro
BG_CARD        = "#0f1624"      # Fondo de tarjetas
BG_INPUT       = "#131b2e"      # Fondo de input
BG_GLASS       = "#1a2332"      # Efecto glassmorphism
ACCENT_BLUE    = "#00d9ff"      # Cyan neón principal
ACCENT_PURPLE  = "#b429f9"      # Púrpura para gradientes
ACCENT_PINK    = "#ff6ec7"      # Rosa para detalles kawaii
TEXT_WHITE     = "#ffffff"
TEXT_GRAY      = "#8b9ab5"
TEXT_DIM       = "#4a5568"
SUCCESS        = "#00ff88"
GLOW_COLOR     = "#00b8ff"

# Colores del avatar robótico
ROBOT_WHITE    = "#f0f0f0"
ROBOT_PINK     = "#ffb6d9"
ROBOT_BLUE     = "#00d9ff"
ROBOT_GRAY     = "#404040"

CHAT_W = 720
CHAT_H = 900


class KalmiyaChatV2:
    """Chat KALMIYA con diseño AI Assistant futurista"""
    
    def __init__(self):
        self._drag_x = 0
        self._drag_y = 0
        self._thinking = False
        self._pulse_state = True
        self._running = True
        self._anim_frame = 0
        self._avatar_breath = 0
        self._build_window()
    
    def _build_window(self):
        self.root = ctk.CTk()
        self.root.title(f"{BOTNAME} AI Assistant")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.97)
        self.root.configure(fg_color=BG_DARK)
        
        # Centrar ventana
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - CHAT_W) // 2
        y = (sh - CHAT_H) // 2
        self.root.geometry(f"{CHAT_W}x{CHAT_H}+{x}+{y}")
        
        # Layout principal
        self._build_header()
        self._build_avatar_section()
        self._build_stats_cards()
        self._build_chat_section()
        self._build_input_section()
        self._build_footer()
        
        self._make_draggable()
        self._start_animations()
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _build_header(self):
        """Header con título y controles"""
        header = ctk.CTkFrame(self.root, fg_color="transparent", height=60)
        header.pack(fill="x", padx=20, pady=(10, 0))
        
        # Título
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="y")
        
        ctk.CTkLabel(
            title_frame,
            text=f"{BOTNAME} AI",
            font=ctk.CTkFont("Segoe UI", 24, "bold"),
            text_color=ACCENT_BLUE
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Personal Assistant",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=TEXT_GRAY
        ).pack(anchor="w")
        
        # Controles derecha
        controls = ctk.CTkFrame(header, fg_color="transparent")
        controls.pack(side="right", fill="y")
        
        # Status indicator
        self.status_canvas = Canvas(
            controls,
            width=12,
            height=12,
            bg=BG_DARK,
            highlightthickness=0
        )
        self.status_canvas.pack(side="left", padx=5)
        self._draw_status_dot()
        
        ctk.CTkLabel(
            controls,
            text="ONLINE",
            font=ctk.CTkFont("Segoe UI", 10, "bold"),
            text_color=SUCCESS
        ).pack(side="left", padx=5)
        
        # Botones minimizar/cerrar
        btn_minimize = ctk.CTkButton(
            controls,
            text="─",
            width=30,
            height=30,
            fg_color=BG_GLASS,
            hover_color=BG_INPUT,
            command=self._minimize
        )
        btn_minimize.pack(side="left", padx=2)
        
        btn_close = ctk.CTkButton(
            controls,
            text="✕",
            width=30,
            height=30,
            fg_color=BG_GLASS,
            hover_color="#ff3333",
            command=self._on_close
        )
        btn_close.pack(side="left", padx=2)
    
    def _build_avatar_section(self):
        """Sección central con avatar robótico animado"""
        avatar_container = ctk.CTkFrame(
            self.root,
            fg_color=BG_CARD,
            corner_radius=20,
            height=220
        )
        avatar_container.pack(fill="x", padx=20, pady=15)
        avatar_container.pack_propagate(False)
        
        # Canvas para el avatar robótico
        self.avatar_canvas = Canvas(
            avatar_container,
            width=180,
            height=200,
            bg=BG_CARD,
            highlightthickness=0
        )
        self.avatar_canvas.pack(side="left", padx=30, pady=10)
        
        # Dibujar avatar robótico kawaii
        self._draw_robot_avatar()
        
        # Info derecha
        info_frame = ctk.CTkFrame(avatar_container, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        # Saludo
        greeting = self._get_greeting()
        ctk.CTkLabel(
            info_frame,
            text=f"{greeting}, {USERNAME}",
            font=ctk.CTkFont("Segoe UI", 22, "bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        ).pack(anchor="w", pady=(20, 5))
        
        ctk.CTkLabel(
            info_frame,
            text="¿En qué puedo ayudarte hoy?",
            font=ctk.CTkFont("Segoe UI", 14),
            text_color=TEXT_GRAY,
            anchor="w"
        ).pack(anchor="w", pady=(0, 15))
        
        # Wave indicator cuando está escuchando
        self.wave_canvas = Canvas(
            info_frame,
            width=280,
            height=40,
            bg=BG_CARD,
            highlightthickness=0
        )
        self.wave_canvas.pack(anchor="w", pady=10)
        self._draw_wave(idle=True)
        
        # Botón de voz
        self.voice_btn = ctk.CTkButton(
            info_frame,
            text="🎤 Pulsa para hablar",
            width=200,
            height=40,
            fg_color=ACCENT_BLUE,
            hover_color=ACCENT_PURPLE,
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            corner_radius=20,
            command=self._toggle_voice
        )
        self.voice_btn.pack(anchor="w")
    
    def _draw_robot_avatar(self):
        """Dibuja avatar robótico kawaii tipo la imagen"""
        c = self.avatar_canvas
        
        # Cuerpo principal (blanco)
        # Cabeza
        c.create_oval(50, 20, 130, 100, fill=ROBOT_WHITE, outline=ROBOT_GRAY, width=2)
        
        # Orejas/sensores (blanco con interior rosa)
        c.create_oval(25, 35, 55, 75, fill=ROBOT_WHITE, outline=ROBOT_GRAY, width=2)
        c.create_oval(125, 35, 155, 75, fill=ROBOT_WHITE, outline=ROBOT_GRAY, width=2)
        c.create_oval(30, 45, 50, 65, fill=ROBOT_PINK, outline="")
        c.create_oval(130, 45, 150, 65, fill=ROBOT_PINK, outline="")
        
        # Ojos grandes (azul cyan brillante)
        # Ojo izquierdo
        c.create_oval(60, 45, 85, 75, fill=ROBOT_BLUE, outline="")
        c.create_oval(67, 50, 78, 65, fill="#ffffff", outline="")  # Brillo
        c.create_oval(70, 53, 75, 60, fill="#ffffff", outline="")  # Brillo pequeño
        
        # Ojo derecho
        c.create_oval(95, 45, 120, 75, fill=ROBOT_BLUE, outline="")
        c.create_oval(102, 50, 113, 65, fill="#ffffff", outline="")
        c.create_oval(105, 53, 110, 60, fill="#ffffff", outline="")
        
        # Detalles faciales (líneas rosa)
        c.create_line(70, 35, 85, 42, fill=ROBOT_PINK, width=2)
        c.create_line(95, 42, 110, 35, fill=ROBOT_PINK, width=2)
        
        # Cuello
        c.create_rectangle(80, 95, 100, 110, fill=ROBOT_GRAY, outline="")
        
        # Torso
        c.create_rounded_rect(c, 50, 105, 130, 160, 15, fill=ROBOT_WHITE, outline=ROBOT_GRAY, width=2)
        
        # Core central (círculo negro con borde)
        c.create_oval(75, 120, 105, 150, fill=ROBOT_GRAY, outline=ROBOT_GRAY, width=2)
        c.create_oval(80, 125, 100, 145, fill="#1a1a1a", outline="")
        
        # Detalles rosas en el torso
        c.create_arc(60, 150, 75, 160, start=180, extent=180, fill=ROBOT_PINK, outline="")
        c.create_arc(105, 150, 120, 160, start=0, extent=180, fill=ROBOT_PINK, outline="")
        
        # Brazos simples
        c.create_rounded_rect(c, 30, 115, 48, 145, 5, fill=ROBOT_WHITE, outline=ROBOT_GRAY, width=1)
        c.create_rounded_rect(c, 132, 115, 150, 145, 5, fill=ROBOT_WHITE, outline=ROBOT_GRAY, width=1)
        
        # Manos (círculos pequeños)
        c.create_oval(25, 140, 35, 150, fill=ROBOT_WHITE, outline=ROBOT_GRAY, width=1)
        c.create_oval(145, 140, 155, 150, fill=ROBOT_WHITE, outline=ROBOT_GRAY, width=1)
        
        # Piernas
        c.create_rounded_rect(c, 60, 157, 78, 185, 5, fill=ROBOT_WHITE, outline=ROBOT_GRAY, width=1)
        c.create_rounded_rect(c, 102, 157, 120, 185, 5, fill=ROBOT_WHITE, outline=ROBOT_GRAY, width=1)
        
        # Pies (zapatos rosas)
        c.create_oval(55, 180, 80, 195, fill=ROBOT_PINK, outline=ROBOT_GRAY, width=1)
        c.create_oval(100, 180, 125, 195, fill=ROBOT_PINK, outline=ROBOT_GRAY, width=1)
    
    def _build_stats_cards(self):
        """Mini cards con stats del sistema"""
        stats_container = ctk.CTkFrame(self.root, fg_color="transparent")
        stats_container.pack(fill="x", padx=20, pady=(0, 10))
        
        # CPU Card
        self._create_stat_card(
            stats_container,
            "CPU",
            "0%",
            ACCENT_BLUE
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        # RAM Card
        self._create_stat_card(
            stats_container,
            "RAM",
            "0%",
            ACCENT_PURPLE
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        # Disco Card
        self._create_stat_card(
            stats_container,
            "DISCO",
            "0%",
            ACCENT_PINK
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        # Iniciar actualización de stats
        if PSUTIL_OK:
            threading.Thread(target=self._update_stats_loop, daemon=True).start()
    
    def _create_stat_card(self, parent, label, value, color):
        """Crea una mini card de estadística"""
        card = ctk.CTkFrame(
            parent,
            fg_color=BG_CARD,
            corner_radius=12,
            height=70
        )
        
        ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_GRAY
        ).pack(pady=(10, 0))
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont("Segoe UI", 20, "bold"),
            text_color=color
        )
        value_label.pack(pady=(0, 10))
        
        # Guardar referencia
        if label == "CPU":
            self.cpu_label = value_label
        elif label == "RAM":
            self.ram_label = value_label
        elif label == "DISCO":
            self.disk_label = value_label
        
        return card
    
    def _build_chat_section(self):
        """Sección de chat con mensajes"""
        # Header del chat
        chat_header = ctk.CTkFrame(self.root, fg_color="transparent", height=40)
        chat_header.pack(fill="x", padx=20, pady=(10, 5))
        
        ctk.CTkLabel(
            chat_header,
            text="💬 Conversación",
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            text_color=TEXT_WHITE
        ).pack(side="left")
        
        # Botón limpiar chat
        ctk.CTkButton(
            chat_header,
            text="🗑️ Limpiar",
            width=80,
            height=28,
            fg_color=BG_GLASS,
            hover_color=BG_INPUT,
            font=ctk.CTkFont("Segoe UI", 11),
            command=self._clear_chat
        ).pack(side="right")
        
        # Container del chat con glassmorphism
        self.chat_container = ctk.CTkFrame(
            self.root,
            fg_color=BG_CARD,
            corner_radius=15,
            border_width=1,
            border_color="#2a3544"
        )
        self.chat_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Scrollable frame para mensajes
        self.chat_frame = ctk.CTkScrollableFrame(
            self.chat_container,
            fg_color="transparent",
            scrollbar_button_color=ACCENT_BLUE,
            scrollbar_button_hover_color=ACCENT_PURPLE
        )
        self.chat_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Mensaje inicial
        self._add_message("KALMIYA", 
                         f"¡Hola {USERNAME}! 👋 Soy {BOTNAME}, tu asistente personal de IA. ¿En qué puedo ayudarte hoy?",
                         is_bot=True)
    
    def _build_input_section(self):
        """Sección de input con diseño futurista"""
        input_container = ctk.CTkFrame(
            self.root,
            fg_color=BG_INPUT,
            corner_radius=25,
            height=70
        )
        input_container.pack(fill="x", padx=20, pady=(0, 10))
        input_container.pack_propagate(False)
        
        # Input con placeholder
        self.input_var = tk.StringVar()
        self.entry = ctk.CTkEntry(
            input_container,
            textvariable=self.input_var,
            placeholder_text="Escribe tu mensaje aquí...",
            font=ctk.CTkFont("Segoe UI", 14),
            fg_color="transparent",
            border_width=0,
            height=50
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        self.entry.bind("<Return>", lambda e: self._send_message())
        
        # Botón enviar con efecto neón
        self.send_btn = ctk.CTkButton(
            input_container,
            text="➤",
            width=50,
            height=50,
            fg_color=ACCENT_BLUE,
            hover_color=ACCENT_PURPLE,
            font=ctk.CTkFont("Segoe UI", 20, "bold"),
            corner_radius=25,
            command=self._send_message
        )
        self.send_btn.pack(side="right", padx=10, pady=10)
    
    def _build_footer(self):
        """Footer con info adicional"""
        footer = ctk.CTkFrame(self.root, fg_color="transparent", height=30)
        footer.pack(fill="x", padx=20, pady=(0, 10))
        
        # Info del motor IA
        status = get_engine_status() if BRAIN_OK else {}
        engine = status.get('engine', 'local')
        
        ctk.CTkLabel(
            footer,
            text=f"🤖 Motor: {engine.upper()}",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=TEXT_DIM
        ).pack(side="left")
        
        ctk.CTkLabel(
            footer,
            text=f"v3.6 • {datetime.now().strftime('%H:%M')}",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=TEXT_DIM
        ).pack(side="right")
    
    def _add_message(self, sender, text, is_bot=False):
        """Agrega un mensaje al chat con diseño moderno"""
        # Frame del mensaje
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_container.pack(fill="x", pady=8, anchor="w" if is_bot else "e")
        
        # Avatar pequeño
        if is_bot:
            avatar_frame = ctk.CTkFrame(
                msg_container,
                width=35,
                height=35,
                fg_color=ACCENT_BLUE,
                corner_radius=17
            )
            avatar_frame.pack(side="left", padx=(0, 10))
            avatar_frame.pack_propagate(False)
            
            ctk.CTkLabel(
                avatar_frame,
                text="🤖",
                font=ctk.CTkFont("Segoe UI", 16)
            ).pack(expand=True)
        
        # Bubble del mensaje
        bubble_color = BG_GLASS if is_bot else ACCENT_BLUE
        text_color = TEXT_WHITE
        
        bubble = ctk.CTkFrame(
            msg_container,
            fg_color=bubble_color,
            corner_radius=15
        )
        bubble.pack(side="left" if is_bot else "right", fill="x", expand=True if is_bot else False)
        
        # Sender name
        if is_bot:
            ctk.CTkLabel(
                bubble,
                text=sender,
                font=ctk.CTkFont("Segoe UI", 11, "bold"),
                text_color=ACCENT_BLUE,
                anchor="w"
            ).pack(anchor="w", padx=15, pady=(10, 2))
        
        # Message text
        ctk.CTkLabel(
            bubble,
            text=text,
            font=ctk.CTkFont("Segoe UI", 13),
            text_color=text_color,
            wraplength=500,
            justify="left" if is_bot else "right",
            anchor="w" if is_bot else "e"
        ).pack(anchor="w" if is_bot else "e", padx=15, pady=(2 if is_bot else 10, 10))
        
        # Timestamp
        ctk.CTkLabel(
            bubble,
            text=datetime.now().strftime("%H:%M"),
            font=ctk.CTkFont("Segoe UI", 9),
            text_color=TEXT_DIM,
            anchor="e"
        ).pack(anchor="e", padx=15, pady=(0, 8))
        
        # Auto scroll
        self.root.after(100, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))
    
    def _send_message(self):
        """Envía un mensaje"""
        text = self.input_var.get().strip()
        if not text or self._thinking:
            return
        
        self.input_var.set("")
        self._add_message(USERNAME, text, is_bot=False)
        
        # Mostrar indicador de escritura
        self._set_thinking(True)
        self._draw_wave(idle=False)
        
        # Procesar en hilo
        threading.Thread(target=self._process_message, args=(text,), daemon=True).start()
    
    def _process_message(self, text):
        """Procesa el mensaje con el brain"""
        try:
            if BRAIN_OK:
                response = ask_kalmiya(text)
            else:
                response = "Lo siento, el sistema de IA no está disponible en este momento."
        except Exception as e:
            response = f"Error al procesar: {str(e)}"
        
        # Agregar respuesta
        self.root.after(0, self._on_response, response)
    
    def _on_response(self, response):
        """Maneja la respuesta del bot"""
        self._set_thinking(False)
        self._draw_wave(idle=True)
        self._add_message(BOTNAME, response, is_bot=True)
    
    def _set_thinking(self, is_thinking):
        """Cambia estado de pensando"""
        self._thinking = is_thinking
        self.entry.configure(state="disabled" if is_thinking else "normal")
        self.send_btn.configure(
            fg_color=BG_GLASS if is_thinking else ACCENT_BLUE,
            text="..." if is_thinking else "➤"
        )
    
    def _clear_chat(self):
        """Limpia el chat"""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self._add_message(BOTNAME, "Chat limpiado. ¿En qué más puedo ayudarte?", is_bot=True)
    
    def _toggle_voice(self):
        """Toggle de voz (placeholder)"""
        self._add_message(BOTNAME, 
                         "🎤 Función de voz en desarrollo. Por ahora usa el chat de texto.",
                         is_bot=True)
    
    def _get_greeting(self):
        """Obtiene saludo según la hora"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Buenos días"
        elif 12 <= hour < 19:
            return "Buenas tardes"
        else:
            return "Buenas noches"
    
    def _draw_status_dot(self):
        """Dibuja indicador de status pulsante"""
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 10, 10, fill=SUCCESS, outline="")
    
    def _draw_wave(self, idle=True):
        """Dibuja wave de audio"""
        self.wave_canvas.delete("all")
        
        if idle:
            # Línea plana cuando está idle
            self.wave_canvas.create_line(
                10, 20, 270, 20,
                fill=TEXT_DIM,
                width=2
            )
        else:
            # Wave animada cuando está escuchando
            points = []
            for i in range(0, 280, 5):
                y = 20 + math.sin((i + self._anim_frame) * 0.1) * 10
                points.extend([i, y])
            
            if len(points) >= 4:
                self.wave_canvas.create_line(
                    points,
                    fill=ACCENT_BLUE,
                    width=3,
                    smooth=True
                )
    
    def _update_stats_loop(self):
        """Loop de actualización de stats"""
        while self._running:
            try:
                cpu = psutil.cpu_percent(interval=1)
                ram = psutil.virtual_memory().percent
                disk = psutil.disk_usage('C:\\' if sys.platform == 'win32' else '/').percent
                
                self.root.after(0, self._update_stats, cpu, ram, disk)
            except:
                pass
            time.sleep(2)
    
    def _update_stats(self, cpu, ram, disk):
        """Actualiza los labels de stats"""
        if hasattr(self, 'cpu_label'):
            self.cpu_label.configure(text=f"{cpu:.0f}%")
        if hasattr(self, 'ram_label'):
            self.ram_label.configure(text=f"{ram:.0f}%")
        if hasattr(self, 'disk_label'):
            self.disk_label.configure(text=f"{disk:.0f}%")
    
    def _start_animations(self):
        """Inicia animaciones"""
        self._animate()
    
    def _animate(self):
        """Loop de animación"""
        if not self._running:
            return
        
        self._anim_frame += 1
        self._avatar_breath += 0.1
        
        # Respiración del avatar (escala sutil)
        # scale = 1.0 + math.sin(self._avatar_breath) * 0.02
        # TODO: Aplicar escala al avatar
        
        # Pulse del status dot
        if self._anim_frame % 30 == 0:
            self._pulse_state = not self._pulse_state
            color = SUCCESS if self._pulse_state else "#00aa66"
            self.status_canvas.delete("all")
            self.status_canvas.create_oval(2, 2, 10, 10, fill=color, outline="")
        
        # Wave si está pensando
        if self._thinking:
            self._draw_wave(idle=False)
        
        self.root.after(33, self._animate)  # ~30 FPS
    
    def _make_draggable(self):
        """Hace la ventana arrastrable"""
        self.root.bind("<ButtonPress-1>", self._drag_start)
        self.root.bind("<B1-Motion>", self._drag_move)
    
    def _drag_start(self, e):
        self._drag_x, self._drag_y = e.x, e.y
    
    def _drag_move(self, e):
        x = self.root.winfo_x() + (e.x - self._drag_x)
        y = self.root.winfo_y() + (e.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")
    
    def _minimize(self):
        """Minimiza la ventana"""
        self.root.overrideredirect(False)
        self.root.iconify()
        self.root.after(500, lambda: self.root.overrideredirect(True))
    
    def _on_close(self):
        """Cierra la ventana"""
        self._running = False
        self.root.destroy()
    
    def run(self):
        """Inicia el chat"""
        self.root.mainloop()


# Helper para crear rectángulos redondeados en Canvas
def Canvas_create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
    """Crea un rectángulo con esquinas redondeadas"""
    points = [
        x1+radius, y1,
        x1+radius, y1,
        x2-radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1+radius,
        x1, y1
    ]
    return self.create_polygon(points, **kwargs, smooth=True)

# Agregar método a Canvas
Canvas.create_rounded_rect = Canvas_create_rounded_rect


def main():
    """Función main para importación"""
    chat = KalmiyaChatV2()
    chat.run()


if __name__ == "__main__":
    main()
