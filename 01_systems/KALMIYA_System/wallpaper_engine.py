
# Stub wrapper to preserve root-level import compatibility.
from ui.wallpaper_engine import *

if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
