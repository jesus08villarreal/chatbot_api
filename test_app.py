from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_whatsapp():
    response = client.post("/whatsapp", data={"Body": "2 pizzas and 3 sodas"})
    assert response.status_code == 200
    assert "Pedido registrado" in response.text
