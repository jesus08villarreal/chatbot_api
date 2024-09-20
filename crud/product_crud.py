# crud/product_crud.py
from models.product import Product
from database import products_collection
from bson import ObjectId

# Crear un producto
async def create_product(product: Product):
    product_data = product.dict()
    result = await products_collection.insert_one(product_data)
    return str(result.inserted_id)

# Obtener productos
async def get_products():
    products = []
    async for product in products_collection.find():
        products.append(Product(**product))
    return products

# Obtener un producto por ID
async def get_product_by_id(id: str):
    product = await products_collection.find_one({"_id": ObjectId(id)})
    if product:
        return Product(**product)

# Actualizar producto
async def update_product(id: str, product: Product):
    await products_collection.update_one({"_id": ObjectId(id)}, {"$set": product.dict()})

# Eliminar producto
async def delete_product(id: str):
    await products_collection.delete_one({"_id": ObjectId(id)})
