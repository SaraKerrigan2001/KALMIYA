
# Stub wrapper to preserve root-level import compatibility.
from core.run_backend import *

if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
