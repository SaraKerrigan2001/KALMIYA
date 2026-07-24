# pyrefly: ignore [missing-import]
from PIL import Image
import os

img_path = r"C:\Users\maria\.gemini\antigravity\brain\44750c5a-96b3-48ea-b668-b9b975d443b8\kalmiya_app_icon_1778296227303.png"
out_path = r"c:\Users\maria\env\kalmiya.ico"

if os.path.exists(img_path):
    img = Image.open(img_path)
    # Redimensionar para tamaños estándar de iconos de Windows
    icon_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    img.save(out_path, format='ICO', sizes=icon_sizes)
    print(f"Icono creado en {out_path}")
else:
    print("No se encontró la imagen original.")
