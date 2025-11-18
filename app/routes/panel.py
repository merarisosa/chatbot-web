from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
import os
from uuid import uuid4

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

CHATBOT_URL = os.getenv("N8N_CHATBOT_URL")  
DOCS_URL = os.getenv("N8N_DOCS_URL")

@router.get("/panel", response_class=HTMLResponse)
async def chat_panel(request: Request, pedimento: str = Query(...)):
    # Traer datos de usuario desde cookies
    nombre_completo = request.cookies.get("nombre_completo", "Usuario")
    rfc = request.cookies.get("rfc", "")

    # 🔹 Crear un session_id nuevo por cada pedimento
    session_id = str(uuid4())

    # Llamada al endpoint de documentos
    documentos = []
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            docs = await client.get(f"{DOCS_URL}?pedimento={pedimento}&rfc={rfc}")
            if docs.status_code == 200:
                documentos = docs.json().get("documentos", [])
    except Exception as e:
        print(f"⚠️ Error obteniendo documentos: {e}")

    response = templates.TemplateResponse(
        "chat_panel.html",
        {
            "request": request,
            "pedimento": pedimento,
            "documentos": documentos,
            "nombre_completo": nombre_completo,
            "CHATBOT_URL": CHATBOT_URL,
            "session_id": session_id
        }
    )

    response.set_cookie("session_id", session_id)
    return response
