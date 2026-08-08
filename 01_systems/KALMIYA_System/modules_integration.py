
# Stub wrapper to preserve root-level import compatibility.
from intelligence.modules_integration import *

if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
