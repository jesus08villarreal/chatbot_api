from pydantic import BaseModel

class OrderDetail(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True
