
# Stub wrapper to preserve root-level import compatibility.
from core.kalmiya_core import *

if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
