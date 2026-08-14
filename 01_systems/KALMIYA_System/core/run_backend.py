# run_backend.py
# Script de ejecucion para levantar todos los servidores web de KALMIYA sin interfaz grafica bloqueante.
# Esto asegura que los tuneles remotos (como Cloudflare) sean 100% funcionales.

import os
import sys
import time
import threading

# Asegurar imports del proyecto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("==================================================")
print("   INICIANDO SERVIDORES BACKEND DE KALMIYA")
print("==================================================")

# 0. Inicializar base de datos y desactivar voz temporalmente (evita cuelgues por falta de tarjeta de sonido)
try:
    from database import init_db, update_memory
    print("[+] Inicializando base de datos...")
    init_db()
    print("[+] Desactivando salida de voz fisica (modo silencioso)...")
    update_memory('voice_enabled', 'false')
    print("[OK] Base de datos y modo silencioso configurados.")
except Exception as e:
    print(f"[!] Advertencia al inicializar base de datos: {e}")

# 1. Iniciar phone_bridge (puente movil en puerto 8765)
try:
    print("[+] Iniciar phone_bridge en puerto 8765...")
    from phone_bridge import start_bridge
    start_bridge(show_qr=False)
    print("[OK] phone_bridge iniciado con exito.")
except Exception as e:
    print(f"[!] Error al iniciar phone_bridge: {e}")

# 2. Iniciar kalmiya_server (dashboard en puerto 5000)
try:
    print("[+] Iniciar kalmiya_server en puerto 5000...")
    from kalmiya_server import run_server
    server_thread = threading.Thread(target=run_server, daemon=True, name="kalmiya-server")
    server_thread.start()
    print("[OK] kalmiya_server iniciado con exito.")
except Exception as e:
    print(f"[!] Error al iniciar kalmiya_server: {e}")

# 3. Iniciar family_projection (servidor familiar en puerto 8766)
try:
    print("[+] Iniciar family_projection en puerto 8766...")
    from family_projection import start_family_server
    projection_thread = threading.Thread(target=start_family_server, daemon=True, name="family-projection")
    projection_thread.start()
    print("[OK] family_projection iniciado con exito.")
except Exception as e:
    print(f"[!] Error al iniciar family_projection: {e}")

print("==================================================")
print("   SISTEMA DE SERVIDORES BACKEND ACTIVO")
print("   Los tuneles Cloudflare/Ngrok ahora son funcionales.")
print("   Presiona Ctrl+C para detener.")
print("==================================================")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDeteniendo servidores...")
