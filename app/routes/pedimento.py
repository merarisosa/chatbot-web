from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

VALIDAR_URL = "http://api-validacion.merrmsdev.work.gd/api/validar"

@router.get("/validar", response_class=HTMLResponse)
async def validar_page(request: Request):
    return templates.TemplateResponse("validar_pedimento.html", {"request": request, "error": None})

@router.post("/validar", response_class=HTMLResponse)
async def validar_pedimento(request: Request, pedimento: str = Form(...)):
    async with httpx.AsyncClient() as client:
        resp = await client.post(VALIDAR_URL, json={"pedimento": pedimento})
    
    data = resp.json()
    if data.get("valido"):
        return RedirectResponse(url=f"/panel?pedimento={pedimento}", status_code=303)
    else:
        return templates.TemplateResponse("validar_pedimento.html", {"request": request, "error": "Pedimento no válido ❌"})
