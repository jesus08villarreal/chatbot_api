from pydantic import BaseModel
from typing import Optional

class ClientBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    named_has: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    foreing_id: Optional[int] = None

class Client(ClientBase):
    id: int
    foreing_id: Optional[int] = None

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    client_id: int
    order_date: str
    delivery_date: str
    delivery_time: str
    location: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    confirmation_status: Optional[str] = None

class Order(OrderBase):
    id: int
    confirmation_status: Optional[str] = None

    class Config:
        from_attributes = True

class OrderDetailBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailUpdate(OrderDetailBase):
    pass

class OrderDetail(OrderDetailBase):
    id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    named_has: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    foreing_id: Optional[int] = None

class Product(ProductBase):
    id: int
    foreing_id: Optional[int] = None

    class Config:
        from_attributes = True

class ConversationStateBase(BaseModel):
    from_number: str
    menu_selected: bool = False
    operation: Optional[str] = None
    client_selected: bool = False
    selected_client: Optional[int] = None
    products_selected: bool = False
    order_confirmed: bool = False
    selected_products: Optional[str] = None
    delivery_date: Optional[str] = None
    delivery_time: Optional[str] = None

class ConversationStateCreate(ConversationStateBase):
    pass

class ConversationStateUpdate(ConversationStateBase):
    pass

class ConversationState(ConversationStateBase):
    id: int

    class Config:
        from_attributes = True