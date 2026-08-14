# SKILL: Audio (Voice I/O)

[[INDEX|← Índice]] | [[06_docs/JARVIS_OS/SKILLS_CATALOG|📘 Catálogo de Skills]] | [[06_docs/JARVIS_OS/README|🌟 JARVIS OS]]

Habla, escucha, responde. Todo en tu máquina.

## Descripción
El skill **Audio** es tu interfaz de voz. Captura lo que dices (STT local), lo procesa (Claude) y responde en voz alta (TTS local). Completamente privado, cero latencia de API.

## Qué Hace
- 🎤 STT local (Speech-to-Text) privado
- 🔄 Procesamiento en tiempo real
- 🎙️ TTS local (Text-to-Speech) natural
- 🔊 Control de volumen y velocidad
- 🎯 Wake word detection ("JARVIS", "Oye JARVIS")

## Parámetros de Activación
```
"JARVIS" → Escucha
Presiona micrófono → Comienza a grabar
"Oye JARVIS, ¿qué hora es?" → Pregunta directa
```

## Flujo de Trabajo
1. **Captura** → Micrófono → STT local
2. **Transcribe** → Audio → Texto
3. **Procesa** → Claude interpreta comando
4. **Ejecuta** → Acción + generación de respuesta
5. **Sintetiza** → Claude response → TTS local
6. **Reproduce** → Altavoz → Voz natural

## Entrada
- Micrófono del sistema
- Formato: WAV, 16kHz, mono
- Wake words: "JARVIS", "Oye JARVIS", "Hey"

## Salida
```
[Usuario] "¿Cuál es mi agenda de hoy?"
[JARVIS] ✓ Escuchado (0.8s)
[JARVIS] "Basado en tu calendario, tienes 3 eventos confirmados...
         Primero, reunión con producto a las 9..."
[Audio] Reproducción en altavoz, voz natural (TTS)
```

## Configuración de Privacidad
✅ STT Local: Whisper (OpenAI, ejecuta localmente)  
✅ TTS Local: Pyttsx3 (sin API)  
✅ Sin conexión: Funciona desconectado  
✅ Sin histórico: No guarda grabaciones  

## Archivos Relacionados
- `01_systems/KALMIYA_System/kalmiya_audio.py` — Captura de audio
- `01_systems/KALMIYA_System/voz.py` — Síntesis de voz
- `01_systems/KALMIYA_System/config/audio_config.json` — Configuración

## Notas
- STT requiere CPU (no GPU necesario, laptop es suficiente)
- Tiempo de respuesta: ~1.2-2s (end-to-end)
- Volumen: Adaptativo al ambiente
- Idioma: Español (ES) configurable

## Mejora Futura
- [ ] Detección de emociones en voz
- [ ] Síntesis con entonación variable
- [ ] Acceso a micrófono remoto (Telegram)
- [ ] Traducción en tiempo real

---
**Creado:** 2026-08-12  
**Estado:** Parcialmente Implementado ⚠️  
**TODO**: Verificar STT/TTS son 100% locales
