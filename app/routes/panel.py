from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
import httpx

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

CHATBOT_URL = "https://hostinger.merrmsdev.work.gd/webhook/chatbot"
DOCS_URL = "http://api-validacion.merrmsdev.work.gd/api/documentos"

@router.get("/panel")
async def chat_panel(request: Request, pedimento: str = Query(...)):
    async with httpx.AsyncClient() as client:
        docs = await client.get(f"{DOCS_URL}?pedimento={pedimento}")
    documentos = docs.json().get("documentos", [])
    return templates.TemplateResponse("chat_panel.html", {"request": request, "pedimento": pedimento, "documentos": documentos})
