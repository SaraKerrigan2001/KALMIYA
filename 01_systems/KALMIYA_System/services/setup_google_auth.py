import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

# Si modificas estos scopes, borra el archivo token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.compose']

def main():
    """Muestra un navegador para iniciar sesión en Google y guarda el token."""
    creds = None
    config_dir = os.path.join(os.path.dirname(__file__), 'config')
    os.makedirs(config_dir, exist_ok=True)
    
    token_path = os.path.join(config_dir, 'token.pickle')
    creds_path = os.path.join(config_dir, 'credentials.json')

    if not os.path.exists(creds_path):
        print("="*60)
        print("ERROR: Faltan las credenciales de la API de Google (credentials.json).")
        print("Pasos para obtenerlo:")
        print("1. Ve a https://console.cloud.google.com/")
        print("2. Crea un proyecto y habilita la 'Gmail API'")
        print("3. Crea credenciales tipo 'OAuth client ID' (Desktop App)")
        print("4. Descarga el JSON, renómbralo a 'credentials.json' y ponlo en la carpeta 'config/'")
        print("="*60)
        return

    print("Iniciando flujo de autenticación. Se abrirá una ventana en tu navegador...")
    try:
        flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Guardar las credenciales
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
            
        print("\n¡Autenticación exitosa! KALMIYA ahora está conectada a tu cuenta de Google.")
    except Exception as e:
        print(f"\nError durante la autenticación: {e}")

if __name__ == '__main__':
    main()
