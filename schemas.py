from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    phone: str
    name: Optional[str] = None

class UserUpdate(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None

class ConversationState(BaseModel):
    menu_selected: bool = False
    operation: Optional[str] = None
    client_selected: Optional[bool] = False
    selected_client: Optional[str] = None
    products_selected: Optional[bool] = False
    order_confirmed: Optional[bool] = False
    selected_products: Optional[str] = None
    delivery_date: Optional[str] = None
    delivery_time: Optional[str] = None

class OrderCreate(BaseModel):
    client_id: str
    order_date: str
    delivery_date: Optional[str] = None
    delivery_time: Optional[str] = None
    location: Optional[str] = None

class OrderDetailCreate(BaseModel):
    order_id: str
    product_id: str
    quantity: int
