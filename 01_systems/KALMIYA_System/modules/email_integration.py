import os.path
import pickle

try:
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GOOGLE_IMPORTS_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    Request = None
    InstalledAppFlow = None
    build = None
    GOOGLE_IMPORTS_AVAILABLE = False

class EmailIntegration:
    """Integración real con la API de Gmail de Google Workspace."""
    
    # Si modificas estos scopes, borra el archivo token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
              'https://www.googleapis.com/auth/gmail.compose']

    def __init__(self):
        self.creds = None
        self.service = None
        self.is_authenticated = False
        if not GOOGLE_IMPORTS_AVAILABLE:
            print("[GMAIL] Google API no disponible en este entorno; integración desactivada.")
            return
        self._authenticate()

    def _authenticate(self):
        """Autentica a la usuaria usando OAuth2."""
        if not GOOGLE_IMPORTS_AVAILABLE:
            return
        token_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'token.pickle')
        creds_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'credentials.json')
        
        # Ensure config dir exists
        os.makedirs(os.path.dirname(token_path), exist_ok=True)

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)
                
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                    self.is_authenticated = True
                except Exception:
                    self.is_authenticated = False
            else:
                self.is_authenticated = False
                print("[GMAIL] Faltan credenciales. Por favor, ejecuta 'python setup_google_auth.py' primero.")
                return

            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)

        if self.creds and self.creds.valid:
            self.is_authenticated = True
            self.service = build('gmail', 'v1', credentials=self.creds)
            print("[GMAIL] Autenticación con Google exitosa.")

    def fetch_emails(self, max_results=5):
        """Fetch emails from the account."""
        if not self.is_authenticated:
            return {'status': 'error', 'message': 'No autenticada con Google.'}
            
        try:
            results = self.service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
            messages = results.get('messages', [])

            emails_data = []
            if not messages:
                return {'status': 'success', 'count': 0, 'emails': []}
            else:
                for message in messages:
                    msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
                    
                    # Extract subject and sender
                    headers = msg['payload'].get('headers', [])
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin Asunto')
                    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
                    snippet = msg.get('snippet', '')
                    
                    emails_data.append({
                        'id': message['id'],
                        'sender': sender,
                        'subject': subject,
                        'snippet': snippet
                    })
                    
            return {'status': 'success', 'count': len(emails_data), 'emails': emails_data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def read_email(self, email_id):
        """Read a specific email fully."""
        if not self.is_authenticated:
            return None
        try:
            msg = self.service.users().messages().get(userId='me', id=email_id).execute()
            return msg
        except Exception:
            return None

    def summarize_emails(self):
        """Summarize all emails for quick review."""
        res = self.fetch_emails(3)
        if res['status'] == 'error':
            return "No estoy conectada a tu cuenta de Google todavía."
            
        emails = res.get('emails', [])
        if not emails:
            return "No tienes correos nuevos en la bandeja de entrada."
            
        summary = f"Tienes {len(emails)} correos recientes. "
        for i, e in enumerate(emails, 1):
            summary += f"{i}. De {e['sender']} sobre '{e['subject']}'. "
        return summary
