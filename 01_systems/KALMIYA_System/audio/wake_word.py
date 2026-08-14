"""
KALMIYA Wake Word Detection v3.6
Detección de palabra de activación "Hey KALMIYA" sin presionar teclas
Usa Pocketsphinx (open-source) como alternativa a Porcupine
"""

import speech_recognition as sr
from pocketsphinx import LiveSpeech, get_model_path
import threading
import time
from pathlib import Path
from typing import Callable, Optional
import json
from datetime import datetime

class WakeWordDetector:
    """
    Detector de wake word para KALMIYA
    Escucha continuamente por "Hey KALMIYA" o palabra personalizada
    """
    
    def __init__(self, wake_words: list = None, sensitivity: float = 0.5):
        """
        Inicializa el detector
        
        Args:
            wake_words: Lista de palabras de activación (default: ["hey kalmiya", "kalmiya"])
            sensitivity: Sensibilidad de detección (0.0 a 1.0)
        """
        if wake_words is None:
            wake_words = ["hey kalmiya", "kalmiya", "oye kalmiya"]
        
        self.wake_words = [w.lower() for w in wake_words]
        self.sensitivity = sensitivity
        self.is_listening = False
        self.detection_count = 0
        self.false_positives = 0
        
        # Callbacks
        self.on_wake_word_detected: Optional[Callable] = None
        self.on_listening_start: Optional[Callable] = None
        self.on_listening_stop: Optional[Callable] = None
        
        # Stats
        self.stats_path = Path(__file__).parent.parent / "data" / "wake_word_stats.json"
        self.stats_path.parent.mkdir(parents=True, exist_ok=True)
        self.load_stats()
        
        # Recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300  # Ajustar según ambiente
        self.recognizer.dynamic_energy_threshold = True
        
        print(f"🎤 Wake Word Detector inicializado")
        print(f"🔊 Palabras de activación: {', '.join(self.wake_words)}")
    
    def start(self):
        """Inicia la escucha continua de wake word"""
        if self.is_listening:
            print("⚠️  Ya está escuchando")
            return False
        
        self.is_listening = True
        
        # Iniciar en thread separado
        threading.Thread(target=self._listen_loop, daemon=True).start()
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          🎤 WAKE WORD DETECTOR ACTIVADO                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🔊 Escuchando por: {words}
💡 Di una de las palabras de activación para despertar a KALMIYA

⚙️  Configuración:
   • Sensibilidad: {sens}
   • Detecciones totales: {count}
   
🔇 Presiona Ctrl+C para detener
        """.format(
            words=', '.join(self.wake_words),
            sens=self.sensitivity,
            count=self.detection_count
        ))
        
        if self.on_listening_start:
            self.on_listening_start()
        
        return True
    
    def stop(self):
        """Detiene la escucha de wake word"""
        if not self.is_listening:
            print("⚠️  No está escuchando")
            return False
        
        self.is_listening = False
        self.save_stats()
        
        print("🔇 Wake Word Detector detenido")
        
        if self.on_listening_stop:
            self.on_listening_stop()
        
        return True
    
    def _listen_loop(self):
        """Loop principal de escucha"""
        with sr.Microphone() as source:
            print("🎙️  Ajustando micrófono al ruido ambiente...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("✅ Micrófono listo")
            
            while self.is_listening:
                try:
                    # Escuchar audio
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    # Reconocer con Sphinx (offline)
                    try:
                        text = self.recognizer.recognize_sphinx(audio).lower()
                        
                        # Verificar si contiene wake word
                        if self._contains_wake_word(text):
                            self._on_wake_word_detected(text)
                    
                    except sr.UnknownValueError:
                        # No se entendió el audio
                        pass
                    except sr.RequestError as e:
                        print(f"⚠️  Error Sphinx: {e}")
                
                except sr.WaitTimeoutError:
                    # Timeout normal, continuar escuchando
                    pass
                except Exception as e:
                    print(f"⚠️  Error en loop: {e}")
                    time.sleep(0.5)
    
    def _contains_wake_word(self, text: str) -> bool:
        """
        Verifica si el texto contiene una wake word
        
        Args:
            text: Texto reconocido
            
        Returns:
            True si contiene wake word
        """
        text = text.lower().strip()
        
        for wake_word in self.wake_words:
            # Coincidencia exacta o contenida
            if wake_word in text or text in wake_word:
                # Verificar que no sea falso positivo obvio
                if len(text) < 3:  # Muy corto
                    return False
                return True
        
        return False
    
    def _on_wake_word_detected(self, text: str):
        """
        Callback interno cuando se detecta wake word
        
        Args:
            text: Texto que activó el wake word
        """
        self.detection_count += 1
        timestamp = datetime.now().isoformat()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║             🎯 WAKE WORD DETECTADO!                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🔊 Escuchado: "{text}"
⏰ Hora: {datetime.now().strftime('%H:%M:%S')}
📊 Detección #{self.detection_count}

🎤 Esperando tu comando...
        """)
        
        # Guardar en stats
        self.save_stats()
        
        # Llamar callback del usuario
        if self.on_wake_word_detected:
            self.on_wake_word_detected(text)
    
    def set_callback(self, callback: Callable):
        """
        Establece callback para cuando se detecte wake word
        
        Args:
            callback: Función a llamar (recibe texto como argumento)
        """
        self.on_wake_word_detected = callback
        print(f"✅ Callback configurado")
    
    def get_stats(self) -> dict:
        """Obtiene estadísticas de detección"""
        return {
            'total_detections': self.detection_count,
            'false_positives': self.false_positives,
            'wake_words': self.wake_words,
            'is_listening': self.is_listening,
            'sensitivity': self.sensitivity
        }
    
    def load_stats(self):
        """Carga estadísticas guardadas"""
        if self.stats_path.exists():
            try:
                with open(self.stats_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.detection_count = data.get('total_detections', 0)
                    self.false_positives = data.get('false_positives', 0)
            except:
                pass
    
    def save_stats(self):
        """Guarda estadísticas"""
        try:
            with open(self.stats_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'total_detections': self.detection_count,
                    'false_positives': self.false_positives,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error guardando stats: {e}")
    
    def report_false_positive(self):
        """Reporta un falso positivo (para mejorar precisión)"""
        self.false_positives += 1
        self.save_stats()
        print(f"📊 Falso positivo reportado (Total: {self.false_positives})")


# Función de utilidad para uso rápido

def start_wake_word_detector(callback: Callable = None) -> WakeWordDetector:
    """
    Inicia detector de wake word con configuración simple
    
    Args:
        callback: Función a llamar cuando se detecte wake word
        
    Returns:
        Instancia del detector
    """
    detector = WakeWordDetector()
    
    if callback:
        detector.set_callback(callback)
    
    detector.start()
    
    return detector


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         KALMIYA WAKE WORD DETECTOR v3.6 - DEMO              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Callback de ejemplo
    def on_wake_word(text):
        print(f"\n🎯 ¡Callback activado! Texto: '{text}'")
        print("💬 Aquí procesarías el comando del usuario\n")
    
    # Iniciar detector
    detector = WakeWordDetector(wake_words=["hey kalmiya", "kalmiya"])
    detector.set_callback(on_wake_word)
    detector.start()
    
    try:
        # Mantener vivo
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo...")
        detector.stop()
        
        # Mostrar stats
        stats = detector.get_stats()
        print(f"\n📊 Estadísticas finales:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
