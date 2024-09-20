# crud/client_crud.py
from models.client import Client
from database import clients_collection
from bson import ObjectId

# Crear un cliente
async def create_client(client: Client):
    client_data = client.dict()
    result = await clients_collection.insert_one(client_data)
    return str(result.inserted_id)

# Obtener clientes
async def get_clients():
    clients = []
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
    await clients_collection.update_one({"_id": ObjectId(id)}, {"$set": client.dict()})

# Eliminar cliente
async def delete_client(id: str):
    await clients_collection.delete_one({"_id": ObjectId(id)})
