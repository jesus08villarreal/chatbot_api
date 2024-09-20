# routes/product_routes.py
from fastapi import APIRouter, HTTPException
from crud.product_crud import create_product, get_products, get_product_by_id, update_product, delete_product
from models.product import Product

router = APIRouter()

@router.post("/products/")
async def create_new_product(product: Product):
    return await create_product(product)

@router.get("/products/")
async def get_all_products():
    return await get_products()

@router.get("/products/{id}")
async def get_product(id: str):
    product = await get_product_by_id(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{id}")
async def update_product_data(id: str, product: Product):
    await update_product(id, product)
    return {"message": "Product updated"}

@router.delete("/products/{id}")
async def delete_product_data(id: str):
    await delete_product(id)
    return {"message": "Product deleted"}
