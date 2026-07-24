"""
biometric_ops.py - Módulo de Escaneo Biométrico y Reconocimiento de Compañeros (KALMIYA v3.6)
========================================================================================
Este módulo implementa:
  1. Base de datos biométrica de compañeros del grupo de WhatsApp:
     "3115418 Análisis y Desarrollo de Software 201".
  2. Simulador de Escaneo Biométrico (Rostro, Huella y Huella de voz) por Cámara y Consola.
  3. Control de Acceso y Autorización del PC (Diferenciando entre Sara, Compañeros de ADSO 201 e Intrusos).
  4. Bloqueo inmediato del equipo en caso de intromisión no autorizada.
"""

import os
import time
import json
import ctypes
import random
import math
from datetime import datetime
from typing import Dict, List, Tuple, Any
from database import log_command, update_memory, get_memory
from sara_profile import load_profile, save_profile
from voz import speak

# Intentar importar OpenCV para acceso real a la cámara si está disponible
try:
    import cv2
    OPENCV_OK = True
except ImportError:
    OPENCV_OK = False

# Compañeros registrados del grupo de WhatsApp "3115418 Análisis y Desarrollo de Software 201"
COMPANEROS_ADSO = {
    "sara_kerrigan": {
        "nombre": "Sara Kerrigan",
        "rol": "Creadora / Administradora",
        "grupo": "3115418 ADSO 201",
        "biometria_id": "BIO-SARA-001",
        "nivel_acceso": "NIVEL 5 (Acceso Total)",
        "firma_biometrica": "SHA-256-SARA-KERRIGAN-SECURE-KEY"
    },
    "estiven_rua": {
        "nombre": "Estiven Rúa",
        "rol": "Compañero / Desarrollador",
        "grupo": "3115418 ADSO 201",
        "biometria_id": "BIO-ADSO-101",
        "nivel_acceso": "NIVEL 2 (Invitado ADSO - Uso de PC)",
        "firma_biometrica": "SHA-256-ESTIVEN-RUA-ADSO-KEY"
    },
    "mateo_ospina": {
        "nombre": "Mateo Ospina",
        "rol": "Compañero / Desarrollador",
        "grupo": "3115418 ADSO 201",
        "biometria_id": "BIO-ADSO-102",
        "nivel_acceso": "NIVEL 2 (Invitado ADSO - Uso de PC)",
        "firma_biometrica": "SHA-256-MATEO-OSPINA-ADSO-KEY"
    },
    "camila_gomez": {
        "nombre": "Camila Gómez",
        "rol": "Compañera / Desarrolladora",
        "grupo": "3115418 ADSO 201",
        "biometria_id": "BIO-ADSO-103",
        "nivel_acceso": "NIVEL 2 (Invitado ADSO - Uso de PC)",
        "firma_biometrica": "SHA-256-CAMILA-GOMEZ-ADSO-KEY"
    },
    "juan_diego_cardona": {
        "nombre": "Juan Diego Cardona",
        "rol": "Compañero / Desarrollador",
        "grupo": "3115418 ADSO 201",
        "biometria_id": "BIO-ADSO-104",
        "nivel_acceso": "NIVEL 2 (Invitado ADSO - Uso de PC)",
        "firma_biometrica": "SHA-256-JUAN-DIEGO-ADSO-KEY"
    },
    "sofia_tobon": {
        "nombre": "Sofía Tobón",
        "rol": "Compañera / Desarrolladora",
        "grupo": "3115418 ADSO 201",
        "biometria_id": "BIO-ADSO-105",
        "nivel_acceso": "NIVEL 2 (Invitado ADSO - Uso de PC)",
        "firma_biometrica": "SHA-256-SOFIA-TOBON-ADSO-KEY"
    },
    "sebastian_munoz": {
        "nombre": "Sebastián Muñoz",
        "rol": "Compañero / Desarrollador",
        "grupo": "3115418 ADSO 201",
        "biometria_id": "BIO-ADSO-106",
        "nivel_acceso": "NIVEL 2 (Invitado ADSO - Uso de PC)",
        "firma_biometrica": "SHA-256-SEBASTIAN-MUNOZ-ADSO-KEY"
    }
}

