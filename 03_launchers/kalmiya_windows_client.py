import requests
import time
import os

# Este es un cliente ligero (Opción 2) que correría en Windows.
# Su único objetivo es escuchar eventos locales (teclado, micrófono)
# y enviarlos al servidor de KALMIYA que corre en Docker.

DOCKER_SERVER_URL = os.environ.get("KALMIYA_SERVER_URL", "http://localhost:5000")

def send_activity(activity_type, data):
    """Envía una actividad al servidor de Docker"""
    try:
        # En una implementación real, aquí habría un endpoint en el Dashboard
        # para recibir texto o comandos de voz. Por ahora comprobamos estado.
        response = requests.get(f"{DOCKER_SERVER_URL}/api/status")
        if response.status_code == 200:
            print(f"[KALMIYA Docker] Servidor alcanzable. Enviando: {activity_type}")
    except requests.exceptions.ConnectionError:
        print("[Error] No se pudo conectar al servidor KALMIYA en Docker.")

def main():
    print("Iniciando KALMIYA Client Ligero (Sentidos en Windows)...")
    print(f"Conectando a Cerebro en Docker: {DOCKER_SERVER_URL}")
    print("Presiona Ctrl+C para salir.")
    
    try:
        while True:
            # Aquí iría la lógica de escuchar pynput (teclado global) o el micrófono
            # simulado por ahora:
            time.sleep(5)
            send_activity("heartbeat", {"status": "listening"})
    except KeyboardInterrupt:
        print("\nCliente apagado.")

if __name__ == "__main__":
    main()
