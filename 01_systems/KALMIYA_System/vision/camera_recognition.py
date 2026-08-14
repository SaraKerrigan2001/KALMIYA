"""
camera_recognition.py — KALMIYA Vision System
==============================================
Sistema de reconocimiento visual por cámara.
Permite a KALMIYA:
- Reconocer personas (face recognition)
- Detectar emociones
- Familiarizarse con el entorno
- Registro de interacciones visuales

Modo privacidad: Todo procesamiento es LOCAL, sin APIs externas
"""

import cv2
import numpy as np
from pathlib import Path
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pickle

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("[VISION] face_recognition no instalado. Instala: pip install face-recognition")

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("[VISION] deepface no instalado (opcional para emociones). Instala: pip install deepface")


class KalmiyaVision:
    """
    Sistema de visión de KALMIYA
    Reconocimiento facial y análisis de entorno
    """
    
    def __init__(self, storage_dir: str = None):
        """
        Inicializa el sistema de visión
        
        Args:
            storage_dir: Directorio para almacenar datos de rostros conocidos
        """
        if storage_dir is None:
            storage_dir = Path(__file__).parent / "known_faces"
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True, parents=True)
        
        # Archivos de almacenamiento
        self.faces_file = self.storage_dir / "known_faces.pkl"
        self.metadata_file = self.storage_dir / "faces_metadata.json"
        self.interactions_log = self.storage_dir / "visual_interactions.json"
        
        # Cargar rostros conocidos
        self.known_faces = self._load_known_faces()
        self.face_metadata = self._load_metadata()
        
        # Configuración
        self.camera_index = 0
        self.recognition_threshold = 0.6  # Umbral de similitud
        
        print(f"[VISION] Sistema iniciado")
        print(f"[VISION] Rostros conocidos: {len(self.known_faces)}")
        print(f"[VISION] Modo privacidad: 100% local")
    
    def _load_known_faces(self) -> Dict:
        """Carga rostros conocidos desde archivo"""
        if self.faces_file.exists():
            try:
                with open(self.faces_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"[VISION] Error cargando rostros: {e}")
        return {}
    
    def _save_known_faces(self):
        """Guarda rostros conocidos en archivo"""
        try:
            with open(self.faces_file, 'wb') as f:
                pickle.dump(self.known_faces, f)
        except Exception as e:
            print(f"[VISION] Error guardando rostros: {e}")
    
    def _load_metadata(self) -> Dict:
        """Carga metadata de rostros"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[VISION] Error cargando metadata: {e}")
        return {}
    
    def _save_metadata(self):
        """Guarda metadata de rostros"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.face_metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[VISION] Error guardando metadata: {e}")
    
    def _log_interaction(self, person_name: str, emotion: str = "neutral", 
                        confidence: float = 0.0, notes: str = ""):
        """Registra una interacción visual"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "person": person_name,
            "emotion": emotion,
            "confidence": confidence,
            "notes": notes
        }
        
        # Cargar log existente
        log = []
        if self.interactions_log.exists():
            try:
                with open(self.interactions_log, 'r', encoding='utf-8') as f:
                    log = json.load(f)
            except:
                pass
        
        # Agregar nueva interacción
        log.append(interaction)
        
        # Guardar (mantener últimas 1000 interacciones)
        log = log[-1000:]
        try:
            with open(self.interactions_log, 'w', encoding='utf-8') as f:
                json.dump(log, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[VISION] Error guardando log: {e}")
    
    def learn_face(self, name: str, num_samples: int = 10) -> bool:
        """
        Aprende un nuevo rostro capturando múltiples muestras
        
        Args:
            name: Nombre de la persona
            num_samples: Número de muestras a capturar
            
        Returns:
            True si se aprendió correctamente
        """
        if not FACE_RECOGNITION_AVAILABLE:
            print("[VISION] face_recognition no disponible")
            return False
        
        print(f"\n[VISION] Aprendiendo rostro de '{name}'...")
        print(f"[VISION] Capturando {num_samples} muestras...")
        print("[VISION] Presiona ESPACIO para capturar, Q para salir")
        
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            print("[VISION] Error: No se pudo abrir la cámara")
            return False
        
        encodings = []
        samples_captured = 0
        
        try:
            while samples_captured < num_samples:
                ret, frame = cap.read()
                if not ret:
                    print("[VISION] Error leyendo frame")
                    break
                
                # Detectar rostros
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                
                # Dibujar rectángulos
                display_frame = frame.copy()
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(display_frame, (left, top), (right, bottom), (0, 255, 0), 2)
                
                # Mostrar progreso
                cv2.putText(display_frame, f"Muestras: {samples_captured}/{num_samples}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(display_frame, "ESPACIO: Capturar | Q: Salir", 
                           (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.imshow('KALMIYA Vision - Learning', display_frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                # Capturar muestra
                if key == ord(' ') and len(face_locations) > 0:
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    if len(face_encodings) > 0:
                        encodings.append(face_encodings[0])
                        samples_captured += 1
                        print(f"[VISION] Muestra {samples_captured} capturada")
                        time.sleep(0.3)  # Pequeña pausa
                
                # Salir
                elif key == ord('q'):
                    print("[VISION] Aprendizaje cancelado")
                    break
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
        
        # Verificar que se capturaron suficientes muestras
        if len(encodings) < 3:
            print(f"[VISION] Error: Solo se capturaron {len(encodings)} muestras (mínimo 3)")
            return False
        
        # Guardar encodings
        self.known_faces[name] = encodings
        self._save_known_faces()
        
        # Guardar metadata
        self.face_metadata[name] = {
            "name": name,
            "first_seen": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat(),
            "total_interactions": 0,
            "samples": len(encodings)
        }
        self._save_metadata()
        
        print(f"[VISION] ✅ Rostro de '{name}' aprendido correctamente ({len(encodings)} muestras)")
        return True
    
    def recognize_faces(self, frame: np.ndarray) -> List[Dict]:
        """
        Reconoce rostros en un frame
        
        Args:
            frame: Frame BGR de OpenCV
            
        Returns:
            Lista de diccionarios con información de rostros detectados
        """
        if not FACE_RECOGNITION_AVAILABLE:
            return []
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detectar rostros
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        results = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Buscar coincidencias
            name = "Desconocido"
            confidence = 0.0
            
            for known_name, known_encodings in self.known_faces.items():
                # Comparar con todas las muestras de esta persona
                matches = face_recognition.compare_faces(known_encodings, face_encoding, 
                                                        tolerance=self.recognition_threshold)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                
                if True in matches:
                    # Calcular confianza (1 - distancia promedio)
                    best_match_distance = min(face_distances)
                    match_confidence = 1 - best_match_distance
                    
                    if match_confidence > confidence:
                        name = known_name
                        confidence = match_confidence
            
            # Actualizar metadata si es conocido
            if name != "Desconocido":
                if name in self.face_metadata:
                    self.face_metadata[name]["last_seen"] = datetime.now().isoformat()
                    self.face_metadata[name]["total_interactions"] += 1
                    self._save_metadata()
            
            results.append({
                "name": name,
                "confidence": confidence,
                "location": face_location,  # (top, right, bottom, left)
                "known": name != "Desconocido"
            })
        
        return results
    
    def detect_emotion(self, frame: np.ndarray, face_location: Tuple) -> str:
        """
        Detecta emoción en un rostro (requiere deepface)
        
        Args:
            frame: Frame BGR de OpenCV
            face_location: (top, right, bottom, left)
            
        Returns:
            Emoción detectada
        """
        if not DEEPFACE_AVAILABLE:
            return "neutral"
        
        try:
            top, right, bottom, left = face_location
            face_img = frame[top:bottom, left:right]
            
            # Analizar emoción
            analysis = DeepFace.analyze(face_img, actions=['emotion'], 
                                       enforce_detection=False, silent=True)
            
            if isinstance(analysis, list):
                analysis = analysis[0]
            
            emotion = analysis.get('dominant_emotion', 'neutral')
            return emotion
        
        except Exception as e:
            return "neutral"
    
    def start_recognition_session(self, duration: int = 30, detect_emotions: bool = False):
        """
        Inicia sesión de reconocimiento en vivo
        
        Args:
            duration: Duración en segundos (0 = infinito)
            detect_emotions: Si True, detecta emociones (más lento)
        """
        if not FACE_RECOGNITION_AVAILABLE:
            print("[VISION] face_recognition no disponible")
            return
        
        print(f"\n[VISION] Iniciando sesión de reconocimiento...")
        print(f"[VISION] Presiona Q para salir")
        
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            print("[VISION] Error: No se pudo abrir la cámara")
            return
        
        start_time = time.time()
        frame_count = 0
        last_recognition_time = 0
        recognition_interval = 1.0  # Reconocer cada 1 segundo
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                current_time = time.time()
                elapsed = current_time - start_time
                
                # Verificar duración
                if duration > 0 and elapsed > duration:
                    break
                
                display_frame = frame.copy()
                
                # Reconocer rostros (no en cada frame para rendimiento)
                if current_time - last_recognition_time > recognition_interval:
                    faces = self.recognize_faces(frame)
                    last_recognition_time = current_time
                    
                    # Dibujar resultados
                    for face in faces:
                        top, right, bottom, left = face['location']
                        name = face['name']
                        confidence = face['confidence']
                        
                        # Color según si es conocido
                        color = (0, 255, 0) if face['known'] else (0, 0, 255)
                        
                        # Rectángulo
                        cv2.rectangle(display_frame, (left, top), (right, bottom), color, 2)
                        
                        # Nombre y confianza
                        label = f"{name}"
                        if face['known']:
                            label += f" ({confidence:.1%})"
                        
                        cv2.rectangle(display_frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                        cv2.putText(display_frame, label, (left + 6, bottom - 6),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                        
                        # Detectar emoción si está habilitado
                        if detect_emotions and DEEPFACE_AVAILABLE and face['known']:
                            emotion = self.detect_emotion(frame, face['location'])
                            cv2.putText(display_frame, emotion, (left, top - 10),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                            
                            # Log interacción
                            self._log_interaction(name, emotion, confidence)
                
                # Info en pantalla
                cv2.putText(display_frame, f"KALMIYA Vision | Q: Salir", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(display_frame, f"Rostros conocidos: {len(self.known_faces)}", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                cv2.imshow('KALMIYA Vision', display_frame)
                
                frame_count += 1
                
                # Salir
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            
            fps = frame_count / elapsed if elapsed > 0 else 0
            print(f"\n[VISION] Sesión terminada")
            print(f"[VISION] Duración: {elapsed:.1f}s | Frames: {frame_count} | FPS: {fps:.1f}")
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas del sistema de visión"""
        stats = {
            "known_faces": len(self.known_faces),
            "people": []
        }
        
        for name, metadata in self.face_metadata.items():
            stats["people"].append({
                "name": name,
                "first_seen": metadata.get("first_seen"),
                "last_seen": metadata.get("last_seen"),
                "interactions": metadata.get("total_interactions", 0)
            })
        
        return stats
    
    def forget_face(self, name: str) -> bool:
        """
        Elimina un rostro conocido
        
        Args:
            name: Nombre de la persona a olvidar
            
        Returns:
            True si se eliminó correctamente
        """
        if name in self.known_faces:
            del self.known_faces[name]
            self._save_known_faces()
            
            if name in self.face_metadata:
                del self.face_metadata[name]
                self._save_metadata()
            
            print(f"[VISION] Rostro de '{name}' eliminado")
            return True
        
        print(f"[VISION] '{name}' no está en la base de datos")
        return False


