
# Stub wrapper to preserve root-level import compatibility.
from services.obsidian_bridge import *

if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
