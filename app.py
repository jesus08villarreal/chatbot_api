from fastapi import FastAPI
from database import init_db
from utils.auth import APIKeyMiddleware
from routes import client_routes, product_routes, order_routes, whatsapp_routes
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# app.add_middleware(APIKeyMiddleware)

app.include_router(client_routes.router, prefix="/api")
app.include_router(product_routes.router, prefix="/api")
app.include_router(order_routes.router, prefix="/api")
app.include_router(whatsapp_routes.router, prefix="/api")

async def startup():
    init_db()

app.add_event_handler("startup", startup)

# 
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000)