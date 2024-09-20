# routes/client_route.py
from fastapi import APIRouter, HTTPException
from crud.client_crud import create_client, get_clients, get_client_by_phone, update_client, delete_client
from models.client import Client

router = APIRouter()

@router.post("/clients/")
async def create_new_client(client: Client):
    return await create_client(client)

@router.get("/clients/")
async def get_all_clients():
    return await get_clients()

@router.get("/clients/{phone}")
async def get_client(phone: str):
    client = await get_client_by_phone(phone)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/clients/{id}")
async def update_client_data(id: str, client: Client):
    await update_client(id, client)
    return {"message": "Client updated"}

@router.delete("/clients/{id}")
async def delete_client_data(id: str):
    await delete_client(id)
    return {"message": "Client deleted"}
