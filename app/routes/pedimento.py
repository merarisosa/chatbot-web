from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

N8N_VALIDAR_URL = os.getenv("N8N_VALIDAR_URL")

@router.get("/validar", response_class=HTMLResponse)
async def validar_page(request: Request):
    nombre_completo = request.cookies.get("nombre_completo")
    rfc = request.cookies.get("rfc")
    usuario = request.cookies.get("usuario")
    return templates.TemplateResponse(
        "validar_pedimento.html",
        {
            "request": request,
            "usuario": usuario,
            "nombre_completo": nombre_completo,
            "rfc": rfc,
            "error": None
        }
    )

@router.post("/validar", response_class=HTMLResponse)
async def validar_pedimento(request: Request, pedimento: str = Form(...)):
    nombre_completo = request.cookies.get("nombre_completo")
    rfc = request.cookies.get("rfc")
    usuario = request.cookies.get("usuario")

    payload = {"pedimento": pedimento, "rfc": rfc, "nombre_completo": nombre_completo, "usuario": usuario}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(N8N_VALIDAR_URL, json=payload)
        
        # Si el servicio no responde 200
        if resp.status_code != 200:
            return templates.TemplateResponse(
                "validar_pedimento.html",
                {"request": request, "error": "⚠️ Error al validar el pedimento. Intenta más tarde."}
            )
        data = resp.json()
        if data.get("valid"):
            return RedirectResponse(url=f"/panel?pedimento={pedimento}", status_code=303)
        else:
            return templates.TemplateResponse(
                "validar_pedimento.html",
                {"request": request, "error": "❌ Pedimento no válido o no encontrado."}
            )   
    
    except httpx.RequestError:
        return templates.TemplateResponse(
            "validar_pedimento.html",
            {"request": request, "error": "🚫 No se pudo conectar con el servidor de validación."}
        )
