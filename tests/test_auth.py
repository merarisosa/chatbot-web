import pytest
from fastapi.testclient import TestClient
import respx
from httpx import Response

from app.main import app
from app.core.config import settings

client = TestClient(app)

@pytest.mark.asyncio
@respx.mock
async def test_login_valido():
    # --- Arrange ---
    # Mock de la respuesta del webhook de n8n
    mock = respx.post(settings.N8N_LOGIN_URL).mock(
        return_value=Response(
            status_code=200,
            json={
                "valid": True,
                "rfc": "MASM0103039C0",
                "nombre_completo": "Merari May Sosa",
                "usuario": "admin"
            }
        )
    )

    # --- Act ---
    response = client.post(
        "/login",
        data={"usuario": "admin", "contrasena": "admin123"},
        follow_redirects=False  #  para capturar el 303
    )

    # --- Assert ---
    # 1. Se llamó al webhook mockeado
    assert mock.called

    # 2. El login devuelve redirect 303
    assert response.status_code == 303
    assert response.headers["location"] == "/validar"

    # 3. Verificar cookies generadas
    cookies = response.cookies
    assert cookies.get("rfc") == "MASM0103039C0"
    assert cookies.get("nombre_completo").strip('"') == "Merari May Sosa"
    assert cookies.get("usuario") == "admin"


@respx.mock
def test_login_invalido():
    # --- Arrange ---
    # Mock del webhook de n8n devolviendo credenciales inválidas
    mock = respx.post(settings.N8N_LOGIN_URL).mock(
        return_value=Response(
            status_code=200,
            json={"valid": False}  # n8n dice: usuario inválido
        )
    )

    # --- Act ---
    response = client.post(
        "/login",
        data={"usuario": "admin", "contrasena": "contrasena_incorrecta"},
        follow_redirects=True  # sigue el render del template
    )

    # --- Assert ---
    # 1. Se llamó al mock
    assert mock.called

    # 2. La respuesta NO es 303, es 200 porque se re-renderiza la página
    assert response.status_code == 200

    # 3. El HTML debe contener el mensaje de error
    assert "Credenciales inválidas" in response.text or "❌" in response.text
