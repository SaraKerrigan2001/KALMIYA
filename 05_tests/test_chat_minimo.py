"""
Test MÍNIMO - Ventana que DEBE aparecer
"""
import customtkinter as ctk
import sys
import os

# Agregar path al brain
sys.path.insert(0, r"C:\Users\maria\env\01_systems\KALMIYA_System\ui")

print("=" * 60)
print("🔧 INICIANDO TEST CHAT MÍNIMO")
print("=" * 60)

# Configuración mínima
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

print("\n1️⃣ Creando ventana...")
root = ctk.CTk()
root.title("✨ KALMIYA TEST ✨")

# FORZAR aparecer - MÁXIMA prioridad
root.attributes("-topmost", True)
root.geometry("400x500+100+100")  # Posición absoluta
root.configure(fg_color="#1a0a1f")

print("2️⃣ Ventana creada")

# Contenido visible
frame = ctk.CTkFrame(root, fg_color="#2d1b3d", corner_radius=15)
frame.pack(fill="both", expand=True, padx=20, pady=20)

title = ctk.CTkLabel(
    frame,
    text="✨ KALMIYA ULTRA ✨",
    font=("Arial", 28, "bold"),
    text_color="#ff6ec7"
)
title.pack(pady=30)

msg = ctk.CTkLabel(
    frame,
    text="Si ves esta ventana,\nel chat funciona ✅",
    font=("Arial", 18),
    text_color="white"
)
msg.pack(pady=20)

btn_cerrar = ctk.CTkButton(
    frame,
    text="CERRAR",
    command=root.quit,
    width=200,
    height=50,
    font=("Arial", 16),
    fg_color="#ff6ec7",
    hover_color="#c74dff"
)
btn_cerrar.pack(pady=30)

print("3️⃣ Contenido agregado")
print("\n🚀 Mostrando ventana...")
print("   → Debería aparecer en posición (100, 100)")
print("   → Siempre al frente (-topmost)")
print("   → Fondo morado/rosa\n")

# FORZAR visibilidad
root.update()
root.deiconify()
root.lift()
root.focus_force()

print("✅ Entrando a mainloop...")
print("   (La ventana DEBE estar visible ahora)\n")

root.mainloop()

print("\n👋 Ventana cerrada")
print("=" * 60)