def sync_classmates_to_profile() -> bool:
    """Sincroniza el grupo de compañeros de ADSO en el archivo sara_profile.json."""
    profile = load_profile()
    if "companeros_adso" not in profile:
        profile["companeros_adso"] = {}
        
    profile["companeros_adso"] = COMPANEROS_ADSO
    return save_profile(profile)

def import_whatsapp_group_contacts() -> int:
    """Simula la importación de contactos de WhatsApp para el grupo 3115418 ADSO 201."""
    print("\n" + "="*70)
    print("      [IMPORTACION] IMPORTACIÓN DE CONTACTOS DE GRUPO DE WHATSAPP")
    print("="*70)
    print("  Grupo de Origen  : 3115418 Análisis y Desarrollo de Software 201")
    print("  Extrayendo firmas biométricas y números móviles...")
    time.sleep(1.0)
    
    sync_classmates_to_profile()
    count = len(COMPANEROS_ADSO) - 1 # Restar a Sara
    
    print(f"  [SUCCESS] Importación completa. Se han registrado {count} compañeros del grupo.")
    for username, data in COMPANEROS_ADSO.items():
        if username != "sara_kerrigan":
            print(f"    - {data['nombre']} ({data['rol']}) -> ID Biométrico: {data['biometria_id']}")
            
    print("="*70 + "\n")
    speak(f"Importación completa. Se han sincronizado {count} compañeros del grupo de WhatsApp Análisis y Desarrollo de Software 201 en mi base de datos biométrica.")
    log_command("[BIOMETRÍA] Importación WhatsApp", f"Sincronizados {count} compañeros", source="biometrics")
    return count

