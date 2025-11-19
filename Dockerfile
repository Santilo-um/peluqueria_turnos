FROM python:3.11-slim

WORKDIR /app

# Copiamos todo el proyecto (incluye entrypoint.sh si está en la raíz)
COPY . .

# Damos permisos de ejecución al script
RUN chmod +x entrypoint.sh

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto del servidor
EXPOSE 5000

# Ejecutamos el script
ENTRYPOINT ["./entrypoint.sh"]