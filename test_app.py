import pytest
from fastapi.testclient import TestClient
from app import app  

client = TestClient(app)


# Prueba para el endpoint de WhatsApp
def test_receive_whatsapp():
    response = client.post("/api/whatsapp", json={"Body": "Hola, quiero hacer un pedido"})
    assert response.status_code == 200
