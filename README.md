# chatbot-web

Proyecto web para un chatbot: interfaz front-end + lógica back-end integradas para desplegar un bot conversacional que interactúa con usuarios en la web oficial de la empresa

## 🧠 Idea general

Este repositorio constituye la capa web del chatbot: UI, estilos, lógica front-end, además de la integración con microservicios/back-end que procesan las respuestas. Diseñado para ser parte del flujo de automatización de lectura y consulta de pedimentos.

## 🔧 Tecnologías usadas

* Python (back-end) + FastAPI.
* HTML / CSS / JavaScript para la interfaz web.
* Dockerfile + docker-compose para montar el entorno de desarrollo.
* Archivo `requirements.txt` para dependencias Python.
* Scripts de configuración (`setup.sh`) para levantar el proyecto.

## 📂 Estructura del repositorio

```text
app/                    ← Código fuente de la aplicación web  
tests/                  ← Pruebas automatizadas  
Dockerfile              ← Imagen Docker para producción/local  
docker-compose.dev.yml  ← Orquestación de servicios en desarrollo  
requirements.txt        ← Dependencias Python  
setup.sh                ← Script de instalación/configuración  
.gitignore              ← Archivos ignorados en Git  
```

## 🏁 Cómo empezar (modo desarrollo)

1. Clona este repositorio:

   ```bash
   git clone https://github.com/merarisosa/chatbot-web.git
   cd chatbot-web
   ```
2. Ejecuta el script de setup para instalar dependencias y configurar el entorno:

   ```bash
   ./setup.sh
   ```
3. Levanta los servicios vía Docker Compose:

   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```
4. Accede al UI del chatbot a través de tu navegador (ej: `http://localhost:8000` — revisa configuración).
5. Conecta tu back-end / servicio de IA (por ejemplo con n8n, API de propia, etc) para que la interfaz muestre/mande mensajes reales.

## ✅ Principales funcionalidades

* Interfaz web amigable para que el usuario interactúe con el bot.
* Conexión a servicio de backend que gestiona lógica de conversación.
* Contenedor Dockerizado para facilitar despliegue.
* Pruebas automatizadas para asegurar calidad del código (tests/).


