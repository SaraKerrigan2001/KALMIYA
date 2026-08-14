
# Stub wrapper to preserve root-level import compatibility.
from intelligence.kalmiya_mcp import *

if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
