from fastapi import APIRouter
import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    try:
        conn = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {"status": "ok", "db_time": result["now"]}
    except Exception as e:
        return {"status": "error", "details": str(e)}
