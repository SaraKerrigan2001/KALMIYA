import cv2
import threading
import time

class VisionAgent:
    """
    Agente de Visión Computacional para KALMIYA.
    Utiliza OpenCV para detectar presencia de usuarios, rostros y analizar el entorno.
    """
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.is_running = False
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.last_detection_time = 0
        self.user_present = False

    def start(self):
        """Inicia el streaming y el análisis en segundo plano."""
        if not self.is_running:
            self.cap = cv2.VideoCapture(self.camera_index)
            self.is_running = True
            threading.Thread(target=self._vision_loop, daemon=True).start()
            print("[VisionAgent] Ojo óptico activado.")

    def stop(self):
        """Detiene la cámara."""
        self.is_running = False
        if self.cap:
            self.cap.release()
        print("[VisionAgent] Ojo óptico desactivado.")

    def _vision_loop(self):
        """Bucle principal de visión."""
        while self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                self.user_present = True
                self.last_detection_time = time.time()
            else:
                if time.time() - self.last_detection_time > 30:
                    self.user_present = False

            time.sleep(1) # Analizar 1 frame por segundo para ahorrar CPU

    def is_user_present(self) -> bool:
        """Retorna si el usuario está activamente frente a la PC."""
        return self.user_present

if __name__ == '__main__':
    agent = VisionAgent()
    agent.start()
    try:
        while True:
            print(f"Usuario presente: {agent.is_user_present()}")
            time.sleep(2)
    except KeyboardInterrupt:
        agent.stop()
