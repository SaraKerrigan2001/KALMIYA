# remote_bridge.py
# Modulo de conexion remota para KALMIYA AI
# Permite que los telefonos se conecten a KALMIYA desde cualquier lugar sin WiFi local

import os
import sys
import threading
import subprocess
import time
import re
import json
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO, format='[KALMIYA Remote] %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from brain import ask_kalmiya
except ImportError:
    logger.warning("No se pudo importar brain.py - usando funcion de respaldo")
    def ask_kalmiya(text: str) -> str:
        return f"KALMIYA recibio: {text}"

try:
    from voz import speak
except ImportError:
    logger.warning("No se pudo importar voz.py - usando funcion de respaldo")
    def speak(text: str):
        print(f"[VOZ] {text}")

try:
    from database import log_command, update_memory, get_memory
except ImportError:
    logger.warning("No se pudo importar database.py - usando funciones de respaldo")
    def log_command(cmd: str, resp: str = ""):
        print(f"[DB] Comando: {cmd} | Respuesta: {resp}")
    def update_memory(key: str, value):
        pass
    def get_memory(key: str):
        return None

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False
    logger.warning("qrcode no disponible - no se generaran codigos QR")

try:
    from pyngrok import ngrok as pyngrok_ngrok
    NGROK_AVAILABLE = True
except ImportError:
    NGROK_AVAILABLE = False
    logger.warning("pyngrok no disponible")

try:
    from telegram import Update
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    logger.warning("python-telegram-bot no disponible")

# Estado global de conexiones
_connection_state = {
    "cloudflare": {"active": False, "url": None, "process": None, "qr_path": None},
    "ngrok":      {"active": False, "url": None, "tunnel": None},
    "telegram":   {"active": False, "bot_thread": None, "token": None, "chats": []},
}

_CLOUDFLARED_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cloudflared.exe")
_LOCAL_PORT = 8765
_QR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kalmiya_remote_qr.png")


# ================================================================
# METODO 1 - CLOUDFLARE TUNNEL
# ================================================================

