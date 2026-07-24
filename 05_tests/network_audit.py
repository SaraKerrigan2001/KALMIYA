import sys
import os
import json

# Ensure we can import from the main directory
sys.path.insert(0, r'c:\Users\maria\env\KALMIYA_System')

from security_ops import scan_network
from phone_bridge import get_connected_devices
import sqlite3

def audit():
    print("=== KALMIYA NETWORK AUDIT ===")
    
    # 1. Scan network
    try:
        devices = scan_network()
    except Exception as e:
        print(f"Error scanning network: {e}")
        devices = []
    
    # 2. Count "cell phones"
    # Mobile vendors and common hostnames
    mobile_vendors = ['Samsung', 'Apple', 'Google', 'Huawei', 'Xiaomi', 'Motorola', 'Oppo', 'Vivo', 'LG', 'Realme']
    mobile_keywords = ['phone', 'android', 'iphone', 'sm-', 'pixel', 'galaxy', 'redmi', 'honor', 'vivo', 'oppo']
    
    mobile_count = 0
    detected_mobiles = []
    
    for d in devices:
        is_mobile = False
        vendor = d.get('vendor', 'Desconocido')
        hostname = d.get('hostname', 'Desconocido').lower()
        
        if any(v.lower() in vendor.lower() for v in mobile_vendors):
            is_mobile = True
        elif any(k in hostname for k in mobile_keywords):
            is_mobile = True
        
        if is_mobile:
            mobile_count += 1
            detected_mobiles.append(d)
    
    print(f"\nDispositivos detectados en total: {len(devices)}")
    print(f"Dispositivos que parecen celulares: {mobile_count}")
    for m in detected_mobiles:
        print(f"  - {m['ip']} | {m['hostname']} | {m['vendor']}")

    # 3. Check for "anonymous" messages in DB
    print("\n=== ANONYMOUS MESSAGE CHECK ===")
    db_path = r'c:\Users\maria\env\KALMIYA_System\kalmiya.db'
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Search for "anon" or sources that aren't 'voice' or 'ui'
        try:
            cursor.execute("SELECT * FROM command_history WHERE command LIKE '%anon%' OR source NOT IN ('voice', 'ui')")
            rows = cursor.fetchall()
            if rows:
                print(f"Se encontraron {len(rows)} posibles mensajes/comandos anomalos o anonimos:")
                for row in rows:
                    print(f"  [{row[1]}] Source: {row[4]} | CMD: {row[2]}")
            else:
                print("No se detectaron mensajes anonimos registrados en el historial.")
        except Exception as e:
            print(f"Error checking DB: {e}")
        conn.close()
    else:
        print("Base de datos no encontrada.")

if __name__ == "__main__":
    audit()
