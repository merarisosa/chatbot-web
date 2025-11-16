from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import chat, health, validation
from app.routes import auth, pedimento, panel

app = FastAPI(title="Chatbot Aduanal - Web")

app.include_router(chat.router)
app.include_router(validation.router)
app.include_router(health.router, prefix="/api")

app.include_router(auth.router)
app.include_router(pedimento.router)
app.include_router(panel.router)

# Montar estáticos y templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def root():
    return {"msg": "API Chatbot Aduanal activa 🚀"}

@app.get("/chat-web", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Registrar rutas del chat
app.include_router(chat.router, prefix="/chat", tags=["chat"])
