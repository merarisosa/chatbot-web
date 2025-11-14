from fastapi import APIRouter, HTTPException
from app.services.orchestrator import send_to_n8n

router = APIRouter()

@router.post("/")
async def chat_message(message: dict):
    try:
        response = await send_to_n8n(message.get("text", ""))
        return {"reply": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
