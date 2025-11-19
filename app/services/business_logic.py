import os
import psycopg2
from psycopg2.extras import RealDictCursor
from app.models.schemas import ValidacionResponse
from app.models.schemas import ReporteResponse
from app.core.config import settings

# 🔧 Conexión a PostgreSQL
conn = psycopg2.connect(
    host= settings.POSTGRES_HOST,
          port=settings.POSTGRES_PORT,
          dbname=settings.POSTGRES_DB,
          user=settings.POSTGRES_USER,
          password=settings.POSTGRES_PASSWORD
)

def generar_reporte(fecha_inicio: str, fecha_fin: str, tipo: str = "general"):
    # Simulación temporal para pruebas
    return ReporteResponse(
        total_pedimentos=3,
        periodo=f"{fecha_inicio} → {fecha_fin}",
        detalles=[
            {"pedimento": "2585174450", "estatus": "Liberado"},
            {"pedimento": "2585174451", "estatus": "En revisión"},
            {"pedimento": "2585174452", "estatus": "Pendiente"}
        ]
    )

def validar_pedimento(pedimento: str, rfc: str = None):
    print(f"🔎 Validando pedimento: {pedimento}, RFC: {rfc}")
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
                SELECT numero_pedimento, rfcs, estatus
                FROM pedimentos
                WHERE numero_pedimento = %s
            """
            cur.execute(query, (pedimento,))
            result = cur.fetchone()
            print(f"📄 Resultado DB: {result}")

        # 🧩 Caso 1: No existe el pedimento
        if not result:
            return {
                "pedimento": pedimento,
                "valido": False,
                "mensaje": f"❌ El pedimento {pedimento} no existe o no se ha cargado en el sistema."
            }

        rfcs_asociados = result["rfcs"]
        estatus = result.get("estatus", "Desconocido")

        # 🧩 Caso 2: RFC no enviado
        if not rfc:
            return {
                "pedimento": pedimento,
                "valido": True,
                "mensaje": f"ℹ️ Pedimento {pedimento} válido. RFCs asociados: {', '.join(rfcs_asociados)}. Estatus: {estatus}"
            }

        # 🧩 Caso 3: RFC enviado y coincide
        if rfc in rfcs_asociados:
            return {
                "pedimento": pedimento,
                "valido": True,
                "mensaje": f"✅ Pedimento {pedimento} válido para RFC {rfc}. Estatus: {estatus}"
            }

        # 🧩 Caso 4: RFC no coincide
        return {
            "pedimento": pedimento,
            "valido": False,
            "mensaje": f"⚠️ El pedimento {pedimento} existe, pero el RFC {rfc} no está asociado. RFCs válidos: {', '.join(rfcs_asociados)}"
        }

    except Exception as e:
        print(f"❌ Error durante validación: {e}")
        conn.rollback()
        return {
            "pedimento": pedimento,
            "valido": False,
            "mensaje": f"💥 Error interno durante la validación: {e}"
        }
