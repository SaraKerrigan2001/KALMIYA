FROM python:3.13-slim

WORKDIR /app

# Instalar dependencias de sistema, incluyendo Xvfb y x11vnc para soporte GUI virtual (Opción 3)
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    libasound2-dev \
    libgl1 \
    libglib2.0-0 \
    xvfb \
    x11vnc \
    fluxbox \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements-docker
COPY 04_config/requirements-docker.txt /app/requirements.txt

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script de entrada y darle permisos
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copiar el resto del código
COPY . /app/

# Configurar variables de entorno
ENV DASHBOARD_HOST=0.0.0.0
ENV DASHBOARD_PORT=5000
ENV DISPLAY=:99

# Exponer el puerto del Dashboard y de VNC
EXPOSE 5000 5900

# Usar el script de entrada que arranca Xvfb y VNC antes del proceso principal
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "01_systems/KALMIYA_System/ui/dashboard_server.py"]
