#!/bin/bash
echo "🚀 Iniciando configuración del proyecto Chatbot Aduanal..."

# ==============================================
# 🧩 Paso 1: Activar entorno virtual o crearlo si no existe
# ==============================================
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

echo "💡 Activando entorno virtual..."
source venv/bin/activate

# ==============================================
# 🧰 Paso 2: Instalar dependencias
# ==============================================
if [ -f "requirements.txt" ]; then
    echo "📚 Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt
else
    echo "⚠️ No se encontró requirements.txt — creando uno básico..."
    echo "fastapi\nuvicorn\ndotenv\npsycopg2" > requirements.txt
    pip install -r requirements.txt
fi

# ==============================================
# 🔐 Paso 3: Verificar archivo .env
# ==============================================
if [ ! -f ".env" ]; then
    echo "⚙️ Creando archivo .env predeterminado..."
    cat <<EOF > .env
POSTGRES_HOST=72.60.112.24
POSTGRES_PORT=5432
POSTGRES_DB=msc_chatbot
POSTGRES_USER=merr
POSTGRES_PASSWORD=admin@merr
EOF
else
    echo "✅ Archivo .env ya existe."
fi

# ==============================================
# 🧠 Paso 4: Verificar conexión a la base de datos
# ==============================================
echo "🔍 Verificando conexión con la base de datos..."
python check_db.py
if [ $? -ne 0 ]; then
    echo "❌ Error de conexión con la base de datos. Revisa tu .env."
    exit 1
fi

# ==============================================
# 💬 Paso 5: Iniciar FastAPI con Uvicorn
# ==============================================
echo "🔥 Levantando servidor FastAPI..."
uvicorn app.main:app --reload
