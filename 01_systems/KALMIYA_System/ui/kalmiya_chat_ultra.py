"""
kalmiya_chat_ultra.py — Chat KALMIYA v3.7 ULTRA
================================================
Versión mejorada con TODAS las actualizaciones:
- Avatar animado (parpadeo, movimiento)
- Temas de color intercambiables
- Botones de voz y comandos
- Notificaciones visuales
- Historial persistente
- Modo compacto/expandido
- Atajos de teclado
- Y mucho más...

Tamaño: 550x750 px
RAM: ~140 MB
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas
import threading
import time
import sys
import os
import json
from datetime import datetime
from pathlib import Path
import random

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

# ══════════════════════════════════════════════════════════════════════════════
# TEMAS DE COLOR
# ══════════════════════════════════════════════════════════════════════════════

THEMES = {
    "cyber_pink": {
        "name": "Cyber Pink 💖",
        "bg_dark": "#1a0a1f",
        "bg_card": "#2d1b3d",
        "bg_input": "#3d2550",
        "accent_primary": "#ff6ec7",
        "accent_secondary": "#c74dff",
        "text_white": "#ffffff",
        "text_gray": "#c9b3d4",
        "success": "#ff6ec7",
        "robot_white": "#f5f5f5",
        "robot_accent": "#ffb6d9",
        "robot_eyes": "#ff6ec7",
        "robot_dark": "#2a2a2a"
    },
    "cyber_cyan": {
        "name": "Cyber Cyan 🌊",
        "bg_dark": "#0a0e1a",
        "bg_card": "#0f1624",
        "bg_input": "#131b2e",
        "accent_primary": "#00d9ff",
        "accent_secondary": "#00ffaa",
        "text_white": "#ffffff",
        "text_gray": "#8b9ab5",
        "success": "#00ff88",
        "robot_white": "#f5f5f5",
        "robot_accent": "#a0e7ff",
        "robot_eyes": "#00d9ff",
        "robot_dark": "#2a2a2a"
    },
    "neon_purple": {
        "name": "Neon Purple 💜",
        "bg_dark": "#0f0a1f",
        "bg_card": "#1a0f2e",
        "bg_input": "#251a3a",
        "accent_primary": "#b844ff",
        "accent_secondary": "#ff44ea",
        "text_white": "#ffffff",
        "text_gray": "#b8a3d4",
        "success": "#b844ff",
        "robot_white": "#f5f5f5",
        "robot_accent": "#d9b3ff",
        "robot_eyes": "#b844ff",
        "robot_dark": "#2a2a2a"
    },
    "sakura": {
        "name": "Sakura 🌸",
        "bg_dark": "#1f0f1a",
        "bg_card": "#2e1a24",
        "bg_input": "#3d2433",
        "accent_primary": "#ffb3d9",
        "accent_secondary": "#ff8cc7",
        "text_white": "#ffffff",
        "text_gray": "#d4b3c9",
        "success": "#ffb3d9",
        "robot_white": "#f5f5f5",
        "robot_accent": "#ffd9ec",
        "robot_eyes": "#ff8cc7",
        "robot_dark": "#2a2a2a"
    }
}

# Tamaño
CHAT_W = 550
CHAT_H = 750

# Archivo de historial
HISTORY_FILE = Path(__file__).parent.parent.parent.parent / "04_config" / "chat_history.json"


class KalmiyaChatUltra:
    """Chat KALMIYA Ultra - Todas las características"""
    
    def __init__(self):
        self._drag_x = 0
        self._drag_y = 0
        self._thinking = False
        self._running = True
        self._current_theme = "cyber_pink"
        self._compact_mode = False
        self._always_on_top = True
        self._blink_state = True
        self._arm_position = 0  # 0=arriba, 1=medio, 2=abajo
        self._head_tilt = 0  # -2, -1, 0, 1, 2
        self._heart_size = 0  # 0=normal, 1=grande
        self._ear_wiggle = 0  # 0=normal, 1=izq, 2=der
        self._is_talking = False
        # NUEVAS animaciones de cuerpo completo
        self._body_bounce = 0  # Salto vertical (0-8 píxeles)
        self._body_sway = 0  # Balanceo horizontal (-4 a +4 píxeles)
        self._body_rotation = 0  # Rotación leve (-2 a +2 para simular giro)
        self._history = []
        self._load_history()
        
        ctk.set_appearance_mode("dark")
        self._build_window()
        self._start_animations()
    
    @property
    def theme(self):
        """Obtiene colores del tema actual"""
        return THEMES[self._current_theme]
    
    def _load_history(self):
        """Carga historial de conversaciones"""
        try:
            if HISTORY_FILE.exists():
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._history = data.get('messages', [])[-50:]  # Últimas 50
        except:
            self._history = []
    
    def _save_history(self):
        """Guarda historial de conversaciones"""
        try:
            HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump({'messages': self._history}, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def _build_window(self):
        self.root = ctk.CTk()
        self.root.title(f"✨ {BOTNAME} Ultra v3.7 ✨")
        # NO usar overrideredirect - ventana normal de Windows
        # self.root.overrideredirect(True)  # DESACTIVADO
        self.root.attributes("-topmost", True)  # Siempre al frente
        self.root.attributes("-alpha", 0.97)
        self.root.configure(fg_color=self.theme["bg_dark"])
        
        # Posicionar CENTRADO en pantalla (más visible)
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - CHAT_W) // 2  # Centrado horizontal
        y = (sh - CHAT_H) // 2  # Centrado vertical
        self.root.geometry(f"{CHAT_W}x{CHAT_H}+{x}+{y}")
        
        # FORZAR ventana visible y al frente
        self.root.deiconify()  # Asegurar que no está minimizada
        self.root.lift()  # Traer al frente
        self.root.focus_force()  # Forzar focus
        self.root.update()  # Actualizar ventana inmediatamente
        
        # Atajos de teclado
        self.root.bind("<Control-q>", lambda e: self._on_close())
        self.root.bind("<Control-l>", lambda e: self._clear_chat())
        self.root.bind("<Control-t>", lambda e: self._cycle_theme())
        self.root.bind("<Control-h>", lambda e: self._show_help())
        self.root.bind("<Control-Shift-M>", lambda e: self.root.iconify())  # Minimizar con atajo
        
        # Layout
        self._build_header()
        self._build_avatar_animated()
        self._build_chat_section()
        self._build_input_section()
        self._build_footer()
        
        # NO hacer draggable - ventana estándar
        # self._make_draggable()  # DESACTIVADO
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _build_header(self):
        """Header simplificado para ventana estándar"""
        header = ctk.CTkFrame(self.root, fg_color="transparent", height=50)
        header.pack(fill="x", padx=15, pady=(10, 0))
        
        # Título con versión
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text=f"✨ {BOTNAME} Ultra",
            font=ctk.CTkFont("Segoe UI", 18, "bold"),
            text_color=self.theme["accent_primary"]
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkLabel(
            title_frame,
            text="v3.7",
            font=ctk.CTkFont("Segoe UI", 9),
            text_color=self.theme["text_gray"]
        ).pack(side="left")
        
        # Controles (solo los funcionales)
        controls = ctk.CTkFrame(header, fg_color="transparent")
        controls.pack(side="right")
        
        # Status
        status_frame = ctk.CTkFrame(controls, fg_color="transparent")
        status_frame.pack(side="left", padx=5)
        
        self.status_canvas = Canvas(
            status_frame, width=10, height=10,
            bg=self.theme["bg_dark"], highlightthickness=0
        )
        self.status_canvas.pack(side="left", padx=2)
        self.status_canvas.create_oval(1, 1, 9, 9, fill=self.theme["success"], outline="")
        
        ctk.CTkLabel(
            status_frame,
            text="ONLINE",
            font=ctk.CTkFont("Segoe UI", 8),
            text_color=self.theme["success"]
        ).pack(side="left")
        
        # Botón de temas
        self.theme_btn = ctk.CTkButton(
            controls,
            text="🎨 Tema",
            width=70,
            height=28,
            fg_color=self.theme["bg_card"],
            hover_color=self.theme["bg_input"],
            command=self._cycle_theme,
            font=ctk.CTkFont("Segoe UI", 10)
        )
        self.theme_btn.pack(side="left", padx=3)
        
        # Botón de ayuda
        ctk.CTkButton(
            controls,
            text="❓ Ayuda",
            width=70,
            height=28,
            fg_color=self.theme["bg_card"],
            hover_color=self.theme["bg_input"],
            command=self._show_help,
            font=ctk.CTkFont("Segoe UI", 10)
        ).pack(side="left", padx=3)
        
        # Nota: Los botones minimizar/cerrar están en la barra de Windows
            height=25,
            fg_color=self.theme["bg_card"],
            hover_color=self.theme["bg_input"],
            command=self._show_help
        ).pack(side="left", padx=1)
        
        # Minimizar
        ctk.CTkButton(
            controls,
            text="─",
            width=25,
            height=25,
            fg_color=self.theme["bg_card"],
            hover_color=self.theme["bg_input"],
            command=self._minimize
        ).pack(side="left", padx=1)
        
        # Cerrar
        ctk.CTkButton(
            controls,
            text="✕",
            width=25,
            height=25,
            fg_color=self.theme["bg_card"],
            hover_color="#ff3333",
            command=self._on_close
        ).pack(side="left", padx=1)
    
    def _build_avatar_animated(self):
        """Avatar animado con parpadeo"""
        container = ctk.CTkFrame(
            self.root,
            fg_color=self.theme["bg_card"],
            corner_radius=15,
            height=160
        )
        container.pack(fill="x", padx=15, pady=10)
        container.pack_propagate(False)
        
        # Avatar animado (90x120)
        self.avatar_canvas = Canvas(
            container,
            width=90,
            height=120,
            bg=self.theme["bg_card"],
            highlightthickness=0
        )
        self.avatar_canvas.pack(side="left", padx=15, pady=20)
        self._draw_animated_avatar()
        
        # Info
        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=10, pady=20)
        
        greeting = self._get_greeting()
        
        # Título animado
        self.greeting_label = ctk.CTkLabel(
            info,
            text=f"👋 {greeting}, {USERNAME}!",
            font=ctk.CTkFont("Segoe UI", 17, "bold"),
            text_color=self.theme["text_white"],
            anchor="w"
        )
        self.greeting_label.pack(anchor="w", pady=(0, 3))
        
        # Mensajes aleatorios
        friendly_messages = [
            "✨ ¡Estoy lista para ayudarte!",
            "💖 ¿En qué puedo asistirte hoy?",
            "🌟 ¡Conversemos sobre lo que necesites!",
            "🚀 ¿Qué aventura tenemos hoy?",
            "💜 ¡Aquí para lo que necesites!"
        ]
        friendly_msg = random.choice(friendly_messages)
        
        ctk.CTkLabel(
            info,
            text=friendly_msg,
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=self.theme["text_gray"],
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        # Botones rápidos
        quick_btns = ctk.CTkFrame(info, fg_color="transparent")
        quick_btns.pack(anchor="w", pady=(5, 0))
        
        # Botón de voz (placeholder)
        ctk.CTkButton(
            quick_btns,
            text="🎤 Voz",
            width=70,
            height=28,
            fg_color=self.theme["accent_primary"],
            hover_color=self.theme["accent_secondary"],
            font=ctk.CTkFont("Segoe UI", 10),
            command=self._voice_command
        ).pack(side="left", padx=(0, 5))
        
        # Botón de comandos rápidos
        ctk.CTkButton(
            quick_btns,
            text="⚡ Rápido",
            width=70,
            height=28,
            fg_color=self.theme["bg_input"],
            hover_color=self.theme["accent_primary"],
            font=ctk.CTkFont("Segoe UI", 10),
            command=self._quick_commands
        ).pack(side="left", padx=(0, 5))
        
        # Stats mini
        if PSUTIL_OK:
            self.stats_label = ctk.CTkLabel(
                info,
                text="CPU: ... | RAM: ... | Disco: ...",
                font=ctk.CTkFont("Segoe UI", 8),
                text_color=self.theme["text_gray"],
                anchor="w"
            )
            self.stats_label.pack(anchor="w", pady=(8, 0))
    
    def _draw_animated_avatar(self):
        """Dibuja avatar que será animado"""
        c = self.avatar_canvas
        t = self.theme
        
        # Limpiar
        c.delete("all")
        
        # Calcular offsets de animación
        head_offset_x = self._head_tilt * 2
        ear_left_offset = -3 if self._ear_wiggle == 1 else 0
        ear_right_offset = 3 if self._ear_wiggle == 2 else 0
        
        # NUEVOS: Offsets de cuerpo completo
        body_offset_y = -self._body_bounce  # Salto (negativo = sube)
        body_offset_x = self._body_sway  # Balanceo lateral
        rotation_skew = self._body_rotation  # Rotación (simulada con skew)
        
        # NUEVOS: Offsets de cuerpo completo
        body_offset_y = -self._body_bounce  # Salto (negativo = sube)
        body_offset_x = self._body_sway  # Balanceo lateral
        rotation_skew = self._body_rotation  # Rotación (simulada con skew)
        
        # ===== OREJAS LARGAS (con movimiento) =====
        # Aplicar offsets de cuerpo (balanceo + salto) + offset individual de orejas
        c.create_oval(8 + ear_left_offset + body_offset_x + rotation_skew, 0 + body_offset_y, 
                     22 + ear_left_offset + body_offset_x + rotation_skew, 35 + body_offset_y, 
                     fill=t["robot_white"], outline=t["robot_dark"], width=2, tags="ear")
        c.create_oval(10 + ear_left_offset + body_offset_x + rotation_skew, 10 + body_offset_y, 
                     20 + ear_left_offset + body_offset_x + rotation_skew, 30 + body_offset_y, 
                     fill=t["robot_accent"], outline="", tags="ear")
        
        c.create_oval(68 + ear_right_offset + body_offset_x - rotation_skew, 0 + body_offset_y, 
                     82 + ear_right_offset + body_offset_x - rotation_skew, 35 + body_offset_y, 
                     fill=t["robot_white"], outline=t["robot_dark"], width=2, tags="ear")
        c.create_oval(70 + ear_right_offset + body_offset_x - rotation_skew, 10 + body_offset_y, 
                     80 + ear_right_offset + body_offset_x - rotation_skew, 30 + body_offset_y, 
                     fill=t["robot_accent"], outline="", tags="ear")
        
        # ===== CABEZA (con inclinación + movimiento de cuerpo) =====
        c.create_oval(20 + head_offset_x + body_offset_x + rotation_skew, 25 + body_offset_y, 
                     70 + head_offset_x + body_offset_x - rotation_skew, 65 + body_offset_y, 
                     fill=t["robot_white"], outline=t["robot_dark"], width=2, tags="head")
        
        # Detalles decorativos (cabeza)
        c.create_line(28 + head_offset_x + body_offset_x, 32 + body_offset_y, 
                     35 + head_offset_x + body_offset_x, 36 + body_offset_y, 
                     fill=t["robot_accent"], width=2, tags="head")
        c.create_line(55 + head_offset_x + body_offset_x, 36 + body_offset_y, 
                     62 + head_offset_x + body_offset_x, 32 + body_offset_y, 
                     fill=t["robot_accent"], width=2, tags="head")
        
        # ===== OJOS (animables con parpadeo + movimiento de cuerpo) =====
        if self._blink_state:
            # Ojos abiertos
            c.create_oval(26 + head_offset_x + body_offset_x, 38 + body_offset_y, 
                         43 + head_offset_x + body_offset_x, 54 + body_offset_y, 
                         fill=t["robot_eyes"], outline="", tags="eyes")
            c.create_oval(47 + head_offset_x + body_offset_x, 38 + body_offset_y, 
                         64 + head_offset_x + body_offset_x, 54 + body_offset_y, 
                         fill=t["robot_eyes"], outline="", tags="eyes")
            # Brillos
            c.create_oval(29 + head_offset_x + body_offset_x, 40 + body_offset_y, 
                         40 + head_offset_x + body_offset_x, 50 + body_offset_y, 
                         fill="#80e0ff", outline="", tags="eyes")
            c.create_oval(50 + head_offset_x + body_offset_x, 40 + body_offset_y, 
                         61 + head_offset_x + body_offset_x, 50 + body_offset_y, 
                         fill="#80e0ff", outline="", tags="eyes")
            c.create_oval(31 + head_offset_x + body_offset_x, 42 + body_offset_y, 
                         38 + head_offset_x + body_offset_x, 48 + body_offset_y, 
                         fill="#ffffff", outline="", tags="eyes")
            c.create_oval(52 + head_offset_x + body_offset_x, 42 + body_offset_y, 
                         59 + head_offset_x + body_offset_x, 48 + body_offset_y, 
                         fill="#ffffff", outline="", tags="eyes")
        else:
            # Ojos cerrados (parpadeo)
            c.create_line(26 + head_offset_x + body_offset_x, 46 + body_offset_y, 
                         43 + head_offset_x + body_offset_x, 46 + body_offset_y, 
                         fill=t["robot_eyes"], width=3, tags="eyes")
            c.create_line(47 + head_offset_x + body_offset_x, 46 + body_offset_y, 
                         64 + head_offset_x + body_offset_x, 46 + body_offset_y, 
                         fill=t["robot_eyes"], width=3, tags="eyes")
        
        # ===== SONRISA (más grande si está hablando + movimiento de cuerpo) =====
        if self._is_talking:
            c.create_arc(30 + head_offset_x + body_offset_x, 46 + body_offset_y, 
                        60 + head_offset_x + body_offset_x, 64 + body_offset_y, 
                        start=200, extent=140, outline=t["robot_accent"], 
                        width=3, style="arc", tags="mouth")
        else:
            c.create_arc(32 + head_offset_x + body_offset_x, 48 + body_offset_y, 
                        58 + head_offset_x + body_offset_x, 62 + body_offset_y, 
                        start=200, extent=140, outline=t["robot_accent"], 
                        width=3, style="arc", tags="mouth")
        
        # ===== RUBOR (con movimiento de cuerpo) =====
        c.create_oval(21 + head_offset_x + body_offset_x, 48 + body_offset_y, 
                     28 + head_offset_x + body_offset_x, 54 + body_offset_y, 
                     fill=t["robot_accent"], outline="", stipple="gray50", tags="blush")
        c.create_oval(62 + head_offset_x + body_offset_x, 48 + body_offset_y, 
                     69 + head_offset_x + body_offset_x, 54 + body_offset_y, 
                     fill=t["robot_accent"], outline="", stipple="gray50", tags="blush")
        
        # ===== CUELLO (con movimiento de cuerpo) =====
        c.create_rectangle(39 + body_offset_x, 62 + body_offset_y, 
                          51 + body_offset_x, 68 + body_offset_y, 
                          fill=t["robot_dark"], outline="", tags="neck")
        
        # ===== TORSO (con movimiento de cuerpo + rotación) =====
        c.create_oval(24 + body_offset_x + rotation_skew, 64 + body_offset_y, 
                     66 + body_offset_x - rotation_skew, 90 + body_offset_y, 
                     fill=t["robot_white"], outline=t["robot_dark"], width=2, tags="body")
        
        # Detalles hombros (con movimiento)
        c.create_oval(22 + body_offset_x + rotation_skew, 68 + body_offset_y, 
                     32 + body_offset_x + rotation_skew, 78 + body_offset_y, 
                     fill=t["robot_accent"], outline=t["robot_dark"], width=1, tags="body")
        c.create_oval(58 + body_offset_x - rotation_skew, 68 + body_offset_y, 
                     68 + body_offset_x - rotation_skew, 78 + body_offset_y, 
                     fill=t["robot_accent"], outline=t["robot_dark"], width=1, tags="body")
        
        # ===== CORE (con movimiento) =====
        c.create_oval(36 + body_offset_x, 72 + body_offset_y, 
                     54 + body_offset_x, 86 + body_offset_y, 
                     fill=t["robot_dark"], outline=t["robot_eyes"], width=2, tags="core")
        c.create_oval(39 + body_offset_x, 75 + body_offset_y, 
                     51 + body_offset_x, 83 + body_offset_y, 
                     fill=t["robot_eyes"], outline="", tags="core")
        c.create_oval(41 + body_offset_x, 76 + body_offset_y, 
                     48 + body_offset_x, 82 + body_offset_y, 
                     fill="#ffffff", outline="", tags="core")
        
        # ===== CORAZÓN (late + movimiento) =====
        heart_scale = 1 + (self._heart_size * 0.15)  # 0-15% más grande
        heart_base_x, heart_base_y = 45 + body_offset_x, 88 + body_offset_y
        heart_w, heart_h = 5 * heart_scale, 4 * heart_scale
        
        c.create_oval(heart_base_x - heart_w, heart_base_y - heart_h, 
                     heart_base_x + heart_w, heart_base_y + heart_h, 
                     fill=t["robot_accent"], outline="", tags="heart")
        
        # Punta del corazón
        points = [
            heart_base_x - heart_w, heart_base_y,
            heart_base_x, heart_base_y + (6 * heart_scale),
            heart_base_x + heart_w, heart_base_y
        ]
        c.create_polygon(points, fill=t["robot_accent"], outline="", tags="heart")
        
        # ===== BRAZOS (con movimiento + movimiento de cuerpo) =====
        # Posiciones: 0=arriba, 1=medio, 2=abajo
        if self._arm_position == 0:
            # Brazos arriba (saludando)
            left_arm = [(26 + body_offset_x, 70 + body_offset_y, 
                        16 + body_offset_x, 62 + body_offset_y, 
                        12 + body_offset_x, 56 + body_offset_y)]
            right_arm = [(64 + body_offset_x, 70 + body_offset_y, 
                         74 + body_offset_x, 62 + body_offset_y, 
                         78 + body_offset_x, 56 + body_offset_y)]
            left_hand_y, right_hand_y = 53 + body_offset_y, 53 + body_offset_y
        elif self._arm_position == 1:
            # Brazos a medio nivel
            left_arm = [(26 + body_offset_x, 70 + body_offset_y, 
                        18 + body_offset_x, 68 + body_offset_y, 
                        14 + body_offset_x, 68 + body_offset_y)]
            right_arm = [(64 + body_offset_x, 70 + body_offset_y, 
                         72 + body_offset_x, 68 + body_offset_y, 
                         76 + body_offset_x, 68 + body_offset_y)]
            left_hand_y, right_hand_y = 65 + body_offset_y, 65 + body_offset_y
        else:
            # Brazos abajo
            left_arm = [(26 + body_offset_x, 72 + body_offset_y, 
                        20 + body_offset_x, 78 + body_offset_y, 
                        18 + body_offset_x, 84 + body_offset_y)]
            right_arm = [(64 + body_offset_x, 72 + body_offset_y, 
                         70 + body_offset_x, 78 + body_offset_y, 
                         72 + body_offset_x, 84 + body_offset_y)]
            left_hand_y, right_hand_y = 81 + body_offset_y, 81 + body_offset_y
        
        # Brazo izquierdo
        c.create_line(*left_arm[0], fill=t["robot_white"], width=8, 
                     capstyle="round", tags="arm")
        c.create_oval(left_arm[0][4] - 3, left_hand_y, left_arm[0][4] + 3, left_hand_y + 6, 
                     fill=t["robot_white"], outline=t["robot_dark"], width=2, tags="hand")
        c.create_oval(left_arm[0][4] - 2, left_hand_y + 1, left_arm[0][4] + 2, left_hand_y + 5, 
                     fill=t["robot_accent"], outline="", tags="hand")
        
        # Brazo derecho
        c.create_line(*right_arm[0], fill=t["robot_white"], width=8, 
                     capstyle="round", tags="arm")
        c.create_oval(right_arm[0][4] - 3, right_hand_y, right_arm[0][4] + 3, right_hand_y + 6, 
                     fill=t["robot_white"], outline=t["robot_dark"], width=2, tags="hand")
        c.create_oval(right_arm[0][4] - 2, right_hand_y + 1, right_arm[0][4] + 2, right_hand_y + 5, 
                     fill=t["robot_accent"], outline="", tags="hand")
        
        # ===== PIERNAS (con movimiento de cuerpo + rotación) =====
        c.create_rectangle(30 + body_offset_x + rotation_skew, 88 + body_offset_y, 
                          40 + body_offset_x + rotation_skew, 102 + body_offset_y, 
                          fill=t["robot_white"], outline=t["robot_dark"], width=1, tags="leg")
        c.create_rectangle(50 + body_offset_x - rotation_skew, 88 + body_offset_y, 
                          60 + body_offset_x - rotation_skew, 102 + body_offset_y, 
                          fill=t["robot_white"], outline=t["robot_dark"], width=1, tags="leg")
        
        # Rodillas
        c.create_oval(32 + body_offset_x, 92 + body_offset_y, 
                     38 + body_offset_x, 98 + body_offset_y, 
                     fill=t["robot_accent"], outline="", tags="leg")
        c.create_oval(52 + body_offset_x, 92 + body_offset_y, 
                     58 + body_offset_x, 98 + body_offset_y, 
                     fill=t["robot_accent"], outline="", tags="leg")
        
        # ===== ZAPATOS (con movimiento de cuerpo + rotación) =====
        c.create_oval(26 + body_offset_x + rotation_skew, 98 + body_offset_y, 
                     44 + body_offset_x + rotation_skew, 110 + body_offset_y, 
                     fill=t["robot_accent"], outline=t["robot_dark"], width=2, tags="shoe")
        c.create_oval(46 + body_offset_x - rotation_skew, 98 + body_offset_y, 
                     64 + body_offset_x - rotation_skew, 110 + body_offset_y, 
                     fill=t["robot_accent"], outline=t["robot_dark"], width=2, tags="shoe")
        
        # Brillos
        c.create_oval(30 + body_offset_x, 100 + body_offset_y, 
                     36 + body_offset_x, 105 + body_offset_y, 
                     fill="#ffffff", outline="", stipple="gray50", tags="shoe")
        c.create_oval(50 + body_offset_x, 100 + body_offset_y, 
                     56 + body_offset_x, 105 + body_offset_y, 
                     fill="#ffffff", outline="", stipple="gray50", tags="shoe")
    
    def _build_chat_section(self):
        """Sección de chat mejorada"""
        # Header
        chat_header = ctk.CTkFrame(self.root, fg_color="transparent", height=35)
        chat_header.pack(fill="x", padx=15, pady=(5, 5))
        
        ctk.CTkLabel(
            chat_header,
            text="💬 Conversación",
            font=ctk.CTkFont("Segoe UI", 12, "bold"),
            text_color=self.theme["text_white"]
        ).pack(side="left")
        
        # Botones de chat
        btn_frame = ctk.CTkFrame(chat_header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        # Historial
        ctk.CTkButton(
            btn_frame,
            text="📜",
            width=30,
            height=25,
            fg_color=self.theme["bg_card"],
            hover_color=self.theme["bg_input"],
            command=self._load_history_to_chat
        ).pack(side="left", padx=1)
        
        # Limpiar
        ctk.CTkButton(
            btn_frame,
            text="🗑️",
            width=30,
            height=25,
            fg_color=self.theme["bg_card"],
            hover_color=self.theme["bg_input"],
            command=self._clear_chat
        ).pack(side="left", padx=1)
        
        # Container
        self.chat_container = ctk.CTkFrame(
            self.root,
            fg_color=self.theme["bg_card"],
            corner_radius=15
        )
        self.chat_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        # Scrollable frame
        self.chat_frame = ctk.CTkScrollableFrame(
            self.chat_container,
            fg_color="transparent",
            scrollbar_button_color=self.theme["accent_primary"]
        )
        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mensaje de bienvenida
        welcome_messages = [
            f"¡Hola {USERNAME}! 👋 Soy {BOTNAME} Ultra v3.7. Ahora con temas de color, animaciones y muchas mejoras. ¿Qué quieres hacer hoy? ✨",
            f"¡Bienvenida {USERNAME}! 🌟 {BOTNAME} Ultra está aquí con todas las funciones mejoradas. Presiona Ctrl+H para ver los atajos. 💜",
            f"¡Hey {USERNAME}! 🚀 Nueva versión Ultra con temas, animaciones y más. ¡Prueba el botón 🎨 para cambiar colores! ✨"
        ]
        self._add_message(BOTNAME, random.choice(welcome_messages), is_bot=True)
    
    def _build_input_section(self):
        """Input mejorado con contador de caracteres"""
        input_container = ctk.CTkFrame(
            self.root,
            fg_color=self.theme["bg_input"],
            corner_radius=20,
            height=70
        )
        input_container.pack(fill="x", padx=15, pady=(0, 10))
        input_container.pack_propagate(False)
        
        # Frame para entry y contador
        entry_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        entry_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        self.input_var = tk.StringVar()
        self.input_var.trace('w', self._update_char_count)
        
        self.entry = ctk.CTkEntry(
            entry_frame,
            textvariable=self.input_var,
            placeholder_text="Escribe aquí... (Ctrl+Enter para enviar)",
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color="transparent",
            border_width=0
        )
        self.entry.pack(fill="both", expand=True)
        self.entry.bind("<Return>", lambda e: self._send_message() if not e.state & 0x1 else None)
        self.entry.bind("<Control-Return>", lambda e: self._send_message())
        
        # Contador de caracteres
        self.char_count = ctk.CTkLabel(
            entry_frame,
            text="0",
            font=ctk.CTkFont("Segoe UI", 8),
            text_color=self.theme["text_gray"]
        )
        self.char_count.pack(anchor="e")
        
        # Botón enviar
        self.send_btn = ctk.CTkButton(
            input_container,
            text="➤",
            width=45,
            height=45,
            fg_color=self.theme["accent_primary"],
            hover_color=self.theme["accent_secondary"],
            font=ctk.CTkFont("Segoe UI", 18, "bold"),
            corner_radius=22,
            command=self._send_message
        )
        self.send_btn.pack(side="right", padx=10, pady=10)
    
    def _build_footer(self):
        """Footer mejorado con más info"""
        footer = ctk.CTkFrame(self.root, fg_color="transparent", height=30)
        footer.pack(fill="x", padx=15, pady=(0, 10))
        
        # Info izquierda
        left_info = ctk.CTkFrame(footer, fg_color="transparent")
        left_info.pack(side="left")
        
        status = get_engine_status() if BRAIN_OK else {}
        engine = status.get('engine', 'local')
        
        ctk.CTkLabel(
            left_info,
            text=f"⚙️ {engine.upper()}",
            font=ctk.CTkFont("Segoe UI", 8),
            text_color=self.theme["text_gray"]
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkLabel(
            left_info,
            text="• Ultra v3.7",
            font=ctk.CTkFont("Segoe UI", 8),
            text_color=self.theme["text_gray"]
        ).pack(side="left")
        
        # Info derecha
        right_info = ctk.CTkFrame(footer, fg_color="transparent")
        right_info.pack(side="right")
        
        # Tema actual
        ctk.CTkLabel(
            right_info,
            text=f"🎨 {self.theme['name']}",
            font=ctk.CTkFont("Segoe UI", 8),
            text_color=self.theme["text_gray"]
        ).pack(side="left", padx=(0, 5))
        
        # Hora
        self.time_label = ctk.CTkLabel(
            right_info,
            text=datetime.now().strftime("%H:%M"),
            font=ctk.CTkFont("Segoe UI", 8),
            text_color=self.theme["text_gray"]
        )
        self.time_label.pack(side="left")
    
    def _add_message(self, sender, text, is_bot=False):
        """Agrega mensaje mejorado con timestamp"""
        msg_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_frame.pack(fill="x", pady=5, anchor="w" if is_bot else "e")
        
        # Bubble
        bubble_color = self.theme["bg_input"] if is_bot else self.theme["accent_primary"]
        text_color = self.theme["text_white"]
        
        bubble = ctk.CTkFrame(
            msg_frame,
            fg_color=bubble_color,
            corner_radius=12
        )
        bubble.pack(side="left" if is_bot else "right", fill="x",
                   expand=True if is_bot else False,
                   padx=(0 if is_bot else 50, 50 if is_bot else 0))
        
        # Header del mensaje
        if is_bot:
            msg_header = ctk.CTkFrame(bubble, fg_color="transparent")
            msg_header.pack(fill="x", padx=12, pady=(8, 2))
            
            ctk.CTkLabel(
                msg_header,
                text=f"🤖 {sender}",
                font=ctk.CTkFont("Segoe UI", 9, "bold"),
                text_color=self.theme["accent_primary"],
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                msg_header,
                text=datetime.now().strftime("%H:%M"),
                font=ctk.CTkFont("Segoe UI", 7),
                text_color=self.theme["text_gray"],
                anchor="e"
            ).pack(side="right")
        
        # Texto
        ctk.CTkLabel(
            bubble,
            text=text,
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=text_color,
            wraplength=380,
            justify="left" if is_bot else "right",
            anchor="w" if is_bot else "e"
        ).pack(anchor="w" if is_bot else "e", padx=12, pady=(2 if is_bot else 8, 8))
        
        # Guardar en historial
        self._history.append({
            'sender': sender,
            'text': text,
            'is_bot': is_bot,
            'timestamp': datetime.now().isoformat()
        })
        
        # Auto scroll
        self.root.after(50, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))
    
    def _send_message(self):
        """Envía mensaje con notificación"""
        text = self.input_var.get().strip()
        if not text or self._thinking:
            return
        
        self.input_var.set("")
        self._add_message(USERNAME, text, is_bot=False)
        self._set_thinking(True)
        
        # Animación de pensando
        self._show_typing_indicator()
        
        threading.Thread(target=self._process_message, args=(text,), daemon=True).start()
    
    def _show_typing_indicator(self):
        """Muestra indicador de escritura"""
        self.typing_label = ctk.CTkLabel(
            self.chat_frame,
            text="✨ KALMIYA está escribiendo...",
            font=ctk.CTkFont("Segoe UI", 9, "italic"),
            text_color=self.theme["text_gray"]
        )
        self.typing_label.pack(anchor="w", padx=15, pady=2)
    
    def _remove_typing_indicator(self):
        """Remueve indicador de escritura"""
        if hasattr(self, 'typing_label'):
            self.typing_label.destroy()
    
    def _process_message(self, text):
        """Procesa mensaje"""
        try:
            # Activar modo "hablando"
            self._is_talking = True
            self.root.after(0, self._draw_animated_avatar)
            
            response = ask_kalmiya(text) if BRAIN_OK else "Sistema IA no disponible. Pero estoy aquí para ayudarte con lo que necesites. 💜"
        except Exception as e:
            response = f"Ups, tuve un problema: {str(e)} 😅"
        
        time.sleep(0.5)  # Simular pensamiento
        
        # Desactivar modo "hablando"
        self._is_talking = False
        self.root.after(0, self._draw_animated_avatar)
        
        self.root.after(0, self._on_response, response)
    
    def _on_response(self, response):
        """Recibe respuesta"""
        self._remove_typing_indicator()
        self._set_thinking(False)
        
        # Agregar emoji según respuesta
        if len(response) < 30:
            response = f"💭 {response}"
        elif "error" in response.lower() or "problema" in response.lower():
            response = f"⚠️ {response}"
        
        self._add_message(BOTNAME, response, is_bot=True)
        self._save_history()
    
    def _set_thinking(self, thinking):
        """Estado de pensando"""
        self._thinking = thinking
        self.entry.configure(state="disabled" if thinking else "normal")
        self.send_btn.configure(
            fg_color=self.theme["bg_card"] if thinking else self.theme["accent_primary"],
            text="..." if thinking else "➤"
        )
    
    def _clear_chat(self):
        """Limpia chat"""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        
        clear_messages = [
            "✨ ¡Chat limpiado! Conversación nueva. ¿Qué necesitas?",
            "🗑️ ¡Listo! Todo limpio. ¿En qué te ayudo?",
            "💫 Chat reiniciado. ¿Qué hacemos ahora?",
            "🌟 ¡Perfecto! Espacio limpio. ¿Qué te gustaría saber?"
        ]
        self._add_message(BOTNAME, random.choice(clear_messages), is_bot=True)
    
    def _cycle_theme(self):
        """Cambia al siguiente tema"""
        themes_list = list(THEMES.keys())
        current_idx = themes_list.index(self._current_theme)
        next_idx = (current_idx + 1) % len(themes_list)
        self._current_theme = themes_list[next_idx]
        
        # Notificación
        theme_name = self.theme["name"]
        self._show_notification(f"🎨 Tema cambiado: {theme_name}")
        
        # Reconstruir UI
        self._rebuild_ui()
    
    def _rebuild_ui(self):
        """Reconstruye la UI con el nuevo tema"""
        # Actualizar colores de fondo
        self.root.configure(fg_color=self.theme["bg_dark"])
        
        # Redibujar avatar
        self._draw_animated_avatar()
        
        # Actualizar footer time
        self._update_footer_theme()
        
        # Nota: Para full theme change necesitaríamos rebuild completo
        # Por ahora cambia los elementos críticos
    
    def _update_footer_theme(self):
        """Actualiza colores del footer"""
        try:
            self.time_label.configure(text_color=self.theme["text_gray"])
        except:
            pass
    
    def _toggle_pin(self):
        """Toggle always on top"""
        self._always_on_top = not self._always_on_top
        self.root.attributes("-topmost", self._always_on_top)
        self.pin_btn.configure(text="📌" if self._always_on_top else "📍")
        
        status = "activado" if self._always_on_top else "desactivado"
        self._show_notification(f"📌 Siempre encima: {status}")
    
    def _show_help(self):
        """Muestra ayuda de atajos"""
        help_text = """⌨️ ATAJOS DE TECLADO:

