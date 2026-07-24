import speech_recognition as sr
from random import choice
from datetime import datetime
from voz import speak
from utils import opening_text


def take_user_input():
    """Toma las entradas del usuario, las reconoce utilizando el módulo de reconocimiento de voz y lo transforma a texto"""

    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print('Escuchando....')
            r.pause_threshold = 1
            r.dynamic_energy_threshold = False
            r.energy_threshold = 4000
            audio = r.listen(source, timeout=10, phrase_time_limit=10)

        print('Reconociendo...')
        query = r.recognize_google(audio, language='es-es')
        
        if 'salir' in query.lower() or 'alto' in query.lower():
            hour = datetime.now().hour
            if hour >= 21 or hour < 6:
                speak("Buenas noches, cuídese")
            else:
                speak('¡Tenga un buen día!')
            exit()
        else:
            speak(choice(opening_text))
            
    except sr.UnknownValueError:
        speak('Disculpe, no he podido entender. ¿Podría decirlo de nuevo?')
        query = 'None'
    except sr.RequestError as e:
        speak(f'Error de conexión: {e}')
        query = 'None'
    except Exception as e:
        speak(f'Error inesperado: {str(e)}')
        query = 'None'
    return query