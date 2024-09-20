# crud/order_crud.py
from models.order import Order
from database import orders_collection
from bson import ObjectId

# Crear una orden
async def create_order(order: Order):
    order_data = order.dict()
    result = await orders_collection.insert_one(order_data)
    return str(result.inserted_id)

# Obtener órdenes
async def get_orders():
    orders = []
    async for order in orders_collection.find():
        orders.append(Order(**order))
    return orders

# Obtener una orden por ID
async def get_order_by_id(order_id: str):
    order = await orders_collection.find_one({"_id": ObjectId(order_id)})
    if order:
        return Order(**order)

# Actualizar orden
async def update_order(id: str, order: Order):
    await orders_collection.update_one({"_id": ObjectId(id)}, {"$set": order.dict()})

# Eliminar orden
async def delete_order(id: str):
    await orders_collection.delete_one({"_id": ObjectId(id)})