Ctrl+Q - Cerrar chat
Ctrl+L - Limpiar conversación
Ctrl+T - Cambiar tema de color
Ctrl+H - Mostrar esta ayuda
Ctrl+Enter - Enviar mensaje
Esc - Minimizar ventana

🎨 TEMAS DISPONIBLES:
• Cyber Pink 💖
• Cyber Cyan 🌊
• Neon Purple 💜
• Sakura 🌸

✨ CARACTERÍSTICAS:
• Avatar animado con parpadeo
• Historial persistente
• Notificaciones visuales
• Temas de color intercambiables
• Modo siempre encima
• Contador de caracteres"""
        
        self._add_message(BOTNAME, help_text, is_bot=True)
    
    def _show_notification(self, text):
        """Muestra notificación temporal"""
        notif = ctk.CTkLabel(
            self.root,
            text=text,
            font=ctk.CTkFont("Segoe UI", 10),
            fg_color=self.theme["accent_primary"],
            corner_radius=8,
            padx=15,
            pady=5
        )
        notif.place(relx=0.5, rely=0.95, anchor="center")
        
        # Auto-hide después de 2 segundos
        self.root.after(2000, notif.destroy)
    
    def _voice_command(self):
        """Placeholder para comando de voz"""
        self._show_notification("🎤 Función de voz próximamente...")
    
    def _quick_commands(self):
        """Muestra comandos rápidos"""
        commands = """⚡ COMANDOS RÁPIDOS:

