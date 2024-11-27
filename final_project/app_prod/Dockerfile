# Dockerfile

# Usar una imagen base oficial de Python slim
FROM python:3.9-slim

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Instalar dependencias del sistema necesarias para MySQL y otras compilaciones
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requisitos primero para aprovechar la cache de Docker
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido de la aplicación al contenedor
COPY . .

# Exponer el puerto en el que Flask correrá
EXPOSE 5000

# Definir la variable de entorno para Flask (opcional, pero recomendado)
ENV FLASK_APP=manage.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para ejecutar la aplicación
CMD ["python", "manage.py"]
