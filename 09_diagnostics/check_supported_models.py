import requests
from decouple import config

GEMINI_KEY = config('GEMINI_API_KEY', default='')

def check_supported_models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_KEY}"
    resp = requests.get(url)
    if resp.status_code == 200:
        models = resp.json().get('models', [])
        for m in models:
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                name = m['name']
                if 'flash' in name.lower() or 'pro' in name.lower():
                    print(f"Supported: {name}")
    else:
        print(f"Error listing: {resp.status_code}")

if __name__ == "__main__":
    check_supported_models()
