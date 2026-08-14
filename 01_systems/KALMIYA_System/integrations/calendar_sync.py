"""
KALMIYA Calendar Sync v3.6
Sincronización bidireccional con Google Calendar, Outlook, y gestores de tareas
Alimenta el skill "Plan" con datos reales de calendario y prioridades
"""

import os
import pickle
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scopes para Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events']

class CalendarSync:
    """
    Sincronizador de calendario para KALMIYA
    Soporta Google Calendar, con posibilidad de extender a Outlook
    """
    
    def __init__(self, credentials_path: str = None):
        """
        Inicializa el sincronizador
        
        Args:
            credentials_path: Ruta al archivo credentials.json de Google
        """
        if credentials_path is None:
            credentials_path = Path(__file__).parent.parent / "config" / "credentials.json"
        
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(__file__).parent.parent / "config" / "token.pickle"
        self.service = None
        
        # Rutas de salida
        self.output_path = Path(__file__).parent.parent.parent / "KALMIYA" / "raw" / "calendar"
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📅 Calendar Sync inicializado")
        print(f"📁 Output: {self.output_path}")
    
    def authenticate(self):
        """Autentica con Google Calendar API"""
        creds = None
        
        # Cargar token existente si existe
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # Si no hay credenciales válidas, obtener nuevas
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.credentials_path.exists():
                    print(f"""
⚠️  CONFIGURACIÓN REQUERIDA:

1. Ve a: https://console.cloud.google.com/
2. Crea un proyecto nuevo o usa uno existente
3. Habilita Google Calendar API
4. Crea credenciales OAuth 2.0
5. Descarga el JSON y guárdalo como:
   {self.credentials_path}

Luego ejecuta este script nuevamente.
                    """)
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Guardar token para próximas ejecuciones
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('calendar', 'v3', credentials=creds)
        print("✅ Autenticación exitosa con Google Calendar")
        return True
    
    def get_todays_events(self) -> List[Dict]:
        """
        Obtiene eventos de hoy
        
        Returns:
            Lista de eventos del día
        """
        if not self.service:
            if not self.authenticate():
                return []
        
        # Definir rango de tiempo (hoy desde las 00:00 hasta las 23:59)
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        try:
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=today_start.isoformat() + 'Z',
                timeMax=today_end.isoformat() + 'Z',
                maxResults=50,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            formatted_events = []
            for event in events:
                formatted_events.append({
                    'id': event.get('id'),
                    'summary': event.get('summary', 'Sin título'),
                    'start': event.get('start', {}).get('dateTime', event.get('start', {}).get('date')),
                    'end': event.get('end', {}).get('dateTime', event.get('end', {}).get('date')),
                    'location': event.get('location', ''),
                    'description': event.get('description', ''),
                    'attendees': event.get('attendees', [])
                })
            
            print(f"📅 Eventos de hoy: {len(formatted_events)}")
            return formatted_events
            
        except Exception as e:
            print(f"⚠️  Error obteniendo eventos: {e}")
            return []
    
    def get_week_events(self, weeks: int = 1) -> List[Dict]:
        """
        Obtiene eventos de las próximas semanas
        
        Args:
            weeks: Número de semanas a consultar
            
        Returns:
            Lista de eventos
        """
        if not self.service:
            if not self.authenticate():
                return []
        
        now = datetime.now()
        end_date = now + timedelta(weeks=weeks)
        
        try:
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now.isoformat() + 'Z',
                timeMax=end_date.isoformat() + 'Z',
                maxResults=100,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            formatted_events = []
            for event in events:
                formatted_events.append({
                    'id': event.get('id'),
                    'summary': event.get('summary', 'Sin título'),
                    'start': event.get('start', {}).get('dateTime', event.get('start', {}).get('date')),
                    'end': event.get('end', {}).get('dateTime', event.get('end', {}).get('date')),
                    'location': event.get('location', ''),
                    'description': event.get('description', '')
                })
            
            print(f"📅 Eventos próximas {weeks} semanas: {len(formatted_events)}")
            return formatted_events
            
        except Exception as e:
            print(f"⚠️  Error obteniendo eventos: {e}")
            return []
    
    def sync_to_vault(self):
        """Sincroniza eventos al vault de KALMIYA"""
        today_events = self.get_todays_events()
        week_events = self.get_week_events(weeks=2)
        
        # Guardar eventos de hoy
        today_file = self.output_path / f"today_{datetime.now().strftime('%Y%m%d')}.json"
        with open(today_file, 'w', encoding='utf-8') as f:
            json.dump({
                'date': datetime.now().isoformat(),
                'events': today_events,
                'count': len(today_events)
            }, f, indent=2, ensure_ascii=False)
        
        # Guardar eventos de la semana
        week_file = self.output_path / f"week_{datetime.now().strftime('%Y%m%d')}.json"
        with open(week_file, 'w', encoding='utf-8') as f:
            json.dump({
                'date': datetime.now().isoformat(),
                'events': week_events,
                'count': len(week_events)
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Calendario sincronizado:")
        print(f"   📄 Hoy: {today_file}")
        print(f"   📄 Semana: {week_file}")
        
        return today_events, week_events
    
    def get_priorities_for_plan(self) -> List[Dict]:
        """
        Genera prioridades para el skill "Plan" basadas en calendario
        
        Returns:
            Lista de prioridades del día
        """
        events = self.get_todays_events()
        
        priorities = []
        
        for event in events[:3]:  # Top 3 eventos
            start_time = event['start']
            if 'T' in start_time:  # Evento con hora
                time_str = datetime.fromisoformat(start_time.replace('Z', '')).strftime('%H:%M')
                priorities.append({
                    'title': event['summary'],
                    'time': time_str,
                    'type': 'calendar_event',
                    'priority': 'high',
                    'source': 'Google Calendar'
                })
        
        return priorities
    
    def create_event(self, summary: str, start_time: datetime, end_time: datetime, 
                    description: str = '', location: str = '') -> bool:
        """
        Crea un nuevo evento en el calendario
        
        Args:
            summary: Título del evento
            start_time: Hora de inicio
            end_time: Hora de fin
            description: Descripción opcional
            location: Ubicación opcional
            
        Returns:
            True si se creó exitosamente
        """
        if not self.service:
            if not self.authenticate():
                return False
        
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Bogota',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Bogota',
            },
        }
        
        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f"✅ Evento creado: {event.get('htmlLink')}")
            return True
        except Exception as e:
            print(f"⚠️  Error creando evento: {e}")
            return False


# Funciones de utilidad

def sync_calendar_now():
    """Sincroniza calendario inmediatamente"""
    sync = CalendarSync()
    return sync.sync_to_vault()

def get_today_priorities():
    """Obtiene prioridades del día basadas en calendario"""
    sync = CalendarSync()
    return sync.get_priorities_for_plan()


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         KALMIYA CALENDAR SYNC v3.6 - DEMO                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    sync = CalendarSync()
    
    # Sincronizar
    today, week = sync.sync_to_vault()
    
    # Mostrar eventos de hoy
    print(f"\n📅 EVENTOS DE HOY ({len(today)}):")
    for i, event in enumerate(today, 1):
        print(f"{i}. {event['summary']}")
        print(f"   ⏰ {event['start']}")
        if event.get('location'):
            print(f"   📍 {event['location']}")
        print()
    
    # Mostrar prioridades
    priorities = sync.get_priorities_for_plan()
    print(f"\n🎯 PRIORIDADES PARA SKILL PLAN ({len(priorities)}):")
    for i, priority in enumerate(priorities, 1):
        print(f"{i}. [{priority['time']}] {priority['title']}")
