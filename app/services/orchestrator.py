import httpx
import os
from dotenv import load_dotenv

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("WEBHOOK_N8N_URL")

async def send_to_n8n(text: str) -> str:
    async with httpx.AsyncClient() as client:
        res = await client.post(N8N_WEBHOOK_URL, json={"message": text})
        data = res.json()
        return data.get("reply", "No se recibió respuesta del flujo n8n.")