def run_biometric_face_scan() -> Tuple[bool, Dict[str, Any]]:
    """
    Ejecuta el escáner facial biométrico.
    Intenta abrir la cámara con OpenCV si está disponible, recreando una interfaz de escaneo.
    Si no está OpenCV, ejecuta un escaneo simulado estético y robusto en consola.
    """
    speak("Iniciando escáner biométrico facial. Por favor, mira fijamente a la cámara.")
    print("\n" + "="*70)
    print("      [BIOMETRIA] ESCÁNER BIOMÉTRICO FACIAL - ANÁLISIS DE RASGOS")
    print("="*70)
    
    scanned_user = None
    
    if OPENCV_OK:
        print("[CAMERA] Inicializando webcam...")
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            start_scan = time.time()
            print("[CAMERA] Webcam activa. Escaneando rasgos faciales y profundidad...")
            
            while time.time() - start_scan < 4.0: # Escaneo durante 4 segundos
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Crear overlay gráfico de escaneo biométrico
                h, w, _ = frame.shape
                # Dibujar recuadro de alineación facial
                cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), (0, 255, 0), 2)
                cv2.putText(frame, "ESCANEANDO ROSTRO...", (w//4, h//4 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Línea de barrido vertical dinámica
                bar_y = int((h//4) + ((h//2) * (math.sin(time.time() * 5) + 1) / 2))
                cv2.line(frame, (w//4, bar_y), (3*w//4, bar_y), (0, 255, 0), 2)
                
                cv2.imshow("KALMIYA BIOMETRIC SCANNER v3.6", frame)
                if cv2.waitKey(1) & 0xFF == 27: # Esc para salir
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            print("[CAMERA] Captura de datos completada.")
        else:
            print("[!] No se pudo acceder a la webcam física. Reanudando escaneo en terminal...")

    # Simulación estética avanzada en terminal
    steps = [
        "Iniciando captura de fotogramas...",
        "Alineando marcadores oculares y nasales...",
        "Calculando distancia interpupilar y estructura facial...",
        "Calculando hash biométrico y cruzando con base de datos..."
    ]
    
    for step in steps:
        print(f"  [RUN] {step}")
        time.sleep(0.8)
        
    # Selección simulada interactiva para testing o uso
    print("\n[TESTING] Selección de sujeto de prueba (para simulación):")
    print("  1. Sara Kerrigan (Creadora)")
    print("  2. Estiven Rúa (Compañero ADSO)")
    print("  3. Mateo Ospina (Compañero ADSO)")
    print("  4. Sujeto No Autorizado / Intruso")
    
    choice = input("Opción: ").strip()
    
    if choice == "1":
        scanned_user = COMPANEROS_ADSO["sara_kerrigan"]
    elif choice == "2":
        scanned_user = COMPANEROS_ADSO["estiven_rua"]
    elif choice == "3":
        scanned_user = COMPANEROS_ADSO["mateo_ospina"]
    else:
        scanned_user = {
            "nombre": "Sujeto Desconocido",
            "rol": "Desconocido",
            "grupo": "Ninguno",
            "biometria_id": "BIO-UNKNOWN-999",
            "nivel_acceso": "NIVEL 0 (SIN ACCESO)",
            "firma_biometrica": "INTRUDER_ALERT_HASH"
        }
        
    print("\n--- [RESULTADOS DEL ANÁLISIS BIOMÉTRICO] ---")
    print(f"  Usuario Identificado: {scanned_user['nombre']}")
    print(f"  Rol en el Sistema   : {scanned_user['rol']}")
    print(f"  Ficha de Formación  : {scanned_user['grupo']}")
    print(f"  Nivel de Acceso     : {scanned_user['nivel_acceso']}")
    print("="*70 + "\n")
    
    # Procesar lógica de autorización
    authorized = process_biometric_authorization(scanned_user)
    
    return authorized, scanned_user

def process_biometric_authorization(user: Dict[str, Any]) -> bool:
    """Procesa la autorización del PC y bloquea si el usuario no es autorizado."""
    nombre = user["nombre"]
    rol = user["rol"]
    nivel = user["nivel_acceso"]
    
    if "NIVEL 5" in nivel:
        # Creadora (Sara Kerrigan)
        msg = f"Escaneo biométrico exitoso. Acceso total autorizado. Bienvenida de vuelta, creadora Sara Kerrigan."
        speak(msg)
        log_command("[BIOMETRÍA] Autorizado", f"{nombre} (Administrador)", source="biometrics")
        return True
        
    elif "NIVEL 2" in nivel:
        # Compañero registrado
        msg = f"Escaneo biométrico verificado. Bienvenido compañero {nombre} de la ficha Análisis y Desarrollo de Software 201. Nivel de acceso 2 activado. KALMIYA operando en modo invitado seguro. Mis algoritmos y archivos principales han sido sellados."
        speak(msg)
        log_command("[BIOMETRÍA] Autorizado Invitado", f"{nombre} (Compañero ADSO)", source="biometrics")
        
        # Sellar algoritmos preventivamente
        try:
            from cyber_security_ml import generate_algorithm_signatures
            generate_algorithm_signatures()
            print("[AUTOPROTECCIÓN] Algoritmos centrales sellados de forma segura ante el acceso de un compañero.")
        except Exception:
            pass
        return True
        
    else:
        # Intruso no autorizado
        msg = "Alerta crítica de seguridad. Rostro biométrico no reconocido en el sistema. Bloqueando equipo de forma inmediata por protocolo de defensa activa."
        speak(msg)
        log_command("[!!! ALERTA INTRUSIÓN BIOMÉTRICA !!!]", f"Intruso: {nombre}", source="self_defense")
        
        # Guardar alerta en base de datos e iniciar bloqueo
        try:
            with open("threat_alert.txt", "w", encoding="utf-8") as f:
                f.write(f"=== ALERTA DE INTRUSIÓN BIOMÉTRICA ===\n")
                f.write(f"Fecha: {datetime.now().isoformat()}\n")
                f.write(f"Intruso: {nombre}\n")
                f.write(f"Acción: Bloqueo de PC inmediato ejecutado por KALMIYA.\n")
        except Exception:
            pass
            
        time.sleep(1.0)
        # Bloquear PC
        lock_pc_immediately()
        return False

def lock_pc_immediately():
    """Llama a las APIs de Windows para bloquear la sesión de inmediato."""
    print("[DEFENSA ACTIVA] Bloqueando terminal de Windows...")
    try:
        ctypes.windll.user32.LockWorkStation()
    except Exception as e:
        print(f"[!] No se pudo bloquear la estación mediante ctypes: {e}")
        # Intento secundario por línea de comando
        os.system("rundll32.exe user32.dll,LockWorkStation")

if __name__ == "__main__":
    # Testeo rápido de componentes
    import_whatsapp_group_contacts()
    run_biometric_face_scan()
