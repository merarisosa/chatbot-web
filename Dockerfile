# Usa una imagen ligera de Python
FROM python:3.12-slim

# Define el directorio de trabajo
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copia los archivos del proyecto
COPY requirements.txt .
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]