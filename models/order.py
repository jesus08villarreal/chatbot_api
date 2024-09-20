from pydantic import BaseModel, Field
from typing import List, Optional

class OrderDetail(BaseModel):
    product_id: str
    quantity: int

class Order(BaseModel):
    id: Optional[str]
    client_id: str
    company_id: str
    order_date: str
    delivery_date: str
    delivery_time: str
    location: str
    products: List[OrderDetail]
    confirmation_status: str