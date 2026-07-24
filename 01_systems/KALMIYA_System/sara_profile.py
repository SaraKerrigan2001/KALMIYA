"""
sara_profile.py - Perfil completo de Sara Kerrigan
====================================================
KALMIYA guarda y accede a toda la informacion personal de Sara:
redes sociales, telefonos, cuentas, familia, preferencias.
Sara puede actualizar su perfil en cualquier momento.
KALMIYA usa esta informacion para personalizar cada interaccion.
"""

import json
import os
from datetime import datetime
from database import update_memory, get_memory, log_command
from voz import speak

PROFILE_FILE = os.path.join(os.path.dirname(__file__), "sara_profile.json")

# ── Estructura base del perfil ─────────────────────────────────────────────────
DEFAULT_PROFILE = {
    "identidad": {
        "nombre_completo": "Sara Kerrigan",
        "nombre_real": "",
        "apodo": "Sara",
        "alias_cultural": "Sara Kerrigan (referencia a StarCraft — personaje ficticio)",
        "fecha_nacimiento": "",
        "ciudad": "",
        "pais": "",
        "ocupacion": "",
        "idiomas": ["Español"]
    },
    "contacto": {
        "telefonos": [],
        "emails": [],
        "direccion": ""
    },
    "redes_sociales": {
        "instagram": "",
        "facebook": "",
        "twitter": "",
        "tiktok": "",
        "youtube": "",
        "linkedin": "",
        "whatsapp": "",
        "telegram": "",
        "otros": {}
    },
    "cuentas_digitales": {
        "google": [],
        "microsoft": [],
        "apple": [],
        "gaming": [],
        "streaming": [],
        "otros": []
    },
    "familia": {},
    "dispositivos": {
        "pc": {
            "nombre": "PC de Sara",
            "os": "Windows",
            "ip_local": ""
        },
        "celulares": []
    },
    "preferencias": {
        "color_favorito": "",
        "musica": "",
        "peliculas": "",
        "comida": "",
        "hobbies": [],
        "app_favorita": ""
    },
    "seguridad": {
        "palabras_clave_emergencia": ["ayuda", "peligro", "socorro"],
        "contactos_emergencia": [],
        "modo_proteccion": "activo"
    },
    "notas_kalmiya": [],
    "ultima_actualizacion": ""
}


# ── Carga y guardado ───────────────────────────────────────────────────────────

def load_profile() -> dict:
    """Carga el perfil de Sara desde el archivo JSON."""
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Fusionar con el perfil por defecto para agregar campos nuevos
            return _deep_merge(DEFAULT_PROFILE.copy(), data)
        except Exception as e:
            print(f"[PERFIL] Error cargando perfil: {e}")
    return DEFAULT_PROFILE.copy()


def save_profile(profile: dict) -> bool:
    """Guarda el perfil de Sara en el archivo JSON."""
    try:
        profile["ultima_actualizacion"] = datetime.now().isoformat()
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[PERFIL] Error guardando perfil: {e}")
        return False


