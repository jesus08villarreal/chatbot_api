from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_whatsapp():
    name = "Chuy"
    response = client.post("/helloword", data={"Body": name})
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello {name}"}

if __name__ == "__main__":
    test_whatsapp()