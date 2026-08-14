"""
Chat KALMIYA Simple - Usando TKINTER PURO
Versión que SÍ se muestra en Windows
"""
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import sys
import os
from datetime import datetime

# Agregar paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from brain import ask_kalmiya
    BRAIN_OK = True
except:
    BRAIN_OK = False
    def ask_kalmiya(q: str, **kwargs) -> str:
        return "🤖 Brain.py no disponible. Soy KALMIYA en modo demo."

from decouple import config
USERNAME = config('USER', default='Sara')
BOTNAME = config('BOTNAME', default='KALMIYA')

# Configuración
CHAT_W = 500
CHAT_H = 700

# Colores
COLOR_BG = "#1a0a1f"
COLOR_CARD = "#2d1b3d"
COLOR_INPUT = "#3d2550"
COLOR_ACCENT = "#ff6ec7"
COLOR_TEXT = "#ffffff"
COLOR_GRAY = "#c9b3d4"

class KalmiyaChatSimple:
    """Chat KALMIYA usando tkinter puro"""
    
    def __init__(self):
        self.history = []
        self._build_ui()
        
    def _build_ui(self):
        """Construir interfaz"""
        self.root = tk.Tk()
        self.root.title(f"✨ {BOTNAME} Chat ✨")
        self.root.geometry(f"{CHAT_W}x{CHAT_H}+100+100")
        self.root.configure(bg=COLOR_BG)
        
        # FORZAR al frente
        self.root.attributes("-topmost", True)
        self.root.after(1000, lambda: self.root.attributes("-topmost", False))
        
        # Header
        header = tk.Frame(self.root, bg=COLOR_CARD, height=80)
        header.pack(fill="x", padx=10, pady=(10, 5))
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text=f"✨ {BOTNAME} ✨",
            font=("Arial", 20, "bold"),
            bg=COLOR_CARD,
            fg=COLOR_ACCENT
        )
        title.pack(expand=True)
        
        # Área de chat
        chat_frame = tk.Frame(self.root, bg=COLOR_BG)
        chat_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            insertbackground=COLOR_ACCENT,
            relief="flat",
            padx=10,
            pady=10
        )
        self.chat_area.pack(fill="both", expand=True)
        self.chat_area.config(state="disabled")
        
        # Input
        input_frame = tk.Frame(self.root, bg=COLOR_BG)
        input_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.input_entry = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bg=COLOR_INPUT,
            fg=COLOR_TEXT,
            insertbackground=COLOR_ACCENT,
            relief="flat",
            bd=10
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.input_entry.bind("<Return>", lambda e: self._send_message())
        self.input_entry.focus()
        
        btn_send = tk.Button(
            input_frame,
            text="Enviar",
            font=("Arial", 11, "bold"),
            bg=COLOR_ACCENT,
            fg="white",
            activebackground="#c74dff",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            command=self._send_message,
            cursor="hand2"
        )
        btn_send.pack(side="right")
        
        # Footer
        footer = tk.Label(
            self.root,
            text="Enter para enviar • Versión Simple con Tkinter",
            font=("Arial", 8),
            bg=COLOR_BG,
            fg=COLOR_GRAY
        )
        footer.pack(pady=(0, 5))
        
        # Mensaje de bienvenida
        self._add_message("bot", f"¡Hola {USERNAME}! 👋 Soy {BOTNAME}. ¿En qué puedo ayudarte?")
        
    def _add_message(self, sender: str, text: str):
        """Agregar mensaje al chat"""
        self.chat_area.config(state="normal")
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "user":
            prefix = f"[{timestamp}] {USERNAME}: "
            self.chat_area.insert("end", prefix, "user_name")
            self.chat_area.insert("end", f"{text}\n\n", "user_msg")
        else:
            prefix = f"[{timestamp}] {BOTNAME}: "
            self.chat_area.insert("end", prefix, "bot_name")
            self.chat_area.insert("end", f"{text}\n\n", "bot_msg")
        
        # Estilos
        self.chat_area.tag_config("user_name", foreground=COLOR_ACCENT, font=("Arial", 10, "bold"))
        self.chat_area.tag_config("user_msg", foreground=COLOR_TEXT)
        self.chat_area.tag_config("bot_name", foreground="#00d9ff", font=("Arial", 10, "bold"))
        self.chat_area.tag_config("bot_msg", foreground=COLOR_GRAY)
        
        self.chat_area.config(state="disabled")
        self.chat_area.see("end")
        
    def _send_message(self):
        """Enviar mensaje"""
        user_text = self.input_entry.get().strip()
        if not user_text:
            return
        
        self.input_entry.delete(0, "end")
        self._add_message("user", user_text)
        
        # Procesar en hilo separado
        threading.Thread(target=self._process_response, args=(user_text,), daemon=True).start()
        
    def _process_response(self, user_text: str):
        """Procesar respuesta del bot"""
        if BRAIN_OK:
            try:
                response = ask_kalmiya(user_text, username=USERNAME)
            except Exception as e:
                response = f"Error: {str(e)}"
        else:
            response = "🤖 Brain.py no disponible. Estoy en modo demo."
        
        self.root.after(0, lambda: self._add_message("bot", response))
        
    def run(self):
        """Iniciar aplicación"""
        print("✅ Ventana creada - Iniciando mainloop...")
        self.root.mainloop()


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 INICIANDO CHAT KALMIYA SIMPLE")
    print("=" * 60)
    app = KalmiyaChatSimple()
    app.run()
