#!/bin/bash
# entrypoint.sh - Start Xvfb and VNC before the main application

# Remove X11 lock files if they exist (happens after ungraceful restarts)
rm -f /tmp/.X99-lock

# Iniciar Xvfb en display :99
echo "Iniciando servidor X virtual (Xvfb)..."
Xvfb :99 -screen 0 1280x800x24 &
sleep 2

# Iniciar x11vnc sin contraseña para debug local (¡no usar en prod público!)
echo "Iniciando servidor VNC en puerto 5900..."
x11vnc -display :99 -nopw -listen 0.0.0.0 -xkb -ncache 10 -ncache_cr -forever &

# Exportar la variable DISPLAY para que las apps gráficas de Python la usen
export DISPLAY=:99

# Ejecutar el comando pasado al contenedor (ej. python dashboard_server.py)
echo "Iniciando KALMIYA..."
exec "$@"
