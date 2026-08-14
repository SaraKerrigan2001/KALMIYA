
# Stub wrapper to preserve root-level import compatibility.
from services.setup_google_auth import *

if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
