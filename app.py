from fastapi import FastAPI
from database import engine, Base
from utils.auth import APIKeyMiddleware
from routes import client_routes, product_routes, order_routes, whatsapp_routes
from dotenv import load_dotenv
from fastapi import Form

load_dotenv()

app = FastAPI()

# app.add_middleware(APIKeyMiddleware)

app.include_router(client_routes.router, prefix="/api")
app.include_router(product_routes.router, prefix="/api")
app.include_router(order_routes.router, prefix="/api")
app.include_router(whatsapp_routes.router, prefix="/api")


async def startup():
    Base.metadata.create_all(bind=engine)

app.add_event_handler("startup", startup)

@app.post("/helloword")
async def hello_word(Body: str = Form(...)):
    name = Body
    return {"message": name}