# crud/client_crud.py
from models.client import Client
from database import clients_collection
from bson import ObjectId
import json

# Crear un cliente
async def create_client(client: Client):
    print(client)
    # Make a json to send to the database
    client_data = client.model_dump()

    result = clients_collection.insert_one(client_data)
    return str(result.inserted_id)

# Obtener clientes
async def get_clients():
    clients = []
    print(clients_collection.find())
    async for client in clients_collection.find():
        clients.append(Client(**client))
    return clients

# Obtener un cliente por teléfono
async def get_client_by_phone(phone: str):
    client = await clients_collection.find_one({"phone": phone})
    if client:
        return Client(**client)

# Actualizar cliente
async def update_client(id: str, client: Client):
    await clients_collection.update_one({"_id": ObjectId(id)}, {"$set": client.model_dump()})

# Eliminar cliente
async def delete_client(id: str):
    await clients_collection.delete_one({"_id": ObjectId(id)})