def main():
    """Demo del sistema de visión"""
    print("="*60)
    print("  KALMIYA VISION SYSTEM - Demo")
    print("="*60)
    
    vision = KalmiyaVision()
    
    if not FACE_RECOGNITION_AVAILABLE:
        print("\n❌ Instala face_recognition para usar este módulo:")
        print("   pip install face-recognition opencv-python")
        return
    
    while True:
        print("\n" + "="*60)
        print("1. Aprender nuevo rostro")
        print("2. Iniciar reconocimiento en vivo")
        print("3. Ver estadísticas")
        print("4. Olvidar rostro")
        print("5. Salir")
        print("="*60)
        
        choice = input("\nOpción: ").strip()
        
        if choice == "1":
            name = input("Nombre de la persona: ").strip()
            if name:
                vision.learn_face(name)
        
        elif choice == "2":
            duration = input("Duración en segundos (0 = infinito): ").strip()
            duration = int(duration) if duration.isdigit() else 0
            
            emotions = input("¿Detectar emociones? (s/n): ").strip().lower() == 's'
            
            vision.start_recognition_session(duration, emotions)
        
        elif choice == "3":
            stats = vision.get_statistics()
            print(f"\n{'='*60}")
            print(f"Rostros conocidos: {stats['known_faces']}")
            print(f"{'='*60}")
            for person in stats['people']:
                print(f"\n👤 {person['name']}")
                print(f"   Primera vez: {person['first_seen']}")
                print(f"   Última vez: {person['last_seen']}")
                print(f"   Interacciones: {person['interactions']}")
        
        elif choice == "4":
            name = input("Nombre a olvidar: ").strip()
            if name:
                vision.forget_face(name)
        
        elif choice == "5":
            print("\n[VISION] Adiós!")
            break


if __name__ == "__main__":
    main()
