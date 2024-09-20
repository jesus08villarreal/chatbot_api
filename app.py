from fastapi import FastAPI, Depends
from utils.auth import APIKeyMiddleware
from routes import client_routes, product_routes, order_routes, whatsapp_routes, user_routes, company_routes
from dotenv import load_dotenv
from fastapi import Form
from database import get_db

load_dotenv()
print ("Starting...")
app = FastAPI()

# app.add_middleware(APIKeyMiddleware)

app.include_router(client_routes.router, prefix="/api")
app.include_router(company_routes.router, prefix="/api")
app.include_router(product_routes.router, prefix="/api")
app.include_router(user_routes.router, prefix="/api")
app.include_router(order_routes.router, prefix="/api")
app.include_router(whatsapp_routes.router, prefix="/api")


async def startup():
    print("Starting up...")

app.add_event_handler("startup", startup)

@app.get("/test-db")
def test_db(db=Depends(get_db)):
    # Ejemplo de uso de la base de datos
    collections = db.list_collection_names()
    return {"collections": collections}