"""
kalmiya_lupa.py - Acceso Directo por Voz (La Lupa de KALMIYA)
Botón flotante minimalista para hablar con la IA directamente.
Usa STT/TTS completamente locales (privado, sin APIs).
"""

import customtkinter as ctk
import tkinter as tk
import threading
import sys
import os

# Importar audio local (privado)
try:
    from audio.audio_local import listen, speak
except ImportError:
    # Fallback a speech_recognition (con APIs)
    print("[LUPA] ADVERTENCIA: audio_local no disponible, usando fallback con APIs")
    import speech_recognition as sr
    
    def listen(*args, **kwargs):
        """Fallback usando Google Speech Recognition (tiene API)"""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                return r.recognize_google(audio, language="es-ES")
            except:
                return None
    
    from voz import speak

from brain import ask_kalmiya

# Configuración Estética (Match con el HUD)
ACCENT = "#00f2ff"
BG_MAIN = "#0a0a1a"
ACCENT_DIM = "#004d55"

class KalmiyaLupa:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("KALMIYA Lupa")
        
        # Ventana circular pequeña
        self.size = 60
        self.root.geometry(f"{self.size}x{self.size}")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(fg_color=BG_MAIN)
        self.root.wm_attributes("-transparentcolor", BG_MAIN)

        # Posición inicial (abajo a la derecha, cerca del reloj)
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"+{sw - 80}+{sh - 120}")

        self.listening = False
        self._build_ui()
        self._make_draggable()
        
    def _build_ui(self):
        # Canvas para dibujar la lupa
        self.canvas = tk.Canvas(self.root, width=self.size, height=self.size, 
                               bg=BG_MAIN, highlightthickness=0)
        self.canvas.pack()
        
        # Dibujar círculo de la lupa
        self.outer_circle = self.canvas.create_oval(10, 10, 45, 45, outline=ACCENT, width=3)
        # Dibujar mango de la lupa
        self.handle = self.canvas.create_line(42, 42, 55, 55, fill=ACCENT, width=5)
        
        # Efecto de brillo interior
        self.inner_glow = self.canvas.create_oval(15, 15, 40, 40, fill="", outline=ACCENT_DIM, width=1)
        
        self.canvas.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        if not self.listening:
            self.start_listening()

    def start_listening(self):
        self.listening = True
        self.canvas.itemconfig(self.outer_circle, outline="#00ff00") # Verde cuando escucha
        self.canvas.itemconfig(self.handle, fill="#00ff00")
        
        threading.Thread(target=self._listen_worker, daemon=True).start()

    def _listen_worker(self):
        try:
            print("[LUPA] Escuchando... (click izquierdo para activar)")
            query = listen(timeout=3.0, phrase_limit=8.0)
            
            # Volver a color normal
            self.canvas.itemconfig(self.outer_circle, outline=ACCENT)
            self.canvas.itemconfig(self.handle, fill=ACCENT)
            
            if query:
                print(f"[LUPA] Usuario: {query}")
                response = ask_kalmiya(query)
                speak(response)
            else:
                print("[LUPA] No se escuchó nada")
                
        except Exception as e:
            print(f"[LUPA] Error: {e}")
            self.canvas.itemconfig(self.outer_circle, outline=ACCENT)
            self.canvas.itemconfig(self.handle, fill=ACCENT)
        
        self.listening = False

    def _make_draggable(self):
        self.canvas.bind("<ButtonPress-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_motion)

    def _on_drag_start(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag_motion(self, event):
        # Si se mueve mucho, no se considera click
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    lupa = KalmiyaLupa()
    lupa.run()
