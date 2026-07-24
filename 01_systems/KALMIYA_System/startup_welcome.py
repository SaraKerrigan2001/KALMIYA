import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(__file__))

from bienvenida import greet_user

if __name__ == "__main__":
    greet_user()