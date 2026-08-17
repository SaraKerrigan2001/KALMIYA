import sys
from unittest.mock import MagicMock

def apply_linux_mocks():
    """
    Opción 1: Refactorización Modular (Mocks)
    Inyecta mocks en sys.modules para dependencias de Windows cuando 
    KALMIYA se ejecuta en Linux (Docker), previniendo que la aplicación 
    se cuelgue por ImportErrors.
    """
    if sys.platform != "win32":
        # Dependencias exclusivas de Windows y GUI que fallarían en Linux
        win_modules = [
            'win32gui', 'win32con', 'win32api', 'win32process', 
            'pypiwin32', 'PyGetWindow', 'PyAutoGUI', 'PyScreeze',
            'PyRect', 'PyMsgBox', 'pytweening', 'MouseInfo'
        ]
        
        for mod in win_modules:
            if mod not in sys.modules:
                sys.modules[mod] = MagicMock()
        
        print("[Core] Mocks de Linux aplicados exitosamente para compatibilidad OS.")
