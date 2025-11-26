from dotenv import load_dotenv
import os
from pathlib import Path

# Detecta si existe .env-dev (modo desarrollo / tests)
DEV_ENV = Path(".env-dev")

if DEV_ENV.exists():
    print("🔧 Cargando entorno de desarrollo (.env-dev)")
    load_dotenv(".env-dev")
else:
    print("🚀 Cargando entorno de producción (.env)")
    load_dotenv()

class Settings:    

    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    API_VALIDACION = os.getenv("API_VALIDACION")
    
    N8N_CHATBOT_URL = os.getenv("N8N_CHATBOT_URL")
    N8N_DOCS_URL = os.getenv("N8N_DOCS_URL")
    N8N_VALIDAR_URL = os.getenv("N8N_VALIDAR_URL")
    N8N_LOGIN_URL = os.getenv("N8N_LOGIN_URL")

    WEBHOOK_N8N_URL = os.getenv("WEBHOOK_N8N_URL")

settings = Settings()
