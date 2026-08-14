"""
vision_chat_integration.py — Integración de Visión con Chat
============================================================
Permite que KALMIYA pueda ver a través de la cámara mientras chateas.
"""

import cv2
import threading
import time
from typing import Optional, Callable
from pathlib import Path

try:
    from .camera_recognition import KalmiyaVision
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False


class VisionChatIntegration:
    """
    Integración del sistema de visión con el chat
    """
    
    def __init__(self, on_person_detected: Optional[Callable] = None):
        """
        Args:
            on_person_detected: Callback cuando se detecta una persona (name, confidence)
        """
        self.vision = KalmiyaVision() if VISION_AVAILABLE else None
        self.on_person_detected = on_person_detected
        
        self._running = False
        self._thread = None
        self._last_detection = {}
        self._detection_cooldown = 5.0  # No notificar la misma persona cada 5 segundos
    
    def start_monitoring(self):
        """Inicia el monitoreo visual en segundo plano"""
        if not VISION_AVAILABLE or not self.vision:
            print("[VISION-CHAT] Sistema de visión no disponible")
            return False
        
        if self._running:
            print("[VISION-CHAT] Ya está monitoreando")
            return False
        
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        
        print("[VISION-CHAT] Monitoreo visual iniciado")
        return True
    
    def stop_monitoring(self):
        """Detiene el monitoreo visual"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        print("[VISION-CHAT] Monitoreo visual detenido")
    
    def _monitor_loop(self):
        """Loop de monitoreo en segundo plano"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[VISION-CHAT] No se pudo abrir la cámara")
            self._running = False
            return
        
        try:
            while self._running:
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.5)
                    continue
                
                # Reconocer rostros
                faces = self.vision.recognize_faces(frame)
                
                # Procesar detecciones
                current_time = time.time()
                for face in faces:
                    if not face['known']:
                        continue
                    
                    name = face['name']
                    confidence = face['confidence']
                    
                    # Verificar cooldown
                    if name in self._last_detection:
                        if current_time - self._last_detection[name] < self._detection_cooldown:
                            continue
                    
                    # Notificar detección
                    self._last_detection[name] = current_time
                    
                    if self.on_person_detected:
                        self.on_person_detected(name, confidence)
                
                # Pausa para no saturar CPU
                time.sleep(1.0)
        
        finally:
            cap.release()
    
    def get_current_view(self) -> Optional[str]:
        """
        Obtiene una descripción de lo que KALMIYA está viendo ahora
        
        Returns:
            Descripción textual de la vista actual
        """
        if not VISION_AVAILABLE or not self.vision:
            return None
        
        # Capturar frame actual
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "No puedo acceder a la cámara"
        
        try:
            ret, frame = cap.read()
            if not ret:
                return "Error capturando imagen"
            
            # Reconocer
            faces = self.vision.recognize_faces(frame)
            
            if len(faces) == 0:
                return "No veo a nadie en este momento"
            
            # Describir lo que ve
            descriptions = []
            for face in faces:
                if face['known']:
                    name = face['name']
                    conf = face['confidence']
                    descriptions.append(f"{name} (confianza {conf:.0%})")
                else:
                    descriptions.append("una persona desconocida")
            
            if len(descriptions) == 1:
                return f"Veo a {descriptions[0]}"
            else:
                return f"Veo a {', '.join(descriptions[:-1])} y {descriptions[-1]}"
        
        finally:
            cap.release()
    
    def learn_current_person(self, name: str) -> bool:
        """
        Aprende el rostro de la persona actual frente a la cámara
        
        Args:
            name: Nombre de la persona
            
        Returns:
            True si se aprendió correctamente
        """
        if not VISION_AVAILABLE or not self.vision:
            return False
        
        return self.vision.learn_face(name, num_samples=10)
    
    def who_am_i_looking_at(self) -> list:
        """
        Retorna lista de personas que KALMIYA está viendo
        
        Returns:
            Lista de nombres detectados
        """
        view = self.get_current_view()
        if not view or "No veo" in view or "Error" in view:
            return []
        
        # Extraer nombres de la descripción
        # Esto es simplificado, en producción usar el resultado directo
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return []
        
        try:
            ret, frame = cap.read()
            if not ret:
                return []
            
            faces = self.vision.recognize_faces(frame)
            return [f['name'] for f in faces if f['known']]
        
        finally:
            cap.release()


# Comandos de chat para integración
VISION_COMMANDS = {
    "¿me ves?": "get_current_view",
    "quien soy": "who_am_i_looking_at",
    "aprender mi rostro": "learn_current_person",
    "quien hay aqui": "get_current_view",
    "que ves": "get_current_view",
}


def process_vision_command(command: str, integration: VisionChatIntegration) -> Optional[str]:
    """
    Procesa comandos relacionados con visión en el chat
    
    Args:
        command: Comando del usuario (texto)
        integration: Instancia de VisionChatIntegration
        
    Returns:
        Respuesta o None si no es comando de visión
    """
    command_lower = command.lower().strip()
    
    # Comandos de vista
    if any(kw in command_lower for kw in ["¿me ves?", "me ves", "que ves", "quien hay"]):
        return integration.get_current_view()
    
    # Aprender rostro
    if "aprender" in command_lower and ("rostro" in command_lower or "cara" in command_lower):
        # Extraer nombre si está en el comando
        # Ej: "aprender mi rostro, soy Sara"
        if "soy" in command_lower:
            name = command_lower.split("soy")[-1].strip()
            name = name.replace(",", "").replace(".", "").strip()
            if name:
                success = integration.learn_current_person(name.title())
                if success:
                    return f"✅ He aprendido tu rostro, {name.title()}. Ahora te reconoceré."
                else:
                    return "❌ No pude aprender tu rostro. Asegúrate de que la cámara funcione."
        
        return "Para aprender tu rostro, di: 'aprender mi rostro, soy [tu nombre]'"
    
    # Quien soy
    if "quien soy" in command_lower or "quién soy" in command_lower:
        people = integration.who_am_i_looking_at()
        if len(people) == 0:
            return "No reconozco a nadie. ¿Quieres que aprenda tu rostro?"
        elif len(people) == 1:
            return f"Eres {people[0]} 👋"
        else:
            return f"Veo a {', '.join(people)}"
    
    return None
