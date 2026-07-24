import requests
import json
from decouple import config

GEMINI_KEY = config('GEMINI_API_KEY', default='')

def test_gemini():
    if not GEMINI_KEY:
        print("No API Key found.")
        return

    # Try different versions and model names
    versions = ["v1", "v1beta"]
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro",
        "gemini-1.5-pro-latest",
        "gemini-pro"
    ]

    for v in versions:
        for model in models_to_try:
            url = f"https://generativelanguage.googleapis.com/{v}/models/{model}:generateContent?key={GEMINI_KEY}"
            payload = {
                "contents": [{
                    "parts": [{"text": "Hola, respondeme brevemente."}]
                }]
            }
            
            print(f"Testing version: {v}, model: {model}...")
            try:
                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    print(f"Success with {v}/{model}!")
                    return model
                else:
                    print(f"Failed with {v}/{model}: {response.status_code}")
            except Exception as e:
                print(f"Error with {v}/{model}: {e}")

    # List models
    print("\nAttempting to list available models...")
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_KEY}"
    try:
        resp = requests.get(list_url, timeout=10)
        if resp.status_code == 200:
            models = resp.json().get('models', [])
            print("Available models:")
            for m in models:
                print(f" - {m['name']}")
        else:
            print(f"Failed to list models: {resp.status_code}")
            print(resp.text)
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    test_gemini()
