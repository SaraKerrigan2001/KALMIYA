import asyncio
import threading
import os
import sys
from decouple import config

# Importar telegram v20+
try:
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, ContextTypes
except ImportError:
    pass

# Importar cerebro para responder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from brain import ask_kalmiya
except ImportError:
    def ask_kalmiya(msg): return "No pude acceder a mi cerebro principal."

def _clean_val(val: str) -> str:
    val = (val or "").strip()
    if val.startswith("TU_") and val.endswith("_AQUI"):
        return ""
    if val == "TU_API_KEY_AQUI":
        return ""
    return val

TOKEN = _clean_val(config('TELEGRAM_BOT_TOKEN', default=''))
USER_ID = _clean_val(config('TELEGRAM_USER_ID', default=''))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Procesa el mensaje entrante y responde usando el cerebro de KALMIYA."""
    # Verificar seguridad (Solo responde a la dueña)
    sender_id = str(update.message.from_user.id)
    if USER_ID and sender_id != USER_ID:
        print(f"[TELEGRAM] Acceso denegado al usuario ID: {sender_id}")
        return

    user_text = update.message.text
    print(f"[TELEGRAM] Recibido: {user_text}")

    # Enviar al cerebro (es sincronico, en un sistema ideal esto deberia correr en executor, 
    # pero para simplicidad aqui lo llamamos directo).
    try:
        respuesta = ask_kalmiya(f"[Telegram]: {user_text}")
    except Exception as e:
        respuesta = f"Hubo un error al procesar tu mensaje: {e}"

    print(f"[TELEGRAM] Respondiendo: {respuesta}")
    await update.message.reply_text(respuesta)

def _run_telegram_loop():
    """Ejecuta el loop de eventos asíncronos en el hilo."""
    try:
        asyncio.set_event_loop(asyncio.new_event_loop())
        
        application = Application.builder().token(TOKEN).build()
        
        # Manejar mensajes de texto
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("[TELEGRAM] Bot iniciado y escuchando mensajes...")
        # Bloquea este hilo
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        print(f"[TELEGRAM] Error fatal en el bot de Telegram: {e}")

def start_telegram_bot():
    """Inicia el bot de Telegram en un hilo de fondo (daemon)."""
    if not TOKEN:
        print("[TELEGRAM] No hay TELEGRAM_BOT_TOKEN configurado. Bot desactivado.")
        return False
        
    bot_thread = threading.Thread(target=_run_telegram_loop, daemon=True, name="TelegramBotThread")
    bot_thread.start()
    return True
