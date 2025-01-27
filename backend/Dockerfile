FROM python:3.10-slim

# Instalar las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y wait-for-it\
    build-essential \
    cmake \
    python3-dev \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY  requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000

# Comando para ejecutar el backend
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
