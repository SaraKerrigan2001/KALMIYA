
# Stub wrapper to preserve root-level import compatibility.
from core.splash_screen import *

if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
