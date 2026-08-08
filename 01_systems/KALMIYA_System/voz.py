
# Stub wrapper to preserve root-level import compatibility.
from audio.voz import *

if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
