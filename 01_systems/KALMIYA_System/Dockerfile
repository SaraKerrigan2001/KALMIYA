FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (e.g. for audio/opencv)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libasound2-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expone puertos comunes (API y MCP)
EXPOSE 8000
EXPOSE 8765

CMD ["python", "api_server.py"]
