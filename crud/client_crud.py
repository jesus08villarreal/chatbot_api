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
    # Get client by phone
    client_by_phone = await get_client_by_phone(client_data['phone'])
    print(client_by_phone)
    # If the client already exists, return the id
    if client_by_phone:
        return str(client_by_phone.objectId)

    result = clients_collection.insert_one(client_data)
    return str(result.inserted_id)

# Obtener clientes
async def get_clients():
    clients = []
    print(clients_collection.find())
    for client in clients_collection.find():
        print("before",client)
        client["_id"] = str(client["_id"])
        print("after", client)
        clients.append(Client(**client))
    return clients

# Obtener un cliente por teléfono
async def get_client_by_phone(phone: str):
    client = clients_collection.find_one({"phone": phone})
    if client:
        return Client(**client)

# Actualizar cliente
async def update_client(id: str, client: Client):
    clients_collection.update_one({"_id": ObjectId(id)}, {"$set": client.model_dump()})
    return True

# Eliminar cliente
async def delete_client(id: str):
    clients_collection.delete_one({"_id": ObjectId(id)})
    return True
