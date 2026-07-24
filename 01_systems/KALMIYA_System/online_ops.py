import requests
import socket
import wikipedia
try:
    import pywhatkit as kit
except Exception as e:
    kit = None
import xml.etree.ElementTree as ET
from voz import speak

# Fallback IP en caso de error
FALLBACK_IP = "No disponible"

NEWS_FEEDS = {
    'nacional': 'https://elpais.com/rss/elpais/portada.xml',
    'mundo': 'https://elpais.com/rss/internacional.xml'
}


def get_news_headlines(source='mundo', max_items=5):
    """Devuelve titulares de noticias recientes en español."""
    source = source.lower()
    feed_url = NEWS_FEEDS.get(source, NEWS_FEEDS['mundo'])
    try:
        response = requests.get(feed_url, timeout=8)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        items = []
        for item in root.findall('.//item')[:max_items]:
            title = item.find('title').text or ''
            link = item.find('link').text or ''
            description = item.find('description').text or ''
            items.append({
                'title': title.strip(),
                'link': link.strip(),
                'description': description.strip()
            })
        return items
    except Exception as e:
        speak(f"Error al obtener noticias {source}: {e}")
        return []


def speak_news_headlines(source='mundo', max_items=3):
    """Lee los titulares de noticias en voz alta."""
    source_name = 'mundiales' if source.lower() == 'mundo' else 'nacionales'
    headlines = get_news_headlines(source, max_items=max_items)
    if not headlines:
        speak(f"No pude obtener las noticias {source_name} en este momento.")
        return

    speak(f"Aquí están las últimas noticias {source_name}.")
    for idx, item in enumerate(headlines, start=1):
        speak(f"{idx}. {item['title']}")


def get_local_ip():
    """Devuelve la IP local del equipo en la red."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def get_ip_info():
    """Devuelve un diccionario con la IP pública y la IP local."""
    return {
        'public_ip': find_my_ip(),
        'local_ip': get_local_ip()
    }


def speak_ip_info():
    """Dice en voz alta la IP pública y la IP local."""
    try:
        ip_data = get_ip_info()
        speak(f"Tu IP pública es {ip_data['public_ip']} y tu IP local es {ip_data['local_ip']}")
    except Exception as e:
        speak(f"Error al obtener información de IP: {e}")


def find_my_ip():
    """Devuelve la IP pública actual usando api64.ipify.org con reintentos."""
    urls = [
        'https://api64.ipify.org?format=json',
        'https://ipapi.co/json/'
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            if 'api64.ipify' in url:
                return response.json().get('ip', FALLBACK_IP)
            else:
                return response.json().get('ip', FALLBACK_IP)
        except requests.RequestException:
            continue
    
    return FALLBACK_IP


def search_on_wikipedia(query):
    """Busca en Wikipedia y devuelve un resumen breve."""
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.PageError:
        return f"No se encontró información sobre '{query}' en Wikipedia"
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Varios resultados para '{query}'. Intenta ser más específico"
    except Exception as e:
        return f"Error en búsqueda de Wikipedia: {str(e)}"


def play_on_youtube(video):
    """Reproduce en YouTube usando pywhatkit."""
    if kit is None:
        speak("No se pudo iniciar pywhatkit. Verifica tu conexión a Internet.")
        return
    try:
        kit.playonyt(video)
        speak(f"Reproduciendo {video} en YouTube")
    except Exception as e:
        speak(f"Error al reproducir en YouTube: {str(e)}")


def search_on_google(query):
    """Busca en Google usando pywhatkit."""
    if kit is None:
        speak("No se pudo iniciar pywhatkit. Verifica tu conexión a Internet.")
        return
    try:
        kit.search(query)
        speak(f"Buscando {query} en Google")
    except Exception as e:
        speak(f"Error al buscar en Google: {str(e)}")


def get_location_info():
    """Obtiene información detallada de ubicación basada en IP."""
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'city': data.get('city', 'Desconocida'),
                'region': data.get('region', 'Desconocida'),
                'country': data.get('country_name', 'Desconocido'),
                'ip': data.get('ip', 'Desconocida')
            }
    except:
        pass
    return None


def send_whatsapp_message(number, message, country_code='+91'):
    """Envía un mensaje instantáneo de WhatsApp a un número con prefijo."""
    if kit is None:
        speak("No se pudo iniciar pywhatkit. Verifica tu conexión a Internet.")
        return
    try:
        kit.sendwhatmsg_instantly(f"{country_code}{number}", message)
        speak(f"Mensaje enviado a {number}")
    except Exception as e:
        speak(f"Error al enviar WhatsApp: {str(e)}")


def open_email_client(service="gmail"):
    """Abre el cliente de correo en el navegador predeterminado."""
    import webbrowser
    urls = {
        'gmail': "https://mail.google.com",
        'outlook': "https://outlook.live.com",
        'hotmail': "https://outlook.live.com",
        'yahoo': "https://mail.yahoo.com"
    }
    url = urls.get(service.lower(), "https://mail.google.com")
    try:
        webbrowser.open(url)
        speak(f"Entendido. Abriendo tu bandeja de entrada de {service} en el navegador.")
        return True
    except Exception as e:
        speak(f"Error al abrir el navegador: {str(e)}")
        return False


def open_claude_web():
    """Abre la interfaz web de Claude en el navegador predeterminado."""
    import webbrowser
    url = "https://claude.ai"
    try:
        webbrowser.open(url)
        speak("Abriendo Claude en el navegador.")
        return True
    except Exception as e:
        speak(f"Error al abrir Claude: {str(e)}")
        return False


def check_email_imap(email_user, email_pass, imap_server="imap.gmail.com", port=993):
    """
    Se conecta vía IMAP SSL, obtiene los últimos 5 correos recibidos 
    y los devuelve listos para mostrar o leer.
    """
    import imaplib
    import email
    from email.header import decode_header
    
    try:
        def clean_header(header_val):
            if not header_val:
                return ""
            decoded_seq = decode_header(header_val)
            header_parts = []
            for bytes_or_str, encoding in decoded_seq:
                if isinstance(bytes_or_str, bytes):
                    try:
                        header_parts.append(bytes_or_str.decode(encoding or 'utf-8', errors='ignore'))
                    except Exception:
                        header_parts.append(bytes_or_str.decode('latin1', errors='ignore'))
                else:
                    header_parts.append(str(bytes_or_str))
            return "".join(header_parts)

        mail = imaplib.IMAP4_SSL(imap_server, port)
        mail.login(email_user, email_pass)
        mail.select("inbox")
        
        status, data = mail.search(None, "ALL")
        mail_ids = data[0].split()
        
        if not mail_ids:
            mail.logout()
            return []
            
        recent_ids = mail_ids[-5:]
        recent_ids.reverse()
        
        emails_list = []
        for m_id in recent_ids:
            status, msg_data = mail.fetch(m_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = clean_header(msg["Subject"])
                    from_sender = clean_header(msg["From"])
                    date_sent = msg["Date"]
                    
                    emails_list.append({
                        'subject': subject,
                        'from': from_sender,
                        'date': date_sent
                    })
        mail.logout()
        return emails_list
    except Exception as e:
        raise e

    