def _deep_merge(base: dict, override: dict) -> dict:
    """Fusiona dos diccionarios de forma recursiva."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


# ── Actualización de campos ────────────────────────────────────────────────────

def update_profile_field(section: str, field: str, value) -> bool:
    """
    Actualiza un campo específico del perfil.
    
    Args:
        section: Sección del perfil (ej: 'contacto', 'redes_sociales')
        field:   Campo dentro de la sección (ej: 'telefonos', 'instagram')
        value:   Nuevo valor
    """
    profile = load_profile()
    try:
        if section in profile:
            if isinstance(profile[section], dict):
                if field in profile[section]:
                    if isinstance(profile[section][field], list) and not isinstance(value, list):
                        # Agregar a lista si no está ya
                        if value not in profile[section][field]:
                            profile[section][field].append(value)
                    else:
                        profile[section][field] = value
                else:
                    profile[section][field] = value
            save_profile(profile)
            # Sincronizar con la base de datos de memoria
            update_memory(f"perfil_{section}_{field}", str(value))
            log_command(f"[PERFIL] Actualizado {section}.{field}", str(value), source='profile')
            return True
    except Exception as e:
        print(f"[PERFIL] Error actualizando {section}.{field}: {e}")
    return False


def add_family_member(nombre: str, relacion: str, telefono: str = "",
                      email: str = "", notas: str = "") -> bool:
    """Agrega un miembro de la familia al perfil."""
    profile = load_profile()
    profile["familia"][nombre] = {
        "relacion": relacion,
        "telefono": telefono,
        "email": email,
        "notas": notas,
        "agregado": datetime.now().isoformat()
    }
    speak(f"He registrado a {nombre} como tu {relacion}, Sara.")
    log_command(f"[FAMILIA] Agregado: {nombre}", relacion, source='profile')
    return save_profile(profile)


def add_device(nombre: str, tipo: str, ip: str = "", notas: str = "") -> bool:
    """Registra un dispositivo (celular, tablet, etc.)."""
    profile = load_profile()
    device = {
        "nombre": nombre,
        "tipo": tipo,
        "ip": ip,
        "notas": notas,
        "registrado": datetime.now().isoformat(),
        "conectado": False
    }
    if tipo.lower() in ("celular", "movil", "telefono", "smartphone"):
        profile["dispositivos"]["celulares"].append(device)
    save_profile(profile)
    speak(f"Dispositivo {nombre} registrado en mi sistema.")
    return True


def add_social_network(red: str, usuario: str) -> bool:
    """Registra una red social."""
    profile = load_profile()
    red_lower = red.lower()
    redes = profile["redes_sociales"]
    if red_lower in redes:
        redes[red_lower] = usuario
    else:
        redes["otros"][red] = usuario
    save_profile(profile)
    speak(f"He registrado tu cuenta de {red}: {usuario}")
    return True


def add_account(tipo: str, cuenta: str) -> bool:
    """Registra una cuenta digital."""
    profile = load_profile()
    tipo_lower = tipo.lower()
    cuentas = profile["cuentas_digitales"]
    if tipo_lower in cuentas:
        if cuenta not in cuentas[tipo_lower]:
            cuentas[tipo_lower].append(cuenta)
    else:
        if cuenta not in cuentas["otros"]:
            cuentas["otros"].append(f"{tipo}: {cuenta}")
    save_profile(profile)
    speak(f"Cuenta de {tipo} registrada en mi memoria.")
    return True


def add_kalmiya_note(nota: str) -> bool:
    """KALMIYA agrega una nota propia sobre Sara."""
    profile = load_profile()
    entry = {
        "nota": nota,
        "fecha": datetime.now().isoformat(),
        "fuente": "KALMIYA_autonoma"
    }
    profile["notas_kalmiya"].append(entry)
    return save_profile(profile)


# ── Consultas ──────────────────────────────────────────────────────────────────

def get_profile_summary() -> str:
    """Genera un resumen del perfil para el prompt de IA."""
    p = load_profile()
    lines = []

    ident = p.get("identidad", {})
    if ident.get("nombre_real"):
        lines.append(f"Nombre real: {ident['nombre_real']}")
    if ident.get("nombre_completo"):
        lines.append(f"Nombre de usuario / alias: {ident['nombre_completo']} (alias cultural inspirado en StarCraft)")
    if ident.get("alias_cultural"):
        lines.append(f"Nota: '{ident.get('nombre_completo')}' es un alias ficticio. La persona real es {ident.get('nombre_real') or 'su creadora'}.") 
    if ident.get("ciudad"):
        lines.append(f"Ciudad: {ident['ciudad']}, {ident.get('pais', '')}")
    if ident.get("ocupacion"):
        lines.append(f"Ocupacion: {ident['ocupacion']}")

    contacto = p.get("contacto", {})
    if contacto.get("telefonos"):
        lines.append(f"Telefonos: {', '.join(contacto['telefonos'])}")
    if contacto.get("emails"):
        lines.append(f"Emails: {', '.join(contacto['emails'])}")

    redes = p.get("redes_sociales", {})
    redes_activas = {k: v for k, v in redes.items() if v and k != "otros"}
    if redes_activas:
        lines.append(f"Redes sociales: {', '.join(f'{k}={v}' for k, v in redes_activas.items())}")

    familia = p.get("familia", {})
    if familia:
        miembros = [f"{n} ({d.get('relacion', '')})" for n, d in familia.items()]
        lines.append(f"Familia: {', '.join(miembros)}")

    prefs = p.get("preferencias", {})
    if prefs.get("color_favorito"):
        lines.append(f"Color favorito: {prefs['color_favorito']}")
    if prefs.get("musica"):
        lines.append(f"Musica favorita: {prefs['musica']}")
    if prefs.get("hobbies"):
        lines.append(f"Hobbies: {', '.join(prefs['hobbies'])}")

    dispositivos = p.get("dispositivos", {})
    celulares = dispositivos.get("celulares", [])
    if celulares:
        nombres = [c.get("nombre", "Celular") for c in celulares]
        lines.append(f"Celulares registrados: {', '.join(nombres)}")

    return "\n".join(lines) if lines else "Perfil aun no configurado."


def get_family() -> dict:
    """Devuelve el diccionario de familia."""
    return load_profile().get("familia", {})


def get_devices() -> list:
    """Devuelve la lista de celulares registrados."""
    return load_profile().get("dispositivos", {}).get("celulares", [])


def get_emergency_contacts() -> list:
    """Devuelve los contactos de emergencia."""
    return load_profile().get("seguridad", {}).get("contactos_emergencia", [])


# ── Interfaz de configuracion interactiva ─────────────────────────────────────

def setup_profile_interactive():
    """Guia a Sara para configurar su perfil completo."""
    speak("Vamos a configurar tu perfil completo, Sara. Puedes dejar en blanco lo que no quieras compartir.")
    profile = load_profile()

    print("\n=== CONFIGURACION DE PERFIL DE SARA ===\n")

    # Identidad
    print("-- IDENTIDAD --")
    nombre_real = input("Tu nombre real (el que usas en el día a día): ").strip()
    if nombre_real:
        profile["identidad"]["nombre_real"] = nombre_real
        from database import update_memory as _um
        _um("nombre_real", nombre_real)

    ciudad = input("Tu ciudad: ").strip()
    if ciudad:
        profile["identidad"]["ciudad"] = ciudad

    pais = input("Tu pais: ").strip()
    if pais:
        profile["identidad"]["pais"] = pais

    ocupacion = input("Tu ocupacion/trabajo: ").strip()
    if ocupacion:
        profile["identidad"]["ocupacion"] = ocupacion

    # Contacto
    print("\n-- CONTACTO --")
    tel = input("Tu numero de telefono principal: ").strip()
    if tel and tel not in profile["contacto"]["telefonos"]:
        profile["contacto"]["telefonos"].append(tel)

    tel2 = input("Segundo numero (opcional): ").strip()
    if tel2 and tel2 not in profile["contacto"]["telefonos"]:
        profile["contacto"]["telefonos"].append(tel2)

    email = input("Tu email principal: ").strip()
    if email and email not in profile["contacto"]["emails"]:
        profile["contacto"]["emails"].append(email)

    # Redes sociales
    print("\n-- REDES SOCIALES (deja en blanco las que no uses) --")
    for red in ["instagram", "facebook", "twitter", "tiktok", "youtube", "linkedin"]:
        val = input(f"  {red.capitalize()}: ").strip()
        if val:
            profile["redes_sociales"][red] = val

    # Cuentas Google
    print("\n-- CUENTAS GOOGLE --")
    while True:
        cuenta = input("Cuenta de Google (Enter para terminar): ").strip()
        if not cuenta:
            break
        if cuenta not in profile["cuentas_digitales"]["google"]:
            profile["cuentas_digitales"]["google"].append(cuenta)

    # Familia
    print("\n-- FAMILIA (Enter en nombre para terminar) --")
    while True:
        nombre = input("Nombre del familiar: ").strip()
        if not nombre:
            break
        relacion = input(f"  Relacion con {nombre} (madre/padre/hermano/etc): ").strip()
        telefono = input(f"  Telefono de {nombre}: ").strip()
        profile["familia"][nombre] = {
            "relacion": relacion,
            "telefono": telefono,
            "email": "",
            "notas": "",
            "agregado": datetime.now().isoformat()
        }

    # Celulares
    print("\n-- CELULARES --")
    for i in range(1, 3):
        nombre_cel = input(f"Nombre del celular {i} (ej: 'Mi Samsung', Enter para omitir): ").strip()
        if not nombre_cel:
            break
        ip_cel = input(f"  IP del celular {i} en WiFi (ej: 192.168.1.X): ").strip()
        profile["dispositivos"]["celulares"].append({
            "nombre": nombre_cel,
            "tipo": "smartphone",
            "ip": ip_cel,
            "notas": "",
            "registrado": datetime.now().isoformat(),
            "conectado": False
        })

    # Preferencias
    print("\n-- PREFERENCIAS --")
    color = input("Color favorito: ").strip()
    if color:
        profile["preferencias"]["color_favorito"] = color
        update_memory("color_favorito", color)

    musica = input("Genero de musica favorito: ").strip()
    if musica:
        profile["preferencias"]["musica"] = musica

    hobbies = input("Hobbies (separados por coma): ").strip()
    if hobbies:
        profile["preferencias"]["hobbies"] = [h.strip() for h in hobbies.split(",")]

    save_profile(profile)
    speak("Perfil guardado en mi memoria permanente. Ahora te conozco mejor, Sara.")
    print("\n[PERFIL] Guardado correctamente.")
    return profile


if __name__ == "__main__":
    setup_profile_interactive()