1. "¿Qué hora es?" - Hora actual
2. "¿Cómo estás?" - Estado del sistema
3. "Ayuda" - Información de ayuda
4. "Info sistema" - Estadísticas
5. "Cambiar tema" - Ciclar temas

¡Escribe cualquiera de estos o pregúntame lo que necesites! 💜"""
        
        self._add_message(BOTNAME, commands, is_bot=True)
    
    def _load_history_to_chat(self):
        """Carga historial en el chat"""
        if not self._history:
            self._show_notification("📜 No hay historial guardado")
            return
        
        self._clear_chat()
        self._add_message(BOTNAME, f"📜 Cargando últimos {len(self._history)} mensajes...", is_bot=True)
        
        for msg in self._history[-20:]:  # Últimos 20
            self._add_message(
                msg['sender'],
                msg['text'],
                is_bot=msg['is_bot']
            )
    
    def _update_char_count(self, *args):
        """Actualiza contador de caracteres"""
        count = len(self.input_var.get())
        self.char_count.configure(text=str(count))
    
    def _start_animations(self):
        """Inicia animaciones del avatar"""
        threading.Thread(target=self._blink_animation, daemon=True).start()
        threading.Thread(target=self._arm_wave_animation, daemon=True).start()
        threading.Thread(target=self._head_tilt_animation, daemon=True).start()
        threading.Thread(target=self._heart_beat_animation, daemon=True).start()
        threading.Thread(target=self._ear_wiggle_animation, daemon=True).start()
        # NUEVAS animaciones de cuerpo completo
        threading.Thread(target=self._body_bounce_animation, daemon=True).start()
        threading.Thread(target=self._body_sway_animation, daemon=True).start()
        threading.Thread(target=self._body_rotation_animation, daemon=True).start()
        threading.Thread(target=self._update_time, daemon=True).start()
        if PSUTIL_OK:
            threading.Thread(target=self._update_stats, daemon=True).start()
    
    def _blink_animation(self):
        """Animación de parpadeo"""
        while self._running:
            time.sleep(random.uniform(2, 5))  # Parpadeo aleatorio
            if self._running:
                self._blink_state = False
                self.root.after(0, self._draw_animated_avatar)
                time.sleep(0.15)
                self._blink_state = True
                self.root.after(0, self._draw_animated_avatar)
    
    def _arm_wave_animation(self):
        """Animación de brazos (arriba, medio, abajo)"""
        while self._running:
            # Ciclo: arriba → medio → abajo → medio → arriba
            positions = [0, 1, 2, 1]
            for pos in positions:
                if not self._running:
                    break
                self._arm_position = pos
                self.root.after(0, self._draw_animated_avatar)
                time.sleep(1.5)  # 1.5s por posición
            time.sleep(random.uniform(3, 6))  # Pausa entre ciclos
    
    def _head_tilt_animation(self):
        """Animación de cabeza (inclina levemente)"""
        while self._running:
            # Ciclo: centro → izq → centro → der → centro
            tilts = [0, -1, -2, -1, 0, 1, 2, 1, 0]
            for tilt in tilts:
                if not self._running:
                    break
                self._head_tilt = tilt
                self.root.after(0, self._draw_animated_avatar)
                time.sleep(0.3)  # Movimiento suave
            time.sleep(random.uniform(5, 10))  # Pausa entre ciclos
    
    def _heart_beat_animation(self):
        """Animación de corazón (late)"""
        while self._running:
            # Late: normal → grande → normal
            for _ in range(2):  # 2 latidos
                if not self._running:
                    break
                self._heart_size = 1
                self.root.after(0, self._draw_animated_avatar)
                time.sleep(0.15)
                self._heart_size = 0
                self.root.after(0, self._draw_animated_avatar)
                time.sleep(0.15)
            time.sleep(random.uniform(2, 4))  # Pausa entre latidos
    
    def _ear_wiggle_animation(self):
        """Animación de orejas (mueven)"""
        while self._running:
            # Wiggle: normal → izq → normal → der → normal
            wiggles = [0, 1, 0, 2, 0]
            for wiggle in wiggles:
                if not self._running:
                    break
                self._ear_wiggle = wiggle
                self.root.after(0, self._draw_animated_avatar)
                time.sleep(0.2)
            time.sleep(random.uniform(8, 15))  # Pausa entre wiggles
    
    def _body_bounce_animation(self):
        """NUEVA: Animación de salto/rebote (cuerpo sube y baja)"""
        while self._running:
            # Rebote: normal → sube → normal → mini rebote
            bounces = [0, 2, 4, 6, 8, 6, 4, 2, 0, 1, 0]
            for bounce in bounces:
                if not self._running:
                    break
                self._body_bounce = bounce
                self.root.after(0, self._draw_animated_avatar)
                time.sleep(0.08)  # Rápido para efecto realista
            time.sleep(random.uniform(6, 12))  # Pausa entre rebotes
    
    def _body_sway_animation(self):
        """NUEVA: Animación de balanceo lateral (izq/der)"""
        while self._running:
            # Balanceo suave: centro → izq → centro → der → centro
            sways = [0, -1, -2, -3, -4, -3, -2, -1, 0, 1, 2, 3, 4, 3, 2, 1, 0]
            for sway in sways:
                if not self._running:
                    break
                self._body_sway = sway
                self.root.after(0, self._draw_animated_avatar)
                time.sleep(0.15)  # Balanceo suave
            time.sleep(random.uniform(10, 18))  # Pausa entre balanceos
    
    def _body_rotation_animation(self):
        """NUEVA: Animación de rotación leve (gira ligeramente)"""
        while self._running:
            # Rotación leve: centro → der → centro → izq → centro
            rotations = [0, 1, 2, 1, 0, -1, -2, -1, 0]
            for rotation in rotations:
                if not self._running:
                    break
                self._body_rotation = rotation
                self.root.after(0, self._draw_animated_avatar)
                time.sleep(0.25)  # Rotación lenta
            time.sleep(random.uniform(12, 20))  # Pausa entre rotaciones
    
    def _update_time(self):
        """Actualiza reloj"""
        while self._running:
            try:
                current_time = datetime.now().strftime("%H:%M")
                self.root.after(0, lambda: self.time_label.configure(text=current_time))
            except:
                pass
            time.sleep(30)
    
    def _update_stats(self):
        """Actualiza stats del sistema"""
        while self._running:
            try:
                cpu = psutil.cpu_percent(interval=1)
                ram = psutil.virtual_memory().percent
                disk = psutil.disk_usage('C:\\' if sys.platform == 'win32' else '/').percent
                
                text = f"CPU: {cpu:.0f}% | RAM: {ram:.0f}% | Disco: {disk:.0f}%"
                self.root.after(0, lambda: self.stats_label.configure(text=text))
            except:
                pass
            time.sleep(5)
    
    def _get_greeting(self):
        """Saludo según hora"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return random.choice(["Buenos días", "¡Buenos días!", "Buen día"])
        elif 12 <= hour < 19:
            return random.choice(["Buenas tardes", "¡Buenas tardes!", "Buena tarde"])
        else:
            return random.choice(["Buenas noches", "¡Buenas noches!", "Buena noche"])
    
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
        """Minimiza ventana"""
        self.root.overrideredirect(False)
        self.root.iconify()
        self.root.after(500, lambda: self.root.overrideredirect(True))
    
    def _on_close(self):
        """Cierra aplicación"""
        self._running = False
        self._save_history()
        self.root.destroy()
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()


def main():
    """Función main"""
    chat = KalmiyaChatUltra()
    chat.run()


if __name__ == "__main__":
    main()
