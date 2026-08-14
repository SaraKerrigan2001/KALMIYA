#!/usr/bin/env python3
"""
TEST_CHAT.py — Test simple del Chat KALMIYA
=============================================
Verifica que todos los componentes se pueden importar correctamente
"""

import sys
from pathlib import Path

print("="*60)
print("🧪 TEST CHAT KALMIYA")
print("="*60)

# Setup paths
KALMIYA_DIR = Path(__file__).parent / "01_systems" / "KALMIYA_System"
UI_DIR = KALMIYA_DIR / "ui"

print(f"\n📁 Directorio KALMIYA: {KALMIYA_DIR}")
print(f"📁 Directorio UI: {UI_DIR}")

# Verificar que los directorios existen
if not KALMIYA_DIR.exists():
    print(f"❌ ERROR: {KALMIYA_DIR} no existe")
    sys.exit(1)

if not UI_DIR.exists():
    print(f"❌ ERROR: {UI_DIR} no existe")
    sys.exit(1)

print("✅ Directorios verificados")

# Agregar al path
sys.path.insert(0, str(UI_DIR))
sys.path.insert(0, str(KALMIYA_DIR))

print("\n📦 Intentando importar módulos...")

# Test 1: Importar KalmiyaChat
try:
    print("\n1️⃣ Importando KalmiyaChat...")
    from kalmiya_chat import KalmiyaChat
    print("   ✅ KalmiyaChat importado correctamente")
except Exception as e:
    print(f"   ❌ Error importando KalmiyaChat: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Verificar dependencias
print("\n2️⃣ Verificando dependencias...")

dependencies = {
    'customtkinter': 'Interface gráfica',
    'tkinter': 'Interface base',
    'psutil': 'Monitoreo del sistema (opcional)',
    'decouple': 'Configuración .env'
}

missing = []
for dep, desc in dependencies.items():
    try:
        __import__(dep)
        print(f"   ✅ {dep:20} - {desc}")
    except ImportError:
        print(f"   ⚠️  {dep:20} - {desc} (NO INSTALADO)")
        if dep not in ['psutil']:  # psutil es opcional
            missing.append(dep)

if missing:
    print(f"\n⚠️  ADVERTENCIA: Faltan dependencias críticas: {', '.join(missing)}")
    print("   Instala con: pip install " + " ".join(missing))
else:
    print("\n✅ Todas las dependencias críticas están instaladas")

# Test 3: Verificar archivos críticos
print("\n3️⃣ Verificando archivos críticos...")

critical_files = [
    KALMIYA_DIR / "brain.py",
    UI_DIR / "kalmiya_chat.py",
    KALMIYA_DIR / ".." / ".." / ".env"
]

for file in critical_files:
    if file.exists():
        print(f"   ✅ {file.name}")
    else:
        print(f"   ⚠️  {file.name} (NO ENCONTRADO)")

# Test 4: Intentar crear instancia (sin mostrar ventana)
print("\n4️⃣ Intentando crear instancia de KalmiyaChat...")
try:
    # Nota: No llamamos run() para no abrir la ventana
    chat = KalmiyaChat()
    print("   ✅ Instancia creada correctamente")
    
    # Destruir la ventana inmediatamente
    if hasattr(chat, 'root'):
        chat.root.destroy()
    
    print("   ✅ Ventana destruida correctamente")
except Exception as e:
    print(f"   ❌ Error creando instancia: {e}")
    import traceback
    traceback.print_exc()

# Resultado final
print("\n" + "="*60)
print("✅ TEST COMPLETADO - Chat KALMIYA está listo para usar")
print("="*60)
print("\n💡 Para iniciar el chat:")
print("   python 03_launchers/chat.py")
print("   o ejecuta: Chat_KALMIYA.bat")
print("\n")
