from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

##def test_whatsapp():
 #   name = "Chatbot"
 #   response = client.post("/whatsapp", data={"Body": name})
 #   assert response.status_code == 200
 #   assert response.json() == {"message": f"Hello {name}"}
