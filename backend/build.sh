#!/bin/bash
# Terminar el script si hay un error
set -o errexit

# Actualizar e instalar dependencias del sistema
apt-get update && apt-get install -y wait-for-it \
    build-essential \
    cmake \
    g++ \
    make \
    libatlas-base-dev \
    libboost-all-dev \
    libeigen3-dev \
    python3-dev \
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

# Instalar dependencias de Python desde requirements.txt
pip install -r requirements.txt

# Ejecutar comandos de Django: recolectar archivos estáticos y migrar la base de datos
python manage.py collectstatic --no-input
python manage.py migrate


# if [[ $CREATE_SUPERUSER ]]
# then
#     python manage.py createsuperuser --no-input
# fi