"""
Test simple para verificar que ventana aparece
"""
import customtkinter as ctk
import sys

print("🔧 Creando ventana de prueba...")

# Crear ventana
root = ctk.CTk()
root.title("TEST - ¿Me ves?")
root.geometry("400x300+100+100")  # Posición absoluta esquina superior
root.attributes("-topmost", True)

# Contenido visible
label = ctk.CTkLabel(
    root, 
    text="✅ SI VES ESTA VENTANA\nDime: SI",
    font=("Arial", 24, "bold"),
    text_color="white"
)
label.pack(expand=True)

button = ctk.CTkButton(
    root,
    text="CERRAR",
    command=root.quit,
    width=200,
    height=50,
    font=("Arial", 16)
)
button.pack(pady=20)

print("✅ Ventana creada")
print("📍 Posición: 100x100 (esquina superior izquierda)")
print("⏳ Esperando... (debería aparecer AHORA)")

# Forzar aparecer
root.update()
root.deiconify()
root.lift()
root.focus_force()

print("🚀 Entrando a mainloop...")
root.mainloop()
print("👋 Ventana cerrada")
