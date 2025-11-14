from fastapi import APIRouter
from app.models.schemas import ValidacionRequest, ReporteRequest
from app.services.business_logic import validar_pedimento, generar_reporte

router = APIRouter(prefix="/api", tags=["Validación y Reportes"])

@router.post("/validar")
def validar(req: ValidacionRequest):
    return validar_pedimento(req.pedimento, req.rfc)

@router.post("/generar-reporte")
def generar(req: ReporteRequest):
    return generar_reporte(req.fecha_inicio, req.fecha_fin, req.tipo)
