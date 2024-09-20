# routes/order_routes.py
from fastapi import APIRouter, HTTPException
from crud.order_crud import create_order, get_orders, get_order_by_id, update_order, delete_order
from models.order import Order

router = APIRouter()

@router.post("/orders/")
async def create_new_order(order: Order):
    return await create_order(order)

@router.get("/orders/")
async def get_all_orders():
    return await get_orders()

@router.get("/orders/{id}")
async def get_order(id: str):
    order = await get_order_by_id(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{id}")
async def update_order_data(id: str, order: Order):
    await update_order(id, order)
    return {"message": "Order updated"}

@router.delete("/orders/{id}")
async def delete_order_data(id: str):
    await delete_order(id)
    return {"message": "Order deleted"}
