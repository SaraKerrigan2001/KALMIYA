"""
Launcher DEBUG del Chat Ultra - Muestra errores
"""
import sys
import os

print("=" * 70)
print("🔧 CHAT KALMIYA ULTRA v3.7 - DEBUG MODE")
print("=" * 70)

# Paths
workspace = r"C:\Users\maria\env"
ui_path = os.path.join(workspace, "01_systems", "KALMIYA_System", "ui")

print(f"\n📁 Workspace: {workspace}")
print(f"📁 UI Path: {ui_path}")

# Agregar paths
sys.path.insert(0, ui_path)
sys.path.insert(0, workspace)

print("\n1️⃣ Importando módulos...")
try:
    import customtkinter as ctk
    print("   ✅ customtkinter")
except Exception as e:
    print(f"   ❌ customtkinter: {e}")
    sys.exit(1)

try:
    from kalmiya_chat_ultra import KalmiyaChatUltra
    print("   ✅ KalmiyaChatUltra")
except Exception as e:
    print(f"   ❌ KalmiyaChatUltra: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n2️⃣ Creando instancia del chat...")
try:
    app = KalmiyaChatUltra()
    print("   ✅ Instancia creada")
except Exception as e:
    print(f"   ❌ Error al crear instancia: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3️⃣ Iniciando mainloop...")
print("   → La ventana debería aparecer AHORA")
print("   → Si no aparece, hay un problema con customtkinter o tkinter\n")

try:
    app.run()
    print("\n✅ Chat cerrado normalmente")
except KeyboardInterrupt:
    print("\n⚠️  Cerrado por usuario (Ctrl+C)")
except Exception as e:
    print(f"\n❌ Error en mainloop: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
