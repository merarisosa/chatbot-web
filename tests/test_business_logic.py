from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1️⃣ Prueba de validación (endpoint /api/validar)
def test_validar_pedimento_valido():
    payload = {"pedimento": "2585174450", "rfc": "MASM0103039C0"}
    response = client.post("/api/validar", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["valido"] is True
    assert "✅" in data["mensaje"]
    assert data["pedimento"] == "2585174450"

def test_validar_pedimento_invalido():
    payload = {"pedimento": "1480000012", "rfc": "MASM0103039C0"}
    response = client.post("/api/validar", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["valido"] is False
    assert "❌" in data["mensaje"]

# 2️⃣ Prueba de generación de reportes (/api/generar-reporte)
def test_generar_reporte():
    payload = {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-01-10"}
    response = client.post("/api/generar-reporte", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "periodo" in data
    assert "detalles" in data
    assert isinstance(data["detalles"], list)
    assert data["total_pedimentos"] == 5