def start_cloudflare_tunnel() -> str:
    """
    Inicia un tunel Cloudflare usando cloudflared.exe.
    Devuelve la URL publica HTTPS generada.
    """
    global _connection_state

    # Asegurar que el servidor local de phone_bridge esté corriendo en el puerto 8765
    import socket
    port_in_use = False
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            port_in_use = (s.connect_ex(('127.0.0.1', _LOCAL_PORT)) == 0)
    except Exception:
        pass

    if not port_in_use:
        logger.info(f"El puerto {_LOCAL_PORT} no está activo. Iniciando phone_bridge...")
        try:
            from phone_bridge import start_bridge
            start_bridge(show_qr=False)
            time.sleep(1) # Esperar a que Flask inicialice
        except Exception as e:
            logger.error(f"No se pudo iniciar el phone_bridge: {e}")

    if not os.path.exists(_CLOUDFLARED_PATH):
        logger.error(f"cloudflared.exe no encontrado en: {_CLOUDFLARED_PATH}")
        speak("No encontre el archivo cloudflared. Intenta con ngrok.")
        return ""

    if _connection_state["cloudflare"]["active"]:
        logger.info("El tunel Cloudflare ya esta activo.")
        return _connection_state["cloudflare"]["url"] or ""

    print("\nIniciando tunel Cloudflare...")
    print(f"   Ejecutable: {_CLOUDFLARED_PATH}")
    print(f"   Puerto local: {_LOCAL_PORT}")

    try:
        process = subprocess.Popen(
            [_CLOUDFLARED_PATH, "tunnel", "--url", f"http://localhost:{_LOCAL_PORT}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        public_url = ""
        url_pattern = re.compile(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com")
        timeout = 30
        start = time.time()

        print("   Esperando URL publica", end="", flush=True)
        for line in process.stdout:
            print(".", end="", flush=True)
            match = url_pattern.search(line)
            if match:
                public_url = match.group(0)
                break
            if time.time() - start > timeout:
                break

        print()

        if not public_url:
            logger.error("No se pudo obtener la URL de Cloudflare en el tiempo esperado.")
            process.terminate()
            speak("No pude obtener la URL de Cloudflare. Intenta con ngrok.")
            return ""

        _connection_state["cloudflare"]["active"] = True
        _connection_state["cloudflare"]["url"] = public_url
        _connection_state["cloudflare"]["process"] = process

        qr_path = _generate_qr(public_url, _QR_PATH)
        _connection_state["cloudflare"]["qr_path"] = qr_path

        update_memory("cloudflare_url", public_url)
        log_command("start_cloudflare_tunnel", public_url)

        print(f"\nTunel Cloudflare activo:")
        print(f"   URL publica: {public_url}")
        if qr_path:
            print(f"   Codigo QR guardado en: {qr_path}")
        print("\nInstrucciones:")
        print("   1. Escanea el codigo QR con tu telefono")
        print("   2. O abre esta URL en cualquier navegador:")
        print(f"      {public_url}")
        print("   3. No necesitas WiFi - funciona con datos moviles\n")

        speak("Tunel Cloudflare activo. Puedes conectarte desde cualquier lugar.")
        return public_url

    except FileNotFoundError:
        logger.error("cloudflared.exe no se pudo ejecutar.")
        speak("No pude ejecutar cloudflared. Verifica que el archivo existe.")
        return ""
    except Exception as e:
        logger.error(f"Error iniciando tunel Cloudflare: {e}")
        speak("Hubo un error al iniciar el tunel Cloudflare.")
        return ""


def _generate_qr(url: str, path: str) -> str:
    """Genera un codigo QR para la URL dada y lo guarda en path."""
    if not QRCODE_AVAILABLE:
        logger.warning("qrcode no instalado - no se genero el QR.")
        return ""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(path)
        logger.info(f"QR guardado en: {path}")
        return path
    except Exception as e:
        logger.error(f"Error generando QR: {e}")
        return ""


# ================================================================
# METODO 2 - NGROK TUNNEL
# ================================================================

def start_ngrok_tunnel(auth_token: str = "") -> str:
    """
    Inicia un tunel ngrok al puerto local de KALMIYA.
    auth_token: token de autenticacion de ngrok (opcional para uso basico).
    Devuelve la URL publica.
    """
    global _connection_state

    # Asegurar que el servidor local de phone_bridge esté corriendo en el puerto 8765
    import socket
    port_in_use = False
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            port_in_use = (s.connect_ex(('127.0.0.1', _LOCAL_PORT)) == 0)
    except Exception:
        pass

    if not port_in_use:
        logger.info(f"El puerto {_LOCAL_PORT} no está activo. Iniciando phone_bridge...")
        try:
            from phone_bridge import start_bridge
            start_bridge(show_qr=False)
            time.sleep(1) # Esperar a que Flask inicialice
        except Exception as e:
            logger.error(f"No se pudo iniciar el phone_bridge: {e}")

    if not NGROK_AVAILABLE:
        logger.error("pyngrok no esta instalado. Ejecuta: pip install pyngrok")
        speak("pyngrok no esta instalado. No puedo iniciar el tunel ngrok.")
        return ""

    if _connection_state["ngrok"]["active"]:
        logger.info("El tunel ngrok ya esta activo.")
        return _connection_state["ngrok"]["url"] or ""

    print("\nIniciando tunel ngrok...")

    try:
        if auth_token:
            pyngrok_ngrok.set_auth_token(auth_token)
            print("   Token de autenticacion configurado.")

        tunnel = pyngrok_ngrok.connect(_LOCAL_PORT, "http")
        public_url = tunnel.public_url

        if public_url.startswith("http://"):
            public_url = public_url.replace("http://", "https://", 1)

        _connection_state["ngrok"]["active"] = True
        _connection_state["ngrok"]["url"] = public_url
        _connection_state["ngrok"]["tunnel"] = tunnel

        update_memory("ngrok_url", public_url)
        log_command("start_ngrok_tunnel", public_url)

        ngrok_qr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kalmiya_ngrok_qr.png")
        qr_path = _generate_qr(public_url, ngrok_qr_path)

        print(f"\nTunel ngrok activo:")
        print(f"   URL publica: {public_url}")
        if qr_path:
            print(f"   Codigo QR guardado en: {qr_path}")
        print("\nInstrucciones:")
        print("   1. Escanea el codigo QR con tu telefono")
        print("   2. O abre esta URL en cualquier navegador:")
        print(f"      {public_url}")
        print("   3. Funciona con WiFi o datos moviles\n")

        speak("Tunel ngrok activo. Puedes conectarte desde cualquier lugar.")
        return public_url

    except Exception as e:
        logger.error(f"Error iniciando tunel ngrok: {e}")
        speak("Hubo un error al iniciar el tunel ngrok. Intenta con Cloudflare.")
        return ""


# ================================================================
# METODO 3 - TELEGRAM BOT
# ================================================================

_telegram_app = None


def start_telegram_bot(token: str) -> threading.Thread:
    """
    Inicia el bot de Telegram de KALMIYA en un hilo separado.
    Sara y la familia pueden enviar mensajes al bot para interactuar con KALMIYA.
    Devuelve el hilo donde corre el bot.
    """
    global _connection_state, _telegram_app

    if not TELEGRAM_AVAILABLE:
        logger.error("python-telegram-bot no esta instalado. Ejecuta: pip install python-telegram-bot")
        speak("La libreria de Telegram no esta instalada.")
        return threading.Thread()

    if _connection_state["telegram"]["active"]:
        logger.info("El bot de Telegram ya esta activo.")
        return _connection_state["telegram"]["bot_thread"]

    print("\nIniciando bot de Telegram de KALMIYA...")

    async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = str(update.effective_chat.id)
        nombre = update.effective_user.first_name or "Usuario"
        if chat_id not in _connection_state["telegram"]["chats"]:
            _connection_state["telegram"]["chats"].append(chat_id)
        await update.message.reply_text(
            f"Hola {nombre}, soy KALMIYA.\n"
            "Puedes hablarme directamente aqui.\n"
            "Escribe /ayuda para ver los comandos disponibles."
        )
        log_command("telegram_start", f"chat_id={chat_id}, nombre={nombre}")

    async def cmd_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Comandos disponibles:\n\n"
            "/start - Iniciar conversacion\n"
            "/ayuda - Ver esta ayuda\n"
            "/estado - Ver estado de KALMIYA\n"
            "/emergencia - Enviar alerta de emergencia\n\n"
            "Tambien puedes escribirme cualquier mensaje y te respondere."
        )

    async def cmd_estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
        estado = get_connection_status()
        texto = "Estado de KALMIYA:\n\n"
        for metodo, info in estado.items():
            activo = "Activo" if info.get("active") else "Inactivo"
            url = info.get("url", "-")
            texto += f"{metodo.capitalize()}: {activo}\n"
            if url and url != "-":
                texto += f"  URL: {url}\n"
        await update.message.reply_text(texto)

    async def cmd_emergencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = str(update.effective_chat.id)
        nombre = update.effective_user.first_name or "Usuario"
        alerta = f"EMERGENCIA desde Telegram - {nombre} (chat: {chat_id})"
        log_command("telegram_emergencia", alerta)
        speak(f"Alerta de emergencia recibida de {nombre} por Telegram.")
        await update.message.reply_text(
            "ALERTA DE EMERGENCIA ENVIADA\n\nSara ha sido notificada. Mantente tranquilo/a."
        )

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = str(update.effective_chat.id)
        nombre = update.effective_user.first_name or "Usuario"
        texto = update.message.text or ""

        if chat_id not in _connection_state["telegram"]["chats"]:
            _connection_state["telegram"]["chats"].append(chat_id)

        log_command(f"telegram_msg:{nombre}", texto)

        try:
            respuesta = ask_kalmiya(texto)
        except Exception as e:
            respuesta = f"Lo siento, tuve un problema al procesar tu mensaje: {e}"

        await update.message.reply_text(respuesta)

    def _run_bot():
        global _telegram_app
        try:
            app = ApplicationBuilder().token(token).build()
            app.add_handler(CommandHandler("start", cmd_start))
            app.add_handler(CommandHandler("ayuda", cmd_ayuda))
            app.add_handler(CommandHandler("estado", cmd_estado))
            app.add_handler(CommandHandler("emergencia", cmd_emergencia))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            _telegram_app = app
            print("Bot de Telegram activo. Esperando mensajes...")
            print("Instrucciones:")
            print("   1. Abre Telegram y busca tu bot")
            print("   2. Envia /start para comenzar")
            print("   3. Funciona sin WiFi - solo necesitas datos moviles\n")
            app.run_polling(drop_pending_updates=True)
        except Exception as e:
            logger.error(f"Error en el bot de Telegram: {e}")
            _connection_state["telegram"]["active"] = False

    bot_thread = threading.Thread(target=_run_bot, daemon=True, name="KalmiyaTelegramBot")
    bot_thread.start()

    _connection_state["telegram"]["active"] = True
    _connection_state["telegram"]["bot_thread"] = bot_thread
    _connection_state["telegram"]["token"] = token

    update_memory("telegram_active", True)
    log_command("start_telegram_bot", "iniciado")
    speak("Bot de Telegram de KALMIYA iniciado. Ya puedes recibir mensajes.")

    return bot_thread


def send_telegram_message(chat_id: str, message: str, token: str) -> bool:
    """
    Envia un mensaje a un chat de Telegram especifico.
    Util para notificaciones proactivas a Sara o la familia.
    """
    try:
        import requests as req
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        response = req.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            log_command("send_telegram_message", f"chat_id={chat_id}")
            return True
        else:
            logger.error(f"Error enviando mensaje Telegram: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Excepcion enviando mensaje Telegram: {e}")
        return False


def get_telegram_status() -> dict:
    """Devuelve el estado actual del bot de Telegram."""
    state = _connection_state["telegram"]
    return {
        "active": state["active"],
        "chats_conectados": len(state["chats"]),
        "chat_ids": state["chats"],
        "token_configurado": bool(state["token"]),
    }


# ================================================================
# ORQUESTADOR PRINCIPAL
# ================================================================

def start_remote_connection(method: str = "cloudflare") -> dict:
    """
    Inicia el metodo de conexion remota especificado.

    method: "cloudflare" | "ngrok" | "telegram" | "all"
    Devuelve un dict con {"method", "url", "qr_path", "status"}
    """
    method = method.lower().strip()
    result = {"method": method, "url": "", "qr_path": "", "status": "error"}

    print(f"\n{'='*50}")
    print(f"  KALMIYA - Conexion Remota [{method.upper()}]")
    print(f"{'='*50}\n")

    if method == "cloudflare":
        url = start_cloudflare_tunnel()
        result["url"] = url
        result["qr_path"] = _connection_state["cloudflare"].get("qr_path", "")
        result["status"] = "activo" if url else "error"

    elif method == "ngrok":
        url = start_ngrok_tunnel()
        result["url"] = url
        result["status"] = "activo" if url else "error"

    elif method == "telegram":
        token = get_memory("telegram_token") or ""
        if not token:
            print("No se encontro el token de Telegram en la memoria.")
            print("Usa: start_telegram_bot(token='TU_TOKEN_AQUI')")
            result["status"] = "sin_token"
        else:
            start_telegram_bot(token)
            result["status"] = "activo"

    elif method == "all":
        print("Iniciando todos los metodos de conexion...\n")
        results = {}

        cf_url = start_cloudflare_tunnel()
        results["cloudflare"] = {
            "url": cf_url,
            "qr_path": _connection_state["cloudflare"].get("qr_path", ""),
            "status": "activo" if cf_url else "error",
        }

        if not cf_url:
            print("Cloudflare fallo - intentando ngrok como respaldo...")
            ng_url = start_ngrok_tunnel()
            results["ngrok"] = {
                "url": ng_url,
                "status": "activo" if ng_url else "error",
            }
        else:
            results["ngrok"] = {"url": "", "status": "omitido (cloudflare activo)"}

        token = get_memory("telegram_token") or ""
        if token:
            start_telegram_bot(token)
            results["telegram"] = {"status": "activo"}
        else:
            results["telegram"] = {"status": "sin_token"}

        result["method"] = "all"
        result["url"] = cf_url or results.get("ngrok", {}).get("url", "")
        result["status"] = "activo"
        result["detalles"] = results

    else:
        logger.error(f"Metodo desconocido: '{method}'. Usa: cloudflare, ngrok, telegram, all")
        result["status"] = f"metodo_desconocido: {method}"

    return result


def get_connection_status() -> dict:
    """Devuelve el estado de todas las conexiones activas."""
    return {
        "cloudflare": {
            "active": _connection_state["cloudflare"]["active"],
            "url": _connection_state["cloudflare"]["url"],
            "qr_path": _connection_state["cloudflare"]["qr_path"],
        },
        "ngrok": {
            "active": _connection_state["ngrok"]["active"],
            "url": _connection_state["ngrok"]["url"],
        },
        "telegram": get_telegram_status(),
    }


def stop_all_tunnels():
    """Detiene todos los tuneles y conexiones activas."""
    global _connection_state, _telegram_app

    print("\nDeteniendo todas las conexiones remotas...")

    if _connection_state["cloudflare"]["active"]:
        proc = _connection_state["cloudflare"]["process"]
        if proc:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
        _connection_state["cloudflare"]["active"] = False
        _connection_state["cloudflare"]["url"] = None
        _connection_state["cloudflare"]["process"] = None
        print("   Tunel Cloudflare detenido.")

    if _connection_state["ngrok"]["active"] and NGROK_AVAILABLE:
        try:
            pyngrok_ngrok.kill()
        except Exception as e:
            logger.warning(f"Error deteniendo ngrok: {e}")
        _connection_state["ngrok"]["active"] = False
        _connection_state["ngrok"]["url"] = None
        _connection_state["ngrok"]["tunnel"] = None
        print("   Tunel ngrok detenido.")

    if _connection_state["telegram"]["active"] and _telegram_app:
        try:
            # python-telegram-bot v20+ ya tiene su propio event loop activo en el hilo del bot.
            # asyncio.run() lanzaría RuntimeError si se llama desde ese mismo hilo.
            # Usamos updater.stop() de forma segura a través del método shutdown del Application.
            import asyncio
            import threading as _threading

            def _stop_bot():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(_telegram_app.stop())
                    loop.run_until_complete(_telegram_app.shutdown())
                    loop.close()
                except Exception as inner_e:
                    logger.warning(f"Error en hilo de detención Telegram: {inner_e}")

            stop_thread = _threading.Thread(target=_stop_bot, daemon=True)
            stop_thread.start()
            stop_thread.join(timeout=5)
        except Exception as e:
            logger.warning(f"Error deteniendo bot Telegram: {e}")
        _connection_state["telegram"]["active"] = False
        print("   Bot de Telegram detenido.")

    log_command("stop_all_tunnels", "todas las conexiones detenidas")
    speak("Todas las conexiones remotas han sido detenidas.")
    print("\nTodas las conexiones remotas detenidas.\n")


# ================================================================
# PUNTO DE ENTRADA PARA PRUEBAS
# ================================================================

if __name__ == "__main__":
    print("KALMIYA Remote Bridge - Prueba de conexion")
    print("Metodos disponibles: cloudflare, ngrok, telegram, all\n")

    metodo = input("Que metodo deseas probar? [cloudflare]: ").strip() or "cloudflare"
    resultado = start_remote_connection(metodo)

    print(f"\nResultado:")
    print(json.dumps({k: v for k, v in resultado.items() if k != "detalles"}, indent=2, ensure_ascii=False))

    if metodo in ("telegram", "all"):
        print("\nBot de Telegram corriendo. Presiona Ctrl+C para detener.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_all_tunnels()
