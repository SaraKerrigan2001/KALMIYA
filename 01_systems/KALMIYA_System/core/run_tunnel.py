# run_tunnel.py
# Script para iniciar el túnel de Cloudflare de KALMIYA en segundo plano y capturar su URL.

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from remote_bridge import start_remote_connection

print("[+] Iniciando conexión remota via Cloudflare...")
result = start_remote_connection("cloudflare")
print("=========================================")
print(f"RESULTADO DEL TÚNEL: {result}")
print("=========================================")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDeteniendo túnel...")
