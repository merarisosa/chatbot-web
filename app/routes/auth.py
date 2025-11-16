from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import httpx
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

N8N_LOGIN_URL = os.getenv("N8N_LOGIN_URL") 

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Muestra el formulario de login"""
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@router.post("/login", response_class=HTMLResponse)
async def login_user(request: Request, usuario: str = Form(...), contrasena: str = Form(...)):
    """Valida el usuario contra n8n"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(N8N_LOGIN_URL, json={"usuario": usuario, "contrasena": contrasena})

    # Si el webhook responde con {"valid": true}
    if resp.status_code == 200 and resp.json().get("valid"):
        return RedirectResponse(url="/validar", status_code=303)

    # Si no, mostrar error
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "error": "Credenciales inválidas ❌"}
    )