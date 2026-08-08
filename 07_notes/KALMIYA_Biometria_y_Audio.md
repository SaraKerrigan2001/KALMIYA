---
title: "KALMIYA_Biometria_y_Audio"
created: "2026-07-13 20:23"
tags:
  - kalmiya
  - biometria
  - audio
  - seguridad
  - nuevo
source: KALMIYA
---

# KALMIYA_Biometria_y_Audio

## 🔒 Sistema Biométrico — kalmiya_biometrics.py

**Implementado:** 2026-07-13

### 3 Métodos de verificación en cascada:

| Método | Tecnología | Estado |
|---|---|---|
| Reconocimiento facial | OpenCV + Haar Cascades | ✅ Activo |
| Verificación de voz | SpeechRecognition (Google) | ✅ Activo |
| PIN biométrico | SHA-256 hash | ✅ Activo |

### Niveles de acceso:

| Nivel | Usuario | Permisos |
|---|---|---|
| **5** | Sara Kerrigan (Creadora) | Acceso total al sistema |
| **2** | Compañeros ADSO 201 | Uso del PC — algoritmos sellados |
| **0** | Desconocido | Bloqueo inmediato + alerta |

### Flujo de verificación:
1. Abre cámara → detecta rostro con OpenCV
2. Si hay rostro → confirma por voz o PIN
3. Si no hay cámara → intenta verificación de voz directa
4. Si voz falla → solicita PIN biométrico
5. Si todo falla (3 intentos) → bloquea PC y alerta a Sara

### Usuarios registrados:
- 👑 **Sara Kerrigan** — PIN: sara2001 — Frases: "kalmiya soy sara"
- 👤 **Estiven Rúa** — PIN: estiven — Nivel 2
- 👤 **Mateo Ospina** — PIN: mateo — Nivel 2

### Comandos de voz:
- *"kalmiya, verifica mi identidad"* → verificación completa
- *"kalmiya, quién tiene acceso"* → muestra sesión activa

### Acceso desde menú:
`BIO1` Verificación completa | `BIO2` Solo cara | `BIO3` Solo voz  
`BIO4` Solo PIN | `BIO5` Estado | `BIO6` Listar usuarios | `BIO7` Cerrar sesión

### Autenticación de inicio automático
- KALMIYA inicia con verificación biométrica antes de cargar el menú principal.
- Si falla la autenticación, el lanzador se detiene por seguridad.
- Desactiva temporalmente esta comprobación con `KALMIYA_REQUIRE_BIOMETRIC=false`.

---

## 🔊 Sistema de Audio — kalmiya_audio.py

### 6 Perfiles predefinidos:

| Perfil | Volumen | Micro | EQ |
|---|---|---|---|
| normal | 70% | 80% | Plano |
| noche | 30% | 60% | -3 graves, -2 agudos |
| musica | 75% | 50% | +5 graves, +2 agudos |
| estudio | 40% | 85% | -2 graves, +2 medios |
| juegos | 80% | 70% | +3 graves, +3 agudos |
| llamada | 65% | 90% | -4 graves, +4 medios |

### Ecualizador:
- 3 bandas: **Graves / Medios / Agudos** (-10 a +10 dB)
- Los valores se traducen a pitch y rate del motor Edge TTS

### Perfil automático por hora:
- 22:00–06:00 → **noche**
- 08:00–14:00 → **estudio**
- Resto → **normal**

### Comandos de voz:
- *"sube el volumen"* / *"baja el volumen"*
- *"silencia el audio"* / *"activa el audio"*
- *"perfil de audio noche"* / *"perfil música"* / etc.

### Acceso desde menú:
`AUD1` Estado | `AUD2-3` Vol +/- | `AUD4` Mute  
`AUD5-9` Perfiles | `AUD10` EQ manual | `AUD11` Dispositivos

---

## 🔗 Integración

| Archivo | Cambio |
|---|---|
| `kalmiya_launcher.py` | Paso 2.7: `_start_audio_system()` al arrancar |
| `kalmiya_core.py` | Comandos de voz bio y audio en `process_command()` |
| `main.py` | Handlers `_handle_bio()` y `_handle_aud()` + menú |

[[KALMIYA_DASHBOARD|📊 Dashboard]] | [[MODULOS_IMPLEMENTADOS|📦 Módulos]] | [[INDEX|📋 Índice]] | [[KALMIYA_FUNCIONES|⚙️ Funciones]]

