from pathlib import Path
import sys

# Añade la ruta al núcleo de KALMIYA para que los tests puedan importar los paquetes locales.
ROOT = Path(__file__).resolve().parents[1]
KALMIYA_SYS = ROOT / "01_systems" / "KALMIYA_System"

if str(KALMIYA_SYS) not in sys.path:
    sys.path.insert(0, str(KALMIYA_SYS))

# También añadir la raíz del repo por si algún test importa desde la raíz.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
