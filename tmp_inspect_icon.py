from PIL import Image
import os
path = r'01_systems\\KALMIYA_System\\kalmiya.ico'
print('exists', os.path.exists(path))
with Image.open(path) as img:
    print('format', img.format)
    print('size', img.size)
    frames = []
    i = 0
    while True:
        try:
            img.seek(i)
            frames.append((i, img.size, img.mode, dict(img.info)))
            i += 1
        except EOFError:
            break
    print('frames', frames)
