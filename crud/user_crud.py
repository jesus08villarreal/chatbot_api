# crud/user_crud.py
from models.user import User
from database import users_collection
from bson import ObjectId

# Crear un usuario
async def create_user(user: User):
    user_data = user.dict()
    result = await users_collection.insert_one(user_data)
    return str(result.inserted_id)

# Obtener usuarios
async def get_users():
    users = []
    async for user in users_collection.find():
        users.append(User(**user))
    return users

# Obtener un usuario por teléfono
async def get_user_by_phone(phone: str):
    user = await users_collection.find_one({"phone": phone})
    if user:
        return User(**user)

# Actualizar usuario
async def update_user(id: str, user: User):
    await users_collection.update_one({"_id": ObjectId(id)}, {"$set": user.dict()})

# Eliminar usuario
async def delete_user(id: str):
    await users_collection.delete_one({"_id": ObjectId(id)})
