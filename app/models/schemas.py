from pydantic import BaseModel, Field
from typing import Optional

class ValidacionRequest(BaseModel):
    pedimento: str = Field(..., description="Número de pedimento a validar")
    rfc: Optional[str] = Field(None, description="RFC del importador/exportador")

class ValidacionResponse(BaseModel):
    pedimento: str
    valido: bool
    mensaje: str

class ReporteRequest(BaseModel):
    fecha_inicio: str
    fecha_fin: str
    tipo: Optional[str] = "general"

class ReporteResponse(BaseModel):
    total_pedimentos: int
    periodo: str
    detalles: list
