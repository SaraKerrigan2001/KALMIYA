
# Stub wrapper to preserve root-level import compatibility.
from services.family_projection import *

if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
