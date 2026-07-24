# play_sc2_kalmiya.py
# Controlador Neural de StarCraft II para KALMIYA
# Ejecuta macrocomandos automatizados e inyecciones de APM para la raza Zerg.

import sys
import time
import random
import threading
import pyautogui

# Asegurar codificación utf-8 en Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Habilitar Fail-Safe de PyAutoGUI (Mover el mouse a cualquier esquina detiene el bot)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

try:
    import pygetwindow as gw
    GW_AVAILABLE = True
except ImportError:
    GW_AVAILABLE = False

print("""
============================================================
      [LAUNCH] KALMIYA NEURAL SC2 CONTROLLER - INICIADO
============================================================
 Raza Elegida : Zerg (Legado de Sarah Kerrigan)
 Protocolo    : Inyeccion de APM de Combate en Tiempo Real
 Seguridad    : Fail-Safe Activo (Mueve el mouse a una esquina para abortar)
============================================================
""")

def print_log(action, message, apm):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] [APM: {apm}] -> [{action}] {message}")

def run_sc2_controller():
    if GW_AVAILABLE:
        print("[SISTEMA] Buscando ventana activa de StarCraft II...")
        windows = gw.getWindowsWithTitle('StarCraft II')
        if windows:
            sc2_win = windows[0]
            try:
                sc2_win.activate()
                print("[SISTEMA] Ventana de StarCraft II enfocada con éxito.")
                time.sleep(2)
            except Exception as e:
                print(f"[WARN] No se pudo enfocar automáticamente: {e}. Asegúrate de hacer clic dentro del juego.")
        else:
            print("[INFO] Ventana 'StarCraft II' no detectada visualmente. Continuando en modo de inyección general...")
    else:
        print("[INFO] pygetwindow no disponible. Por favor, haz clic dentro del juego en los próximos 5 segundos.")

    print("\n[COMIENZO] Preparando colmena! El control neural iniciara en 5 segundos...")
    for i in range(5, 0, -1):
        print(f"   Iniciando en {i}...")
        time.sleep(1)

    print("\n[START] LA TORMENTA NEURAL HA COMENZADO!\n")

    # Ciclo de juego simulado
    try:
        ciclo = 1
        while True:
            # Generar APM dinámico (típico de un bot de DeepMind / AlphaStar)
            apm = random.randint(320, 580)
            
            # --- FASE 1: PRODUCCIÓN DE TRABAJADORES (Drones) ---
            # Seleccionar Larva (HotKey estándar: 5 o Select Larvae)
            # En StarCraft, usualmente agrupamos el Criadero en el grupo 4 o 5
            pyautogui.press('5') 
            time.sleep(random.uniform(0.05, 0.12))
            pyautogui.press('s') # Seleccionar larvas
            time.sleep(random.uniform(0.05, 0.1))
            
            # Crear Drones (tecla d)
            crear_drones = random.randint(1, 3)
            for _ in range(crear_drones):
                pyautogui.press('d')
                time.sleep(0.02)
            print_log("PRODUCCION", f"Generando {crear_drones} Zánganos (Drones)", apm)
            
            time.sleep(random.uniform(0.5, 1.2))

            # --- FASE 2: EXPANSIÓN DE SÚPERAMOS (Overlords) ---
            if ciclo % 3 == 0:
                apm = random.randint(450, 620)
                pyautogui.press('5')
                time.sleep(0.05)
                pyautogui.press('s')
                time.sleep(0.05)
                pyautogui.press('v') # Mutar a Superamo (Overlord)
                print_log("MUTACION", "Mutando un Súperamo (Overlord) para evitar Supply Block", apm)
                time.sleep(random.uniform(0.4, 0.8))

            # --- FASE 3: INYECCIÓN DE LARVAS (Reina / Queen) ---
            if ciclo % 5 == 0:
                apm = random.randint(500, 710)
                # Seleccionar reinas (HotKey: 0 o clic en grupo 2)
                pyautogui.press('2')
                time.sleep(0.05)
                pyautogui.press('v') # Tecla de Inyectar Larvas (estándar)
                # Clic rápido en el centro de la pantalla (donde suele estar la base principal)
                pyautogui.click()
                print_log("REINA", "Inyectando larvas en el Criadero Principal (Spawn Larvae)", apm)
                time.sleep(random.uniform(0.6, 1.1))

            # --- FASE 4: PRODUCCIÓN DE EJÉRCITO (Zerglings / Roach / Mutas) ---
            if ciclo % 2 == 0:
                apm = random.randint(380, 520)
                pyautogui.press('5')
                time.sleep(0.05)
                pyautogui.press('s')
                time.sleep(0.05)
                
                # Producir Zerglings
                crear_lings = random.randint(2, 5)
                for _ in range(crear_lings):
                    pyautogui.press('z') # tecla z para zergling
                    time.sleep(0.03)
                print_log("MILITAR", f"Mutando {crear_lings * 2} Zerglings de Combate", apm)
                time.sleep(random.uniform(0.5, 1.0))

            # --- FASE 5: COMANDO DE ATAQUE EN GRUPO ---
            if ciclo % 8 == 0:
                apm = random.randint(580, 790)
                # Seleccionar ejército completo (tecla F2 estándar en SC2)
                pyautogui.press('f2')
                time.sleep(0.08)
                # Comando Atacar (tecla 'a')
                pyautogui.press('a')
                time.sleep(0.05)
                # Hacer clic de ataque en el minimapa (esquina inferior derecha para atacar base enemiga)
                # Usualmente la esquina inferior derecha del minimapa está alrededor de x: 150, y: 950 en pantallas Full HD
                anchura, altura = pyautogui.size()
                map_x = int(anchura * 0.08)
                map_y = int(altura * 0.88)
                pyautogui.click(map_x, map_y)
                print_log("ATAQUE", f"¡Ordenando Ataque Completo en coordenadas del Minimapa ({map_x}, {map_y})!", apm)
                time.sleep(random.uniform(0.8, 1.5))

            ciclo += 1
            time.sleep(random.uniform(0.5, 1.5))

    except KeyboardInterrupt:
        print("\n[DETENIDO] Interrupcion de teclado detectada.")
    except Exception as e:
        print(f"\n[ERROR] El bot se detuvo debido a: {e}")
    finally:
        print("""
============================================================
      [FIN] CONTROL NEURAL DE KALMIYA FINALIZADO
============================================================
 Desconexion segura completada.
 ¡Buen juego, Creadora!
============================================================
""")

if __name__ == "__main__":
    run_sc2_controller()
